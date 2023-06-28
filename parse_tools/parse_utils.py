import requests
import os
from dotenv import load_dotenv
import asyncio
import time

from db_tools.db_tools import get_site_ids, insert_into_cars, get_data_of_single_id, update_data
from tg_tools.tg_tools import notify_user
load_dotenv()


API_KEY = os.environ.get('API_KEY')
CATEGORY_ID = 1  # Легковые авто
MARK_ID = 79  # Toyota
MODEL_ID = 2104  # Sequoia
DAMAGE = 1  # После ДТП
MATCH_COUNT = 840  # Пригнаны из США
COUNTPAGE = 100  # Кол-во результатов на странице


def make_request(url):
    try:
        response = requests.get(url)
        if response.status_code < 300:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return None


def get_data_by_site_id(id_num):
    title = year = price = race = city = link = 'Unknown'
    photo_links = []

    url = f'https://developers.ria.com/auto/info?api_key={API_KEY}&auto_id={id_num}'

    data = make_request(url)

    if data:
        price = data.get('USD', 0.0)
        link_to_view = data.get('linkToView', '')
        link = f'https://auto.ria.com/{link_to_view}'
        title = data.get('title', 'Unknown')
        year = data.get('autoData').get('year', 'Unknown')
        city = data.get('stateData', {}).get('name', 'Unknown')
        race = data.get('autoData', {}).get('race', 'Unknown')

        album = data.get('photoData', {}).get('all', [])
        if album:
            for i in range(5):
                try:
                    photo = f'https://cdn2.riastatic.com/photosnew/auto/photo/toyota_sequoia__{album[i]}f.jpg'
                except IndexError:
                    break
                else:
                    photo_links.append(photo)

    return title, year, price, race, city, link, photo_links


def process_item(r_id, resp_ids, site_ids, adds):
    r_id_title, r_id_year, r_id_price, r_id_race, r_id_city, r_id_link, photo_links = get_data_by_site_id(r_id)
    loop = asyncio.get_event_loop()
    if r_id not in site_ids:
        loop.run_until_complete(notify_user(
            r_id_title, r_id_year, r_id_price, r_id_race, r_id_city, r_id_link, photo_links))

        adds.append((r_id, r_id_price))
    else:
        price_db = get_data_of_single_id(r_id)
        if price_db != r_id_price:
            loop.run_until_complete(notify_user(
                r_id_title, r_id_year, r_id_price, r_id_race, r_id_city, r_id_link, photo_links,
                'ПОНОВЛЕННЯ ЦIНИ!!!:\n'))
            update_data('price', r_id_price, r_id)

    for s_id in site_ids:
        if s_id not in resp_ids:
            loop.run_until_complete(notify_user(
                r_id_title, r_id_year, r_id_price, r_id_race, r_id_city, r_id_link, photo_links,
                'ПРОДАНО!!!\n'))
            update_data('status', '"sold"', s_id)


def auto_ria_parse(pause):
    url = f"https://developers.ria.com/auto/search?api_key={API_KEY}&category_id={CATEGORY_ID}&marka_id={MARK_ID}" \
          f"&model_id={MODEL_ID}&damage={DAMAGE}&matched_country={MATCH_COUNT}&countpage={COUNTPAGE}"

    data = make_request(url)

    if data:
        resp_ids = data.get('result', {}).get('search_result', {}).get('ids', [])
        if resp_ids:
            site_ids = get_site_ids()
            adds = []
            for r_id in resp_ids:
                process_item(r_id, resp_ids, site_ids, adds)

            if adds:
                insert_into_cars(adds)

    time.sleep(pause)

    return auto_ria_parse(pause)
