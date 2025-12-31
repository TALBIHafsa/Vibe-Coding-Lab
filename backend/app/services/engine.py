from backend.app.schemas.sensor import SensorDataCreate, RecommendationResponse

def generate_recommendation(data: SensorDataCreate) -> RecommendationResponse:
    """
    Generates advice with distinct 'Action' and 'Explanation' components.
    """
    # Defaults
    irrig_status = "Keep Current State"
    irrig_explanation = "Conditions are stable."
    fert_status = "Wait"
    fert_explanation = "Conditions not optimal for nutrient uptake."
    action_needed = False
    
    # ---------------------------------------------------------
    # 1. IRRIGATION LOGIC (Prioritized by Severity)
    # ---------------------------------------------------------
    if data.soil_moisture < 15.0:
        irrig_status = "IRRIGATE IMMEDIATELY"
        irrig_explanation = "CRITICAL: Soil moisture is dangerously low (Drought risk)."
        action_needed = True
        
    elif data.soil_moisture > 80.0:
        irrig_status = "STOP IRRIGATION"
        irrig_explanation = "CRITICAL: Soil saturated. Risk of root rot and fungal infection."
        action_needed = True

    elif data.temperature > 30.0 and data.soil_moisture < 50.0:
        # Adjusted threshold (50%) to compensate for heat stress
        irrig_status = "IRRIGATE (Heat Compensation)"
        irrig_explanation = "High temperatures detected. Watering increased to offset transpiration."
        action_needed = True

    elif data.soil_moisture < 30.0:
        irrig_status = "IRRIGATE"
        irrig_explanation = "Soil moisture is below target threshold."
        action_needed = True

    else:
        irrig_status = "DO NOT WATER"
        irrig_explanation = "Moisture levels are sufficient for now."

    # ---------------------------------------------------------
    # 2. FERTILIZATION LOGIC (Safety First)
    # ---------------------------------------------------------
    if data.soil_moisture < 40.0:
        fert_status = "BLOCK FERTILIZER"
        fert_explanation = "Soil is too dry. Adding nutrients now causes root burn."
    
    elif data.soil_moisture > 80.0:
        fert_status = "BLOCK FERTILIZER"
        fert_explanation = "Soil is saturated. Nutrients will wash away (leaching)."

    elif data.temperature > 30.0:
        fert_status = "BLOCK FERTILIZER"
        fert_explanation = "High heat puts plant in stress. Feeding now causes damage."

    elif 20.0 <= data.temperature <= 30.0:
        fert_status = "APPLY FERTILIZER"
        fert_explanation = "Optimal temperature and moisture for nutrient absorption."
        action_needed = True # Flagging this as an action

    return RecommendationResponse(
        status="Action Required" if action_needed else "Stable",
        action_required=action_needed,
        irrigation_advice=f"{irrig_status} | {irrig_explanation}",
        fertilizer_advice=f"{fert_status} | {fert_explanation}",
        # Pass the source data back
        current_moisture=data.soil_moisture,
        current_temp=data.temperature,
        current_humidity=data.humidity
    )