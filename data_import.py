# Copyright 2017 Jonathan Anderson
# Copyright 2017 Keegan Joseph Brophy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import bs4
import collections
import db
import itertools
import muncal
import re
import sys

from ConvertParse import sanitize_course
from Core import progress


def import_courses(filenames):
    """
    Import descriptions of courses from the online Calendar.

    The Calendar has a number of "Coruse Descriptions" pages that include
    course codes, names, descriptions and details like lecture hours,
    credit-hours, etc. This function uses calendar-parsing code derived from
    https://github.com/trombonehero/memorial-calendar to import all of the
    course descriptions in a set of HTML files and organize them into
    db.Course and db.CourseGeneration objects.
    """

    file_count = len(filenames)
    print('Parsing %d calendar files...' % file_count)

    # Parse each (annual) calendar's description of every course.
    courses_by_year = collections.defaultdict(list)

    for (i, filename) in enumerate(filenames):
        progress(i, file_count)

        year = int(re.findall(r'\d{4}', filename)[-1])

        for (name, c) in muncal.parseHTML(open(filename)).items():
            course = sanitize_course(name, c)
            courses_by_year[year].append(course)

    progress(1, 1)
    print('\n')

    # Arrange courses by course code (e.g., ENGI 200W) and then by year.
    courses = collections.defaultdict(dict)
    for (i, (year, year_courses)) in enumerate(courses_by_year.items()):
        for course in year_courses:
            subject = course['Subject']
            code = course['Name']
            courses[(subject, code)][year] = course

    # For each course, identify homogeneous "generations".
    #
    # For example, if a course was introduced in 2010 and modified in 2013,
    # the calendar descriptions in 2010, 2011 and 2012 will be identical but
    # the description in 2013 will be different. We need to effectively
    # reverse-engineer the calendar change process, resulting in a
    # 2010-2012 generation and a 2013-??? generation.
    course_count = len(courses)
    print('Identifying generations of %d courses...' % course_count)
    for (i, ((subject, code), details_by_year)) in enumerate(courses.items()):
        progress(i, course_count)

        course, created = db.Course.get_or_create(subject = subject, code = code)
        gen = None

        for year in sorted(details_by_year.keys()):
            details = details_by_year[year]

            # Is this the first time we've seen this course description?
            if gen is None or gen.differs_from(details):
                gen = db.CourseGeneration.create(
                    course = course,
                    labs = details['Labs'],
                    credit_hours = details['Credit Hours'],
                    lecture_hours = details['Lecture Hours'],
                    title = details['Title'],
                    comments = details['Description'],
                    other_info = details['Other info'],
                    previous_course = details['PreviousCourseCode'],
                    start_year = year,
                    end_year = year)

            # Otherwise, it's another year of the same thing.
            else:
                gen.end_year = year
                gen.save()

    progress(1, 1)
    print('\n')


def import_offerings(files):
    file_count = len(files)
    print('Importing offering data from %d files...' % file_count)

    crosslist = re.compile(r"(?<=CROSS LISTED)(\W)")
    term_details = re.compile(r"Course Offerings: ([0-9]+)-[0-9]+ ([A-Za-z]+)")
    section_line = re.compile(r'^([A-Z]+) ([A-Z0-9]+) ([^0-9]+) ([0-9]{3}) ([0-9]{5}) ')
    instructor_name = re.compile(r'Primary - (.*)$')

    for (i, filename) in enumerate(files):
        progress(i, file_count)

        # Parse the year and session from the HTML at the top of the file,
        # before we enter the Big Blob of Text.
        soup = bs4.BeautifulSoup(open(filename, 'r'), 'html.parser')
        if soup.body is None:
            sys.stderr.write('error: %s has no HTML body\n' % filename)
            continue

        ((year, session),) = term_details.findall(soup.body.h2.text)
        year = int(year)
        session = db.Session.get(name = session)
        term, _ = db.Semester.get_or_create(year = year, session = session)

        # Parse the raw text in the remainder of the file.
        #
        # This big blob of text is stateful in that multiple sections of the
        # same course offering are grouped together, so we ened to keep track
        # of what the "current offering" is.
        offering = None

        for (lineno, line) in enumerate(open(filename, 'r')):
            # The lines we care about all contain sections and CRNs (xxx yyyy):
            match = section_line.findall(line)
            if len(match) == 0:
                continue

            ((subject, code, title, section, crn),) = match
            section = int(section)
            crn = int(crn)

            # Parse instructor names, e.g., "A Aliceson     B Bobson"
            instructors = instructor_name.findall(line)
            if len(instructors) == 0 or instructors[0].strip() == 'm munprod':
                continue

            instructors = instructors[0].split()
            a = iter(instructors)
            instructors = set(itertools.izip(a, a))

            # If the line starts right at the beginning with no spaces,
            # it's the first section of the course being described.
            # We need to find the course and the correct course generation,
            # create a new Offering and link the instructor(s) to it.
            if not line.startswith(' '):
                offering = create_offering(subject, code, title, term)

                for instructor in instructors:
                    (initial, surname) = instructor
                    candidates = db.Person.select().where(
                        db.Person.name.startswith(initial),
                        db.Person.name.endswith(surname)
                    )

                    if candidates.count() == 0:
                        sys.stderr.write(
                                "%s:%d: error: no such instructor: %s %s\n" % (
                                    filename, lineno, initial, surname))
                        sys.stderr.write('  Course:         %s\n' %
                                offering.course)
                        sys.stderr.write('  Offering:       %s\n' %
                                offering.semester)
                        sys.stderr.write('  Instructor(s):  %s\n' %
                                ', '.join([ '%s %s' % i for i in instructors ]))
                        continue

                    print(list(candidates))

            # Otherwise (i.e., if this isn't the first section), we just need
            # to increment the section count for the existing offering data.
            else:
                assert offering is not None
                offering.sections += 1
                offering.save()


def create_offering(subject, code, title, term):
    """
    Create a new Offering for a specific course in a specific term,
    creating the Course itself and a CourseGeneration if need be.
    """

    # Find the course being offered or, if it doesn't exist in the calendar
    # (e.g., a new or Special Topics course), create it.
    try:
        course = db.Course.get(subject = subject, code = code)

    except db.Course.DoesNotExist:
        course = db.Course.create(subject = subject, code = code)

    # Similarly, try to find a matching CourseGeneration, but if there isn't one
    # (as in new or Special Topics course), create one.
    try:
        gen = db.CourseGeneration.get(
            db.CourseGeneration.start_year <= term.year,
            db.CourseGeneration.end_year >= term.year,
            course = course
        )

    except db.CourseGeneration.DoesNotExist:
        gen = db.CourseGeneration.create(
            course = course,
            title = title,
            start_year = term.year,
            end_year = term.year
        )

    # Finally, create the new Offering.
    return db.Offering.create(
            course = course,
            semester = term,
            generation = gen,
    )
