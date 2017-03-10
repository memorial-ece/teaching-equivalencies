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
import random
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
			if ac != c:
				list1.append(i + ':' + 'lecturehours')
				ac = c
			if ad != d:
				list1.append(i + ':' + 'title')
				ad = d
			if ae != e:
				list1.append(i + ':' + 'comments')
				ae = e
			if af != f:
				list1.append(i + ':' + 'courseid')
				af = f
			if ag != g:
				list1.append(i + ':' + 'other info')
				ag = g
			if ah != h:
				ah = str(ah)
				list1.append(i + ':' + 'old id')
				ah = h
	return list1


def semester_quick_gen(fromD):
	now = str(datetime.datetime.now())
	year= now.split()
	p=re.compile(r"\d+")
	year=p.findall(year[0])
	start=fromD
	while int(start)<=int(year[0]):
		session=0
		while session!=5:
			session+=1
			try:
				Term.get_or_create(year=start,session=session)
			except:
				pass
		else:
			start+=1
		if start == 2020:
			break

def offer(year,code,session,profid,numberofstudents,sectionnumbers):
	for x in CourseGeneration.select().join(Course).where(Course.code==code).order_by(CourseGeneration.year_valid_to.asc()):
		if int(x.year_valid_to)>=int(year):
			year2=x.year_valid_to
			ses=Term.select().where(Term.year==year2,Term.session==session).get()
			b1 = x.credit_hours
			c1 = x.labs
			d1= x.other_info
			wb1 = float(b1) / 3
			wc1 = float(c1) / 36 *.27 * sectionnumbers
			wd1 = 0
			if d1 == 'up to eight tutorial sessions per semester':
				wd1 = float(.07)
			if d1 == 'tutorial one hour per week':
				wd1 = float(.14)
			if d1 == 'tutorial 1 hour per week':
				wd1 = float(.14)
			if d1 == 'one tutorial hour per week':
				wd1 = float(.14)
			if d1 == '1 client meeting per week, 1 tutorial per week':
				wd1 = float(.14)
			print wb1
			print wc1
			print wd1
			weight1 = wb1 + wc1 + wd1
			print weight1
			Offering.get_or_create(enrolment=1,prof_id=1,semester_id=ses,course_gen_id=x.id,weight=weight1)
			break



def Psuper():
	ProjectClass.get_or_create(description='Undergraduate project course', weight=0.5)
	ProjectClass.get_or_create(description='senior project supervision of a group of 4 students', weight=(float(0.125)/3))
	ProjectClass.get_or_create(description='Case by Case', weight=2)


def superC(BOOLDoyouwanttocreateanewone,Description,Weight):
	SupervisionClass.get_or_create(description='Gradstudent 1 term', weight=0.047)
	SupervisionClass.get_or_create(description='Masters 1 term', weight=0.07)
	SupervisionClass.get_or_create(description='Doctoral 1 term', weight=(float(.32)/3))
	if BOOLDoyouwanttocreateanewone==True:
		SupervisionClass.get_or_create(description=Description, weight=Weight)


def supera(TermS,profid,Studentid,supervisoncalss,session):
	ses=Term.select().where(Term.year==TermS,Term.session==session).get()
	Supervision.get_or_create(prof_id=profid,student_id=Studentid,supervision_class_id=supervisoncalss,semester_id=ses)


def person(name,email,staryear,startsem):
	# can't hear
	ses=Term.select().where(Term.year==staryear,Term.session==startsem).get()
	Person.get_or_create(name='Mr. Anderson',email='jonathan.anderson@mun.ca', start=ses.id)


def student(name,email):
	# use sign language
	Student.get_or_create(name='Juteau',email='2011205085')
	Student.get_or_create(name='Derakhshan Nik',email='201509962')
	Student.get_or_create(name='Nguyen',email='201051471')


def deficit(prof_id):
	personal = Person.get(Person.id == prof_id)
	now = datetime.datetime.now()
	year = now.year
	startYear = personal.start.year
	startsem = personal.start.session
	sem=currentsem()
	timeyear=year-startYear
	timesemester=sem-startsem
	if timesemester<0:
		timeyear-=1
		timesemester=-timesemester
		timesemester=3-timesemester
	deduction=0
	duty_for_first_two_year=3.3333333333
	duty_for_normal=4.0
	if timeyear>=3:
		deduction=duty_for_first_two_year * 2
		timefix=timeyear-2
		deduction+=duty_for_normal*timefix
	elif timeyear<3:
		deduction=duty_for_first_two_year * 2
	if deduction==0:
		print 'keegan you dicked up'
	return deduction

def currentsem():
	now = datetime.datetime.now()
	month = now.month
	if month>=7:
		sem=1
	elif month<=4:
		sem=2
	else:
		sem=3
	return sem



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
# 			wd=float(.14)
# 		if d=='tutorial 1 hour per week':
# 			wd =float(.14)
# 		if d=='one tutorial hour per week':
# 			wd = float(.14)
# 		if d=='1 client meeting per week, 1 tutorial per week':
# 			wd = float(.14)
# 		weight=wb+wc+wd
# 		Offering.update(weight=weight).where(Offering.id==z)