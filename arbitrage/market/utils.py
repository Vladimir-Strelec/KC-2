import json
import os

from dotenv import load_dotenv
import requests
import time

from .models import SkinportData, SteamData, BitskinsData

load_dotenv()


def get_steam_skins_full():
    start = 0
    all_items = []

    while True:
        data = get_skins_page(start)

        if not data:
            break

        results = data.get("results", [])
        if not results:
            break

        all_items.extend(results)
        start += 100

        total = data.get("total_count", 0)
        if total and start >= total:
            break

    steam_data_obj = SteamData()
    steam_data_obj.save_data(all_items)



BASE_URL = "https://steamcommunity.com/market/search/render/"


def get_skins_page(start=0):
    params = {
        "appid": 730,
        "norender": 1,
        "count": 100,
        "start": start,
        "query": ""
    }

    r = requests.get(BASE_URL, params=params)

    if r.status_code != 200:
        return None

    return r.json()


def get_skinport_price():
    url = "https://api.skinport.com/v1/items"
    params = {
        "app_id": 730,
        "currency": "EUR",
        "tradable": "true",

    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    time.sleep(1)
    data = response.json()

    skinport_data_obj = SkinportData()
    if isinstance(data, list):
        skinport_data_obj.save_data(data=data)
    else:
        return None


def get_bitskins_price():
    auth_key = os.getenv("API_KEY")

    headers = {'x-apikey': auth_key}
    res = requests.get('https://api.bitskins.com/market/skin/730', headers=headers)
    response = json.loads(res.text)
    bitskins_data_obj = BitskinsData()
    bitskins_data_obj.save_data(data=response)


def normalize_name(name):
    # убираем спецсимволы и лишние пробелы
    name = name.lower().replace('|', '').replace('(', '').replace(')', '')
    return ' '.join(name.split())  # убираем двойные пробелы