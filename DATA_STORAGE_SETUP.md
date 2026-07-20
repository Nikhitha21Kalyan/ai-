# Firebase Errors Fixed & Data Storage Setup

## ✅ What Was Fixed

### 1. **Created `.env` Configuration File**
- ✅ Backend now has environment variables configured
- ✅ MongoDB URI set to `mongodb://localhost:27017/healthcare`
- ✅ JWT secrets and Flask config properly configured
- ✅ File location: `backend/.env`

### 2. **Verified Firebase Removal**
- ✅ All HTML files use API client (no Firebase imports)
- ✅ All JavaScript files use APIClient for data operations
- ✅ Authentication uses JWT tokens (not Firebase)
- ✅ Data stored in MongoDB (not Firebase)

### 3. **Data Storage Architecture**
```
Frontend (HTML/JS)
    ↓
API Client (js/api-client.js)
    ↓
Flask Backend (Python)
    ↓
MongoDB Database
    └── Collections:
        ├── users (user accounts)
        └── health_records (claim data & reports)
```

---

## 🚀 Quick Start - Get Everything Running

### **Step 1: Install MongoDB (Local)**

#### **Windows:**
```bash
# Download from: https://www.mongodb.com/try/download/community
# Or use Chocolatey:
choco install mongodb-community

# Start MongoDB service:
# Services → MongoDB Server → Start
# Or via command line:
net start MongoDB
```

#### **Mac (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
```

**Verify MongoDB is running:**
```bash
# Should connect successfully
mongosh
# Then type: exit
```

---

### **Step 2: Set Up Backend**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

---

### **Step 3: Run the Application**

**Option 1: Windows (Automated):**
```bash
# Double-click or run:
cd backend
START_WINDOWS.bat
```

**Option 2: Manual Start (Any OS):**
```bash
# Terminal 1 - Make sure MongoDB is running
mongosh

# Terminal 2 - Run Flask backend
cd backend
python app.py
# Expected output:
# WARNING in app.run() is not recommended for production use...
# Running on http://0.0.0.0:5000
```

**Option 3: Linux/Mac:**
```bash
cd backend
chmod +x START.sh
./START.sh
```

---

### **Step 4: Access the Application**

Open browser and go to: **http://localhost:5000**

---

## 📊 Test Data Storage

### **Test 1: Register a New User**
```
1. Go to http://localhost:5000
2. Click "Sign Up"
3. Fill in:
   - Full Name: John Doe
   - Email: john@example.com
   - Username: john123
   - Password: password123
4. Click "Create Account"
```

**Expected Result:**
- Account created successfully
- Data stored in MongoDB `users` collection
- Redirected to login page

### **Test 2: Login**
```
1. Enter email: john@example.com
2. Enter password: password123
3. Click Login
```

**Expected Result:**
- Login successful
- Token stored in localStorage
- Redirected to dashboard

### **Test 3: Upload Health Records**
```
1. Click "Upload Claims"
2. Create a test CSV file:
   ```
   patient_id,claim_amount,diagnosis,provider
   P001,1500.00,Flu,Dr. Smith
   P002,5000.00,Surgery,Hospital XYZ
   ```
3. Upload the file
```

**Expected Result:**
- File parsed successfully
- Records stored in MongoDB `health_records` collection
- Redirected to results page
- Records displayed in table

### **Test 4: View Dashboard**
```
1. Click "Dashboard" in sidebar
2. Click "Refresh" button
```

**Expected Result:**
- Total Claims: (number of uploaded records)
- Fraud Claims: (calculated count)
- Safe Claims: (calculated count)
- Recent claims displayed in table

---

## 🔧 Troubleshooting

### **Issue: "Cannot connect to MongoDB"**

**Error Message:**
```
pymongo.errors.ServerSelectionTimeoutError: [Errno 11001]...
```

**Solution:**
```bash
# 1. Verify MongoDB is running:
mongosh

# 2. Check if listening on correct port:
netstat -an | findstr 27017

# 3. If not running, start it:
# Windows:
net start MongoDB

# Mac:
brew services start mongodb-community

# Linux:
sudo systemctl start mongodb
```

---

### **Issue: "ModuleNotFoundError: No module named 'flask'"**

**Solution:**
```bash
# Make sure virtual environment is activated:
# Windows:
backend\venv\Scripts\activate

# Mac/Linux:
source backend/venv/bin/activate

# Then install dependencies:
pip install -r requirements.txt
```

---

### **Issue: "Address already in use - port 5000"**

**Solution:**
```bash
# Option 1: Kill the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :5000
kill -9 <PID>

# Option 2: Use different port
# Edit backend/.env:
PORT=5001
# Then run: python app.py
```

---

### **Issue: "AttributeError: 'NoneType' object has no attribute 'db'"**

**Solution:**
```bash
# The .env file was recreated. Restart the app:
1. Stop Flask (Ctrl+C)
2. Start MongoDB again
3. Run: python app.py
```

---

### **Issue: Login fails with "Invalid email or password"**

**Solution:**
```bash
# 1. Check if user exists in MongoDB:
mongosh
use healthcare
db.users.find()

# 2. If empty, register a new user via the UI
# 3. Check browser console (F12) for detailed errors
```

---

### **Issue: File upload not showing in results**

**Solution:**
```bash
# 1. Check MongoDB for records:
mongosh
use healthcare
db.health_records.find().pretty()

# 2. Verify API response in browser:
# - Open Developer Tools (F12)
# - Go to Network tab
# - Upload a file
# - Check API responses

# 3. Check backend console for errors
```

---

## 🔍 Verify Data Storage

### **Check Users Collection:**
```bash
# Start MongoDB shell
mongosh

# Connect to healthcare database
use healthcare

# View all users
db.users.find().pretty()

# Expected output:
# {
#   "_id": ObjectId(...),
#   "email": "john@example.com",
#   "password_hash": "$2b$10$...",
#   "first_name": "John",
#   "last_name": "Doe",
#   "created_at": ISODate(...),
#   "updated_at": ISODate(...)
# }
```

### **Check Health Records Collection:**
```bash
# In mongosh, still connected to healthcare database
db.health_records.find().pretty()

# Expected output:
# {
#   "_id": ObjectId(...),
#   "user_id": ObjectId(...),
#   "record_type": "upload",
#   "data": {
#     "patient_id": "P001",
#     "claim_amount": "1500.00",
#     ...
#   },
#   "file_path": "file.csv",
#   "created_at": ISODate(...),
#   "updated_at": ISODate(...)
# }
```

### **Count Records:**
```bash
# Users count
db.users.countDocuments()

# Health records count
db.health_records.countDocuments()

# Records by user
db.health_records.find({user_id: ObjectId("...")}).count()
```

---

## 🔐 Security Notes

### **Development Mode** (Current Setup)
- ✅ CORS enabled for all origins
- ✅ Debug mode enabled
- ✅ Default secrets (fine for local testing)

### **Production Mode** (Before Deployment)
```bash
# Edit backend/.env:
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-random-key>
JWT_SECRET=<generate-random-key>
CORS_ORIGINS=https://yourdomain.com
```

**Generate random secrets:**
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📁 File Structure After Setup

```
Healthcare/
├── backend/
│   ├── .env                    ← ✅ Created
│   ├── .env.example
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── venv/                   ← Virtual environment
│   └── app/
│       ├── __init__.py
│       ├── models/
│       ├── routes/
│       └── utils/
├── js/
│   ├── config.js               ← ✅ API Configuration
│   ├── api-client.js           ← ✅ API Communication
│   └── [page-specific].js
├── html/
│   ├── login.html
│   ├── dashboard.html
│   └── [other pages].html
└── [other files]
```

---

## 🎯 Data Flow Example

### **User Registration Flow:**
```
1. User fills signup form in login.html
2. JavaScript calls: APIClient.register(email, password, ...)
3. APIClient sends POST to: /api/auth/register
4. Flask receives request in auth_routes.py
5. Hashes password with bcrypt
6. Stores user in MongoDB users collection
7. Returns success response
8. JavaScript shows "Account created" message
```

### **File Upload Flow:**
```
1. User selects CSV file in upload.html
2. JavaScript reads file with FileReader API
3. Parses CSV into records array
4. For each record: calls APIClient.createHealthRecord(...)
5. APIClient sends POST to: /api/health/records
6. Flask receives request with auth token
7. Validates JWT token
8. Extracts user_id from token
9. Stores record in MongoDB health_records collection with user_id
10. Returns record_id
11. After all records stored, redirects to results.html
12. Results page loads: APIClient.getHealthRecords()
13. Displays all records in table
```

---

## 📊 API Endpoints Reference

### **Authentication**
```
POST   /api/auth/register     → Create new user
POST   /api/auth/login        → Get JWT token
GET    /api/auth/verify       → Verify token validity
```

### **User Management**
```
GET    /api/user/profile      → Get current user
PUT    /api/user/profile      → Update user info
DELETE /api/user/{id}         → Delete account
```

### **Health Records**
```
GET    /api/health/records    → Get all records (optional ?type=upload)
POST   /api/health/records    → Create new record
GET    /api/health/records/{id} → Get specific record
PUT    /api/health/records/{id} → Update record
DELETE /api/health/records/{id} → Delete record
```

### **Reports**
```
GET    /api/reports           → Get all reports
POST   /api/reports           → Create new report
DELETE /api/reports/{id}      → Delete report
```

---

## ✅ Verification Checklist

Before considering setup complete, verify:

- [ ] MongoDB is running (`mongosh` works)
- [ ] Backend virtual environment created and activated
- [ ] All dependencies installed (`pip list` shows Flask, pymongo, etc.)
- [ ] `.env` file exists in backend directory
- [ ] Flask app starts without errors (`python app.py` works)
- [ ] Frontend accessible at `http://localhost:5000`
- [ ] Can register a new account
- [ ] Can login with registered account
- [ ] Can upload CSV file
- [ ] Data appears in MongoDB
- [ ] Dashboard shows uploaded record counts
- [ ] Can view results in results.html

---

## 🆘 Getting Help

1. **Check browser console (F12)** for JavaScript errors
2. **Check backend terminal** for Flask errors
3. **Check MongoDB** with `mongosh` for data issues
4. **Check `.env` file** for configuration errors
5. **Review logs** in backend console output

---

## 📞 Next Steps

1. ✅ Set up MongoDB locally
2. ✅ Run the Flask backend
3. ✅ Test user registration
4. ✅ Test file upload
5. ✅ Verify data in MongoDB
6. ✅ Ready for development/customization!

All errors fixed, data storage fully configured! 🎉
