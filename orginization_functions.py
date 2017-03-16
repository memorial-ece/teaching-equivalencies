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

namestrip = re.compile(r"(?<=Primary - )...\S+")
stripprimary = re.compile(r"[a-zA-Z0-9._-]{2,}")
crsnumber= re.compile(r"(?<=ENGI )(\d+)")


def test():
	targ=open('terminalcode','w')
	targ.write('./Calendar.py ')
	a=2007
	while a<2016:
		b=0
		a+=1
		while b<7:
			b+=1
			targ.write('calendar/'+str(a)+str(b)+'.html ')


def lang():
	starttear=2010
	while starttear!=2012:
		starttear+=1
		startsem = 0
		while startsem!=3:
			startsem+=1
			try:
				x_file = list((open('offerings/'+str(starttear)+'0'+str(startsem)+'.html').readlines()))
				for w in (x_file):
					w = str(w.splitlines())
					file1 = str((namestrip.findall(w)))
					file3 = str(crsnumber.findall(w))
					if file1[1]!=']' and file3[1]!=']':
						file1 = str(file1).strip("[]'")
						file3 = str(file3).strip("'[]")
						person(file1,file1+'@mun.ca',starttear,startsem)
						pid=Person.select().where(Person.name==file1).get()
						offer(starttear,file3,startsem,pid.id,1,1)
			except:
				print 'no latest semester'


def informationXchange(generation,list1):
	first_run_var=1
	for x in generation:
		a = x.labs
		b = x.credit_hours
		c = x.lecture_hours
		d = x.title
		e = x.comments
		f = x.course
		g = x.other_info
		h = x.previous_course
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
				list1.append(i + ':' + 'previous id')
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
	for x in CourseGeneration.select().join(Course).where(Course.code==code).order_by(CourseGeneration.end_year.asc()):
		if int(x.end_year)>=int(year):
			ses=Term.select().where(Term.year==year,Term.session==session).get()
			b1 = x.credit_hours
			c1 = x.labs
			d1= x.other_info
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
			weight1=fix(numberofstudents,sectionnumbers,b1,c1,wd1)
			try:
				Offering.get_or_create(enrolment=numberofstudents,semester=ses,generation=x.id,weight=weight1)
				A=Offering.select().where(Offering.enrolment==numberofstudents,Offering.semester==ses,Offering.generation==x.id,Offering.weight==weight1).get()
			except:
				A=Offering.select().where(Offering.enrolment==numberofstudents,Offering.semester==ses,Offering.generation==x.id,Offering.weight==weight1).get()
			Mastermany.get_or_create(instructor=profid,oid=A, split=1)
			break


def fix(numberofstudents,sectionnumbers,b1,c1,wd1,):
	wa1=float(float(b1)/float(3))
	numberofstudents=float(numberofstudents)
	if numberofstudents > 75:
		we = float((((float(b1) + ((numberofstudents) - float(75))) / float(75 ))* .5))
	else:
		we = 0
	wb1 = ((((float(b1) + float(c1)) / float(36))* .27))*float(sectionnumbers)
	wc1 = ((((float(b1) + float(wd1)) / float(12) )* .14))
	weight1 = wb1 + wc1 + we+wa1
	if numberofstudents < 5:
		weight1 = 0
	return weight1


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
	Supervision.get_or_create(student_id=Studentid,supervision_class_id=supervisoncalss,semester=ses)
	A=Supervision.select().where(Supervision.student_id==Studentid,Supervision.supervision_class_id==supervisoncalss,Supervision.semester==ses).get()
	Mastermany.get_or_create(instructor=profid,sid=A, split=1)


def person(name,email,staryear,startsem):
	# can't hear
	ses=Term.select().where(Term.year==staryear,Term.session==startsem).get()
	try:
		B=Person.get_or_create(name=name,email=email,start=ses.id)
		Person.get_or_create(name=name,email=email,start=ses.id)
	except:
		pass


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


def check(code1,code2,code3):
	if code1!=0:
		check1 = Mastermany.select().where(Mastermany.oid==code1)
		n=0
		for a in check1:
			n=a.split
		return n
	if code2!=0:
		check1=Mastermany.select().where(Mastermany.pid==code2)
		n=0
		for a in check1:
			n=a.split
		return n
	if code3!=0:
		check1=Mastermany.select().where(Mastermany.sid==code3)
		n=0
		for a in check1:
			n=a.split
		return n


def splitting(number_of_people,code,what_to_update):
	var=float(float(1)/float(number_of_people))
	print code
	if what_to_update=='offering':
		a=check(code,0,0)
		print a
		if a >1:
			update = Mastermany.update(split=var).where(Mastermany.oid == code)
			update.execute()
	if what_to_update=='projectsupervision':
		a=check(0,code,0)
		print a
		if a >1:
			update = Mastermany.update(split=var).where(Mastermany.pid == code)
			update.execute()
	if what_to_update=='supervision':
		a=check(0,0,code)
		print a
		if a>1:
			update = Mastermany.update(split=var).where(Mastermany.sid == code)
			update.execute()


def start_splitting():
	person=Person.select()
	for id in person:
		a=people_also_teaching(id,'offering')
		loop_num=-1
		for x in a[0]:
			loop_num+=1
			if x>1:
				p= a[1][loop_num]
				o=x
				splitting(o,p,'offering')
	for id in person:
		a = people_also_teaching(id, 'projectsupervision')
		loop_num = -1
		for x in a[0]:
			loop_num += 1
			if x > 1:
				p = a[1][loop_num]
				o = x
				splitting(o,p,'projectsupervision')
	for id in person:
		a=people_also_teaching(id,'supervision')
		loop_num = -1
		for x in a[0]:
			loop_num += 1
			if x > 1:
				p = a[1][loop_num]
				o = x
				splitting(o,p,'supervision')


def people_also_teaching(prof_id,activator):
	if activator=='offering':
		activated = (Offering
				.select()
				.join(Mastermany)
				.where(Mastermany.instructor == prof_id)
				.order_by(Offering.semester.desc()))
	if activator=='projectsupervision':
		activated = (ProjectSupervision
							  .select()
							  .join(Mastermany)
							  .where(Mastermany.instructor == prof_id)
							  .order_by(ProjectSupervision.semester.desc()))
	if activator=='supervision':
		activated = (Supervision
					   .select()
					   .join(Mastermany)
					   .where(Mastermany.instructor == prof_id)
					   .order_by(Supervision.semester.desc()))
	courseteaching1=list()
	a2=list()
	n=0
	try:
		for x in activated:
			courseteaching2=list()
			if activator=='offering':
				teaching=Mastermany.select().where(Mastermany.oid==x.id)
				a2.append(x.id)
			if activator=='projectsupervision':
				teaching=Mastermany.select().where(Mastermany.pid==x.id)
				a2.append(x.id)
			if activator=='supervision':
				teaching=Mastermany.select().where(Mastermany.sid==x.id)
				a2.append(x.id)
			b=0
			for y in teaching:
				n+=1
				a=y.instructor.id
				courseteaching2.append(a)
			courseteaching1.append(len(courseteaching2))
		return courseteaching1,a2
	except:
		return 'error'