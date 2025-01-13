<template>
  <div id="app">
    <header v-if="showHeader" class="flex flex-col items-center justify-center h-20 mt-24">
      <h1 class="text-red-500 text-center">Hobbies App</h1>

      <!-- Navigation Links -->
      <router-link to="/profile/" class="mt-2">
        <button class="bg-blue-500 text-white py-2 px-4 rounded">Go to Profile</button>
      </router-link>

      <!-- Conditional Login/Logout Links -->
      <div class="flex flex-col items-center">
        <a v-if="!isAuthenticated" href="/login/" class="px-4 py-2 mt-2 bg-blue-500 text-white rounded">Login</a>
        <a v-if="!isAuthenticated" href="/signup/" class="px-4 py-2 mt-2 bg-blue-500 text-white rounded">Sign Up</a>

        <button
          v-if="isAuthenticated"
          @click="logout"
          class="px-4 py-2 mt-2 bg-red-500 text-white rounded"
        >
          Logout
        </button>
      </div>
    </header>

    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';

export default defineComponent({
  name: 'App',
  setup() {
    const showHeader = computed(() => location.pathname === '/');
    const isAuthenticated = ref(false); // Reactive state for authentication

    const checkAuthStatus = async () => {
      try {
        const response = await fetch('/auth-status/');
        if (response.ok) {
          const data = await response.json();
          isAuthenticated.value = data.isAuthenticated;
        } else {
          isAuthenticated.value = false;
        }
      } catch (error) {
        console.error('Error checking authentication status:', error);
        isAuthenticated.value = false;
      }
    };

    const logout = async () => {
      try {
        const response = await fetch('/logout/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.getAttribute('value') || '',
          },
        });

        if (response.ok) {
          isAuthenticated.value = false; // Update authentication state
          window.location.href = '/login/';
        } else {
          console.error('Logout failed');
        }
      } catch (error) {
        console.error('An error occurred:', error);
      }
    };

    // Check authentication status on app load
    checkAuthStatus();

    return { showHeader, isAuthenticated, logout };
  }
});
</script>
