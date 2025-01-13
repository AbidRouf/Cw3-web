<template>
  <div id="app">
    <header v-if="showHeader" class="flex flex-col items-center justify-center h-20 mt-24">
      <h1 class="text-red-500 text-center">Hobbies App</h1>
      <!-- add links -->
      <router-link to="/profile/" class="mt-2">
        <button class="bg-blue-500 text-white py-2 px-4 rounded">Go to Profile</button>
      </router-link>

      <a href="/login/" class="px-4 py-2 mt-2 bg-blue-500 text-white rounded">Login</a>
      <a href="/signup/" class="px-4 py-2 mt-2 bg-blue-500 text-white rounded">Sign Up</a>

      

    </header>

    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';


export default defineComponent({
  name: 'App',
  setup() {
    const showHeader = computed(() => location.pathname === '/');

    const logout = async () => {
      try {
        const response = await fetch('/logout/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.getAttribute('value') || '',
          },
        });

        if (response.ok) {
          window.location.href = '/login/';
        } else {
          console.error('Logout failed');
        }
      } catch (error) {
        console.error('An error occurred:', error);
      }
    };

    return { showHeader, logout };
  }
});
</script>
