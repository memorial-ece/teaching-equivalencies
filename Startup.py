from flask import *
import os
from Populate import *

app = Flask(__name__)
random.seed(a=2)
DATABASE = 'database.db'
database = SqliteDatabase(DATABASE)

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
								'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/profile/<ID>")
def Profile(ID):
	person = Person.get(Person.ID == ID)
	supervision = Supervision.select().join(Person).where(Person.ID == ID)
	projectsupervision = ProjectSupervision.select().join(Person).where(Person.ID == ID)
	offering = Offering.select().join(Person).where(Person.ID == ID)
	adjustment=Adjustment.select().join(Person).where(Person.ID == ID)
	return render_template("profile.html", person=person,supervision=supervision,
						   projectsupervision=projectsupervision,offering=offering, adjustment=adjustment)

@app.route('/populate', methods=["GET", "POST"])
def populate():
	if request.method == 'POST':
		if request.form['Full'] == "Full gen":
			Gen1()
		elif request.form['Full'] == "Simple gen":
			Gen2()
	return render_template('populate.html')


@app.route('/listm', methods=['GET', 'POST'])
def listm():
	if request.method == 'POST':
		if request.form['subm1'] == "submit1":
			labs=request.form['Labs']
			credit=request.form['Credit']
			title=request.form['Title']
			cRN=request.form['CRN']
			CourseGeneration.create(Labs=labs, CreditHours=credit, Title=title, CRN=cRN)
		elif request.form['subm1'] == "submit2":
			semesterID1 = request.form['SemesterID1']
			student = request.form['stu']
			iD1 = request.form['ID1']
			courseGenID = request.form['CourseGenID']
			Offering.create(StudentsTaking=student, ID=iD1, SemesterID=semesterID1, CourseGenID=courseGenID)
		elif request.form['subm1'] == "submit3":
			sID = request.form['StudentID']
			superclass = request.form['SupervisionClassID']
			semesterID2 = request.form['SemesterID2']
			iD2 = request.form['ID2']
			Supervision.create(ID=iD2, StudentID=sID, SupervisionClassID=superclass,SemesterID=semesterID2)
		elif request.form['subm1'] == "submit4":
			iD3 = request.form['ID3']
			semesterID3 = request.form['SemesterID3']
			pseudoID = request.form['PseudoID']
			projectClassID = request.form['ProjectClassID']
			ProjectSupervision.create(ID=iD3, PseudoID=pseudoID, ProjectClassID=projectClassID,SemesterID=semesterID3)
		elif request.form['subm1']== "submit5":
			iD4 = request.form['ID4']
			ADJWeight = request.form['ADJWeight']
			AUDITCOMMENT = request.form['AUDITCOMMENT']
			Adjustment.create(ID=iD4, ADJWeight=ADJWeight,AUDITCOMMENT=AUDITCOMMENT)
	return render_template("masterlist.html", Person=Person, Pseudo=PseudoPeople, Course=Course,
							SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
							ProjectSupervision=ProjectSupervision, Supervision=Supervision, Adjustment=Adjustment,
							RolePerson=RolePerson, Role=Role, Term=Term, Offering=Offering,
							CourseGeneration=CourseGeneration, Student=Student)


@app.route('/Dashboard')
@app.route('/index')
@app.route('/', methods=["GET"])
def index():
	return render_template("home.html")

@app.route('/peeweetable', methods=["GET", "POST"])
def peeweetable():
	if request.method == 'POST':
		if request.form['Full'] == 'Drop and ReCreate':
			database.connect()
			database.drop_tables(
			[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
			 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment,],safe=True)
			database.create_tables(
			[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
			 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment],safe=True)
			database.close()
		elif request.form['Full'] == 'Create':
			database.connect()
			database.create_tables(
				[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment],safe=True)
			database.close()
		elif request.form['Full'] == 'Drop':
			database.connect()
			database.drop_tables(
				[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment, ],safe=True)
			database.close()
	return render_template('reset.html')


if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)
