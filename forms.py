# Copyright 2017 Jonathan Anderson
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

from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.widgets import HiddenInput
from wtforms.validators import Required, Email


class UpdateCourseGeneration(FlaskForm):
    id = IntegerField(widget = HiddenInput())
    lab_hours = FloatField()
    credit_hours = FloatField()
    lecture_hours = FloatField()
    title = TextField()
    description = TextAreaField()
    other_info = TextField()
    start_year = IntegerField()
    end_year = IntegerField()

    submit = SubmitField(u'Update')


class UpdatePerson(FlaskForm):
    id = IntegerField(widget = HiddenInput())
    name = TextField(u'Name', validators = [ Required() ])
    email = TextField(u'Email address', validators = [ Email() ])
    validated = BooleanField(u'This information has been human-validated')

    submit = SubmitField(u'Update')
