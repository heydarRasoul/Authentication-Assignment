from flask import jsonify, request

from db import db
from models.product import Products, product_schema, products_schema
from models.category import Categories
from util.reflection import populate_obj
from lib.authenticate import authenticate_return_auth, authenticate


@authenticate
def create_product():
    post_data = request.form if request.form else request.get_json()

    new_product = Products.new_product_obj()
    populate_obj(new_product, post_data)

    try:
        db.session.add(new_product)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "product created", "result": product_schema.dump(new_product)}), 201


@authenticate
def add_product_to_category():
    post_data = request.form if request.form else request.get_json()
    product_id= post_data.get("product_id")
    category_id= post_data.get("category_id")

    product_query = db.session.query(Products).filter(Products.product_id==product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id==category_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    if not category_query:
        return jsonify({"message":"category not found"}),404
    
    if category_query in product_query.categories:
        return jsonify({"message": "product already in this category"}), 400
    
    product_query.categories.append(category_query)


    db.session.commit()
    return jsonify({"message":"product added to category", "result": product_schema.dump(product_query)}),200


@authenticate
def get_all_products():
    products_query = db.session.query(Products).all()

    if not products_query:
        return jsonify({"message":"no products found"}),404
    
    else:
        return jsonify({"message":"products found", "results": products_schema.dump(products_query)}), 200


@authenticate
def get_active_products():
    active_products_query = db.session.query(Products).filter(Products.active).all()

    if not active_products_query:
        return jsonify({"message":"no active product found"}),400
    else:
        return jsonify({"message":"products found", "results":products_schema.dump(active_products_query)}),200

@authenticate  
def get_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify ({"message":"no result found for provided id"}),400
    else:
        return jsonify ({"message":"product found", "result": product_schema.dump(product_query)}), 200


@authenticate
def get_product_by_company_id(company_id):
    query = db.session.query(Products).filter(Products.company_id == company_id).all()

    if not query:
        return jsonify ({"message":"no result found"}),400
    else:
        return jsonify ({"message":"product found", "result": products_schema.dump(query)}), 200



@authenticate_return_auth
def update_product_by_id(product_id, auth_info):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    post_data = request.form if request.form else request.get_json()

    if auth_info.user.role == 'super-admin' and product_query:
        populate_obj(product_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "product found", "results": product_schema.dump(product_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400



@authenticate_return_auth
def delete_product_by_id(product_id, auth_info):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if auth_info.user.role == 'super-admin':
        if not query:
            return jsonify({"message": "no product with provided id founded."}),400
    
        db.session.delete(query)
        db.session.commit()

        return jsonify({"message":"product deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    
    