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
import sys
import time
from itertools import *
from colorama import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
from playhouse.csv_loader import *
from bs4 import *
from db import *

cg=Fore.GREEN
cr=Fore.RED
rs=Style.RESET_ALL
cy=Fore.YELLOW
cb=Fore.BLUE


def informationXchange(generation,list1):
    first_run_var=1
    aa = None
    ab = None
    ac = None
    ad = None
    ae = None
    af = None
    ag = None
    ah = None
    for x in generation:
        a = x.labs
        b = x.credit_hours
        c = x.lecture_hours
        d = x.title
        e = x.comments
        f = x.course
        g = x.other_info
        h = x.previous_course
        if first_run_var == 1:
            aa = a
            ab = b
            ac = c
            ad = d
            ae = e
            af = f
            ag = g
            ah = h
            first_run_var = 2
        else:
            i = str(x.id)
            if aa != a:
                list1.append(i + ':' + 'labs')
                aa = a
            if ab != b:
                list1.append(i + ':' + 'credithours')
                ab = b
            if ac != c:
                list1.append(i + ':' + 'lecturehours')
                ac = c
            if ad != d:
                list1.append(i + ':' + 'title')
                ad = d
            if ae != e:
                list1.append(i + ':' + 'comments')
                ae = e
            if af != f:
                list1.append(i + ':' + 'courseid')
                af = f
            if ag != g:
                list1.append(i + ':' + 'other info')
                ag = g
            if ah != h:
                list1.append(i + ':' + 'previous id')
                ah = h
    return list1


def offer(year,code,session,profid,numberofstudents,sectionnumbers):
    for x in CourseGeneration.select().join(Course).where(Course.code==code).order_by(CourseGeneration.end_year.asc()):
        if int(x.end_year)>=int(year):
            ses=Semester.select().where(Semester.year==year,Semester.session==session).get()
            try:
                Offering.get_or_create(enrolment=numberofstudents,semester=ses,generation=x.id,sections=sectionnumbers,reviewed=False)
                A=Offering.select().where(Offering.enrolment==numberofstudents,Offering.semester==ses,Offering.generation==x.id,Offering.sections==sectionnumbers).get()
            except:
                A=Offering.select().where(Offering.enrolment==numberofstudents,Offering.semester==ses,Offering.generation==x.id,Offering.sections==sectionnumbers).get()
            Activity.get_or_create(subject=profid,offering=A)
            return A.id


def weight_calc(OID):
    off=Offering.select().where(Offering.id==OID).get()
    gen=CourseGeneration.select().join(off).where(CourseGeneration.id==off.generation).get()
    b1 = gen.credit_hours
    c1 = gen.labs
    d1= gen.other_info
    wd1 = 0
    if d1 == 'up to eight tutorial sessions per semester':
        wd1 = float(.07)
    if d1 == 'tutorial one hour per week':
        wd1 = float(.14)
    if d1 == 'tutorial 1 hour per week':
        wd1 = float(.14)
    if d1 == 'one tutorial hour per week':
        wd1 = float(.14)
    if d1 == 'one tutorial hour per week':
        wd1 = float(.14)
    if d1 == 'one tutorial hour per week':
        wd1 = float(.14)
    if d1 == '1 client meeting per week, 1 tutorial per week':
        wd1 = float(.14)
    weight1=fix(off.enrolment,off.sections,b1,c1,wd1)
    return weight1


def fix(numberofstudents, sectionnumbers, b1, c1, wd1):
    wa1=float(float(b1)/float(3))
    numberofstudents=float(numberofstudents)
    if numberofstudents > 75:
        we = float((((float(b1) + (numberofstudents - float(75))) / float(75)) * .5))
    else:
        we = 0
    wb1 = (((float(b1) + float(c1)) / float(36)) * .27) * float(sectionnumbers)
    wc1 = (((float(b1) + float(wd1)) / float(12)) * .14)
    weight1 = wb1 + wc1 + we+wa1
    if numberofstudents < 5:
        weight1 = 0
    return weight1


def Psuper(BOOLDoyouwanttocreateanewone, Description ,Weight):
    ProjectClass.get_or_create(description='Undergraduate project course', weight=0.5)
    ProjectClass.get_or_create(description='senior project supervision of a group of 4 students', weight=(float(0.125)/3))
    ProjectClass.get_or_create(description='Case by Case', weight=2)
    if BOOLDoyouwanttocreateanewone:
        ProjectClass.get_or_create(description=Description, weight=Weight)


def superC(BOOLDoyouwanttocreateanewone, Description, Weight):
    SupervisionClass.get_or_create(description='Gradstudent 1 term', weight=0.047)
    SupervisionClass.get_or_create(description='Masters 1 term', weight=0.07)
    SupervisionClass.get_or_create(description='Doctoral 1 term', weight=(float(.32)/3))
    if BOOLDoyouwanttocreateanewone:
        SupervisionClass.get_or_create(description=Description, weight=Weight)


def supera(TermS, profid, Studentid, supervisoncalss, session):
    ses=Semester.select().where(Semester.year==TermS,Semester.session==session).get()
    Supervision.get_or_create(student_id=Studentid,supervision_class_id=supervisoncalss,semester=ses)
    A=Supervision.select().where(Supervision.student_id==Studentid,Supervision.supervision_class_id==supervisoncalss,Supervision.semester==ses).get()
    Activity.get_or_create(subject=profid,supervision=A, split=1)


def Psupera(TermS, profid, team_id, supervisoncalss, session):
    ses=Semester.select().where(Semester.year==TermS,Semester.session==session).get()
    ProjectSupervision.get_or_create(team_id=team_id,project_class_id=supervisoncalss,semester=ses)
    A=ProjectSupervision.select().where(ProjectSupervision.team_id==team_id,ProjectSupervision.project_class_id==supervisoncalss,ProjectSupervision.semester==ses).get()
    Activity.get_or_create(subject=profid,project=A, split=1)


def person(name, email, staryear, startsem):
    # can't hear
    try:Semester.get_or_create(year= staryear, session = startsem)
    except:pass
    ses=Semester.select().where(Semester.year==staryear,Semester.session==startsem).get()
    try:Person.get_or_create(name=name,email=email,start=ses.id,reviewed=False)
    except:pass


def student(name, email):
    # use sign language
    Student.get_or_create(name=name,email=email)


def team(name, email):
    # use sign language
    ProjectType.get_or_create(name=name,description=email)


def deficit_func(prof_id,year_first,year_second):
    now = datetime.datetime.now()
    defic = PersonalLoad.select().join(Person).where(Person.id == prof_id,PersonalLoad.end.year<=year_second)
    totaldef = 0
    for x in defic:
        if x.applied_final<year_first:
            pass
        elif x.applied_start<=year_first:
            totaldef+=x.deficit*(x.applied_final-year_first+1)
        else:
            totaldef+=x.deficit*(x.applied_final-x.applied_start+1)
    defic2=PersonalLoad.select().join(Person).where(Person.id == prof_id, PersonalLoad.end.year==None).get()
    if year_second >= defic2.applied_start:
        totaldef+=defic2.deficit*(year_second-defic2.applied_start)
    return totaldef


def currentsem():
    now = datetime.datetime.now()
    month = now.month
    if month>=7:
        sem=1
    elif month<=4:
        sem=2
    else:
        sem=3
    return sem


def import_file(selector):
    name = selector+'.csv'
    if selector == 'Person':
        load_csv(Person, name)
    if selector == 'Supervision':
        load_csv(Supervision, name)
    if selector == 'SupervisionClass':
        load_csv(SupervisionClass, name)
    if selector == 'Course':
        load_csv(Course, name)
    if selector == 'CourseGeneration':
        load_csv(CourseGeneration, name)
    if selector == 'Student':
        load_csv(Student, name)
    if selector == 'Semester':
        load_csv(Semester, name)
    if selector == 'Offering':
        load_csv(Offering, name)
    if selector == 'Role':
        load_csv(Role, name)
    if selector == 'ProjectClass':
        load_csv(ProjectClass, name)
    if selector == 'ProjectType':
        load_csv(ProjectType, name)
    if selector == 'Activity':
        load_csv(Activity, name)
    if selector == 'ProjectSupervision':
        load_csv(ProjectSupervision, name)
    if selector == 'Adjustment':
        load_csv(Adjustment, name)


def export_file(selector, name='default'):
    with open(str(name)+'.csv', 'w') as fh:
        if str(selector) == 'Person':
            query = Person.select().order_by(Person.id)
            dump_csv(query, fh)
        if str(selector) == 'Supervision':
            query = Supervision.select().order_by(Supervision.id)
            dump_csv(query, fh)
        if str(selector) == 'SupervisionClass':
            query = SupervisionClass.select().order_by(SupervisionClass.id)
            dump_csv(query, fh)
        if str(selector) == 'Course':
            query = Course.select().order_by(Course.code)
            dump_csv(query, fh)
        if str(selector) == 'CourseGeneration':
            query = CourseGeneration.select().order_by(CourseGeneration.id)
            dump_csv(query, fh)
        if str(selector) == 'Student':
            query = Student.select().order_by(Student.id)
            dump_csv(query, fh)
        if str(selector) == 'Semester':
            query = Semester.select().order_by(Semester.id)
            dump_csv(query, fh)
        if str(selector) == 'Offering':
            query = Offering.select().order_by(Offering.id)
            dump_csv(query, fh)
        if str(selector) == 'Role':
            query = Role.select().order_by(Role.id)
            dump_csv(query, fh)
        if str(selector) == 'ProjectClass':
            query = ProjectClass.select().order_by(ProjectClass.id)
            dump_csv(query, fh)
        if str(selector) == 'ProjectType':
            query = ProjectType.select().order_by(ProjectType.id)
            dump_csv(query, fh)
        if str(selector) == 'Activity':
            query = Activity.select().order_by(Activity.subject)
            dump_csv(query, fh)
        if str(selector) == 'ProjectSupervision':
            query = ProjectSupervision.select().order_by(ProjectSupervision.id)
            dump_csv(query, fh)
        if str(selector) == 'Adjustment':
            query = Adjustment.select().order_by(Adjustment.id)
            dump_csv(query, fh)
        else:
            dump_csv(selector, fh)



def anyplot(semester,name,weights):
    # rename need test data again
    var = None
    p1 = re.compile(r"\w+")
    p2 = p1.findall(name)
    listany=list()
    counter=-1
    for x,y in enumerate(semester):
        if x % 2==0:
            var=y
        else:
            counter+=1
            listany.append(str(var)+'0'+str(y))
            listany.append(weights[counter])
    list3,list4=matchandsort(listany)
    width = 1
    if p2[0]=='project':
        stack=3
    else:
        stack=1.5
    N = len(list4)
    ind = np.arange(N)
    plt.bar(left=ind, height=list3, width=width, color='#d62728')
    plt.ylabel('Credit Value')
    plt.xlabel('Semester in format (year)(semester id)')
    plt.title(p2[0])
    plt.yticks(np.arange(0, stack, 0.125))
    plt.xticks(ind, list4, rotation='vertical')
    plt.savefig(str(name) + '.pdf', bbox_inches='tight')
    plt.close()


def matchandsort(diction_of_var):
    var =- 2
    terms = list()
    values = list()
    for i, j in enumerate(diction_of_var):
        if i %2==0:
            try:
                var=terms.index(j)
            except:
                var=-2
                terms.append(j)
        else:
            if var != -2:
                values[var]+=j
            else:
                values.append(j)
    total_weight = list()
    year_term = list()
    for (y, x) in sorted(zip(terms, values)):
        total_weight.append(x)
        year_term.append(y)
    return total_weight,year_term


def offerplot(dict_temp2,name,scale='default'):
    if scale=='default':
        workaround1 = 0
        workaround2 = 6
        workaround3 = 0.25
    elif scale=='offer':
        workaround1 = 0
        workaround2 = -1000
        workaround3 = -125
    else:
        print cr+'scale not reconized'
        workaround1 = 0
        workaround2 = 6
        workaround3 = 0.25
    p1 = re.compile(r"\w+")
    p2 = p1.findall(name)
    width = 1
    total_weight,year_term=matchandsort(dict_temp2)
    N = len(year_term)
    ind = np.arange(N)
    plt.bar(left=ind,height=total_weight,width=width,color='#d62728')
    plt.ylabel('Credit Value')
    plt.xlabel('Semester Term')
    plt.title(p2[0])
    plt.yticks(np.arange(workaround1,workaround2,workaround3))
    plt.xticks(ind, year_term, rotation='vertical')
    plt.savefig(str(name)+'.pdf',bbox_inches='tight')
    plt.close()


def set_false():
    person=Person.select()
    for x in person:
        if x.reviewed == True:
            a=Person.update(reviewed=False).where(Person.id==x.id)
            a.execute()
    course=Course.select()
    for x in course:
        if x.reviewed == True:
            a=Course.update(reviewed=False).where(Course.id==x.id)
            a.execute()
    coursegen=CourseGeneration.select()
    for x in coursegen:
        if x.reviewed == True:
            a=CourseGeneration.update(reviewed=False).where(CourseGeneration.id==x.id)
            a.execute()
    offering=Offering.select()
    for x in offering:
        if x.reviewed == True:
            a=Offering.update(reviewed=False).where(Offering.id==x.id)
            a.execute()

def termselect(year):
    if year == 'true':
        term=Semester.select()
    else:
        term=Semester.select().where(Semester.year<=year)
    return term

def percent():
    list_teach = list()
    file = open('Faculty and Staff List.csv')
    person = Person.select()
    p2 = re.compile(r"[A-Z]\s")
    p3 = re.compile(r".[A-Z]")
    p4 = re.compile(r"^[A-Z]")
    p5 = re.compile(r"[,][A-z-0-9].+")
    emaildict=dict()
    for row in file:
        p1 = re.compile(r"[A-z]+[,][ ][A-z]+")
        p3 = re.compile(r".[A-Z]")
        rowE = str(p5.findall(row)).strip("''[],")
        row1 = str(p1.findall(row)).strip("''[],")
        emaildict[row1]=rowE
        list_teach.append(row1)
    for peps in person:
        pep_first=p2.findall(peps.name)
        pep_last = p3.findall(peps.name)
        guess=process.extractOne(peps.name,list_teach)
        if guess[1]>50:
            row3 = p3.findall(guess[0])
            row4= p4.findall(guess[0])
            pep_first=str(pep_first).strip("''[]u ")
            row3=str(row3).strip("''[]u ")
            pep_last=str(pep_last).strip("''[]u ")
            row4=str(row4).strip("''[]u ")
            if row3 == pep_first and row4==pep_last:
                print rs+'I am confident that '+cg+str(peps.name)+rs+' is '+cg+str(guess[0])
                a = Person.update(reviewed=True, email=emaildict.get(guess[0])).where(Person.name == peps.name)
                a.execute()
