import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import Options
import time


class SignUpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configure WebDriver options (e.g., ChromeDriver path)
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        cls.driver = webdriver.Chrome(service=Service("/path/to/chromedriver"), options=chrome_options)  # Update path

    def test_signup_and_success_page(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/signup/")  # Update URL if different

        # Fill in the signup form
        username_field = driver.find_element(By.NAME, "username")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "password2")
        dob_field = driver.find_element(By.NAME, "dob")

        username_field.send_keys("testuser123")
        email_field.send_keys("testuser123@example.com")
        password_field.send_keys("password123")
        confirm_password_field.send_keys("password123")
        dob_field.send_keys("2000-01-01")

        # Submit the form
        driver.find_element(By.CSS_SELECTOR, ".submit-button").click()

        # Wait for redirect to success page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )

        # Validate the success page content
        header = driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(header, "Hobbies App", "Header does not match on the success page")

        # Check if "Manage Profile" button is visible
        manage_profile_button = driver.find_element(By.LINK_TEXT, "Manage Profile")
        self.assertTrue(manage_profile_button.is_displayed(), "Manage Profile button is not visible")

        # Logout to clean up
        logout_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")
        logout_button.click()

        # Wait for redirect to login/signup page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Login"))
        )

        login_button = driver.find_element(By.LINK_TEXT, "Login")
        self.assertTrue(login_button.is_displayed(), "Login button is not visible after logout")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
