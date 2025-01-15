<template>
    <div v-if="isModalVisible" class="modal fade show" id="Modal" tabindex="-1" aria-labelledby="ModalLabel"
        style="display: block;" data-keyboard="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title ms-3" id="ModalLabel">See Requests</h5>
                    <button type="button" class="btn-close" aria-label="Close" @click="closeModal"></button>
                </div>
                <div>
                    <h3>Pending Friend Requests</h3>
                    <ul>
                        <li v-for="request in friendRequests" :key="request.id">
                            {{ request.from_username }} sent you a friend request on {{ request.sent_on }}
                            <button @click="acceptFriendRequest(request.id)">Accept</button>
                            <button @click="declineFriendRequest(request.id)">Decline</button>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
    setup() {
        const friendRequests = ref([]);
        const isModalVisible = ref(true);

        // Close the modal and navigate away
        const closeModal = () => {
            isModalVisible.value = false;
            window.location.href = "/";
        };
        const fetchFriendRequests = async () => {
            try {
                const response = await fetch('/api/friend-requests/');
                if (!response.ok) throw new Error('Failed to fetch friend requests');
                const data = await response.json();
                friendRequests.value = data.friend_requests;
            } catch (error) {
                console.error('Error fetching friend requests:', error);
            }
        };

        onMounted(fetchFriendRequests);

        return {
            friendRequests,
            closeModal,
            isModalVisible,
        };
    }
};
</script>