from flask_wtf import FlaskForm
from wtforms import widgets, TextAreaField, StringField, IntegerField, SelectField, SelectMultipleField, BooleanField, PasswordField
from wtforms.fields.html5 import EmailField, DateField, TelField
from wtforms.fields import RadioField
from wtforms.validators import DataRequired
import datetime

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CareHomeForm(FlaskForm):
    operator_name = StringField('Operator Name', validators=[DataRequired()])
    carehome_name = StringField('Care Home Name', validators=[DataRequired()])
    address_street = StringField('Address', validators=[DataRequired()])
    address_city = StringField('City', validators=[DataRequired()])
    address_region = StringField('Region', validators=[DataRequired()])
    address_zip = IntegerField('Zip', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = TelField('Phone', validators=[DataRequired()])
    certification = SelectField('Certification', choices=[('RN', 'RN'), ('LPN', 'LPN'), ('CNA', 'CNA')], validators=[DataRequired()])
    license_expiration = DateField('License Expiration Date', default=datetime.datetime.now(), validators=[DataRequired()])
    case_management_company = StringField('Case Management Company', validators=[DataRequired()])
    subs = IntegerField('How many subs do you have?', default=0, validators=[DataRequired()])
    # previous_experience = TextAreaField('What is your previous experience prior to opening care home?')
    carehome_open_year = IntegerField('What year did you open your care home?', default=datetime.datetime.now().year, validators=[DataRequired()])
    type = SelectField('Type', choices=[('ARCH', 'ARCH'), ('EXPANDED', 'EXPANDED'), ('FOSTER', 'FOSTER')], validators=[DataRequired()])
    private_rooms = IntegerField('Amount of Private Rooms', validators=[DataRequired()])
    shared_rooms = IntegerField('Amount of Shared Rooms', validators=[DataRequired()])
    min_price_private = IntegerField('Min Price of Private Rooms', validators=[DataRequired()])
    max_price_private = IntegerField('Max Price of Private Rooms', validators=[DataRequired()])
    min_price_shared = IntegerField('Min Price of Shared Rooms', validators=[DataRequired()])
    max_price_shared = IntegerField('Max Price of Shared Rooms', validators=[DataRequired()])
    patient_gender = SelectField('I accept patients who are', choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('BOTH', 'Both')], validators=[DataRequired()])
    patient_age = IntegerField('Age of patients that you would prefer to work with', validators=[DataRequired()])
    patient_private = BooleanField('I only accept patients who private pay', validators=[DataRequired()])
    patient_medicaid = BooleanField('I accept patients who are medicaid', validators=[DataRequired()])
    patient_ssi = BooleanField('I accept patients who pay through supplemental social security income (SSI)', validators=[DataRequired()])
    patient_walking_device = MultiCheckboxField('I accept patients who are ambulatory with following assistive walking devices', choices=[('CANE', 'Cane'), ('WALKER', 'Walker'), ('WHEELCHAIR', 'Wheelchair')])
    patient_behavioral = BooleanField('I will accept patients with behavioral issues', validators=[DataRequired()])
    patient_dialysis = BooleanField('I will accept patients who are on dialysis', validators=[DataRequired()])
    patient_hospice = BooleanField('I will accept patients who are hospice status', validators=[DataRequired()])
    patient_insulin = BooleanField('I will accept patients who have insulin', validators=[DataRequired()])
    patient_tube_feed = BooleanField('I will accept tube feeding patients', validators=[DataRequired()])
    patient_wounds = BooleanField('I accept patients with wounds', validators=[DataRequired()])
    patient_weight = IntegerField('What is the max weight of patient you are able to work with?', validators=[DataRequired()])
    open_rooms = IntegerField('Open Rooms', validators=[DataRequired()])
    notes = TextAreaField('Notes')

class EditNotes(FlaskForm):
    notes = TextAreaField('Edit Notes')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])