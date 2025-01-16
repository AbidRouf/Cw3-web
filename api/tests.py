from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from time import sleep


class HobbiesAppSeleniumTests(StaticLiveServerTestCase):
    fixtures = ["user-data.json"]  # Replace with your actual fixture if needed

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_signup(self):
        """Test account creation/signup."""
        self.selenium.get(f"{self.live_server_url}/signup/")
        self.selenium.find_element(By.NAME, "username").send_keys("testuser")
        self.selenium.find_element(By.NAME, "email").send_keys("testuser@example.com")
        self.selenium.find_element(By.NAME, "password").send_keys("password123")
        self.selenium.find_element(By.NAME, "password2").send_keys("password123")
        self.selenium.find_element(By.NAME, "dob").send_keys("1995-01-01")
        self.selenium.find_element(By.CLASS_NAME, "submit-button").click()

        # Assert successful redirect after signup
        self.assertEqual(self.selenium.current_url, f"{self.live_server_url}/login/")

    def test_login(self):
        """Test login functionality."""
        self.selenium.get(f"{self.live_server_url}/login/")
        self.selenium.find_element(By.NAME, "username").send_keys("testuser")
        self.selenium.find_element(By.NAME, "password").send_keys("password123")
        self.selenium.find_element(By.CLASS_NAME, "submit-button").click()

        # Assert successful redirect to the home page
        sleep(2)  # Optional: Wait for the page to load
        self.assertIn("Hobbies App", self.selenium.page_source)

    def test_edit_profile(self):
        """Test editing user's profile."""
        # Login first
        self.test_login()

        # Navigate to profile page
        self.selenium.find_element(By.LINK_TEXT, "Manage Profile").click()
        sleep(2)

        # Edit profile fields
        first_name_input = self.selenium.find_element(By.NAME, "first_name")
        first_name_input.clear()
        first_name_input.send_keys("UpdatedFirstName")

        last_name_input = self.selenium.find_element(By.NAME, "last_name")
        last_name_input.clear()
        last_name_input.send_keys("UpdatedLastName")

        self.selenium.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Assert success message or changes
        self.assertIn("Profile updated successfully!", self.selenium.page_source)

    def test_filter_users_by_age(self):
        """Test filtering users by age on the users page."""
        # Login first
        self.test_login()

        # Navigate to users page
        self.selenium.find_element(By.LINK_TEXT, "See Users").click()
        sleep(2)

        # Set age filter
        min_age_input = self.selenium.find_element(By.NAME, "min_age")
        min_age_input.send_keys(Keys.CONTROL + "a")
        min_age_input.send_keys("18")

        max_age_input = self.selenium.find_element(By.NAME, "max_age")
        max_age_input.send_keys(Keys.CONTROL + "a")
        max_age_input.send_keys("30")

        self.selenium.find_element(By.XPATH, '//button[text()="Apply Filters"]').click()

        # Assert filtered results
        self.assertIn("Filtered Users", self.selenium.page_source)

    def test_send_friend_request(self):
        """Test sending a friend request."""
        # Login first
        self.test_login()

        # Navigate to users page
        self.selenium.find_element(By.LINK_TEXT, "See Users").click()
        sleep(2)

        # Send a friend request to the first user
        self.selenium.find_element(By.XPATH, '//button[text()="Send Friend Request"]').click()

        # Assert success message
        self.assertIn("Friend request sent successfully!", self.selenium.page_source)

    def test_accept_friend_request(self):
        """Test accepting a friend request as another user."""
        # Login as another user
        self.selenium.get(f"{self.live_server_url}/login/")
        self.selenium.find_element(By.NAME, "username").send_keys("anotheruser")
        self.selenium.find_element(By.NAME, "password").send_keys("anotherpassword")
        self.selenium.find_element(By.CLASS_NAME, "submit-button").click()

        # Navigate to friend requests page
        self.selenium.find_element(By.LINK_TEXT, "See Requests").click()
        sleep(2)

        # Accept the first friend request
        self.selenium.find_element(By.XPATH, '//button[text()="Accept"]').click()

        # Assert success message
        self.assertIn("Friend request accepted successfully!", self.selenium.page_source)
