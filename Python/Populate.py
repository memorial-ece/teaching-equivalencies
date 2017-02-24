from Class import *
import random
def Gen2():
	random.seed(a=2)
	count = 0
	for x in range(1, 9):
		while (True):
			count += 1
			WORDS = open('words').readlines()
			ranlist = range(1, 2)
			a = random.uniform(0, 1)
			cb = random.choice([True, False])
			ab = random.choice([True, False])
			bb = random.choice([True, False])
			db = random.choice([True, False])
			word = random.choice(WORDS)
			Subj = random.choice(WORDS)
			Emale = word + "@mail.to"
			Crse = random.randrange(0000, 9999)
			sem1 = open('semesters').readlines()
			sem2 = random.choice(sem1)
			year1 = random.randrange(1970, 2017)
			year2 = str(year1)
			if count == 30:
				roa = 1
				break
			elif 4 > count > 2:
				person = Person.create(email=Emale, name=word)
			elif 2> count > 0:
				pseudoPeople = PseudoPeople.create(pseudo_email=Emale, pseudo_name=word)
			elif 6 > count > 4:
				course = Course.create(subject=Subj, course_num=Crse)
			elif 8 > count > 6:
				supervisionClass = SupervisionClass.create(description=word, weight=a)
			elif 10 > count > 8:
				projectClass = ProjectClass.create(weight=a, description=word)
			elif 16 > count > 14:
				term = Term.create(year=year2, session=sem2)
			elif 20 > count > 18:
				role = Role.create(role_name=word, view_only_you=ab, view_only_dept=bb, view_only_All=cb, edit_dept=db)
			elif 28 > count > 26:
				student = Student.create(student_name=word, student_email=Emale)
def Gen1():
	random.seed(a=2)
	print x
	count = 0
	while (count!=131):
		print count
		count += 1
		WORDS = open('words').readlines()
		ranlist = range(1, 10)
		ransam1 = random.choice(ranlist)
		ransam2 = random.choice(ranlist)
		ransam3 = random.choice(ranlist)
		ransam4 = random.choice(ranlist)
		ransam5 = random.choice(ranlist)
		a = random.uniform(0, 1)
		cb = random.choice([True, False])
		d = random.uniform(1, 12)
		e = random.uniform(1, 200)
		ab = random.choice([True,False])
		bb = random.choice([True, False])
		db = random.choice([True, False])
		word = random.choice(WORDS)
		Subj = random.choice(WORDS)
		Emale = word + "@mail.to"
		Crse = random.randrange(0000, 9999)
		sem1 = open('semesters').readlines()
		sem2 = random.choice(sem1)
		year1 = random.randrange(2016, 2018)
		year2 = str(year1)
		if 20 > count > 10:
			person = Person.create(email=Emale, name=word)
		elif 10 > count > 0:
			pseudoPeople = PseudoPeople.create(pseudo_email=Emale, pseudo_name=word)
		elif 30 > count > 20:
			course = Course.create(subject=Subj, course_num=Crse)
		elif 40 > count > 30:
			supervisionClass = SupervisionClass.create(description=word, weight=a )
		elif 50 > count > 40:
			projectClass = ProjectClass.create(weight=a, description=word)
		elif 60 > count > 50:
			courseGeneration = CourseGeneration.create(labs=e, credit_hours=d, title=word, course_id=ransam1)
		elif 70 > count > 60:
			term = Term.create(year=year2, session=sem2)
		elif 80 > count > 70:
			offering = Offering.create(students_taking=e, prof_id=ransam1, semester_id=ransam2, course_gen_id=ransam3)
		elif 90 > count > 80:
			role = Role.create(role_name=word, view_only_you=ab, view_only_dept=bb, view_only_All=cb, edit_dept=db)
		elif 100 > count > 90:
			supervision = Supervision.create(prof_id=ransam1, student_id=ransam2, supervision_class_id=ransam3,
											 semester_id=ransam4)
		elif 110 > count > 100:
			projectSupervision = ProjectSupervision.create(prof_id=ransam1, pseudo_id=ransam2, project_class_id=ransam4,
														   semester_id=ransam5)
		elif 120 > count > 110:
			student = Student.create(student_name=word, student_email=Emale)
		elif 130>count>120:
			rolePerson= RolePerson.create(prof_id=ransam1, role_id=ransam2)
def Gen3():
	year=1970
	term1=0
	count = 0
	while (True):
		term1 +=1
		term = Term.create(year=year, session=term1)
		if term1==5:
			term1=0
			year +=1
		if year==2020:
			break