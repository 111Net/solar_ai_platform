# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.solar_engine import (
    calculate_panel_size,
    calculate_battery_capacity,
    estimate_cost,
    calculate_roi
)
import uvicorn

app = FastAPI(title="Solar As A Service API")

# Request body model
class SolarPlanRequest(BaseModel):
    daily_energy_kwh: float
    days_of_autonomy: int
    panel_efficiency: float = 0.18  # default 18%
    battery_voltage: float = 12.0

# Response model
class SolarPlanResponse(BaseModel):
    panel_size_kw: float
    battery_capacity_kwh: float
    estimated_cost: float
    roi_years: float

@app.post("/solar-plan", response_model=SolarPlanResponse)
def solar_plan(request: SolarPlanRequest):
    try:
        panel_size = calculate_panel_size(
            daily_energy_kwh=request.daily_energy_kwh,
            panel_efficiency=request.panel_efficiency
        )
        battery_capacity = calculate_battery_capacity(
            daily_energy_kwh=request.daily_energy_kwh,
            days_of_autonomy=request.days_of_autonomy,
            battery_voltage=request.battery_voltage
        )
        cost = estimate_cost(panel_size, battery_capacity)
        roi = calculate_roi(cost, request.daily_energy_kwh)

        return SolarPlanResponse(
            panel_size_kw=panel_size,
            battery_capacity_kwh=battery_capacity,
            estimated_cost=cost,
            roi_years=roi
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# This allows running with: python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)