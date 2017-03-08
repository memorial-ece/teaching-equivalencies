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

def import_profile():
	load_csv(Person, 'account-Person.csv')


def import_course():
	load_csv(Course, 'account-Course.csv')


def import_course_generation():
	load_csv(CourseGeneration, 'account-CourseGeneration.csv')


def import_student():
	load_csv(Student, 'account-Student.csv')


def import_term():
	load_csv(Term, 'account-Term.csv')


def import_offering():
	load_csv(Offering, 'account-Offering.csv')


def import_role():
	load_csv(Role, 'account-Role.csv')


def import_supervision_class():
	load_csv(SupervisionClass, 'account-SupervisionClass.csv')


def import_project_class():
	load_csv(ProjectClass, 'account-ProjectClass.csv')


def import_ProjectTeam():
	load_csv(ProjectTeam, 'account-PseudoPeople.csv')
	
	
def import_role_person():
	load_csv(RolePerson, 'account-RolePerson.csv')


def import_project_supervision():
	load_csv(ProjectSupervision, 'account-ProjectSupervision.csv')


def import_supervision():
	load_csv(Supervision, 'account-Supervision.csv')


def import_adjustment():
	load_csv(Adjustment, 'account-Adjustment.csv')
