# import time
#
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from db_tools.db_tools import Connect
# from parse_tools.page_processing import PageProcessing
# from parse_tools.parse_utils import get_driver

# connect = Connect()
#
# data = [
#     {'url': 'url1', 'title': 'title1', 'price_usd': 4500, 'odometer': 10000, 'username': 'username1', 'phone_number': '+30001234533', 'image_url': 'image_url2', 'images_count': 4, 'car_number': 'car_number1', 'car_vin': 'car_vin1'},
#     {'url': 'url2', 'title': 'title2', 'price_usd': 9500, 'odometer': 12000, 'username': 'username3', 'phone_number': '+30001234578', 'image_url': 'image_url3', 'images_count': 5, 'car_number': 'car_number2', 'car_vin': 'car_vin2'},
#     {'url': 'url3', 'title': 'title3', 'price_usd': 3300, 'odometer': 13000, 'username': 'username4', 'phone_number': '+30001234570', 'image_url': 'image_url4', 'images_count': 6, 'car_number': 'car_number3', 'car_vin': 'car_vin3'}
# ]
#
# connect.alchemy_post_mult_data('public', 'info', data)

# def get_links(wait):
#     links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="m-link-ticket"]')))
#     links = [element.get_attribute('href') for element in links]
#     return links


# def pages_count(wait):
#     propositions = wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, 'span[id="floatingSearchResultsCount"]'))).text
#     propositions = int(propositions.replace(' ', ''))
#     pages = 1 + (propositions // 100) if propositions % 100 > 0 else propositions // 100
#     return pages


# def manager():
#     driver = get_driver(0)
#     driver.get(f'https://auto.ria.com/')
#     time.sleep(1)
#     wait = WebDriverWait(driver, 5)
#
#     pages = pages_count(wait)
#     connection = Connect()
#     for i in range(pages):
#         driver.get(f'https://auto.ria.com/uk/search/?lang_id=4&page={i}&countpage=100&indexName=auto&custom=1&abroad=2')
#         links = get_links(wait)
#         parse_data(links, 1, 0, 1, connection)


# def get_data_from_the_page(driver):
#     page_proc = PageProcessing(driver)
#     data_dict = dict()
#     data_dict['url'] = driver.current_url
#     data_dict['title'] = page_proc.get_title()
#     data_dict['price_usd'] = page_proc.get_price_usd()
#     data_dict['odometer'] = page_proc.get_odometer()
#     data_dict['username'] = page_proc.get_username()
#     data_dict['image_url'], data_dict['images_count'] = page_proc.get_image_url_count()
#     data_dict['car_number'] = page_proc.get_car_number()
#     data_dict['car_vin'] = page_proc.get_car_vin()
#     data_dict['phone_number'] = page_proc.get_phone_number()
#
#     return data_dict


# def parse_data(list_of_links, bot_num, start_index, step, connection):
#     driver = get_driver(bot_num, headless=True)
#     list_for_post = []
#     for i in range(start_index, 3, step):
#         driver.get(list_of_links[i])
#         data_dict = get_data_from_the_page(driver)
#         list_for_post.append(data_dict)
#
#     connection.alchemy_post_mult_data('public', 'info', list_for_post)



