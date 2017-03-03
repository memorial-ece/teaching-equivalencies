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


class Person(Model):
	name = TextField()
	email = TextField()
	id = IntegerField(primary_key=True)


class Course(Model):
	id = IntegerField(primary_key=True)
	subject = TextField()
	course_num = CharField(4, unique=True)


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


class Student(Model):
	id = IntegerField(primary_key=True)
	name = TextField()
	email = TextField()


class Term(Model):
	id = IntegerField(primary_key=True)
	year = DateField()
	session = IntegerField()


class Offering(Model):
	id = IntegerField(primary_key=True)
	students_taking = IntegerField()
	prof_id = ForeignKeyField(Person, related_name='taking')
	semester_id = ForeignKeyField(Term, related_name='offering')
	course_gen_id = ForeignKeyField(CourseGeneration, related_name='offerings')


class Role(Model):
	id = IntegerField(primary_key=True)
	role_name = TextField()
	view_only_you = BooleanField()
	view_only_dept = BooleanField()
	view_only_All = BooleanField()
	edit_dept = BooleanField()


class SupervisionClass(Model):
	id = IntegerField(primary_key=True)
	description = TextField()
	weight = FloatField()


class ProjectClass(Model):
	id = IntegerField(primary_key=True)
	description = TextField()
	weight = FloatField()


class PseudoPeople(Model):
	id = IntegerField(primary_key=True)
	pseudo_name = TextField()
	pseudo_email = TextField()


class RolePerson(Model):
	prof = ForeignKeyField(Person, related_name='people_roles')
	role = ForeignKeyField(Role, related_name='roles_ofpeople')


class ProjectSupervision(Model):
	id = IntegerField(primary_key=True)
	prof_id = ForeignKeyField(Person, related_name='supervisied_projects')
	pseudo_id = ForeignKeyField(PseudoPeople, related_name='projects')
	project_class_id = ForeignKeyField(ProjectClass, related_name='projects')
	semester_id = ForeignKeyField(Term, related_name='projects')


class Supervision(Model):
	id = IntegerField(primary_key=True)
	prof_id = ForeignKeyField(Person, related_name='supervised_people')
	student_id = ForeignKeyField(Student, related_name='supered')
	supervision_class_id = ForeignKeyField(SupervisionClass, related_name='supered')
	semester_id = ForeignKeyField(Term, related_name='supered')


class Adjustment(Model):
	id = IntegerField(primary_key=True)
	adjustment_weight = FloatField()
	comment = TextField()
	prof_id = ForeignKeyField(Person, related_name='made_change')
