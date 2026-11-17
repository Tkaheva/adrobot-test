import os
import requests

class KeitaroClient:
    def __init__(self):
        self.base_url = os.getenv("KEITARO_URL", "https://tlgk.host").rstrip("/")
        self.api_key = os.getenv("KEITARO_API_KEY")
        self.headers = {"Api-Key": self.api_key} if self.api_key else {}

    def _get(self, endpoint: str, mock_data=None):
        """Универсальный метод с возможностью подмены на мок"""
        if not self.api_key:  # Если ключа нет — возвращаем заглушку
            print(f"[MOCK] GET {endpoint}")
            return mock_data or []
        
        r = requests.get(f"{self.base_url}/admin_api/v1/{endpoint}", headers=self.headers)
        r.raise_for_status()
        return r.json()

    def get_domains(self):
        return self._get("domains", [{"id": 1, "name": "test-domain.com"}])

    def get_groups(self):
        return self._get("groups", [{"id": 1, "name": "Test Group"}])

    def get_sources(self):
        return self._get("sources", [{"id": 1, "name": "Facebook"}])

    def get_offers(self):
        return self._get("offers", [{"id": 1, "name": "Test Offer"}])

    def create_campaign(self, payload: dict):
        if not self.api_key:
            print(f"[MOCK] POST campaigns: {payload}")
            return {"id": 999, "name": payload.get("name")}
        
        r = requests.post(f"{self.base_url}/admin_api/v1/campaigns", headers=self.headers, json=payload)
        r.raise_for_status()
        return r.json()