import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable = True)

# Endpoint 1: Get all tasks
@app.route('http://86.109.211.132/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    groccery_list = [{"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity} for product in products]
    return jsonify({"products": groccery_list})

# Endpoint 2: Get a specific task by ID
@app.route('http://86.109.211.132/products/<int:product_id>', methods=['GET'])
def get_products(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({"product": {"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity }})
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 3: Create a new task
@app.route('http://86.109.211.132/products', methods=['POST'])
def create_product():
    data = request.json
    if "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    new_product = Product(name=data['name'], done=False)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "product created", "product": {"id": new_product.id, "name": new_product.name, "price": new_product.price, "quantity": new_product.quantity }}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)