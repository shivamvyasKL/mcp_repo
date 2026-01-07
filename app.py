from flask import Flask, jsonify, request
from datetime import datetime
import os
import logging
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory data storage for demo
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30, "city": "New York"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 25, "city": "Los Angeles"},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "age": 35, "city": "Chicago"}
]

products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 50, "category": "Electronics"},
    {"id": 2, "name": "Mouse", "price": 29.99, "stock": 200, "category": "Electronics"},
    {"id": 3, "name": "Keyboard", "price": 79.99, "stock": 150, "category": "Electronics"},
    {"id": 4, "name": "Monitor", "price": 299.99, "stock": 75, "category": "Electronics"},
    {"id": 5, "name": "Desk Chair", "price": 199.99, "stock": 30, "category": "Furniture"}
]

# API statistics
api_stats = {
    "total_requests": 0,
    "endpoints_hit": {},
    "start_time": datetime.now().isoformat()
}

# Middleware to track requests
@app.before_request
def track_request():
    api_stats["total_requests"] += 1
    endpoint = request.endpoint or "unknown"
    api_stats["endpoints_hit"][endpoint] = api_stats["endpoints_hit"].get(endpoint, 0) + 1
    logger.info(f"{request.method} {request.path} - Client: {request.remote_addr}")

# Decorator for logging
def log_endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Completed {func.__name__}")
        return result
    return wrapper

# Root endpoint
@app.route('/', methods=['GET'])
@log_endpoint
def home():
    return jsonify({
        "message": "Welcome to Enhanced Test API",
        "version": "2.0.0",
        "features": [
            "CRUD operations for users",
            "Search and filter",
            "Pagination support",
            "Request logging",
            "API analytics"
        ],
        "endpoints": [
            "GET / - API info",
            "GET /api/health - Health check",
            "GET /api/stats - API statistics",
            "GET /api/users - Get all users (supports ?search=, ?city=, ?page=, ?limit=)",
            "GET /api/users/<id> - Get user by ID",
            "POST /api/users - Create new user",
            "PUT /api/users/<id> - Update user",
            "DELETE /api/users/<id> - Delete user",
            "GET /api/products - Get all products (supports ?category=, ?page=, ?limit=)",
            "GET /api/products/<id> - Get product by ID",
            "GET /api/time - Get current time",
            "POST /api/echo - Echo request body"
        ]
    })

# Health check endpoint
@app.route('/api/health', methods=['GET'])
@log_endpoint
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Enhanced Test API",
        "version": "2.0.0"
    })

# API Statistics endpoint
@app.route('/api/stats', methods=['GET'])
@log_endpoint
def get_stats():
    uptime = (datetime.now() - datetime.fromisoformat(api_stats["start_time"])).total_seconds()
    return jsonify({
        "success": True,
        "data": {
            "total_requests": api_stats["total_requests"],
            "endpoints_hit": api_stats["endpoints_hit"],
            "uptime_seconds": uptime,
            "start_time": api_stats["start_time"],
            "current_time": datetime.now().isoformat(),
            "total_users": len(users),
            "total_products": len(products)
        }
    })

# Get all users with search and filter
@app.route('/api/users', methods=['GET'])
@log_endpoint
def get_users():
    # Get query parameters
    search = request.args.get('search', '').lower()
    city = request.args.get('city', '').lower()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    # Filter users
    filtered_users = users
    
    if search:
        filtered_users = [
            u for u in filtered_users 
            if search in u['name'].lower() or search in u['email'].lower()
        ]
    
    if city:
        filtered_users = [u for u in filtered_users if city in u['city'].lower()]
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_users = filtered_users[start:end]
    
    return jsonify({
        "success": True,
        "count": len(filtered_users),
        "page": page,
        "limit": limit,
        "total_pages": (len(filtered_users) + limit - 1) // limit,
        "data": paginated_users
    })

# Get user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
@log_endpoint
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
@log_endpoint
def create_user():
    data = request.get_json()
    
    # Validation
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Field '{field}' is required"
            }), 400
    
    # Check if email already exists
    if any(u['email'] == data['email'] for u in users):
        return jsonify({
            "success": False,
            "error": "Email already exists"
        }), 409
    
    new_user = {
        "id": max([u['id'] for u in users]) + 1 if users else 1,
        "name": data['name'],
        "email": data['email'],
        "age": data.get('age'),
        "city": data.get('city')
    }
    users.append(new_user)
    
    logger.info(f"Created new user: {new_user['id']}")
    
    return jsonify({
        "success": True,
        "message": "User created successfully",
        "data": new_user
    }), 201

# Update user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
@log_endpoint
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        # Check if new email is already used by another user
        if any(u['id'] != user_id and u['email'] == data['email'] for u in users):
            return jsonify({
                "success": False,
                "error": "Email already exists"
            }), 409
        user['email'] = data['email']
    if 'age' in data:
        user['age'] = data['age']
    if 'city' in data:
        user['city'] = data['city']
    
    logger.info(f"Updated user: {user_id}")
    
    return jsonify({
        "success": True,
        "message": "User updated successfully",
        "data": user
    })

# Delete user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@log_endpoint
def delete_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404
    
    users.remove(user)
    logger.info(f"Deleted user: {user_id}")
    
    return jsonify({
        "success": True,
        "message": "User deleted successfully"
    })

# Get all products with filter and pagination
@app.route('/api/products', methods=['GET'])
@log_endpoint
def get_products():
    category = request.args.get('category', '').lower()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    # Filter products
    filtered_products = products
    
    if category:
        filtered_products = [p for p in filtered_products if category in p['category'].lower()]
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_products = filtered_products[start:end]
    
    return jsonify({
        "success": True,
        "count": len(filtered_products),
        "page": page,
        "limit": limit,
        "total_pages": (len(filtered_products) + limit - 1) // limit,
        "data": paginated_products
    })

# Get product by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
@log_endpoint
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
@log_endpoint
def get_time():
    return jsonify({
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "unix_timestamp": int(datetime.now().timestamp()),
        "formatted": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Echo endpoint
@app.route('/api/echo', methods=['POST'])
@log_endpoint
def echo():
    data = request.get_json()
    return jsonify({
        "success": True,
        "echo": data,
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "headers": dict(request.headers)
    })

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "path": request.path
    }), 404

# Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Enhanced Test API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
