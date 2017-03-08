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

from playhouse.csv_loader import *
from Python.Class import *


def export_profile():
	with open('table_Person.csv', 'w') as fh:
		query = Person.select().order_by(Person.id)
		dump_csv(query, fh)


def export_supervision():
	with open('table_Supervision.csv', 'w') as fh:
		query = Supervision.select().order_by(Supervision.id)
		dump_csv(query, fh)


def export_supervision_class():
	with open('table_SupervisionClass.csv', 'w') as fh:
		query = SupervisionClass.select().order_by(SupervisionClass.id)
		dump_csv(query, fh)


def export_course():
	with open('table_Course.csv', 'w') as fh:
		query = Course.select().order_by(Course.course_num)
		dump_csv(query, fh)


def export_course_generation():
	with open('table_CourseGeneration.csv', 'w') as fh:
		query = CourseGeneration.select().order_by(CourseGeneration.id)
		dump_csv(query, fh)


def export_student():
	with open('table_Student.csv', 'w') as fh:
		query = Student.select().order_by(Student.id)
		dump_csv(query, fh)


def export_term():
	with open('table_Term.csv', 'w') as fh:
		query = Term.select().order_by(Term.id)
		dump_csv(query, fh)


def export_offering():
	with open('table_Offering.csv', 'w') as fh:
		query = Offering.select().order_by(Offering.id)
		dump_csv(query, fh)


def export_role():
	with open('table_Role.csv', 'w') as fh:
		query = Role.select().order_by(Role.id)
		dump_csv(query, fh)


def export_project_class():
	with open('table_ProjectClass.csv', 'w') as fh:
		query = ProjectClass.select().order_by(ProjectClass.id)
		dump_csv(query, fh)


def export_ProjectTeam():
	with open('table_PseudoPeople.csv', 'w') as fh:
		query = ProjectTeam.select().order_by(ProjectTeam.id)
		dump_csv(query, fh)


def export_role_person():
	with open('table_RolePerson.csv', 'w') as fh:
		query = RolePerson.select().order_by(RolePerson.id)
		dump_csv(query, fh)


def export_project_supervision():
	with open('table_ProjectSupervision.csv', 'w') as fh:
		query = ProjectSupervision.select().order_by(ProjectSupervision.id)
		dump_csv(query, fh)


def export_adjustment():
	with open('table_Adjustment.csv', 'w') as fh:
		query = Adjustment.select().order_by(Adjustment.id)
		dump_csv(query, fh)
