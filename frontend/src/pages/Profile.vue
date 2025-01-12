<template>
    <div class="max-w-3xl mx-auto p-6 bg-white shadow-md rounded-lg">
      <!-- Header / Breadcrumb -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-800">My Profile</h1>
        <p class="text-gray-600">Manage your account details and hobbies</p>
      </div>
  
      <!-- User Information Section -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">User Information</h2>
        <form @submit.prevent="handleSubmit">
          <div class="grid grid-cols-1 gap-4">
            <!-- Name Field -->
            <div>
              <label class="block text-gray-700 font-medium mb-1" for="name">Name:</label>
              <input
                id="name"
                type="text"
                v-model="form.name"
                placeholder="Your full name"
                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                required
              />
            </div>
  
            <!-- Email Field -->
            <div>
              <label class="block text-gray-700 font-medium mb-1" for="email">Email:</label>
              <input
                id="email"
                type="email"
                v-model="form.email"
                placeholder="you@example.com"
                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                required
              />
            </div>
  
            <!-- Date of Birth Field -->
            <div>
              <label class="block text-gray-700 font-medium mb-1" for="dob">Date of Birth:</label>
              <input
                id="dob"
                type="date"
                v-model="form.dob"
                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                required
              />
            </div>
  
            <!-- Password Fields -->
            <div>
              <label class="block text-gray-700 font-medium mb-1" for="password">New Password:</label>
              <input
                id="password"
                type="password"
                v-model="form.password"
                placeholder="Enter new password"
                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>
            <div>
              <label class="block text-gray-700 font-medium mb-1" for="confirmPassword">Confirm Password:</label>
              <input
                id="confirmPassword"
                type="password"
                v-model="form.confirmPassword"
                placeholder="Confirm new password"
                class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>
          </div>
        </form>
      </div>
  
      <!-- Hobbies Management Section -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">Hobbies</h2>
        <!-- Current Hobbies Display -->
        <ul class="flex flex-wrap gap-2 mb-4">
          <li
            v-for="(hobby, index) in form.hobbies"
            :key="index"
            class="px-3 py-1 bg-blue-200 text-blue-900 rounded-full flex items-center"
          >
            {{ hobby }}
            <button
              type="button"
              class="ml-2 text-red-500 hover:text-red-700"
              @click="removeHobby(index)"
            >
              &times;
            </button>
          </li>
        </ul>
  
        <!-- Select Existing Hobby -->
        <div class="flex items-center gap-2 mb-4">
          <select
            v-model="selectedExistingHobby"
            class="flex-1 border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          >
            <option disabled value="">Select an existing hobby</option>
            <option
              v-for="(hobby, idx) in existingHobbies"
              :key="idx"
              :value="hobby"
            >
              {{ hobby }}
            </option>
          </select>
          <button
            type="button"
            @click="addExistingHobby"
            class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Add Hobby
          </button>
        </div>
  
        <!-- Add New Hobby Option -->
        <div class="flex items-center gap-2">
          <input
            type="text"
            v-model="newHobby"
            placeholder="Add a new hobby"
            class="flex-1 border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="button"
            @click="addNewHobby"
            class="px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600"
          >
            Add New
          </button>
        </div>
      </div>
  
      <!-- Submission Button -->
      <div>
        <button
          type="button"
          @click="handleSubmit"
          class="w-full py-3 bg-blue-600 text-white rounded-md font-semibold hover:bg-blue-700"
        >
          Save Changes
        </button>
      </div>
  
      <!-- Feedback (Placeholder) -->
      <div v-if="feedbackMessage" class="mt-4 text-center text-green-600">
        {{ feedbackMessage }}
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  
  export default defineComponent({
    name: 'Profile',
    setup() {
      // Form data (dummy backbone for now)
      const form = ref({
        name: 'John Doe',
        email: 'john.doe@example.com',
        dob: '1990-01-01',
        password: '',
        confirmPassword: '',
        hobbies: ['Reading', 'Swimming'],
      });
      const url = ref('http://localhost:8000/api/')
  
      // Dummy list of existing hobbies
      const existingHobbies = ref(['Gaming', 'Cooking', 'Traveling', 'Running']);
  
      // For selecting existing hobby from the dropdown
      const selectedExistingHobby = ref('');
  
      // New hobby input field
      const newHobby = ref('');
  
      // Feedback message (for submission)
      const feedbackMessage = ref('');
  
      // Add hobby from the existing list
      const addExistingHobby = () => {
        if (selectedExistingHobby.value && !form.value.hobbies.includes(selectedExistingHobby.value)) {
          form.value.hobbies.push(selectedExistingHobby.value);
          selectedExistingHobby.value = '';
        }
      };
  
      // Add new hobby from input
      const addNewHobby = () => {
        const hobby = newHobby.value.trim();
        if (hobby && !form.value.hobbies.includes(hobby)) {
          form.value.hobbies.push(hobby);
          newHobby.value = '';
        }
      };
  
      // Remove a hobby based on index
      const removeHobby = (index: number) => {
        form.value.hobbies.splice(index, 1);
      };
  
<<<<<<< HEAD
      // Handle form submission (dummy logic)
      const handleSubmit = () => {
        // Simple password match check
        if (form.value.password !== form.value.confirmPassword) {
          alert('Passwords do not match.');
          return;
        }
        // Dummy AJAX simulation: log to console and show feedback
        console.log('Profile data:', form.value);
        feedbackMessage.value = 'Profile updated successfully!';
        setTimeout(() => {
          feedbackMessage.value = '';
        }, 3000);
      };
  
      return {
        form,
        existingHobbies,
        selectedExistingHobby,
        newHobby,
        addExistingHobby,
        addNewHobby,
        removeHobby,
        handleSubmit,
        feedbackMessage,
=======
      // Update profile handler
    //   const updateProfile = () => {
    //     // In a real app, send an API request to update the user's profile
    //     // For now, we'll just log the updated user data
    //     console.log('Updated User:', user.value);
    //     // console.log('New Password:', newPassword.value);
    //     // console.log('Confirm Password:', confirmPassword.value);
    //     if (newPassword.value === confirmPassword.value) {
    //       // console.log('New Password:', newPassword.value);
    //       // Handle password update logic here
    //       newPassword.value = '';
    //       confirmPassword.value = '';
    //       alert('Profile updated successfully!');
    //       user.value = {id: 1, name: '', email: '', dateOfBirth: '', hobbies: []};
    //       newHobbyName.value = ''
    //       selectedHobbyId.value = ''
    //     }
    //     else{alert('Passwords do not match.')}
    //   };
  
      return {
        user,
        url,
        allHobbies,
        selectedHobbyId,
        availableHobbies,
        addHobby,
        newHobbyName,
        createAndAddHobby,
        removeHobby,
        newPassword,
        confirmPassword,
        // updateProfile,
>>>>>>> bad1f6f21f2f984ab9496455b7b009c029bfe5a8
      };
    },
    methods: {
        async updateProfile() {
            // In a real app, send an API request to update the user's profile
            // For now, we'll just log the updated user data
            console.log('User:', this.user);
            // console.log('New Password:', newPassword.value);
            // console.log('Confirm Password:', confirmPassword.value);
            if (this.newPassword === this.confirmPassword) {
                try {
                    const response = await fetch(`${this.url}signup/`, {
                        method: 'POST',
                        body: JSON.stringify({ user: this.user }),
                        headers: { 'Content-Type': 'application/json' },
                    });
                    const reply = await response.json();
                    console.log(`Status: ${response.status}  ${reply.message}`);
                    this.newPassword = '';
                    this.confirmPassword = '';
                    this.user = { name: '', email: '', dateOfBirth: '', hobbies: [] };
                    this.newHobbyName = ''
                    this.selectedHobbyId = ''
                    alert('Profile updated successfully!');
                } catch (error) {
                    alert('Error creating a profile')
                    console.error('Error creating a profile:', error);
                }
                // console.log('New Password:', newPassword.value);
                // Handle password update logic here
                // try {
                //     const response = await fetch(`${this.url}db/comment/`, {
                //         method: 'DELETE',
                //         body: JSON.stringify({ id: commentId }),
                //         headers: { 'Content-Type': 'application/json' },
                //     });
                //     const reply = await response.json();
                //     console.log(`Status: ${response.status}  ${reply.message}`);
                //     if (response.ok) {
                //         this.comments = this.comments.filter(comment => comment.id !== commentId);
                //     }
                // } catch (error) {
                //     console.error('Error deleting comment:', error);
                // } 

            }
            else { alert('Passwords do not match.') }
        }
    }
  });
  </script>
  
  <style scoped>
  /* Additional styling if needed */
  </style>
  