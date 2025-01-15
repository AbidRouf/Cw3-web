import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: {
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      dob: null,
      password: '',
      confirmPassword: '',
      hobbies: ['N/A'],
    }, // Initial state
  }),
  actions: {
    setUser(userData: any) {
      this.user = userData;
    },
    clearUser() {
      this.user = {
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        dob: null,
        password: '',
        confirmPassword: '',
        hobbies: ['N/A'],
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