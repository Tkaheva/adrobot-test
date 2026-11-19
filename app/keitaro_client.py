import os
import requests

class KeitaroClient:
    def __init__(self):
        self.base_url = os.getenv("KEITARO_URL", "https://tlgk.host").rstrip("/")
        self.api_key = os.getenv("KEITARO_API_KEY")
        
        if not self.api_key:
            raise ValueError("KEITARO_API_KEY не задан в .env файле. Пожалуйста, добавьте его.")
            
        self.headers = {"Api-Key": self.api_key}

    def _get(self, endpoint: str):
        """Базовый GET-запрос к API Keitaro"""
        r = requests.get(
            f"{self.base_url}/admin_api/v1/{endpoint}", 
            headers=self.headers, 
            timeout=10
        )
        r.raise_for_status()
        return r.json()

    def get_domains(self):
        return self._get("domains")

    def get_groups(self):
        return self._get("groups")

    def get_sources(self):
        # В API Keitaro эндпоинт называется именно traffic_sources
        return self._get("traffic_sources")

    def get_offers(self):
        return self._get("offers")

    def create_campaign(self, payload: dict):
        """Создает кампанию с вложенными потоками"""
        r = requests.post(
            f"{self.base_url}/admin_api/v1/campaigns", 
            headers=self.headers, 
            json=payload,
            timeout=10
        )
        r.raise_for_status()
        return r.json()