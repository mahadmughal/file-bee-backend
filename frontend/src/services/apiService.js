import { useAuth } from "../contexts/AuthContext";

const API_BASE_URL = "http://localhost:8000";

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  getToken() {
    // This method will be overwritten with the actual token getter
    return null;
  }

  async fetchWithAuth(endpoint, options = {}) {
    const token = this.getToken();
    const headers = {
      Authorization: `Token ${token?.key}`,
      ...options.headers,
    };
    return this.fetchBase(endpoint, { ...options, headers });
  }

  async fetchWithoutAuth(endpoint, options = {}) {
    return this.fetchBase(endpoint, options);
  }

  async fetchBase(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, options);
      return this.handleResponse(response);
    } catch (error) {
      throw new Error("Network error or server unreachable");
    }
  }

  async handleResponse(response) {
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || `HTTP error! Status: ${response.status}`);
      }
      return data;
    } else {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response;
    }
  }

  async getWithAuth(endpoint) {
    return this.fetchWithAuth(endpoint, { method: "GET" });
  }

  async postWithAuth(endpoint, data) {
    return this.fetchWithAuth(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  }

  async postWithoutAuth(endpoint, data) {
    return this.fetchWithoutAuth(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  }

  async deleteWithAuth(endpoint) {
    return this.fetchWithAuth(endpoint, { method: "DELETE" });
  }

  async postFormDataWithAuth(endpoint, formData) {
    return this.fetchWithAuth(endpoint, {
      method: "POST",
      body: formData,
    });
  }

  async postFormDataWithoutAuth(endpoint, formData) {
    return this.fetchWithoutAuth(endpoint, {
      method: "POST",
      body: formData,
    });
  }

  // Specific API methods
  async fetchSupportedMimetypes() {
    return this.getWithAuth("/target_conversions/");
  }

  async convertFile(file, targetMimetype) {
    const formData = new FormData();
    formData.append("original_file", file);
    formData.append("converted_mimetype", targetMimetype);
    return this.postFormDataWithAuth("/", formData);
  }

  async resetPassword(passwordResetToken, newPassword, confirmPassword) {
    const formData = {
      token: passwordResetToken,
      password: newPassword,
      confirm_password: confirmPassword,
    };
    return this.postWithoutAuth("/api/user/reset_password/", formData);
  }

  async updateUserProfile(userData) {
    return this.postWithAuth("/api/user/profile", userData);
  }

  async deleteAccount() {
    return this.deleteWithAuth("/api/user/delete_account");
  }
}

export const apiService = new ApiService();

export const useApiService = () => {
  const { token } = useAuth();
  apiService.getToken = () => token;
  return apiService;
};
