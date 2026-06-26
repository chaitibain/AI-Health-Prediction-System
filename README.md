# AI Health Prediction System

## Overview
The AI Health Prediction System is a Flask-based web application that allows users to manage patient records and generate AI-powered health recommendations using the Google Gemini API.

## Features
- Add Patient
- View Patient Records
- Edit Patient Information
- Delete Patient Records
- Automatic BMI Calculation
- AI-powered Health Risk Assessment
- Personalized Health Recommendations
- SQLite Database Storage

## Technologies Used
- Python
- Flask
- SQLite
- SQLAlchemy
- Bootstrap 5
- Google Gemini API
- HTML
- CSS

## Project Structure

```
health_prediction_app/
│
├── app.py
├── ai.py
├── config.py
├── models.py
├── requirements.txt
├── templates/
├── static/
└── README.md
```

## Installation

1. Clone the repository

```bash
git clone <repository-url>
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

macOS/Linux

```bash
source venv/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

6. Run the application

```bash
python app.py
```

## Future Improvements
- PDF Health Report
- Dashboard Charts
- User Authentication
- Email Reports
- File Upload Support

## Author

Chaiti Bain