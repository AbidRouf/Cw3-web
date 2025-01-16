import { createRouter, createWebHistory } from 'vue-router';
import Profile from '../pages/Profile.vue';
import Users from '../pages/Users.vue';
import Requests from '../pages/Requests.vue';
import ShowFriends from '../pages/ShowFriends.vue';

let base = import.meta.env.MODE === 'development' ? import.meta.env.BASE_URL : '';

const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/profile/', name: 'Profile', component: Profile },
        { path: '/users/', name: 'Users', component: Users },
        { path: '/requests/', name: 'Requests', component: Requests },
        { path: '/showfriends', name: 'ShowFriends', component: ShowFriends }

    ],
});

export default router;
