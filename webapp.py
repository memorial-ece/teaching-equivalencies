# Copyright 2017 Jonathan Anderson
# Copyright 2017 Keegan Joseph Brophy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import config
import db
import forms
import flask
import flask_bootstrap
import flask_dotenv
import nav

database = db.get()
frontend = flask.Blueprint('frontend', __name__)

@frontend.before_request
def _db_connect(): database.connect()

@frontend.teardown_request
def _db_close(exc):
    if not database.is_closed(): database.close()


@frontend.route('/')
def index():
    return flask.render_template('index.html',
        courses = db.Course.select().order_by(
            db.Course.subject, db.Course.code),

        people = db.Person.current_instructors(),
    )


@frontend.route('/course/<int:id>', methods = [ 'GET', 'POST' ])
def course(id):
    course = db.Course.get(id = id)

    f = forms.CourseGenerationUpdate()
    if f.validate_on_submit():
        g = db.CourseGeneration.get(id = f.id.data)
        g.lab_hours = f.lab_hours.data
        g.credit_hours = f.credit_hours.data
        g.lecture_hours = f.lecture_hours.data
        g.title = f.title.data
        g.description = f.description.data
        g.other_info = f.other_info.data
        g.start_year = f.start_year.data
        g.end_year = f.end_year.data
        g.save()

    generations = (
        course.generations.order_by(db.CourseGeneration.end_year.desc())
    )

    return flask.render_template('course.html',
        course = course,
        generations = generations,
    )


@frontend.route('/course/generation/<int:id>', methods = [ 'GET', 'POST' ])
def course_generation(id):
    g = db.CourseGeneration.get(id = id)
    f = forms.CourseGenerationUpdate(obj = g)

    if f.validate_on_submit():
        g.lab_hours = f.lab_hours.data
        g.credit_hours = f.credit_hours.data
        g.lecture_hours = f.lecture_hours.data
        g.title = f.title.data
        g.description = f.description.data
        g.other_info = f.other_info.data
        g.start_year = f.start_year.data
        g.end_year = f.end_year.data
        g.save()

    return flask.render_template('course-generation.html', form = f, gen = g)


@frontend.route('/course/offering/<int:id>', methods = [ 'GET', 'POST' ])
def course_offering(id):
    o = db.Offering.get(id = id)
    f = forms.CourseOfferingUpdate(obj = o)

    if f.validate_on_submit():
        o.enrolment = f.enrolment.data
        o.lab_sections = f.lab_sections.data
        o.save()

    return flask.render_template('course-offering.html', form = f, offering = o)


@frontend.route('/courses')
def courses():
    courses = db.Course.select().order_by(db.Course.subject, db.Course.code)
    return flask.render_template('courses.html', courses = courses)


@frontend.route('/people', methods = [ 'GET', 'POST' ])
def people():
    f = forms.PersonUpdate()
    if f.validate_on_submit():
        p = db.Person.get(id = f.id.data)
        p.name = f.name.data
        p.email = f.email.data
        p.validated = f.validated.data
        p.save()

    people = (
        db.Person.select()
            .order_by(db.Person.name)
            .order_by(db.Person.validated.desc())
    )
    person_forms = [ forms.PersonUpdate(None, obj = p) for p in people ]

    return flask.render_template('people.html', db = db, people = person_forms)


@frontend.route('/person/<int:id>', methods = [ 'GET', 'POST' ])
def person(id):
    p = db.Person.get(id = id)

    f = forms.PersonUpdate()
    if f.validate_on_submit():
        p.name = f.name.data
        p.email = f.email.data
        p.validated = f.validated.data
        p.save()

    return flask.render_template('person.html', db = db, person = p, sum = sum)


@frontend.route('/teaching-load/<int:id>', methods = [ 'GET', 'POST' ])
def teaching_load(id):
    l = db.TeachingLoad.get(id = id)

    return flask.render_template('teaching-load.html', load = l)


@frontend.route('/teaching-load/add', methods = [ 'GET', 'POST' ])
def teaching_load_add():
    f = personal_load_create()
    print(f.data)
    if f.validate_on_submit():
        db.PersonalLoad.create(
            instructor = f.instructor.data,
            load = int(flask.request.form['load']),
            start = f.start.data,
            end = f.end.data if f.end.data != -1 else None)
    else:
        flask.flash('Invalid form input: %s' % f.data, category = 'error')

    return flask.redirect(flask.url_for('.teaching_loads'))


@frontend.route('/teaching-load/create', methods = [ 'GET', 'POST' ])
def teaching_load_create():
    f = forms.TeachingLoadCreate()
    if f.validate_on_submit():
        l = db.TeachingLoad.create(name = f.name.data, load = f.load.data)
    else:
        flask.flash('Invalid form input: %s' % f.data, category = 'error')

    return flask.redirect(flask.url_for('.teaching_loads'))


@frontend.route('/teaching-loads')
def teaching_loads():
    add_load = personal_load_create()

    return flask.render_template('teaching-loads.html',
        add_load = add_load, db = db,
        loads = db.TeachingLoad.select(), new = forms.TeachingLoadCreate())

def personal_load_create():
    form = forms.PersonalLoadCreate()
    form.instructor.choices = [
        (p.id, p.name) for p in db.Person.select().where(db.Person.validated)
    ]
    form.start.choices = form.end.choices = [ (-1, '') ] + [
        (s.id, str(s))
            for s in db.Semester.select().order_by(db.Semester.year.desc())
    ]
    return form


nav.nav.register_element('frontend_top',
    nav.Navbar(
        nav.View('teq', '.index'),
        nav.View('Courses', '.courses'),
        nav.View('Loads', '.teaching_loads'),
        nav.View('People', '.people'),
    )
)


def create_app():
    # See http://flask.pocoo.org/docs/patterns/appfactories
    app = flask.Flask(__name__)
    nav.nav.init_app(app)
    flask_dotenv.DotEnv().init_app(app, verbose_mode = True)

    flask_bootstrap.Bootstrap(app)
    app.register_blueprint(frontend)

    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    return app
