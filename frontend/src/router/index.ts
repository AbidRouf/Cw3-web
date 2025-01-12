// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import Profile from '../pages/Profile.vue';
// import Login from '../pages/LoginComp.vue';
// import Signup from '../pages/SignUpComp.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/profile/', name: 'Profile Page', component: Profile },
        // { path: '/login/', name: 'login Page', component: Login },
        // { path: '/signup/', name: 'sign up Page', component: Signup },
    ]
})

export default router
