from playhouse.csv_loader import *
from Populate import *


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


def import_pseudo_people():
	load_csv(PseudoPeople, 'account-PseudoPeople.csv')
	
	
def import_role_person():
	load_csv(RolePerson, 'account-RolePerson.csv')


def import_project_supervision():
	load_csv(ProjectSupervision, 'account-ProjectSupervision.csv')


def import_supervision():
	load_csv(Supervision, 'account-Supervision.csv')


def import_adjustment():
	load_csv(Adjustment, 'account-Adjustment.csv')
