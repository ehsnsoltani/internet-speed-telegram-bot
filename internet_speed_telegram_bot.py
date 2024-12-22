import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import time

SPEED_TEST_LINK = "https://www.speedtest.net/"
TELEGRAM_LINK = "https://web.telegram.org/"
PHONE_NUMBER = "Your-Phone-Number"


class InternetSpeedTelegramBot:
    def __init__(self):
        self.down = 0
        self.up = 0
        self.chrome_options = Options()
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.maximize_window()
        self.ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, TimeoutException)
        self.wait = WebDriverWait(self.driver, 60, ignored_exceptions=self.ignored_exceptions)

    def get_internet_speed(self):
        """Get the Download and Upload speed from Speedtest.net"""
        self.driver.get(SPEED_TEST_LINK)
        self.wait.until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/a'))).click()

        # check the value of download and upload speed html element until it gives us a numeric value
        while True:
            time.sleep(1)
            self.down = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "download-speed"))).text

            self.up = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "upload-speed"))).text
            if self.up.replace(".", "").isnumeric() and self.down.replace(".", "").isnumeric():
                break

    def send_message_at_telegram(self, message):
        """Send Message by Telegram"""

        self.driver.get("https://web.telegram.org/")
        # pause the code and scan the QR code to log in
        input("Did you scan the QR code for login? if yes press Enter")

        time.sleep(3)

        # click on menu button
        try:
            menu_button = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="column-left"]/div/div/div[1]/div[1]/button')))
            print(1)

        except TimeoutException:
            menu_button = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="LeftMainHeader"]/div[1]/button')))
            print(2)

        finally:
            menu_button.click()


        # Get hold of menu options and then click on Contacts item
        try:
            menu_items = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="LeftMainHeader"]/div[1]/div/div[2]/div[2]')))
            print(1)

        except TimeoutException:
            menu_items = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "btn-menu-item")))
            print(2)


        for item in menu_items:
            if "Contacts" in item.text:
                item.click()


        # send keys to search input for finding the target contact and then click on it
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contacts-container"]/div[1]/div/input'))).send_keys("Myself")
        time.sleep(3)
        ul_tag = self.wait.until(EC.visibility_of_element_located((By.ID, "contacts")))
        all_a_tags = ul_tag.find_elements(By.TAG_NAME, "a")
        print(len(all_a_tags))
        for a in all_a_tags:
            if "Myself" in a.text:
                a.click()


        # Send message to Target Contact
        message_to_send = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="column-center"]/div/div/div[4]/div/div[1]/div/div[8]/div[1]/div[1]')))
        message_to_send.clear()
        message_to_send.send_keys(message)
        time.sleep(3)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="column-center"]/div/div/div[4]/div/div[5]/button'))).click()
