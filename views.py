from flask import render_template, request, redirect, url_for, flash, abort
from app import app, db, photos
from models import Operator, Address, CareHome, Room, User
from forms import CareHomeForm, EditNotes, LoginForm
import datetime
import os
from passlib.hash import sha512_crypt
from flask_uploads import UploadNotAllowed
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('care_homes'))
    return redirect(url_for('login'))


@app.route('/carehomes')
@login_required
def care_homes():
    carehomes = CareHome.query.all()
    return render_template('carehomes.html', carehomes=carehomes)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        
        if user is not None:
            if sha512_crypt.verify(password, user.password):
                login_user(user)
                flash('Logged in.', 'success')
                return redirect(url_for('care_homes'))
            else:
                flash('Invalid username or password.', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/carehome/<id>')
@login_required
def care_home(id):
    carehome = CareHome.query.filter_by(id=id).first()

    if carehome is None:
        abort(404)

    directory = '/static/carehomes/{0}/photos/'.format(id)
    carousel = get_carousel_images(id)
    profilepicture = get_profile_picture(id)
    edit_notes_form = EditNotes(request.form)
    edit_notes_form.notes.data = carehome.notes
    if datetime.datetime.now() > carehome.operator.license_expiration:
        flash('Operator\'s license has expired!', 'danger')
    return render_template('carehome.html', carehome=carehome, carousel=carousel, profilepicture=profilepicture, edit_notes_form=edit_notes_form)


@app.route('/carehome/<id>/edit/notes', methods=['POST'])
@login_required
def edit_notes(id):
    carehome = CareHome.query.filter_by(id=id).first()
    form = EditNotes(request.form)
    print(request.form)
    if form.notes is not None:
        carehome.notes = form.notes.data
        db.session.commit()
        flash('Successfully updated notes', 'success')
        return redirect(url_for('care_home', id=id))
    
    flash('Couldn\'t edit notes', 'warning')
    return redirect(url_for('care_home', id=id))


@app.route('/carehome/<id>/gallery')
@login_required
def gallery(id):
    images = get_carousel_images(id)
    return render_template('gallery.html', images=images, id=id)


@app.route('/carehome/<id>/photos/<photo>/delete')
@login_required
def delete_photo(id, photo):
    directory = '/static/carehomes/{0}/photos/'.format(id)
    if not os.path.exists('.' + directory):
        return redirect(url_for('gallery', id=id))

    if photo in os.listdir('.' + directory):
        os.remove('.' + directory + photo)
        flash('Photo deleted', 'success')
        return redirect(url_for('gallery', id=id))
    
    flash('Couldn\'t delete image', 'info')
    return redirect(url_for('gallery', id=id))

def get_profile_picture(id):
    directory = '/static/carehomes/{0}/sensitive/profilepicture/'.format(id)
    if not os.path.exists('.' + directory):
        os.makedirs('.' + directory)
    if len(os.listdir('.' + directory)) == 0:
        return url_for('static', filename='img/placeholder.svg')
    return directory + os.listdir('.' + directory)[0]

def get_sensitive_file(id, filename):
    directory = '/static/carehomes/{0}/sensitive/'.format(id)
    if not os.path.exists('.' + directory):
        os.makedirs('.' + directory)
    for file in os.listdir('.' + directory):
        if file.split('.')[0] == filename:
            return directory + file
    return None

def get_carousel_images(id):
    directory = '/static/carehomes/{0}/photos/'.format(id)
    if not os.path.exists('.' + directory):
        os.makedirs('.' + directory)
    return [(directory + file) for file in os.listdir('.' + directory)]


@app.route('/carehome/<id>/photos/upload', methods=['POST'])
@login_required
def upload_carehome_photo(id):
    if 'photo' in request.files:
        files = request.files.getlist('photo')
        for image in files:
            try:
                photos.save(image, folder='{0}/photos/'.format(id))
            except UploadNotAllowed:
                flash('That type of file is not allowed!', 'danger')
                return redirect(url_for('gallery', id=id))
        flash('Successfully added {0} photos'.format(len(files)), 'success')
        return redirect(url_for('gallery', id=id))
    else:
        flash('Failed to upload photo, did you upload an image?', 'warning')
        return redirect(url_for('gallery', id=id))


@app.route('/carehome/<id>/sensitive/upload/', methods=['POST'])
@login_required
def upload_sensitive(id):
    if 'photo' in request.files:
        directory = '/static/carehomes/{0}/sensitive/profilepicture/'.format(id)
        if not os.path.exists('.' + directory):
            os.makedirs('.' + directory)
        for file in os.listdir('.' + directory):
            os.remove('.' + directory + file)
        try:
            photos.save(request.files['photo'], folder='{0}/sensitive/profilepicture/'.format(id))
        except UploadNotAllowed:
            flash('That type of file is not allowed!', 'danger')
            return redirect(url_for('care_home', id=id))
        flash('Successfully uploaded', 'success')
        return redirect(url_for('care_home', id=id))
    else:
        flash('That file type is not allowed to be uploaded', 'warning')
        return redirect(url_for('care_home', id=id))


@app.route('/carehome/<id>/delete')
@login_required
def delete_care_home(id):
    carehome = CareHome.query.filter_by(id=id).first()
    db.session.delete(carehome)
    db.session.commit()
    flash('Care Home deleted', 'success')
    return redirect(url_for('care_homes'))

@app.errorhandler(404)
def page_not_found(error):
    return '404', 404


@app.route('/carehome/<id>/edit', methods=['GET', 'POST'])
@login_required
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
        form.address_region.data = operator.address.region
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
        form.notes.data = carehome.notes
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
        operator.address.region = form.address_region.data
        operator.address.street = form.address_street.data
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
        carehome.notes = form.notes.data
        shared_room.amount = form.shared_rooms.data
        private_room.amount = form.private_rooms.data
        carehome.assistive_walking_devices = str(form.patient_walking_device.data).replace('[', '').replace(']', '').replace('\'', '')
        db.session.commit()
        flash('Care Home updated', 'success')
        return redirect(url_for('care_home', id=carehome.id))


@app.route('/carehome/add', methods=['GET', 'POST'])
@login_required
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
            region=form.address_region.data ,
            state='HI', 
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
            notes=form.notes.data,
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