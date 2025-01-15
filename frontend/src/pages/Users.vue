<template>
    <div v-if="isModalVisible" class="modal fade show" id="Modal" tabindex="-1" aria-labelledby="ModalLabel"
        style="display: block;" data-keyboard="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title ms-3" id="ModalLabel">Other Users</h5>
                    <button type="button" class="btn-close" @click="closeModal"></button>
                </div>
                <div class="max-w-3xl p-6 bg-white rounded-lg">
                    <div class="mb-6 flex justify-between items-center">
                        <div class="flex space-x-4">
                            <label class="flex items-center space-x-2">
                                <span>Min Age:</span>
                                <input type="number" v-model.number="filters.minAge" @change="applyFilters"
                                    class="border border-gray-300 rounded p-2" />
                            </label>
                            <label class="flex items-center space-x-2">
                                <span>Max Age:</span>
                                <input type="number" v-model.number="filters.maxAge" @change="applyFilters"
                                    class="border border-gray-300 rounded p-2" />
                            </label>
                        </div>
                    </div>
                    <ul v-if="users.length > 0" class="space-y-4">
                        <li v-for="user in users" :key="user.id" class="border border-gray-300 rounded p-4 flex justify-between">
                            {{ user.username }} - Hobbies: {{ user.hobbies.join(', ') }}
                            <button @click="sendFriendRequest(user.id)" class="ml-2 bg-blue-500 text-white rounded p-2">Send Friend Request</button>

                        </li>
                    </ul>
                    <p v-else>No users found.</p>
                    <button v-if="hasNext" @click="loadMore" class="mt-4 bg-blue-500 text-white rounded p-2">
                        Load More
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';

interface User {
    id: number;
    username: string;
    hobbies: string[];
    dob: Date;
}

export default defineComponent({
    name: 'OtherUsers',
    setup() {
        const isModalVisible = ref(true);
        const users = ref<User[]>([]);
        const hasNext = ref(false);
        const page = ref(1);
        const filters = ref({
            minAge: 0,
            maxAge: 300,
        });

        // Function to fetch users from the backend
        const fetchUsers = async () => {
            try {
                const params = new URLSearchParams({
                    page: page.value.toString(),
                    min_age: filters.value.minAge.toString(),
                    max_age: filters.value.maxAge.toString(),
                }).toString();

                const response = await fetch(`/users/similar-hobbies/?${params}`);
                if (!response.ok) throw new Error('Failed to fetch users.');

                const data = await response.json();
                console.log("API Response:", data);  // Check what you receive from the API
                users.value = data.users;
                hasNext.value = data.has_next;
            } catch (error) {
                console.error('Error fetching users:', error);
                alert('Failed to fetch users. Please try again.');
            }
        };

        const sendFriendRequest = async (toUserId: number) => {
            try {
                const response = await fetch('/send-friend-request/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: new URLSearchParams({ to_user_id: toUserId.toString() })
                });
                const data = await response.json();
                if (data.success) {
                    alert(data.message);
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.error('Error sending friend request:', error);
                alert('Failed to send friend request.');
            }
        };

    const getCSRFToken = () => {
        const csrfCookie = document.cookie.split(';').find(row => row.startsWith('csrftoken='));
        if (csrfCookie) {
            return csrfCookie.split('=')[1];
        }
        return '';
    };

        // Call fetchUsers on component mount
        onMounted(fetchUsers);

        // Load more users when the button is clicked
        const loadMore = () => {
            page.value += 1;
            fetchUsers();
        };

        // Apply filters and reset pagination
        const applyFilters = () => {
            page.value = 1;
            fetchUsers();
        };

        // Close the modal and navigate away
        const closeModal = () => {
            isModalVisible.value = false;
            window.location.href = "/";
        };

        return {
            closeModal,
            applyFilters,
            loadMore,
            isModalVisible,
            users,
            hasNext,
            page,
            filters,
            sendFriendRequest,
        };
    },
});
</script>

<style scoped>
.modal {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>