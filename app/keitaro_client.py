import os
import requests

class KeitaroClient:
    def __init__(self):
        self.base_url = os.getenv("KEITARO_URL", "https://tlgk.host").rstrip("/")
        self.api_key = os.getenv("KEITARO_API_KEY")
        
        if not self.api_key:
            raise ValueError("KEITARO_API_KEY не задан в .env файле. Пожалуйста, добавьте его.")
            
        self.headers = {"Api-Key": self.api_key}

    def _get(self, endpoint: str, params: dict = None):
        """Базовый GET-запрос к API Keitaro"""
        r = requests.get(
            f"{self.base_url}/admin_api/v1/{endpoint}", 
            headers=self.headers, 
            params=params,
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

    # --- Методы для редактора кампаний (Вторая часть ТЗ) ---

    def get_campaigns(self):
        """Получить список всех кампаний"""
        return self._get("campaigns")

    def get_campaign(self, campaign_id: int):
        """Получить детали одной кампании (с потоками)"""
        # Просим Keitaro отдать кампанию вместе с потоками
        return self._get(f"campaigns/{campaign_id}", params={"with": "streams"})

    def update_campaign(self, campaign_id: int, payload: dict):
        """Обновить кампанию (передаём только те поля, которые меняем)"""
        r = requests.put(
            f"{self.base_url}/admin_api/v1/campaigns/{campaign_id}",
            headers=self.headers,
            json=payload,
            timeout=10
        )
        r.raise_for_status()
        return r.json()