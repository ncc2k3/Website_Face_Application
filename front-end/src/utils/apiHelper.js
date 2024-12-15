// apiHelper.js

import axios from 'axios';
import { API_CONFIG } from 'apiConfig';

/**
 * Gửi yêu cầu POST đến API.
 * 
 * @param {string} endpoint - Endpoint của API cần gọi.
 * @param {Object|FormData} data - Dữ liệu cần gửi (có thể là JSON hoặc FormData).
 * @param {boolean} isFormData - Cờ xác định liệu dữ liệu có phải là FormData hay không.
 * @returns {Promise} - Promise trả về kết quả từ API.
 */
export const callApi = async (endpoint, data, isFormData = false) => {
    try {
        const headers = isFormData
            ? { 'Content-Type': 'multipart/form-data' }  // Sử dụng multipart/form-data khi cần
            : { 'Content-Type': 'application/json' };  // Mặc định là JSON

        const response = await axios.post(`${API_CONFIG.BASE_URL}${endpoint}`, data, { headers });
        return response;
    } catch (error) {
        console.error("API Error: ", error);
        throw error;  // Xử lý lỗi tùy ý ở đây
    }
};
