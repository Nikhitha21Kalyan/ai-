# Healthcare Fraud Detection - Complete Setup Guide

## Project Overview

This is a full-stack Healthcare Fraud Detection system with:
- **Frontend**: HTML/CSS/JavaScript (Vanilla JS)
- **Backend**: Python Flask REST API
- **Database**: MongoDB
- **Authentication**: JWT Tokens

## Prerequisites

- Python 3.8+
- MongoDB (local or cloud instance)
- Node.js/npm (optional, for frontend build tools)

## Project Structure

```
Healthcare/
├── frontend files (html, css, js)
├── backend/
│   ├── app/
│   │   ├── models/        # Database models
│   │   ├── routes/        # API endpoints
│   │   ├── utils/         # Helper functions
│   │   └── __init__.py    # App factory
│   ├── config.py          # Configuration
│   ├── app.py             # Entry point
│   └── requirements.txt   # Dependencies
└── README.md
```

## Setup Instructions

### 1. Backend Setup

#### Step 1.1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Step 1.2: Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and update:
```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_very_secret_key_here_change_in_production
MONGODB_URI=mongodb://localhost:27017/healthcare
JWT_SECRET=your_jwt_secret_key_here_change_in_production
JWT_EXPIRATION_HOURS=24
PORT=5000
```

#### Step 1.3: Start MongoDB

**Local MongoDB:**
```bash
mongod
```

**Cloud MongoDB (MongoDB Atlas):**
- Update `MONGODB_URI` in `.env` with your connection string

#### Step 1.4: Run Backend Server

```bash
python app.py
```

The backend API will be available at: `http://localhost:5000`

### 2. Frontend Setup

The frontend is automatically served by the Flask backend at `http://localhost:5000`

#### Frontend Configuration

The frontend uses configuration from `js/config.js`. By default, it connects to:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

To change the API endpoint:
1. Open browser console while on the app
2. Run: `localStorage.setItem('apiUrl', 'http://your-api-url:port/api')`
3. Reload the page

## Running the Application

### Quick Start (All-in-One)

1. **Start MongoDB**
```bash
mongod
```

2. **Start Backend**
```bash
cd backend
python app.py
```

3. **Access Application**
- Open browser: `http://localhost:5000`
- Register or login with your credentials
- Use the application

### Environment Setup for Development

**Windows (PowerShell)**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python app.py
```

**Linux/Mac (Bash)**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Login user
- `GET /api/auth/verify` - Verify token

### User Management
- `GET /api/user/profile` - Get profile
- `PUT /api/user/profile` - Update profile
- `DELETE /api/user/{user_id}` - Delete account

### Health Records
- `GET /api/health/records` - List records
- `POST /api/health/records` - Create record
- `GET /api/health/records/{id}` - Get record
- `PUT /api/health/records/{id}` - Update record
- `DELETE /api/health/records/{id}` - Delete record

### Reports
- `GET /api/reports` - List reports
- `POST /api/reports` - Create report
- `GET /api/reports/{id}` - Get report
- `DELETE /api/reports/{id}` - Delete report

## Testing

### Test User Credentials

After starting the app:

1. **Register New Account**
   - Navigate to http://localhost:5000
   - Click "Login"
   - Go to "Sign Up" tab
   - Fill in details and create account

2. **Login**
   - Use the credentials you just created

3. **Upload Sample Data**
   - Go to "Upload Claims" page
   - Create a test CSV with columns: `ClaimID,Patient,Amount,Diagnosis`
   - Upload and analyze

## Troubleshooting

### MongoDB Connection Error
```
Error: [Errno 10061] No connection could be made because the target machine actively refused it
```
**Solution**: Make sure MongoDB is running
```bash
mongod
```

### Port Already in Use
```
Address already in use
```
**Solution**: Use a different port
```bash
# In backend/app.py
app.run(host='0.0.0.0', port=5001)  # Change port number
```

### Token Expiration
- Tokens expire after 24 hours (configurable in `.env`)
- User will be redirected to login automatically

### CORS Errors
- Backend CORS is configured for all origins in development
- For production, update `CORS` settings in `app/__init__.py`

## Database Reset

To clear all data:

```bash
# Using MongoDB shell
mongo
use healthcare
db.dropDatabase()
exit
```

## Deployment

### Production Setup

1. **Update Configuration**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=<strong-random-secret>
   JWT_SECRET=<strong-random-secret>
   ```

2. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

3. **Security Checklist**
   - [ ] Change SECRET_KEY and JWT_SECRET
   - [ ] Use HTTPS only
   - [ ] Set strong database password
   - [ ] Configure CORS for specific origins
   - [ ] Enable rate limiting
   - [ ] Use environment variables for secrets

### Deploy to Heroku

```bash
heroku create your-app-name
git push heroku main
heroku config:set MONGODB_URI=<your-mongodb-atlas-uri>
heroku open
```

## File Structure

```
Healthcare/
├── html/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── results.html
│   ├── reports.html
│   ├── profile.html
│   ├── about.html
│   └── contact.html
├── css/
│   ├── index.css
│   ├── login.css
│   ├── dashboard.css
│   ├── upload.css
│   ├── results.css
│   ├── reports.css
│   ├── profile.css
│   ├── about.css
│   └── contact.css
├── js/
│   ├── config.js              # API configuration
│   ├── api-client.js          # API client service
│   ├── index.js
│   ├── login.js               # Authentication
│   ├── dashboard.js
│   ├── upload.js
│   ├── results.js
│   ├── reports.js
│   ├── profile.js
│   ├── about.js
│   └── contact.js
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── health_record.py
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   ├── user_routes.py
│   │   │   ├── health_routes.py
│   │   │   └── report_routes.py
│   │   ├── utils/
│   │   │   └── auth.py
│   │   └── __init__.py
│   ├── config.py
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   └── README.md
└── vercel.json
```

## API Integration Examples

### JavaScript Fetch Examples

**Login:**
```javascript
const response = await APIClient.login('user@example.com', 'password');
console.log(response.token);
```

**Get Profile:**
```javascript
const profile = await APIClient.getUserProfile();
console.log(profile);
```

**Create Record:**
```javascript
const record = await APIClient.createHealthRecord(
    'upload',
    { claimID: '123', patient: 'John', amount: 1000 }
);
```

## Support & Documentation

- **API Docs**: See `/backend/README.md`
- **Frontend Config**: Check `/js/config.js`
- **Database Models**: See `/backend/app/models/`
- **Routes**: See `/backend/app/routes/`

## License

MIT

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

---

**Last Updated**: 2026-07-20
**Version**: 1.0.0
