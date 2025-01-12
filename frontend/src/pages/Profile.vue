<template>
    <div class="profile-container">
      <h2>Your Profile</h2>
      <form @submit.prevent="updateProfile">
        <!-- Name Field -->
        <div class="form-group">
          <label for="name">Full Name:</label>
          <input
            type="text"
            id="name"
            v-model="user.name"
            placeholder="Enter your full name"
            required
          />
        </div>
  
        <!-- Email Field -->
        <div class="form-group">
          <label for="email">Email:</label>
          <input
            type="email"
            id="email"
            v-model="user.email"
            placeholder="Enter your email"
            required
          />
        </div>
  
        <!-- Date of Birth Field -->
        <div class="form-group">
          <label for="dob">Date of Birth:</label>
          <input
            type="date"
            id="dob"
            v-model="user.dateOfBirth"
            required
          />
        </div>
  
        <!-- Hobbies Section -->
        <div class="form-group">
          <label for="hobbies">Hobbies:</label>
          <!-- Add Existing Hobby -->
          <div class="hobbies-selector">
            <select v-model="selectedHobbyId">
              <option disabled value="">Select a hobby</option>
              <option v-for="hobby in availableHobbies" :key="hobby.id" :value="hobby.id">
                {{ hobby.name }}
              </option>
            </select>
            <button type="button" @click="addHobby">Add Hobby</button>
          </div>
  
          <!-- List of Current Hobbies -->
          <ul class="hobbies-list">
            <li v-for="hobby in user.hobbies" :key="hobby.id">
              {{ hobby.name }}
              <button type="button" @click="removeHobby(hobby.id)">Remove</button>
            </li>
          </ul>
  
          <!-- Add New Hobby -->
          <div class="add-hobby">
            <input
              type="text"
              v-model="newHobbyName"
              placeholder="Add different hobby"
            />
            <button type="button" @click="createAndAddHobby">Add New Hobby</button>
          </div>
        </div>
  
        <!-- Password Update Section -->
         <!-- New Password -->
        <div class="form-group">
          <label for="password">New Password:</label>
          <input
            type="password"
            id="password"
            v-model="newPassword"
            placeholder="Enter new password"
          />
        </div>
        <!-- Confirm Password -->
        <div class="form-group">
          <label for="password">Confirm Password:</label>
          <input
            type="password"
            id="password"
            v-model="confirmPassword"
            placeholder="Confirm password"
          />
        </div>
  
        <!-- Submit Button -->
        <button type="submit" class="update-button">Update Profile</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed } from 'vue';
  
  export default defineComponent({
    name: 'Profile',
    setup() {
      // Initial user data; in a real app, fetch this from the backend
      const user = ref({
        id: 1,
        name: '',
        email: '',
        dateOfBirth: '',
        hobbies: [
        ],
      });
      const url = ref('http://localhost:8000/api/')
  
      // List of all available hobbies; in a real app, fetch this from the backend
      const allHobbies = ref([
        { id: 1, name: 'Reading' },
        { id: 2, name: 'Swimming' },
        { id: 3, name: 'Gaming' },
        { id: 4, name: 'Cooking' },
        { id: 5, name: 'Driving' },
        // Add more hobbies as needed
      ]);
  
      // Selected hobby ID from the dropdown
      const selectedHobbyId = ref<string | number>('');
  
      // New hobby name input
      const newHobbyName = ref('');
  
      // New password input
      const newPassword = ref('');
        
      // Confirm password input
      const confirmPassword = ref('');
  
      // Compute available hobbies that are not already added
      const availableHobbies = computed(() => {
        return allHobbies.value.filter(
          (hobby) => !user.value.hobbies.some((userHobby) => userHobby.id === hobby.id)
        );
      });
  
      // Add selected hobby to the user's hobbies list
      const addHobby = () => {
        const hobbyToAdd = allHobbies.value.find((hobby) => hobby.id === selectedHobbyId.value);
        if (hobbyToAdd) {
          user.value.hobbies.push(hobbyToAdd);
          selectedHobbyId.value = '';
          // In a real app, send an API request to update hobbies
        }
      };
  
      // Create a new hobby and add it to the user's hobbies list
      const createAndAddHobby = () => {
        const trimmedName = newHobbyName.value.trim();
        if (trimmedName) {
          // In a real app, send an API request to create the hobby
          // Here, we'll mock the creation with a new ID
          const newId = allHobbies.value.length + 1;
          const newHobby = { id: newId, name: trimmedName };
          allHobbies.value.push(newHobby);
          user.value.hobbies.push(newHobby);
          newHobbyName.value = '';
        }
      };
  
      // Remove a hobby from the user's hobbies list
      const removeHobby = (hobbyId: number) => {
        user.value.hobbies = user.value.hobbies.filter((hobby) => hobby.id !== hobbyId);
        // In a real app, send an API request to update hobbies
      };
  
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
  .profile-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: #f9f9f9;
    border-radius: 8px;
  }
  
  h2 {
    text-align: center;
    margin-bottom: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  input[type='text'],
  input[type='email'],
  input[type='date'],
  input[type='password'],
  select {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .hobbies-selector {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .hobbies-selector select {
    flex: 1;
  }
  
  .hobbies-selector button {
    padding: 0.5rem 1rem;
    background-color: #3498db;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .hobbies-selector button:hover {
    background-color: #2980b9;
  }
  
  .hobbies-list {
    list-style: none;
    padding: 0;
    margin-bottom: 0.5rem;
  }
  
  .hobbies-list li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.3rem 0;
    border-bottom: 1px solid #eee;
  }
  
  .hobbies-list button {
    padding: 0.3rem 0.6rem;
    background-color: #e74c3c;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .hobbies-list button:hover {
    background-color: #c0392b;
  }
  
  .add-hobby {
    display: flex;
    gap: 0.5rem;
  }
  
  .add-hobby input {
    flex: 1;
  }
  
  .add-hobby button {
    padding: 0.5rem 1rem;
    background-color: #2ecc71;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .add-hobby button:hover {
    background-color: #27ae60;
  }
  
  .update-button {
    width: 100%;
    padding: 0.7rem;
    background-color: #9b59b6;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }
  
  .update-button:hover {
    background-color: #8e44ad;
  }
  </style>
  