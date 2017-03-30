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
from flask import *
from werkzeug.utils import *
from Core import *
app = Flask(__name__)
DATABASE = 'database.db'
db = SqliteDatabase(DATABASE)
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/export', methods=['GET','POST'])
def docustomexport():
	if request.method == 'POST':
		selector = request.form.get('Select')
		export_file(selector)
		name = selector+'.csv'
		return send_file(name,mimetype=None,as_attachment=True)
	return render_template('export.html')


@app.route('/import', methods=['GET', 'POST'])
def docustomimport():
	if request.method == 'POST':
		selector = request.form.get('Select')
		import_file(selector)
	return render_template('import.html')


@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'favicon.ico', mimetype='image/vnd.microsoft.icon')


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


@app.route("/gen/<id>", methods=['GET', 'POST'])
def gen(id):
	list2=[]
	gen=CourseGeneration.get(CourseGeneration.id == id)
	course = Course.get(Course.code == gen.course.code)
	generation = (CourseGeneration.select().join(Course).where(Course.code == gen.course.code))
	list1=informationXchange(generation,list2)
	return render_template("course.html", course=course,generation=generation,list1=list1)


@app.route("/profile/<prof_id>/", methods=['GET', 'POST'])
def Profile(prof_id):
	person = Person.get(Person.id == prof_id)
	supervision = (Supervision
				   .select()
				   .join(Mastermany)
				   .where(Mastermany.instructor == prof_id)
				   .order_by(Supervision.semester.desc()))
	projectsupervision = (ProjectSupervision
						  .select()
						  .join(Mastermany)
						  .where(Mastermany.instructor == prof_id)
						  .order_by(ProjectSupervision.semester.desc()))
	offering = (Mastermany
				.select()
				.join(Offering)
				.where(Mastermany.instructor == prof_id)
				.order_by(Offering.semester.desc()))
	list1=list()
	for x in offering:
		list1.append(x.oid.id)
		list1.sort()
	adjustment = (Adjustment
				  .select()
				  .join(Person)
				  .where(Person.id == prof_id)
				  .order_by(Adjustment.id.desc()))
	Stotal = 0
	Atotal = 0
	Ptotal = 0
	Ototal = 0
	Snum = (Supervision
				  .select()
				  .join(Mastermany)
				  .where(Mastermany.instructor == prof_id))
	list31=list()
	list32=list()
	for num in Snum:
		Ssum=Mastermany.select().where(Mastermany.sid==num.id).get()
		Stotal+=num.supervision_class_id.weight*Ssum.split
		list31.append(Ssum.sid.semester.year)
		list31.append(Ssum.sid.semester.session)
		list32.append(num.supervision_class_id.weight * Ssum.split)
	Onum = (Offering
				  .select()
				  .join(Mastermany)
				  .where(Mastermany.instructor == prof_id))
	list_forviewer = dict()
	list_split = dict()
	dict_temp2=list()
	counter=-1
	for num in Onum:
		counter+=1
		Osum=Mastermany.select().where(Mastermany.oid==num.id).get()
		var1=weight_calc(Osum.oid.id)
		Ototal+=var1*Osum.split
		list_forviewer[Osum.oid.id]=var1
		list_split[Osum.oid.id]=Osum.split
		dict_temp2.append((str(Osum.oid.semester.year)+'0'+str(Osum.oid.semester.session)))
		dict_temp2.append(var1*Osum.split)
	list21=list()
	list22=list()
	Pnum = (ProjectSupervision
				  .select()
				  .join(Mastermany)
				  .where(Mastermany.instructor == prof_id))
	for num in Pnum:
		Psum=Mastermany.select().where(Mastermany.pid==num.id).get()
		Ptotal+=num.project_class_id.weight*Psum.split
		list21.append(Psum.pid.semester.year)
		list21.append(Psum.pid.semester.session)
		list22.append(num.project_class_id.weight * Psum.split)
	Atotal = (Person
			  .select()
			  .where(Person.id == prof_id)
			  .join(Adjustment)
			  .select(fn.SUM(Adjustment.weight))
			  .scalar())
	defi=deficit(prof_id)
	if Ototal is None:
		Ototal = 0
	if Atotal is None:
		Atotal = 0
	if Stotal is None:
		Stotal = 0
	if Ptotal is None:
		Ptotal = 0
	total = (Ptotal) + (Atotal) + (Stotal) + (Ototal) - defi
	if request.method == 'POST':
		if request.form['subm1']=="Supervisions CSV":
			print ' works'
			print list31
			print list32
			anyplot(list31,'super for id '+str(prof_id),list32)
			return send_file('super for id '+str(prof_id)+'.pdf')
		if request.form['subm1']=="Project Supervisions CSV":
			print list21
			print list22
			anyplot(list21,'project for id '+str(prof_id),list22)
			return send_file('project for id '+str(prof_id)+'.pdf')
		if request.form['subm1']=="Offerings CSV":
			print ' works'
			offerplot(dict_temp2,'offer for id '+str(prof_id))
			return send_file('offer for id '+str(prof_id)+'.pdf')
		if request.form['subm1'] == "submit2":
			weight = request.form['weight']
			weight = float(weight)
			AUDITCOMMENT = request.form['AUDITCOMMENT']
			Adjustment.create(instructor=prof_id, weight=weight, comment=AUDITCOMMENT)
	return render_template("profilehist.html", person=person, supervision=supervision,instructor=prof_id,
						   projectsupervision=projectsupervision, offering=offering, adjustment=adjustment,total=total,
						   Stotal=Stotal,Ptotal=Ptotal,Ototal=Ototal,Onum=Onum,deficit=defi,list_forviewer=list_forviewer,list_split=list_split)


"""
To be worked on
"""
# @app.route("/profile/<prof_id>", methods=['GET', 'POST'])
# def Profile(prof_id):
# 	now = datetime.datetime.now()
# 	year1 = now.year
# 	person = Person.get(Person.id == prof_id)
# 	supervision = (Supervision.select()
# 				   .join(Person, on=(Supervision.id == Person.id))
# 				   .join(Term, on=(Supervision.id == Term.id))
# 				   .where(Person.id == prof_id, Term.year == year1)
# 				   .order_by(Supervision.id.desc()))
# 	projectsupervision = (ProjectSupervision
# 						  .select()
# 						  .join(Person, on=(ProjectSupervision.id == Person.id))
# 						  .join(Term, on=(ProjectSupervision.id == Term.id))
# 						  .where(Person.id == prof_id, Term.year == year1)
# 						  .order_by(ProjectSupervision.id.desc()))
# 	offering = (Offering
# 				.select()
# 				.join(Mastermany, on=(Offering.id == Mastermany.instructor))
# 				.join(Term, on=(Offering.id == Term.id))
# 				.where(Mastermany.id == prof_id, Term.year == year1)
# 				.order_by(Offering.id.desc()))
	# list1=list()
	# for x in offering:
	# 	list1.append(x.id)
	# adjustment = (Adjustment
	# 			  .select()
	# 			  .join(Person)
	# 			  .where(Person.id == prof_id)
	# 			  .order_by(Adjustment.id.desc()))
	# Stotal = 0
	# Atotal = 0
	# Ptotal = 0
	# Ototal = 0
	# Snum = (Supervision
	# 			  .select()
	# 			  .join(Mastermany)
	# 			  .where(Mastermany.instructor == prof_id))
	# for num in Snum:
	# 	Ssum=Mastermany.select().where(Mastermany.sid==num.id).get()
	# 	Stotal+=num.supervision_class_id.weight*Ssum.split
	#
	# Onum = (Offering
	# 			  .select()
	# 			  .join(Mastermany)
	# 			  .where(Mastermany.instructor == prof_id))
	# list_forviewer = dict()
	# list_split = dict()
	# counter=-1
	# for num in Onum:
	# 	counter+=1
	# 	Osum=Mastermany.select().where(Mastermany.oid==num.id).get()
	# 	var1=weight_calc(Osum.oid)
	# 	Ototal+=var1*Osum.split
	# 	list_forviewer[list1[counter]]=var1
	# 	list_split[list1[counter]]=Osum.split
	#
	#
	# Pnum = (ProjectSupervision
	# 			  .select()
	# 			  .join(Mastermany)
	# 			  .where(Mastermany.instructor == prof_id))
	# for num in Pnum:
	# 	Psum=Mastermany.select().where(Mastermany.pid==num.id).get()
	# 	Ptotal+=num.project_class_id.weight*Psum.split
	# Atotal = (Person
	# 		  .select()
	# 		  .where(Person.id == prof_id)
	# 		  .join(Adjustment)
	# 		  .select(fn.SUM(Adjustment.weight))
	# 		  .scalar())
	# defi=deficit(prof_id)
	# if Ototal is None:
	# 	Ototal = 0
	# if Atotal is None:
	# 	Atotal = 0
	# if Stotal is None:
	# 	Stotal = 0
	# if Ptotal is None:
	# 	Ptotal = 0
	# total = (Ptotal) + (Atotal) + (Stotal) + (Ototal) - defi
	# if request.method == 'POST':
	# 	if request.form['subm1'] == "submit2":
	# 		weight = request.form['weight']
	# 		weight = float(weight)
	# 		AUDITCOMMENT = request.form['AUDITCOMMENT']
	# # 		Adjustment.create(instructor=prof_id, weight=weight, comment=AUDITCOMMENT)
	# return render_template("profilehist.html", person=person, supervision=supervision,instructor=prof_id,
	# 					   projectsupervision=projectsupervision, offering=offering,
	# 					   # adjustment=adjustment,total=total,
	# 					   # Stotal=Stotal,Ptotal=Ptotal,Ototal=Ototal,Onum=Onum,deficit=defi,list_forviewer=list_forviewer,list_split=list_split
	# 					   )


@app.route('/listm', methods=['GET', 'POST'])
def listm():
	if request.method == 'POST':
		if request.form['subm1'] == "submit1":
			labs = request.form['Labs']
			credit = request.form['Credit']
			title = request.form['Title']
			cRN = request.form['CRN']
			CourseGeneration.create(labs=labs, credit_hours=credit, title=title, course=cRN)
		elif request.form['subm1'] == "submit2":
			semesterID1 = request.form['SemesterID1']
			student = request.form['stu']
			iD1 = request.form['ID1']
			courseGenID = request.form['CourseGenID']
			Offering.create(enrolment=student, instructor=iD1, semester=semesterID1, generation=courseGenID)
		elif request.form['subm1'] == "submit3":
			sID = request.form['StudentID']
			superclass = request.form['SupervisionClassID']
			semesterID2 = request.form['SemesterID2']
			iD2 = request.form['ID2']
			Supervision.create(instructor=iD2, student_id=sID, supervision_class_id=superclass, semester=semesterID2)
		elif request.form['subm1'] == "submit4":
			iD3 = request.form['ID3']
			semesterID3 = request.form['SemesterID3']
			pseudoID = request.form['PseudoID']
			projectClassID = request.form['ProjectClassID']
			ProjectSupervision.create(instructor=iD3, Team=pseudoID, project_class_id=projectClassID,
									  semester=semesterID3)
		elif request.form['subm1'] == "submit5":
			iD4 = request.form['ID4']
			ADJWeight = request.form['ADJWeight']
			AUDITCOMMENT = request.form['AUDITCOMMENT']
			Adjustment.create(instructor=iD4, weight=ADJWeight, audit_comment=AUDITCOMMENT)
	mastermany = Mastermany.select().order_by(Mastermany.oid.asc())
	return render_template("masterlist.html", Person=Person, ProjectType=ProjectType, Course=Course,
						   SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
						   ProjectSupervision=ProjectSupervision, Supervision=Supervision, Adjustment=Adjustment,
						   Role=Role, Term=Term, Offering=Offering,
						   CourseGeneration=CourseGeneration, Student=Student,Mastermany=mastermany)


@app.route('/Dashboard')
@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
	return render_template("home.html")

if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)