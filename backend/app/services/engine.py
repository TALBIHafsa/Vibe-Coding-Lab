from backend.app.schemas.sensor import SensorDataCreate, RecommendationResponse

# Configuration: thresholds (Could be moved to config.py or DB)
RULES_CONFIG = {
    "moisture_low": 30.0,
    "moisture_critical": 15.0,
    "moisture_high": 80.0,
    "moisture_heat_stress_threshold": 45.0,
    "temp_high": 30.0,
    "temp_low": 5.0,
    "fert_min_moisture": 40.0,
    "fert_optimal_temp_min": 20.0,
    "fert_optimal_temp_max": 30.0
}

def generate_recommendation(data: SensorDataCreate) -> RecommendationResponse:
    irrigation_msg = "Moisture levels are optimal."
    fert_msg = "Conditions not suitable for fertilization."
    action = False

    # --- IRRIGATION LOGIC ---
    if data.soil_moisture > RULES_CONFIG["moisture_high"]:
         irrigation_msg = "STOP: Overwatering risk. Risk of root rot."
    
    elif data.temperature < RULES_CONFIG["temp_low"]:
        irrigation_msg = "STOP: Temperature too low for irrigation."

    elif data.soil_moisture < RULES_CONFIG["moisture_critical"]:
        irrigation_msg = "ALARM: Critical drought! Water immediately."
        action = True

    elif data.temperature >= RULES_CONFIG["temp_high"] and data.soil_moisture < RULES_CONFIG["moisture_heat_stress_threshold"]:
        irrigation_msg = "ADVICE: High heat detected. Irrigation recommended to prevent heat stress."
        action = True

    elif data.soil_moisture < RULES_CONFIG["moisture_low"]:
        irrigation_msg = "ADVICE: Soil is dry. Standard irrigation recommended."
        action = True

    # --- FERTILIZATION LOGIC ---
    # Check "Blockers" first
    if data.soil_moisture < RULES_CONFIG["fert_min_moisture"]:
        fert_msg = "BLOCK: Soil too dry. Fertilizer may cause root burn."
    elif data.temperature > RULES_CONFIG["temp_high"]:
        fert_msg = "BLOCK: High heat. Fertilizer may induce stress."
    elif data.temperature < 10.0: # Dormancy
        fert_msg = "BLOCK: Plant dormant. Nutrient uptake low."
    # If no blockers, check for optimal range
    elif (RULES_CONFIG["fert_optimal_temp_min"] <= data.temperature <= RULES_CONFIG["fert_optimal_temp_max"]):
        fert_msg = "ADVICE: Optimal conditions for fertilization."
    
    return RecommendationResponse(
        status="Action Required" if action else "Stable",
        action_required=action,
        irrigation_advice=irrigation_msg,
        fertilizer_advice=fert_msg
    )