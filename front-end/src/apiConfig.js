// apiConfig.js

export const API_CONFIG = {
    BASE_URL: 'http://localhost:8800',
    ENDPOINTS: {
        FACE_DETECTION: '/face_recognition/detect',
        FACE_COMPARISON: '/face_recognition/compare',
        FACE_SEARCH: '/face_recognition/search_folder',
        LIVENESS: '/face_recognition/liveness_detection',

        REGISTER: '/auth/register',
        LOGIN: '/auth/login',
        REGISTER_FACE: '/auth/register_face',
        LOGIN_FACE: '/auth/login_face',
    }
};
