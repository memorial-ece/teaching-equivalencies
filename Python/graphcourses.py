#!/usr/bin/env python

import argparse
import calendar as cal
import collections
import sys
import csv
import random
from Class import *
from ConvertParse import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

args = argparse.ArgumentParser()
args.add_argument('filename', nargs = '+')
args.add_argument('--format', choices = [ 'calendar', 'dot' ], default = 'dot')
args.add_argument('-o', '--output', default = '-')

args = args.parse_args()
output = sys.stdout if args.output == '-' else open(args.output, 'w')


courses = collections.defaultdict(dict)


for filename in args.filename:
	f = open(filename)
	html = filename.endswith('.htm') or filename.endswith('.html')
	parse = cal.parseHTML if html else cal.parseText

	for (name,c) in parse(open(filename), prefix = 'ENGI').items():
		courses[name].update(c)

	for course in courses.values():
		if course['name'].startswith('ENGI '):
			num = str(course['number'])
			term = int(num[0])
			department = int(num[1])

dictyear={'2008':courses}

with open('dict.csv', 'wb') as csv_file:
	writer = csv.writer(csv_file)
	for key, value in courses.items():
		writer.writerow([key, value])


for name, course in courses.items():
	sem1 = open('fun').readlines()
	sem2 = random.choice(sem1)
	print sem2
	labs = convert_parse_labs(name, course)
	credit_hours = convert_parse_credit_hours(name, course)
	lecture_hours = convert_parse_lecture_hours(name, course)
	title = convert_parse_title(name, course)
	comments = convert_parse_comments(name, course)
	course_num = convert_parse_course_id(name, course)
	other_info=convert_parse_other(name,course)
	exclusive=convert_parse_exclusive(name,course)
	for course_2 in Course1.select():
		num2=course_2.course_num
		id2=course_2.course_id
		if exclusive!=None:
			if exclusive ==num2:
				try:
					Course1.create(subject="ENGI", course_num=course_num)
					late_update = Course1.select().order_by(Course1.course_id.desc()).get()
					CourseGeneration1.create(labs=labs, credit_hours=credit_hours, lecture_hours=lecture_hours,
											 title=title, comments=comments,
											 course_id=late_update, useable=True, other_info=other_info,
											 old_course_id=id2)
				except:
					pass
	try:
		Course1.create(subject="ENGI", course_num=course_num)
		late_update = Course1.select().order_by(Course1.course_id.desc()).get()
		CourseGeneration1.create(labs=labs, credit_hours=credit_hours, lecture_hours=lecture_hours, title=title, comments=comments,
			 course_id=late_update,useable=True,other_info=other_info,old_course_id=exclusive)
	except:
		pass
	for course_1 in Course1.select():
		id1=course_1.course_id
		num1=course_1.course_num
		if exclusive==num1:
			qaq = CourseGeneration1.update(useable=False).where(CourseGeneration1.course_id == id1)
			qaq.execute()
		if course_num==num1 :
			for y in CourseGeneration1.select():
				id2=(y.course_id)
				com=(y.comments)
				titl=str(y.title)
				chou=str(y.credit_hours)
				lab=str(y.labs)
				boo=y.useable
				if boo:
					if id1==id2.course_id:
						if exclusive==None:
							if com!=comments or titl!=title or (y.lecture_hours)!=lecture_hours or chou!=credit_hours or lab!=labs and boo:
								qqq=CourseGeneration1.update(useable=False).where(CourseGeneration1.course_id==id1)
								qqq.execute()
								CourseGeneration1.create(labs=labs, credit_hours=credit_hours, lecture_hours=lecture_hours, title=title,
									 comments=comments, course_id=id2.course_id,useable=True,other_info=other_info,old_course_id=exclusive)
						elif exclusive==num1:
							exclusive=id1
							if com!=comments or titl!=title or (y.lecture_hours)!=lecture_hours or chou!=credit_hours or lab!=labs and boo:
								qqq=CourseGeneration1.update(useable=False).where(CourseGeneration1.course_id==id1)
								qqq.execute()
								CourseGeneration1.create(labs=labs, credit_hours=credit_hours, lecture_hours=lecture_hours, title=title,
									 comments=comments, course_id=id2.course_id,useable=True,other_info=other_info,old_course_id=exclusive)
