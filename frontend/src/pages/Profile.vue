<template>
    <div v-if="isModalVisible" class="modal fade show" id="commentModal" tabindex="-1"
        aria-labelledby="commentModalLabel" style="display: block;" data-keyboard="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title ms-3" id="commentModalLabel">Manage Profile</h5>
                    <button type="button" class="btn-close" aria-label="Close" @click="closeModal"></button>
                </div>
                <div class="max-w-3xl p-6 bg-white rounded-lg">
                    <!-- Header / Breadcrumb -->
                    <div class="mb-6 flex justify-between items-center">
                        <div>
                            <h1 class="text-3xl font-bold text-gray-800">My Profile</h1>
                            <p class="text-gray-600">Manage your account details and hobbies</p>
                        </div>
                    </div>

                    <!-- User Information Section -->
                    <div class="mb-8">
                        <h2 class="text-2xl font-semibold text-gray-700 mb-4">User Information</h2>
                        <form @submit.prevent="handleSubmit">
                            <div class="grid grid-cols-1 gap-4">
                                <!-- Userame Field -->
                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="name">userame:</label>
                                    <input id="name" type="text" v-model="form.username" placeholder="Your full name"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        required />
                                </div>

                                <!-- Name Field -->
                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="name">Name:</label>
                                    <input id="name" type="text" v-model="name" placeholder="Your full name"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        required />
                                </div>

                                <!-- Email Field -->
                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="email">Email:</label>
                                    <input id="email" type="email" v-model="form.email" placeholder="you@example.com"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        required />
                                </div>

                                <!-- Date of Birth Field -->
                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="dob">Date of Birth:</label>
                                    <input id="dob" type="date" v-model="form.dob"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        required />
                                </div>

                                <!-- Password Fields -->
                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="password">New
                                        Password:</label>
                                    <input id="password" type="password" v-model="form.password"
                                        placeholder="Enter new password"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
                                </div>
                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="confirmPassword">Confirm
                                        Password:</label>
                                    <input id="confirmPassword" type="password" v-model="form.confirmPassword"
                                        placeholder="Confirm new password"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
                                </div>
                            </div>
                        </form>
                    </div>

                    <!-- Hobbies Management Section -->
                    <div class="mb-8">
                        <h2 class="text-2xl font-semibold text-gray-700 mb-4">Hobbies</h2>
                        <!-- Current Hobbies Display -->
                        <ul class="flex flex-wrap gap-2 mb-4">
                            <li v-for="(hobby, index) in form.hobbies" :key="index"
                                class="px-3 py-1 bg-blue-200 text-blue-900 rounded-full flex items-center">
                                {{ hobby }}
                                <button type="button" class="ml-2 text-red-500 hover:text-red-700"
                                    @click="removeHobby(index)">
                                    &times;
                                </button>
                            </li>
                        </ul>

                        <!-- Select Existing Hobby -->
                        <div class="flex items-center gap-2 mb-4">
                            <select v-model="selectedExistingHobby"
                                class="flex-1 border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400">
                                <option disabled value="">Select an existing hobby</option>
                                <option v-for="(hobby, idx) in existingHobbies" :key="idx" :value="hobby">
                                    {{ hobby }}
                                </option>
                            </select>
                            <button type="button" @click="addExistingHobby"
                                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
                                Add Hobby
                            </button>
                        </div>

                        <!-- Add New Hobby Option -->
                        <div class="flex items-center gap-2">
                            <input type="text" v-model="newHobby" placeholder="Add a new hobby"
                                class="flex-1 border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
                            <button type="button" @click="addNewHobby"
                                class="px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600">
                                Button
                            </button>
                        </div>
                    </div>

                    <!-- Submission Button -->
                    <div>
                        <button type="button" @click="handleSubmit"
                            class="w-full py-3 bg-blue-600 text-white rounded-md font-semibold hover:bg-blue-700">
                            Save
                        </button>
                    </div>

                    <!-- Feedback (Placeholder) -->
                    <div v-if="feedbackMessage" class="mt-4 text-center text-green-600">
                        {{ feedbackMessage }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';

export default defineComponent({
    name: 'Profile',
    setup() {
        // Form data (dummy backbone for now)
        const form = ref({
            username: '',
            first_name: '',
            last_name: '',
            email: '',
            dob: null,
            password: '',
            confirmPassword: '',
            hobbies: ['N/A'],
        });
        const name = computed({
            get: () => `${form.value.first_name} ${form.value.last_name}`.trim(),
            set: (newValue: string) => {
                const [firstName, ...lastName] = newValue.split(' ');
                form.value.first_name = firstName || '';
                form.value.last_name = lastName.join(' ') || '';
            },
        }); const isModalVisible = ref(true)
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            form.value = JSON.parse(storedUser);
        }
        const closeModal = () => {
            isModalVisible.value = false;
            window.location.href = "/";
        }



        const existingHobbies = ref(['Gaming', 'Cooking', 'Traveling', 'Running', 'Reading', 'Swimming']);
        const selectedExistingHobby = ref('');
        const newHobby = ref('');
        const feedbackMessage = ref('');

        const addExistingHobby = () => {
            if (selectedExistingHobby.value && !form.value.hobbies.includes(selectedExistingHobby.value)) {
                form.value.hobbies.push(selectedExistingHobby.value);
                const index = existingHobbies.value.indexOf(selectedExistingHobby.value);
                existingHobbies.value.splice(index, 1)
                selectedExistingHobby.value = '';
            }
        };

        const addNewHobby = () => {
            const hobby = newHobby.value.trim();
            if (hobby && !form.value.hobbies.includes(hobby)) {
                form.value.hobbies.push(hobby);
                newHobby.value = '';
            }
        };

        const removeHobby = (index: number) => {
            existingHobbies.value.push(form.value.hobbies[index])
            form.value.hobbies.splice(index, 1);
        };

        const handleSubmit = () => {
            if (!form.value.username || !form.value.first_name || !form.value.last_name || !form.value.email || !form.value.dob || !form.value.password || form.value.hobbies.length < 1) {
                alert('Fill in all fields');
                return;
            }
            if (form.value.password !== form.value.confirmPassword) {
                alert('Passwords do not match.');
                return;
            }
            console.log('Profile data:', form.value);
            feedbackMessage.value = 'Profile updated successfully!';
            setTimeout(() => {
                feedbackMessage.value = '';
                closeModal()
            }, 3000);
        };

        // Logout functionality
        const logout = async () => {
            try {
                const response = await fetch('/logout/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.getAttribute('value') || '',
                    },
                });

                if (response.ok) {
                    window.location.href = '/login/';
                } else {
                    alert('Failed to log out. Please try again.');
                }
            } catch (error) {
                console.error('Error during logout:', error);
            }
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
            logout,
            closeModal,
            isModalVisible,
            name,
        };
    },
});
</script>

<style scoped>
/* Additional styling if needed */
</style>