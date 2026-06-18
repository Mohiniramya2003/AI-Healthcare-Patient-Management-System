def generate_health_prediction(glucose, haemoglobin, cholesterol):

    risk = []

    if glucose > 140:
        risk.append("High Diabetes Risk")

    elif glucose > 100:
        risk.append("Pre-Diabetes Risk")

    if cholesterol > 240:
        risk.append("High Cholesterol Risk")

    elif cholesterol > 200:
        risk.append("Borderline Cholesterol")

    if haemoglobin < 12:
        risk.append("Possible Anemia")

    if not risk:
        return "Patient appears healthy based on provided values."

    return ", ".join(risk)