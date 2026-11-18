from fastapi import FastAPI, Depends
from pydantic import BaseModel
from .keitaro_client import KeitaroClient
from .database import get_db
from sqlalchemy.orm import Session

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
    return client.get_domains()

@app.post("/api/campaigns")
def create_campaign(data: CampaignCreate):
    # Логика формирования payload для Keitaro
    payload = {
        "name": f"test_tkacheva_{data.name}",
        "domain_id": 1813,  
        "group_id": 9799,
        "source_id": 836,
        "streams": [
            {
                "name": "Google Stream",
                "type": "regular",
                "action_type": "redirect",
                "action_payload": "https://google.com",
                "filters": [{"name": "geo", "mode": "accept", "payload": data.geo}]
            },
            {
                "name": "Offer Stream",
                "type": "regular",
                "action_type": "redirect",
                "offers": [{"id": data.offer_id}]
            }
        ]
    }
    result = client.create_campaign(payload)
    return {"message": "Campaign created (mock or real)", "data": result}