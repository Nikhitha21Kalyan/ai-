# Development & Testing Guide

## Quick Start

### Windows
1. Open PowerShell in the `backend` folder
2. Run: `.\START_WINDOWS.bat`
3. Open browser: `http://localhost:5000`

### Linux/Mac
1. Open terminal in the `backend` folder
2. Run: `chmod +x START.sh && ./START.sh`
3. Open browser: `http://localhost:5000`

## Manual Setup

### Prerequisites
- Python 3.8+
- MongoDB 4.0+
- Git (optional)

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```
FLASK_ENV=development
MONGODB_URI=mongodb://localhost:27017/healthcare
SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
```

### Step 3: Start MongoDB

```bash
mongod
```

In another terminal:

### Step 4: Start Backend

```bash
cd backend
python app.py
```

### Step 5: Access Application

Open browser: `http://localhost:5000`

## Testing the Application

### Test Case 1: User Registration

1. Navigate to login page
2. Click "Sign Up" tab
3. Fill in:
   - Full Name: John Doe
   - Email: john@example.com
   - Username: johndoe
   - Password: password123
4. Click "Create Account"
5. Expected: Account created, redirected to login

### Test Case 2: User Login

1. Fill in:
   - Email: john@example.com
   - Password: password123
2. Click "Login"
3. Expected: Redirected to dashboard

### Test Case 3: View Profile

1. Login successfully
2. Click "Profile" link
3. Expected: Profile information displayed

### Test Case 4: Upload CSV Data

1. Create sample CSV file (`test.csv`):
   ```csv
   ClaimID,Patient,Amount,Provider,Diagnosis
   C001,John Smith,5000,Hospital A,Pneumonia
   C002,Jane Doe,10000,Hospital B,Cardiac
   C003,Bob Wilson,3000,Clinic C,Fracture
   ```

2. Go to "Upload Claims" page
3. Choose `test.csv`
4. Click "Detect Fraud"
5. Expected: File uploaded, results displayed

### Test Case 5: View Results

1. After uploading data
2. Check "Detection Results" page
3. Expected: Claims table with predictions

### Test Case 6: View Reports

1. Go to "Reports" page
2. Expected: Summary cards and report content

### Test Case 7: Logout

1. Click "Logout" button
2. Expected: Redirected to login page

## API Testing with cURL

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Response will include `token`. Use this token for authenticated requests.

### Get Profile (Authenticated)
```bash
curl -X GET http://localhost:5000/api/user/profile \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

### Create Health Record
```bash
curl -X POST http://localhost:5000/api/health/records \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "record_type": "upload",
    "data": {
      "claim_id": "C001",
      "patient": "John",
      "amount": 5000
    }
  }'
```

### Get Health Records
```bash
curl -X GET http://localhost:5000/api/health/records \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

## Debugging

### Check Backend Status

Open browser: `http://localhost:5000/api/health`

Expected response:
```json
{"status": "API is running"}
```

### MongoDB Connection Issues

1. Check if MongoDB is running:
   ```bash
   mongod --version
   ```

2. Test connection:
   ```bash
   mongo mongodb://localhost:27017
   ```

3. View MongoDB logs:
   ```bash
   mongod --logpath /path/to/log.txt
   ```

### Frontend Console Errors

1. Open browser Developer Tools (F12)
2. Go to "Console" tab
3. Check for errors
4. Look for API connection issues

### Backend Debug Mode

Edit `backend/.env`:
```
FLASK_DEBUG=True
```

This enables:
- Auto-reload on code changes
- Detailed error messages
- Debugger interface

### Check API Connectivity

In browser console:
```javascript
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

## Common Issues & Solutions

### Issue: "Connection refused" error

**Solution**: MongoDB not running
```bash
mongod
```

### Issue: Port 5000 already in use

**Solution**: Use different port
```bash
# In backend/app.py
app.run(port=5001)
```

### Issue: CORS errors

**Solution**: Backend CORS is configured. Check if:
1. API endpoint is correct in `js/config.js`
2. Backend is running
3. Request headers are correct

### Issue: Login fails with "Invalid token"

**Solution**: 
1. Clear browser localStorage
2. Logout and login again
3. Check if JWT_SECRET is consistent

### Issue: "ModuleNotFoundError" when running Python

**Solution**: Activate virtual environment
```bash
# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

## Performance Testing

### Load Testing with Apache Bench

```bash
ab -n 100 -c 10 http://localhost:5000/api/health
```

### Memory Profiling

```bash
pip install memory-profiler
python -m memory_profiler app.py
```

## Security Testing

### Test CSRF Protection
- Configured at application level
- Ensure tokens are validated

### Test SQL Injection
- Using MongoDB, not vulnerable to SQL injection
- Validate all inputs in routes

### Test XSS Vulnerabilities
- Frontend sanitizes inputs
- MongoDB escapes dangerous characters

## Performance Optimization

### Database Indexing

Add to `backend/app/models/user.py`:
```python
# Create index on email
self.collection.create_index("email", unique=True)
```

### Caching

Add to `backend/config.py`:
```python
CACHE_TYPE = "simple"
CACHE_DEFAULT_TIMEOUT = 300
```

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/
```

## Deployment Checklist

- [ ] Update `.env` with production values
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS/SSL
- [ ] Configure database backups
- [ ] Set up monitoring
- [ ] Enable logging
- [ ] Configure rate limiting
- [ ] Update CORS settings
- [ ] Run security audit
- [ ] Test all workflows

## Support Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Docs](https://docs.mongodb.com/)
- [JWT Documentation](https://jwt.io/)
- [Python Requests](https://requests.readthedocs.io/)

---

**Last Updated**: 2026-07-20
