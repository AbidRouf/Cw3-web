from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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
        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys("newuser")
        self.selenium.find_element(By.ID, "id_email").send_keys("newuser@example.com")
        self.selenium.find_element(By.ID, "id_password").send_keys("password123")
        self.selenium.find_element(By.ID, "id_password2").send_keys("password123")
        self.selenium.find_element(By.ID, "id_dob").send_keys("2001-02-02")
        self.selenium.find_element(By.CSS_SELECTOR, ".submit-button").click()

        self.assertIn("You have successfully registered", self.selenium.page_source)

    def test_login(self):
        self.selenium.get(f"{self.live_server_url}/login/")
        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys("user1")
        self.selenium.find_element(By.ID, "id_password").send_keys("password1")
        self.selenium.find_element(By.CSS_SELECTOR, ".submit-button").click()

        self.assertIn("You are now logged in", self.selenium.page_source)

    def test_edit_profile(self):
        self.selenium.get(f"{self.live_server_url}/login/")
        self.selenium.find_element(By.ID, "id_username").send_keys("user1")
        self.selenium.find_element(By.ID, "id_password").send_keys("password1")
        self.selenium.find_element(By.CSS_SELECTOR, ".submit-button").click()

        # Wait for the profile page to load
        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Manage Profile"))).click()

        self.selenium.find_element(By.NAME, "first_name").send_keys("UpdatedFirst")
        self.selenium.find_element(By.NAME, "last_name").send_keys("UpdatedLast")
        self.selenium.find_element(By.NAME, "email").clear()
        self.selenium.find_element(By.NAME, "email").send_keys("updateduser1@example.com")
        self.selenium.find_element(By.NAME, "dob").send_keys("1999-12-12")
        self.selenium.find_element(By.CSS_SELECTOR, ".save-button").click()

        self.assertIn("Profile updated successfully", self.selenium.page_source)
