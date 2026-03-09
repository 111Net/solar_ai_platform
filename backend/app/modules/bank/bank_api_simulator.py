import random

def simulate_bank_approval(credit_score, default_probability):
    if credit_score > 750 and default_probability < 0.2:
        return {"approved": True, "interest_rate": 0.14}

    if credit_score > 650:
        return {"approved": True, "interest_rate": 0.18}

    return {"approved": False, "reason": "High risk profile"}