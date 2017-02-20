from playhouse.csv_loader import *
from Populate import *

def importProfile():
	load_csv(Person, 'account-Person.csv')

def importCourse():
	load_csv(Course, 'account-Course.csv')

def importCourseGeneration():
	load_csv(CourseGeneration, 'account-CourseGeneration.csv')

def importStudent():
	load_csv(Student, 'account-Student.csv')

def importTerm():
	load_csv(Term, 'account-Term.csv')

def importOffering():
	load_csv(Offering, 'account-Offering.csv')

def importRole():
	load_csv(Role, 'account-Role.csv')

def importSupervisionClass():
	load_csv(SupervisionClass, 'account-SupervisionClass.csv')

def importProjectClass():
	load_csv(ProjectClass, 'account-ProjectClass.csv')

def importPseudoPeople():
	load_csv(PseudoPeople, 'account-PseudoPeople.csv')
	
def importRolePerson():
	load_csv(RolePerson, 'account-RolePerson.csv')

def importProjectSupervision():
	load_csv(ProjectSupervision, 'account-ProjectSupervision.csv')

def importSupervision():
	load_csv(Supervision, 'account-Supervision.csv')

def importAdjustment():
	load_csv(Adjustment, 'account-Adjustment.csv')
