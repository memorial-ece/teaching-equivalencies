from playhouse.csv_loader import *
from Class import *


def export_profile():
	with open('table_Person.csv', 'w') as fh:
		query = Person.select().order_by(Person.prof_id)
		dump_csv(query, fh)


def export_supervision():
	with open('table_Supervision.csv', 'w') as fh:
		query = Supervision.select().order_by(Supervision.supervision_id)
		dump_csv(query, fh)


def export_supervision_class():
	with open('table_SupervisionClass.csv', 'w') as fh:
		query = SupervisionClass.select().order_by(SupervisionClass.supervision_class_id)
		dump_csv(query, fh)


def export_course():
	with open('table_Course.csv', 'w') as fh:
		query = Course.select().order_by(Course.course_num)
		dump_csv(query, fh)


def export_course_generation():
	with open('table_CourseGeneration.csv', 'w') as fh:
		query = CourseGeneration.select().order_by(CourseGeneration.course_gen_id)
		dump_csv(query, fh)


def export_student():
	with open('table_Student.csv', 'w') as fh:
		query = Student.select().order_by(Student.student_id)
		dump_csv(query, fh)


def export_term():
	with open('table_Term.csv', 'w') as fh:
		query = Term.select().order_by(Term.semester_id)
		dump_csv(query, fh)


def export_offering():
	with open('table_Offering.csv', 'w') as fh:
		query = Offering.select().order_by(Offering.offering_id)
		dump_csv(query, fh)


def export_role():
	with open('table_Role.csv', 'w') as fh:
		query = Role.select().order_by(Role.role_id)
		dump_csv(query, fh)


def export_project_class():
	with open('table_ProjectClass.csv', 'w') as fh:
		query = ProjectClass.select().order_by(ProjectClass.project_class_id)
		dump_csv(query, fh)


def export_pseudo_people():
	with open('table_PseudoPeople.csv', 'w') as fh:
		query = PseudoPeople.select().order_by(PseudoPeople.pseudo_id)
		dump_csv(query, fh)


def export_role_person():
	with open('table_RolePerson.csv', 'w') as fh:
		query = RolePerson.select().order_by(RolePerson.role_id)
		dump_csv(query, fh)


def export_project_supervision():
	with open('table_ProjectSupervision.csv', 'w') as fh:
		query = ProjectSupervision.select().order_by(ProjectSupervision.project_supervision_id)
		dump_csv(query, fh)


def export_adjustment():
	with open('table_Adjustment.csv', 'w') as fh:
		query = Adjustment.select().order_by(Adjustment.adjustment_id)
		dump_csv(query, fh)