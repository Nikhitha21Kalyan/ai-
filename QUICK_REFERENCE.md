# Quick Reference Card

## 🚀 Start Application

### Windows
```bash
cd backend
START_WINDOWS.bat
```

### Linux/Mac
```bash
cd backend
./START.sh
```

## 📍 Access Points

| What | Where |
|------|-------|
| Frontend | http://localhost:5000 |
| API | http://localhost:5000/api |
| API Health | http://localhost:5000/api/health |

## 🔑 Test Credentials

```
Email: test@example.com
Password: password123
```

Or register a new account at the login page.

## 📁 Important Files

### Frontend
- `js/config.js` - API configuration
- `js/api-client.js` - API client service
- `html/index.html` - Home page
- `html/login.html` - Login/signup page

### Backend
- `backend/app.py` - Main entry point
- `backend/config.py` - Configuration
- `backend/.env` - Environment variables
- `backend/requirements.txt` - Dependencies

## 🔧 Configure API Endpoint

Edit `js/config.js` to change API URL:
```javascript
const API_BASE_URL = 'http://your-api-url:port/api'
```

Or in browser console:
```javascript
localStorage.setItem('apiUrl', 'http://your-api-url:port/api')
```

## 📋 Common Tasks

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Start MongoDB
```bash
mongod
```

### Run Backend Only
```bash
cd backend
python app.py
```

### Check if Backend Running
```bash
curl http://localhost:5000/api/health
```

### Clear Database
```bash
mongo
use healthcare
db.dropDatabase()
```

## 🔗 API Endpoints Quick Reference

### Auth
```
POST /api/auth/register
POST /api/auth/login
GET /api/auth/verify
```

### User
```
GET /api/user/profile
PUT /api/user/profile
DELETE /api/user/{id}
```

### Health Records
```
GET /api/health/records
POST /api/health/records
GET /api/health/records/{id}
PUT /api/health/records/{id}
DELETE /api/health/records/{id}
```

### Reports
```
GET /api/reports
POST /api/reports
GET /api/reports/{id}
DELETE /api/reports/{id}
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 in use | `lsof -i :5000` then kill process |
| MongoDB not running | `mongod` in separate terminal |
| Module not found | `pip install -r requirements.txt` |
| Token expired | Logout and login again |
| CORS error | Check API URL in config.js |

## 📝 Sample API Calls

### Login with cURL
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Get Profile with Token
```bash
curl -X GET http://localhost:5000/api/user/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔐 Environment Setup

```bash
# Create .env from template
cp backend/.env.example backend/.env

# Edit backend/.env
# Change:
# - SECRET_KEY
# - JWT_SECRET
# - MONGODB_URI (if using remote)
```

## 📊 Project Structure

```
Healthcare/
├── html/           # Frontend HTML
├── css/            # Frontend Styles
├── js/             # Frontend JavaScript
│   ├── config.js          ← API config
│   ├── api-client.js      ← API service
│   └── *.js               ← Page logic
├── backend/        # Backend API
│   ├── app/
│   ├── config.py
│   ├── app.py
│   └── requirements.txt
└── README.md       # Project docs
```

## 🧪 Testing Workflow

1. Register account
2. Login
3. Go to Upload page
4. Upload sample CSV
5. View results
6. Check reports
7. Update profile
8. Logout

## 💡 Tips & Tricks

### Debug API Calls
```javascript
// In browser console
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(console.log)
```

### Check Token
```javascript
// In browser console
localStorage.getItem('authToken')
```

### Clear All Data
```javascript
// In browser console
localStorage.clear()
```

### Change API at Runtime
```javascript
localStorage.setItem('apiUrl', 'http://new-url:5000/api')
location.reload()
```

## 📞 Support Resources

- **Setup Issues** → See SETUP_GUIDE.md
- **Development** → See DEVELOPMENT_GUIDE.md
- **API Documentation** → See backend/README.md
- **Full Summary** → See INTEGRATION_SUMMARY.md

## ✅ Verification Checklist

- [ ] Backend running on port 5000
- [ ] MongoDB connected
- [ ] Frontend accessible at localhost:5000
- [ ] Can register new account
- [ ] Can login with credentials
- [ ] Profile loads correctly
- [ ] Can upload CSV files
- [ ] Results display properly
- [ ] Reports generate
- [ ] Logout works

---

**Quick Help**: If stuck, check the documentation files:
1. SETUP_GUIDE.md - Installation issues
2. DEVELOPMENT_GUIDE.md - Testing & debugging
3. backend/README.md - API documentation
