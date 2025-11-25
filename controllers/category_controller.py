from flask import request, jsonify

from db import db
from models.category import Categories, category_schema, categories_schema
from models.product import Products
from util.reflection import populate_obj
from lib.authenticate import authenticate_return_auth, authenticate

@authenticate
def add_category():
    post_data = request.form if request.form else request.get_json()

    new_category= Categories.new_category_obj()
    populate_obj(new_category, post_data)

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"messsage":"unable to create category"}),400
    
    return jsonify({"message":"category created", "result": category_schema.dump(new_category)}),201

@authenticate
def get_all_categories():
    query= db.session.query(Categories).all()

    if not query:
        return jsonify({"message":"no category found"}), 400
    else:
        return jsonify({"message":"categories found", "results": categories_schema.dump(query)}),200
    
@authenticate
def get_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id ).first()

    if not query:
        return jsonify({"message": "no category with provided id founded."})
    else:
        return jsonify({"message": "category found", "result": category_schema.dump(query)}),200
    

@authenticate_return_auth
def update_category_by_id(category_id, auth_info):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    post_data = request.form if request.form else request.get_json()

    if auth_info.user.role == 'super-admin' and query:
        populate_obj(query, post_data)

        db.session.commit()
   
        return jsonify({"message": "company found", "results": category_schema.dump(query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400

@authenticate_return_auth
def delete_category_by_id(category_id, auth_info):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if auth_info.user.role == 'super-admin':
        if not query:
            return jsonify({"message": "no category with provided id founded."}),400

        db.session.delete(query)
        db.session.commit()

        return jsonify({"message":"category deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
        
    