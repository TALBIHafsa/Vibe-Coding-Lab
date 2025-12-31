from backend.app.schemas.sensor import SensorDataCreate, RecommendationResponse

def generate_recommendation(data: SensorDataCreate) -> RecommendationResponse:
    # Simple heuristic logic (Phase 4 will refine this) [cite: 121]
    irrigation_msg = "Optimal moisture levels."
    action = False
    
    # Basic drought risk logic [cite: 42]
    if data.soil_moisture < 30:
        irrigation_msg = "WARNING: Low soil moisture. Irrigation recommended immediately."
        action = True
    elif data.soil_moisture > 80:
        irrigation_msg = "ALERT: Overwatering risk. Stop irrigation." # [cite: 42]
        action = True

    # Simple logic for temperature/fertilizer context
    fert_msg = "Conditions suitable for standard fertilization."
    if data.temperature > 30:
        fert_msg = "High heat detected. Avoid fertilization to prevent root burn."

    return RecommendationResponse(
        status="Critical" if action else "Normal",
        action_required=action,
        irrigation_advice=irrigation_msg, # [cite: 40]
        fertilizer_advice=fert_msg        # [cite: 41]
    )