from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.prediction import generate_prediction, generate_forecast

router = APIRouter()

class UserInput(BaseModel):
    last_period: str
    cycle_length: int
    sleep_hours: Optional[float] = 8.0
    current_mood: Optional[str] = "Normal"

@router.post("/predict")
def predict(data: UserInput):
    return generate_prediction(data.last_period, data.cycle_length, data.sleep_hours or 8.0, data.current_mood or "Normal")

@router.post("/forecast")
def forecast(data: UserInput):
    return generate_forecast(data.last_period, data.cycle_length, data.sleep_hours or 8.0, data.current_mood or "Normal", days=7)