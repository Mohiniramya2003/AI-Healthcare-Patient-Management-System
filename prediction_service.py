import google.generativeai as genai

genai.configure(
    api_key="YOUR_API_KEY"
)

model = genai.GenerativeModel("gemini-2.0-flash-lite")


def generate_health_prediction(
    glucose,
    haemoglobin,
    cholesterol
):

    prompt = f"""
    Glucose: {glucose}
    Haemoglobin: {haemoglobin}
    Cholesterol: {cholesterol}

    Predict health risk in one short sentence.
    """

    try:

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception:

        # Fallback prediction if Gemini quota is exceeded

        if glucose > 180:
            return "High glucose level detected. Medical consultation recommended."

        elif cholesterol > 240:
            return "High cholesterol level detected. Lifestyle changes recommended."

        elif haemoglobin < 10:
            return "Low haemoglobin detected. Possible anemia risk."

        else:
            return "Health parameters appear within acceptable range."
