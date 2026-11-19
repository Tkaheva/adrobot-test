from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from .keitaro_client import KeitaroClient
from .database import get_db
from sqlalchemy.orm import Session
import requests

app = FastAPI(title="Adrobot Test")
client = KeitaroClient()

class CampaignCreate(BaseModel):
    name: str
    geo: str
    offer_id: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/domains")
def get_domains():
    try:
        return client.get_domains()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка от Keitaro: {e.response.text}")

@app.post("/api/campaigns")
def create_campaign(data: CampaignCreate):
    # Формируем payload с реальными ID, которые мы нашли в Swagger
    payload = {
        "name": f"test_tkacheva_{data.name}",
        "alias": f"test_tkacheva_{data.name.lower().replace(' ', '_')}",
        "domain_id": 1813,         # ID домена kylovoa.com
        "group_id": 9799,          # ID группы "VZ adrobot test"
        "traffic_source_id": 836,  # ID источника "FOR TESTS"
        "streams": [
            {
                "name": "Google Stream",
                "type": "regular",
                "action_type": "http",
                "action_payload": "https://google.com",
                "schema": "redirect",
                "filters": [
                    {"name": "country", "mode": "accept", "payload": data.geo}
                ]
            },
            {
                "name": "Offer Stream",
                "type": "regular",
                "action_type": "http",
                "schema": "landings",
                "offers": [
                    {"offer_id": data.offer_id}
                ]
            }
        ]
    }
    
    try:
        result = client.create_campaign(payload)
    except requests.exceptions.HTTPError as e:
        # Если Keitaro вернул 400/422, показываем его ответ, чтобы понять, что не так
        error_msg = e.response.text if e.response is not None else str(e)
        raise HTTPException(status_code=400, detail=f"Ошибка от Keitaro: {error_msg}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")

    return {"message": "Campaign created successfully", "data": result}