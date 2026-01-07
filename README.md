# Enhanced Test API - MCP Repository

🚀 A comprehensive Flask-based REST API with full CRUD operations, search, filtering, pagination, and analytics.

## 🎯 Features

### Core Functionality
- ✅ **Complete CRUD operations** for users
- 🔍 **Search and filter** capabilities
- 📄 **Pagination support** for large datasets
- 📊 **API analytics** and request tracking
- 📝 **Comprehensive logging**
- ✉️ **Email validation** and uniqueness checks
- 🛡️ **Enhanced error handling**

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/shivamvyasKL/mcp_repo.git
cd mcp_repo

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Running the API

```bash
python app.py
```

The API will start on `http://localhost:5000`

## 📚 API Endpoints

### 🏠 Root & Utilities

#### GET `/`
Returns API information and available endpoints.

#### GET `/api/health`
Health check endpoint.
```json
{
  "status": "healthy",
  "timestamp": "2026-01-07T12:00:00",
  "service": "Enhanced Test API",
  "version": "2.0.0"
}
```

#### GET `/api/stats`
Returns API statistics and analytics.
```json
{
  "success": true,
  "data": {
    "total_requests": 150,
    "endpoints_hit": {...},
    "uptime_seconds": 3600,
    "total_users": 3,
    "total_products": 5
  }
}
```

### 👥 Users Endpoints

#### GET `/api/users`
Get all users with optional search, filter, and pagination.

**Query Parameters:**
- `search` - Search in name or email
- `city` - Filter by city
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 10)

**Example:**
```bash
curl "http://localhost:5000/api/users?search=john&page=1&limit=5"
```

#### GET `/api/users/<id>`
Get user by ID.

#### POST `/api/users`
Create a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "city": "New York"
}
```

#### PUT `/api/users/<id>`
Update an existing user.

**Request Body:**
```json
{
  "name": "John Updated",
  "age": 31,
  "city": "Boston"
}
```

#### DELETE `/api/users/<id>`
Delete a user.

### 🛍️ Products Endpoints

#### GET `/api/products`
Get all products with optional filter and pagination.

**Query Parameters:**
- `category` - Filter by category
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 10)

**Example:**
```bash
curl "http://localhost:5000/api/products?category=electronics&page=1&limit=3"
```

#### GET `/api/products/<id>`
Get product by ID.

### 🕐 Other Endpoints

#### GET `/api/time`
Get current server time.

#### POST `/api/echo`
Echo back the request body with additional metadata.

## 💡 Usage Examples

### Create a User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28,
    "city": "Seattle"
  }'
```

### Update a User
```bash
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "city": "San Francisco"
  }'
```

### Delete a User
```bash
curl -X DELETE http://localhost:5000/api/users/1
```

### Search Users
```bash
curl "http://localhost:5000/api/users?search=john"
```

### Filter Users by City
```bash
curl "http://localhost:5000/api/users?city=new%20york"
```

### Get Products with Pagination
```bash
curl "http://localhost:5000/api/products?page=1&limit=3"
```

### Get API Statistics
```bash
curl http://localhost:5000/api/stats
```

## 📊 Response Format

All successful responses follow this format:

```json
{
  "success": true,
  "data": {...},
  "message": "Optional message"
}
```

Paginated responses include:

```json
{
  "success": true,
  "count": 10,
  "page": 1,
  "limit": 10,
  "total_pages": 3,
  "data": [...]
}
```

## 🚨 Error Handling

Errors return appropriate HTTP status codes:
- **400** - Bad Request (validation errors)
- **404** - Not Found
- **409** - Conflict (e.g., duplicate email)
- **500** - Internal Server Error

**Error Response Format:**
```json
{
  "success": false,
  "error": "Error message"
}
```

## 🧪 Running Tests

```bash
python test_api.py
```

## 📝 Logging

All API requests are logged with:
- Timestamp
- HTTP method
- Endpoint
- Client IP
- Response status

Logs are output to console in the format:
```
2026-01-07 12:00:00 - __main__ - INFO - GET /api/users - Client: 127.0.0.1
```

## 🛠️ Technology Stack

- **Flask 3.0.0** - Web framework
- **Python 3.x** - Programming language
- **Logging** - Built-in Python logging

## 📋 API Versioning

Current Version: **2.0.0**

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 📄 License

MIT License

## 👨‍💻 Author

Created and enhanced using GitHub MCP specialist

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
