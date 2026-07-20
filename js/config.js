// API Configuration
const API_BASE_URL = localStorage.getItem('apiUrl') || 'http://localhost:5000/api';

const API_ENDPOINTS = {
    // Authentication
    AUTH_REGISTER: `${API_BASE_URL}/auth/register`,
    AUTH_LOGIN: `${API_BASE_URL}/auth/login`,
    AUTH_VERIFY: `${API_BASE_URL}/auth/verify`,
    
    // User
    USER_PROFILE: `${API_BASE_URL}/user/profile`,
    USER_DELETE: (userId) => `${API_BASE_URL}/user/${userId}`,
    
    // Health Records
    HEALTH_RECORDS: `${API_BASE_URL}/health/records`,
    HEALTH_RECORD: (recordId) => `${API_BASE_URL}/health/records/${recordId}`,
    
    // Reports
    REPORTS: `${API_BASE_URL}/reports`,
    REPORT: (reportId) => `${API_BASE_URL}/reports/${reportId}`,
    
    // Health Check
    HEALTH_CHECK: `${API_BASE_URL.replace('/api', '')}/api/health`
};

// Storage Keys
const STORAGE_KEYS = {
    TOKEN: 'authToken',
    USER: 'userProfile',
    API_URL: 'apiUrl'
};

// Helper to get auth token from localStorage
function getAuthToken() {
    return localStorage.getItem(STORAGE_KEYS.TOKEN);
}

// Helper to get auth headers
function getAuthHeaders() {
    const token = getAuthToken();
    return {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
}

// Helper to check if user is authenticated
function isAuthenticated() {
    return !!getAuthToken();
}

// Helper to get stored user profile
function getUserProfile() {
    const profile = localStorage.getItem(STORAGE_KEYS.USER);
    return profile ? JSON.parse(profile) : null;
}
