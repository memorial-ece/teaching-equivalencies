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


@app.route("/profile/<ID>")
def Profile(ID):
	lolerson = Person.get(Person.ID == ID)
	print (lolerson)
	return render_template("listcompanyforempl.html", lolerson=lolerson)


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
		con = sql.connect("database.db")
		c = con.cursor()
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
			supervisionClass = SupervisionClass.create(Grad=a, UGrad=b, Master=ci)
		elif 50 > count > 40:
			projectClass = ProjectClass.create(Grad=a, UGrad=b, Master=ci)
		elif 60 > count > 50:
			courseGeneration = CourseGeneration.create(Labs=a, CreditHours=d, Title=word, CRN=ransam1)
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
		elif 130> count >120:
			rolePerson= Role.select().join(RolePerson.RoleID).join(Person.ID).where(Person.ID==ransam1,RolePerson.RoleID==ransam2)

	return render_template('populate.html')


def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sql.connect(DATABASE)
	return db


@app.route('/listm', methods=['GET', 'POST'])
def listm():
	error=None
	if request.method == 'POST':
		FIXER=request.form['FIXER']
		ID=request.form['ID']
		SID = request.form['SID']
		SCID = request.form['SCID']
		PCID = request.form['PCID']
		PID = request.form['PID']
		OID = request.form['OID']
		CGID = request.form['CGID']
		SEM= request.form['SEM']
		SUDO= request.form['SUDO']
		AUCOM=request.form['AUCOM']
		ADJW=request.form['ADJW']
		AUDITDATE=datetime.date.today()
		print(FIXER)
		if FIXER=="1":
			q= Offering.update(ID = ID,CourseGenID=CGID,SemesterID=SEM).where(Offering.OID == OID)
			q.execute()
		elif FIXER=="2":
			q = ProjectSupervision.update(ID=ID, ProjectClassID=PCID, SemesterID=SEM).where(
				ProjectSupervision.ProjectSupervisionID == PID)
			q.execute()
		elif FIXER=="3":
			q = Supervision.update(ID=ID, SupervisionClassID=SCID, SemesterID=SEM).where(
				Supervision.SupervisionID == SID)
			q.execute()
		elif FIXER=="4":
			q = PseudoPeople.update(SupervisionID=SID, ProjectSupervisionID=PID).where(
				PseudoPeople.PseudoID == SUDO)
			q.execute()
		elif FIXER=="5":
			if not AUCOM=="":
				q = Adjustment.insert(ID=ID,ADJWeight=ADJW,AUDITDATE=AUDITDATE,AUDITCOMMENT=AUCOM)
				q.execute()
			else:
				error="comment not filled"
				return render_template("listcompany.html", Person=Person, Pseudo=PseudoPeople, Course=Course,
									   SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
									   ProjectSupervision=ProjectSupervision, Supervision=Supervision,
									   Adjustment=Adjustment,
									   RolePerson=RolePerson, Role=Role, Term=Term, Offering=Offering,
									   CourseGeneration=CourseGeneration, error=error)

	return render_template("listcompany.html", Person=Person, Pseudo=PseudoPeople, Course=Course,
							SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
							ProjectSupervision=ProjectSupervision, Supervision=Supervision, Adjustment=Adjustment,
							RolePerson=RolePerson, Role=Role, Term=Term, Offering=Offering,
							CourseGeneration=CourseGeneration, error=error)


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
	ViewOnlyYou = BooleanField()
	ViewOnlyDept = BooleanField()
	ViewOnlyAll = BooleanField()
	EditDept = BooleanField()


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
	class Meta:
		indexes = ((('ID','RoleID'),True),)

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


if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)
