# Copyright 2017 Keegan Joseph Brophy
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

import re


# noinspection PyUnboundLocalVariable
def convert_parse_labs(name, course):
    labs = course['lab hours'] if 'lab hours' in course else 3
    if labs == 'at least three 1.5-hour sessions per semester':
        l4 = 4.5
    if labs == 'scheduled as required':
        l4 = 0
    p = re.compile(r"(\w+) (\d+)")
    p1 = re.compile(r"(\d+)")
    p2 = re.compile(r"([a-z]+)")
    lab = str(labs)
    l = p.findall(lab)
    l1 = str(l)
    a1 = p2.findall(l1)
    a2 = p1.findall(lab)
    l2 = ''.join(map(str, a2))
    l3 = ''.join(map(str, a1))
    if l3 == 'one':
        a = 1
    elif l3 == 'two':
        a = 2
    elif l3 == 'three':
        a = 3
    elif l3 == 'four':
        a = 4
    elif l3 == 'five':
        a = 5
    elif l3 == 'six':
        a = 6
    elif l3 == 'seven':
        a = 7
    elif l3 == 'eight':
        a = 8
    elif l3 == 'nine':
        a = 9
    elif l3 == 'ten':
        a = 10
    elif l3 == 'eleven':
        a = 11
    elif l3 == 'twelve':
        a = 12
    elif l3 == 'thirteen':
        a = 13
    else:
        a = 3
    a_1 = int(a)
    if l2 == '':
        l2 = 0
    l2_1 = int(l2)
    tot = l2_1 * a_1
    if tot == 0:
        tot = 0
    try:
        if l4 is not None:
            tot = l4
            tot = str(tot)
            return tot
    except:
        tot = str(tot)
        return tot


def convert_parse_credit_hours(name, course):
    credit_hours = course['credit-hours'] if 'credit-hours' in course else 0
    credit_hours1 = str(credit_hours)
    return credit_hours1


def convert_parse_lecture_hours(name, course):
    lecture_hours = course['lecture hours'] if 'lecture hours' in course else 0
    if lecture_hours == 'at least 10 lecture hours per semester':
        lecture_hours = 10
    if lecture_hours == 'at least 15 lecture hours per semester':
        lecture_hours = 15
    if lecture_hours == 'scheduled as required':
        lecture_hours = 3
    if lecture_hours == 'at least 25 lecture hours per semester':
        lecture_hours = 25
    lecture_hours1 = str(lecture_hours)
    return lecture_hours1


def convert_parse_title(name, course):
    title = course['title'] if 'title' in course else None
    return title


def convert_parse_comments(name, course):
    comments = course['description'] if 'description' in course else None
    return comments


def convert_parse_course_id(name, course):
    course_id1 = course['number'] if 'number' in course else None
    p1 = re.compile(r"(\d+\-\d+)")
    course_id2 = ''.join(p1.findall(course_id1))
    if course_id2=='':
        return course_id1
    else:
        p2 = re.compile(r"(\d+)")
        course_id4 = p2.findall(course_id2)
        return course_id4[0]

def convert_parse_name(name, course):
    p2 = re.compile(r"([A-Z]{4})")
    name1 = str(name)
    sub = p2.findall(name1)
    subject = ''.join(map(str,sub))
    return subject

def convert_parse_other(name, course):
    other = course['other information'] if 'other information' in course else None
    return other


def convert_parse_exclusive(name, course):
    prefix = convert_parse_name(name, course)
    exclusive = course['exclusive with'] if 'exclusive with' in course else None
    if exclusive is not None:
        p = re.compile(r"\d+")
        exc = str(exclusive)
        excl = p.findall(exc)
        excl1 = ''.join(map(str, excl))
        if exclusive == ('the former '+prefix+' '+ excl1):
            exclusive = excl1
        else:
            exclusive = None
    return exclusive


def sanitize_course(name, course):
    labs = convert_parse_labs(name, course)
    id = convert_parse_course_id(name, course)
    credit_hours = convert_parse_credit_hours(name, course)
    lecture_hours = convert_parse_lecture_hours(name, course)
    title = (convert_parse_title(name, course))
    comments = convert_parse_comments(name, course)
    other_info = convert_parse_other(name, course)
    exclusive = convert_parse_exclusive(name, course)
    subject = convert_parse_name(name, course)
    dict_course_gen = {'Subject': subject, 'Name': id, 'PreviousCourseCode': exclusive, 'Description': comments, 'Title': title,
                       'Lecture Hours': lecture_hours, 'Credit Hours': credit_hours, 'Labs': labs,
                       'Other info': other_info}
    return dict_course_gen
