import axios from 'axios';

// Create an Axios instance with custom configuration
const apiInstance = axios.create({
    baseURL: 'https://127.0.0.1:8000/api/v1/', // Base URL for the API
    timeout: 5000, // Request timeout in milliseconds
    headers: {
        'Content-Type': 'application/json', // Content type for the requests
        'Accept': 'application/json', // Accept header for the responses
    },
});

export default apiInstance;