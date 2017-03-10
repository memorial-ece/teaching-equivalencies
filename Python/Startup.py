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
import sys
from flask import *
from werkzeug.utils import *
from orginization_functions import *
from Exporter import *
reload(sys)
sys.setdefaultencoding('utf-8')

course_number = re.compile('[0-9W]{4} [A-Z][a-z]+')
numeric = re.compile('^[0-9]+$')
special_topics = re.compile('[0-9]{4}-[0-9]{4} [A-Z][a-z]+')
app = Flask(__name__)
DATABASE = 'database.db'
db = SqliteDatabase(DATABASE)
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'favicon.ico', mimetype='image/vnd.microsoft.icon')


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/export", methods=['GET', 'POST'])
def docustomexport():
	if request.method == 'POST':
		selector = request.form.get('Select')
		if selector == 'Person':
			export_profile()
			return send_file('table_Person.csv')
		if selector == 'Supervision':
			export_supervision()
			return send_file('table_Supervision.csv')
		if selector == 'SupervisionClass':
			export_supervision_class()
			return send_file('table_SupervisionClass.csv')
		if selector == 'Course':
			export_course()
			return send_file('table_Course.csv')
		if selector == 'CourseGeneration':
			export_course_generation()
			return send_file('table_CourseGeneration.csv')
		if selector == 'Student':
			export_student()
			return send_file('table_Student.csv')
		if selector == 'Term':
			export_term()
			return send_file('table_Term.csv')
		if selector == 'Offering':
			export_offering()
			return send_file('table_Offering.csv')
		if selector == 'Role':
			export_role()
			return send_file('table_Role.csv')
		if selector == 'ProjectClass':
			export_project_class()
			return send_file('table_ProjectClass.csv')
		if selector == 'PseudoPeople':
			export_ProjectTeam()
			return send_file('table_PseudoPeople.csv')
		if selector == 'RolePerson':
			export_role_person()
			return send_file('table_RolePerson.csv')
		if selector == 'ProjectSupervision':
			export_project_supervision()
			return send_file('table_ProjectSupervision.csv')
		if selector == 'Adjustment':
			export_adjustment()
			return send_file('table_Adjustment.csv')
	return render_template('export.html')


@app.route('/offering')
def offergen():
	# semester_quick_gen(fromD)
	semester_quick_gen(2010)
	# person(name,email)
	person('Mr. Anderson','jonathan.anderson@mun.ca',2012,3)
	# student(name, email)
	student('Juteau','2011205085')
	student('Derakhshan Nik','201509962')
	student('Nguyen','201051471')
	# superC(BOOLDoyouwanttocreateanewone,Description,Weight)
	superC(False,'lol',400)
	# supera(TermS,profid,Studentid,supervisoncalss,session)
	supera(2015,1,1,1,1)
	supera(2015,1,2,1,2)
	supera(2015,1,1,1,3)
	supera(2015,1,2,1,3)
	supera(2015,1,3,1,3)
	# offer(year,code,session,profid,numberofstudents)
	offer(2015,1020,2,1,1,3)
	offer(2015,3891,1,1,1,1)
	offer(2015,8894,2,1,1,1)
	return redirect('/listm')


@app.route("/course/<id>", methods=['GET', 'POST'])
def Coursehist(id):
	list2=[]
	course = Course.get(Course.id==id)
	generation = (CourseGeneration.select().join(Course).where(Course.id == id))
	list1=informationXchange(generation,list2)
	return render_template("course.html", course=course,generation=generation,list1=list1)


@app.route("/c/<id>", methods=['GET', 'POST'])
def Courseh(id):
	list2=[]
	course = Course.get(Course.code==id)
	generation = (CourseGeneration.select().join(Course).where(Course.code == id))
	list1=informationXchange(generation,list2)
	return render_template("course.html", course=course,generation=generation,list1=list1)


@app.route("/profile/<prof_id>/history", methods=['GET', 'POST'])
def Profilehist(prof_id):
	person = Person.get(Person.id == prof_id)
	supervision = (Supervision
				   .select()
				   .join(Person)
				   .where(Person.id == prof_id)
				   .order_by(Supervision.semester_id.desc()))
	projectsupervision = (ProjectSupervision
						  .select()
						  .join(Person)
						  .where(Person.id == prof_id)
						  .order_by(ProjectSupervision.semester_id.desc()))
	offering = (Offering
				.select()
				.join(Person)
				.where(Person.id == prof_id)
				.order_by(Offering.semester_id.desc()))
	adjustment = (Adjustment
				  .select()
				  .join(Person)
				  .where(Person.id == prof_id)
				  .order_by(Adjustment.id.desc()))
	Stotal = 0
	Atotal = 0
	Ptotal = 0
	Ototal = 0
	Stotal = (Supervision
			  .select()
			  .where(Supervision.prof_id == prof_id)
			  .join(SupervisionClass)
			  .select(fn.SUM(SupervisionClass.weight))
			  .scalar())
	Atotal = (Person
			  .select()
			  .where(Person.id == prof_id)
			  .join(Adjustment)
			  .select(fn.SUM(Adjustment.weight))
			  .scalar())
	Ototal = (Offering
			  .select()
			  .where(Offering.prof_id == prof_id)
			  .select(fn.SUM(Offering.weight))
			  .scalar())
	Ptotal = (ProjectSupervision
			  .select()
			  .where(ProjectSupervision.prof_id == prof_id)
			  .join(ProjectClass)
			  .select(fn.SUM(ProjectClass.weight))
			  .scalar())
	defi=deficit(prof_id)
	if Atotal is None:
		Atotal = 0
	if Stotal is None:
		Stotal = 0
	if Ptotal is None:
		Ptotal = 0
	total = Ptotal + Atotal + Stotal + Ototal - defi
	if request.method == 'POST':
		if request.form['subm1'] == "submit2":
			# semesterID1 = request.form['SemesterID1']
			# student = request.form['stu']
			# iD1 = request.form['ID1']
			# courseGenID = request.form['CourseGenID']
			weight = request.form['weight']
			myid = request.form['myid']
			update=Offering.update(weight=weight).where(Offering.id==myid)
			update.execute()
	return render_template("profilehist.html", person=person, supervision=supervision,prof_id=prof_id,
						   projectsupervision=projectsupervision, offering=offering, adjustment=adjustment,total=total,Stotal=Stotal,Ototal=Ototal)


@app.route("/profile/<prof_id>", methods=['GET', 'POST'])
def Profile(prof_id):
	now = datetime.datetime.now()
	year1 = now.year
	person = Person.get(Person.id == prof_id)
	supervision = (Supervision
				   .select()
				   .join(Person)
				   .where(Person.id == prof_id)
				   .order_by(Supervision.semester_id.desc()))
	projectsupervision = (ProjectSupervision
						  .select()
						  .join(Person)
						  .where(Person.id == prof_id)
						  .order_by(ProjectSupervision.semester_id.desc()))
	offering = (Offering
				.select()
				.join(Person)
				.where(Person.id == prof_id)
				.order_by(Offering.semester_id.desc()))
	adjustment = (Adjustment
				  .select()
				  .join(Person)
				  .where(Person.id == prof_id)
				  .order_by(Adjustment.id.desc()))
	Stotal = 0
	Atotal = 0
	Ptotal = 0
	Ototal = 0
	Stotal = (Supervision
			  .select()
			  .where(Supervision.prof_id == prof_id)
			  .join(SupervisionClass)
			  .select(fn.SUM(SupervisionClass.weight))
			  .scalar())
	Atotal = (Person
			  .select()
			  .where(Person.id == prof_id)
			  .join(Adjustment)
			  .select(fn.SUM(Adjustment.weight))
			  .scalar())
	Ototal = (Offering
			  .select()
			  .where(Offering.prof_id == prof_id)
			  .select(fn.SUM(Offering.weight))
			  .scalar())
	Ptotal = (ProjectSupervision
			  .select()
			  .where(ProjectSupervision.prof_id == prof_id)
			  .join(ProjectClass)
			  .select(fn.SUM(ProjectClass.weight))
			  .scalar())
	defi = deficit(prof_id)
	if Atotal is None:
		Atotal = 0
	if Stotal is None:
		Stotal = 0
	if Ptotal is None:
		Ptotal = 0
	total = Ptotal + Atotal + Stotal + Ototal - defi
	if request.method == 'POST':
		if request.form['subm1'] == "submit2":
			# semesterID1 = request.form['SemesterID1']
			# student = request.form['stu']
			# iD1 = request.form['ID1']
			# courseGenID = request.form['CourseGenID']
			weight = request.form['weight']
			myid = request.form['myid']
			update = Offering.update(weight=weight).where(Offering.id == myid)
			update.execute()
	return render_template("profile.html", person=person, supervision=supervision, prof_id=prof_id,
						   projectsupervision=projectsupervision, offering=offering, adjustment=adjustment, total=total,
						   Stotal=Stotal, Ototal=Ototal)


@app.route('/listm', methods=['GET', 'POST'])
def listm():
	if request.method == 'POST':
		if request.form['subm1'] == "submit1":
			labs = request.form['Labs']
			credit = request.form['Credit']
			title = request.form['Title']
			cRN = request.form['CRN']
			CourseGeneration.create(labs=labs, credit_hours=credit, title=title, course_id=cRN)
		elif request.form['subm1'] == "submit2":
			semesterID1 = request.form['SemesterID1']
			student = request.form['stu']
			iD1 = request.form['ID1']
			courseGenID = request.form['CourseGenID']
			Offering.create(enrolment=student, prof_id=iD1, semester_id=semesterID1, course_gen_id=courseGenID)
		elif request.form['subm1'] == "submit3":
			sID = request.form['StudentID']
			superclass = request.form['SupervisionClassID']
			semesterID2 = request.form['SemesterID2']
			iD2 = request.form['ID2']
			Supervision.create(prof_id=iD2, student_id=sID, supervision_class_id=superclass, semester_id=semesterID2)
		elif request.form['subm1'] == "submit4":
			iD3 = request.form['ID3']
			semesterID3 = request.form['SemesterID3']
			pseudoID = request.form['PseudoID']
			projectClassID = request.form['ProjectClassID']
			ProjectSupervision.create(prof_id=iD3, pTeam=pseudoID, project_class_id=projectClassID,
									  semester_id=semesterID3)
		elif request.form['subm1'] == "submit5":
			iD4 = request.form['ID4']
			ADJWeight = request.form['ADJWeight']
			AUDITCOMMENT = request.form['AUDITCOMMENT']
			Adjustment.create(prof_id=iD4, weight=ADJWeight, audit_comment=AUDITCOMMENT)
	return render_template("masterlist.html", Person=Person, ProjectTeam=ProjectTeam, Course=Course,
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
			# removed Course and CourseGeneration
			db.drop_tables(
				[Person,  Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, ProjectTeam, Student, Adjustment],safe=True)
			db.create_tables(
				[Person, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, ProjectTeam, Student, Adjustment],safe=True)
			db.close()
		elif request.form['Full'] == 'Create':
			db.connect()
			db.create_tables(
				[Person, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, ProjectTeam, Student, Adjustment],safe=True)
			db.close()
		elif request.form['Full'] == 'Drop':
			db.connect()
			db.drop_tables(
				[Person, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, ProjectTeam, Student, Adjustment],safe=True)
			db.close()
	return render_template('reset.html')


if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)
