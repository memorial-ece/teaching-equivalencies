from flask import *
import sqlite3 as sql
import os
import random
import datetime
from peewee import *
from peewee import Model

app = Flask(__name__)
random.seed(a=2)


@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
								'favicon.ico', mimetype='image/vnd.microsoft.icon')


DATABASE = 'database.db'
database = SqliteDatabase(DATABASE)


@app.route("/profile/<CID>")
def Profile(CID):
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	c = con.cursor()
	c.execute("select * from Person where ID = ?", (CID,))
	Person = c.fetchall()
	return render_template("listcompanyforempl.html", Person=Person, ID=CID)


# @app.route('/resettables')
# def bringdtatonline():
# 	con = sql.connect("database.db")
# 	c = con.cursor()
# 	c.execute('drop table if exists CourseGeneration')
# 	c.execute('drop table if exists Course')
# 	c.execute('drop table if exists Offering')
# 	c.execute('drop table if exists Term')
# 	c.execute('drop table if exists Supervision')
# 	c.execute('drop table if exists Person')
# 	c.execute('drop table if exists RolePerson')
# 	c.execute('drop table if exists Adjustment')
# 	c.execute('drop table if exists ProjectSupervision')
# 	c.execute('drop table if exists SupervisionClass')
# 	c.execute('drop table if exists PseudoPeople')
# 	c.execute('drop table if exists Role')
# 	c.execute('drop table if exists ProjectClass')
# c.execute('CREATE TABLE CourseGeneration(COURSEGEN int NOT NULL, CRN int, Weight REAL, PRIMARY KEY (COURSEGEN),FOREIGN KEY (CRN) REFERENCES Course (CRN))')
# c.execute('CREATE TABLE Course(CRN int, Subj text, Crse text, Sec text, Session text, Title text, PRIMARY KEY (CRN))')
# c.execute('CREATE TABLE Offering(OID int NOT NULL, Semester text, ID int, COURSEGEN int, PRIMARY KEY (OID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (COURSEGEN) REFERENCES CourseGeneration (COURSEGEN))')
# c.execute('CREATE TABLE Person(ID int NOT NULL, Email text NOT NULL, Name text NOT NULL, PRIMARY KEY (ID))')
# c.execute('CREATE TABLE Term(Semester text NOT NULL, PRIMARY KEY (Semester))')
# #ADD THE AUTOIMCREMENT STATMENT BACK TO ADJ ID, AUDIT ID, AND THE DATE
# c.execute('CREATE TABLE RolePerson(ID int, RoleID int, FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (RoleID) REFERENCES Role (RoleID))')
# c.execute('CREATE TABLE Role(RoleID int, ViewOnlyYou int,ViewOnlyDept int, ViewOnlyAll int, EditDept int, PRIMARY KEY (RoleID))')
# c.execute('CREATE TABLE ProjectSupervision(ProjectSupervisionID int NOT NULL, ID int,PseudoID int, ProjectClassID int, PRIMARY KEY(ProjectSupervisionID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (ProjectClassID) REFERENCES ProjectClass (ProjectClassID), FOREIGN KEY (PseudoID) REFERENCES PseudoPeople (PseudoID))')
# c.execute('CREATE TABLE SupervisionClass(SupervisionClassID int NOT NULL, Graduate REAL, Undergrad REAL, Masters REAL, PRIMARY KEY (SupervisionClassID))')
# c.execute('CREATE TABLE PseudoPeople(PseudoID int NOT NULL, PseudoName text NOT NULL, Email text, Team text, int, PRIMARY KEY (PseudoID))')
# c.execute('CREATE TABLE ProjectClass(ProjectClassID int NOT NULL, Graduate REAL, Undergrad REAL, Masters REAL, PRIMARY KEY (ProjectClassID))')
# c.execute('CREATE TABLE Adjustment(AdjustmentID INTEGER PRIMARY KEY AUTOINCREMENT, ADJTO int NOT NULL, ID int, ADJWeight REAL,  AUDITDATE date, AUDITCOMMENT text, FOREIGN KEY (ID) REFERENCES Person (ID))')
# c.execute('CREATE TABLE Supervision(SupervisionID int NOT NULL, ID int, PseudoID int, SupervisionClassID int, PRIMARY KEY (SupervisionID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (SupervisionClassID) REFERENCES SupervisionClass (SupervisionClassID), FOREIGN KEY (PseudoID) REFERENCES PseudoPeople (PseudoID))')
# 	con.commit()
# 	ID=random.randrange(0,100)
# 	print (ID)
# 	return render_template('reset.html')

@app.route('/populate', methods=["GET", "POST"])
def populate():
	count = 0
	if 'roa' in locals():
		random.seed(a=1)
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
		cb = random.uniform(0, 1)
		d = random.uniform(1, 12)
		e = random.uniform(1, 200)
		word = random.choice(WORDS)
		Subj = random.choice(WORDS)
		Emale = word + "@mail.to"
		Teammates = ("no team", "a Team")
		Crse = random.randrange(0000, 9999)
		con = sql.connect("database.db")
		c = con.cursor()
		sem1 = open('semesters').readlines()
		sem2 = random.choice(sem1)
		year1 = random.randrange(1970, 2017)
		year2 = str(year1)
		if count == 121:
			roa = 1
			break
		elif 20 > count > 10:
			person = Person.create(Email=Emale, Name=word)
		# c.execute ('INSERT INTO Person (ID,Email,Name) VALUES (?, ?, ?)', (ID, Emale, word))
		# con.commit()
		elif 10 > count > 0:
			pseudoPeople = PseudoPeople.create(PEmail=Emale, PName=word)
		# c.execute('insert into PseudoPeople (PseudoID,Email,PseudoName,Team) Values (?,?,?,?)', (ID, Emale, word,myteam))
		# con.commit()
		elif 30 > count > 20:
			course = Course.create(Subj=Subj, Crse=Crse)
		# c.execute('insert into Course (CRN,Subj,Crse,Sec,Session,Title) Values (?,?,?,?,?,?)', (CRN,Subj,Crse,Sec,Session,Title))
		# con.commit()
		elif 40 > count > 30:
			supervisionClass = SupervisionClass.create(Grad=a, UGrad=b, Master=cb)
		# c.execute('insert into SupervisionClass(SupervisionClassID,Graduate,Undergrad,Masters) Values (?,?,?,?)', (ID,a,b,cb))
		# con.commit()
		elif 50 > count > 40:
			projectClass = ProjectClass.create(Grad=a, UGrad=b, Master=cb)
		# c.execute('insert into ProjectClass(ProjectClassID,Graduate,Undergrad,Masters) Values (?,?,?,?)', (ID,a,b,cb))
		# con.commit()
		elif 60 > count > 50:
			courseGeneration = CourseGeneration.create(Labs=a, CreditHours=d, Title=word, CRN=ransam1)
		# c.execute('insert into CourseGeneration(COURSEGEN,CRN,Weight) Values (?,?,?)', (ID,CRN,a))
		# con.commit()
		elif 70 > count > 60:
			term = Term.create(Year=year2, Session=sem2)
		# c.execute('insert into Term(Semester) Values (?)', (put,))
		# con.commit()
		elif 80 > count > 70:
			offering = Offering.create(StudentsTaking=e, ID=ransam1, SemesterID=ransam2, CourseGenID=ransam3)
		# c.execute('insert into Offering (OID) Values (?)', (ID,))
		# con.commit()
		elif 90 > count > 80:
			role = Role.create(ViewOnlyYou=a, ViewOnlyDept=b, ViewOnlyAll=cb, EditDept=d)
		# c.execute('insert into Role(RoleID) Values (?)', (ID,))
		# con.commit()
		elif 100 > count > 90:
			supervision = Supervision.create(ID=ransam1, StudentID=ransam2, SupervisionClassID=ransam3,
												SemesterID=ransam4)
		# c.execute('insert into Supervision (SupervisionID) Values (?)', (ID,))
		# con.commit()
		elif 110 > count > 100:
			projectSupervision = ProjectSupervision.create(ID=ransam1, PseudoID=ransam2, StudentID=ransam3,
															ProjectClassID=ransam4, SemesterID=ransam5)
		# c.execute('insert into ProjectSupervision (ProjectSupervisionID) Values (?)', (ID,))
		# con.commit()
		elif 120 > count > 110:
			student = Student.create(SName=word, SEmail=Emale)
	return render_template('populate.html')


def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sql.connect(DATABASE)
	return db


@app.route('/listm', methods=['GET', 'POST'])
def listm():

	# if request.method == 'POST':
	# 	con = sql.connect("database.db")
	# 	con.row_factory = sql.Row
	# 	c = con.cursor()
	# 	FIXER=request.form['FIXER']
	# 	ID=request.form['ID']
	# 	SID = request.form['SID']
	# 	SCID = request.form['SCID']
	# 	PCID = request.form['PCID']
	# 	PID = request.form['PID']
	# 	OID = request.form['OID']
	# 	CGID = request.form['CGID']
	# 	SEM= request.form['SEM']
	# 	SUDO= request.form['SUDO']
	# 	AUCOM=request.form['AUCOM']
	# 	ADJTO=request.form['ADJTO']
	# 	ADJW=request.form['ADJW']
	# 	AUDITDATE=datetime.date.today()
	# 	print(FIXER)
	# 	if FIXER=="1":
	# 		c.execute("update Offering set ID = ?,COURSEGEN=?,Semester=? where OID = ?", (ID,CGID,SEM,OID))
	# 		con.commit()
	# 	elif FIXER=="2":
	# 		c.execute("update ProjectSupervision set ID = ?,Semester=?,ProjectClassID=? where ProjectSupervisionID = ?", (ID, SEM,PCID,PID))
	# 		con.commit()
	# 	elif FIXER=="3":
	# 		c.execute("update Supervision set ID = ?,Semester=?,SupervisionClassID=? where SupervisionID = ?", (ID, SEM,SCID,SID))
	# 		con.commit()
	# 	elif FIXER=="4":
	# 		c.execute("update PseudoPeople set SupervisionID=?,ProjectSupervisionID=? where PseudoID=?",(SID,PID,SUDO))
	# 		con.commit()
	# 	elif FIXER=="5":
	# 		if not AUCOM=="":
	# 			c.execute("Insert into Adjustment (ADJTO, ID, ADJWeight,AUDITDATE,AUDITCOMMENT) values (?,?,?,?,?)",(ADJTO,ID,ADJW,AUDITDATE,AUCOM))
	# 			con.commit()
	# 		else:
	# 			error="comment not filled"
	# 			return render_template("listcompany.html", error=error, Person=Person, Pseudo=Pseudo, Course=Course,SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,ProjectSupervision=ProjectSupervision, Supervision=Supervison, Adjustment=Adjustment,RolePerson=RolePerson, Role=Role, Term=Term, Offering=Offering,CourseGeneration=CourseGeneration)
	return render_template("listcompany.html", Person=Person, Pseudo=PseudoPeople, Course=Course,
							SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
							ProjectSupervision=ProjectSupervision, Supervision=Supervision, Adjustment=Adjustment,
							RolePerson=RolePerson, Role=Role, Term=Term, Offering=Offering,
							CourseGeneration=CourseGeneration)


@app.route('/Dashboard')
@app.route('/index')
@app.route('/', methods=["GET"])
def index():
	return render_template("Home.html")


class Person(Model):
	Name = TextField()
	Email = TextField()
	ID = IntegerField(unique=True, primary_key=True, null=False)


class Course(Model):
	CRN = IntegerField(unique=True, primary_key=True, null=False)
	Subj = TextField()
	Crse = IntegerField()


class CourseGeneration(Model):
	CourseGenID = IntegerField(unique=True, primary_key=True, null=False)
	Labs = IntegerField()
	CreditHours = IntegerField()
	Title = TextField()
	CRN = ForeignKeyField(Course, related_name='CourseGenerations')


class Student(Model):
	StudentID = IntegerField(primary_key=True, unique=True, null=False)
	SName = TextField()
	SEmail = TextField()


class Term(Model):
	SemesterID = IntegerField(unique=True, primary_key=True, null=False)
	Year = DateField()
	Session = IntegerField()


class Offering(Model):
	OID = IntegerField(unique=True, primary_key=True, null=False, )
	StudentsTaking = IntegerField()
	ID = ForeignKeyField(Person, related_name='Offerings')
	SemesterID = ForeignKeyField(Term, related_name='Offerings')
	CourseGenID = ForeignKeyField(CourseGeneration, related_name='Offerings')


class Role(Model):
	RoleID = IntegerField(primary_key=True, unique=True, null=False)
	ViewOnlyYou = IntegerField()
	ViewOnlyDept = IntegerField()
	ViewOnlyAll = IntegerField()
	EditDept = IntegerField()


class SupervisionClass(Model):
	SupervisionClassID = IntegerField(primary_key=True, unique=True, null=False)
	Grad = FloatField()
	UGrad = FloatField()
	Master = FloatField()


class ProjectClass(Model):
	ProjectClassID = IntegerField(primary_key=True, unique=True, null=False)
	Grad = FloatField()
	UGrad = FloatField()
	Master = FloatField()


class PseudoPeople(Model):
	PseudoID = IntegerField(primary_key=True, unique=True, null=False)
	PName = TextField()
	PEmail = TextField()


class RolePerson(Model):
	ID = ForeignKeyField(Person, related_name='RolePersons')
	RoleID = ForeignKeyField(Role, related_name='RolePersons')


class ProjectSupervision(Model):
	ProjectSupervisionID = IntegerField(primary_key=True, unique=True, null=False)
	ID = ForeignKeyField(Person, related_name='ProjectSupervisions')
	PseudoID = ForeignKeyField(PseudoPeople, related_name='ProjectSupervisions')
	ProjectClassID = ForeignKeyField(ProjectClass, related_name='ProjectSupervisions')
	SemesterID = ForeignKeyField(Term, related_name='ProjectSupervisions')


class Supervision(Model):
	SupervisionID = IntegerField(primary_key=True, unique=True, null=False)
	ID = ForeignKeyField(Person, related_name='Supervisions')
	StudentID = ForeignKeyField(Student, related_name='Supervisions')
	SupervisionClassID = ForeignKeyField(SupervisionClass, related_name='Supervisions')
	SemesterID = ForeignKeyField(Term, related_name='Supervisions')


class Adjustment(Model):
	AdjustmentID = IntegerField(primary_key=True, unique=True, null=False)
	ADJWeight = FloatField()
	AUDITDATE = DateTimeField()
	AUDITCOMMENT = TextField()
	ID = ForeignKeyField(Person, related_name='Adjustments')


@app.route('/peewee')
def create_tables():
	database.connect()
	database.drop_tables(
		[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
		 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment])
	database.create_tables(
		[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
		 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment])
	return render_template('reset.html')


@app.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p><a href="/">home</a>')


if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)
