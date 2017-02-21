from flask import *
import os
from Exporter import *
from Importer import *
from werkzeug.utils import *

app = Flask(__name__)
random.seed(a=2)
DATABASE = 'database.db'
db = SqliteDatabase(DATABASE)
UPLOAD_FOLDER=''
ALLOWED_EXTENSIONS=set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
								'favicon.ico', mimetype='image/vnd.microsoft.icon')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		a=request.form.get('Select')
		file = request.files['file']
		if a == 'Person':
			filenam='account-Person.csv'
		if a == 'Course':
			filenam='account-Course.csv'
		if a == 'CourseGeneration':
			filenam='account-CourseGeneration.csv'
		if a == 'Student':
			filenam='account-Student.csv'
		if a == 'Term':
			filenam='account-Term.csv'
		if a == 'Offering':
			filenam='account-Offering.csv'
		if a == 'Role':
			filenam='account-Role.csv'
		if a == 'SupervisionClass':
			filenam='account-SupervisionClass.csv'
		if a == 'ProjectClass':
			filenam='account-ProjectClass.csv'
		if a == 'PseudoPeople':
			filenam='account-PseudoPeople.csv'
		if a == 'RolePerson':
			filenam='account-RolePerson.csv'
		if a == 'ProjectSupervision':
			filenam='account-ProjectSupervision.csv'
		if a == 'Supervision':
			filenam='account-Supervision.csv'
		if a == 'Adjustment':
			filenam='account-Adjustment.csv'
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filenam))
			return redirect(url_for('upload',
									filename=filename))

	return render_template('upload.html')


@app.route("/export",  methods=['GET', 'POST'])
def docustomexport():
	if request.method == 'POST':
		a=request.form['Person']
		b=request.form['Supervision']
		c=request.form['SupervisionClass']
		d=request.form['Course']
		e=request.form['CourseGeneration']
		f=request.form['Student']
		g=request.form['Term']
		h=request.form['Offering']
		i=request.form['Role']
		j=request.form['ProjectClass']
		k=request.form['PseudoPeople']
		l=request.form['RolePerson']
		m=request.form['ProjectSupervision']
		n=request.form['Adjustment']
		if a == '1':
			exportProfile()
		if b == '1':
			exportSupervision()
		if c == '1':
			exportSupervisionClass()
		if d == '1':
			exportCourse()
		if e == '1':
			exportCourseGeneration()
		if f == '1':
			exportStudent()
		if g == '1':
			exportTerm()
		if h == '1':
			exportOffering()
		if i == '1':
			exportRole()
		if j == '1':
			exportProjectClass()
		if k == '1':
			exportPseudoPeople()
		if l == '1':
			exportRolePerson()
		if m == '1':
			exportProjectSupervision()
		if n == '1':
			exportAdjustment()
	return render_template('export.html')


@app.route("/import", methods=['GET', 'POST'])
def docustomimport():
	if request.method == 'POST':
		a=request.form['Person']
		b=request.form['Supervision']
		c=request.form['SupervisionClass']
		d=request.form['Course']
		e=request.form['CourseGeneration']
		f=request.form['Student']
		g=request.form['Term']
		h=request.form['Offering']
		i=request.form['Role']
		j=request.form['ProjectClass']
		k=request.form['PseudoPeople']
		l=request.form['RolePerson']
		m=request.form['ProjectSupervision']
		n=request.form['Adjustment']
		if a == '1':
			importProfile()
		if b == '1':
			importSupervision()
		if c == '1':
			importSupervisionClass()
		if d == '1':
			importCourse()
		if e == '1':
			importCourseGeneration()
		if f == '1':
			importStudent()
		if g == '1':
			importTerm()
		if h == '1':
			importOffering()
		if i == '1':
			importRole()
		if j == '1':
			importProjectClass()
		if k == '1':
			importPseudoPeople()
		if l == '1':
			importRolePerson()
		if m == '1':
			importProjectSupervision()
		if n == '1':
			importAdjustment()
	return render_template('import.html')


@app.route("/profile/<ID>/history")
def Profilehist(ID):
	person = Person.get(Person.ID == ID)
	supervision = Supervision.select().join(Person).where(Person.ID == ID).order_by(Supervision.SemesterID.desc())
	projectsupervision = ProjectSupervision.select().join(Person).where(Person.ID == ID).order_by(
		ProjectSupervision.SemesterID.desc())
	offering = Offering.select().join(Person).where(Person.ID == ID).order_by(Offering.SemesterID.desc())
	adjustment=Adjustment.select().join(Person).where(Person.ID == ID).order_by(Adjustment.AdjustmentID.desc())
	return render_template("profilehist.html", person=person,supervision=supervision,
						   projectsupervision=projectsupervision,offering=offering, adjustment=adjustment)

@app.route("/profile/<ID>")
def Profile(ID):
	person = Person.get(Person.ID == ID)
	supervision = Supervision.select().join(Person).where(Person.ID == ID).order_by(Supervision.SupervisionClassID.desc())
	projectsupervision = ProjectSupervision.select().join(Person).where(Person.ID == ID).order_by(
		ProjectSupervision.ProjectSupervisionID.desc())
	offering = Offering.select().join(Person).where(Person.ID == ID).order_by(Offering.OID.desc())
	adjustment=Adjustment.select().join(Person).where(Person.ID == ID).order_by(Adjustment.AdjustmentID.desc())
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
			db.connect()
			db.drop_tables(
			[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
			 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment,],safe=True)
			db.create_tables(
			[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
			 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment],safe=True)
			db.close()
		elif request.form['Full'] == 'Create':
			db.connect()
			db.create_tables(
				[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment],safe=True)
			db.close()
		elif request.form['Full'] == 'Drop':
			db.connect()
			db.drop_tables(
				[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment, ],safe=True)
			db.close()
	return render_template('reset.html')



if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)
