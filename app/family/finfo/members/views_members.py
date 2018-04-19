from . import member_bp

from app.models import *
from .models_members import *
from flask import jsonify, request
from sqlalchemy import and_
from sqlalchemy import or_
import json
from datetime import datetime
from lib.decorators import json
from lib.email1 import send_email2

@member_bp.route('/add_update_member_info', methods=['POST'])
def add_update_member_info():
    requestObject =  request.get_json()
    try:
        if "id" in requestObject:
            member_info = Member_Info.query.get(requestObject["id"])
        else:
            member_info = Member_Info()
        member_info.import_data(requestObject)  #instance is created which tranfers the frontend info to backend
        db.session.add(member_info)
        db.session.commit()
        return jsonify({"message": "success"})
    except Exception as e:
        print str(e)
        db.session.rollback()
        return jsonify({"message": "error","error_info" : str(e)})

@member_bp.route('/add_update_family_info', methods=['POST'])
def add_update_family_info():
    requestObject =  request.get_json()
    try:
        if "id" in requestObject:
            family_info = Family_Info.query.get(requestObject["id"])
        else:
            family_info = Family_Info()
        family_info.import_data(requestObject)
        db.session.add(family_info)
        db.session.commit()
        return jsonify({"message": "success"})
    except Exception as e:
        print str(e)
        db.session.rollback()
        return jsonify({"message": "error","error_info" : str(e)})

@member_bp.route('/get_member_info_by_id', methods=['GET']) # getting 1 using 1 argument
def get_member_info_by_id():
    id = request.args["id"]
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSES": {
                "age": "",
                "name": "",
                "married": "",

            }}
        request_settings = TEMP_API_PARAMETERS['SEARCH_RESPONSES']

        member = Member_Info.query.get(id)
        member_info = {}
        if member is not None:
            for key in request_settings:
                member_info[key] = getattr(member, key)
        return jsonify({
            "response": "success", "member_detail": member_info})
    except Exception as e:
         print str(e)
         return jsonify({"response": "error"})


@member_bp.route('/get_members_by_age', methods=['GET'])# getting multiple using 1 argument
def get_members_by_age():
    age = request.args["age"]
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSES": {
                "id": "",
                "name": "",

            }}
        request_settings = TEMP_API_PARAMETERS['SEARCH_RESPONSES']
        result = []

        members = Member_Info.query.filter(Member_Info.age>=age)
        for member in members:
             member_data = {}
             for key in request_settings:
                member_data[key] = getattr(member, key)
             result.append(member_data)
        return jsonify({
            "response": "success", "members_details": result})
    except Exception as e:
         print str(e)
         return jsonify({"response": "error"})


@member_bp.route('/add_member_image', methods=['POST'])
def add_member_image():
        requestObject = request.get_json()
        try:
            member = Member_Info.query.get(requestObject["mid"])
            if member is None:
                return jsonify({"response": "failure", "error": "no member found"})
            image = Member_Images()                            # creates an object
            image.import_data(requestObject)                # sends the data from the frontend to the backend
            db.session.add(image)                           # adds the data in the buffer
            db.session.flush()                              # flush allows to use the info in the buffer
            image.set_film_id(requestObject["mid"])         # flush is not needed in this case as there is no info which we need in this line
            db.session.commit()
            return jsonify({"message": "success"})

        except Exception as e:                                  #flush is needed to use when we need to use an info from the buffer before
            print str(e)                                        #committing the info
            db.session.rollback()
            return jsonify({"message": "error"})

@member_bp.route('/get_member_images', methods=['GET'])    # getting multiple using 1 argument
def get_member_images():
    fid = request.args["fid"]
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSES": {
                "id": "",
                "image_url": ""

            }}
        request_settings = TEMP_API_PARAMETERS['SEARCH_RESPONSES']
        result = []

        images = Member_Images.query.filter(fid==Member_Images.mem_id)
        for image in images:
             image_data = {}
             for key in request_settings:
                image_data[key] = getattr(image, key)
             result.append(image_data)
        return jsonify({
            "response": "success", "image_details": result})
    except Exception as e:
         print str(e)
         return jsonify({"response": "error"})

@member_bp.route('/add_member_address', methods=['POST'])
def add_member_address():
        requestObject = request.get_json()
        try:
            member = Member_Info.query.get(requestObject["fid"])
            if member is None:
                return jsonify({"response": "failure", "error": "no member found"})
            address = Member_Address()           #using class make object
            address.import_data(requestObject)
            db.session.add(address)
            db.session.flush()
            member.set_address(address.id)     #used for association of the to tables
            db.session.commit()
            return jsonify({"message": "success"})

        except Exception as e:
            print str(e)
            db.session.rollback()
            return jsonify({"message": "error"})

@member_bp.route('/get_member_address', methods=['GET'])    # case 2 of foreign
def get_member_address():
    fid = request.args["fid"]
    try:
        TEMP_API_PARAMETERS = {
            "SEARCH_RESPONSES": {
                "id": "",
                "address" : ""


            }}
        request_settings = TEMP_API_PARAMETERS['SEARCH_RESPONSES']
        member= Member_Info.query.get(fid)
        #print "hi"
        address= Member_Address.query.get(member.id)
        #print "hi"
        address_data={}

        if address is not None:
            for key in request_settings:
                address_data[key] = getattr(address, key)
        return jsonify({
            "response": "success", "address_detail": address_data})
    except Exception as e:
         print str(e)
         return jsonify({"response": "error"})

@member_bp.route('/sendquery', methods=['GET', 'POST'])
def sendQuery():


    RequestObject = request.get_json()
    print "hi"
    request_user_query = RequestObject['user_query']
    request_user_name = RequestObject['user_name']
    request_user_mail = RequestObject['user_mail']
    request_user_number = RequestObject['user_mobile_number']


    if len(request_user_query) > 0 and len(request_user_name) > 0 and len(request_user_mail) > 0 and len(request_user_number) > 0 :
        send_email2('shambhavisingh15@gmail.com','New User Query',request_user_query)
        return {"message":"success"}
    else:
        return {"message" : "form not filled"}