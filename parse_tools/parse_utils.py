import random
import threading
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import os
import subprocess
from dotenv import load_dotenv

from db_tools.db_tools import Connect
from parse_tools.page_processing import PageProcessing

# Load the environment variables from the .env file
load_dotenv()
CHROME_PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH")
BOT_NUMBERS = int(os.getenv("BOT_NUMBERS"))
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

class ParseUtils:
    @staticmethod
    def get_driver(bot: int, headless=False):
        ua = UserAgent()
        random_user_agent = ua.random

        options = chrome_options()
        options.add_argument(f"user-agent={random_user_agent}")
        options.add_argument("--headless") if headless else None
        options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}/AutoriaProfile_{bot}")
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        return driver

    @staticmethod
    def get_data_from_the_page(driver: webdriver.Chrome):
        page_proc = PageProcessing(driver)
        data_dict = dict()
        data_dict['url'] = driver.current_url
        data_dict['title'] = page_proc.get_title()
        data_dict['price_usd'] = page_proc.get_price_usd()
        data_dict['odometer'] = page_proc.get_odometer()
        data_dict['username'] = page_proc.get_username()
        data_dict['image_url'], data_dict['images_count'] = page_proc.get_image_url_count()
        data_dict['car_number'] = page_proc.get_car_number()
        data_dict['car_vin'] = page_proc.get_car_vin()
        data_dict['phone_number'] = page_proc.get_phone_number()

        return data_dict

    def parse_data(self, list_of_links: list, bot_num: int, start_index: int, step: int, connection: Connect, sleep=0.5):
        driver = self.get_driver(bot_num, headless=True)
        list_for_post = []
        loop = 0
        for i in range(start_index, len(list_of_links), step):
            loop += 1
            print(f'Bot#{bot_num}: loop - {loop}')
            time.sleep(sleep)
            driver.get(list_of_links[i])
            data_dict = self.get_data_from_the_page(driver)
            list_for_post.append(data_dict)

        try:
            connection.alchemy_post_mult_data('public', 'info', list_for_post)
            print('Data has been inserted into DB')
        except Exception:
            print('Error while working with DB')

    @staticmethod
    def get_links(wait: WebDriverWait):
        links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="m-link-ticket"]')))
        links = [element.get_attribute('href') for element in links]
        return links

    @staticmethod
    def pages_count(wait: WebDriverWait):
        propositions = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[id="floatingSearchResultsCount"]'))).text
        propositions = int(propositions.replace(' ', ''))
        pages = 1 + (propositions // 100) if propositions % 100 > 0 else propositions // 100
        return pages

    def manager(self):
        driver = self.get_driver(0)
        driver.get(f'https://auto.ria.com/uk/search/?lang_id=4&page={0}&countpage=100&indexName=auto&custom=1&abroad=2')
        time.sleep(1)
        wait = WebDriverWait(driver, 5)

        pages = self.pages_count(wait)
        connection = Connect()
        for i in range(pages):
            driver.get(f'https://auto.ria.com/uk/search/?lang_id=4&page={i}&countpage=100&indexName=auto&custom=1&abroad=2')
            links = self.get_links(wait)
            self.run_threads(connection, BOT_NUMBERS, links)

    def run_threads(self, connection: Connect, bot_numbers: int, links: list):
        threads = []
        random_sleep = [0.2, 0.3, 0.4]
        for i in range(bot_numbers):
            t = threading.Thread(target=self.parse_data,
                                 args=(links, i+1, i, bot_numbers, connection, random.choice(random_sleep)))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()

    @staticmethod
    def bd_dump():
        output_file = 'backup.dump'
        try:
            command = [
                'pg_dump',
                '-h', 'localhost',
                '-U', DB_USER,
                '-d', DB_NAME,
                '-F', 'c',  # dump format (custom)
                '-f', output_file
            ]

            subprocess.run(command, check=True)

            print(f"DB dump '{DB_NAME}' has been created in '{output_file}'")
        except Exception as e:
            print(f"Error while dump creating: {e}")
