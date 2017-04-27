# Copyright 2017 Jonathan Anderson
# Copyright 2017 Keegan Joseph Brophy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import config
import peewee
from peewee import *

(scheme, url) = config.DATABASE_URL.split('://')
db = {
    'mysql': peewee.MySQLDatabase,
    'postgres': peewee.PostgresqlDatabase,
    'sqlite': peewee.SqliteDatabase,
}[scheme](url)

class BaseModel(Model):
    class Meta:
        database = db


class Term(BaseModel):
    """
    Term is the numerical representation of year and semester by Memorial University
    """
    year = IntegerField()
    session = IntegerField()


class Person(BaseModel):
    """
    A person in this database is a teaching professional
    """
    name = TextField(null = False)
    email = TextField(unique = True)
    start = ForeignKeyField(Term, related_name = 'startdate', null = False)
    retired = BooleanField(default = False)
    reviewed = BooleanField(default = False)
    # def load(self):


class Deficit(BaseModel):
    """
    To track the irregular deficits accumulated by professors
    """
    deficit = FloatField()
    applied = ForeignKeyField(Person, related_name = 'applicant', null = False)
    applied_start = IntegerField()
    applied_final = IntegerField()


class Course(BaseModel):
    """
    A person in this database is a teaching professional
    """
    subject = TextField()
    # Because of courses like 200W we cannot store info as int
    code = CharField(4)
    reviewed = BooleanField(default = False)

    def __str__(self):
        return '%s %s' % (self.subject, self.code)


class CourseGeneration(BaseModel):
    """
    As a course changes over time it becomes necessary to update it to moder information
    """
    # due to situations like 4.5 these numbers are stored as doubles
    labs = DoubleField(default = 0)
    credit_hours = DoubleField(default = 3)
    lecture_hours = DoubleField(default = 3)
    title = TextField()
    comments = TextField(null = True)
    course = ForeignKeyField(Course, related_name = 'generations')
    other_info = TextField(null = True)
    previous_course = TextField(null = True)
    start_year = IntegerField()
    end_year = IntegerField()
    reviewed = BooleanField(default = False)

    def differs_from(self, details):
        return (self.labs != details['Labs'] or
            self.credit_hours != details['Credit Hours'] or
            self.lecture_hours != details['Lecture Hours'] or
            self.title != details['Title'] or
            self.comments != details['Description'] or
            self.other_info != details['Other info'] or
            self.previous_course != details['PreviousCourseCode'])

    def __str__(self):
        return '%s (%d-%d)' % (self.course, self.start_year, self.end_year)


class Student(BaseModel):
    """
    A student is typically a non-undergrad student
    """
    name = TextField()
    email = TextField()

    def __str__(self):
        return '%s (%s)' % (name, email)


class Offering(BaseModel):
    """
    Display the current courses on offering during the current session
    """
    enrolment = IntegerField()
    # prof_id = ForeignKeyField(Person, related_name='instructor')
    semester = ForeignKeyField(Term, related_name = 'semester')
    generation = ForeignKeyField(CourseGeneration, related_name = 'generation')
    sections = IntegerField(default = 1)
    reviewed = BooleanField(default = False)


class Role(BaseModel):
    """
    These fields represent the class of the user and information they have access too, dept is short for department.
    """
    role_name = TextField(null = False)
    view_you = BooleanField(null = False)
    view_dept = BooleanField(null = False)
    view_all = BooleanField(null = False)
    edit_dept = BooleanField(null = False)


class SupervisionClass(BaseModel):
    """
    Supervising student level, grad, under grad, ect
    """
    description = TextField(null = False)
    weight = FloatField(null = False)


class ProjectClass(BaseModel):
    """
    Supervising student level, grad, under grad, ect
    """
    description = TextField(null = False)
    weight = FloatField(null = False)


class ProjectType(BaseModel):
    """
    A pseudo stand in for teams as students
    """
    name = TextField()
    description = TextField()


class ProjectSupervision(BaseModel):
    """
    A table to tie together projects and their class
    """
    # prof_id = ForeignKeyField(Person, related_name = 'supervisied_projects')
    team_id = ForeignKeyField(ProjectType, related_name = 'projects')
    project_class_id = ForeignKeyField(ProjectClass, related_name = 'projects')
    semester = ForeignKeyField(Term, related_name = 'projects')


class Supervision(BaseModel):
    """
    A table to tie together students ans their class
    """
    student_id = ForeignKeyField(Student, related_name = 'supervisions')
    supervision_class_id = ForeignKeyField(SupervisionClass, related_name = 'supervisions')
    semester = ForeignKeyField(Term, related_name = 'supervisions')


class Adjustment(BaseModel):
    """
    A human entry in that overrides the automatic data
    """
    weight = FloatField(null = True)
    comment = TextField(null = True)
    overide_value = FloatField(null = True)
    overide_address = TextField(null = True)
    instructor = ForeignKeyField(Person, related_name = 'made_change', null = True)


class Mastermany(BaseModel):
    """
    A table that ties together all aspects of a teachers equivalency
    """
    instructor = ForeignKeyField(Person, related_name = 'person_id')
    oid = ForeignKeyField(Offering, related_name = 'offering_id', null = True)
    sid = ForeignKeyField(Supervision, related_name = 'supervision_id', null = True)
    pid = ForeignKeyField(ProjectSupervision, related_name = 'project_id', null = True)
    rid = ForeignKeyField(Role, related_name = 'role_id', null = True)
    split = FloatField(null = True)


ALL_TABLES = [
    Adjustment,
    Course,
    CourseGeneration,
    Deficit,
    Mastermany,
    Offering,
    Person,
    ProjectClass,
    ProjectSupervision,
    ProjectType,
    Role,
    Student,
    Supervision,
    SupervisionClass,
    Term,
]

def get():
    return db

def init(drop_first = True):
    if drop_first:
        db.drop_tables(ALL_TABLES, safe = True)

    db.create_tables(ALL_TABLES)
