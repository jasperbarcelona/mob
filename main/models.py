import flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean
from db_conn import db, app
import json

class Serializer(object):
  __public__ = None

  def to_serializable_dict(self):
    dict = {}
    for public_key in self.__public__:
      value = getattr(self, public_key)
      if value:
        dict[public_key] = value
    return dict

class SWEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Serializer):
      return obj.to_serializable_dict()
    if isinstance(obj, (datetime)):
      return obj.isoformat()
    return json.JSONEncoder.default(self, obj)

def SWJsonify(*args, **kwargs):
  return app.response_class(json.dumps(dict(*args, **kwargs), cls=SWEncoder, 
         indent=None if request.is_xhr else 2), mimetype='application/json')
        # from https://github.com/mitsuhiko/flask/blob/master/flask/helpers.py

class Household(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60))
    number_of_members = db.Column(db.Integer())
    region = db.Column(db.String(60))
    province = db.Column(db.String(60))
    city = db.Column(db.String(60))
    barangay = db.Column(db.String(100))
    address = db.Column(db.Text())
    cluster = db.Column(db.String(100))
    contact = db.Column(db.String(15))
    status = db.Column(db.String(60))
    remarks = db.Column(db.String(60))

class Citizen(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    last_name = db.Column(db.String(60))
    first_name = db.Column(db.String(60))
    middle_name = db.Column(db.String(60))
    gender = db.Column(db.String(60))
    age = db.Column(db.Integer())
    birthday = db.Column(db.String(80))
    employment_status = db.Column(db.String(60))
    occupation = db.Column(db.String(60))
    company = db.Column(db.String(60))
    email = db.Column(db.String(60))
    citizenship = db.Column(db.String(60))
    religion = db.Column(db.String(60))
    civil_status = db.Column(db.String(60))
    msisdn = db.Column(db.String(15))
    household_id = db.Column(db.Integer())
    household_name = db.Column(db.String(60))
    position = db.Column(db.String(60))
    status = db.Column(db.String(60))
    remarks = db.Column(db.String(60))

class HouseholdImage(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    household_id = db.Column(db.Integer())
    path = db.Column(db.Text())

class AdminUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(60))
    status = db.Column(db.String(60))
    name = db.Column(db.String(100))


class ParentChild(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    parent_id = db.Column(db.Integer())
    child_id = db.Column(db.Integer())
    relation = db.Column(db.String(60))