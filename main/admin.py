import flask, flask.views
from flask import url_for, request, session, redirect, jsonify, Response, make_response, current_app
from jinja2 import environment, FileSystemLoader
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean
from flask.ext import admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from dateutil.parser import parse as parse_date
from flask import render_template, request
from flask import session, redirect
from datetime import timedelta
from datetime import datetime
from functools import wraps, update_wrapper
import threading
from threading import Timer
from multiprocessing.pool import ThreadPool
import calendar
from calendar import Calendar
from time import sleep
import requests
import datetime
from datetime import date
import time
import json
import uuid
import random
import string
import smtplib
from email.mime.text import MIMEText as text
import os
import db_conn
from db_conn import db, app
from models import Household, ParentChild, Citizen, HouseholdImage, AdminUser

APP_SECRET = '01c5d1f8d3bfa9966786065c5a2d829d7e84cf26fbfb4a47c91552cb7c091608'
now = datetime.datetime.now()

class IngAdmin(sqla.ModelView):
    column_display_pk = True

admin = Admin(app, name='mobilization')
admin.add_view(IngAdmin(Household, db.session))
admin.add_view(IngAdmin(Citizen, db.session))
admin.add_view(IngAdmin(ParentChild, db.session))

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)

def authenticate_user(email, password):
    user = AdminUser.query.filter_by(email=email,password=password).first()
    if not user or user == None:
        return jsonify(status='failed', error='Invalid email or password')
    if user.status != 'Active':
        return jsonify(status='failed', error='Your account has been deactivated')
    session['user_id'] = user.id
    session['user_name'] = user.name
    return jsonify(status='success', error=''),200


@app.route('/', methods=['GET', 'POST'])
@nocache
def dashboard():
    if not session:
        return redirect('/login')
    households = Household.query.all()
    return flask.render_template('index.html',households=households, name=session['user_name'])


@app.route('/login', methods=['GET', 'POST'])
@nocache
def login():
    if session:
        return redirect('/')
    return flask.render_template('login.html')


@app.route('/user/authenticate', methods=['GET', 'POST'])
@nocache
def authenticate():
    if session:
        return redirect('/')
    login_data = flask.request.form.to_dict()
    return authenticate_user(login_data['user_email'], login_data['user_password'])


@app.route('/household', methods=['GET', 'POST'])
@nocache
def get_household_data():
    household_id = flask.request.args.get('household_id')
    household = Household.query.filter_by(id=household_id).first()
    images = HouseholdImage.query.filter_by(household_id=household_id).all()
    return jsonify(
        household_name = household.name,
        template = flask.render_template(
            'household_data.html', 
            household=household,
            images=images
            )
        )
    

@app.route('/logout', methods=['GET', 'POST'])
@nocache
def logout():
    session.clear()
    return redirect('/login')


@app.route('/db/rebuild', methods=['GET', 'POST'])
def rebuild_database():
    db.drop_all()
    db.create_all()
    household = Household(
        name='Barcelona-001',
        number_of_members='5',
        region='Region IV-A',
        province='Quezon',
        city='Lucena',
        barangay='Ilayang Iyam',
        address='12 Zamora St. Ciudad Maharlika, Ilayang Iyam, Lucena City',
        cluster='2011334281',
        contact='09159484200',
        status='Green',
        remarks=''
        )

    household1 = Household(
        name='Barcelona-002',
        number_of_members=3,
        region='Region IV-A',
        province='Quezon',
        city='Lucena',
        barangay='Isabang',
        address='Barcelona Compound, Lucena City',
        cluster='2011334281',
        contact='09159484200',
        status='Green',
        remarks=''
        )

    household2 = Household(
        name='Armamento-001',
        number_of_members=3,
        region='Region IV-A',
        province='Quezon',
        city='Lucena',
        barangay='Gulang Gulang',
        address='Capistrano Subdivision, Lucena City',
        cluster='2011334282',
        contact='09159484200',
        status='Green',
        remarks=''
        )

    image = HouseholdImage(
        household_id=1,
        path='../static/images/households/test_household.jpg'
        )

    image1 = HouseholdImage(
        household_id=2,
        path='../static/images/households/test_household1.jpg'
        )

    image2 = HouseholdImage(
        household_id=3,
        path='../static/images/households/test_household2.jpg'
        )

    citizen1 = Citizen(
        last_name='Barcelona',
        first_name='Jasper Oliver',
        middle_name='Estrada',
        gender='Male',
        age=23,
        birthday='June 11, 1994',
        employment_status='Employed',
        occupation='Chief Executive Officer',
        company='Pisara',
        email='jasper@pisara.tech',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Single',
        msisdn='09159484200',
        household_id=1,
        household_name='Barcelona-001',
        position='Child',
        status='Green',
        remarks=''
        )

    citizen2 = Citizen(
        last_name='Barcelona',
        first_name='Flora',
        middle_name='Estrada',
        gender='Female',
        age=63,
        birthday='May 29, 1953',
        employment_status='Retired',
        occupation='Government Health Worker',
        company='City Health Office',
        email='N/A',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Widowed',
        msisdn='09159484200',
        household_id=1,
        household_name='Barcelona-001',
        position='Head',
        status='Green',
        remarks=''
        )

    citizen3 = Citizen(
        last_name='Barcelona',
        first_name='Ma Angelica',
        middle_name='Estrada',
        gender='Female',
        age=29,
        birthday='December 18, 1988',
        employment_status='Employed',
        occupation='Web Content Developer',
        company='Intercontinental Hotels Group',
        email='N/A',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Single',
        msisdn='09159484200',
        household_id=1,
        household_name='Barcelona-001',
        position='Child',
        status='Green',
        remarks=''
        )

    citizen4 = Citizen(
        last_name='Barcelona',
        first_name='Ma April Therese',
        middle_name='Estrada',
        gender='Female',
        age=34,
        birthday='April 26, 1986',
        employment_status='Employed',
        occupation='Technical Support',
        company='Direct with Hotels',
        email='N/A',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Single',
        msisdn='09159484200',
        household_id=1,
        household_name='Barcelona-001',
        position='Child',
        status='Green',
        remarks=''
        )

    citizen5 = Citizen(
        last_name='Sacristia',
        first_name='Rolando',
        middle_name='Dela Cruz',
        gender='Male',
        age=46,
        birthday='Augyst 08, 1976',
        employment_status='Employed',
        occupation='House Helper',
        company='N/A',
        email='N/A',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Single',
        msisdn='09159484200',
        household_id=1,
        household_name='Barcelona-001',
        position='Resident',
        status='Green',
        remarks=''
        )

    citizen6 = Citizen(
        last_name='Barcelona',
        first_name='Jadd Paolo Luigi',
        middle_name='Ong',
        gender='Male',
        age=29,
        birthday='April 14, 1986',
        employment_status='Employed',
        occupation='Chief Marketing Officer',
        company='Pisara',
        email='jadd@pisara.tech',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Married',
        msisdn='09159484200',
        household_id=2,
        household_name='Barcelona-002',
        position='Head',
        status='Green',
        remarks=''
        )

    citizen7 = Citizen(
        last_name='Barcelona',
        first_name='Cyril Joy',
        middle_name='Lucero',
        gender='Female',
        age=23,
        birthday='April 25, 1986',
        employment_status='Employed',
        occupation='Dentist',
        company='Lucero Dental Clinic',
        email='N/A',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Married',
        msisdn='09159484200',
        household_id=2,
        household_name='Barcelona-002',
        position='Spouse',
        status='Green',
        remarks=''
        )

    citizen8 = Citizen(
        last_name='Barcelona',
        first_name='Stephen Skylar',
        middle_name='Lucero',
        gender='Male',
        age=1,
        birthday='November 15, 2017',
        employment_status='Unemployed',
        occupation='N/A',
        company='N/A',
        email='N/A',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Single',
        msisdn='N/A',
        household_id=2,
        household_name='Barcelona-002',
        position='Spouse',
        status='Green',
        remarks=''
        )

    citizen9 = Citizen(
        last_name='Armamento',
        first_name='Jan Paolo',
        middle_name='Calzado',
        gender='Male',
        age=23,
        birthday='January 23, 1994',
        employment_status='Employed',
        occupation='Chief Infrastructure Officer',
        company='Pisara',
        email='janno@pisara.tech',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Married',
        msisdn='09159484200',
        household_id=3,
        household_name='Armamento-001',
        position='Head',
        status='Green',
        remarks=''
        )

    citizen10 = Citizen(
        last_name='Armamento',
        first_name='Caithlin Lois',
        middle_name='Nicolas',
        gender='Female',
        age=23,
        birthday='January 23, 1994',
        employment_status='Unemployed',
        occupation='Student',
        company='MSEUF',
        email='N/A',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Married',
        msisdn='09159484200',
        household_id=3,
        household_name='Armamento-001',
        position='Spouse',
        status='Green',
        remarks=''
        )

    citizen11 = Citizen(
        last_name='Armamento',
        first_name='Coco',
        middle_name='Nicolas',
        gender='Female',
        age=1,
        birthday='January 23, 1994',
        employment_status='Unemployed',
        occupation='N/A',
        company='N/A',
        email='N/A',
        citizenship='Filipino',
        religion='Roman Catholic',
        civil_status='Single',
        msisdn='N/A',
        household_id=3,
        household_name='Armamento-001',
        position='Child',
        status='Green',
        remarks=''
        )

    admin_user = AdminUser(
        email='admin@gmail.com',
        password='password',
        status='Active',
        name="Jasper Barcelona"
        )

    db.session.add(household)
    db.session.add(household1)
    db.session.add(household2)   

    db.session.add(citizen1)
    db.session.add(citizen2)
    db.session.add(citizen3)
    db.session.add(citizen4)
    db.session.add(citizen5)
    db.session.add(citizen6)
    db.session.add(citizen7)
    db.session.add(citizen8)
    db.session.add(citizen9)
    db.session.add(citizen10)
    db.session.add(citizen11)

    db.session.add(image)
    db.session.add(image1)
    db.session.add(image2)

    db.session.add(admin_user)

    db.session.commit()

    return jsonify(status='success'),201

if __name__ == '__main__':
    app.run(port=8000,debug=True,host='0.0.0.0')
    # port=int(os.environ['PORT']), host='0.0.0.0'