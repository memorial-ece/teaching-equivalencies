from flask import *
import os
from Populate import *

app = Flask(__name__)
random.seed(a=2)
DATABASE = 'database.db'
database = SqliteDatabase(DATABASE)

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
								'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/profile/<ID>")
def Profile(ID):
	person = Person.get(Person.ID == ID)
	supervising=Supervision.get(Supervision.ID == ID)
	offer=Offering.get(Offering.ID == ID)
	Psuper=ProjectSupervision.get(ProjectSupervision.ID == ID)

	return render_template("listcompanyforempl.html", person=person, supervising=supervising,offer=offer,Psuper=Psuper)

@app.route('/populate', methods=["GET", "POST"])
def populate():
	Gen2()
	return render_template('populate.html')


@app.route('/listm', methods=['GET', 'POST'])
def listm():
	return render_template("listcompany.html", Person=Person, Pseudo=PseudoPeople, Course=Course,
							SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
							ProjectSupervision=ProjectSupervision, Supervision=Supervision, Adjustment=Adjustment,
							RolePerson=RolePerson, Role=Role, Term=Term, Offering=Offering,
							CourseGeneration=CourseGeneration)


@app.route('/Dashboard')
@app.route('/index')
@app.route('/', methods=["GET"])
def index():
	return render_template("Home.html")

@app.route('/peewee')
def create_tables():
	database.connect()
	database.drop_tables(
		[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
		 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment,])
	database.create_tables(
		[Person, Course, CourseGeneration, Term, Offering, Role, RolePerson, ProjectSupervision, ProjectClass,
		 Supervision, SupervisionClass, PseudoPeople, Student, Adjustment])
	return render_template('reset.html')


if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)
