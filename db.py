# -*- coding: utf8 -*-

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

class ValidatableModel(BaseModel):
    """
    An object that is derived from noisy data and thus requires
    human validation.
    """

    validated = BooleanField(default = False)


class Session(BaseModel):
    """
    A period of the year that a semester can fall in (e.g., Fall, Winter...).
    """

    code = CharField(1)
    name = TextField()

    def __repr__(self):
        return 'Session { %d / %s }' % (self.code, self.name)

    def __str__(self):
        return self.name


class Semester(BaseModel):
    """
    Semester is the numerical representation of year and semester by Memorial University
    """
    year = IntegerField()
    session = ForeignKeyField(Session)

    def __repr__(self):
        return 'Semester { %d %r }' % (self.year, self.session)

    def __str__(self):
        # Truncate next year to two digits unless the current year is xx99.
        next_year = (self.year % 100 if self.year % 100 < 99 else self.year) + 1
        return '%s %d-%02d' % (self.session, self.year, next_year)


class Person(ValidatableModel):
    """
    A person can be an instructor, a graduate student under supervision
    or even some combination of the two.
    """

    # A student or employee ID
    mun_id = IntegerField(null = True)

    # Human-meaningful name (also used for processing of offering data).
    name = TextField()

    # Email addresses are useful for the application to have, and they are also
    # a useful signal of uniqueness.
    email = TextField(unique = True)

    class Meta:
        order_by = [ 'name' ]

    def graduate_supervision(self):
        return (
            a.supervision
                for a in self.activities.where(Activity.supervision != None)
        )

    def project_supervision(self):
        return (
            a.project for a in self.activities.where(Activity.project != None)
        )

    def teaching(self):
        return self.activities.where(Activity.instruction != None)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Person { name: '%s', email: '%s', validated: %s }" % (
            self.name, self.email, self.validated
        )


class TeachingLoad(BaseModel):
    """
    The annual teaching expectation for an instructor.
    """

    # Description of the load, e.g., "Typical ASM (Engineering)"
    name = TextField()

    # Numeric expectation of courses taught per year
    load = FloatField()


class PersonalLoad(ValidatableModel):
    """
    A teaching load for an individual over a specific time period.
    """

    instructor = ForeignKeyField(Person, related_name = 'teaching_loads')
    load = ForeignKeyField(TeachingLoad, related_name = 'with_load')
    start = ForeignKeyField(Semester, related_name = 'load_starts')
    end = ForeignKeyField(Semester, null = True, related_name = 'load_ends')

    def years(self):
        return u'%s–%s' % (self.start, self.end if self.end else '')


class Course(BaseModel):
    """
    A person in this database is a teaching professional
    """
    subject = TextField()
    # Because of courses like 200W we cannot store info as int
    code = CharField(4)

    def most_recent_name(self):
        gen = self.generations.order_by(CourseGeneration.end_year.desc())
        return None if gen.count() == 0 else gen.get().title

    def __str__(self):
        return '%s %s' % (self.subject, self.code)


class CourseGeneration(ValidatableModel):
    """
    As a course changes over time it becomes necessary to update it to moder information
    """
    # due to situations like 4.5 these numbers are stored as doubles
    lab_hours = DoubleField(default = 0)
    credit_hours = DoubleField(default = 3)
    lecture_hours = DoubleField(default = 3)
    tutorial_hours = DoubleField(default = 0)
    title = TextField()
    description = TextField(null = True)
    course = ForeignKeyField(Course, related_name = 'generations')
    other_info = TextField(null = True)
    previous_course = TextField(null = True)
    start_year = IntegerField()
    end_year = IntegerField()

    class Meta:
        order_by = [ '-end_year' ]

    def differs_from(self, details):
        return (self.labs != details['Labs'] or
            self.credit_hours != details['Credit Hours'] or
            self.lecture_hours != details['Lecture Hours'] or
            self.title != details['Title'] or
            self.description != details['Description'] or
            self.other_info != details['Other info'] or
            self.previous_course != details['PreviousCourseCode'])

    def weights(self):
        return [
            ('Lectures', u'', self.credit_hours / 3.0),
            (
                'Labs', u'%f/3 ⨉ 0.27' % self.lab_hours,
                self.lab_hours / 3.0 * 0.27
            ),
            ('Tutorials', u'', self.tutorial_hours * 0.14),
        ]

    def years(self):
        if self.start_year == self.end_year:
            return str(self.start_year)

        else:
            return u'%s–%s' % (self.start_year, self.end_year)

    def __str__(self):
        return '%s (%s)' % (self.course, self.years())


class Student(BaseModel):
    """
    A student is typically a non-undergrad student
    """
    name = TextField()
    email = TextField()

    def __str__(self):
        return '%s (%s)' % (name, email)


class Offering(ValidatableModel):
    """
    Display the current courses on offering during the current session
    """
    enrolment = IntegerField(null = True)
    semester = ForeignKeyField(Semester)
    generation = ForeignKeyField(CourseGeneration, related_name = 'offerings')
    lab_sections = IntegerField(default = 1)

    class Meta:
        order_by = [ '-semester' ]

    def credit(self):
        return sum([ value for (_, _, value) in self.weights() ])

    def weights(self):
        size_factor = 1
        if self.enrolment:
            size_factor += max(0, (self.enrolment - 75.0) / 75 / 2)

        section_factor = {
            'Labs': self.lab_sections,
            'Lectures': 1.0,
            'Tutorials': 1.0,
        }

        return [
            (key, formula, val * size_factor * section_factor[key])
            for (key, formula, val) in self.generation.weights()
        ]

    def __str__(self):
        return '%s (%s)' % (self.generation.course, self.semester)


class Role(BaseModel):
    """
    These fields represent the class of the user and information they have access too, dept is short for department.
    """
    role_name = TextField()
    view_you = BooleanField()
    view_dept = BooleanField()
    view_all = BooleanField()
    edit_dept = BooleanField()


class SupervisionClass(BaseModel):
    """
    Supervising student level, grad, under grad, ect
    """
    description = TextField()
    weight = FloatField()


class ProjectClass(BaseModel):
    """
    Supervising student level, grad, under grad, ect
    """
    description = TextField()
    weight = FloatField()


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
    semester = ForeignKeyField(Semester, related_name = 'projects')

    def credit(self):
        return 0.125


class Supervision(BaseModel):
    """
    A table to tie together students ans their class
    """
    student_id = ForeignKeyField(Student)
    supervision_class_id = ForeignKeyField(SupervisionClass)
    semester = ForeignKeyField(Semester)

    def credit(self):
        # Graduate student supervision credit is based on an annual credit
        # of 0.14, so divide it by three each term.
        return 0.14 / 3


class Adjustment(BaseModel):
    """
    A human entry in that overrides the automatic data
    """
    weight = FloatField(null = True)
    comment = TextField(null = True)
    overide_value = FloatField(null = True)
    overide_address = TextField(null = True)
    instructor = ForeignKeyField(Person, null = True)


class Activity(BaseModel):
    """
    A record of someone doing something that counts for teaching credit.
    """

    # Who performed the activity.
    subject = ForeignKeyField(Person, related_name = 'activities')

    instruction = ForeignKeyField(Offering, null = True,
            related_name = 'instructors')

    supervision = ForeignKeyField(Supervision, null = True)
    project = ForeignKeyField(ProjectSupervision, null = True)
    split = FloatField(null = True)

    def credit(self):
        shares = Activity.select()

        if self.instruction:
            total = self.instruction.credit()
            shares = shares.where(Activity.instruction == self.instruction)

        elif self.supervision:
            total = self.supervision.credit()
            shares = shares.where(Activity.supervision == self.supervision)

        elif self.project:
            total = self.project.credit()
            shares = shares.where(Activity.project == self.project)

        # If we have an explicit `split` value, use it, otherwise assume
        # equal shares among all visible instructors/supervisors
        if self.split: return total / self.split
        else: return total / shares.count()

    def __getattr__(self, name):
        if name == 'total_credit':
            return self.credit()

        raise AttributeError


ALL_TABLES = [
    Activity,
    Adjustment,
    Course,
    CourseGeneration,
    Offering,
    Person,
    PersonalLoad,
    ProjectClass,
    ProjectSupervision,
    ProjectType,
    Role,
    Semester,
    Session,
    Student,
    Supervision,
    SupervisionClass,
    TeachingLoad,
]

def get():
    return db

def init(drop_first = True):
    if drop_first:
        db.drop_tables(ALL_TABLES, safe = True)

    db.create_tables(ALL_TABLES)

    db.fall = Session.create(code = 'F', name = 'Fall')
    db.winter = Session.create(code = 'W', name = 'Winter')
    db.spring = Session.create(code = 'S', name = 'Spring')
    db.intersession = Session.create(code = 'I', name = 'Intersession')
    db.summer = Session.create(code = 's', name = 'Summer')

    TeachingLoad.create(name = 'Engineering ASM', load = 4.0)
    TeachingLoad.create(name = 'New faculty remission', load = -1.0)
