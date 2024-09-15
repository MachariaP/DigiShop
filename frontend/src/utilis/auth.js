import { useAuthStore } from '../store/auth'; // Import the Zustand store
import axios from './axios'; // Import the Axios instance
import jwt_decode from 'jwt-decode'; // Import JWT decode library
import cookie from 'js-cookie'; // Import js-cookie for cookie management

// Function to handle user login
export const login = async (email, password) => {
    try {
        // Make a POST request to the login endpoint with email and password
        const { data, status } = await axios.post('user/token/', {
            email,
            password,
        });

        if (status === 200) {
            // Decode the JWT token to get user information
            const decoded = jwt_decode(data.access);

            // Set user data in the store
            useAuthStore.getState().setUser(decoded);

            // Set JWT tokens in cookies
            cookie.set('access_token', data.access);
            cookie.set('refresh_token', data.refresh);

            // Alert - Sign in Successfully
            // alert('Sign in Successfully');
        }

        // Return the response data if login is successful
        return { data, error: null };
    } catch (error) {
        // Return the error message if login fails
        return {
            data: null,
            error: error.response?.data?.detail || 'Something went wrong',
        };
    }
};

// Function to handle user registration
export const register = async (full_name, email, phone, password, password2) => {
    try {
        // Make a POST request to the register endpoint with user details
        const { data } = await axios.post('user/register/', {
            full_name,
            email,
            phone,
            password,
            password2,
        });

        // Automatically log in the user after successful registration
        await login(email, password);

        // Alert - Signed up successfully
        alert('Signed up successfully');

        // Return the response data if registration is successful
        return { data, error: null };
    } catch (error) {
        // Return the error message if registration fails
        return {
            data: null,
            error: error.response?.data?.detail || 'Something went wrong',
        };
    }
};

// Function to handle user logout
export const logout = () => {
    // Remove JWT tokens from cookies
    cookie.remove('access_token');
    cookie.remove('refresh_token');

    // Clear user data from the store
    useAuthStore.getState().setUser(null);

    // Alert - Signed out successfully
    // alert('Signed out successfully');
};

export const setUser = async () => {
    const accessToken = cookie.get("access_token");
    const refreshToken = cookie.get("refresh_token");

    if (!accessToken || !refreshToken) {
        return;
    }

    if (isAccessTokenExpired(accessToken)){
        const response = await getRefreshToken(refreshToken);
        setAuthUser(response.access, response.refresh);
    } else {
        setAuthUser(accessToken, refreshToken);
    }
};

export const setAuthUser = (access_token, refresh_token) => {
    cookie.set('access_token', access_token, {
        expires: 1,
        secure: true
    });

    cookie.set('refresh_token', refresh_token, {
        expires: 7,
        secure: true
    });

    const user = jwt_decode(access_token) ?? null;

    if (user){
        useAuthStore.getState().setUser(user);
    }
    useAuthStore.getState().setLoading(false);
};

export const getRefreshToken = async () => {
    const refresh_token = cookie.get('refresh_token');
    const response = await axios.post('user/token/refresh/', {
            refresh: refresh_token,
        });

    return response.data;
};

// Function to check if access token is expired
export const isAccessTokenExpired = (accessToken) => {
    try {
        const decodeToken = jwt_decode(accessToken);
        return decodeToken.exp < Date.now() / 1000;
    } catch (error) {
        console.error(error);
        return true;
    }
};