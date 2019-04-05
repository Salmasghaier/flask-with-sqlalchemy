import os
import logging

from flask import Flask, jsonify, render_template, abort, request
from config import Config
app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
        return products_schema.jsonify(products)
    elif request.method == 'POST':
        product_json = request.get_json()
        ed_product = Product(name=product_json['name'],description=product_json['description'])
        db.session.add(ed_product)
        db.session.commit()
        return '',201

@app.route('/products/<int:id>', methods = ['GET', 'DELETE', 'PATCH'])
def get_products(id):
    if request.method == 'GET':
        products = db.session.query(Product).get(id) # SQLAlchemy request => 'SELECT * FROM products'
        return product_schema.jsonify(products)
    elif request.method == 'DELETE':
        db.session.query(Product).filter(Product.id == id).delete(synchronize_session=False)
        db.session.commit()
        return '',204
    elif request.method == 'PATCH':
        if request.get_json() is None:
                return jsonify(''),422
        my_json = request.get_json()
        db.session.query(Product).filter(Product.id == my_json['id']).update({Product.name: my_json['name'], Product.description: my_json['description']}, synchronize_session=False)
        db.session.commit()
        return jsonify(''),204
