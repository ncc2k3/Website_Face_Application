// apiHelper.js

import axios from 'axios';
import { API_CONFIG } from 'apiConfig';

/**
 * Gửi yêu cầu POST đến API.
 * 
 * @param {string} endpoint - Endpoint của API cần gọi.
 * @param {FormData} formData - Dữ liệu FormData cần gửi.
 * @returns {Promise} - Promise trả về kết quả từ API.
 */
export const callApi = async (endpoint, formData) => {
    try {
        const response = await axios.post(`${API_CONFIG.BASE_URL}${endpoint}`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response;
    } catch (error) {
        console.error("API Error: ", error);
        throw error;  // Bạn có thể thêm xử lý lỗi phù hợp
    }
};
