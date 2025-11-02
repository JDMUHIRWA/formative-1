# MongoDB API - Earthquake Data Management

## Overview
This module provides RESTful API endpoints for managing earthquake data in MongoDB Atlas with **full Pydantic validation**.

## Files

### `schemas.py`
Defines Pydantic models for request/response validation:

- **`EarthquakeMongoBase`**: Base schema with all common fields
- **`EarthquakeMongoCreate`**: Schema for creating new earthquakes (validates required fields)
- **`EarthquakeMongoUpdate`**: Schema for updating earthquakes (all fields optional)
- **`EarthquakeMongoResponse`**: Response schema including MongoDB `_id`
- **`DeleteResponse`**: Standard delete operation response

### `crud.py`
Database operations with type hints and proper validation:

- `create_earthquake()`: Insert new earthquake with validation
- `get_earthquakes()`: Retrieve all earthquakes with pagination
- `get_earthquake_by_id()`: Get single earthquake by MongoDB `_id`
- `update_earthquake()`: Update earthquake fields (partial updates supported)
- `delete_earthquake()`: Delete earthquake by `_id`

### `routers/earthquake_routes.py`
FastAPI router with validated endpoints:

- **POST** `/earthquakes`: Create new earthquake
- **GET** `/earthquakes`: List all earthquakes (with pagination)
- **GET** `/earthquakes/{eq_id}`: Get single earthquake
- **PUT** `/earthquakes/{eq_id}`: Update earthquake
- **DELETE** `/earthquakes/{eq_id}`: Delete earthquake

## Validation Features

✅ **Input Validation**
- Magnitude: 0-10
- Depth: Must be positive
- Year: 1900-2100
- Month: 1-12
- Latitude: -90 to 90
- Longitude: -180 to 180
- CDI: 0-9
- MMI: 1-9

✅ **Error Handling**
- Invalid ID format detection
- 404 for missing records
- Clear error messages

✅ **Type Safety**
- Proper type hints throughout
- Pydantic models prevent invalid data
- Better IDE autocomplete support

## Example Usage

### Create Earthquake
```bash
curl -X POST "http://localhost:8000/mongo/earthquakes" \
  -H "Content-Type: application/json" \
  -d '{
    "magnitude": 6.5,
    "depth": 10.0,
    "sig": 500,
    "Year": 2024,
    "Month": 3,
    "latitude": 35.5,
    "longitude": -120.5,
    "tsunami": 0
  }'
```

### Get All Earthquakes (with pagination)
```bash
curl "http://localhost:8000/mongo/earthquakes?skip=0&limit=10"
```

### Update Earthquake
```bash
curl -X PUT "http://localhost:8000/mongo/earthquakes/507f1f77bcf86cd799439011" \
  -H "Content-Type: application/json" \
  -d '{
    "magnitude": 7.0,
    "depth": 15.0
  }'
```

### Delete Earthquake
```bash
curl -X DELETE "http://localhost:8000/mongo/earthquakes/507f1f77bcf86cd799439011"
```

## Improvements Over Previous Version

1. **Replaced generic `dict` with Pydantic models** - Ensures type safety and validation
2. **Added pagination** to GET all endpoint
3. **Better error messages** with detailed HTTP exceptions
4. **API documentation** - All endpoints have docstrings visible in Swagger UI
5. **Type hints** - Full type coverage for better IDE support
6. **Validation constraints** - Field-level validation (ranges, formats, etc.)
7. **Partial updates** - Update endpoint only modifies provided fields

## Integration with Main API

This MongoDB version can run alongside the PostgreSQL version, providing flexibility to use either database backend.
