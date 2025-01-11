<template>
  <div id="app">
    <header v-if="showHeader" class="flex flex-col items-center justify-center h-20 mt-24">
      <h1 class="text-red-500 text-center">Hobbies App</h1>
      <!-- add links -->
      <router-link to="/profile" class="mt-2">
        <button class="bg-blue-500 text-white py-2 px-4 rounded">Go to Profile</button>
      </router-link>

      <router-link to="/login" class="mt-2">
        <button class="bg-blue-500 text-white py-2 px-4 rounded">Go to Sign In</button>
      </router-link>
      
      <router-link to="/signup" class="mt-2">
        <button class="bg-blue-500 text-white py-2 px-4 rounded">Go to Sign Up</button>
      </router-link>
    </header>

    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useRoute } from 'vue-router';

export default defineComponent({
  name: 'App',
  setup() {
    const route = useRoute();

    const showHeader = computed(() => route.path == '/');

    return { showHeader };
  }
});
</script>
