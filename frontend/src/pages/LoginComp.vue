<template>
    <div class="login-container" v-html="loginTemplate"></div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import loginTemplate from "../../../api/templates/api/login.html?raw"
  
  export default defineComponent({
    name: 'LoginComponent',
    setup() {
      return { loginTemplate };
    }
  });
  </script>
  
  <style scoped>
  </style>
  