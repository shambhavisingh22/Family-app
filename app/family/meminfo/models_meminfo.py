from app import db
from sqlalchemy import event
from app.models import *
from app.family.finfo.members.models_members import *


class Study_Info(Base):
    __tablename__='study_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, db.ForeignKey('member_info.id'), index=True)
    college_name = db.Column(db.String(128),nullable=False)
    area_of_study = db.Column(db.String(128), nullable=False)
    branch = db.Column(db.String(128), nullable=False)
    place = db.Column(db.String(128), nullable=False)
    year = db.Column(db.Integer,nullable=False)

    def import_data(self, data):
        try:
            self.id = data.get('id', None)
            self.updated_by = "Shambhavi"
            self.college_name = data['college_name']
            self.area_of_study = data['area_of_study']
            self.branch = data['branch']
            self.place = data['place']
            self.year = data['year']
            return self

        except Exception as e:

            return str(e)

    def member_name(self, name):
        try:
            self.name = name

            return self

        except Exception as e:

            return str(e)

class Marriage_Info(Base):
    __tablename__='marriage_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, db.ForeignKey('member_info.id'), index=True)
    date_of_marriage = db.Column(db.Date)
    marriage_place = db.Column(db.String(128))

    def import_data(self, data):
        try:
            self.id = data.get('id', None)
            self.updated_by = "Shambhavi"
            self.date_of_marriage = data.get('date_of_marriage',None)
            self.marriage_place = data.get('marriage_place',None)
            return self

        except Exception as e:

            return str(e)

    def member_name(self, name):
        try:
            self.name = name

            return self

        except Exception as e:

            return str(e)

class Health_Info(Base):
    __tablename__='health_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, db.ForeignKey('member_info.id'), index=True)
    family = db.Column(db.Integer,db.ForeignKey('family_info.id'),index=True)
    chronic_disease = db.Column(db.String(1024), nullable=False)

    def import_data(self, data):
        try:
            self.id = data['id']
            self.chronic_disease = data['chronic_disease']
            return self

        except Exception as e:
                return str(e)

    def member_name(self, name):
        try:
            self.name = name

            return self

        except Exception as e:

            return str(e)

    def family_name(self,family):
        try:
            self.family = family

            return self

        except Exception as e:

            return str(e)
