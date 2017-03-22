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

import_file


def import_profile():
	load_csv(Person, 'Person.csv')


def import_course():
	load_csv(Course, 'Course.csv')


def import_course_generation():
	load_csv(CourseGeneration, 'CourseGeneration.csv')


def import_student():
	load_csv(Student, 'Student.csv')


def import_term():
	load_csv(Term, 'Term.csv')


def import_offering():
	load_csv(Offering, 'Offering.csv')


def import_role():
	load_csv(Role, 'Role.csv')


def import_supervision_class():
	load_csv(SupervisionClass, 'SupervisionClass.csv')


def import_project_class():
	load_csv(ProjectClass, 'ProjectClass.csv')


def import_ProjectTeam():
	load_csv(ProjectTeam, 'PseudoPeople.csv')
	
	
def import_role_person():
	load_csv(RolePerson, 'RolePerson.csv')


def import_project_supervision():
	load_csv(ProjectSupervision, 'ProjectSupervision.csv')


def import_supervision():
	load_csv(Supervision, 'Supervision.csv')


def import_adjustment():
	load_csv(Adjustment, 'Adjustment.csv')
