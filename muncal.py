# Copyright 2014, 2017 Jonathan Anderson
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
from bs4 import BeautifulSoup

course_number = re.compile('[0-9W]{4} [A-Z][a-z]+')
numeric = re.compile('^[0-9]+$')
special_topics = re.compile('[0-9]{4}-[0-9]{4} [A-Z][a-z]+')
prefix=None


def parse_prerequisites(s, prefix):
    prereqs = []
    for x in s.split(' or '):
        for y in x.split(','):
            y = y.strip()

            if y.startswith('permission of'):
                continue

            prereqs += [prefix + ' ' + y if numeric.match(y) else y]

    return prereqs


_ = lambda x, _: x
codes = {
    'AR': ('attendance', _, _),
    'CH': ('credit-hours', lambda x, _: int(x), _),
    'CO': ('co-requisite', _, _),
    'CR': ('exclusive with', _, _),
    'LC': ('lecture hours', _, _),
    'LH': ('lab hours', _, _),
    'OR': ('other information', _, _),
    'PR': ('prerequisites', parse_prerequisites, lambda xs: ', '.join(xs)),
    'UL': ('limitations', _, _),
}


def parseHTML(calfile):
    courses = {}
    soup = BeautifulSoup(calfile, 'html.parser')
    subj = str(soup.find('br'))
    if subj=='<br/>':
        subj = str(soup.find("div", {"id": "printtitle"}))
        p = re.compile(r"(\w+\s)")
        subj = p.findall(subj)
        prefix1 = subj[6]
        if prefix1=='Engineering ':
            prefix = 'ENGI'
        if prefix1 == 'Business ':
            prefix = 'BUSI'
        if prefix1 == 'Human ':
            prefix = 'HKR '
        if prefix1 == 'Education  ':
            prefix = 'ED  '
    subj = str(subj)
    p= re.compile(r"(\w+\s)")
    subj = p.findall(subj)
    try:
        if subj[2]=='Business ':
            prefix='BUSI'
        if subj[2]=='Engineering ':
            prefix='ENGI'
        if subj[2]=='Human ':
            prefix='HKR '
        if subj[2]=='Education  ':
            prefix='ED  '
    except:
        pass
    for block in soup.find_all(class_='CourseBlock'):
        for c in block.find_all(class_='course'):
            number = c.find(class_='courseNumber').string.strip()
            name = '%s %s' % (prefix, number)
            title = c.find(class_='courseTitle').string.strip()
            description = ''.join([
                d.string.strip()
                    for d in c.find(class_='courseDesc').p
                    if d.string is not None
            ])
            if 'inactive course' in description:
                continue
            course = {
                'credit-hours': 3,
                'description': description,
                'lecture hours': 3,
                'name': name,
                'number': number,
                'title': title,
            }
            courses[name] = course
            for attr in c.find_all(class_='courseAttrs'):
                content = ' '.join([
                    a.string.strip()
                        for a in attr
                        if a.string is not None
                ])
                parts = content.split(':')
                key = parts[0]
                value = parts[-1].strip()

                (name, parse, reformat) = codes[key]
                course[name] = parse(value, prefix)
    return courses


def format(courses, output):
    for course in sorted(courses.values(), key=lambda c: c['number']):
        output.write('%d %s\n' % (course['number'], course['description']))

        for (code, (name, parse, reformat)) in sorted(codes.items()):
            if name in course:
                output.write('\t%s: %s\n' % (code, reformat(course[name])))

