import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get('API_KEY')
category_id = 1  # Легковые авто
marka_id = 79  # Toyota
model_id = 2104  # Sequoia
damage = 1  # После ДТП
matched_country = 840  # Пригнаны из США
countpage = 100  # Кол-во результатов на странице


def get_data_by_site_id(id_num):
    title = 'Unknown'
    year = 'Unknown'
    price = 'Unknown'
    race = 'Unknown'
    city = 'Unknown'
    link = 'Unknown'
    photo_links = []

    try:
        response = requests.get(f'https://developers.ria.com/auto/info?api_key={API_KEY}&auto_id={id_num}')
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
