<template>
    <div v-if="isModalVisible" class="modal fade show" id="Modal" tabindex="-1" aria-labelledby="ModalLabel"
        style="display: block;" data-keyboard="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title ms-3" id="ModalLabel">Manage Profile</h5>
                    <button type="button" class="btn-close" aria-label="Close" @click="closeModal"></button>
                </div>
                <div class="max-w-3xl p-6 bg-white rounded-lg">
                    <!-- Header / Breadcrumb -->
                    <div class="mb-6 flex justify-between items-center">
                        <div></div>
                        <div>
                            <h1>Other Users</h1>

                            <!-- Filters -->
                            <div>
                                <label>
                                    Min Age:
                                    <input type="number" v-model.number="filters.minAge" @change="applyFilters" />
                                </label>
                                <label>
                                    Max Age:
                                    <input type="number" v-model.number="filters.maxAge" @change="applyFilters" />
                                </label>
                                <label>
                                    Hobby:
                                    <input type="text" v-model="filters.hobby" @change="applyFilters" />
                                </label>
                            </div>

                            <!-- User List -->
                            <ul v-if="users.length > 0 && users[0].id !== -1">
                                <li v-for="user in users" :key="user.id">
                                    {{ user.username }} - Hobbies: {{ user.hobbies.join(', ') }}
                                </li>
                            </ul>
                            <p v-else>No users found.</p>

                            <!-- Load More Button -->
                            <button v-if="hasNext" @click="loadMore">Load More</button>

                            <!-- Reusable Modal -->
                            <div v-if="selectedUser" class="modal fade show" id="userModal" tabindex="-1"
                                aria-labelledby="userModalLabel" style="display: block;" data-keyboard="true">
                                <div class="modal-dialog modal-lg">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title ms-3" id="userModalLabel">{{
                                                selectedUser.username
                                                }}'s Profile</h5>
                                            <button type="button" class="btn-close" aria-label="Close"
                                                @click="closeModal"></button>
                                        </div>
                                        <div class="modal-body">
                                            <h2 class="text-2xl font-semibold text-gray-700 mb-4">Other Users</h2>
                                            <p><strong>Age:</strong> {{ selectedUser.dob }}</p>
                                            <p><strong>Hobbies:</strong> {{ selectedUser.hobbies.join(', ') }}
                                            </p>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary"
                                                @click="closeModal">Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
    name: 'OtherUsers',
    setup() {
        const isModalVisible = ref(true)
        const users = ref<{ id: number; username: string; hobbies: string[]; dob: Date }[]>([]); // Array of user objects
    const selectedUser = ref<{ username: string; email: string; hobbies: string[]; dob: Date } | null>(null); // Single user or null

        const hasNext = ref(false) // Whether more users are available
        const page = ref(1) // Current page
        const filters = ref({
            minAge: -1, // Minimum age filter
            maxAge: 300, // Maximum age filter
            hobby: '', // Hobby filter
        })
        // const selectedUser = ref(null)
        const fetchUsers = async () => {
            try {
                const params = new URLSearchParams({
                    page: page.value.toString(),
                    min_age: filters.value.minAge?.toString() || '',
                    max_age: filters.value.maxAge?.toString() || '',
                    hobby: filters.value.hobby || '',
                }).toString();

                const response = await fetch(`/users/?${params}`);
                if (!response.ok) throw new Error('Failed to fetch users.');

                const data = await response.json();
                users.value = [...users.value, ...data.users];
                hasNext.value = data.has_next;
                // if (users.value.length > 0 && !selectedUser.value) {
                //     openModal(users.value[0]);
                // }
            } catch (error) {
                console.error('Error fetching users:', error);
                alert('Failed to fetch users. Please try again.');
            }
        }
        fetchUsers()
        // Load more users when the button is clicked
        const loadMore = () => {
            page.value += 1;
            fetchUsers();
        }
        // Apply filters and reset state
        const applyFilters = () => {
            users.value = [];
            page.value = 1;
            fetchUsers();
        }
        // Close the modal
        const closeModal = () => {
            isModalVisible.value = false;
            window.location.href = "/";
        }
        return {
            closeModal,
            applyFilters,
            loadMore,
            isModalVisible,
            users,
            hasNext,
            page,
            filters,
            selectedUser,
        };
    },
});
</script>