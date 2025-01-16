<template>
    <div v-if="isModalVisible" class="modal fade show" id="Modal" tabindex="-1" aria-labelledby="ModalLabel"
        style="display: block;" data-keyboard="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title ms-3" id="ModalLabel">Manage Profile</h5>
                    <button type="button" class="btn-close" aria-label="Close" @click="closeModal"></button>
                </div>
                <div class="max-w-3xl p-6 bg-white rounded-lg">
                    <div class="mb-6 flex justify-between items-center">
                        <div>
                            <h1 class="text-3xl font-bold text-gray-800">My Profile</h1>
                            <p class="text-gray-600">Manage your account details and hobbies</p>
                        </div>
                    </div>

                    <div class="mb-8">
                        <h2 class="text-2xl font-semibold text-gray-700 mb-4">User Information</h2>
                        <form @submit.prevent="handleSubmit">
                            <div class="grid grid-cols-1 gap-4">
                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="name">Userame:</label>
                                    <input id="name" type="text" v-model="form.username" placeholder="Username"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
                                </div>

                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="name">Name:</label>
                                    <input id="name" type="text" v-model="name" placeholder="Your full name"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
                                </div>

                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="email">Email:</label>
                                    <input id="email" type="email" v-model="form.email" placeholder="you@example.com"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
                                </div>

                                <div>
                                    <label class="block text-gray-700 font-medium mb-1" for="dob">Date of Birth:</label>
                                    <input id="dob" type="date" v-model="form.dob"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
                                </div>

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
                                    <input id="confirmPassword" type="password" v-model="confirmPassword"
                                        placeholder="Confirm new password"
                                        class="w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
                                </div>
                            </div>
                        </form>
                    </div>

                    <div class="mb-8">
                        <h2 class="text-2xl font-semibold text-gray-700 mb-4">Hobbies</h2>
                        <ul class="flex flex-wrap gap-2 mb-4">
                            <li v-for="(hobby, index) in form.hobbies" :key="index"
                                class="px-3 py-1 bg-blue-200 text-blue-900 rounded-full flex items-center">
                                {{ hobby.name }}
                                <button type="button" class="ml-2 text-red-500 hover:text-red-700"
                                    @click="removeHobby(index)">
                                    &times;
                                </button>
                            </li>
                        </ul>

                        <div class="flex items-center gap-2 mb-4">
                            <select v-model="selectedExistingHobby"
                                class="flex-1 border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400">
                                <option disabled :value="{ id: -1, name: '' }">Select an existing hobby</option>
                                <option v-for="hobby in availableHobbies" :key="hobby.id" :value="hobby">
                                    {{ hobby.name }}
                                </option>
                            </select>
                            <button type="button" @click="addExistingHobby"
                                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
                                Add Hobby
                            </button>
                        </div>

                        <div class="flex items-center gap-2">
                            <input type="text" v-model="newHobby" placeholder="Add a new hobby"
                                class="flex-1 border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
                            <button type="button" @click="addNewHobby"
                                class="px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600">
                                Add Hobby
                            </button>
                        </div>
                    </div>

                    <div>
                        <button type="button" @click="handleSubmit"
                            class="w-full py-3 bg-blue-600 text-white rounded-md font-semibold hover:bg-blue-700">
                            Save
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { useCSRFStore, useUserStore } from '../store';
import { defineComponent, ref, computed, onMounted } from 'vue';
export default defineComponent({
    name: 'Profile',
    setup() {
        interface User {
            id: number;
            username: string;
            email: string;
            first_name: string;
            last_name: string;
            dob: Date;
            password: string;
            hobbies: Hobby[];
        }
        interface Hobby {
            id: number,
            name: string
        }
        const userStore = useUserStore();
        const CSRFToken = useCSRFStore().csrfToken;
        const form = ref<User>({
            id: 0,
            username: '',
            email: '',
            first_name: '',
            last_name: '',
            dob: new Date(),
            password: '',
            hobbies: [] as Hobby[],
        })
        const confirmPassword = ref('')


        const name = computed({
            get: () => `${form.value.first_name} ${form.value.last_name}`.trim(),
            set: (newValue: string) => {
                const [firstName, ...lastName] = newValue.split(' ');
                form.value.first_name = firstName || '';
                form.value.last_name = lastName.join(' ') || '';
            },
        });
        const isModalVisible = ref(true)
        if (userStore.user) {
            form.value = { ...userStore.user, password: '' };
        }
        const closeModal = (): void => {
            isModalVisible.value = false;
            window.location.href = "/";
        };



        const originalHobbies = ref<Hobby[]>([]);
        const getAllHobbies = async (): Promise<void> => {
            try {
                const response = await fetch('/hobbies/', {
                    method: 'GET',
                });
                if (response.ok) {
                    const data = await response.json();
                    originalHobbies.value = data.hobbies.map((hobby: { id: number, name: string; }) => ({ id: hobby.id, name: hobby.name }));
                } else {
                    alert('Failed to get all hobbies');
                }
            } catch (error) {
                console.error('Error getting all hobbies:', error);
            }
        };
        onMounted(() => {
            getAllHobbies();
        });
        const hobbycount = ref(originalHobbies.value.length)
        const availableHobbies = computed(() =>
            originalHobbies.value.filter((hobby) => !form.value.hobbies.some((userHobby) => userHobby.name === hobby.name))
        );

        const selectedExistingHobby = ref<Hobby>({ id: -1, name: '' });
        const newHobby = ref('');

        const addExistingHobby = async (): Promise<void> => {
            if (!selectedExistingHobby.value || selectedExistingHobby.value.id === -1) {
                alert('Please select a hobby to add.');
                return;
            }
            const formData = new URLSearchParams();
            formData.append('hobby_name', selectedExistingHobby.value.name);
            try {
                const response = await fetch('/profile/add-hobby/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': CSRFToken,
                    },
                    body: formData.toString(),
                });
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        form.value.hobbies.push({ id: selectedExistingHobby.value.id, name: selectedExistingHobby.value.name });
                        selectedExistingHobby.value = { id: -1, name: '' };
                        alert('Hobby added successfully!');
                    } else {
                        alert(data.error || 'Failed to add the hobby.');
                    }
                } else {
                    alert('Failed to add the hobby. Please try again.');
                }
            } catch (error) {
                console.error('Error adding hobby:', error);
                alert('An error occurred while adding the hobby.');
            }
        };


        const addNewHobby = async (): Promise<void> => {
            const hobby = newHobby.value.trim();

            if (!hobby) {
                alert('Please enter a hobby name.');
                return;
            }

            const formData = new FormData();
            formData.append('hobby', hobby);

            try {
                const response = await fetch('/profile/create-hobby/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': CSRFToken,
                    },
                    body: formData,
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        originalHobbies.value.push({ id: hobbycount.value, name: hobby })
                        form.value.hobbies.push({ id: hobbycount.value, name: hobby });
                        newHobby.value = '';
                        alert('Hobby added successfully!');
                    } else {
                        alert(`${data.error}, Failed to add the hobby.`);
                    }
                } else {
                    alert('Failed to add the hobby. Please try again.');
                    console.log(response)
                }
            } catch (error) {
                console.error('Error adding hobby:', error);
                alert('An error occurred while adding the hobby.');
            }
        };

        const removeHobby = async (index: number): Promise<void> => {
            const hobbyToRemove = form.value.hobbies[index].name;

            if (!hobbyToRemove) {
                alert('Invalid hobby selected for removal.');
                return;
            }

            try {
                const response = await fetch('/profile/remove-hobby/', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': CSRFToken,
                    },
                    body: JSON.stringify({ hobby: hobbyToRemove }),
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        form.value.hobbies.splice(index, 1);
                        alert(`Hobby "${hobbyToRemove}" removed successfully!`);
                    } else {
                        alert(data.error || 'Failed to remove the hobby.');
                    }
                } else {
                    console.error('Response error:', await response.text());
                    alert('Failed to remove the hobby. Please try again.');
                }
            } catch (error) {
                console.error('Error removing hobby:', error);
                alert('An error occurred while removing the hobby.');
            }
        };


        const handleSubmit = async (): Promise<void> => {
            if (form.value.password !== confirmPassword.value) {
                alert('Passwords do not match.');
                return;
            }
            try {
                let profile = false
                let password = false
                const formData = new URLSearchParams({
                    username: form.value.username,
                    first_name: form.value.first_name,
                    last_name: form.value.last_name,
                    email: form.value.email,
                    dob: form.value.dob.toString(),
                });
                const response = await fetch('/profile/update/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': CSRFToken,
                    },
                    body: formData.toString(),
                });
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        profile = true
                    } else {
                        alert(data.error || 'Failed to update profile.');
                    }
                } else {
                    console.error('Response error:', await response.text());
                    alert('Failed to update the profile. Please try again.');
                }
                if (form.value.password) {
                    const formPasswordData = new URLSearchParams({
                        new_password: form.value.password,
                        confirm_password: confirmPassword.value,
                    })
                    const passwordresponse = await fetch('/profile/change-password/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': CSRFToken,
                        },
                        body: formPasswordData.toString(),
                    });
                    if (passwordresponse.ok) {
                        const data = await passwordresponse.json();
                        if (data.success) {
                            password = true
                        } else {
                            alert(data.error || 'Failed to update password.');
                        }
                    } else {
                        console.error('Response error:', await response.text());
                        alert('Failed to update the profile. Please try again.');
                    }
                    if (password && profile) {
                        alert("Profile and password updated successfully!")
                        setTimeout(() => {
                            closeModal();
                        }, 200);
                        return
                    }
                }
                if (profile) {
                    alert("Profile updated successfully!")
                    closeModal();
                    return
                }
            } catch (error) {
                console.error('Error submitting profile:', error);
                alert('An error occurred while updating the profile.');
            }
        };

        return {
            form,
            availableHobbies,
            selectedExistingHobby,
            newHobby,
            addExistingHobby,
            addNewHobby,
            removeHobby,
            handleSubmit,
            closeModal,
            isModalVisible,
            name,
            confirmPassword,
        };
    },
});
</script>