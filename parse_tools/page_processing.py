import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class PageProcessing:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 2)

    def get_title(self):
        try:
            title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[class="head"]'))).text
        except Exception:
            title = None
            print("No data for title")

        return title

    def get_price_usd(self):
        try:
            price_usd = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="price_value"]/strong'))).text
            price_usd = float(price_usd[:-1].strip().replace(' ', ''))
        except Exception:
            price_usd = None
            print("No data for price_usd")

        return price_usd

    def get_odometer(self):
        try:
            odometer = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="base-information bold"]/span[@class="size18"]'))).text
            odometer = int(odometer) * 1000
        except Exception as e:
            odometer = None
            print("No data for odometer")

        return odometer

    def get_username(self):
        locators = ('//section[@id="userInfoBlock"]//div[@class="seller_info_name bold"]',
                '//section[@id="userInfoBlock"]//a[@target="_blank"]')
        username = None
        for locator in locators:
            try:
                username = self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, locator))).text
                break
            except Exception:
                print("No data for username_locator")

        return username

    def get_phone_number(self):
        try:
            show_phone = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "показати")]')))
            self.driver.execute_script('arguments[0].click()', show_phone)
            time.sleep(0.5)

            phone_number  = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[class*="popup-successful-call"]'))).text
            phone_number = phone_number.replace(' ', '').replace(')', '').replace('(', '+38')
        except Exception:
            phone_number  = None
            print("No data for phone_number")

        return phone_number

    def get_image_url_count(self):
        try:
            image_urls = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//picture/img')))
        except Exception:
            print("No data for image_url_count")
            image_url = None
            images_count = None
        else:
            images_count = len(image_urls)
            image_url = image_urls[1].get_attribute('src')

        return image_url, images_count

    def get_car_number(self):
        try:
            car_number = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="state-num ua"]'))).text
            car_number = car_number.strip()
        except Exception:
            print("No data for car_number")
            car_number = None

        return car_number

    def get_car_vin(self):
        try:
            car_vin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="label-vin"]'))).text
        except Exception:
            print("No data for car_vin")
            car_vin = None

        return car_vin
