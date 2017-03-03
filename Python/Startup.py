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
import datetime
import re
import sys

from flask import *
from werkzeug.utils import *
from Exporter import *
from Importer import *

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


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		selector = request.form.get('Select')
		file = request.files['file']
		if selector == 'Person':
			filename = 'table_Person.csv'
		if selector == 'Course':
			filename = 'table_Course.csv'
		if selector == 'CourseGeneration':
			filename = 'table_CourseGeneration.csv'
		if selector == 'Student':
			filename = 'table_Student.csv'
		if selector == 'Term':
			filename = 'table_Term.csv'
		if selector == 'Offering':
			filename = 'table_Offering.csv'
		if selector == 'Role':
			filename = 'table_Role.csv'
		if selector == 'SupervisionClass':
			filename = 'table_SupervisionClass.csv'
		if selector == 'ProjectClass':
			filename = 'table_ProjectClass.csv'
		if selector == 'PseudoPeople':
			filename = 'table_PseudoPeople.csv'
		if selector == 'RolePerson':
			filename = 'table_RolePerson.csv'
		if selector == 'ProjectSupervision':
			filename = 'table_ProjectSupervision.csv'
		if selector == 'Supervision':
			filename = 'table_Supervision.csv'
		if selector == 'Adjustment':
			filename = 'table_Adjustment.csv'
		if file and allowed_file(file.filename):
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('upload.html'))
	return render_template('upload.html')


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
			export_pseudo_people()
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


@app.route("/import", methods=['GET', 'POST'])
def docustomimport_():
	if request.method == 'POST':
		selector = request.form.get('Select')
		if selector == 'Person':
			import_profile()
		if selector == 'Supervision':
			import_supervision()
		if selector == 'SupervisionClass':
			import_supervision_class()
		if selector == 'Course':
			import_course()
		if selector == 'CourseGeneration':
			import_course_generation()
		if selector == 'Student':
			import_student()
		if selector == 'Term':
			import_term()
		if selector == 'Offering':
			import_offering()
		if selector == 'Role':
			import_role()
		if selector == 'ProjectClass':
			import_project_class()
		if selector == 'PseudoPeople':
			import_pseudo_people()
		if selector == 'RolePerson':
			import_role_person()
		if selector == 'ProjectSupervision':
			import_project_supervision()
		if selector == 'Adjustment':
			import_adjustment()
	return render_template('import.html')


@app.route("/profile/<prof_id>/history")
def Profilehist(prof_id):
	person = Person.get(Person.prof_id == prof_id)
	supervision = (Supervision
				   .select()
				   .join(Person)
				   .where(Person.prof_id == prof_id)
				   .order_by(Supervision.semester_id.desc()))
	projectsupervision = (ProjectSupervision
						  .select()
						  .join(Person)
						  .where(Person.prof_id == prof_id)
						  .order_by(ProjectSupervision.semester_id.desc()))
	offering = (Offering
				.select()
				.join(Person)
				.where(Person.prof_id == prof_id)
				.order_by(Offering.semester_id.desc()))
	adjustment = (Adjustment
				  .select()
				  .join(Person)
				  .where(Person.prof_id == prof_id)
				  .order_by(Adjustment.adjustment_id.desc()))
	return render_template("profilehist.html", person=person, supervision=supervision,
						   projectsupervision=projectsupervision, offering=offering, adjustment=adjustment)


@app.route("/profile/<prof_id>")
def Profile(prof_id):
	now = datetime.datetime.now()
	year1 = now.year
	person = Person.get(Person.prof_id == prof_id)
	supervision = (Supervision.select()
				   .join(Person, on=(Supervision.prof_id == Person.prof_id))
				   .join(Term, on=(Supervision.semester_id == Term.semester_id))
				   .where(Person.prof_id == prof_id, Term.year == year1)
				   .order_by(Supervision.supervision_class_id.desc()))
	projectsupervision = (ProjectSupervision
						  .select()
						  .join(Person, on=(ProjectSupervision.prof_id == Person.prof_id))
						  .join(Term, on=(ProjectSupervision.semester_id == Term.semester_id))
						  .where(Person.prof_id == prof_id, Term.year == year1)
						  .order_by(ProjectSupervision.project_supervision_id.desc()))
	offering = (Offering
				.select()
				.join(Person, on=(Offering.prof_id == Person.prof_id))
				.join(Term, on=(Offering.semester_id == Term.semester_id))
				.where(Person.prof_id == prof_id, Term.year == year1)
				.order_by(Offering.offering_id.desc()))
	adjustment = (Adjustment
				  .select()
				  .join(Person)
				  .where(Person.prof_id == prof_id)
				  .order_by(Adjustment.adjustment_id.desc()))
	Stotal = (Supervision
			  .select()
			  .where(Supervision.prof_id == prof_id)
			  .join(SupervisionClass)
			  .select(fn.SUM(SupervisionClass.weight))
			  .scalar())
	Atotal = (Person
			  .select()
			  .where(Person.prof_id == prof_id)
			  .join(Adjustment)
			  .select(fn.SUM(Adjustment.adjustment_weight))
			  .scalar())
	Ptotal = (ProjectSupervision
			  .select()
			  .where(ProjectSupervision.prof_id == prof_id)
			  .join(ProjectClass)
			  .select(fn.SUM(ProjectClass.weight))
			  .scalar())
	if Atotal is None:
		Atotal = 0
	if Stotal is None:
		Stotal = 0
	if Ptotal is None:
		Ptotal = 0
	return render_template("profile.html", person=person, supervision=supervision,
						   projectsupervision=projectsupervision, offering=offering,
						   adjustment=adjustment, Ptotal=Ptotal,
						   Stotal=Stotal, Atotal=Atotal)


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
			Offering.create(students_taking=student, prof_id=iD1, semester_id=semesterID1, course_gen_id=courseGenID)
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
			ProjectSupervision.create(prof_id=iD3, pseudo_id=pseudoID, project_class_id=projectClassID,
									  semester_id=semesterID3)
		elif request.form['subm1'] == "submit5":
			iD4 = request.form['ID4']
			ADJWeight = request.form['ADJWeight']
			AUDITCOMMENT = request.form['AUDITCOMMENT']
			Adjustment.create(prof_id=iD4, adjustment_weight=ADJWeight, audit_comment=AUDITCOMMENT)
	return render_template("masterlist.html", Person=Person, Pseudo=PseudoPeople, Course=Course,
						   SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
						   ProjectSupervision=ProjectSupervision, Supervision=Supervision, Adjustment=Adjustment,
						   RolePerson=RolePerson, Role=Role, Term=Term, Offering=Offering,
						   CourseGeneration=CourseGeneration, Student=Student, CourseGeneration1=CourseGeneration1,
						   Course1=Course1)


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
				 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment, Course1, CourseGeneration1],
				safe=True)
			db.create_tables(
				[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment, Course1, CourseGeneration1],
				safe=True)
			db.close()
		elif request.form['Full'] == 'Create':
			db.connect()
			db.create_tables(
				[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment, Course1, CourseGeneration1],
				safe=True)
			db.close()
		elif request.form['Full'] == 'Drop':
			db.connect()
			db.drop_tables(
				[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
				 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment, Course1, CourseGeneration1],
				safe=True)
			db.close()
	return render_template('reset.html')


if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)
