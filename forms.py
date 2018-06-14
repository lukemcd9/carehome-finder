from flask_wtf import FlaskForm
from wtforms import widgets, TextAreaField, StringField, IntegerField, SelectField, SelectMultipleField, BooleanField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.fields import RadioField
import datetime

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CareHomeForm(FlaskForm):
    operator_name = StringField('Operator Name')
    carehome_name = StringField('Care Home Name')
    address_street = StringField('Address')
    address_city = StringField('City')
    address_state = StringField('State')
    address_zip = IntegerField('Zip')
    email = EmailField('Email')
    phone = StringField('Phone')
    certification = SelectField('Certification', choices=[('RN', 'RN'), ('LPN', 'LPN'), ('CNA', 'CNA')])
    license_expiration = DateField('License Expiration Date')
    case_management_company = StringField('Case Management Company')
    subs = IntegerField('How many subs do you have?')
    previous_experience = TextAreaField('What is your previous experience prior to opening care home?')
    carehome_open_year = SelectField('What year did you open your care home', choices=[(x, x) for x in range(1980, datetime.datetime.now().year + 1)])
    type = SelectField('Type', choices=[('ARCH', 'ARCH'), ('ARCH_EXPANDED', 'EXPANDED'), ('FOSTER', 'FOSTER')])
    private_rooms = IntegerField('Amount of Private Rooms')
    shared_rooms = IntegerField('Amount of Shared Rooms')
    min_price_private = IntegerField('Min Price of Private Rooms')
    max_price_private = IntegerField('Max Price of Private Rooms')
    min_price_shared = IntegerField('Min Price of Shared Rooms')
    max_price_shared = IntegerField('Max Price of Shared Rooms')
    patient_gender = SelectField('I accept patients who are', choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('BOTH', 'Both')])
    patient_age = IntegerField('Age of patients that you would prefer to work with')
    patient_private = BooleanField('I only accept patients who private pay')
    patient_medicaid = BooleanField('I accept patients who are medicaid')
    patient_ssi = BooleanField('I accept patients who pay through supplemental social security income (SSI)')
    patient_walking_device = MultiCheckboxField('I accept patients who are ambulatory with following assistive walking devices', choices=[('CANE', 'Cane'), ('WALKER', 'Walker'), ('WHEELCHAIR', 'Wheelchair')], default=[])
    patient_behavioral = BooleanField('I will accept patients with behavioral issues')
    patient_dialysis = BooleanField('I will accept patients who are on dialysis')
    patient_hospice = BooleanField('I will accept patients who are hospice status')
    patient_insulin = BooleanField('I will accept patients who have insulin')
    patient_tube_feed = BooleanField('I will accept tube feeding patients')
    patient_wounds = BooleanField('I accept patients with wounds')
    patient_weight = IntegerField('What is the max weight of patient you are able to work with?')
    open_rooms = IntegerField('Open Rooms')