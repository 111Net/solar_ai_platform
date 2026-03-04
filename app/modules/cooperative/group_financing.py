def calculate_group_risk(members):
    total_income = sum(m["monthly_income"] for m in members)
    total_expenses = sum(m["monthly_expenses"] for m in members)

    group_surplus = total_income - total_expenses

    if group_surplus > 500000:
        return "LOW_RISK"
    elif group_surplus > 200000:
        return "MEDIUM_RISK"
    return "HIGH_RISK"