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


@app.route('/test_csv')
def test_csv():
    prof = Person.select()
    targ = open('CSV test', 'w')
    targ.write('Course#, Title, EE, CoE, # Stud., Instructor, Load, Cnt., Location, Cnt., Sctn., Length, Location, Cnt., Location')
    for i in prof:
        prof_id=i.id
        term = Semester.select().where(Semester.year == 2008,Semester.session==01)
        list_of_offerings = list()
        person = Person.get(Person.id == prof_id)
        for x in term:
            offering = (Activity
                        .select()
                        .join(Offering)
                        .where(Activity.subject == prof_id,Offering.semester==x.id)
                        .order_by(Offering.semester.desc()))

            for y in offering:
                list_of_offerings.append(y)
        list_offering_id = list()
        for x in list_of_offerings:
            list_offering_id.append(x.offering.id)
            list_offering_id.sort()
        Stotal = 0
        Ptotal = 0
        Ototal = 0
        Snum = (Supervision
                      .select()
                      .join(Activity)
                      .where(Activity.subject == prof_id))
        list_supervision_date = list()
        list_supervision_value = list()
        for num in Snum:
            Ssum = Activity.select().where(Activity.supervision==num.id).get()
            Stotal += num.supervision_class_id.weight*Ssum.split
            list_supervision_date.append(Ssum.supervision.semester.year)
            list_supervision_date.append(Ssum.supervision.semester.session)
            list_supervision_value.append(num.supervision_class_id.weight * Ssum.split)
        list_forviewer = dict()
        list_split = dict()
        offering_value_date = list()
        counter =- 1
        for num in list_of_offerings:
            counter += 1
            Osum = Activity.select().where(Activity.offering==num.offering.id).get()
            var1 = weight_calc(Osum.offering.id)
            Ototal += var1*Osum.split
            list_forviewer[Osum.offering.id] = var1
            list_split[Osum.offering.id] = Osum.split
            offering_value_date.append((str(Osum.offering.semester.year)+'0'+str(Osum.offering.semester.session)))
            offering_value_date.append(var1*Osum.split)
        list_project_supervision_date = list()
        list_project_supervision_value = list()
        Pnum = (ProjectSupervision
                      .select()
                      .join(Activity)
                      .where(Activity.subject == prof_id))
        for num in Pnum:
            Psum = Activity.select().where(Activity.project == num.id).get()
            Ptotal += num.project_class_id.weight*Psum.split
            list_project_supervision_date.append(Psum.project.semester.year)
            list_project_supervision_date.append(Psum.project.semester.session)
            list_project_supervision_value.append(num.project_class_id.weight * Psum.split)
        for x in list_of_offerings:
            if x.offering.generation.other_info=='None' or x.offering.generation.other_info=='36-hour field school conducted during the first two weeks of the semester' or x.offering.generation.other_info=='meetings with project supervisor as required' or x.offering.generation.other_info=='weekly meetings with project supervisor' or x.offering.generation.other_info==None:
                tut=''
            else:
                tut=x.offering.generation.other_info
            targ.write('\n')
            targ.write(str(x.offering.generation.course.code)+','+str(x.offering.generation.title)+','+''+','+''+','+str(x.offering.enrolment)+','+str(person.name)+','+str(weight_calc(x.offering.id))+','+str(x.offering.generation.lecture_hours)+','+''+','+str(x.offering.generation.labs)+','+str(x.offering.sections)+','+''+','+''+','+str(tut)+','+'')
    return redirect('/')


@app.route('/test_csv2')
def test_csv2():
    """
    planed test for new csv styles
    """
    first_year=2011
    seconf_year=2011
    targ = open('CSV test2', 'w')
    targ.write('Name,'+str(first_year)+', Base, Load, F'+str(first_year)+', W'+str(first_year+1)+', S'+str(first_year+1)+', Other \n')
    master= Activity.select().join(Person, on=Activity.subject)
    for m in master:
        if m.offering.semester.year==first_year:
            try:
                deficit2=PersonalLoad.select().where(instructor=m.subject.id,PersonalLoad.end.year>=first_year).order_by(PersonalLoad.end.asc()).get()
            except:
                deficit2=PersonalLoad.select().where(instructor=m.subject.id).order_by(PersonalLoad.end.asc()).get()
                print deficit2.deficit
            Ototal=0
            list_of_offerings=list()
            offering = (Activity
                        .select()
                        .join(Offering)
                        .where(Activity.subject == m.subject, Offering.semester <= first_year)
                        .order_by(Offering.semester.desc()))
            for y in offering:
                list_of_offerings.append(y)
            for num in list_of_offerings:
                var1 = weight_calc(num.offering.id)
                Ototal += var1 * m.split
            defi=deficit_func(m.subject.id, 2008, first_year)
            targ.write(str(m.subject.name)+','+str(defi)+','+str(deficit2.deficit)+','+str(Ototal)+','+'\n')
    return redirect('/')


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
def Profile(prof_id,year,reports,):
    term=termselect(year)
    list_of_offerings = list()
    for x in term:
        person = Person.get(Person.id == prof_id)
        supervision = (Supervision
                       .select()
                       .join(Activity)
                       .where(Activity.subject == prof_id)
                       .order_by(Supervision.semester.desc()))
        projectsupervision = (ProjectSupervision
                              .select()
                              .join(Activity)
                              .where(Activity.subject == prof_id)
                              .order_by(ProjectSupervision.semester.desc()))
        offering = (Activity
                    .select()
                    .join(Offering)
                    .where(Activity.subject == prof_id,Offering.semester==x.id)
                    .order_by(Offering.semester.desc()))

        for y in offering:
            list_of_offerings.append(y)
    list_offering_id = list()
    for x in list_of_offerings:
        list_offering_id.append(x.offering.id)
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
                  .join(Activity)
                  .where(Activity.subject == prof_id))
    list_supervision_date = list()
    list_supervision_value = list()
    for num in Snum:
        Ssum = Activity.select().where(Activity.supervision==num.id).get()
        Stotal += num.supervision_class_id.weight*Ssum.split
        list_supervision_date.append(Ssum.supervision.semester.year)
        list_supervision_date.append(Ssum.supervision.semester.session)
        list_supervision_value.append(num.supervision_class_id.weight * Ssum.split)
    list_forviewer = dict()
    list_split = dict()
    offering_value_date = list()
    counter =- 1
    for num in list_of_offerings:
        counter += 1
        Osum = Activity.select().where(Activity.offering==num.offering.id).get()
        var1 = weight_calc(Osum.offering.id)
        Ototal += var1*Osum.split
        list_forviewer[Osum.offering.id] = var1
        list_split[Osum.offering.id] = Osum.split
        offering_value_date.append((str(Osum.offering.semester.year)+'0'+str(Osum.offering.semester.session)))
        offering_value_date.append(var1*Osum.split)
    list_project_supervision_date = list()
    list_project_supervision_value = list()
    Pnum = (ProjectSupervision
                  .select()
                  .join(Activity)
                  .where(Activity.subject == prof_id))
    for num in Pnum:
        Psum = Activity.select().where(Activity.project == num.id).get()
        Ptotal += num.project_class_id.weight*Psum.split
        list_project_supervision_date.append(Psum.project.semester.year)
        list_project_supervision_date.append(Psum.project.semester.session)
        list_project_supervision_value.append(num.project_class_id.weight * Psum.split)
    Atotal = (Person
              .select()
              .where(Person.id == prof_id)
              .join(Adjustment)
              .select(fn.SUM(Adjustment.weight))
              .scalar())
    term2=Semester.select().order_by(Semester.year.asc()).get()
    defi = deficit_func(prof_id,None,2016)  # TODO: fix cumulative load calc.
    deficit2=PersonalLoad.select().join(Person).where(Person.id==prof_id)
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
        if request.form['subm1'] == "Supervisions CSV":
            anyplot(list_supervision_date, 'super for id '+str(prof_id), list_supervision_value)
            return send_file('super for id '+str(prof_id)+'.pdf')
        if request.form['subm1'] == "Project Supervisions CSV":
            anyplot(list_project_supervision_date, 'project for id '+str(prof_id), list_project_supervision_value)
            return send_file('project for id '+str(prof_id)+'.pdf')
        if request.form['subm1'] == "Offerings CSV":
            print 'asd'
            offerplot(offering_value_date, 'offer for id '+str(prof_id))
            return send_file('offer for id '+str(prof_id)+'.pdf')
        if request.form['subm1'] == "update":
            name = request.form['name']
            email = request.form['email']
            start = request.form['start']
            varyear= Semester.select().where(Semester.year==start,Semester.session==01).get()
            A=Person.update(name=name,email=email,start=varyear.id).where(Person.id==prof_id)
            A.execute()
            Adjustment.create(comment=("Person table update, name + "+str(name)+" + email + "+str(email)+" + start + "+str(start)+" +"), instructor=prof_id)
        if request.form['subm1'] == "adjustment":
            weight = request.form['weight']
            comment = request.form['comment']
            Adjustment.create(weight=weight, comment=comment, instructor=prof_id)
#        if request.form['subm1'] == "deficit":
#            defi2=Deficit.select()
#            for x in defi2:
#                if 'applied_start'+str(x.id) in request.form:
#                    if request.form['applied_start'+str(x.id)]!='':
#                        a = Deficit.update(applied_start=int(request.form['applied_start'+str(x.id)])).where(Deficit.id == x.id)
#                        a.execute()
#                if 'applied_final'+str(x.id) in request.form:
#                    if request.form['applied_start'+str(x.id)]!='':
#                        b = Deficit.update(applied_final=int(request.form['applied_final'+str(x.id)])).where(Deficit.id == x.id)
#                        b.execute()
#                if 'deficit'+str(x.id) in request.form:
#                    if request.form['applied_start'+str(x.id)]!='':
#                        c = Deficit.update(deficit=float(request.form['deficit'+str(x.id)])).where(Deficit.id == x.id)
#                        c.execute()
#            deficit3 = request.form['deficit3']
#            applied_start = request.form['applied_start']
#
#            var = Deficit.select().where(Deficit.applied==prof_id).order_by(Deficit.applied_start.desc()).get()
#            if deficit3=="":
#                deficit3=4.0
#            applied_start=int(applied_start)
#            var2 = int(var.applied_start)
#            if var2>=applied_start:
#                return 'error'
#            A=Deficit.update(applied_final=applied_start).where(Deficit.applied==prof_id,Deficit.applied_final==None)
#            A.execute()
#            Deficit.create(deficit=deficit3,applied=prof_id, applied_start=applied_start)
#            Adjustment.create(comment=("Deficit table update, applied_start"+str(applied_start)+" deficit"+str(deficit3)), applied=prof_id)
        if request.form['subm1'] == "offering":
            off=Offering.select()
            for id in off:
                print request.form['applied_start'+str(id.id)]
                if 'enroll' + str(id.id) in request.form:
                        l = Offering.update(enrolment=(int(request.form['applied_start'+str(id.id)]))).where(Offering.id == id.id)
                        l.execute()
                        Adjustment.create(comment=('enrolment in + '+str(id.id)+' + offering to become + '+str(int(request.form['applied_start'+str(id.id)]))+' +'))

    if reports==True:
        return total, defi, offering_value_date, list_project_supervision_date, list_project_supervision_value, list_supervision_value, list_supervision_date
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
                offering = request.form['offering']
                supervision = request.form['supervision']
                project = request.form['pid']
                role = request.form['rid']
                split = request.form['split']
                if instructor=='':
                    error='instructor is none'
                if supervision=='':
                    supervision=None
                if offering=='':
                    offering=None
                if project=='':
                    project=None
                if role=='':
                    role=None
                if split=='':
                    split = 1
                Activity.create(subject=instructor, offering=offering, supervision=supervision,project=project, role=role, split=split)
                B=Activity.select().where(Activity.subject==instructor, Activity.offering==offering, Activity.supervision==supervision,Activity.project==project, Activity.role==role, Activity.split==split).get()
                Adjustment.create(comment='Created Teaching paring ' + str(B.id),
                                  overide_address='Activity.' + str(B.id))
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
                Semester.create(year=year,session=session)
                B=Semester.select().where(Semester.year==year,Semester.session==session)
                Adjustment.create(comment='Created Semester ' + str(B.id),
                                  overide_address='Semester.' + str(B.id))
            except:
                pass
        if request.form['subm1'] == "update info":
            enrol = request.form['enroll']
            ooid = request.form['offering']
            sections = request.form['sections']
            sections = int(sections)
            enrol = int(enrol)
            ooid = int(ooid)
            A=Offering.update(enrolment=enrol, sections=sections).where(Offering.id==ooid)
            A.execute()
            print 'i updated?'
            Adjustment.create(comment=('enrolment in + '+str(ooid)+' + offering to become + '+str(enrol)+' +'))
        if request.form['subm1'] == "reviewed":
            person=Person.select()
            for id in person:
                # print request.form['name'+str(id.id)] != ""
                # if request.form['name'+str(id.id)] != "":
                #     name = request.form['name']
                #     email = request.form['email']
                #     id = request.form['professrid']
                #     print id
                #     print email
                #     print name
                #     A = Person.update(name=name, email=email).where(Person.id == id.id)
                #     A.execute()
                #     Adjustment.create(comment=(
                #         "Person table update, name + " + str(name) + " + email + " + str(email) + " + start + "),
                #         instructor=id, reviewed=True)
                if 'cbox1'+str(id.id) in request.form:
                    a = Person.update(reviewed=True).where(Person.id == id.id)
                    a.execute()
                else:
                    pass
            course = Course.select()
            for x in course:
                if 'cbox2' + str(id.id) in request.form:
                    a = Course.update(reviewed=True).where(Course.id == x.id)
                    a.execute()
                else:
                    pass
            coursegen = CourseGeneration.select()
            for x in coursegen:
                if 'cbox3' + str(id.id) in request.form:
                    a = CourseGeneration.update(reviewed=True).where(CourseGeneration.id == x.id)
                    a.execute()
                else:
                    pass
            offering = Offering.select()
            for x in offering:
                if 'cbox4' + str(id.id) in request.form:
                    a = Offering.update(reviewed=True).where(Offering.id == x.id)
                    a.execute()
                else:
                    pass
        # if request.form['subm1'] == "PURGE1":
        #     purge=request.form['purgeid1']
        #     print purge
        #     a=Person.delete().where(Person.id==purge)
        #     a.execute()
        # if request.form['subm1'] == "PURGE2":
        #     purge=request.form['purgeid2']
        #     a=Course.delete().where(Course.id==purge)
        #     a.execute()
        # if request.form['subm1'] == "PURGE3":
        #     purge=request.form['purgeid3']
        #     a=Offering.delete().where(Offering.id==purge)
        #     a.execute()
        # if request.form['subm1'] == "PURGE4":
        #     purge=request.form['purgeid4']
        #     a=CourseGeneration.delete().where(CourseGeneration.id==purge)
        #     a.execute()
    mastermany = Activity.select().order_by(Activity.offering.asc())
    return render_template("masterlist.html", Person=Person, ProjectType=ProjectType, Course=Course,
                           SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
                           ProjectSupervision=ProjectSupervision, Supervision=Supervision, Adjustment=Adjustment,
                           Role=Role, Semester=Semester, Offering=Offering,
                           CourseGeneration=CourseGeneration, Student=Student,Activity=mastermany)


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
            master=Activity.select().join(Offering).where(Activity.offering==Offering.id,Offering.semester==x.id)
            for y in master:
                list_of_teachers1.append(y.subject)
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
