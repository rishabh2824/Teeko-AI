import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:8000'; // Default to localhost

const axiosInstance = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000, // 10 seconds timeout
});

// Handle API errors
const handleApiError = (error) => {
    console.error('API Error:', error);
    const errorMessage = error.response?.data?.detail || 'An error occurred while communicating with the server.';
    return new Error(errorMessage);
};

// Logging helper
const log = (message, data) => {
    if (process.env.REACT_APP_DEBUG === 'true') {
        console.log(message, data);
    }
};

// API Methods
export const getGameState = async () => {
    try {
        const response = await axiosInstance.get('/');
        log('Response from GET /:', response.data);
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};

export const aiMove = async () => {
    try {
        const response = await axiosInstance.post('/ai-move/');
        console.log('Response from POST /ai-move/:', response.data);
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};

export const opponentMove = async (move) => {
    try {
        const response = await axiosInstance.post('/opponent-move/', { move });
        log('Response from POST /opponent-move/:', response.data);
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};

export const resetGame = async () => {
    try {
        const response = await axiosInstance.post('/reset/');
        log('Response from POST /reset/:', response.data);
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};
