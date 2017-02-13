from flask import *
import sqlite3 as sql
import os
import random
import datetime
app = Flask(__name__)
random.seed(a=2)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
DATABASE = 'database.db'
@app.route("/profile/<CID>")
def Profile(CID):
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	c = con.cursor()
	c.execute("select * from Person where ID = ?", (CID,))
	rows = c.fetchall()
	return render_template("listcompanyforempl.html", rows=rows, ID=CID)
@app.route('/resettables')
def bringdtatonline():
	con = sql.connect("database.db")
	c = con.cursor()
	c.execute('drop table if exists CourseGeneration')
	c.execute('drop table if exists Course')
	c.execute('drop table if exists Offering')
	c.execute('drop table if exists Term')
	c.execute('drop table if exists Supervision')
	c.execute('drop table if exists Person')
	c.execute('drop table if exists RolePerson')
	c.execute('drop table if exists Adjustment')
	c.execute('drop table if exists ProjectSupervision')
	c.execute('drop table if exists SupervisionClass')
	c.execute('drop table if exists PseudoPeople')
	c.execute('drop table if exists Role')
	c.execute('drop table if exists ProjectClass')
	c.execute('CREATE TABLE CourseGeneration(COURSEGEN int NOT NULL, CRN int, Weight REAL, PRIMARY KEY (COURSEGEN),FOREIGN KEY (CRN) REFERENCES Course (CRN))')
	c.execute('CREATE TABLE Course(CRN int, Subj text, Crse text, Sec text, Session text, Title text, PRIMARY KEY (CRN))')
	c.execute('CREATE TABLE Offering(OID int NOT NULL, Semester text, ID int, COURSEGEN int, PRIMARY KEY (OID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (COURSEGEN) REFERENCES CourseGeneration (COURSEGEN))')
	c.execute('CREATE TABLE Person(ID int NOT NULL, Email text NOT NULL, Name text NOT NULL, PRIMARY KEY (ID))')
	c.execute('CREATE TABLE Term(Semester text NOT NULL, PRIMARY KEY (Semester))')
	#ADD THE AUTOIMCREMENT STATMENT BACK TO ADJ ID, AUDIT ID, AND THE DATE
	c.execute('CREATE TABLE RolePerson(ID int, RoleID int, FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (RoleID) REFERENCES Role (RoleID))')
	c.execute('CREATE TABLE Role(RoleID int, ViewOnlyYou int,ViewOnlyDept int, ViewOnlyAll int, EditDept int, PRIMARY KEY (RoleID))')
	c.execute('CREATE TABLE ProjectSupervision(ProjectSupervisionID int NOT NULL, ID int,PseudoID int, ProjectClassID int, PRIMARY KEY(ProjectSupervisionID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (ProjectClassID) REFERENCES ProjectClass (ProjectClassID), FOREIGN KEY (PseudoID) REFERENCES PseudoPeople (PseudoID))')
	c.execute('CREATE TABLE SupervisionClass(SupervisionClassID int NOT NULL, Graduate REAL, Undergrad REAL, Masters REAL, PRIMARY KEY (SupervisionClassID))')
	c.execute('CREATE TABLE PseudoPeople(PseudoID int NOT NULL, PseudoName text NOT NULL, Email text, Team text, int, PRIMARY KEY (PseudoID))')
	c.execute('CREATE TABLE ProjectClass(ProjectClassID int NOT NULL, Graduate REAL, Undergrad REAL, Masters REAL, PRIMARY KEY (ProjectClassID))')
	c.execute('CREATE TABLE Adjustment(AdjustmentID INTEGER PRIMARY KEY AUTOINCREMENT, ADJTO int NOT NULL, ID int, ADJWeight REAL,  AUDITDATE date, AUDITCOMMENT text, FOREIGN KEY (ID) REFERENCES Person (ID))')
	c.execute('CREATE TABLE Supervision(SupervisionID int NOT NULL, ID int, PseudoID int, SupervisionClassID int, PRIMARY KEY (SupervisionID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (SupervisionClassID) REFERENCES SupervisionClass (SupervisionClassID), FOREIGN KEY (PseudoID) REFERENCES PseudoPeople (PseudoID))')
	con.commit()
	ID=random.randrange(0,100)
	print (ID)
	return render_template('reset.html')

@app.route('/populate', methods=["GET","POST"])
def populate():
	count=0
	if 'roa' in locals():
		random.seed(a=1)
	while(True):
		count += 1
		WORDS = open('words').readlines()
		a=random.uniform(0,1)
		b=random.uniform(0,1)
		cb=random.uniform(0,1)
		word = random.choice(WORDS)
		Subj = random.choice(WORDS)
		Sec = random.choice(WORDS)
		Title = random.choice(WORDS)
		Session=random.choice(WORDS)
		Emale = word + "@mail.to"
		Teammates = ("no team", "a Team")
		Crse=random.randrange(0000,9999)
		myteam = random.choice(Teammates)
		print (myteam)
		print (a)
		print(b)
		con=sql.connect("database.db")
		c=con.cursor()
		ID=random.randrange(0,1000000000)
		CRN=random.randrange(00000,99999)
		sem1=open('semesters').readlines()
		sem2=random.choice(sem1)
		year1=random.randrange(1970,2017)
		year2=str(year1)
		put=sem2+year2
		print (put)
		if count == 111:
			roa=1
			break
		elif 20>count>10:
			c.execute ('INSERT INTO Person (ID,Email,Name) VALUES (?, ?, ?)', (ID, Emale, word))
			con.commit()
		elif 10>count>0:
			c.execute('insert into PseudoPeople (PseudoID,Email,PseudoName,Team) Values (?,?,?,?)', (ID, Emale, word,myteam))
			con.commit()
		elif 30>count>20:
			c.execute('insert into Course (CRN,Subj,Crse,Sec,Session,Title) Values (?,?,?,?,?,?)', (CRN,Subj,Crse,Sec,Session,Title))
			con.commit()
		elif 40>count>30:
			c.execute('insert into SupervisionClass(SupervisionClassID,Graduate,Undergrad,Masters) Values (?,?,?,?)', (ID,a,b,cb))
			con.commit()
		elif 50>count>40:
			c.execute('insert into ProjectClass(ProjectClassID,Graduate,Undergrad,Masters) Values (?,?,?,?)', (ID,a,b,cb))
			con.commit()
		elif 60>count>50:
			c.execute('insert into CourseGeneration(COURSEGEN,CRN,Weight) Values (?,?,?)', (ID,CRN,a))
			con.commit()
		elif 70>count>60:
			c.execute('insert into Term(Semester) Values (?)', (put,))
			con.commit()
		elif 80>count>70:
			c.execute('insert into Offering (OID) Values (?)', (ID,))
			con.commit()
		elif 90>count>80:
			c.execute('insert into Role(RoleID) Values (?)', (ID,))
			con.commit()
		elif 100>count>90:
			c.execute('insert into Supervision (SupervisionID) Values (?)', (ID,))
			con.commit()
		elif 110>count>100:
			c.execute('insert into ProjectSupervision (ProjectSupervisionID) Values (?)', (ID,))
			con.commit()
	return render_template('populate.html')
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db
@app.route('/listm', methods=['GET', 'POST'])
def listm():
	error=None
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	c = con.cursor()
	c.execute("select * from Person ")
	Person = c.fetchall()
	c.execute("select * from PseudoPeople ")
	Pseudo=c.fetchall()
	c.execute("select * from Course ")
	Course=c.fetchall()
	c.execute("select * from CourseGeneration ")
	CourseGeneration=c.fetchall()
	c.execute("select * from Term ")
	Term=c.fetchall()
	c.execute("select * from Offering ")
	Offering=c.fetchall()
	c.execute("select * from RolePerson ")
	RolePerson=c.fetchall()
	c.execute("select * from Role ")
	Role=c.fetchall()
	c.execute("select * from Adjustment ")
	Adjustment=c.fetchall()
	c.execute("select * from Supervision ")
	Supervison=c.fetchall()
	c.execute("select * from ProjectSupervision ")
	ProjectSupervision=c.fetchall()
	c.execute("select * from ProjectClass ")
	ProjectClass=c.fetchall()
	c.execute("select * from SupervisionClass ")
	SupervisionClass=c.fetchall()
	if request.method == 'POST':
		con = sql.connect("database.db")
		con.row_factory = sql.Row
		c = con.cursor()
		FIXER=request.form['FIXER']
		ID=request.form['ID']
		SID = request.form['SID']
		SCID = request.form['SCID']
		PCID = request.form['PCID']
		PID = request.form['PID']
		OID = request.form['OID']
		CGID = request.form['CGID']
		SEM= request.form['SEM']
		SUDO= request.form['SUDO']
		AUCOM=request.form['AUCOM']
		ADJTO=request.form['ADJTO']
		ADJW=request.form['ADJW']
		AUDITDATE=datetime.date.today()
		print(FIXER)
		if FIXER=="1":
			c.execute("update Offering set ID = ?,COURSEGEN=?,Semester=? where OID = ?", (ID,CGID,SEM,OID))
			con.commit()
		elif FIXER=="2":
			c.execute("update ProjectSupervision set ID = ?,Semester=?,ProjectClassID=? where ProjectSupervisionID = ?", (ID, SEM,PCID,PID))
			con.commit()
		elif FIXER=="3":
			c.execute("update Supervision set ID = ?,Semester=?,SupervisionClassID=? where SupervisionID = ?", (ID, SEM,SCID,SID))
			con.commit()
		elif FIXER=="4":
			c.execute("update PseudoPeople set SupervisionID=?,ProjectSupervisionID=? where PseudoID=?",(SID,PID,SUDO))
			con.commit()
		elif FIXER=="5":
			if not AUCOM=="":
				c.execute("Insert into Adjustment (ADJTO, ID, ADJWeight,AUDITDATE,AUDITCOMMENT) values (?,?,?,?,?)",(ADJTO,ID,ADJW,AUDITDATE,AUCOM))
				con.commit()
			else:
				error="comment not filled"
				return render_template("listcompany.html", error=error, Person=Person, Pseudo=Pseudo, Course=Course,SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,ProjectSupervision=ProjectSupervision, Supervision=Supervison, Adjustment=Adjustment,RolePerson=RolePerson, Role=Role, Term=Term, Offering=Offering,CourseGeneration=CourseGeneration)

	return render_template("listcompany.html", Person=Person, Pseudo=Pseudo, Course=Course,SupervisionClass=SupervisionClass,ProjectClass=ProjectClass,ProjectSupervision=ProjectSupervision,Supervision=Supervison,Adjustment=Adjustment,RolePerson=RolePerson,Role=Role,Term=Term,Offering=Offering,CourseGeneration=CourseGeneration)

@app.route('/Dashboard')
@app.route('/index')
@app.route('/',methods=["GET"])
def index():
    return render_template("Home.html")
@app.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p><a href="/">home</a>')
if __name__ == '__main__':
    app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000,debug=True)