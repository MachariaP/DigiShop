import { create } from 'zustand';
import { mountStoreDevtool } from 'simple-zustand-devtools';

const useAuthStore = create((set, get) => ({
    alluserData: null,
    loadings: false,

    user: () => ({
        user_id: get().alluserData?.user_id || null,
        usernames: get().alluserData?.usernames || null,
    }),

    setUser: (user) => set({ alluserData: user }),
    setLoading: (loadings) => set({ loadings }),
    setLoggedIn: () => get().alluserData !== null,
}));

if (import.meta.env.DEV) {
    mountStoreDevtool('Store', useAuthStore);
}

export { useAuthStore };