from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# In-memory data storage for demo
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 50},
    {"id": 2, "name": "Mouse", "price": 29.99, "stock": 200},
    {"id": 3, "name": "Keyboard", "price": 79.99, "stock": 150}
]

# Root endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to Test API",
        "version": "1.0.0",
        "endpoints": [
            "/api/health",
            "/api/users",
            "/api/users/<id>",
            "/api/products",
            "/api/products/<id>",
            "/api/time",
            "/api/echo"
        ]
    })

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Test API"
    })

# Get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({
        "success": True,
        "count": len(users),
        "data": users
    })

# Get user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify({
            "success": True,
            "data": user
        })
    return jsonify({
        "success": False,
        "error": "User not found"
    }), 404

# Create new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            "success": False,
            "error": "Name and email are required"
        }), 400
    
    new_user = {
        "id": max([u['id'] for u in users]) + 1 if users else 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    
    return jsonify({
        "success": True,
        "message": "User created successfully",
        "data": new_user
    }), 201

# Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({
        "success": True,
        "count": len(products),
        "data": products
    })

# Get product by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify({
            "success": True,
            "data": product
        })
    return jsonify({
        "success": False,
        "error": "Product not found"
    }), 404

# Get current time
@app.route('/api/time', methods=['GET'])
def get_time():
    return jsonify({
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "unix_timestamp": int(datetime.now().timestamp())
    })

# Echo endpoint - returns whatever is sent
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({
        "success": True,
        "echo": data,
        "timestamp": datetime.now().isoformat()
    })

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

# Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
