import axios from "axios";
import { isAccessTokenExpired, setAuthUser, getRefreshToken } from "./auth";
import { BASE_URL } from "./constants";
import cookies from "js-cookie";

// Function to create an axios instance with token handling
const useAxios = async () => {
    // Retrieve tokens from cookies
    const access_token = cookies.get("access_token");
    const refresh_token = cookies.get("refresh_token");

    // Create an axios instance with base URL and authorization header
    const axiosInstance = axios.create({
        baseURL: BASE_URL,
        headers: {
            Authorization: `Bearer ${access_token}`
        }
    });

    // Add a request interceptor to handle token expiration
    axiosInstance.interceptors.request.use(async (req) => {
        // Check if the access token is expired
        if (!isAccessTokenExpired(access_token)) {
            return req; // If not expired, proceed with the request
        }

        // If expired, get a new access token using the refresh token
        const response = await getRefreshToken(refresh_token);
        // Update the auth user with new tokens
        setAuthUser(response.access, response.refresh);

        // Update the request's authorization header with the new access token
        req.headers.Authorization = `Bearer ${response.access}`;
        return req; // Proceed with the updated request
    });

    return axiosInstance; // Return the configured axios instance
};

export default apiInstance  // Return the configured axios instance