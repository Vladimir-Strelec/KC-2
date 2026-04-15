from django.shortcuts import render
from .models import SkinportData, SteamData, BitskinsData
from django.core.paginator import Paginator

from .utils import get_bitskins_price, get_steam_skins_full, get_skinport_price


def arbitrage_page(request):
    # get_steam_skins_full()
    # get_skinport_price()
    # get_bitskins_price()

    skinport = SkinportData.objects.first()
    steam = SteamData.objects.first()
    bitskins = BitskinsData.objects.first()

    if not skinport or not steam or not bitskins:
        return render(request, "market/arbitrage.html", {"result": []})

    # steam dict (ключ = имя)
    steam_dict = {s["name"]: s for s in steam.all_items_list if s.get("name")}
    bitskins_dict = {s["name"]: s for s in bitskins.all_items_list if s.get("name")}

    result = []

    for skin in skinport.all_items_list:
        name = skin.get("market_hash_name")

        if not name:
            continue

        steam_item = steam_dict.get(name)
        bitskins_item = bitskins_dict.get(name)

        if not steam_item or not bitskins_item:
            continue

        icon_hash = (
            steam_item.get("asset_description", {})
            .get("icon_url")
        )

        steam_icon = (
            f"https://steamcommunity-a.akamaihd.net/economy/image/{icon_hash}"
            if icon_hash else None
        )

        steam_price = steam_item.get("sell_price", 0) or 0
        skinport_price = skin.get("min_price", 0) or 0
        bitskins_price = bitskins_item.get("suggested_price", 0) or 0

        prices = {
            "steam": steam_price,
            "skinport": skinport_price,
            "bitskins": bitskins_price,
        }

        # убираем нули (иначе сломают min/max)
        valid_prices = {k: v for k, v in prices.items() if v > 0}

        if len(valid_prices) < 2:
            best_profit = 0
            best_route = None
        else:
            buy_market = min(valid_prices, key=valid_prices.get)
            sell_market = max(valid_prices, key=valid_prices.get)

            best_profit = round(valid_prices[sell_market] - valid_prices[buy_market], 2)
            best_route = f"{buy_market}_to_{sell_market}"

        result.append({
            "name": name,
            "skinport_price": skinport_price,
            "bitskins_price": bitskins_price,
            "steam_price": steam_price,
            "skinport_icon": steam_icon,
            "steam_icon": steam_icon,
            "profit": best_profit,
            "route": best_route,
        })

    # pagination
    paginator = Paginator(result, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "market/arbitrage.html", {
        "result": page_obj,
        "page_obj": page_obj
    })