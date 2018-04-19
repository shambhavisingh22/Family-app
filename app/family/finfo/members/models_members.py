from app import db
from sqlalchemy import event
from app.models import *



class Family_Info(Base):
    __tablename__='family_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(128),nullable=False)
    no_of_members = db.Column(db.Integer, nullable=False)
    no_of_adults = db.Column(db.Integer, nullable=False)

    def import_data(self, data):
        try:
            self.id = data.get('id', None)
            self.updated_by = "Shambhavi"
            self.fname = data['fname']
            self.no_of_adults = data['no_of_adults']
            self.no_of_members = data['no_of_members']
            return self

        except Exception as e:

            return str(e)

class Member_Info(Base):
    __tablename__='member_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    family = db.Column(db.Integer,db.ForeignKey('family_info.id'))
    name = db.Column(db.String(128),nullable=False)
    age = db.Column(db.Integer, nullable=False)
    married = db.Column(db.Enum('Yes','No'),nullable=False)
    DOB = db.Column(db.Date)
    phone_no = db.Column(db.BigInteger,nullable=False)
    birth_place = db.Column(db.String(128))
    address = db.Column(db.Integer, db.ForeignKey('member_address.id'), index=True)

    def import_data(self, data):
        try:
            self.id = data.get('id', None)
            self.updated_by = "Shambhavi"
            self.name = data['name']
            self.age = data['age']
            self.married = data['married']
            self.DOB = data.get('DOB',None)
            self.phone_no = data['phone_no']
            self.birth_place = data.get('birth_place',None)
            return self

        except Exception as e:

            return str(e)

    def set_family(self, family):
        try:
            self.family = family

            return self

        except Exception as e:

            return str(e)

    def set_address(self, address):
        try:
            self.address = address

            return self

        except Exception as e:

            return str(e)


class Member_Address(Base):
    __tablename__='member_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(1024), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    pincode = db.Column(db.String(16), nullable=False)
    state = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(32), default="India")
    landmark = db.Column(db.String(128))

    def import_data(self, data):
        try:
            self.id = data['id']
            self.address = data['address']
            self.city = data['city']
            self.pincode = data['pincode']
            self.state = data['state']
            self.landmark = data.get('landmark', None)
            if "country" in data:
                self.country = data['country']
            return self

        except Exception as e:
                return str(e)


class Member_Images(Base) :
    __tablename__ = 'member_images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(512))
    mem_id = db.Column(db.Integer, db.ForeignKey('member_info.id'), index=True)

    def import_data(self, data):
        try:
            self.id = data.get('id',None)
            self.updated_by = "Shambhavi"
            self.image_url = data.get('image_url',None)
            return self

        except Exception as e:

            return str(e)

    def set_mem_id(self, mem_id):
        try:
            self.mem_id = mem_id

            return self

        except Exception as e:

            return str(e)