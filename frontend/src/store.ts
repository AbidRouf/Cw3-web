import { defineStore } from 'pinia';
interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    dob: Date;
    password: string;
    hobbies: Hobby[];
    friends: User[];
}
interface Hobby {
    id: number,
    name: string
}
export const useUserStore = defineStore('user', {
    state: (): { user: User } => ({
        user: {
            id: -1,
            username: '',
            first_name: '',
            last_name: '',
            email: '',
            dob: new Date(),
            password: '',
            hobbies: [],
            friends: []
        }, // Initial state
    }),
    actions: {
        setUser(userData: any) {
            this.user = userData;
        },
        clearUser() {
            this.user = {
                id: -1,
                username: '',
                first_name: '',
                last_name: '',
                email: '',
                dob: new Date(),
                password: '',
                hobbies: [],
                friends: []
            }; // Reset to the initial state
        },
    },
});

export const useCSRFStore = defineStore('csrf', {
    state: () => ({
        csrfToken: '', // Initialize token as empty
    }),
    actions: {
        // Set CSRF token manually
        setCSRFToken(token: string) {
            this.csrfToken = token;
        },

        // Dynamically fetch the CSRF token
        fetchCSRFToken() {
            const token =
                document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
            if (token) {
                this.csrfToken = token;
                // console.log('CSRF Token fetched and stored:', this.csrfToken);
            } else {
                console.error('Failed to fetch CSRF token.');
            }
        },
    },
});