from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from random import randrange
import os

# Initialize App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), unique=True)
    percentage_cpu_used = db.Column(db.Integer)
    percentage_memory_used = db.Column(db.Integer)

    def __init__(self, ip, percentage_cpu_used, percentage_memory_used):
        self.ip = ip
        self.percentage_cpu_used = percentage_cpu_used
        self.percentage_memory_used = percentage_memory_used


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        # fields = ('id', 'percentage_cpu_used', 'percentage_memory_used')
        fields = ('ip', 'percentage_cpu_used', 'percentage_memory_used')


# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Create Product
@app.route('/metrics', methods=['POST'])
def add_product():
    ip = request.json['ip']
    percentage_cpu_used = request.json['percentage_cpu_used']
    percentage_memory_used = request.json['percentage_memory_used']

    new_product = Product(ip, percentage_cpu_used, percentage_memory_used)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get All Products
@app.route('/report', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Generate Database
db.create_all()

# Run the Server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
