<template>
    <div id="app">
        <header v-if="showHeader" class="flex flex-col items-center justify-center h-auto mt-10 space-y-6">
            <h1 class="text-5xl font-bold text-red-600 text-center mb-4">Hobbies App</h1>

            <div class="flex flex-col space-y-4">
                <router-link v-if="isAuthenticated" to="/profile/">
                    <button
                        class="w-48 min-w-16 bg-gradient-to-r from-blue-500 to-gray-500 text-white py-3 px-6 text-lg rounded-lg shadow-md hover:from-gray-600 hover:to-gray-600 transition-all duration-300">
                        Manage Profile
                    </button>
                </router-link>
                <router-link v-if="isAuthenticated" to="/users/">
                    <button
                        class="w-48 min-w-16 bg-gradient-to-r from-blue-500 to-gray-500 text-white py-3 px-6 text-lg rounded-lg shadow-md hover:from-gray-600 hover:to-gray-600 transition-all duration-300">
                        See Users
                    </button>
                </router-link>
                <router-link v-if="isAuthenticated" to="/requests/">
                    <button
                        class="w-48 min-w-16 bg-gradient-to-r from-blue-500 to-gray-500 text-white py-3 px-6 text-lg rounded-lg shadow-md hover:from-gray-600 hover:to-gray-600 transition-all duration-300">
                        See Requests
                    </button>
                </router-link>
                <router-link v-if="isAuthenticated" to="/showfriends/">
                    <button
                        class="w-48 min-w-16 bg-gradient-to-r from-blue-500 to-gray-500 text-white py-3 px-6 text-lg rounded-lg shadow-md hover:from-gray-600 hover:to-gray-600 transition-all duration-300">
                        Show Friends
                    </button>
                </router-link>
            </div>

            <div class="flex flex-col items-center space-y-4">
                <a v-if="!isAuthenticated" href="/login/">
                    <button
                        class="bg-blue-500 text-white py-3 px-6 text-lg rounded-lg shadow-md hover:bg-blue-600 transition-all duration-300">
                        Login
                    </button>
                </a>
                <a v-if="!isAuthenticated" href="/signup/">
                    <button
                        class="bg-green-500 text-white py-3 px-6 text-lg rounded-lg shadow-md hover:bg-green-600 transition-all duration-300">
                        Sign Up
                    </button>
                </a>
                <button v-if="isAuthenticated" @click="logout"
                    class="bg-red-500 text-white py-3 px-6 text-lg rounded-lg shadow-md hover:bg-red-600 transition-all duration-300">
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
        const userStore = useUserStore();
        const isAuthenticated = ref(false);
        const showHeader = computed(() => location.pathname === '/');

        const getCSRFToken = (): string => {
            return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
        };

        const checkAuthStatus = async (): Promise<void> => {
            try {
                const response = await fetch('/auth-status/');
                if (response.ok) {
                    const data = await response.json();
                    isAuthenticated.value = data.isAuthenticated;
                    if (isAuthenticated.value) {
                        try {
                            const response = await fetch('/profile/');
                            if (response.ok) {
                                const data = await response.json();
                                userStore.setUser(data.user);
                            }
                        } catch (error) {
                            console.error('Error getting profile data:', error);
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

        const logout = async (): Promise<void> => {
            const csrfToken = getCSRFToken();
            if (!csrfToken) {
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
                    userStore.clearUser();
                    alert('Logout successful.');
                } else {
                    alert('Logout failed. Please try again.');
                }
            } catch (error) {
                console.error('An error occurred during logout:', error);
                alert('An unexpected error occurred. Please try again.');
            }
        };

        checkAuthStatus();

        return { showHeader, isAuthenticated, logout };
    },
});
</script>

<style scoped>
body {
    font-family: 'Arial', sans-serif;
    background-color: #f9fafb;
    /* Light background for better contrast */
    color: #1a202c;
    /* Default text color */
}
</style>
