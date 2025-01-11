<template>
    <div class="signup-container" v-html="signupTemplate"></div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import signupTemplate from '../../../api/templates/api/signup.html?raw';
  
  export default defineComponent({
    name: 'SignupComponent',
    setup() {
      return { signupTemplate };
    }
  });
  </script>
  
  <style scoped>
  </style>
  