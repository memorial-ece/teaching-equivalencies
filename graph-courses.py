#!/usr/bin/env python

import argparse
import calendar as cal
import collections
import sys
import csv
import re
import operator
from ConvertParse import *
reload(sys)
sys.setdefaultencoding('utf-8')


args = argparse.ArgumentParser()
args.add_argument('filename', nargs = '+')
args.add_argument('-o', '--output', default = '-')

args = args.parse_args()
output = sys.stdout if args.output == '-' else open(args.output, 'w')


courses = collections.defaultdict(list)
list_course= collections.defaultdict(dict)
dict_gen=collections.defaultdict(dict)
dict_view_gen=collections.defaultdict(dict)

for filename in args.filename:
	p1 = re.compile(r"(\d+\b)(?!.*\1\b)")
	filen2 = int(''.join(p1.findall(str(filename))))
	html = filename.endswith('.htm') or filename.endswith('.html')
	parse = cal.parseHTML if html else cal.parseText
	for (name,c) in parse(open(filename)).items():
		codex=convert_parse_course_id(name,c)
		course=obscure_refference(name,c)
		courses[filen2].append(course)

for year, cour in courses.items():
	dict_year = collections.defaultdict(dict)
	for course in cour:
		a=courses[year].index(course)
		code=course['Name']
		dict_year[year]=courses[year][a]
		list_course[code][year] = course

# print list_course
a=0
for code, details in list_course.items():
	sorted_det= sorted(details.items(), key=operator.itemgetter(0))
	year2=None
	info2=None
	peewee_check=None
	try:
		peewee_check = CourseGeneration1.select().join(Course1).where(Course1.course_num == code).order_by(CourseGeneration1.year_of_valid_generation.desc()).get()
	except:
		pass
	for keyyear in sorted_det:
		year1,info1=keyyear[0],keyyear[1]
		if peewee_check!=None:
			print 'data in table'
			pc=peewee_check
			if pc.labs!=info1['Labs'] or pc.credit_hours!=info1['Credit Hours'] or pc.lecture_hours!=info1['Lecture Hours'] or pc.title!=info1['Title'] or pc.comments!=info1['Description'] or pc.other_info!=info1['Other info'] or pc.old_course_id!=info1['OldCourseCode'] and pc.year_of_valid_generation==year1:
				print pc.old_course_id!=info1['OldCourseCode']
				print pc.course_gen_id
		else:
			if year1>year2:
				if info1!=info2:
					info2=info1
					year2=year1
					print 'clean'
					try:
						Course1.create(subject="ENGI", course_num=code)
						late_update = Course1.select().where(Course1.course_num==code).get()
						CourseGeneration1.create(labs=info1['Labs'], credit_hours=info1['Credit Hours'],
												 lecture_hours=info1['Lecture Hours'],
												 title=info1['Title'], comments=info1['Description'],
												 course_id=late_update, other_info=info1['Other info'],
												 old_course_id=info1['OldCourseCode'], year_of_valid_generation=year1,year_valid_to=year1)
					except:
						late_update = Course1.select().where(Course1.course_num==code).get()
						CourseGeneration1.create(labs=info1['Labs'],credit_hours=info1['Credit Hours'],
											 lecture_hours=info1['Lecture Hours'],
											 title=info1['Title'],comments=info1['Description'],
											 course_id=late_update,other_info=info1['Other info'],
											 old_course_id=info1['OldCourseCode'],year_of_valid_generation=year1,year_valid_to=year1)
				else:
					print'update'
					update=CourseGeneration1.update(year_valid_to=year1).where(CourseGeneration1.course_gen_id==CourseGeneration1.select().order_by(CourseGeneration1.course_gen_id.desc()).get())
					update.execute()
			else:
				year2=year1
				info2=info1
				print 'error'
