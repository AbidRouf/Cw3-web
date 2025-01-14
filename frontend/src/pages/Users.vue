<template>
    <div>
        <h1>Other Users</h1>

        <!-- Filters -->
        <div>
            <label>
                Min Age:
                <input type="number" v-model="filters.minAge" @change="applyFilters" />
            </label>
            <label>
                Max Age:
                <input type="number" v-model="filters.maxAge" @change="applyFilters" />
            </label>
            <label>
                Hobby:
                <input type="text" v-model="filters.hobby" @change="applyFilters" />
            </label>
        </div>

        <!-- User List -->
        <ul v-if="users.length > 0">
            <li v-for="user in users" :key="user.id">
                {{ user.username }} - Hobbies: {{ user.hobbies.join(', ') }}
            </li>
        </ul>
        <p v-else>No users found.</p>

        <!-- Load More Button -->
        <button v-if="hasNext" @click="loadMore">Load More</button>
    </div>
</template>

<script>
export default {
    name: 'OtherUsers',
    data() {
        return {
            users: [], // Loaded users
            hasNext: false, // Whether more users are available
            page: 1, // Current page
            filters: {
                minAge: null, // Minimum age filter
                maxAge: null, // Maximum age filter
                hobby: '', // Hobby filter
            },
        };
    },
    methods: {
        // Fetch users from the API
        async fetchUsers() {
            try {
                const params = new URLSearchParams({
                    page: this.page,
                    min_age: this.filters.minAge || '',
                    max_age: this.filters.maxAge || '',
                    hobby: this.filters.hobby || '',
                }).toString();

                const response = await fetch(`/users/?${params}`);
                const data = await response.json();

                // Append new users to the list
                this.users = [...this.users, ...data.users];
                this.hasNext = data.has_next;
            } catch (error) {
                console.error('Error fetching users:', error);
                alert('Failed to fetch users. Please try again.');
            }
        },
        // Load more users when the button is clicked
        loadMore() {
            this.page += 1;
            this.fetchUsers();
        },
        // Apply filters and reset state
        applyFilters() {
            this.users = [];
            this.page = 1;
            this.fetchUsers();
        },
    },
    mounted() {
        // Fetch initial users on mount
        this.fetchUsers();
    },
};
</script>

<style scoped>
/* Your component styles go here */
</style>
