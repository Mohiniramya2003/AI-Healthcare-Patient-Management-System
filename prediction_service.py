import google.generativeai as genai

genai.configure(
    api_key"ADD_YOUR_GEMINI_API_KE" 
)

model = genai.GenerativeModel("gemini-flash-latest")


def generate_health_prediction(
    glucose,
    haemoglobin,
    cholesterol
):

    prompt = f"""
    You are a healthcare AI assistant.

    Analyze the following patient health parameters:

    Glucose: {glucose}
    Haemoglobin: {haemoglobin}
    Cholesterol: {cholesterol}

    Provide:
    1. Health assessment
    2. Possible risks
    3. Short recommendation

    Keep the response within 2 sentences.
    """

    try:

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:

        return f"AI Service Error: {str(e)}"
