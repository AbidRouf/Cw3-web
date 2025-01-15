<template>
    <div v-if="isModalVisible" class="modal fade show" id="Modal" tabindex="-1" aria-labelledby="ModalLabel"
        style="display: block;" data-keyboard="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title ms-3" id="ModalLabel">Manage Profile</h5>
                    <button type="button" class="btn-close" @click="closeModal"></button>
                </div>
                <div class="max-w-3xl p-6 bg-white rounded-lg">
                    <div class="mb-6 flex justify-between items-center">
                        <h1>Other Users</h1>
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
                    </div>
                    <ul v-if="users.length > 0">
                        <li v-for="user in users" :key="user.id">
                            {{ user.username }} - Hobbies: {{ user.hobbies.join(', ') }}
                        </li>
                    </ul>
                    <p v-else>No users found.</p>
                    <button v-if="hasNext" @click="loadMore">Load More</button>
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
              hobby: ''
          });
  
          // Function to fetch users from the backend
          const fetchUsers = async () => {
              try {
                  const params = new URLSearchParams({
                      page: page.value.toString(),
                      min_age: filters.value.minAge.toString(),
                      max_age: filters.value.maxAge.toString(),
                      hobby: filters.value.hobby
                  }).toString();
  
                  const response = await fetch(`/users/?${params}`);
                  if (!response.ok) throw new Error('Failed to fetch users.');
  
                  const data = await response.json();
                  users.value = data.users;
                  hasNext.value = data.has_next;
              } catch (error) {
                  console.error('Error fetching users:', error);
                  alert('Failed to fetch users. Please try again.');
              }
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
              users.value = [];
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
              filters
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
  