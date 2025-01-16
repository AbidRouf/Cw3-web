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
        },
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
            };
        },
    },
});

export const useCSRFStore = defineStore('csrf', {
    state: () => ({
        csrfToken: '',
    }),
    actions: {
        setCSRFToken(token: string) {
            this.csrfToken = token;
        },

        fetchCSRFToken() {
            const token =
                document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
            if (token) {
                this.csrfToken = token;
            } else {
                console.error('Failed to fetch CSRF token.');
            }
        },
    },
});