#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Home route
@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET all bakeries
@app.route('/bakeries')
def bakeries():
    all_bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(all_bakeries), 200)

# GET single bakery by ID
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        return make_response(jsonify(bakery.to_dict()), 200)
    return make_response(jsonify({"error": "Bakery not found"}), 404)

# GET baked goods sorted by price descending
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    goods_list = [good.to_dict() for good in goods]
    return make_response(jsonify(goods_list), 200)

# GET the single most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bg = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if bg:
        return make_response(jsonify(bg.to_dict()), 200)
    return make_response(jsonify({"error": "No baked goods found"}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)


