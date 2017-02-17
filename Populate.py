from PeeweeClass import *
import random
def Gen2():
	count = 0
	while (True):
		count += 1
		WORDS = open('words').readlines()
		ranlist = range(1, 2)
		ransam1 = random.choice(ranlist)
		ransam2 = random.choice(ranlist)
		ransam3 = random.choice(ranlist)
		ransam4 = random.choice(ranlist)
		ransam5 = random.choice(ranlist)
		a = random.uniform(0, 1)
		b = random.uniform(0, 1)
		ci = random.uniform(0, 1)
		cb = random.choice([True, False])
		d = random.uniform(1, 2)
		e = random.uniform(1, 2)
		ab = random.choice([True, False])
		bb = random.choice([True, False])
		db = random.choice([True, False])
		word = random.choice(WORDS)
		Subj = random.choice(WORDS)
		Emale = word + "@mail.to"
		Teammates = ("no team", "a Team")
		Crse = random.randrange(0000, 9999)
		sem1 = open('semesters').readlines()
		sem2 = random.choice(sem1)
		year1 = random.randrange(1970, 2017)
		year2 = str(year1)
		if count == 30:
			roa = 1
			break
		elif 4 > count > 2:
			person = Person.create(Email=Emale, Name=word)
		elif 2> count > 0:
			pseudoPeople = PseudoPeople.create(PEmail=Emale, PName=word)
		elif 6 > count > 4:
			course = Course.create(Subj=Subj, Crse=Crse)
		elif 8 > count > 6:
			supervisionClass = SupervisionClass.create(Description=word, Weight=a)
		elif 10 > count > 8:
			projectClass = ProjectClass.create(Weight=a, Description=word)
		elif 16 > count > 14:
			term = Term.create(Year=year2, Session=sem2)
		elif 20 > count > 18:
			role = Role.create(ViewOnlyYou=ab, ViewOnlyDept=bb, ViewOnlyAll=cb, EditDept=db)
		elif 28 > count > 26:
			student = Student.create(SName=word, SEmail=Emale)
def Gen1():
	count = 0
	while (True):
		count += 1
		WORDS = open('words').readlines()
		ranlist = range(1, 10)
		ransam1 = random.choice(ranlist)
		ransam2 = random.choice(ranlist)
		ransam3 = random.choice(ranlist)
		ransam4 = random.choice(ranlist)
		ransam5 = random.choice(ranlist)
		a = random.uniform(0, 1)
		b = random.uniform(0, 1)
		ci= random.uniform(0, 1)
		cb = random.choice([True, False])
		d = random.uniform(1, 12)
		e = random.uniform(1, 200)
		ab = random.choice([True,False])
		bb = random.choice([True, False])
		db = random.choice([True, False])
		word = random.choice(WORDS)
		Subj = random.choice(WORDS)
		Emale = word + "@mail.to"
		Teammates = ("no team", "a Team")
		Crse = random.randrange(0000, 9999)
		sem1 = open('semesters').readlines()
		sem2 = random.choice(sem1)
		year1 = random.randrange(1970, 2017)
		year2 = str(year1)
		if count == 131:
			roa = 1
			break
		elif 20 > count > 10:
			person = Person.create(Email=Emale, Name=word)
		elif 10 > count > 0:
			pseudoPeople = PseudoPeople.create(PEmail=Emale, PName=word)
		elif 30 > count > 20:
			course = Course.create(Subj=Subj, Crse=Crse)
		elif 40 > count > 30:
			supervisionClass = SupervisionClass.create(Description=word, Weight=a )
		elif 50 > count > 40:
			projectClass = ProjectClass.create(Weight=a, Description=word)
		elif 60 > count > 50:
			courseGeneration = CourseGeneration.create(Labs=e, CreditHours=d, Title=word, CRN=ransam1)
		elif 70 > count > 60:
			term = Term.create(Year=year2, Session=sem2)
		elif 80 > count > 70:
			offering = Offering.create(StudentsTaking=e, ID=ransam1, SemesterID=ransam2, CourseGenID=ransam3)
		elif 90 > count > 80:
			role = Role.create(ViewOnlyYou=ab, ViewOnlyDept=bb, ViewOnlyAll=cb, EditDept=db)
		elif 100 > count > 90:
			supervision = Supervision.create(ID=ransam1, StudentID=ransam2, SupervisionClassID=ransam3,
												SemesterID=ransam4)
		elif 110 > count > 100:
			projectSupervision = ProjectSupervision.create(ID=ransam1, PseudoID=ransam2, StudentID=ransam3,
															ProjectClassID=ransam4, SemesterID=ransam5)
		elif 120 > count > 110:
			student = Student.create(SName=word, SEmail=Emale)
		elif 130>count>120:
			rolePerson= RolePerson.create(ID=ransam1,RoleID=ransam2)