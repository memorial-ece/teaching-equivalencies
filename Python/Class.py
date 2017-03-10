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

from peewee import *


class Term(Model):
	id = IntegerField(primary_key=True)
	year = DateField()
	session = IntegerField()
# session refers to the fall winter and spring sessions, these are respectively represented by the numbers 1,2, and 3


class Person(Model):
	name = TextField(null=False)
	email = TextField(unique=True)
	id = IntegerField(primary_key=True)
	start = ForeignKeyField(Term, related_name='startdate',null=False)
# A person in this database is a teaching professional


class Course(Model):
	id = IntegerField(primary_key=True)
	subject = TextField()
	code = CharField(4)


class CourseGeneration(Model):
	id = IntegerField(primary_key=True)
	labs = TextField(null=True)
	credit_hours = TextField(null=True)
	lecture_hours = TextField(null=True)
	title = TextField(null=True)
	comments = TextField(null=True)
	course_id = ForeignKeyField(Course, related_name='course_gen', null=True)
	other_info = TextField(null=True)
	old_course_id = TextField(null=True)
	year_of_valid_generation = TextField(null=False)
	year_valid_to = TextField(null=False)
# other_info, and old_course_id maybe inconsistent but that is because of the ripping process turned up the reported results.


class Student(Model):
	id = IntegerField(primary_key=True)
	name = TextField()
	email = TextField()
# A student is typically a non-undergrad student


class Offering(Model):
	id = IntegerField(primary_key=True)
	enrolment = IntegerField()
	prof_id = ForeignKeyField(Person, related_name='instructor')
	semester_id = ForeignKeyField(Term, related_name='offering')
	course_gen_id = ForeignKeyField(CourseGeneration, related_name='offerings')
	weight = FloatField()
# Display the current courses on offering during the current session


class Role(Model):
	id = IntegerField(primary_key=True)
	role_name = TextField(null=False)
	view_you = BooleanField(null=False)
	view_dept = BooleanField(null=False)
	view_All = BooleanField(null=False)
	edit_dept = BooleanField(null=False)
# These fields are meant to represent the class of the user and information they have access too, dept is short for department.


class SupervisionClass(Model):
	id = IntegerField(primary_key=True)
	description = TextField(null=False)
	weight = FloatField(null=False)
# Supervising students


class ProjectClass(Model):
	id = IntegerField(primary_key=True)
	description = TextField(null=False)
	weight = FloatField(null=False)
# Supervising projects

class ProjectTeam(Model):
	id = IntegerField(primary_key=True)
	name = TextField()
	email = TextField()


class RolePerson(Model):
	prof = ForeignKeyField(Person, related_name='perosn_id')
	role = ForeignKeyField(Role, related_name='role_id')
# A way to tie multiple people to different roles.


class ProjectSupervision(Model):
	id = IntegerField(primary_key=True)
	prof_id = ForeignKeyField(Person, related_name='supervisied_projects')
	pTeam_id = ForeignKeyField(ProjectTeam, related_name='projects')
	project_class_id = ForeignKeyField(ProjectClass, related_name='projects')
	semester_id = ForeignKeyField(Term, related_name='projects')


class Supervision(Model):
	id = IntegerField(primary_key=True)
	prof_id = ForeignKeyField(Person, related_name='supervised_people')
	student_id = ForeignKeyField(Student, related_name='supervisions')
	supervision_class_id = ForeignKeyField(SupervisionClass, related_name='supervisions')
	semester_id = ForeignKeyField(Term, related_name='supervisions')


class Adjustment(Model):
	id = IntegerField(primary_key=True)
	weight = FloatField()
	comment = TextField()
	prof_id = ForeignKeyField(Person, related_name='made_change')
