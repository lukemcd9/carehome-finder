from app import db
from uuid import uuid4
from enum import Enum

class Operator(db.Model):
    class Certification(Enum):
        RN = 'RN'
        LPN = 'LPN'
        CNA = 'CNA'
    __tablename__ = 'operator'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    certification = db.Column(db.Enum(Certification))
    license_expiration = db.Column(db.DateTime())
    address = db.relationship('Address', uselist=False, backref='operator')
    carehomes = db.relationship('CareHome', backref='operator')

class CareHome(db.Model):
    class PatientGender(Enum):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
        BOTH = 'BOTH'

    class Type(Enum):
        ARCH = 'ARCH'
        ARCH_EXPANDED = 'ARCH EXPANDED'
        FOSTER = 'FOSTER'

    __tablename__ = 'carehome'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    patient_gender = db.Column(db.Enum(PatientGender))
    patient_max_age = db.Column(db.Integer())
    type = db.Column(db.Enum(Type))
    max_rooms = db.Column(db.Integer())
    open_rooms = db.Column(db.Integer())
    private_patients = db.Column(db.Boolean())
    medicaid_patients = db.Column(db.Boolean())
    ssi_patients = db.Column(db.Boolean())
    assistive_walking_devices = db.Column(db.String(25))
    behavioral_issues_patient = db.Column(db.Boolean())
    dialysis_patient = db.Column(db.Boolean())
    hospice_patient = db.Column(db.Boolean())
    insulin_patient = db.Column(db.Boolean())
    tube_feed_patient = db.Column(db.Boolean())
    wounded_patient = db.Column(db.Boolean())
    max_weight_patient = db.Column(db.Integer())
    case_management_company = db.Column(db.String(100))
    previous_experience = db.Column(db.Text())
    subs = db.Column(db.Integer())
    open_year = db.Column(db.Integer())
    operator_id = db.Column(db.Integer(), db.ForeignKey('operator.id'))
    rooms = db.relationship('Room', backref='carehome')

class Room(db.Model):
    class Type(Enum):
        PRIVATE = 'PRIVATE'
        SHARED = 'SHARED'
    __tablename__ = 'room'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    min_price = db.Column(db.Integer())
    max_price = db.Column(db.Integer())
    amount = db.Column(db.Integer())
    type = db.Column(db.Enum(Type))
    carehome_id = db.Column(db.Integer(), db.ForeignKey('carehome.id'))

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    street = db.Column(db.String(100))
    city = db.Column(db.String(25))
    state = db.Column(db.String(2)) 
    zip = db.Column(db.Integer())
    email = db.Column(db.String(255))
    operator_id = db.Column(db.Integer(), db.ForeignKey('operator.id'))
