from playhouse.csv_loader import *
from Populate import *


def exportProfile():
	with open('account-Person.csv', 'w') as fh:
		query = Person.select().order_by(Person.ID)
		dump_csv(query, fh)


def exportSupervision():
	with open('account-Supervision.csv', 'w') as fh:
		query = Supervision.select().order_by(Supervision.SupervisionID)
		dump_csv(query, fh)


def exportSupervisionClass():
	with open('account-SupervisionClass.csv', 'w') as fh:
		query = SupervisionClass.select().order_by(SupervisionClass.SupervisionClassID)
		dump_csv(query, fh)


def exportCourse():
	with open('account-Course.csv', 'w') as fh:
		query = Course.select().order_by(Course.CRN)
		dump_csv(query, fh)


def exportCourseGeneration():
	with open('account-CourseGeneration.csv', 'w') as fh:
		query = CourseGeneration.select().order_by(CourseGeneration.CourseGenID)
		dump_csv(query, fh)


def exportStudent():
	with open('account-Student.csv', 'w') as fh:
		query = Student.select().order_by(Student.StudentID)
		dump_csv(query, fh)


def exportTerm():
	with open('account-Term.csv', 'w') as fh:
		query = Term.select().order_by(Term.SemesterID)
		dump_csv(query, fh)


def exportOffering():
	with open('account-Offering.csv', 'w') as fh:
		query = Offering.select().order_by(Offering.OID)
		dump_csv(query, fh)


def exportRole():
	with open('account-Role.csv', 'w') as fh:
		query = Role.select().order_by(Role.RoleID)
		dump_csv(query, fh)


def exportProjectClass():
	with open('account-ProjectClass.csv', 'w') as fh:
		query = ProjectClass.select().order_by(ProjectClass.ProjectClassID)
		dump_csv(query, fh)


def exportPseudoPeople():
	with open('account-PseudoPeople.csv', 'w') as fh:
		query = PseudoPeople.select().order_by(PseudoPeople.PseudoID)
		dump_csv(query, fh)


def exportRolePerson():
	with open('account-RolePerson.csv', 'w') as fh:
		query = RolePerson.select().order_by(RolePerson.ID)
		dump_csv(query, fh)


def exportProjectSupervision():
	with open('account-ProjectSupervision.csv', 'w') as fh:
		query = ProjectSupervision.select().order_by(ProjectSupervision.ProjectSupervisionID)
		dump_csv(query, fh)


def exportAdjustment():
	with open('account-Adjustment.csv', 'w') as fh:
		query = Adjustment.select().order_by(Adjustment.AdjustmentID)
		dump_csv(query, fh)