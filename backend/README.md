# Healthcare Backend API

A Flask-based REST API backend for the Healthcare application with MongoDB database and JWT authentication.

## Features

- User authentication (register, login, JWT tokens)
- User profile management
- Health records management
- Medical reports management
- MongoDB integration
- CORS support
- Role-based access control

## Project Structure

```
backend/
├── app/
│   ├── models/           # Database models
│   │   ├── user.py       # User model
│   │   └── health_record.py  # Health records model
│   ├── routes/           # API route handlers
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── health_routes.py
│   │   └── report_routes.py
│   ├── utils/            # Utility functions
│   │   └── auth.py       # Authentication helpers
│   └── __init__.py       # App factory
├── config.py             # Configuration settings
├── app.py                # Main entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation

1. **Clone or navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and update:
   - `SECRET_KEY` - A strong secret key for Flask
   - `MONGODB_URI` - Your MongoDB connection string
   - `JWT_SECRET` - A secret key for JWT tokens

5. **Ensure MongoDB is running**
   - MongoDB should be accessible at the URI specified in `.env`

## Running the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/verify` - Verify JWT token

### User Management
- `GET /api/user/profile` - Get user profile (requires auth)
- `PUT /api/user/profile` - Update user profile (requires auth)
- `DELETE /api/user/<user_id>` - Delete user account (requires auth)

### Health Records
- `GET /api/health/records` - Get all health records (requires auth)
- `POST /api/health/records` - Create health record (requires auth)
- `GET /api/health/records/<record_id>` - Get specific record (requires auth)
- `PUT /api/health/records/<record_id>` - Update record (requires auth)
- `DELETE /api/health/records/<record_id>` - Delete record (requires auth)

### Medical Reports
- `GET /api/reports` - Get all reports (requires auth)
- `POST /api/reports` - Create new report (requires auth)
- `GET /api/reports/<report_id>` - Get specific report (requires auth)
- `DELETE /api/reports/<report_id>` - Delete report (requires auth)

## Example API Usage

### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password",
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "gender": "Male"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password"
  }'
```

### Get Profile (with token)
```bash
curl -X GET http://localhost:5000/api/user/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Technologies Used

- Flask 3.0.0
- MongoDB with PyMongo
- JWT for authentication
- Bcrypt for password hashing
- CORS for cross-origin requests

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_APP | Flask application entry point | app.py |
| FLASK_ENV | Flask environment (development/production) | development |
| FLASK_DEBUG | Enable Flask debug mode | True |
| SECRET_KEY | Flask secret key | dev-secret-key-change-in-production |
| MONGODB_URI | MongoDB connection string | mongodb://localhost:27017/healthcare |
| JWT_SECRET | JWT secret key | jwt-secret-key-change-in-production |
| JWT_EXPIRATION_HOURS | JWT token expiration time | 24 |

## Security Notes

- Always change SECRET_KEY and JWT_SECRET in production
- Use HTTPS in production
- Store sensitive information in environment variables
- Validate all user inputs
- Implement rate limiting for production

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

To run tests (if implemented):
```bash
pytest
```

## License

MIT

## Support

For issues or questions, please contact the development team.
