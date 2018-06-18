from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Operator, Address, CareHome, Room
from forms import CareHomeForm
import os


@app.route('/')
def care_homes():
    carehomes = CareHome.query.all()
    return render_template('carehomes.html', carehomes=carehomes)

@app.route('/carehome/<id>')
def care_home(id):
    carehome = CareHome.query.filter_by(id=id).first()
    return render_template('carehome.html', carehome=carehome)

@app.route('/carehome/<id>/delete')
def delete_care_home(id):
    carehome = CareHome.query.filter_by(id=id).first()
    db.session.delete(carehome)
    db.session.commit()
    flash('Care Home deleted', 'success')
    return redirect(url_for('care_homes'))

@app.route('/carehome/<id>/edit', methods=['GET', 'POST'])
def edit_care_home(id):
    carehome = CareHome.query.filter_by(id=id).first()
    operator = carehome.operator
    private_room = Room.query.filter_by(carehome_id=id, type=Room.Type.PRIVATE).first()
    shared_room = Room.query.filter_by(carehome_id=id, type=Room.Type.SHARED).first()
    form = CareHomeForm(request.form)
    if request.method == 'GET':
        form.operator_name.data = operator.name
        form.carehome_name.data = carehome.name
        form.carehome_open_year.data = carehome.open_year
        form.type.data = carehome.type.value
        form.case_management_company.data = carehome.case_management_company
        form.address_city.data = operator.address.city
        form.address_street.data = operator.address.street
        form.address_state.data = operator.address.state
        form.address_zip.data = operator.address.zip
        form.certification.data = operator.certification.value
        form.email.data = operator.address.email
        form.license_expiration.data = carehome.operator.license_expiration
        form.max_price_private.data = private_room.max_price
        form.min_price_private.data = private_room.min_price
        form.max_price_shared.data = shared_room.max_price
        form.min_price_shared.data = shared_room.min_price
        form.open_rooms.data = carehome.open_rooms
        form.patient_age.data = carehome.patient_max_age
        form.patient_behavioral.data = carehome.behavioral_issues_patient
        form.patient_dialysis.data = carehome.dialysis_patient
        form.patient_gender.data = carehome.patient_gender.value
        form.patient_hospice.data = carehome.hospice_patient
        form.patient_insulin.data = carehome.insulin_patient
        form.patient_medicaid.data = carehome.medicaid_patients
        form.patient_private.data = carehome.private_patients
        form.patient_ssi.data = carehome.ssi_patients
        form.patient_tube_feed.data = carehome.tube_feed_patient
        form.patient_weight.data = carehome.max_weight_patient
        form.patient_wounds.data = carehome.wounded_patient
        form.phone.data = operator.phone
        form.subs.data = carehome.subs
        form.shared_rooms.data = shared_room.amount
        form.private_rooms.data = private_room.amount
        form.patient_walking_device.data = str(carehome.assistive_walking_devices).replace('[', '').replace(']', '').replace('\'', '').split(', ')
        return render_template('editcarehome.html', form=form, id=id)
    
    if request.method == 'POST':
        operator.name = form.operator_name.data
        carehome.name = form.carehome_name.data
        carehome.open_year = form.carehome_open_year.data
        carehome.case_management_company = form.case_management_company.data
        operator.address.city = form.address_city.data
        operator.address.street = form.address_street.data
        operator.address.state = form.address_state.data
        operator.address.zip = form.address_zip.data
        operator.certification = form.certification.data
        operator.address.email = form.email.data
        carehome.operator.license_expiration = form.license_expiration.data
        private_room.max_price = form.max_price_private.data
        private_room.min_price = form.min_price_private.data
        shared_room.max_price = form.max_price_shared.data
        shared_room.min_price = form.min_price_shared.data
        carehome.open_rooms = form.open_rooms.data
        carehome.patient_max_age = form.patient_age.data
        carehome.behavioral_issues_patient = form.patient_behavioral.data
        carehome.dialysis_patient = form.patient_dialysis.data
        carehome.patient_gender = form.patient_gender.data 
        carehome.hospice_patient = form.patient_hospice.data
        carehome.insulin_patient = form.patient_insulin.data
        carehome.medicaid_patients = form.patient_medicaid.data
        carehome.private_patients = form.patient_private.data
        carehome.ssi_patients = form.patient_ssi.data
        carehome.tube_feed_patient = form.patient_tube_feed.data
        carehome.max_weight_patient = form.patient_weight.data
        carehome.wounded_patient = form.patient_wounds.data
        carehome.type = form.type.data
        operator.phone = form.phone.data
        carehome.subs = form.subs.data
        shared_room.amount = form.shared_rooms.data
        private_room.amount = form.private_rooms.data
        carehome.assistive_walking_devices = str(form.patient_walking_device.data).replace('[', '').replace(']', '').replace('\'', '')
        db.session.commit()
        flash('Care Home updated', 'success')
        return redirect(url_for('care_homes'))


@app.route('/carehome/add', methods=['GET', 'POST'])
def add_care_home():
    form = CareHomeForm(request.form)

    if request.method == 'POST':
        operator = Operator (
            name=form.operator_name.data, 
            phone=form.phone.data, 
            certification=form.certification.data,
            license_expiration=form.license_expiration.data
        )
        address = Address (
            street=form.address_street.data, 
            city=form.address_city.data, 
            state=form.address_state.data, 
            zip=form.address_zip.data,
            email=form.email.data, 
            operator=operator
        )
        carehome = CareHome (
            name=form.carehome_name.data, 
            type=form.type.data,
            open_rooms=form.open_rooms.data,
            max_rooms=form.private_rooms.data + form.shared_rooms.data, 
            patient_gender=form.patient_gender.data,
            patient_max_age=form.patient_age.data,
            private_patients=form.patient_private.data,
            medicaid_patients=form.patient_medicaid.data,
            ssi_patients=form.patient_ssi.data,
            assistive_walking_devices=str(form.patient_walking_device.data).replace('[', '').replace(']', '').replace('\'', ''),
            behavioral_issues_patient=form.patient_behavioral.data,
            dialysis_patient=form.patient_dialysis.data,
            hospice_patient=form.patient_hospice.data,
            insulin_patient=form.patient_insulin.data,
            tube_feed_patient=form.patient_tube_feed.data,
            wounded_patient=form.patient_wounds.data,
            max_weight_patient=form.patient_weight.data,
            case_management_company=form.case_management_company.data,
            previous_experience=form.previous_experience.data,
            subs=form.subs.data,
            open_year=form.carehome_open_year.data,
            operator=operator 
        )
        private_rooms = Room (
            min_price=form.min_price_private.data,
            max_price=form.max_price_private.data,
            amount=form.private_rooms.data,
            type=Room.Type.PRIVATE,
            carehome=carehome
        )
        shared_rooms = Room (
            min_price=form.min_price_shared.data,
            max_price=form.max_price_shared.data,
            amount=form.shared_rooms.data,
            type=Room.Type.SHARED,
            carehome=carehome
        )
        db.session.add(operator)
        db.session.add(address)
        db.session.add(carehome)
        db.session.add(private_rooms)
        db.session.add(shared_rooms)
        db.session.commit()
        flash('Care Home added', 'success')
        return redirect(url_for('care_homes'))
    return render_template('addcarehome.html', form=form)