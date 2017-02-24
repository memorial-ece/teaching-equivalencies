#!/usr/bin/env python

import argparse
import calendar as cal
import collections
import sys
import csv
from Class import *
import numpy as np
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
	print course.keys()
	print course['number']
	print course['name']
	if course['number']=='8801-8805 (Excluding 8804)':
		cc = Course1()
		g = CourseGeneration1()
		labs = course['lab hours'] if 'lab hours' in course else None
		credit_hours = course['credit-hours'] if 'credit-hours' in course else None
		lecture_hours = course['lecture hours'] if 'lecture hours' in course else None
		title = course['title'] if 'title' in course else None
		comments = course['description'] if 'description' in course else None
		course_id = course['number'] if 'number' in course else None
		subject = 'ENGR'
		course_num = '8001-8805'
		print "there"
		# if (for x in cc.select())!=None:
		# for x in cc.select():
		# 	c=x.course_id
		# 	a=x.course_num
		# 	b=x.subject
		# 	arb=[a]
		# 	if course_num==a and subject==b:
		# 		for y in g.select():
		# 			d=y.course_id
		# 			e=y.comments
		# 			f=y.title
		# 			h=y.lecture_hours
		# 			i=y.credit_hours
		# 			j=y.labs
		# 			if c==d:
		# 				if d!=course_id or e!=comments or f!=title or h!=lecture_hours or i!=credit_hours or j!=labs:
		# 					g.create(labs=labs, credit_hours=credit_hours, lecture_hours=lecture_hours, title=title,
		# 						 comments=comments, course_id=b)
		# 					print 'aaaaaaaaaaaaaaaaaaa'
		# else:
		# cc.create(subject=subject, course_num=course_num)
		# b= Course1.select().order_by(Course1.course_id.desc()).get()
		# g.create(labs=labs,credit_hours=credit_hours,lecture_hours=lecture_hours,title=title,comments=comments,course_id=b)

	else:
		cc=Course1()
		g=CourseGeneration1()
		labs = course['lab hours'] if 'lab hours' in course else None
		if labs=='at least 9 hours per semester':
			labs='9'
		if labs=='at least 12 hours per semester':
			labs='12'
		if labs=='at least ten 2-hour sessions per semester':
			labs='20'
		if labs=='at least five 3-hour sessions per semester':
			labs='15'
		if labs=='at least three 1-hour sessions per semester':
			labs='3'
		if labs=='at least one 4-hour session per semester':
			labs='4'
		if labs=='at least four 2-hour sessions per semester':
			labs='8'
		if labs=='at least eight 1-hour sessions per semester':
			labs='8'
		if labs=='at least four 3-hour sessions per semester':
			labs='12'
		if labs=='at least ten 3-hour sessions per semester':
			labs='30'
		if labs=='at least three 3-hour sessions per semester':
			labs='9'
		if labs=='at least six 3-hour laboratory sessions per semester':
			labs='18'
		if labs=='at least four 3-hour sessions per term':
			labs='12'
		if labs=='at least nine 2-hour sessions per semester':
			labs='18'
		if labs=='at least eight 3-hour sessions per semester':
			labs='24'
		if labs=='at least eight 2-hour sessions per semester':
			labs='16'
		if labs=='at least one 3-hour session per semester':
			labs='3'
		if labs=='at least 6 hours per semester':
			labs='6'
		if labs=='at least two 2-hour sessions per semester':
			labs='4'
		if labs=='at least six 3-hour sessions per semester':
			labs='18'
		if labs=='at least four 1-hour sessions per semester':
			labs='4'
		if labs=='scheduled as required':
			labs='3'
		if labs=='at least four 3-hour sessions per semester.':
			labs='12'
		if labs=='at least five 1-hour sessions per semester':
			labs='5'
		if labs=='at least ten 3-hour lab sessions per semester':
			labs='10'
		if labs=='at least 20 hours per semester':
			labs='20'
		if labs=='at least nine 3-hour sessions per semester':
			labs='27'
		if labs=='at least three 1.5-hour sessions per semester':
			labs='4.5'
		if labs=='at least nine 3-hour laboratory sessions per semester':
			labs='27'
		credit_hours = course['credit-hours'] if 'credit-hours' in course else None
		lecture_hours = course['lecture hours'] if 'lecture hours' in course else None
		if lecture_hours == 'at least 10 lecture hours per semester':
			lecture_hours="10"
		if lecture_hours == 'at least 15 lecture hours per semester':
			lecture_hours="15"
		if lecture_hours == 'scheduled as required':
				lecture_hours = "3"
		title = course['title'] if 'title' in course else None
		comments = course['description'] if 'description' in course else None
		course_id = course['number'] if 'number' in course else None
		(subject, course_num)=name.split()
		for x in cc.select():
			c=x.course_id
			a=x.course_num
			b=x.subject
			if course_num==a and subject==b:
				for y in g.select():
					d=y.course_id
					e=y.comments
					f=y.title
					h=y.lecture_hours
					i=y.credit_hours
					j=y.labs
					print"anderson look below me or above me but i am the cuting point"
					print d.course_id
					print ''
					print c
					if c==d.course_id:
						print 'lol'
						fixer1=str(h).strip()
						fixer2=str(course_num).strip()
						print fixer1==fixer2

						if   e!=comments or f!=title or h!=lecture_hours or i!=credit_hours or j!=labs:
							# g.create(labs=labs, credit_hours=credit_hours, lecture_hours=lecture_hours, title=title,
						# 		 comments=comments, course_id=d.course_id)
							print 'aaaaaaaaaaaaaaaaaaa'
							print h!=lecture_hours
							print h
							print lecture_hours
							print i!=credit_hours





		# cc.create(subject=subject, course_num=course_num)
		# b= Course1.select().order_by(Course1.course_id.desc()).get()
		# g.create(labs=labs,credit_hours=credit_hours,lecture_hours=lecture_hours,title=title,comments=comments,course_id=b)
