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
    return flask.render_template('index.html')


@frontend.route('/course/<int:id>', methods = [ 'GET', 'POST' ])
def course(id):
    course = db.Course.get(id = id)

    f = forms.UpdateCourseGeneration()
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

    generations = [
        forms.UpdateCourseGeneration(None, obj = g) for g in course.generations
    ]

    return flask.render_template('course.html',
        course = course,
        generations = generations,
    )


@frontend.route('/courses')
def courses():
    courses = db.Course.select().order_by(db.Course.subject, db.Course.code)
    return flask.render_template('courses.html', courses = courses)


@frontend.route('/people', methods = [ 'GET', 'POST' ])
def people():
    f = forms.UpdatePerson()
    if f.validate_on_submit():
        p = db.Person.get(id = f.id.data)
        p.name = f.name.data
        p.email = f.email.data
        p.validated = f.validated.data
        p.save()

    people = db.Person.select().order_by(db.Person.name)
    person_forms = [ forms.UpdatePerson(None, obj = p) for p in people ]

    return flask.render_template('people.html', people = person_forms)


nav.nav.register_element('frontend_top',
    nav.Navbar(
        nav.View('ECE::teq', '.index'),
        nav.View('Courses', '.courses'),
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
