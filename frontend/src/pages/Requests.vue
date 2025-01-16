<template>
    <div v-if="isModalVisible" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
        <div class="bg-white rounded-lg shadow-lg overflow-hidden w-full max-w-2xl">
            <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <h5 class="text-xl font-semibold" id="ModalLabel">See Requests</h5>
                <button type="button" class="text-gray-400 hover:text-gray-600" aria-label="Close" @click="closeModal">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <div class="px-6 py-4">
                <h3 class="text-lg font-medium mb-4">Pending Friend Requests</h3>
                <ul class="space-y-4">
                    <li v-for="request in friendRequests" :key="request.id" class="flex justify-between items-center">
                        <span>{{ request.from_username }} (has hobbies: {{ request.hobbies.join(', ') }}) sent you a friend request on {{ request.sent_on }}</span>
                        <div class="space-y-2">
                            <button @click="acceptFriendRequest(request)"
                                class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600">Accept</button>
                            <button @click="declineFriendRequest(request)"
                                class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">Decline</button>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { ref, onMounted, defineComponent } from 'vue';
import { useCSRFStore } from '../store';
interface Hobby{
        id: number;
        name: string;
    }
interface Request{
    from_user_id: string;
    id: any;
    hobbies: Hobby[];
    from_username: string;
    sent_on: string;
}    
export default defineComponent({
    
    name: 'FriendRequests',
    setup() {
        const CSRFToken = useCSRFStore().csrfToken;
        const friendRequests = ref<Request[]>([]);
        const isModalVisible = ref(true);

        // Close the modal and navigate away
        const closeModal = () => {
            isModalVisible.value = false;
            window.location.href = "/";
        };
        const fetchFriendRequests = async () => {
            try {
                const response = await fetch('/friend-requests/');
                if (!response.ok) throw new Error('Failed to fetch friend requests');
                const data = await response.json();
                friendRequests.value = data.friend_requests;
            } catch (error) {
                console.error('Error fetching friend requests:', error);
            }
        };
        const declineFriendRequest = async (request: Request) => {
            try {
                const formData = new FormData();
                formData.append('to_user_id', request.from_user_id);

                const response = await fetch(`/remove-friend-request/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': CSRFToken,
                    },
                    body: formData,
                });

                if (!response.ok) {
                    throw new Error('Failed to decline friend request');
                }

                friendRequests.value = friendRequests.value.filter(r => r.id !== request.id);
            } catch (error) {
                console.error('Error declining friend request:', error);
            }
        };
        const acceptFriendRequest = async (request: Request) => {
    try {
        const formData = new FormData();
        formData.append('to_user_id', request.from_user_id);

        const response = await fetch(`/accept-friend-request/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': CSRFToken,
            },
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Error from backend:", errorData);
            throw new Error(errorData.error || 'Failed to accept friend request');
        }

        // Remove the accepted request from the list
        friendRequests.value = friendRequests.value.filter(r => r.id !== request.id);
        alert('Friend request accepted successfully.');
    } catch (error) {
        console.error('Error accepting friend request:', error);
        alert('Failed to accept friend request. Please try again.');
    }
        };
        onMounted(fetchFriendRequests);

        return {
            friendRequests,
            closeModal,
            isModalVisible,
            declineFriendRequest,
            acceptFriendRequest,
        };
    }
});
</script>