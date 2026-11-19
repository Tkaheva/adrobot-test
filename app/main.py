from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .keitaro_client import KeitaroClient
import requests

app = FastAPI(title="Adrobot Test")
client = KeitaroClient()

# --- Модели данных ---

class CampaignCreate(BaseModel):
    name: str
    geo: str
    offer_id: int

class OfferUpdate(BaseModel):
    action: str  # "add" или "remove"
    offer_id: int

# --- Эндпоинты ---

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
        error_msg = e.response.text if e.response is not None else str(e)
        raise HTTPException(status_code=400, detail=f"Ошибка от Keitaro: {error_msg}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")

    return {"message": "Campaign created successfully", "data": result}

# --- Вторая часть ТЗ: Редактор кампаний ---

@app.get("/api/campaigns")
def list_campaigns():
    """Вернуть список всех кампаний из Keitaro"""
    try:
        return client.get_campaigns()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка от Keitaro: {e.response.text}")

@app.put("/api/campaigns/{campaign_id}/offers")
def update_offers(campaign_id: int, data: OfferUpdate):
    """
    Добавить или удалить оффер в кампании.
    data.action: "add" или "remove"
    data.offer_id: ID оффера
    """
    try:
        # 1. Получаем текущее состояние кампании
        campaign = client.get_campaign(campaign_id)

        # 2. Ищем поток с офферами (тот, у которого schema == "landings")
        streams = campaign.get("streams", [])
        target_stream = None
        for stream in streams:
            if stream.get("schema") == "landings":
                target_stream = stream
                break

        if target_stream is None:
            raise HTTPException(
                status_code=400,
                detail="В кампании не найден поток с офферами (schema='landings')"
            )

        # 3. Меняем список офферов
        current_offers = target_stream.get("offers", [])
        if data.action == "add":
            # Проверяем, нет ли уже такого оффера, чтобы не дублировать
            if not any(o.get("offer_id") == data.offer_id for o in current_offers):
                current_offers.append({"offer_id": data.offer_id})
        elif data.action == "remove":
            current_offers = [
                o for o in current_offers
                if o.get("offer_id") != data.offer_id
            ]
        else:
            raise HTTPException(
                status_code=400,
                detail="Неверное действие. Используйте 'add' или 'remove'"
            )

        # 4. Обновляем поток в массиве streams
        target_stream["offers"] = current_offers

        # 5. Отправляем обновлённый список потоков через PUT
        result = client.update_campaign(campaign_id, {"streams": streams})

        return {
            "message": f"Оффер {data.offer_id} успешно {'добавлен' if data.action == 'add' else 'удалён'}",
            "campaign_id": campaign_id,
            "current_offers": current_offers
        }

    except requests.exceptions.HTTPError as e:
        error_msg = e.response.text if e.response is not None else str(e)
        raise HTTPException(status_code=400, detail=f"Ошибка от Keitaro: {error_msg}")