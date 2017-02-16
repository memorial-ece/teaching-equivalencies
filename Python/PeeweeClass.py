from peewee import *

class Person(Model):
	Name = TextField()
	Email = TextField()
	ID = IntegerField(unique=True, primary_key=True, null=False)

	class Meta:
		order_by = ('Name',)

	def power1(self):
		# query other users through the "relationship" table
		return Person.select().join(
			RolePerson, on=RolePerson.ID,
		).where(RolePerson.RoleID == self)

	def power2(self):
		return Person.select().join(
			RolePerson, on=RolePerson.RoleID,
		).where(RolePerson.ID == self)

	def poswers(self, Person):
		return RolePerson.select().where(
			(RolePerson.RoleID == self) &
			(RolePerson.ID == Person)
		).count() > 0


class Course(Model):
	CRN = IntegerField(unique=True, primary_key=True, null=False)
	Subj = TextField()
	Crse = IntegerField()


class CourseGeneration(Model):
	CourseGenID = IntegerField(unique=True, primary_key=True, null=False)
	Labs = IntegerField()
	CreditHours = IntegerField()
	Title = TextField()
	CRN = ForeignKeyField(Course, related_name='course_gen')


class Student(Model):
	StudentID = IntegerField(primary_key=True, unique=True, null=False)
	SName = TextField()
	SEmail = TextField()


class Term(Model):
	SemesterID = IntegerField(unique=True, primary_key=True, null=False)
	Year = DateField()
	Session = IntegerField()


class Offering(Model):
	OID = IntegerField(unique=True, primary_key=True, null=False, )
	StudentsTaking = IntegerField()
	ID = ForeignKeyField(Person, related_name='taking')
	SemesterID = ForeignKeyField(Term, related_name='offering')
	CourseGenID = ForeignKeyField(CourseGeneration, related_name='offerings')


class Role(Model):
	RoleID = IntegerField(primary_key=True, unique=True, null=False)
	ViewOnlyYou = BooleanField()
	ViewOnlyDept = BooleanField()
	ViewOnlyAll = BooleanField()
	EditDept = BooleanField()


class SupervisionClass(Model):
	SupervisionClassID = IntegerField(primary_key=True, unique=True, null=False)
	Description = TextField()
	Weight = FloatField()


class ProjectClass(Model):
	ProjectClassID = IntegerField(primary_key=True, unique=True, null=False)
	Description = TextField()
	Weight = FloatField()


class PseudoPeople(Model):
	PseudoID = IntegerField(primary_key=True, unique=True, null=False)
	PName = TextField()
	PEmail = TextField()


class RolePerson(Model):
	ID = ForeignKeyField(Person, related_name='people_roles')
	RoleID = ForeignKeyField(Role, related_name='roles_ofpeople')

class ProjectSupervision(Model):
	ProjectSupervisionID = IntegerField(primary_key=True, unique=True, null=False)
	ID = ForeignKeyField(Person, related_name='supervisied_projects')
	PseudoID = ForeignKeyField(PseudoPeople, related_name='projects')
	ProjectClassID = ForeignKeyField(ProjectClass, related_name='projects')
	SemesterID = ForeignKeyField(Term, related_name='projects')


class Supervision(Model):
	SupervisionID = IntegerField(primary_key=True, unique=True, null=False)
	ID = ForeignKeyField(Person, related_name='supervised_people')
	StudentID = ForeignKeyField(Student, related_name='supered')
	SupervisionClassID = ForeignKeyField(SupervisionClass, related_name='supered')
	SemesterID = ForeignKeyField(Term, related_name='supered')


class Adjustment(Model):
	AdjustmentID = IntegerField(primary_key=True, unique=True, null=False)
	ADJWeight = FloatField()
	AUDITDATE = DateTimeField()
	AUDITCOMMENT = TextField()
	ID = ForeignKeyField(Person, related_name='made_change')
