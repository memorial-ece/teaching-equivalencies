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
from playhouse.csv_loader import *
from itertools import *
import random
reload(sys)
sys.setdefaultencoding('utf-8')

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


def lang(year):
	list6=list()
	list7 = list()
	list8=list()
	namestrip = re.compile(r"(?<=Primary - )...\S+")
	namestrip2= re.compile(r"(?<=Primary - )\w+\s+\w+\s+\w+\s+\w+")
	starttear=2007
	try:
		while starttear!=year:
			progress(starttear,year)
			starttear += 1
			startsem = 0
			while startsem!=3:
				list1 = list()
				list2 = list()
				list3 = list()
				list4 = list()
				list5 = list()
				var = -1
				startsem+=1
				try:
					x_file = list((open('offerings/'+str(starttear)+'0'+str(startsem)+'.html').readlines()))
					for w in (x_file):
						w = str(w.splitlines())
						file1 = str((namestrip.findall(w)))
						file3 = str(crsnumber.findall(w))
						list7.append(file3)
						file2 = str((namestrip2.findall(w)))
						if file1[1]!=']':
							var+=1
							list1.append(file1)
							file1 = str(file1).strip("[]'")
							file2 = str(file2).strip("[]'")
							file4 = str(file3).strip("'[]")
							list5.append(file2)
							var3=[len(list(group)) for key, group in groupby(list1)]
							list2.append(file1)
							list3.append(file4)

							if file3[1]!=']':
								list4.append(file1)
				except:
					print 'no latest semester'

				var5=-1
				for x in var3:
					var5+=1
					if list5[var5]!='':
						patch=str(list5[var5]).split()
						person((patch[2]+' '+patch[3]),(patch[2]+' '+patch[3])+'@mun.ca',starttear,startsem)
						pid2=Person.select().where(Person.name==(patch[2]+' '+patch[3])).get()
						offer(starttear, list3[var5], startsem, pid2.id, 80, x)
						person((patch[0]+' '+patch[1]),(patch[0]+' '+patch[1])+'@mun.ca',starttear,startsem)
						pid1=Person.select().where(Person.name==(patch[0]+' '+patch[1])).get()
						var12=offer(starttear, list3[var5], startsem, pid1.id, 80, x)
						list6.append(var12)
					else:
						person(list4[var5],list4[var5]+'@mun.ca',starttear,startsem)
						pid1=Person.select().where(Person.name==list4[var5]).get()
						offer(starttear,list3[var5],startsem,pid1.id,80,x)
	except:
		print 'completed files in parameters'
	list8.append(list6)
	list8.append(list7)
	return list8


def splitting(pid1):
		var2=pid1[0]
		for var1 in var2:
			if var1 is not None:
				update1=Mastermany.update(split=float(0.5)).where(Mastermany.oid==var1)
				update1.execute()


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
			try:
				Offering.get_or_create(enrolment=numberofstudents,semester=ses,generation=x.id,sections=sectionnumbers)
				A=Offering.select().where(Offering.enrolment==numberofstudents,Offering.semester==ses,Offering.generation==x.id,Offering.sections==sectionnumbers).get()
			except:
				A=Offering.select().where(Offering.enrolment==numberofstudents,Offering.semester==ses,Offering.generation==x.id,Offering.sections==sectionnumbers).get()
			Mastermany.get_or_create(instructor=profid,oid=A)
			return A.id


def weight_calc(OID):
	print OID.id
	off=Offering.select().where(Offering.id==OID.id).get()
	gen=CourseGeneration.select().join(off).where(CourseGeneration.id==off.generation).get()
	b1 = gen.credit_hours
	c1 = gen.labs
	d1= gen.other_info
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
	weight1=fix(off.enrolment,off.sections,b1,c1,wd1)
	return weight1


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


def Psuper(BOOLDoyouwanttocreateanewone,Description,Weight):
	ProjectClass.get_or_create(description='Undergraduate project course', weight=0.5)
	ProjectClass.get_or_create(description='senior project supervision of a group of 4 students', weight=(float(0.125)/3))
	ProjectClass.get_or_create(description='Case by Case', weight=2)
	if BOOLDoyouwanttocreateanewone==True:
		ProjectClass.get_or_create(description=Description, weight=Weight)


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


def Psupera(TermS,profid,team_id,supervisoncalss,session):
	ses=Term.select().where(Term.year==TermS,Term.session==session).get()
	ProjectSupervision.get_or_create(team_id=team_id,project_class_id=supervisoncalss,semester=ses)
	A=ProjectSupervision.select().where(ProjectSupervision.team_id==team_id,ProjectSupervision.project_class_id==supervisoncalss,ProjectSupervision.semester==ses).get()
	Mastermany.get_or_create(instructor=profid,pid=A, split=1)

def person(name,email,staryear,startsem):
	# can't hear
	ses=Term.select().where(Term.year==staryear,Term.session==startsem).get()
	try:
		Person.get_or_create(name=name,email=email,start=ses.id)
	except:
		pass


def student(name,email):
	# use sign language
	Student.get_or_create(name=name,email=email)


def team(name,email):
	# use sign language
	ProjectType.get_or_create(name=name,description=email)


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


def import_file(selector):
	name = selector+'.csv'
	if selector == 'Person':
		load_csv(Person, name)
	if selector == 'Supervision':
		load_csv(Supervision, name)
	if selector == 'SupervisionClass':
		load_csv(SupervisionClass, name)
	if selector == 'Course':
		load_csv(Course, name)
	if selector == 'CourseGeneration':
		load_csv(CourseGeneration, name)
	if selector == 'Student':
		load_csv(Student, name)
	if selector == 'Term':
		load_csv(Term, name)
	if selector == 'Offering':
		load_csv(Offering, name)
	if selector == 'Role':
		load_csv(Role, name)
	if selector == 'ProjectClass':
		load_csv(ProjectClass, name)
	if selector == 'ProjectType':
		load_csv(ProjectType, name)
	if selector == 'Mastermany':
		load_csv(Mastermany, name)
	if selector == 'ProjectSupervision':
		load_csv(ProjectSupervision, name)
	if selector == 'Adjustment':
		load_csv(Adjustment, name)


def export_file(selector):
	with open(selector+'.csv', 'w') as fh:
		if selector == 'Person':
			query = Person.select().order_by(Person.id)
			dump_csv(query, fh)
		if selector == 'Supervision':
			query = Supervision.select().order_by(Supervision.id)
			dump_csv(query, fh)
		if selector == 'SupervisionClass':
			query = SupervisionClass.select().order_by(SupervisionClass.id)
			dump_csv(query, fh)
		if selector == 'Course':
			query = Course.select().order_by(Course.course_num)
			dump_csv(query, fh)
		if selector == 'CourseGeneration':
			query = CourseGeneration.select().order_by(CourseGeneration.id)
			dump_csv(query, fh)
		if selector == 'Student':
			query = Student.select().order_by(Student.id)
			dump_csv(query, fh)
		if selector == 'Term':
			query = Term.select().order_by(Term.id)
			dump_csv(query, fh)
		if selector == 'Offering':
			query = Offering.select().order_by(Offering.id)
			dump_csv(query, fh)
		if selector == 'Role':
			query = Role.select().order_by(Role.id)
			dump_csv(query, fh)
		if selector == 'ProjectClass':
			query = ProjectClass.select().order_by(ProjectClass.id)
			dump_csv(query, fh)
		if selector == 'ProjectType':
			query = ProjectType.select().order_by(ProjectType.id)
			dump_csv(query, fh)
		if selector == 'Mastermany':
			query = Mastermany.select().order_by(Mastermany.instructor)
			dump_csv(query, fh)
		if selector == 'ProjectSupervision':
			query = ProjectSupervision.select().order_by(ProjectSupervision.id)
			dump_csv(query, fh)
		if selector == 'Adjustment':
			query = Adjustment.select().order_by(Adjustment.id)
			dump_csv(query, fh)


DATABASE = 'database.db'
db = SqliteDatabase(DATABASE)
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def docustomexport(Table):
	export_file(Table)


def docustomimport(Table):
	import_file(Table)


def error():
	for term in Term.select():
		a = 0
		for courses in Offering.select().where(Offering.semester==term.id):
			a+=1
		if a<15:
			print 'i think there is an error in courses offered with the id of '+str(term.id)+' becasue there are only '+str(a)+' records and im looking for at least 20'
		else:
			print a


def offergen(year):
	# ######################semester_quick_gen(fromD)
	semester_quick_gen(2007)
	# #####################person(name,email)
	person('Mr. Anderson','jonathan.anderson@mun.ca',2012,3)
	person('Mr. Anders54on','jon56athan.anderson@mun.ca',2008,3)
	# person('Mr. Anon','jonathan.arson@mun.ca',2013,3)
	var1=lang(year)
	# ################student(name, email)
	student('Juteau','2011205085')
	student('Derakhshan Nik','201509962')
	student('Nguyen','201051471')
	team('Juteau','test')
	team('Derakhshan Nik','test2')
	team('Nguyen','test3')
	# ##################superC(BOOLDoyouwanttocreateanewone,Description,Weight)
	superC(True,'example of custom descriptions',400)
	Psuper(True,'example of custom descriptions',4050)
	# #############supera(TermS,profid,Studentid,supervisoncalss,session)
	supera(2015,1,1,1,1)
	supera(2015,1,2,2,1)
	supera(2015,1,2,2,2)
	supera(2015,1,1,1,3)
	supera(2015,1,3,3,3)
	supera(2015,1,3,4,3)
	supera(2015,1,3,3,3)
	Psupera(2015,1,1,1,1)
	Psupera(2015,1,2,2,1)
	Psupera(2015,1,2,2,2)
	Psupera(2015,1,1,1,3)
	Psupera(2015,1,3,3,3)
	Psupera(2015,1,3,4,3)
	Psupera(2015,1,3,3,3)
	# ###########offer(year,code,session,profid,numberofstudents,sectionnumbers):
	offer(2015,1020,2,1,80,3)
	offer(2015,1020,2,3,80,3)
	offer(2015,3891,1,1,80,1)
	offer(2015,8894,2,1,70,1)
	offer(2015,8894,2,3,70,1)
	offer(2015,3891,1,2,80,1)
	offer(2015,8894,2,2,70,1)
	person1=Person.select()
	for ixd in person1:
		update=Mastermany.update(split=1).where(Mastermany.instructor == ixd.id)
		update.execute()
		update1=Mastermany.update(split=.5).where(Mastermany.oid == 904)
		update1.execute()
	splitting(var1)


def peeweetable(Droptype):
	if Droptype == 'DropReCreate':
		db.connect()
		db.drop_tables(
			[Person,Mastermany,
			 # Term,
			 Offering,
			 # Course,
			 Role, ProjectSupervision, ProjectClass,
			 Supervision,
			 # CourseGeneration,
			 SupervisionClass, ProjectType,
			 Student, Adjustment],safe=True)
		db.create_tables(
			[Person,Mastermany,
			 # Term,
			 Offering,
			 # Course,
			 Role, ProjectSupervision, ProjectClass,
			 Supervision,
			 # CourseGeneration,
				SupervisionClass, ProjectType, Student, Adjustment],safe=True)
		db.close()
	elif Droptype == 'Create':
		db.connect()
		db.create_tables(
			[Person, Mastermany,
			 # Term,
			 Offering,
			 # Course,
				Role, ProjectSupervision, ProjectClass,
			 Supervision,
			 # CourseGeneration,
			 SupervisionClass, ProjectType, Student, Adjustment],safe=True)
		db.close()
	elif Droptype == 'Drop':
		db.connect()
		db.drop_tables(
			[Person, Mastermany,
			 # Term,
			 Offering,
			 # Course,
			 Role, ProjectSupervision, ProjectClass,
			 Supervision,
			 # CourseGeneration,
			 SupervisionClass, ProjectType, Student, Adjustment],safe=True)
		db.close()


def progress(count, total, status=''):
	bar_len = 60
	filled_len = int(round(bar_len * count / float(total)))
	percents = round(100.0 * count / float(total), 1)
	bar = '=' * filled_len + '-' * (bar_len - filled_len)
	sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
	sys.stdout.flush()