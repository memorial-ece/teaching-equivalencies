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

import collections
import reader as calendar

from ConvertParse import sanitize_course

from Core import *
import operator
from db import *


def import_courses(filenames):
    file_count = len(filenames)
    print('Parsing %d calendar files...' % file_count)

    # Parse each (annual) calendar's description of every course.
    courses_by_year = collections.defaultdict(list)

    for (i, filename) in enumerate(filenames):
        progress(i, file_count)

        year = int(re.findall(r'\d{4}', filename)[-1])

        for (name, c) in calendar.parseHTML(open(filename)).items():
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

        course, created = Course.get_or_create(subject = subject, code = code)
        gen = None

        for year in sorted(details_by_year.keys()):
            details = details_by_year[year]

            # Is this the first time we've seen this course description?
            if gen is None or gen.differs_from(details):
                gen = CourseGeneration.create(
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

