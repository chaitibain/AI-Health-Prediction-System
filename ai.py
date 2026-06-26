import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_health_recommendation(patient):

    prompt = f"""
You are an experienced physician.

Analyze the following patient's laboratory report.

Patient Details

Full Name: {patient.full_name}
Date of Birth: {patient.date_of_birth}
Email: {patient.email}

Medical Values

Glucose: {patient.glucose} mg/dL
Haemoglobin: {patient.haemoglobin} g/dL
Cholesterol: {patient.cholesterol} mg/dL

Please provide:

1. Overall Health Risk (Low / Moderate / High)

2. Interpretation of Glucose

3. Interpretation of Haemoglobin

4. Interpretation of Cholesterol

5. Possible health concerns

6. Diet recommendations

7. Lifestyle recommendations

8. Whether the patient should consult a doctor urgently

Keep the response professional, short and easy to understand.
"""

    response = model.generate_content(prompt)

    return response.text