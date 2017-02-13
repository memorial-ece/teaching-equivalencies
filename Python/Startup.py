from flask import *
import sqlite3 as sql
import os
import random
app = Flask(__name__)
random.seed(a=1)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
DATABASE = 'database.db'
@app.route("/profile/<ID>")
def Profile(ID):
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("select * from Person where ID = ?", (ID,))
	rows = cur.fetchall()
	return render_template("listcompanyforempl.html", rows=rows, ID=ID)
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
	c.execute('CREATE TABLE ProjectSupervision(ProjectSupervisionID int NOT NULL, ID int, ProjectClassID int, PRIMARY KEY(ProjectSupervisionID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (ProjectClassID) REFERENCES ProjectClass (ProjectClassID))')
	c.execute('CREATE TABLE SupervisionClass(SupervisionClassID int NOT NULL, Graduate REAL, Undergrad REAL, Masters REAL, PRIMARY KEY (SupervisionClassID))')
	c.execute('CREATE TABLE PseudoPeople(PseudoID int NOT NULL, PseudoName text NOT NULL, Email text, Team text,SupID int, ProjectID, int, PRIMARY KEY (PseudoID), FOREIGN KEY (SupID) REFERENCES Supervision (SupID), FOREIGN KEY (ProjectID) REFERENCES ProjectSupervision(ProjectID))')
	c.execute('CREATE TABLE ProjectClass(ProjectClassID int NOT NULL, Graduate REAL, Undergrad REAL, Masters REAL, PRIMARY KEY (ProjectClassID))')
	c.execute('CREATE TABLE Adjustment(AdjustmentID INTEGER PRIMARY KEY AUTOINCREMENT, ADJTO int NOT NULL, ID int, ADJWeight REAL,  AUDITDATE date, AUDITCOMMENT text NOT NULL, FOREIGN KEY (ID) REFERENCES Person (ID))')
	c.execute('CREATE TABLE Supervision(SupervisionID int NOT NULL, ID int, SupervisionClassID int, PRIMARY KEY (SupervisionID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (SupervisionClassID) REFERENCES SupervisionClass (SupervisionClassID))')
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
		c=random.uniform(0,1)
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
		print(c)
		con=sql.connect("database.db")
		c=con.cursor()
		ID=random.randrange(0,1000000000000)
		CRN=random.randrange(00000,99999)
		sem1=open('semesters').readlines()
		sem2=random.choice(sem1)
		year1=random.randrange(1970,2017)
		year2=str(year1)
		put=sem2+year2
		print (put)
		if count == 81:
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
		# elif 40>count>30:
		# 	c.execute('insert into SupervisionClass(SupervisionClassID,Graduate,Undergrad,Masters) Values (?,?,?,?)', (ID,a,b,c))
		# 	con.commit()
		# elif 50>count>40:
		# 	c.execute('insert into ProjectClass(ProjectClassID,Graduate,Undergrad,Masters) Values (?,?,?,?)', (ID,a,b,c))
		# 	con.commit()
		elif 60>count>50:
			c.execute('insert into CourseGeneration(COURSEGEN,CRN,Weight) Values (?,?,?)', (ID,CRN,a))
			con.commit()
		elif 60>count>50:
			c.execute('insert into Term(Semester) Values (?)', (put))
			con.commit()
	return render_template('populate.html')
@app.route("/work")
def workspace():
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db
@app.route('/listm', methods=['POST', 'GET'])
def listm():
	error=None
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("select * from Person ")
	Person = cur.fetchall()
	cur.execute("select * from PseudoPeople ")
	Pseudo=cur.fetchall()
	cur.execute("select * from Course ")
	Course=cur.fetchall()
	cur.execute("select * from CourseGeneration ")
	CourseGeneration=cur.fetchall()
	cur.execute("select * from Term ")
	Term=cur.fetchall()
	cur.execute("select * from Offering ")
	Offering=cur.fetchall()
	cur.execute("select * from RolePerson ")
	RolePerson=cur.fetchall()
	cur.execute("select * from Role ")
	Role=cur.fetchall()
	cur.execute("select * from Adjustment ")
	Adjustment=cur.fetchall()
	cur.execute("select * from Supervision ")
	Supervison=cur.fetchall()
	cur.execute("select * from ProjectSupervision ")
	ProjectSupervision=cur.fetchall()
	cur.execute("select * from ProjectClass ")
	ProjectClass=cur.fetchall()
	cur.execute("select * from SupervisionClass ")
	SupervisionClass=cur.fetchall()
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