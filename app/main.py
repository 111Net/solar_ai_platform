from fastapi import FastAPI, Depends
from app.schemas import SolarPlanRequest
from app.modules.solar_design.sizing import calculate_system_size
from app.modules.risk_engine.credit_score import calculate_credit_score
from app.modules.ml.default_model import DefaultPredictionModel
from app.modules.bank.bank_api_simulator import simulate_bank_approval

app = FastAPI()

@app.post("/solar-plan")
def solar_plan(request: SolarPlanRequest):

    system = calculate_system_size(request.daily_kwh)

    credit_score = calculate_credit_score({
        "monthly_income": request.monthly_income,
        "monthly_expenses": request.monthly_expenses
    })

    model = DefaultPredictionModel()
    model.load()

    default_prob = model.predict_default_probability([
        request.monthly_income,
        request.monthly_expenses,
        credit_score,
        8
    ])

    bank_decision = simulate_bank_approval(credit_score, default_prob)

    return {
        "system_design": system,
        "credit_score": credit_score,
        "default_probability": default_prob,
        "bank_decision": bank_decision
    }