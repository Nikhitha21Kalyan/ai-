// API Service Client
class APIClient {
    static async request(url, options = {}) {
        const defaultOptions = {
            headers: getAuthHeaders(),
            ...options
        };

        try {
            const response = await fetch(url, defaultOptions);
            const data = await response.json();

            if (!response.ok) {
                throw {
                    status: response.status,
                    message: data.message || 'API Error',
                    data
                };
            }

            return data;
        } catch (error) {
            if (error.status === 401) {
                // Unauthorized - clear auth and redirect to login
                localStorage.clear();
                window.location.href = 'login.html';
            }
            throw error;
        }
    }

    // Authentication Methods
    static async register(email, password, firstName, lastName, age, gender) {
        return this.request(API_ENDPOINTS.AUTH_REGISTER, {
            method: 'POST',
            body: JSON.stringify({
                email,
                password,
                first_name: firstName,
                last_name: lastName,
                age,
                gender
            })
        });
    }

    static async login(email, password) {
        const response = await this.request(API_ENDPOINTS.AUTH_LOGIN, {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        // Store token and user info
        if (response.token) {
            localStorage.setItem(STORAGE_KEYS.TOKEN, response.token);
            localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.user));
        }

        return response;
    }

    static async verifyToken() {
        try {
            const response = await this.request(API_ENDPOINTS.AUTH_VERIFY);
            return response.valid;
        } catch (error) {
            return false;
        }
    }

    static logout() {
        localStorage.removeItem(STORAGE_KEYS.TOKEN);
        localStorage.removeItem(STORAGE_KEYS.USER);
    }

    // User Methods
    static async getUserProfile() {
        return this.request(API_ENDPOINTS.USER_PROFILE);
    }

    static async updateUserProfile(data) {
        return this.request(API_ENDPOINTS.USER_PROFILE, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deleteUserAccount(userId) {
        return this.request(API_ENDPOINTS.USER_DELETE(userId), {
            method: 'DELETE'
        });
    }

    // Health Records Methods
    static async getHealthRecords(recordType = null) {
        const url = recordType 
            ? `${API_ENDPOINTS.HEALTH_RECORDS}?type=${recordType}`
            : API_ENDPOINTS.HEALTH_RECORDS;
        return this.request(url);
    }

    static async createHealthRecord(recordType, data, filePath = null) {
        return this.request(API_ENDPOINTS.HEALTH_RECORDS, {
            method: 'POST',
            body: JSON.stringify({
                record_type: recordType,
                data,
                file_path: filePath
            })
        });
    }

    static async getHealthRecord(recordId) {
        return this.request(API_ENDPOINTS.HEALTH_RECORD(recordId));
    }

    static async updateHealthRecord(recordId, data) {
        return this.request(API_ENDPOINTS.HEALTH_RECORD(recordId), {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deleteHealthRecord(recordId) {
        return this.request(API_ENDPOINTS.HEALTH_RECORD(recordId), {
            method: 'DELETE'
        });
    }

    // Reports Methods
    static async getReports() {
        return this.request(API_ENDPOINTS.REPORTS);
    }

    static async createReport(title, content, doctor, diagnosis, medication, notes) {
        return this.request(API_ENDPOINTS.REPORTS, {
            method: 'POST',
            body: JSON.stringify({
                title,
                content,
                doctor,
                diagnosis,
                medication,
                notes
            })
        });
    }

    static async getReport(reportId) {
        return this.request(API_ENDPOINTS.REPORT(reportId));
    }

    static async deleteReport(reportId) {
        return this.request(API_ENDPOINTS.REPORT(reportId), {
            method: 'DELETE'
        });
    }

    // Check API Health
    static async checkAPIHealth() {
        try {
            const response = await fetch(API_ENDPOINTS.HEALTH_CHECK);
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}
