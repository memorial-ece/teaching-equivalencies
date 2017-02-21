from peewee import *


class Person(Model):
	name = TextField()
	email = TextField()
	prof_id = IntegerField(unique=True, primary_key=True, null=False)


class Course(Model):
	course_id = IntegerField(unique=True, primary_key=True, null=False)
	subject = TextField()
	course_num = CharField(4)


class CourseGeneration(Model):
	course_gen_id = IntegerField(unique=True, primary_key=True, null=False)
	labs = IntegerField()
	credit_hours = IntegerField()
	title = TextField()
	course_id = ForeignKeyField(Course, related_name='course_gen')


class Student(Model):
	student_id = IntegerField(primary_key=True, unique=True, null=False)
	student_name = TextField()
	student_email = TextField()


class Term(Model):
	semester_id = IntegerField(unique=True, primary_key=True, null=False)
	year = DateField()
	session = IntegerField()


class Offering(Model):
	offering_id = IntegerField(unique=True, primary_key=True, null=False, )
	students_taking = IntegerField()
	id = ForeignKeyField(Person, related_name='taking')
	semester_id = ForeignKeyField(Term, related_name='offering')
	course_gen_id = ForeignKeyField(CourseGeneration, related_name='offerings')


class Role(Model):
	role_id = IntegerField(primary_key=True, unique=True, null=False)
	role_name = TextField()
	view_only_you = BooleanField()
	view_only_dept = BooleanField()
	view_only_All = BooleanField()
	edit_dept = BooleanField()


class SupervisionClass(Model):
	supervision_class_id = IntegerField(primary_key=True, unique=True, null=False)
	description = TextField()
	weight = FloatField()


class ProjectClass(Model):
	project_class_id = IntegerField(primary_key=True, unique=True, null=False)
	description = TextField()
	weight = FloatField()


class PseudoPeople(Model):
	pseudo_id = IntegerField(primary_key=True, unique=True, null=False)
	pseudo_name = TextField()
	pseudo_email = TextField()


class RolePerson(Model):
	id = ForeignKeyField(Person, related_name='people_roles')
	role_id = ForeignKeyField(Role, related_name='roles_ofpeople')


class ProjectSupervision(Model):
	project_supervision_id = IntegerField(primary_key=True, unique=True, null=False)
	prof_id = ForeignKeyField(Person, related_name='supervisied_projects')
	pseudo_id = ForeignKeyField(PseudoPeople, related_name='projects')
	project_class_id = ForeignKeyField(ProjectClass, related_name='projects')
	semester_id = ForeignKeyField(Term, related_name='projects')


class Supervision(Model):
	supervision_id = IntegerField(primary_key=True, unique=True, null=False)
	prof_id = ForeignKeyField(Person, related_name='supervised_people')
	student_id = ForeignKeyField(Student, related_name='supered')
	supervision_class_id = ForeignKeyField(SupervisionClass, related_name='supered')
	semester_id = ForeignKeyField(Term, related_name='supered')


class Adjustment(Model):
	adjustment_id = IntegerField(primary_key=True, unique=True, null=False)
	adjustment_weight = FloatField()
	# AUDITDATE = DateTimeField()
	audit_comment = TextField()
	prof_id = ForeignKeyField(Person, related_name='made_change')
