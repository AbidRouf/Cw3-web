from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

User = get_user_model()


class HobbiesAppSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Create test users
        User.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com",
            dob="1995-01-01",
        )
        User.objects.create_user(
            username="anotheruser",
            password="anotherpassword",
            email="anotheruser@example.com",
            dob="1990-01-01",
        )

    def handle_alert(self):
        try:
            WebDriverWait(self.selenium, 3).until(EC.alert_is_present())
            alert = Alert(self.selenium)
            alert.dismiss()  # Dismiss the alert
        except TimeoutException:
            pass

    def login(self, username, password):
        """Login helper function."""
        self.selenium.get(f"{self.live_server_url}/login/")
        self.selenium.find_element(By.NAME, "username").send_keys(username)
        self.selenium.find_element(By.NAME, "password").send_keys(password)
        self.selenium.find_element(By.XPATH, '//button[text()="Log in"]').click()

        # Handle unexpected alerts
        self.handle_alert()

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Manage Profile"))
        )

    def test_login(self):
        """Test login functionality."""
        self.login("testuser", "password123")
        self.assertIn("Manage Profile", self.selenium.page_source)

    def test_edit_profile(self):
        """Test editing the profile."""
        self.login("testuser", "password123")
        self.selenium.find_element(By.LINK_TEXT, "Manage Profile").click()

        # Update profile fields
        self.selenium.find_element(By.NAME, "first_name").send_keys("Updated")
        self.selenium.find_element(By.NAME, "last_name").send_keys("User")
        self.selenium.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Handle success alert
        self.handle_alert()

    def test_filter_users_by_age(self):
        """Test filtering users by age."""
        self.login("testuser", "password123")
        self.selenium.find_element(By.LINK_TEXT, "See Users").click()

        # Set age filters
        min_age_input = self.selenium.find_element(By.NAME, "min_age")
        min_age_input.clear()
        min_age_input.send_keys("18")

        max_age_input = self.selenium.find_element(By.NAME, "max_age")
        max_age_input.clear()
        max_age_input.send_keys("30")

        self.selenium.find_element(By.XPATH, '//button[text()="Apply Filters"]').click()

    def test_send_friend_request(self):
        """Test sending a friend request."""
        self.login("testuser", "password123")
        self.selenium.find_element(By.LINK_TEXT, "See Users").click()

        self.selenium.find_element(By.XPATH, '//button[text()="Send Friend Request"]').click()
        self.handle_alert()

    def test_accept_friend_request(self):
        """Test accepting a friend request."""
        self.login("testuser", "password123")
        self.selenium.find_element(By.LINK_TEXT, "Logout").click()

        self.login("anotheruser", "anotherpassword")
        self.selenium.find_element(By.LINK_TEXT, "See Requests").click()
        self.selenium.find_element(By.XPATH, '//button[text()="Accept"]').click()
        self.handle_alert()
