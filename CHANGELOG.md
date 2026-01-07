# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-01-07

### Added
- **UPDATE endpoint** for users (PUT /api/users/<id>)
- **DELETE endpoint** for users (DELETE /api/users/<id>)
- **Search functionality** for users (query parameter: ?search=)
- **Filter by city** for users (query parameter: ?city=)
- **Pagination support** for users and products (query parameters: ?page=, ?limit=)
- **Category filter** for products (query parameter: ?category=)
- **API statistics endpoint** (GET /api/stats) - tracks requests, endpoints hit, uptime
- **Request logging** - all API calls are now logged
- **Email uniqueness validation** - prevents duplicate emails
- **Enhanced error messages** with more context
- **Additional user fields** - age and city
- **Additional product fields** - category
- **Request tracking middleware** - automatically tracks all requests

### Enhanced
- Improved input validation for user creation
- Better error handling with detailed messages
- Enhanced echo endpoint with headers information
- More comprehensive API documentation in root endpoint
- Logging decorator for all endpoints
- Version bumped to 2.0.0

### Changed
- Users now include age and city fields
- Products now include category field
- Health check now includes version information
- Time endpoint now includes formatted timestamp

## [1.0.0] - 2026-01-07

### Initial Release
- Basic Flask REST API
- GET endpoints for users and products
- POST endpoint for user creation
- Health check endpoint
- Echo endpoint
- Basic error handling
