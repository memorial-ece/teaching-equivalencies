from peewee import *

class Person(Model):
    Name = TextField()
    Email = TextField()
    ID = IntegerField(unique=True, primary_key=True, null=False)

class Course(Model):
    CRN = IntegerField(unique=True, primary_key=True, null=False)
    Subj = TextField()
    Crse = IntegerField()

class CourseGeneration(Model):
    CourseGenID = IntegerField(unique=True, primary_key=True, null=False)
    Labs = IntegerField()
    CreditHours = IntegerField()
    Title = TextField()
    CRN = ForeignKeyField(Course, related_name='CourseGenerations')


class Term(Model):
    SemesterID = IntegerField(unique=True, primary_key=True, null=False)
    Year = DateField()
    Session = IntegerField()


class Offering(Model):
    OID = IntegerField(unique=True, primary_key=True, null=False, )
    StudentsTaking = IntegerField()
    ID = ForeignKeyField(Person, related_name='Offerings')
    SemesterID = ForeignKeyField(Term, related_name='Offerings')


class Role(Model):
    RoleID = IntegerField(primary_key=True, unique=True, null=False)
    ViewOnlyYou = IntegerField()
    ViewOnlyDept = IntegerField()
    ViewOnlyAll = IntegerField()
    EditDept = IntegerField()


class RolePerson(Model):
    ID = ForeignKeyField(Person, related_name='RolePersons')
    RoleID = ForeignKeyField(Role, related_name='RolePersons')


class ProjectSupervision(Model):
    ProjectSupervisionID = IntegerField(primary_key=True, unique=True, null=False)
    ID = ForeignKeyField(Person, related_name='ProjectSupervisions')
    PseudoID = ForeignKeyField(PseudoPeople, related_name='ProjectSupervisions')
    ProjectClassID = ForeignKeyField(ProjectClass, related_name='ProjectSupervisions')
    SemesterID = ForeignKeyField(Term, related_name='ProjectSupervisions')


class ProjectClass(Model):
    ProjectClassID = IntegerField(primary_key=True, unique=True, null=False)
    Grad = FloatField()
    UGrad = FloatField()
    Master = FloatField()


class Supervision(Model):
    SupervisionID = IntegerField(primary_key=True, unique=True, null=False)
    ID = ForeignKeyField(Person, related_name='Supervisions')
    StudentID = ForeignKeyField(Student, related_name='Supervisions')
    SupervisionClassID = ForeignKeyField(SupervisionClass, related_name='Supervisions')
    SemesterID = ForeignKeyField(Term, related_name='ProjectSupervisions')


class SupervisionClass(Model):
    SupervisionClassID = IntegerField(primary_key=True, unique=True, null=False)
    Grad = FloatField()
    UGrad = FloatField()
    Master = FloatField()


class PseudoPeople(Model):
    PseudoID = IntegerField(primary_key=True, unique=True, null=False)
    PName = TextField()
    PEmail = TextField()


class Student(Model):
    StudentID = IntegerField(primary_key=True, unique=True, null=False)
    SName = TextField()
    SEmail = TextField()


class Adjustment(Model):
    AdjustmentID = IntegerField(primary_key=True, unique=True, null=False)
    ADJWeight = FloatField()
    AUDITDATE = DateTimeField()
    AUDITCOMMENT = TextField()
    ID = ForeignKeyField(Person, related_name='Adjustments')


@app.route('/peewee')
def peewee():
    database.connect()
    database.create_tables(
        [Person, Course, CourseGeneration, Adjustment, PseudoPeople, Supervision, SupervisionClass, ProjectClass,
         ProjectSupervision, Offering, Term, Student, Role, Role])
