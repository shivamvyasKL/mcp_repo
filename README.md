# Test API - MCP Repository

A simple Flask-based REST API for testing GitHub MCP functionality.

## Features

- RESTful API endpoints
- User management (GET, CREATE)
- Product listing
- Health check endpoint
- Echo endpoint for testing
- Error handling

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### Root
- **GET /** - Welcome message with available endpoints

### Health Check
- **GET /api/health** - Returns health status of the API

### Users
- **GET /api/users** - Get all users
- **GET /api/users/<id>** - Get user by ID
- **POST /api/users** - Create new user
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
  ```

### Products
- **GET /api/products** - Get all products
- **GET /api/products/<id>** - Get product by ID

### Utilities
- **GET /api/time** - Get current server time
- **POST /api/echo** - Echo back the request body

## Example Usage

```bash
# Health check
curl http://localhost:5000/api/health

# Get all users
curl http://localhost:5000/api/users

# Create a new user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# Get all products
curl http://localhost:5000/api/products

# Echo test
curl -X POST http://localhost:5000/api/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World"}'
```

## Response Format

All responses follow this format:

```json
{
  "success": true,
  "data": {...},
  "message": "Optional message"
}
```

## Error Handling

Errors return appropriate HTTP status codes:
- **400** - Bad Request
- **404** - Not Found
- **500** - Internal Server Error

## Technology Stack

- **Flask 3.0.0** - Web framework
- **Python 3.x** - Programming language

## License

MIT License

## Author

Created using GitHub MCP specialist
