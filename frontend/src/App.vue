<template>
    <div id="app">
        <header v-if="showHeader" class="flex flex-col items-center justify-center h-20 mt-24">
            <h1 class="text-red-500 text-center">Hobbies App</h1>

            <!-- Navigation Links -->
            <router-link v-if="isAuthenticated" to="/profile/" class="mt-2">
                <button class="bg-blue-500 text-white py-2 px-4 rounded">Manage Profile</button>
            </router-link>
            <router-link v-if="isAuthenticated" to="/users/" class="mt-2">
                <button class="bg-blue-500 text-white py-2 px-4 rounded">See Users</button>
            </router-link>

            <!-- Conditional Login/Logout Links -->
            <div class="flex flex-col items-center">
                <a v-if="!isAuthenticated" href="/login/"
                    class="px-4 py-2 mt-2 bg-blue-500 text-white rounded">Login</a>
                <a v-if="!isAuthenticated" href="/signup/" class="px-4 py-2 mt-2 bg-blue-500 text-white rounded">Sign
                    Up</a>


                <button v-if="isAuthenticated" @click="logout" class="px-4 py-2 mt-2 bg-red-500 text-white rounded">
                    Logout
                </button>
            </div>
        </header>

        <router-view />
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useUserStore } from './store';

export default defineComponent({
    name: 'App',
    setup() {
        // Access Pinia store inside the setup function
        const userStore = useUserStore();

        // Reactive state for authentication
        const isAuthenticated = ref(false);
        // Show header conditionally based on the path
        const showHeader = computed(() => location.pathname === '/');

        // Fetch the CSRF token from the meta tag
        const getCSRFToken = (): string => {
            return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
        };

        // Check authentication status
        const checkAuthStatus = async () => {
            try {
                const response = await fetch('/auth-status/');
                if (response.ok) {
                    const data = await response.json();
                    isAuthenticated.value = data.isAuthenticated;
                    if (isAuthenticated.value){
                        console.log("test")
                        try{
                        const response = await fetch('/profile/');
                        if (response.ok) {
                            const data = await response.json();
                            userStore.setUser(data.user); // Replace localStorage.setItem
                        }
                    }
                    catch(error){
                        console.error('Error getting profile data:', error)
                    }
                }
                } else {
                    isAuthenticated.value = false;
                }
            } catch (error) {
                console.error('Error checking authentication status:', error);
                isAuthenticated.value = false;
            }
        };

        // Handle logout functionality
        const logout = async () => {
            const csrfToken = getCSRFToken();

            if (!csrfToken) {
                console.error('CSRF token is missing. Logout cannot proceed.');
                alert('CSRF token is missing. Please refresh the page and try again.');
                return;
            }

            try {
                const response = await fetch('/logout/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    isAuthenticated.value = false;
                    userStore.clearUser(); // Clear the user data
                    alert('Logout successful.')
                    //   window.location.href = '/';
                } else {
                    const errorData = await response.json();
                    console.error('Logout failed:', errorData);
                    alert('Logout failed. Please try again.');
                }
            } catch (error) {
                console.error('An error occurred during logout:', error);
                alert('An unexpected error occurred. Please try again.');
            }
        };

        // Check authentication status on app load
        checkAuthStatus();

        return { showHeader, isAuthenticated, logout };
    },
});
</script>

<style>
/* Add any custom styles here */
</style>
