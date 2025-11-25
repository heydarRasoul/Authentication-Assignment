from flask import request, jsonify

from db import db
from models.warranty import Warranties, warranty_schema, warranties_schema
from util.reflection import populate_obj
from lib.authenticate import authenticate_return_auth, authenticate

@authenticate
def add_warranty():
    post_data = request.form if request.form else request.get_json()

    new_warranty = Warranties.new_warranty_obj()
    populate_obj(new_warranty, post_data)

    try:
        db.session.add(new_warranty)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"messsage":"unable to create warranty"}),400
    
    return jsonify({"message":"warranty created", "result": warranty_schema.dump(new_warranty)}),201

@authenticate
def get_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id ).first()

    if not query:
        return jsonify({"message": "no warranty with provided id founded."})
    else:
        return jsonify({"message": "warranty found", "result": warranty_schema.dump(query)}),200
    
@authenticate
def update_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    post_data = request.form if request.form else request.get_json()

    if query:
        populate_obj(query, post_data)

        db.session.commit()
   
        return jsonify({"message": "warranty found", "results": warranty_schema.dump(query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400

@authenticate_return_auth
def delete_warranty_by_id(warranty_id, auth_info):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if auth_info.user.role== 'super-admin':
        if not query:
            return jsonify({"message": "no warranty with provided id founded."}),400
        db.session.delete(query)
        db.session.commit()

        return jsonify({"message":"warranty deleted"}),200
        
    return jsonify({"message":"unathorized"}),400
            
    