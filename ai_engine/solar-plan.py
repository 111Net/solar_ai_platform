from fastapi import Depends

@app.post("/solar-plan/", response_model=schemas.SolarPlanResponse)
def create_solar_plan(
    request: schemas.SolarPlanRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db_session)
):
    panel_size = calculate_panel_size(request.daily_energy_kwh, request.panel_efficiency)
    battery_capacity = calculate_battery_capacity(request.daily_energy_kwh, request.days_of_autonomy, request.battery_voltage)
    cost = estimate_cost(panel_size, battery_capacity)
    roi = calculate_roi(cost, request.daily_energy_kwh)

    plan = models.SolarPlan(
        user_id=current_user.id,
        daily_energy_kwh=request.daily_energy_kwh,
        days_of_autonomy=request.days_of_autonomy,
        panel_size_kw=panel_size,
        battery_capacity_kwh=battery_capacity,
        estimated_cost=cost,
        roi_years=roi
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan
#----------------------endpoint to list user's solar plans--------------------

@app.get("/solar-plans/", response_model=list[schemas.SolarPlanResponse])
def list_solar_plans(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db_session)
):
    plans = db.query(models.SolarPlan).filter(models.SolarPlan.user_id == current_user.id).all()
    return plans