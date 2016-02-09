#!flask/bin/python
from __future__ import print_function
from pymongo import MongoClient
from flask import Flask
from flask import request
from bson import BSON
from bson import json_util
import json
import os
import sys

class veganDb:

    client = MongoClient('localhost', 27017)
    db = client.vegandb        

    def getAllProducts(self):
        products = veganDb.db.products
        product_list = list(products.find())
        return json.dumps(product_list, default=json_util.default, ensure_ascii=False).encode('utf8')
        
    def getProductByName(self, name):
        products = veganDb.db.products
        product_list = list(products.find({'Name': name}))
        return json.dumps(product_list, default=json_util.default, ensure_ascii=False).encode('utf8')

    def getProductsByCategory(self, category):
        products = veganDb.db.products
        product_list = list(products.find({'Category': category}))
        return json.dumps(product_list, default=json_util.default, ensure_ascii=False).encode('utf8')

    def getProductsByProducer(self, producer):
        products = veganDb.db.products
        product_list = list (products.find({'Producer': producer}))
        return json.dumps(product_list, default=json_util.default, ensure_ascii=False).encode('utf8')

    def addProduct(self, name, category, producer, notes, countrys):
        product = { "Name": unicode(name),
                    "Category": unicode(category),
                    "Producer": unicode(producer),
                    "Notes": unicode(notes),
                    "Countrys": countrys,
                    }
        products = veganDb.db.products
        existing = products.count({'Name': name})
        if (existing > 0):
            return json.dumps("FAIL, Duplicate", default=json_util.default)
        else: 
            productId = products.insert_one(product).inserted_id
            return json.dumps("Sucess: " + unicode(productId), default=json_util.default, ensure_ascii=False).encode('utf8')
    
vegansaml = Flask(__name__)

vegandb = veganDb()

@vegansaml.route('/getProductByName', methods=['GET'])
def byname():
    name = str(request.args.get('name'))
    if (name == None):
        return json.dumps('FAIL, Name not supplied')
    return vegandb.getProductByName(name)

@vegansaml.route('/getProductsByCategory')
def bycategory():
    category = str(request.args.get('category'))
    if (category == None):
        return json.dumps('FAIL, Category not supplied')
    return vegandb.getProductsByCategory(category)

@vegansaml.route('/addProduct', methods=['POST'])
def addProduct():
    name = request.form['name']
    category = request.form['category']
    producer = request.form['producer']
    notes = request.form['notes']
    countrys = list(request.form['countrys'].split(","))
    return vegandb.addProduct(name, category, producer, notes, countrys)

@vegansaml.route('/getAllProducts')
def allProducts():
    return vegandb.getAllProducts()

@vegansaml.route('/getProductsByProducer', methods=['GET'])
def byproducer():
    producer = str(request.args.get('producer'))
    if (producer == None):
        return json.dumps('Producer, Name not supplied')
    return vegandb.getProductsByProducer(producer)


if __name__ == '__main__':
    vegansaml.run(debug=True)
    

            
