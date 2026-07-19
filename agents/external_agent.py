import requests
from config import AIConfig

class ExternalAgent:
    def __init__(self):
        self.weather_key = AIConfig.OPENWEATHER_KEY
        self.alpha_key = AIConfig.ALPHA_VANTAGE_KEY
        self.news_key = AIConfig.NEWS_API_KEY
        self._cache = {}
    
    def get_weather(self, city="Delhi"):
        cache_key = f"weather_{city}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        if not self.weather_key:
            return None
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.weather_key}&units=metric"
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            if "list" in data:
                self._cache[cache_key] = data["list"][:3]
                return self._cache[cache_key]
            return None
        except:
            return None
    
    def get_cotton_price(self):
        if "cotton" in self._cache:
            return self._cache["cotton"]
        if not self.alpha_key:
            return None
        url = f"https://www.alphavantage.co/query?function=COTTON&apikey={self.alpha_key}"
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            price = data.get("price", None)
            if price:
                self._cache["cotton"] = price
            return price
        except:
            return None
    
    def get_news(self, query="cooperative business"):
        if not self.news_key:
            return []
        cache_key = f"news_{query}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={self.news_key}&pageSize=5"
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            articles = data.get("articles", [])
            result = [{"title": a["title"], "source": a["source"]["name"], "published": a["publishedAt"]} for a in articles]
            self._cache[cache_key] = result
            return result
        except:
            return []
    
    def get_exchange_rate(self, from_cur="USD", to_cur="INR"):
        cache_key = f"fx_{from_cur}_{to_cur}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        url = f"https://api.frankfurter.app/latest?from={from_cur}&to={to_cur}"
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            rate = data["rates"].get(to_cur)
            if rate:
                self._cache[cache_key] = rate
            return rate
        except:
            return None
    
    def get_all(self):
        return {
            "weather": self.get_weather(),
            "cotton": self.get_cotton_price(),
            "news": self.get_news(),
            "exchange": self.get_exchange_rate()
        }
