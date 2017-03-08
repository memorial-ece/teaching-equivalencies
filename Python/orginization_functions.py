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
from Class import *
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def informationXchange(generation,list1):
	first_run_var=1
	for x in generation:
		a = x.labs
		b = x.credit_hours
		c = x.lecture_hours
		d = x.title
		e = x.comments
		f = x.course_id
		g = x.other_info
		h = x.old_course_id
		if first_run_var == 1:
			aa = a
			ab = b
			ac = c
			ad = d
			ae = e
			af = f
			ag = g
			ah = h
			first_run_var = 2
		else:
			i = str(x.id)
			if aa != a:
				list1.append(i + ':' + 'labs')
				aa = a
			if ab != b:
				list1.append(i + ':' + 'credithours')
				ab = b
				print'b'
			if ac != c:
				list1.append(i + ':' + 'lecturehours')
				ac = c
				print'c'
			if ad != d:
				list1.append(i + ':' + 'title')
				ad = d
				print'd'
			if ae != e:
				list1.append(i + ':' + 'comments')
				ae = e
				print'e'
			if af != f:
				list1.append(i + ':' + 'courseid')
				af = f
				print'f'
			if ag != g:
				list1.append(i + ':' + 'other info')
				ag = g
				print'g'
			if ah != h:
				ah = str(ah)
				print ah
				list1.append(i + ':' + 'old id')
				ah = h
	return list1


def gen_offering():
	now = str(datetime.datetime.now())
	year= now.split()
	p=re.compile(r"\d+")
	year=p.findall(year[0])
	if year[1]>=8:
		year=int(year[0])-1
	offering = CourseGeneration.select().where(CourseGeneration.year_of_valid_generation==year)
	for x in offering:
		for y in Term.select().where(Term.year==year):

			Offering.create(semester_id=y.session,course_gen_id=x.id)


def semester_quick_gen():
	now = str(datetime.datetime.now())
	year= now.split()
	p=re.compile(r"\d+")
	year=p.findall(year[0])
	start=2007
	while int(start)<=int(year[0]):
		print year[0]
		print start
		session=0
		while session!=5:
			session+=1
			try:
				Term.create_or_get(year=start,session=session)
			except:
				pass
			print session
		else:
			start+=1
		if start == 2020:
			break

def offer():
	fall_2015=Term.select().where(Term.year==2015,Term.session==1).get()
	winter_2015=Term.select().where(Term.year==2015,Term.session==2).get()
	sprint_2015=Term.select().where(Term.year==2015,Term.session==3).get()
	c3891=CourseGeneration.select().join(Course).where(Course.code==3891).order_by(CourseGeneration.year_valid_to.desc()).get()
	b1 = c3891.lecture_hours
	c1 = c3891.labs
	d1= c3891.other_info
	wb1 = int(b1) / 3
	wc1 = int(c1) / 3
	wd1 = 0
	if d1 == 'up to eight tutorial sessions per semester':
		wd1 = .07
	if d1 == 'tutorial one hour per week':
		wd1 = .14
	if d1 == 'tutorial 1 hour per week':
		wd1 = .14
	if d1 == 'one tutorial hour per week':
		wd1 = .14
	if d1 == '1 client meeting per week, 1 tutorial per week':
		wd1 = .14
	weight1 = wb1 + wc1 + wd1
	c1020=CourseGeneration.select().join(Course).where(Course.code==1020).order_by(CourseGeneration.year_valid_to.desc()).get()
	b2 = c1020.lecture_hours
	c2 = c1020.labs
	d2= c1020.other_info
	wb2 = int(b2) / 3
	wc2 = int(c2) / 3
	wd2 = 0
	if d2 == 'up to eight tutorial sessions per semester':
		wd2 = .07
	if d2 == 'tutorial one hour per week':
		wd2 = .14
	if d2 == 'tutorial 1 hour per week':
		wd2 = .14
	if d2 == 'one tutorial hour per week':
		wd2 = .14
	if d2 == '1 client meeting per week, 1 tutorial per week':
		wd2 = .14
	weight2 = wb2 + wc2 + wd2
	c8894=CourseGeneration.select().join(Course).where(Course.code==8894).order_by(CourseGeneration.year_valid_to.desc()).get()
	b = c8894.lecture_hours
	c = c8894.labs
	d= c8894.other_info
	wb = int(b) / 3
	wc = int(c)/ 3
	wd = 0
	if d == 'up to eight tutorial sessions per semester':
		wd = .07
	if d == 'tutorial one hour per week':
		wd = .14
	if d == 'tutorial 1 hour per week':
		wd = .14
	if d == 'one tutorial hour per week':
		wd = .14
	if d == '1 client meeting per week, 1 tutorial per week':
		wd = .14
	weight = wb + wc + wd
	# Offering.create_or_get(enrolment=1,prof_id=1,semester_id=fall_2015,course_gen_id=c3891,weight=weight1)
	# Offering.create_or_get(enrolment=1,prof_id=1,semester_id=winter_2015,course_gen_id=c1020,weight=weight2)
	# Offering.create_or_get(enrolment=1,prof_id=1,semester_id=winter_2015,course_gen_id=c8894,weight=weight)


def superC():
	SupervisionClass.create(description='test stuff', weight=0.047)

def supera():
	fall_2015=Term.select().where(Term.year==2015,Term.session==1).get()
	winter_2015=Term.select().where(Term.year==2015,Term.session==2).get()
	sprint_2015=Term.select().where(Term.year==2015,Term.session==3).get()
	Supervision.create(prof_id=1,student_id=1,supervision_class_id=1,semester_id=fall_2015)
	Supervision.create(prof_id=1,student_id=2,supervision_class_id=1,semester_id=winter_2015)
	Supervision.create(prof_id=1,student_id=2,supervision_class_id=1,semester_id=sprint_2015)
	Supervision.create(prof_id=1,student_id=3,supervision_class_id=1,semester_id=sprint_2015)
	Supervision.create(prof_id=1,student_id=1,supervision_class_id=1,semester_id=sprint_2015)


def person():
	# can't hear
	Person.create_or_get(name='Mr. Anderson',email='jonathan.anderson@mun.ca')

def student():
	# use sign language
	Student.create_or_get(name='Juteau',email='2011205085')
	Student.create_or_get(name='Derakhshan Nik',email='201509962')
	Student.create_or_get(name='Nguyen',email='201051471')

# def weight():
# 	offering = Offering.select()
# 	for x in offering:
# 		b=x.course_gen_id.lecture_hours
# 		c=x.course_gen_id.labs
# 		d=x.course_gen_id.other_info
# 		wb=b/3
# 		wc=c/3
# 		wd=0
# 		if d=='up to eight tutorial sessions per semester':
# 			wd=.07
# 		if d=='tutorial one hour per week':
# 			wd=.14
# 		if d=='tutorial 1 hour per week':
# 			wd =.14
# 		if d=='one tutorial hour per week':
# 			wd = .14
# 		if d=='1 client meeting per week, 1 tutorial per week':
# 			wd = .14
# 		weight=wb+wc+wd
# 		Offering.update(weight=weight).where(Offering.id==z)