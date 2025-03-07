from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Set up the database URI (Using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the inventory model (SQLAlchemy ORM)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Endpoint to get all inventory items
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    products = Product.query.all()
    inventory = [{"id": p.id, "name": p.name, "stock": p.stock, "buying_price": p.buying_price,
                  "selling_price": p.selling_price, "date_added": p.date_added.strftime("%Y-%m-%d")}
                 for p in products]
    return jsonify(inventory)

# Endpoint to add a new product to the inventory
@app.route('/api/inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        stock=data['stock'],
        buying_price=data['buying_price'],
        selling_price=data['selling_price'],
        date_added=datetime.strptime(data['date_added'], "%Y-%m-%d")
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201

# Simple route to serve the HTML frontend
@app.route('/')
def index():
    return render_template('index.html')

# Route for manage inventory page
@app.route('/manage-inventory')
def manage_inventory():
    return render_template('manage_inventory.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
