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