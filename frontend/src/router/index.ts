import { createRouter, createWebHistory } from 'vue-router';

// Import components for the routes
import Profile from '../pages/Profile.vue';
import Users from '../pages/Users.vue';
// Uncomment these if you have Login and Signup components
// import Login from '../pages/Login.vue';
// import Signup from '../pages/Signup.vue';

// Determine base URL based on environment
let base = import.meta.env.MODE === 'development' ? import.meta.env.BASE_URL : '';

// Create router instance
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/profile/', name: 'Profile', component: Profile }, // Profile page route
        { path: '/users/', name: 'Users', component: Users }, // Users page route

        // Uncomment these if Login and Signup pages are implemented
        // { path: '/login/', name: 'Login', component: Login },
        // { path: '/signup/', name: 'Signup', component: Signup },
    ],
});

// Export the router instance
export default router;
