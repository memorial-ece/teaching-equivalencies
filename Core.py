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
import sys
import time
from itertools import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from playhouse.csv_loader import *
from db import *

stripprimary = re.compile(r"[a-zA-Z0-9._-]{2,}")
matplotlib.rcParams['backend'] = "Qt4Agg"
crsnumber= re.compile(r"(?<=ENGI )(\d+)")
DATABASE = 'database.db'
db = SqliteDatabase(DATABASE)
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'csv'}


def intake(year):
	list_of_error_types=list()
	list_Errors = list()
	varlen_for_progress = len(year)
	counter=0
	last_selester=0
	offering_id = list()
	code = list()
	try:
		for filename in year:
			counter+=1
			coursecodes = list()
			list_names = list()
			primary_prof_list_and_instances = list()
			courses_offered = list()
			primary_prof_list = list()
			secondary_prof_list = list()
			list_sections = list()
			var = -1
			progress(counter,varlen_for_progress)
			crsnumber = re.compile(r"(?<=ENGI )(\d+)")
			crosslist = re.compile(r"(?<=CROSS LISTED)(\W)")
			namestrip = re.compile(r"(?<=Primary - )...\S+")
			namestrip2 = re.compile(r"(?<=Primary - )\w+\s+\w+\s+\w+\s+\w+")
			semstrip = re.compile(r".\d$")
			yearstrip = re.compile(r"^\d...")
			p1 = re.compile(r".....\d.....$")
			filename4 = p1.findall(filename)
			p3 = re.compile(r"(\d+\b)(?!.*\1\b)")
			filen2 = int(''.join(p3.findall(str(filename4))))
			filen3 = str(filen2)
			startyear = (yearstrip.findall(filen3))
			startsem = (semstrip.findall(filen3))
			startyear = str(startyear).strip("[]'")
			startsem = str(startsem).strip("[]'")
			last_selester=filename
			x_file = open(filename).readlines()
			for w in x_file:
				w = str(w.splitlines())
				P_name = str((namestrip.findall(w))).strip("[]'")
				crosscheck = str((crosslist.findall(w))).strip("[]'")
				crse = str(crsnumber.findall(w)).strip("[]'")
				code.append(crse)
				file2 = str((namestrip2.findall(w)))
				if crse!='' and P_name=='':
					if crosscheck == "":
						list_of_error_types.append('cross listed:')
					else:
						list_of_error_types.append('no prof')
					file4 = str(crse).strip("'[]")
					list_Errors.append(filename)
					list_Errors.append(file4)
				if P_name!='' and P_name!='m munprod':
					var+=1
					list_names.append(P_name)
					P_name = str(P_name).strip("[]'")
					file2 = str(file2).strip("[]'")
					file4 = str(crse).strip("'[]")
					secondary_prof_list.append(file2)
					primary_prof_list_and_instances.append(P_name)
					courses_offered.append(file4)
					if crse!=''and list_names[var]!='m munprod':
						list_sections.append(1)
						primary_prof_list.append(P_name)
					elif list_names[var]!='m munprod':
						list_sections[-1]=list_sections[-1]+1
			counter1 = -1
			y=None
			fixer_counter = -1
			for prof in primary_prof_list_and_instances:
				if prof != 'm munprod':
					x=prof
					counter1+=1
					if x!=y:
						fixer_counter+=1
						y=x
					if secondary_prof_list[counter1]!='':
						patch=str(secondary_prof_list[counter1]).split()
						person((patch[2]+' '+patch[3]),(patch[2]+' '+patch[3])+'@mun.ca',startyear,startsem)
						pid2=Person.select().where(Person.name==(patch[2]+' '+patch[3])).get()
						offer(startyear, courses_offered[counter1], startsem, pid2.id, 80, list_sections[fixer_counter])
						person((patch[0]+' '+patch[1]),(patch[0]+' '+patch[1])+'@mun.ca',startyear,startsem)
						pid1=Person.select().where(Person.name==(patch[0]+' '+patch[1])).get()
						off=offer(startyear, courses_offered[counter1], startsem, pid1.id, 80, list_sections[fixer_counter])
						offering_id.append(off)
					else:
						person(primary_prof_list_and_instances[counter1],primary_prof_list_and_instances[counter1]+'@mun.ca',startyear,startsem)
						pid1=Person.select().where(Person.name==primary_prof_list_and_instances[counter1]).get()
						offer(startyear,courses_offered[counter1],startsem,pid1.id,80,list_sections[fixer_counter])
		print
		print 'completed files in parameters'
		print
		coursecodes.append(offering_id)
		coursecodes.append(code)
		return coursecodes,list_Errors,list_of_error_types
	except:
		print
		print 'The file '+last_selester+" is bad and this was the file i was processing when i failed"


def splitting(pid1):
	id_storage=pid1[0]
	for id_num in id_storage:
		if id_num is not None:
			update1=Mastermany.update(split=float(0.5)).where(Mastermany.oid==id_num)
			update1.execute()


def informationXchange(generation,list1):
	first_run_var=1
	aa = None
	ab = None
	ac = None
	ad = None
	ae = None
	af = None
	ag = None
	ah = None
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
				list1.append(i + ':' + 'previous id')
				ah = h
	return list1


def offer(year,code,session,profid,numberofstudents,sectionnumbers):
	for x in CourseGeneration.select().join(Course).where(Course.code==code).order_by(CourseGeneration.end_year.asc()):
		if int(x.end_year)>=int(year):
			ses=Term.select().where(Term.year==year,Term.session==session).get()
			try:
				Offering.get_or_create(enrolment=numberofstudents,semester=ses,generation=x.id,sections=sectionnumbers,reviewed=False)
				A=Offering.select().where(Offering.enrolment==numberofstudents,Offering.semester==ses,Offering.generation==x.id,Offering.sections==sectionnumbers).get()
			except:
				A=Offering.select().where(Offering.enrolment==numberofstudents,Offering.semester==ses,Offering.generation==x.id,Offering.sections==sectionnumbers).get()
			Mastermany.get_or_create(instructor=profid,oid=A)
			return A.id


def weight_calc(OID):
	off=Offering.select().where(Offering.id==OID).get()
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
		we = float((((float(b1) + (numberofstudents - float(75))) / float(75)) * .5))
	else:
		we = 0
	wb1 = (((float(b1) + float(c1)) / float(36)) * .27) * float(sectionnumbers)
	wc1 = (((float(b1) + float(wd1)) / float(12)) * .14)
	weight1 = wb1 + wc1 + we+wa1
	if numberofstudents < 5:
		weight1 = 0
	return weight1


def Psuper(BOOLDoyouwanttocreateanewone,Description,Weight):
	ProjectClass.get_or_create(description='Undergraduate project course', weight=0.5)
	ProjectClass.get_or_create(description='senior project supervision of a group of 4 students', weight=(float(0.125)/3))
	ProjectClass.get_or_create(description='Case by Case', weight=2)
	if BOOLDoyouwanttocreateanewone:
		ProjectClass.get_or_create(description=Description, weight=Weight)


def superC(BOOLDoyouwanttocreateanewone,Description,Weight):
	SupervisionClass.get_or_create(description='Gradstudent 1 term', weight=0.047)
	SupervisionClass.get_or_create(description='Masters 1 term', weight=0.07)
	SupervisionClass.get_or_create(description='Doctoral 1 term', weight=(float(.32)/3))
	if BOOLDoyouwanttocreateanewone:
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
	try:Term.get_or_create(year= staryear, session = startsem)
	except:pass
	ses=Term.select().where(Term.year==staryear,Term.session==startsem).get()
	try:Person.get_or_create(name=name,email=email,start=ses.id,reviewed=False)
	except:pass


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
		print 'oups error in deficit'
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


def export_file(selector, name='default'):
	with open(str(name)+'.csv', 'w') as fh:
		if str(selector) == 'Person':
			query = Person.select().order_by(Person.id)
			dump_csv(query, fh)
		if str(selector) == 'Supervision':
			query = Supervision.select().order_by(Supervision.id)
			dump_csv(query, fh)
		if str(selector) == 'SupervisionClass':
			query = SupervisionClass.select().order_by(SupervisionClass.id)
			dump_csv(query, fh)
		if str(selector) == 'Course':
			query = Course.select().order_by(Course.code)
			dump_csv(query, fh)
		if str(selector) == 'CourseGeneration':
			query = CourseGeneration.select().order_by(CourseGeneration.id)
			dump_csv(query, fh)
		if str(selector) == 'Student':
			query = Student.select().order_by(Student.id)
			dump_csv(query, fh)
		if str(selector) == 'Term':
			query = Term.select().order_by(Term.id)
			dump_csv(query, fh)
		if str(selector) == 'Offering':
			query = Offering.select().order_by(Offering.id)
			dump_csv(query, fh)
		if str(selector) == 'Role':
			query = Role.select().order_by(Role.id)
			dump_csv(query, fh)
		if str(selector) == 'ProjectClass':
			query = ProjectClass.select().order_by(ProjectClass.id)
			dump_csv(query, fh)
		if str(selector) == 'ProjectType':
			query = ProjectType.select().order_by(ProjectType.id)
			dump_csv(query, fh)
		if str(selector) == 'Mastermany':
			query = Mastermany.select().order_by(Mastermany.instructor)
			dump_csv(query, fh)
		if str(selector) == 'ProjectSupervision':
			query = ProjectSupervision.select().order_by(ProjectSupervision.id)
			dump_csv(query, fh)
		if str(selector) == 'Adjustment':
			query = Adjustment.select().order_by(Adjustment.id)
			dump_csv(query, fh)
		else:
			dump_csv(selector, fh)


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def docustomexport(Table):
	export_file(Table)


def docustomimport(Table):
	import_file(Table)


def error(list_of_error, list_of_error_types):
	print 'please see that these errors are attended to '
	print 'list of error types found'
	targ = open('Errors', 'w')
	counter=-1
	var = len(list_of_error)
	var = var/2
	for x in list_of_error_types:
		targ.write(x)
		targ.write('\n')
	print'locations of errors'
	while counter != var:
		counter += 1
		if  counter == var:
			break
		var3 = counter*2
		var4 = var3+1
		targ.write('\n')
		targ.write(list_of_error[var3])
		targ.write('\n')
		targ.write(list_of_error[var4])
	print 'view the HTML files to correct'


def offergen(files):
	start_time = time.time()
	coursecodes, list_of_error, list_of_error_types = intake(files)
	print
	if list_of_error != '':
		print
		print "please check on the errors file, I have some results"
	print
	print "My program took", time.time() - start_time, "to run"
	print
	return coursecodes,list_of_error,list_of_error_types


def split(files):
	start_time = time.time()
	person1 = Person.select()
	counter = 0
	varlen = len(person1)
	for ixd in person1:
		counter += 1
		progress(counter,varlen)
		update = Mastermany.update(split=1).where(Mastermany.instructor == ixd.id)
		update.execute()
		update1 = Mastermany.update(split=.5).where(Mastermany.oid == 904)
		update1.execute()
	print
	print "My program took", time.time() - start_time, "to run"
	splitting(files)


def peeweetable(Droptype):
	if Droptype == 'DropReCreate':
		db.connect()
		db.drop_tables(
			[Person,Mastermany,
			 Term,
			 Offering,
			 # Course,
			 Role, ProjectSupervision, ProjectClass,
			 Supervision,
			 # CourseGeneration,
			 SupervisionClass, ProjectType,
			 Student, Adjustment],safe=True)
		db.create_tables(
			[Person,Mastermany,
			 Term,
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
			 Term,
			 Offering,
			 Course,
			 Role, ProjectSupervision, ProjectClass,
			 Supervision,
			 CourseGeneration,
			 SupervisionClass, ProjectType, Student, Adjustment],safe=True)
		db.close()
	elif Droptype == 'Drop':
		db.connect()
		db.drop_tables(
			[Person, Mastermany,
			 Term,
			 Offering,
			 Course,
			 Role, ProjectSupervision, ProjectClass,
			 Supervision,
			 CourseGeneration,
			 SupervisionClass, ProjectType, Student, Adjustment],safe=True)
		db.close()


def progress(count, total, status=''):
	bar_len = 60
	filled_len = int(round(bar_len * count / float(total)))
	percents = round(100.0 * count / float(total), 1)
	bar = '=' * filled_len + '-' * (bar_len - filled_len)
	sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
	sys.stdout.flush()


def anyplot(semester,name,weights):
	# rename need test data again
	var = None
	p1 = re.compile(r"\w+")
	p2 = p1.findall(name)
	listany=list()
	counter=-1
	for x,y in enumerate(semester):
		if x % 2==0:
			var=y
		else:
			counter+=1
			listany.append(str(var)+'0'+str(y))
			listany.append(weights[counter])
	list3,list4=matchandsort(listany)
	width = 1
	if p2[0]=='project':
		stack=3
	else:
		stack=1.5
	N = len(list4)
	ind = np.arange(N)
	plt.bar(left=ind, height=list3, width=width, color='#d62728')
	plt.ylabel('Credit Value')
	plt.xlabel('Semester in format (year)(semester id)')
	plt.title(p2[0])
	plt.yticks(np.arange(0, stack, 0.125))
	plt.xticks(ind, list4, rotation='vertical')
	plt.savefig(str(name) + '.pdf', bbox_inches='tight')
	plt.close()


def matchandsort(diction_of_var):
	var =- 2
	terms = list()
	values = list()
	for i, j in enumerate(diction_of_var):
		if i %2==0:
			try:
				var=terms.index(j)
			except:
				var=-2
				terms.append(j)
		else:
			if var != -2:
				values[var]+=j
			else:
				values.append(j)
	total_weight = list()
	year_term = list()
	for (y, x) in sorted(zip(terms, values)):
		total_weight.append(x)
		year_term.append(y)
	return total_weight,year_term


def offerplot(dict_temp2,name):
	print dict_temp2
	p1 = re.compile(r"\w+")
	p2 = p1.findall(name)
	width = 1
	total_weight,year_term=matchandsort(dict_temp2)
	N = len(year_term)
	ind = np.arange(N)
	plt.bar(left=ind,height=total_weight,width=width,color='#d62728')
	plt.ylabel('Credit Value')
	plt.xlabel('Semester Term')
	plt.title(p2[0])
	plt.yticks(np.arange(0,6,0.25))
	plt.xticks(ind, year_term, rotation='vertical')
	plt.savefig(str(name)+'.pdf',bbox_inches='tight')
	plt.close()


def populate(files):
		coursecodes, htmldates, list_of_error_types = offergen(files)
		split(coursecodes)
		error(htmldates, list_of_error_types)


def test():
	print str(1)+str(1)
	quick_verify()


def quick_verify():
	person=Person.select()
	for x in person:
		a=Person.update(reviewed=True).where(Person.id==x.id)
		a.execute()
	course=Course.select()
	for x in course:
		a=Course.update(reviewd=True).where(Course.id==x.id)
		a.execute()
	coursegen=CourseGeneration.select()
	for x in coursegen:
		a=CourseGeneration.update(reviewed=True).where(CourseGeneration.id==x.id)
		a.execute()
	offering=Offering.select()
	for x in offering:
		a=Offering.update(reviewed=True).where(Offering.id==x.id)
		a.execute()

def termselect(year):
	if year == 'true':
		term=Term.select()
	else:
		term=Term.select().where(Term.year<=year)
	return term