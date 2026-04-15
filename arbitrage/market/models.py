from django.db import models


class BaseMarketData(models.Model):
    all_items_list = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)

    def save_data(self, data):
        self.all_items_list = data
        self.save()

    class Meta:
        abstract = True


class SkinportData(BaseMarketData):
    pass


class SteamData(BaseMarketData):
    pass


class BitskinsData(BaseMarketData):
    pass


class Skin(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название скина
    steam_price = models.FloatField(default=0.0)           # Цена на Steam
    skinport_price = models.FloatField(default=0.0)        # Цена на Skinport
    bitskins_price = models.FloatField(default=0.0)        # Цена на Bitskins
    last_update = models.DateTimeField(auto_now=True)      # Когда обновляли

    @property
    def best_deal(self):
        prices = {
            "Steam": self.steam_price,
            "Skinport": self.skinport_price,
            "Bitskins": self.bitskins_price
        }
        buy = min(prices, key=prices.get)
        sell = max(prices, key=prices.get)
        profit = round(prices[sell] - prices[buy], 2)
        return {
            "buy": buy,
            "sell": sell,
            "profit": profit
        }

    @property
    def profit(self):
        return self.best_deal["profit"]

    @property
    def buy(self):
        prices = {
            'Steam': self.steam_price,
            'Skinport': self.skinport_price,
            'Bitskins': self.bitskins_price
        }
        # минимальная цена — место для покупки
        return min(prices, key=prices.get)

    @property
    def sell(self):
        prices = {
            'Steam': self.steam_price,
            'Skinport': self.skinport_price,
            'Bitskins': self.bitskins_price
        }
        # максимальная цена — место для продажи
        return max(prices, key=prices.get)

    def __str__(self):
        return self.name
