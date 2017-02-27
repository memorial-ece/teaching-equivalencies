#!/usr/bin/env python

import argparse
import calendar as cal
import collections
import sys
import csv
from Class import *
from ConvertParse import *
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
	cc = Course1()
	g = CourseGeneration1()
	print course.keys()
	length=len(courses)
	labs = convert_parse_labs(name, course)
	credit_hours = convert_parse_credit_hours(name, course)
	lecture_hours = convert_parse_lecture_hours(name, course)
	title = convert_parse_title(name, course)
	comments = convert_parse_comments(name, course)
	course_num = convert_parse_course_id(name, course)
	try:
		cc.create(subject="ENGI", course_num=course_num)
		b = Course1.select().order_by(Course1.course_id.desc()).get()
		g.create(labs=labs, credit_hours=credit_hours, lecture_hours=lecture_hours, title=title, comments=comments,
			 course_id=b,useable=True)
	except:
		pass
	for x in cc.select():
		c=x.course_id
		a=x.course_num
		if course_num==a :
			for y in g.select():
				d=(y.course_id)
				e=(y.comments)
				f=str(y.title)
				h=str(y.lecture_hours)
				i=str(y.credit_hours)
				j=str(y.labs)
				k=y.useable
				if k:
					if c==d.course_id:
						if   e!=comments or f!=title or (y.lecture_hours)!=lecture_hours or i!=credit_hours or j!=labs and k:

							qqq=CourseGeneration1.update(useable=False).where(CourseGeneration1.course_id==c)
							qqq.execute()
							g.create(labs=labs, credit_hours=credit_hours, lecture_hours=lecture_hours, title=title,
								 comments=comments, course_id=d.course_id,useable=True)
