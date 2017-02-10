from flask import *
import sqlite3 as sql
import flask_excel as excel
from wtforms import *
from wtforms.validators import DataRequired
from flask_wtf import *
from passlib.hash import sha256_crypt
from forms import LoginForm
from flask_login import LoginManager
from flask_openid import OpenID
import os
import random

app = Flask(__name__)
# @babel.timezoneselector
# def get_timezone():
#     user = getattr(g, 'user', None)
#     if user is not None:
#         return user.timezone


# @app.route('/login', methods=['GET', 'POST'])
# def lologin():
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 		flash('Login requested for OpenID="%s", remember_me=%s' %
# 			  (form.openid.data, str(form.remember_me.data)))
# 		return redirect('/index')
# 	return render_template('login.html',
# 						   title='Sign In',
# 						   form=form,
# 						   providers=OPENID_PROVIDERS)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

DATABASE = 'database.db'

#@app.route("/upload", methods=['GET', 'POST'])
#def upload_file():
 #   if request.method == 'POST':
  #      return jsonify({"result": request.get_array(field_name='file')})
   # return '''
   # <!doctype html>
    #<title>Upload an excel file</title>
   # <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    #<form action="" method=post enctype=multipart/form-data><p>
    #<input type=file name=file><input type=submit value=Upload>
    #</form>
    #'''

#@app.route("/download", methods=['GET'])
#def download_file():
 #   return excel.make_response_from_array([[1,2], [3, 4]], "csv")

#@app.route("/export", methods=['GET'])
#def export_records():
 #   return excel.make_response_from_array([[1,2], [3, 4]], "csv", file_name="export_data")

#('CREATE TRIGGER audit_log AFTER INSERT ON COMPANY')
#BEGIN
#("INSERT INTO AUDIT(EMP_ID, ENTRY_DATE) VALUES (new.ID, datetime('now'))")
#END
@app.route("/profile/<ID>")
def Profile(ID):
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("select * from Person where ID = ?", (ID,))
	rows = cur.fetchall()
	return render_template("listcompanyforempl.html", rows=rows, ID=ID)

@app.route('/Dropemall')
def droppemall():
	con = sql.connect("database.db")
	c = con.cursor()
	c.execute("DROP TABLES")
	con.commit()
	return "dropped"

@app.route('/resettables')
def bringdtatonline():
	con = sql.connect("database.db")
	c = con.cursor()
	# c.execute('drop table if exists table1')
	# c.execute('drop table if exists table2')
	# c.execute('drop table if exists table3')
	# c.execute('drop table if exists company')
	# c.execute('drop table if exists users')
	# c.execute('drop table if exists holder')
	# c.execute('CREATE TABLE holder (hold varchar (350000), hold1 varchar (10000))')
	# c.execute(
	# 	'CREATE TABLE table3(CID forigen key,opp double, aadd double, sub double, mtp double , dvd double, rslt double)')
	# c.execute('CREATE TABLE table1(name INTERGER PRIMARY KEY ASC, addr, city, pin)')
	# c.execute(
	# 	'CREATE TABLE users(CID INT, UID INTERGER PRIMARY KEY NOT NULL,username varchar(25),password varchar(50), settings varchar(32500), tracking varchar (325000), rank int(3) )')
	# c.execute('CREATE TABLE table2(name INTERGER PRIMARY KEY ASC, addr, city, pin)')
	# c.execute(
	# 	'CREATE TABLE company (CID INTEGER PRIMARY KEY AUTOINCREMENT,UID INT NOT NULL, NAME TEXT NOT NULL, AGE INT NOT NULL,ADDRESS CHAR(50), SALARY DOUBLE(100,2), Hiredate datetime NOT NULL DEFAULT GETDATE())')
	# c.execute('INSERT INTO COMPANY (UID,NAME,AGE,ADDRESS,SALARY)VALUES (1, "Paul", 32, "California", 20000.00,)')
	# c.execute('INSERT INTO COMPANY (UID,NAME,AGE,ADDRESS,SALARY)VALUES (2, "Allen", 25, "Texas", 15000.00 )')
	# c.execute('INSERT INTO COMPANY (UID,NAME,AGE,ADDRESS,SALARY)VALUES (3, "Teddy", 23, "Norway", 20000.00 )')
	# c.execute('INSERT INTO COMPANY (UID,NAME,AGE,ADDRESS,SALARY)VALUES (4, "Mark", 25, "Rich Mond" , 65000.00 )')
	# c.execute('INSERT INTO COMPANY (UID,NAME,AGE,ADDRESS,SALARY)VALUES (5, "David", 27, "Texas", 85000.00 )')
	# c.execute('INSERT INTO COMPANY (UID,NAME,AGE,ADDRESS,SALARY)VALUES (6, "Kim", 22, "South Hall", 45000.00 )')
	# c.execute("Insert into table3 (CID, opp, rslt) select CID, salary, salary from company")
	# c.execute('UPDATE table3 set aadd=0, sub=0, mtp=0, dvd=0')
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
	c.execute('CREATE TABLE CourseGeneration(COURSEGEN int NOT NULL, CRN int, PRIMARY KEY (COURSEGEN),FOREIGN KEY (CRN) REFERENCES Course (CRN))')
	c.execute('CREATE TABLE Course(CRN int, Subj text, Crse text, Sec text, Session text, Title text, PRIMARY KEY (CRN))')
	c.execute('CREATE TABLE Offering(OID int NOT NULL, Semester text, ID int, COURSEGEN int, PRIMARY KEY (OID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (COURSEGEN) REFERENCES CourseGeneration (COURSEGEN))')
	c.execute('CREATE TABLE Person(ID int NOT NULL, Email text NOT NULL, Name text NOT NULL, PRIMARY KEY (ID))')
	c.execute('CREATE TABLE Term(Semester text NOT NULL, PRIMARY KEY (Semester))')
	#ADD THE AUTOIMCREMENT STATMENT BACK TO ADJ ID, AUDIT ID, AND THE DATE
	c.execute('CREATE TABLE ProjectSupervision(ProjectSupervisionID int NOT NULL, ID int, ProjectClassID int, PRIMARY KEY(ProjectSupervisionID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (ProjectClassID) REFERENCES ProjectClass (ProjectClassID))')
	c.execute('CREATE TABLE SupervisionClass(SupervisionClassID int NOT NULL, Graduate int, Undergrad int, Masters int, PRIMARY KEY (SupervisionClassID))')
	c.execute('CREATE TABLE PseudoPeople(PseudoID int NOT NULL, PseudoName text NOT NULL, Email text, Team text, PRIMARY KEY (PseudoID))')
	c.execute('CREATE TABLE ProjectClass(ProjectClassID int NOT NULL, Graduate int, Undergrad int, Masters int, PRIMARY KEY (ProjectClassID))')
	c.execute('CREATE TABLE Adjustment(AdjustmentID int NOT NULL, ADJTO int NOT NULL, ID int, ADJWeight float, AUDITID int, AUDITDATE date, AUDITCOMMENT text NOT NULL, PRIMARY KEY (AdjustmentID), FOREIGN KEY (ID) REFERENCES Person (ID))')
	c.execute('CREATE TABLE Supervision(SupervisionID int NOT NULL, ID int, SupervisionClassID int, PRIMARY KEY (SupervisionID), FOREIGN KEY (ID) REFERENCES Person (ID), FOREIGN KEY (SupervisionClassID) REFERENCES SupervisionClass (SupervisionClassID))')
	con.commit()
	ID=random.randrange(0,100)
	print (ID)
	return render_template('reset.html')

@app.route('/populate', methods=["GET","POST"])
def populate():
	count=0
	while(True):
		count += 1
		WORDS = open('/etc/dictionaries-common/words').readlines()
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
		con=sql.connect("database.db")
		c=con.cursor()
	# if request.method == "POST":
	# 	ID = request.form['ID']
		ID=random.randrange(0,1000000000000)
	# Email=random.randrange(101,200)
	# Name=random.randrange(201,300)
		CRN=random.randrange(00000,99999)
		# name = request.form['name']
		# age = request.form['age']
		# city = request.form['city']
		# salary = request.form['salary']
		if count == 31:
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
		# 	c.execute('insert into CourseGeneration (COURSEGEN) Values (?)',(COURSEGEN))
		# 	con.commit()
		# c.execute("Insert into table3 (opp) select salary from company WHERE CID = (SELECT MAX(CID)  FROM company);")
	# con.commit()
		# return redirect("/populate")
	# else:
		# return render_template("populate.html")
	return render_template('populate.html')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db
#
# def make_dicts(cursor, row):
#     return dict((cursor.description[idx][0], value)
#                 for idx, value in enumerate(row))
#
# # login_manager = LoginManager()
# # login_manager.init_app(app)
# # login_manager.login_view = "login"
# #
# # @login_manager.user_loader
# # def load_user(user_id):
# #     return User.get(user_id)
#
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     # Here we use a class of some kind to represent and validate our
# #     # client-side form data. For example, WTForms is a library that will
# #     # handle this for us, and we use a custom LoginForm to validate.
# #     form = LoginForm()
# #     if form.validate_on_submit():
# #         # Login and validate the user.
# #         # user should be an instance of your `User` class
# #         login_user(user)
# #
# #         flask.flash('Logged in successfully.')
# #
# #         next = flask.request.args.get('next')
# #         # is_safe_url should check if the url is safe for redirects.
# #         # See http://flask.pocoo.org/snippets/62/ for an example.
# #         if not is_safe_url(next):
# #             return flask.abort(400)
# #
# #         return flask.redirect(next or flask.url_for('index'))
# #     return flask.render_template('login.html', form=form)
# #
# # @app.route('/enternew2')
# # def new_student2():
# # 	return render_template('student2.html')
# #
# # @app.route('/enternew')
# # def new_student():
# # 	return render_template('student.html')
# #
# # @app.route('/addrec', methods=['POST', 'GET'])
# # def addrec():
# # 	if request.method == 'POST':
# # 		#try:
# # 			nm = request.form['nm']
# # 			addr = request.form['add']
# # 			city = request.form['city']
# # 			pin = request.form['pin']
# #
# # 			with sql.connect("database.db") as con:
# # 				cur = con.cursor()
# #
# # 				cur.execute("INSERT INTO table1 (name,addr,city,pin) VALUES(?, ?, ?, ?)" , (nm,addr,city,pin))
# # 				con.commit()
# # 				msg = "Record successfully added"
# # 		#except:
# # 		#	con.rollback()
# # 		#	msg = "error in insert operation"
# #
# # 		#finally:
# # 		#	con.close()
# # 			return render_template("result.html", msg=msg)
# # 	else:
# # 		return 'fail'
# #
# # @app.route('/addrec2', methods=['POST', 'GET'])
# # def addrec2():
# # 	if request.method == 'POST':
# # 		#try:
# # 			nm = request.form['nm']
# # 			addr = request.form['add']
# # 			city = request.form['city']
# # 			pin = request.form['pin']
# #
# # 			with sql.connect("database.db") as con:
# # 				cur = con.cursor()
# #
# # 				cur.execute("INSERT INTO table2 (name,addr,city,pin) VALUES(?, ?, ?, ?)" , (nm,addr,city,pin))
# # 				con.commit()
# # 				msg = "Record successfully added"
# # 		#except:
# # 		#	con.rollback()
# # 		#	msg = "error in insert operation"
# #
# # 		#finally:
# # 		#	con.close()
# # 			return render_template("result.html", msg=msg)
# # 	else:
# # 		return 'fail'
# #
# # @app.route('/addingtables', methods=['GET' , 'POST'])
# # def addingtables():
# # 	error=None
# # 	con = sql.connect("database.db")
# # 	con.row_factory = sql.Row
# # 	c = con.cursor()
# # 	c.execute("select * from company")
# # 	rowc = c.fetchall()
# # 	c.execute("select * from table3")
# # 	rows = c.fetchall()
# # 	if request.method == 'POST':
# # 		CID= request.form['CID']
# # 		#opp= request.form['opp']
# # 		aadd= request.form['aadd']
# # 		sub = request.form['sub']
# # 		mtp = request.form['mtp']
# # 		dvd = request.form['dvd']
# # 		#rslt = request.form['rslt']
# # 		if not "to" in request.form:
# # 			if not CID=="":
# # 				if not aadd=="":
# # 					c.execute("UPDATE table3 SET rslt = rslt + ?, aadd = aadd + ? WHERE CID = ? ", (aadd,aadd, CID))
# # 					con.commit()
# # 				elif not sub=="":
# # 					c.execute("UPDATE table3 SET rslt = rslt - ?, sub = sub + ? WHERE CID = ? ", (sub,sub, CID))
# # 					con.commit()
# # 				elif not mtp=="":
# # 					c.execute("UPDATE table3 SET rslt = rslt * ?, mtp = mtp + ? WHERE CID = ? ", (mtp,mtp, CID))
# # 					con.commit()
# # 				elif not dvd=="":
# # 					c.execute("UPDATE table3 SET dvd = dvd + ?, rslt = rslt / ?  WHERE CID = ? ", (dvd, dvd, CID))
# # 					con.commit()
# # 				else:
# # 					error ="incorrect feild usage"
# # 					return render_template("list3.html", rows=rows, rowc=rowc, error=error )
# # 			else:
# # 				error = 'Invalid use of NOT NULL FEILDS'
# # 				return render_template("list3.html", rows=rows, rowc=rowc, error=error)
# # 		#else:
# # 			#c.execute("insert into company (UID, salary) select rslt from table3 ")
# # 	return render_template("list3.html", rowc=rowc, rows=rows, error=error)
# #
# # @app.route('/list')
# # def list():
# # 	con = sql.connect("database.db")
# # 	con.row_factory = sql.Row
# #
# # 	cur = con.cursor()
# # 	cur.execute("select * from table1 ")
# #
# # 	rows = cur.fetchall()
# # 	return render_template("list.html", rows=rows)

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

	# if request.method == "POST":
	# 	# ID = request.form['ID']
	# 	# add = request.form['add']
	# 	# sub = request.form['sub']
	# 	# mtp= request.form['multiply']
	# 	# dvd=request.form['divide']
	# 	con = sql.connect("database.db")
	# 	cur = con.cursor()
	# 	if not ID=="":
	# 		if not add=="":
	# 			cur.execute("UPDATE COMPANY SET SALARY = SALARY + ? WHERE UID = ? ", (add, ID))
	# 			con.commit()
	# 		elif not sub=="":
	# 			cur.execute("UPDATE COMPANY SET SALARY = SALARY - ? WHERE UID = ? ", (sub, ID))
	# 			con.commit()
	# 		elif not mtp=="":
	# 			cur.execute("UPDATE COMPANY SET SALARY = SALARY * ? WHERE UID = ? ", (mtp, ID))
	# 			con.commit()
	# 		elif not dvd=="":
	# 			cur.execute("UPDATE COMPANY SET SALARY = SALARY / ? WHERE UID = ? ", (dvd, ID))
	# 			con.commit()
	# 		else:
	# 			error ="incorrect feild usage"
	# 			return render_template("listcompany.html", rows=rows, error=error )
	# 	else:
	# 		error = 'Invalid use of NOT NULL FEILDS'
	# 	return render_template("listcompany.html", rows=rows, error=error)
	# else:
	return render_template("listcompany.html", Person=Person, Pseudo=Pseudo, Course=Course)

#
# def list2():
# 	con = sql.connect("database.db")
# 	con.row_factory = sql.Row
#
# 	cur = con.cursor()
# 	cur.execute("select * from table2")
#
# 	rows = cur.fetchall()
# 	return render_template("list.html", rows=rows)

@app.route('/Dashboard')
@app.route('/index')
@app.route('/',methods=["GET"])
def index():
    return render_template("Home.html")

#class RegistrationForm(Form):
#	username = TextFeild('username',[validators.Length(min=1, max=25)])
#	password = PasswordFeild('Password', [validators.Required(), validators.EqualTo('confirm', message='passwords must match')])
#	confirm = PasswordFeild('Repeat password')
#	accept = BooleanFeild ('click me'),[validators.Required()]
#
# @app.route('/lo', methods=['GET', 'POST'])
# def lo():
# 	error = None
# 	if request.method == 'POST':
# 		if request.form['username'] != 'admin' or \
# 						request.form['password'] != 'admin':
# 			error = 'Invalid username or password. Please try again!'
# 		else:
# 			flash('You were successfully logged in')
# 			return redirect(url_for('index'))
# 	return render_template('lo.html', error=error)
#
# @app.route('/reg', methods=["GET","POST"])
# def register_page():
# 	con = sql.connect("database.db")
# 	c = con.cursor()
# 	form=RegistrationForm(request.form)
# 	if request.method=="POST" and form.Validate():
# 		username= form.username.data
# 		password = sha256_crypt.encrypt((str(form.password.data)))
# 		x=c.execute("select * from users where username = (%s)")
# 		if int(len(x)>0):
# 			flash(taken)
# 			return render_template('register.html', form=form)
# 		else:
# 			c.execute("insert into users (username, password, tracking) Values (?, ?, ?, ?")
# 			con.commit()
# 			session['Logged in']=True
# 			session['username']= username
# 			return ("alive jim alive")
# 	return ("dead jim dead")
#
# #@app.route("/login", methods=["GET", "POST"])
# #def login():
# #	error=''
# #	c, con = sql.connect("database.db")
# 	#if request.method == 'POST':
# 	#	data=c.execute("select * from users where ID = (%s)", thwart(request.form['ID']))
# 	#	data=c.fetchone()[2]
# 			#if
# 		#		session['logged in'] = True
# 			#	session['ID']= request.form['ID']

@app.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p><a href="/">home</a>')

# somewhere to logout
#@app.route("/logout")
#@login_required
#def logout():
#	logout_user()
#3	return Response('<p>Logged out</p> <a href="/">home</a>')

#@app.route("/protected/",methods=["GET"])
#@login_required
#def protected():
   # return Response(response="Hello Protected World!", status=200)

if __name__ == '__main__':
    app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000,debug=True)