<template>
    <div v-if="isModalVisible" class="modal fade show" id="Modal" tabindex="-1" aria-labelledby="ModalLabel"
        style="display: block;" data-keyboard="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content min-h-32">
                <div class="modal-header">
                    <h5 class="modal-title ms-3" id="ModalLabel">Other Users</h5>
                    <button type="button" id="Close" class="btn-close" @click="closeModal"></button>
                </div>
                <div class="max-w-3xl p-6 bg-white rounded-lg">
                    <div class="mb-6 flex justify-between items-center">
                        <div class="flex space-x-4">
                            <label class="flex items-center space-x-2">
                                <span>Min Age:</span>
                                <input type="number" v-model.number="filters.minAge" @change="applyFilters"
                                    class="border border-gray-300 rounded p-2" id="minAge"/>
                            </label>
                            <label class="flex items-center space-x-2">
                                <span>Max Age:</span>
                                <input type="number" v-model.number="filters.maxAge" @change="applyFilters"
                                    class="border border-gray-300 rounded p-2"  id="maxAge"/>
                            </label>
                        </div>
                    </div>
                    <ul v-if="users.length > 0" class="space-y-4" id="UserList">
                        <li v-for="user in users" :key="user.id" :id="user.username"
                            class="border border-gray-300 rounded p-4 flex justify-between">
                            {{ user.username }} - Hobbies: {{ user.hobbies.join(', ') }}
                            <button  id="AddFriend" @click="sendFriendRequest(user.id)"
                                class="ml-2 bg-green-500 text-white rounded h-12 p-2 flex-shrink-0">Send Friend
                                Request</button>

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
import { useCSRFStore } from '../store';

interface Hobby {
    id: number;
    name: string;
}
interface User {
    id: number;
    username: string;
    hobbies: Hobby[];
    dob: Date;
}
interface Filter{
    minAge: number;
    maxAge: number;
}
export default defineComponent({
    name: 'OtherUsers',
    setup() {
        const CSRFToken = useCSRFStore().csrfToken;
        const isModalVisible = ref<boolean>(true);
        const users = ref<User[]>([]);
        const hasNext = ref<boolean>(false);
        const page = ref<number>(1);
        const filters = ref<Filter>({
            minAge: 0,
            maxAge: 300,
        });

        const fetchUsers = async (): Promise<void> => {
            try {
                const params = new URLSearchParams({
                    page: page.value.toString(),
                    min_age: filters.value.minAge.toString(),
                    max_age: filters.value.maxAge.toString(),
                }).toString();

                const response = await fetch(`/users/similar-hobbies/?${params}`);
                if (!response.ok) throw new Error('Failed to fetch users.');

                const data = await response.json();
                users.value = data.users;
                hasNext.value = data.has_next;
            } catch (error) {
                console.error('Error fetching users:', error);
                alert('Failed to fetch users. Please try again.');
            }
        };

        const sendFriendRequest = async (toUserId: number): Promise<void> => {
            try {
                const response = await fetch('/send-friend-request/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': CSRFToken
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

        onMounted(fetchUsers);

        const loadMore = (): void => {
            page.value += 1;
            fetchUsers();
        };

        const applyFilters = (): void => {
            page.value = 1;
            fetchUsers();
        };

        const closeModal = (): void => {
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
    min-height: 32rem;
    /* Minimum height of 32rem */
    background-color: rgba(0, 0, 0, 0.5);
    /* Optional: dim background */
}

.modal-content {
    max-height: 90vh;
    /* Ensures the modal doesn't exceed viewport height */
    overflow-y: auto;
    /* Adds scroll for overflowing content */
}
</style>
