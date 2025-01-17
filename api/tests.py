from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from api.models import Hobby

User = get_user_model()

class HobbiesAppSeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        cls.selenium = Chrome(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password1", dob="2000-01-01"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password2", dob="1995-06-15"
        )
        Hobby.objects.create(name="Football")
        Hobby.objects.create(name="Cycling")

    def test_signup(self):
        self.selenium.get(f"{self.live_server_url}/signup/")
        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("newuser")
        self.selenium.find_element(By.ID, "email").send_keys("newuser@example.com")
        self.selenium.find_element(By.ID, "password").send_keys("password123")
        self.selenium.find_element(By.ID, "password2").send_keys("password123")
        self.selenium.find_element(By.ID, "dob").send_keys("2001-02-02")
        self.selenium.find_element(By.CSS_SELECTOR, ".submit-button").click()
        current_url = self.selenium.current_url
        self.assertEqual(current_url, f"{self.live_server_url}/login/", f"URL is not the expected login URL, we are instead at {current_url}")

    def test_login(self):
        self.selenium.get(f"{self.live_server_url}/login/")
        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("user1")
        self.selenium.find_element(By.ID, "password").send_keys("password1")
        self.selenium.find_element(By.CSS_SELECTOR, ".submit-button").click()
        current_url = self.selenium.current_url
        self.assertEqual(current_url, f"{self.live_server_url}/", f"URL is not the expected homepage URL, we are instead at {current_url}")

    def test_edit_profile(self):
        self.selenium.get(f"{self.live_server_url}/login/")
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys("user1")
        self.selenium.find_element(By.ID, "password").send_keys("password1")
        self.selenium.find_element(By.CSS_SELECTOR, ".submit-button").click()

        # Navigate to the profile page
        profile_button = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "profile"))
        )
        profile_button.click()

        # Select 'Football' and 'Cycling' from the dropdown
        dropdown = self.selenium.find_element(By.CSS_SELECTOR, "select[v-model='selectedExistingHobby']")
        dropdown.click()
        self.selenium.find_element(By.XPATH, "//option[text()='Football']").click()
        dropdown.click()  # Reopen the dropdown
        self.selenium.find_element(By.XPATH, "//option[text()='Cycling']").click()

        # Add 'Singing', 'Gaming', and 'Driving' as new hobbies
        new_hobby_input = self.selenium.find_element(By.CSS_SELECTOR, "input[v-model='newHobby']")
        for hobby in ["Singing", "Gaming", "Driving"]:
            new_hobby_input.clear()
            new_hobby_input.send_keys(hobby)
            self.selenium.find_element(By.CSS_SELECTOR, "button[@click='addNewHobby']").click()

        # Remove 'Football' and 'Singing'
        for hobby_to_remove in ["Football", "Singing"]:
            hobby_element = self.selenium.find_element(By.XPATH, f"//li[contains(text(), '{hobby_to_remove}')]")
            remove_button = hobby_element.find_element(By.XPATH, ".//button")
            remove_button.click()

        # Save changes
        self.selenium.find_element(By.CSS_SELECTOR, "button[@click='handleSubmit']").click()

        # Verify success alert
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())
        alert = self.selenium.switch_to.alert
        self.assertEqual(
            alert.text,
            "Profile and password updated successfully!",
            f"Unexpected alert message: {alert.text}"
        )
        alert.accept()

