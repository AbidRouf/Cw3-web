<template>
  <div id="app">
    <header v-if="showHeader">
      <h1 class="text-red-500">Hobbies App</h1>
      <!-- ADD LINKS HERE -->
      <router-link to="/profile">
        <button>Go to Profile</button>
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

    // Only show the header if the route is NOT '/profile'
    const showHeader = computed(() => route.path == '/');

    return { showHeader };
  }
});
</script>

<style>
/* your styles here */
</style>
