from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from api.models import Hobby
import time

User = get_user_model()

class HobbiesAppSeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        cls.selenium = Chrome(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password1", dob="1983-12-04"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password2", dob="2005-06-15"
        )
        self.user3 = User.objects.create_user(
            username="user3", email="user3@example.com", password="password3", dob="2013-05-03"
        )
        self.user4 = User.objects.create_user(
            username="user4", email="user4@example.com", password="password4", dob="2000-01-01"
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
        self.test_login()
        profile_button = WebDriverWait(self.selenium, 10).until(
           EC.presence_of_element_located((By.ID, "profile"))
        )
        profile_button.click()
        username = self.selenium.find_element(By.ID, "username")
        username.clear()
        username.send_keys("newusername")
        self.selenium.find_element(By.ID, "name").send_keys("User's Full Name")
        email = self.selenium.find_element(By.ID, "email")
        email.clear()
        email.send_keys("user1newemail@example.com")
        self.selenium.find_element(By.ID, "dob").send_keys("12-12-1999")
        self.selenium.find_element(By.ID, "password").send_keys("newpassword1")
        self.selenium.find_element(By.ID, "confirmPassword").send_keys("newpassword1")
        self.selenium.find_element(By.ID, "Football").click()
        self.selenium.find_element(By.ID, "ExistingHobbyButton").click()
        WebDriverWait(self.selenium, 2).until(EC.alert_is_present())
        self.selenium.switch_to.alert.accept()
        self.selenium.find_element(By.ID, "Cycling").click()
        self.selenium.find_element(By.ID, "ExistingHobbyButton").click()
        WebDriverWait(self.selenium, 2).until(EC.alert_is_present())
        self.selenium.switch_to.alert.accept()
        self.selenium.find_element(By.ID, "NewHobby").send_keys("Singing")
        self.selenium.find_element(By.ID, "NewHobbyButton").click()
        WebDriverWait(self.selenium, 2).until(EC.alert_is_present())
        self.selenium.switch_to.alert.accept()
        self.selenium.find_element(By.ID, "NewHobby").send_keys("Gaming")
        self.selenium.find_element(By.ID, "NewHobbyButton").click()
        WebDriverWait(self.selenium, 2).until(EC.alert_is_present())
        self.selenium.switch_to.alert.accept()
        self.selenium.find_element(By.ID, "NewHobby").send_keys("Driving")
        self.selenium.find_element(By.ID, "NewHobbyButton").click()
        WebDriverWait(self.selenium, 2).until(EC.alert_is_present())
        self.selenium.switch_to.alert.accept()
        self.selenium.find_element(By.ID, "Remove Hobby Football").click()
        WebDriverWait(self.selenium, 2).until(EC.alert_is_present())
        self.selenium.switch_to.alert.accept()
        self.selenium.find_element(By.ID, "Remove Hobby Singing").click()
        WebDriverWait(self.selenium, 2).until(EC.alert_is_present())
        self.selenium.switch_to.alert.accept()
        self.selenium.find_element(By.ID, "SaveButton").click()
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())
        alert = self.selenium.switch_to.alert
        alert.text
        self.assertEqual(
            alert.text,
            "Profile and password updated successfully!",
            f"Unexpected alert message: {alert.text}"
        )
        alert.accept()

    def test_filter_by_age(self):
        self.test_login()
        users_button = WebDriverWait(self.selenium, 10).until(
           EC.presence_of_element_located((By.ID, "users"))
        )
        users_button.click()
        # totalUsers = len(self.selenium.find_elements(By.CSS_SELECTOR, "ul#UserList li"))
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element(By.ID, "minAge").get_attribute("value") == "0"
        )
        minAge = self.selenium.find_element(By.ID, "minAge")
        minAge.click()
        minAge.clear()
        minAge.send_keys("15")
        # WebDriverWait(self.selenium, 10).until(
        #     lambda driver: driver.find_element(By.ID, "maxAge").get_attribute("value") == "300"
        # )
        maxAge = self.selenium.find_element(By.ID, "maxAge")
        maxAge.click()
        maxAge.send_keys(Keys.CONTROL + "a")
        maxAge.send_keys(Keys.BACKSPACE)
        maxAge.send_keys("22")
        minAge.click()
        try:
            WebDriverWait(self.selenium, 10).until(
                lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "ul li")) == 1
            )
            filteredUsers = len(self.selenium.find_elements(By.CSS_SELECTOR, "ul#UserList li"))
            self.assertEqual(
                filteredUsers,
                1,
                f"{filteredUsers} number of users displayed"
            )   
        except Exception as e:
            filteredUsers = len(self.selenium.find_elements(By.CSS_SELECTOR, "ul#UserList li"))
            print(f"Test failed, expected 1 user to be displayed, but {filteredUsers} users were displayed")
            raise e

    def test_send_friend_request(self):
        self.test_login()
        users_button = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "users"))
        )
        users_button.click()
        self.selenium.find_element(By.CSS_SELECTOR, "ul li#user2 button#AddFriend").click()
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())
        alert = self.selenium.switch_to.alert
        alert.text
        self.assertEqual(
            alert.text,
            "Friend request sent successfully.",
            f"Unexpected alert message: {alert.text}"
        )
        alert.accept()
    
    def test_accept_friend_request(self):
        self.test_login()
        users_button = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "users"))
        )
        users_button.click()
        self.selenium.find_element(By.CSS_SELECTOR, "ul li#user2 button#AddFriend").click()
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())
        alert = self.selenium.switch_to.alert
        alert.text
        self.assertEqual(
            alert.text,
            "Friend request sent successfully.",
            f"Unexpected alert message: {alert.text}"
        )
        alert.accept()
        self.selenium.find_element(By.ID, "Close").click()
        time.sleep(1)
        self.selenium.find_element(By.ID, "logout").click()
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())
        self.selenium.switch_to.alert.accept()
        self.selenium.find_element(By.ID, "login").click()
        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("user2")
        self.selenium.find_element(By.ID, "password").send_keys("password2")
        self.selenium.find_element(By.CSS_SELECTOR, ".submit-button").click()
        requests_button = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "requests"))
        )
        requests_button.click()
        self.selenium.find_element(By.CSS_SELECTOR, "ul li#user1 button").click()
        WebDriverWait(self.selenium, 10).until(EC.alert_is_present())
        self.selenium.switch_to.alert.accept()
        time.sleep(1)
        self.selenium.find_element(By.ID, "Close").click()
        friends_button = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "friends"))
        )
        friends_button.click()
        friend = self.selenium.find_element(By.CSS_SELECTOR, "ul li#user1")
        self.assertIn(
            "user1",
            friend.text,
            f"Unexpected friend: {friend.text}"
        )