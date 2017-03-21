#!/usr/bin/env python

import argparse
import collections
import operator
import reader as cal
from Class import *
from ConvertParse import *

args = argparse.ArgumentParser()
args.add_argument('filename', nargs='+')
args = args.parse_args()
courses = collections.defaultdict(list)
for filename in args.filename:
	p1 = re.compile(r"(\d+\b)(?!.*\1\b)")
	filen2 = int(''.join(p1.findall(str(filename))))
	html = filename.endswith('.htm') or filename.endswith('.html')
	parse = cal.parseHTML if html else cal.parseText
	for (name, c) in parse(open(filename)).items():
		codex = convert_parse_course_id(name, c)
		course = sanitize_course(name, c)
		courses[filen2].append(course)


list_course = collections.defaultdict(dict)
for year, cour in courses.items():
	dict_year = collections.defaultdict(dict)
	for course in cour:
		var1 = courses[year].index(course)
		code = course['Name']
		dict_year[year] = courses[year][var1]
		list_course[code][year] = course


Progress_counter=0
for code, details in list_course.items():
	Progress_counter+=1
	sorted_det = sorted(details.items(), key=operator.itemgetter(0))
	year2 = None
	info2 = None
	peewee_check = None
	print Progress_counter
	for keyyear in sorted_det:
		Progress_counter+=1
		year1, info1 = keyyear[0], keyyear[1]
		var1=re.compile(r"....")
		year1=str(var1.findall(str(year1)))
		year1=year1.strip("'[]")
		try:
			peewee_check = CourseGeneration.select()\
				.join(Course).where(Course.code == code,CourseGeneration.start_year == year1).get()
		except:
			pass
		if peewee_check is not None:
			print 'if you see this then incorrect data was entered, no data should update'
			info2 = info1
			year2 = year1
			pc = peewee_check
			if pc.labs != info1['Labs'] or pc.credit_hours != info1['Credit Hours'] \
					or pc.lecture_hours != info1['Lecture Hours'] or pc.title != info1['Title'] \
					or pc.comments != info1['Description'] or pc.other_info != info1['Other info'] \
					or pc.previous_course_id != info1['PreviousCourseCode']:
				if pc.start_year == year1:
					late_update = Course.select().where(Course.code == code).get()
					CourseGeneration.update(labs=info1['Labs'], credit_hours=info1['Credit Hours'],
											lecture_hours=info1['Lecture Hours'],
											title=info1['Title'], comments=info1['Description'],
											course=late_update, other_info=info1['Other info'],
											previous_course=info1['PreviousCourseCode'], start_year=year1,
											end_year=year1) \
						.where(CourseGeneration.id == pc.id)
			elif info1 != info2 and year1 > pc.end_year:
				info2 = info1
				year2 = year1
				late_update = Course.select().where(Course.code == code).get()
				CourseGeneration.create(labs=info1['Labs'], credit_hours=info1['Credit Hours'],
										lecture_hours=info1['Lecture Hours'],
										title=info1['Title'], comments=info1['Description'],
										course=late_update, other_info=info1['Other info'],
										previous_course=info1['PreviousCourseCode'], start_year=year1,
										end_year=year1)
			elif info1 == info2 and year1 > pc.end_year:
				update = CourseGeneration.update(end_year=year1).where(
					CourseGeneration.id == pc.id)
				update.execute()
		else:
			print Progress_counter
			if year1 > year2:
				if info1 != info2:
					info2 = info1
					year2 = year1
					try:
						Course.get_or_create(subject=info1['Subject'], code=code)
						late_update = Course.select().where(Course.code == code).get()
						CourseGeneration.create(labs=info1['Labs'], credit_hours=info1['Credit Hours'],
												lecture_hours=info1['Lecture Hours'],
												title=info1['Title'], comments=info1['Description'],
												course=late_update, other_info=info1['Other info'],
												previous_course=info1['PreviousCourseCode'], start_year=year1,
												end_year=year1)
						print 'ive done something new'
					except:
						late_update = Course.select().where(Course.code == code).get()
						CourseGeneration.create(labs=info1['Labs'], credit_hours=info1['Credit Hours'],
												lecture_hours=info1['Lecture Hours'],
												title=info1['Title'], comments=info1['Description'],
												course=late_update, other_info=info1['Other info'],
												previous_course=info1['PreviousCourseCode'], start_year=year1,
												end_year=year1)
						print 'ive created new things'
				else:
					update = CourseGeneration.update(end_year=year1).where(
						CourseGeneration.id == CourseGeneration.select().order_by(
							CourseGeneration.id.desc()).get())
					update.execute()
					print 'ive updated things'