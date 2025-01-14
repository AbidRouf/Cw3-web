import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia';
import { useCSRFStore } from './store';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import '../src/assets/main.css'

const pinia = createPinia();
const app = createApp(App)

app.use(router)
app.use(pinia);

const csrfStore = useCSRFStore();
csrfStore.fetchCSRFToken();

app.mount('#app')
