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
      hobbies: [''],
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
        hobbies: [''],
      }; // Reset to the initial state
    },
  },
});
