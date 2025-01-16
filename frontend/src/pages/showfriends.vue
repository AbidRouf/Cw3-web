<template>
    <div v-if="isModalVisible" class="modal fade show" id="Modal" tabindex="-1" aria-labelledby="ModalLabel"
        style="display: block;" data-keyboard="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content min-h-32">
                <div class="modal-header">
                    <h5 class="modal-title ms-3" id="ModalLabel">My Friends</h5>
                    <button type="button" class="btn-close" @click="closeModal"></button>
                </div>
                <div class="max-w-3xl p-6 bg-white rounded-lg">
                    <ul v-if="friends.length > 0" class="space-y-4">
                        <li v-for="friend in friends" :key="friend.id"
                            class="border border-gray-300 rounded p-4 flex justify-between">
                            {{ friend.username }} - Hobbies: {{ friend.hobbies.join(', ') }}
                        </li>
                    </ul>
                    <p v-else>No friends found.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
interface Hobby {
    id: number;
    name: string;
}
interface User {
    id: number;
    username: string;
    email: string;
    hobbies: Hobby[]
}

export default defineComponent({
    name: 'ShowFriends',
    setup() {
        const isModalVisible = ref(true);
        const friends = ref<User[]>([]);

        const fetchFriends = async () => {
            try {
                const response = await fetch('/api/friends/');
                if (!response.ok) throw new Error('Failed to fetch friends');
                const data = await response.json();
                if (data.success) {
                    friends.value = data.friends;
                } else {
                    alert(data.error || 'Failed to load friends');
                }
            } catch (error) {
                console.error('Error fetching friends:', error);
                alert('Failed to fetch friends.');
            }
        };

        const closeModal = () => {
            isModalVisible.value = false;
            window.location.href = "/";
        };

        onMounted(fetchFriends);

        return {
            isModalVisible,
            friends,
            closeModal,
        };
    },
});
</script>

<style scoped>
.modal {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 32rem; /* Minimum height of 32rem */
    background-color: rgba(0, 0, 0, 0.5); /* Optional: dim background */
}

.modal-content {
    max-height: 90vh; /* Ensures the modal doesn't exceed viewport height */
    overflow-y: auto; /* Adds scroll for overflowing content */
}
</style>
