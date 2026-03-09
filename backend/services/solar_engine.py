# services/solar_engine.py

def calculate_panel_size(daily_energy_kwh: float, panel_efficiency: float) -> float:
    """
    Simple placeholder: panel size in kW
    Formula: panel_size = daily_energy_kwh / (5 * panel_efficiency)
    """
    return round(daily_energy_kwh / (5 * panel_efficiency), 2)

def calculate_battery_capacity(daily_energy_kwh: float, days_of_autonomy: int, battery_voltage: float) -> float:
    """
    Simple placeholder: battery capacity in kWh
    Formula: battery_capacity = daily_energy_kwh * days_of_autonomy
    """
    return round(daily_energy_kwh * days_of_autonomy, 2)

def estimate_cost(panel_size_kw: float, battery_capacity_kwh: float) -> float:
    """
    Simple placeholder: estimate cost in USD
    Assumes $1000 per kW of panels and $200 per kWh of batteries
    """
    return round(panel_size_kw * 1000 + battery_capacity_kwh * 200, 2)

def calculate_roi(total_cost: float, daily_energy_kwh: float) -> float:
    """
    Simple placeholder: ROI in years
    Assumes $0.15 per kWh savings, 365 days/year
    """
    annual_savings = daily_energy_kwh * 0.15 * 365
    if annual_savings == 0:
        return float('inf')  # Avoid division by zero
    return round(total_cost / annual_savings, 1)