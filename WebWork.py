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
	# noinspection PyUnresolvedReferences
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/s/<search>/<id>", methods=['GET', 'POST'])
def Coursehist(search,id):
	if request.method == 'POST':
		if request.form['subm1'] == "submit1":
			labs = request.form['labs']
			credit_hours = request.form['credit_hours']
			lecture_hours = request.form['lecture_hours']
			title = request.form['title']
			comments = request.form['comments']
			course = int(request.form['course'])
			A=Course.get_or_create(code=course,subject='ENGI',reviewed=True)
			other_info = request.form['other_info']
			previous_course = request.form['previous_course']
			start_year = request.form['start_year']
			end_year = request.form['end_year']
			CourseGeneration.create(labs=labs,
									credit_hours=credit_hours,
									lecture_hours=lecture_hours,
									title=title,
									comments=comments,
									other_info=other_info,
									previous_course=previous_course,
									start_year=start_year,
									end_year=end_year,
									course=A[0].id,
									reviewed=True)
			B=CourseGeneration.select().where(CourseGeneration.labs==labs,
											  CourseGeneration.credit_hours==credit_hours,
											  CourseGeneration.lecture_hours==lecture_hours,
											  CourseGeneration.title==title,
											  CourseGeneration.comments==comments,
											  CourseGeneration.other_info==other_info,
											  CourseGeneration.previous_course==previous_course,
											  CourseGeneration.start_year==start_year,
											  CourseGeneration.end_year==end_year,
											  CourseGeneration.course==A[0].id,
											  CourseGeneration.reviewed==True).get()
			Adjustment.create(comment='Created a course generation'+str(B.id),overide_address='CourseGeneration'+str(B.id))
	list2 = []
	if search=='course':
		course = Course.get(Course.id==id)
		generation = (CourseGeneration.select().join(Course).where(Course.id == id))
		list1 = informationXchange(generation, list2)
	if search =='gen':
		gen = CourseGeneration.get(CourseGeneration.id == id)
		course = Course.get(Course.code == gen.course.code)
		generation = (CourseGeneration.select().join(Course).where(Course.code == gen.course.code))
		list1 = informationXchange(generation, list2)
	if search=='c':
		course = Course.get(Course.code==id)
		generation = (CourseGeneration.select().join(Course).where(Course.code == id))
		list1 = informationXchange(generation, list2)
	return render_template("course.html", course=course, generation=generation, list1=list1, course_id=id, search=search)


@app.route("/profile/<prof_id>/<year>/<reports>", methods=['GET', 'POST'])
def Profile(prof_id,year,reports):
	term=termselect(year)
	list_of_offerings = list()
	for x in term:
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
					.where(Mastermany.instructor == prof_id,Offering.semester==x.id)
					.order_by(Offering.semester.desc()))

		for y in offering:
			list_of_offerings.append(y)
	list_offering_id = list()
	for x in list_of_offerings:
		list_offering_id.append(x.oid.id)
		list_offering_id.sort()
	adjustment = (Adjustment
				  .select()
				  .join(Person)
				  .where(Person.id == prof_id)
				  .order_by(Adjustment.id.desc()))
	Stotal = 0
	Ptotal = 0
	Ototal = 0
	Snum = (Supervision
				  .select()
				  .join(Mastermany)
				  .where(Mastermany.instructor == prof_id))
	list_supervision_date = list()
	list_supervision_value = list()
	for num in Snum:
		Ssum = Mastermany.select().where(Mastermany.sid==num.id).get()
		Stotal += num.supervision_class_id.weight*Ssum.split
		list_supervision_date.append(Ssum.sid.semester.year)
		list_supervision_date.append(Ssum.sid.semester.session)
		list_supervision_value.append(num.supervision_class_id.weight * Ssum.split)
	list_forviewer = dict()
	list_split = dict()
	offering_value_date = list()
	counter =- 1
	for num in list_of_offerings:
		counter += 1
		Osum = Mastermany.select().where(Mastermany.oid==num.oid.id).get()
		var1 = weight_calc(Osum.oid.id)
		Ototal += var1*Osum.split
		list_forviewer[Osum.oid.id] = var1
		list_split[Osum.oid.id] = Osum.split
		offering_value_date.append((str(Osum.oid.semester.year)+'0'+str(Osum.oid.semester.session)))
		offering_value_date.append(var1*Osum.split)
	list_project_supervision_date = list()
	list_project_supervision_value = list()
	Pnum = (ProjectSupervision
				  .select()
				  .join(Mastermany)
				  .where(Mastermany.instructor == prof_id))
	for num in Pnum:
		Psum = Mastermany.select().where(Mastermany.pid == num.id).get()
		Ptotal += num.project_class_id.weight*Psum.split
		list_project_supervision_date.append(Psum.pid.semester.year)
		list_project_supervision_date.append(Psum.pid.semester.session)
		list_project_supervision_value.append(num.project_class_id.weight * Psum.split)
	Atotal = (Person
			  .select()
			  .where(Person.id == prof_id)
			  .join(Adjustment)
			  .select(fn.SUM(Adjustment.weight))
			  .scalar())
	defi = deficit(prof_id,2009,2017)
	if Ototal is None:
		Ototal = 0
	if Atotal is None:
		Atotal = 0
	if Stotal is None:
		Stotal = 0
	if Ptotal is None:
		Ptotal = 0
	total = Ptotal + Atotal + Stotal + Ototal - defi
	if request.method == 'POST':
		if request.form['subm1']=="Supervisions CSV":
			anyplot(list_supervision_date, 'super for id '+str(prof_id), list_supervision_value)
			return send_file('super for id '+str(prof_id)+'.pdf')
		if request.form['subm1']=="Project Supervisions CSV":
			anyplot(list_project_supervision_date, 'project for id '+str(prof_id), list_project_supervision_value)
			return send_file('project for id '+str(prof_id)+'.pdf')
		if request.form['subm1']=="Offerings CSV":
			print 'asd'
			offerplot(offering_value_date, 'offer for id '+str(prof_id))
			return send_file('offer for id '+str(prof_id)+'.pdf')
		if request.form['subm1'] == "update":
			name = request.form['name']
			email = request.form['email']
			start = request.form['start']
			A=Person.update(name=name,email=email,start=start).where(Person.id==prof_id)
			A.execute()
		if request.form['subm1'] == "adjustment":
			weight = request.form['weight']
			comment = request.form['comment']
			A=Adjustment.create(weight=weight, comment=comment, instructor=prof_id)
		if request.form['subm1'] == "deficit5":
			deficit3 = request.form['deficit3']
			applied_start = request.form['applied_start']
			A=Deficit.update(applied_final=applied_start).where(Deficit.applied==prof_id,Deficit.applied_final==None)
			A.execute()
			Deficit.create(deficit=deficit3,applied=prof_id, applied_start=applied_start)
	if reports==True:
		return total, defi, offering_value_date, list_project_supervision_date, list_project_supervision_value, list_supervision_value, list_supervision_date
	deficit2=Deficit.select().join(Person).where(Person.id==prof_id)
	return render_template("profilehist.html", person=person, supervision=supervision,instructor=prof_id,
					   projectsupervision=projectsupervision, offering=list_of_offerings, adjustment=adjustment,total=total,
					   Stotal=Stotal, Ptotal=Ptotal, Ototal=Ototal, deficit=defi, list_forviewer=list_forviewer,list_split=list_split
					   ,year=year, reports=reports, Deficit=deficit2)

@app.route('/listm', methods=['GET', 'POST'])
def listm():
	if request.method == 'POST':
		if request.form['subm1'] == "submit1":
			try:
				labs = request.form['labs']
				credit_hours = request.form['credit_hours']
				lecture_hours = request.form['lecture_hours']
				title = request.form['title']
				comments = request.form['comments']
				course = int(request.form['course'])
				A=Course.get_or_create(code=course,subject='ENGI')
				other_info = request.form['other_info']
				previous_course = request.form['previous_course']
				start_year = request.form['start_year']
				end_year = request.form['end_year']
				if end_year != '' and start_year != '' and labs != '' and credit_hours != '' and lecture_hours != '' and title != '' and course != '':
					A=CourseGeneration.create(labs=labs,
											credit_hours=credit_hours,
											lecture_hours=lecture_hours,
											title=title,
											comments=comments,
											other_info=other_info,
											previous_course=previous_course,
											start_year=start_year,
											end_year=end_year,
											course=A[0].id,
											reviewed=True)
					B = CourseGeneration.select().where(CourseGeneration.labs == labs,
														CourseGeneration.credit_hours == credit_hours,
														CourseGeneration.lecture_hours == lecture_hours,
														CourseGeneration.title == title,
														CourseGeneration.comments == comments,
														CourseGeneration.other_info == other_info,
														CourseGeneration.previous_course == previous_course,
														CourseGeneration.start_year == start_year,
														CourseGeneration.end_year == end_year,
														CourseGeneration.course == A[0].id,
														CourseGeneration.reviewed==True).get()
					Adjustment.create(comment='Created a course generation ' + str(B.id),
									  overide_address='CourseGeneration.' + str(B.id))
			except:
				pass
		if request.form['subm1'] == "submit3":
			try:
				instructor = request.form['instructor']
				oid = request.form['oid']
				sid = request.form['sid']
				pid = request.form['pid']
				rid = request.form['rid']
				split = request.form['split']
				if instructor=='':
					error='instructor is none'
				if sid=='':
					sid=None
				if oid=='':
					oid=None
				if pid=='':
					pid=None
				if rid=='':
					rid=None
				if split=='':
					split = 1
				Mastermany.create(instructor=instructor, oid=oid, sid=sid,pid=pid, rid=rid, split=split)
				B=Mastermany.select().where(Mastermany.instructor==instructor, Mastermany.oid==oid, Mastermany.sid==sid,Mastermany.pid==pid, Mastermany.rid==rid, Mastermany.split==split).get()
				Adjustment.create(comment='Created Teaching paring ' + str(B.id),
								  overide_address='Mastermany.' + str(B.id))
			except:
				pass
		if request.form['subm1'] == "submit2":
			try:
				enrolment = request.form['enrolment']
				semester = request.form['semester']
				generation = request.form['generation']
				sections = request.form['sections']
				Offering.create(enrolment=enrolment, semester=semester, generation=generation,sections=sections,reviewed=True)
				B=Offering.select().where(Offering.enrolment==enrolment, Offering.semester==semester, Offering.generation==generation,Offering.sections==sections,Offering.reviewed==True).get()
				Adjustment.create(comment='Created Offering ' + str(B.id),
							  overide_address='Offering.' + str(B.id))
			except:
				pass
		if request.form['subm1'] == "submit4":
			try:
				year = request.form['year']
				session = request.form['session']
				Term.create(year=year,session=session)
				B=Term.select().where(Term.year==year,Term.session==session)
				Adjustment.create(comment='Created Term ' + str(B.id),
								  overide_address='Term.' + str(B.id))
			except:
				pass
		if request.form['subm1'] == "subm2":
			person=Person.select()
			for id in person:
				try:
					update=request.form['cbox1'+str(id.id)]
					a = Person.update(reviewed=True).where(Person.id == id.id)
					a.execute()
				except:
					pass
			course = Course.select()
			for x in course:
				try:
					update=request.form['cbox2'+str(x.id)]
					a = Course.update(reviewed=True).where(Course.id == x.id)
					a.execute()
				except:
					pass
			coursegen = CourseGeneration.select()
			for x in coursegen:
				try:
					update=request.form['cbox3'+str(x.id)]
					a = CourseGeneration.update(reviewed=True).where(CourseGeneration.id == x.id)
					a.execute()
				except:
					pass
			offering = Offering.select()
			for x in offering:
				try:
					update=request.form['cbox4'+str(x.id)]
					a = Offering.update(reviewed=True).where(Offering.id == x.id)
					a.execute()
				except:
					pass
		# if request.form['subm1'] == "PURGE1":
		# 	purge=request.form['purgeid1']
		# 	print purge
		# 	a=Person.delete().where(Person.id==purge)
		# 	a.execute()
		# if request.form['subm1'] == "PURGE2":
		# 	purge=request.form['purgeid2']
		# 	a=Course.delete().where(Course.id==purge)
		# 	a.execute()
		# if request.form['subm1'] == "PURGE3":
		# 	purge=request.form['purgeid3']
		# 	a=Offering.delete().where(Offering.id==purge)
		# 	a.execute()
		# if request.form['subm1'] == "PURGE4":
		# 	purge=request.form['purgeid4']
		# 	a=CourseGeneration.delete().where(CourseGeneration.id==purge)
		# 	a.execute()
	mastermany = Mastermany.select().order_by(Mastermany.oid.asc())
	return render_template("masterlist.html", Person=Person, ProjectType=ProjectType, Course=Course,
						   SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
						   ProjectSupervision=ProjectSupervision, Supervision=Supervision, Adjustment=Adjustment,
						   Role=Role, Term=Term, Offering=Offering,
						   CourseGeneration=CourseGeneration, Student=Student,Mastermany=mastermany)


@app.route('/yearly/<year>/', methods=['GET', 'POST'])
def reports(year):
	list_total = list()
	reports=True
	term=termselect(year)
	targ = open('asd', 'w')
	if term!=True:
		for x in term:
			var1=str(x.year)
			list_of_teachers1 = list()
			master=Mastermany.select().join(Offering).where(Mastermany.oid==Offering.id,Offering.semester==x.id)
			for y in master:
				list_of_teachers1.append(y.instructor)
			list_of_teachers2=set(list_of_teachers1)
			for z in list_of_teachers2:
				total, defi, offering_value_date, list_project_supervision_date, list_project_supervision_value, list_supervision_value, list_supervision_date = Profile(z.id, var1, reports)
				if x.session==1:
					targ.write('made to date ' + str(defi + total))
					targ.write('\n')
					targ.write('total deficit ' + str(total))
					targ.write('\n')
					targ.write(str(z.id) + ' ' + str(z.name))
					targ.write('\n')
					targ.write(str(x.year) + str(x.session))
					targ.write('\n')
					targ.write('\n')
					targ.write('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
					targ.write('\n')
					list_total.append(str(x.year)+'0'+str(x.session))
					list_total.append(total)
	offerplot(list_total,'Deficit','offer')
	return redirect('/')


@app.route('/Dashboard')
@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
	return render_template("home.html")

if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)
