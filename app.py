from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

from config import Config
from models import db, Patient
from ai import generate_health_recommendation

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------------- HOME ---------------- #

@app.route("/")
def home():

    total = Patient.query.count()

    return render_template(
        "index.html",
        total=total
    )


# ---------------- VIEW PATIENTS ---------------- #

@app.route("/patients")
def patients():

    all_patients = Patient.query.order_by(Patient.id.desc()).all()

    return render_template(
        "patients.html",
        patients=all_patients
    )


# ---------------- ADD PATIENT ---------------- #

@app.route("/add-patient", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        full_name = request.form["full_name"].strip()
        date_of_birth = request.form["date_of_birth"]
        email = request.form["email"].strip()

        glucose = float(request.form["glucose"])
        haemoglobin = float(request.form["haemoglobin"])
        cholesterol = float(request.form["cholesterol"])

        # Validation
        if datetime.strptime(date_of_birth, "%Y-%m-%d").date() > datetime.today().date():
            return "Date of Birth cannot be in the future."

        patient = Patient(
            full_name=full_name,
            date_of_birth=date_of_birth,
            email=email,
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol
        )

        db.session.add(patient)
        db.session.commit()

        return redirect(url_for("patients"))

    return render_template("add_patient.html")


# ---------------- EDIT PATIENT ---------------- #

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == "POST":

        patient.full_name = request.form["full_name"]
        patient.date_of_birth = request.form["date_of_birth"]
        patient.email = request.form["email"]

        patient.glucose = float(request.form["glucose"])
        patient.haemoglobin = float(request.form["haemoglobin"])
        patient.cholesterol = float(request.form["cholesterol"])

        db.session.commit()

        return redirect(url_for("patients"))

    return render_template(
        "edit_patient.html",
        patient=patient
    )


# ---------------- DELETE ---------------- #

@app.route("/delete/<int:id>")
def delete(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)

    db.session.commit()

    return redirect(url_for("patients"))


# ---------------- AI PREDICTION ---------------- #

@app.route("/predict/<int:id>")
def predict(id):

    patient = Patient.query.get_or_404(id)

    remarks = generate_health_recommendation(patient)

    patient.remarks = remarks

    db.session.commit()

    return render_template(
        "prediction.html",
        patient=patient,
        recommendation=remarks
    )


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)