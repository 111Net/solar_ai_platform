from pydantic import BaseModel, Field, EmailStr

class SolarPlanRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    location: str
    bvn: str = Field(min_length=11, max_length=11)
    daily_kwh: float = Field(gt=0)
    monthly_income: float = Field(gt=0)
    monthly_expenses: float = Field(ge=0)
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    class Config:
        orm_mode = True

class SolarPlanRequest(BaseModel):
    daily_energy_kwh: float
    days_of_autonomy: int
    panel_efficiency: float = 0.18
    battery_voltage: float = 12.0

class SolarPlanResponse(BaseModel):
    id: int
    daily_energy_kwh: float
    days_of_autonomy: int
    panel_size_kw: float
    battery_capacity_kwh: float
    estimated_cost: float
    roi_years: float
    created_at: str
    class Config:
        orm_mode = True
