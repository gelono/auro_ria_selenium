import asyncio
import time
import requests

from db_tools import get_site_ids, insert_into_cars, get_data_of_single_id, update_data, get_all_data
from tg_tools import notify_user
from utils import *


def auto_ria_parse(pause):
    try:
        print(API_KEY)
        response = requests.get(f"https://developers.ria.com/auto/search?api_key={API_KEY}&category_id={category_id}"
                           f"&marka_id={marka_id}&model_id={model_id}&damage={damage}&matched_country={matched_country}"
                           f"&countpage={countpage}")
    except Exception as e:
        print(e)
        response = None

    if response:
        status_code = response.status_code
        if 300 > status_code >= 200:
            try:
                data = response.json()
            except AttributeError as e:
                print(e)
                print("[INFO] XXX The response does not have JSON data XXX")
            else:
                resp_ids = data.get('result', {}).get('search_result', {}).get('ids', [])
                if resp_ids:
                    site_ids = get_site_ids()
                    adds = []
                    for r_id in resp_ids:
                        r_id_title, r_id_year, r_id_price, r_id_race, r_id_city, r_id_link, photo_links = \
                            get_data_by_site_id(r_id)
                        if r_id not in site_ids:
                            loop = asyncio.get_event_loop()
                            loop.run_until_complete(notify_user(
                                r_id_title, r_id_year, r_id_price, r_id_race, r_id_city, r_id_link, photo_links))

                            adds.append((r_id, r_id_price))
                        else:
                            price_db = get_data_of_single_id(r_id)
                            if price_db != r_id_price:
                                loop = asyncio.get_event_loop()
                                loop.run_until_complete(notify_user(
                                    r_id_title, r_id_year, r_id_price, r_id_race, r_id_city, r_id_link, photo_links,
                                    'ПОНОВЛЕННЯ ЦIНИ!!!:\n'))
                                update_data('price', r_id_price, r_id)

                        for s_id in site_ids:
                            if s_id not in resp_ids:
                                loop = asyncio.get_event_loop()
                                loop.run_until_complete(notify_user(
                                    r_id_title, r_id_year, r_id_price, r_id_race, r_id_city, r_id_link, photo_links,
                                    'ПРОДАНО!!!\n'))
                                update_data('status', '"sold"', s_id)

                    if adds:
                        insert_into_cars(adds)

    print(get_all_data())
    time.sleep(pause)

    return auto_ria_parse(600)


if __name__ == "__main__":
    auto_ria_parse(600)
