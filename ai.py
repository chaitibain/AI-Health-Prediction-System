import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_health_recommendation(patient):

    prompt = f"""
You are an experienced doctor.

Patient Information:

Name: {patient.name}
Age: {patient.age}
Gender: {patient.gender}

Height: {patient.height} cm
Weight: {patient.weight} kg
BMI: {patient.bmi}

Blood Pressure: {patient.blood_pressure}
Blood Sugar: {patient.blood_sugar}

Smoking: {patient.smoking}
Exercise: {patient.exercise}

Based on this information:

1. Predict overall health risk (Low, Moderate, High).
2. Explain why.
3. Give 5 health recommendations.
4. Suggest lifestyle improvements.

Keep the response short and easy to understand.
"""

    response = model.generate_content(prompt)

    return response.text