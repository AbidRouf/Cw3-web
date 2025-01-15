<template>
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
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  
  export default {
    setup() {
      const friendRequests = ref([]);
  
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
        friendRequests
      };
    }
  };
  </script>
  