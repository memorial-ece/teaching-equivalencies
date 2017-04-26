#  Copyright 2017 Keegan Joseph Brophy
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import collections
from Core import *
import operator
import reader as cal
from db import *
from ConvertParse import *


def import_courses(filename_import):
    courses = collections.defaultdict(list)
    for filename in filename_import:
        parser1 = re.compile(r"\d+\D\w+$")
        filename_year_subsection = (''.join(parser1.findall(str(filename))))
        filename_year_subsection = filename_year_subsection.strip("'.html'")
        parse = cal.parseHTML
        for (name, c) in parse(open(filename)).items():
            course = sanitize_course(name, c)
            courses[filename_year_subsection].append(course)
    list_course = collections.defaultdict(dict)
    for year, cour in courses.items():
        for course in cour:
            code = course['Name']
            list_course[code][year] = course
    progress_counter = 0
    for code, details in list_course.items():
        progress_counter += 1
        try:
            progress(progress_counter, len(list_course))
        except:
            pass
        sorted_det = sorted(details.items(), key=operator.itemgetter(0))
        lastyear = None
        info2 = None
        peewee_check = None
        for keyyear in sorted_det:
            thisyear, info1 = keyyear[0], keyyear[1]
            var1 = re.compile(r"....")
            thisyear = str(var1.findall(str(thisyear)))
            thisyear = thisyear.strip("'[]")
            try:
                peewee_check = CourseGeneration.select()\
                    .join(Course).where(Course.code == code, CourseGeneration.start_year == thisyear).get()
            except:
                pass
            if peewee_check is not None:
                print 'if you see this no data should update'
                info2 = info1
                lastyear = thisyear
                pc = peewee_check
                if pc.labs != info1['Labs'] or pc.credit_hours != info1['Credit Hours'] \
                        or pc.lecture_hours != info1['Lecture Hours'] or pc.title != info1['Title'] \
                        or pc.comments != info1['Description'] or pc.other_info != info1['Other info'] \
                        or pc.previous_course_id != info1['PreviousCourseCode']:
                    if pc.start_year == thisyear:
                        late_update = Course.select().where(Course.code == code).get()
                        CourseGeneration.update(labs=info1['Labs'], credit_hours=info1['Credit Hours'],
                                                lecture_hours=info1['Lecture Hours'],
                                                title=info1['Title'], comments=info1['Description'],
                                                course=late_update, other_info=info1['Other info'],
                                                previous_course=info1['PreviousCourseCode'], start_year=thisyear,
                                                end_year=thisyear,reviewed=False) \
                            .where(CourseGeneration.id == pc.id)
                elif info1 != info2 and thisyear > pc.end_year:
                    info2 = info1
                    lastyear = thisyear
                    late_update = Course.select().where(Course.code == code).get()
                    CourseGeneration.create(labs=info1['Labs'], credit_hours=info1['Credit Hours'],
                                            lecture_hours=info1['Lecture Hours'],
                                            title=info1['Title'], comments=info1['Description'],
                                            course=late_update, other_info=info1['Other info'],
                                            previous_course=info1['PreviousCourseCode'], start_year=thisyear,
                                            end_year=thisyear,reviewed=False)
                elif info1 == info2 and thisyear > pc.end_year:
                    update = CourseGeneration.update(end_year=thisyear).where(
                        CourseGeneration.id == pc.id)
                    update.execute()
            else:
                if thisyear > lastyear:
                    if info1 != info2:
                        info2 = info1
                        lastyear = thisyear
                        try:
                            Course.get_or_create(subject=info1['Subject'], code=code,reviewed=False)
                            late_update = Course.select().where(Course.code == code).get()
                            CourseGeneration.create(labs=info1['Labs'], credit_hours=info1['Credit Hours'],
                                                    lecture_hours=info1['Lecture Hours'],
                                                    title=info1['Title'], comments=info1['Description'],
                                                    course=late_update, other_info=info1['Other info'],
                                                    previous_course=info1['PreviousCourseCode'], start_year=thisyear,
                                                    end_year=thisyear,reviewed=False)
                        except:
                            late_update = Course.select().where(Course.code == code).get()
                            CourseGeneration.create(labs=info1['Labs'], credit_hours=info1['Credit Hours'],
                                                    lecture_hours=info1['Lecture Hours'], title=info1['Title'],
                                                    comments=info1['Description'], course=late_update,
                                                    other_info=info1['Other info'],
                                                    previous_course=info1['PreviousCourseCode'],
                                                    start_year=thisyear, end_year=thisyear,reviewed=False)
                    else:
                        update = CourseGeneration.update(end_year=thisyear).where(
                            CourseGeneration.id == CourseGeneration.select().order_by(
                                CourseGeneration.id.desc()).get())
                        update.execute()
    print
