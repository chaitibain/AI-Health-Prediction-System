from flask import Flask, render_template, request, redirect, url_for

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


# ---------------- VIEW ALL PATIENTS ---------------- #

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

        height = float(request.form["height"])
        weight = float(request.form["weight"])

        bmi = weight / ((height / 100) ** 2)

        blood_sugar = request.form["blood_sugar"]
        blood_sugar = float(blood_sugar) if blood_sugar else None

        patient = Patient(

            name=request.form["name"],
            age=int(request.form["age"]),
            gender=request.form["gender"],

            height=height,
            weight=weight,

            bmi=round(bmi, 2),

            blood_pressure=request.form["blood_pressure"],
            blood_sugar=blood_sugar,

            smoking=request.form["smoking"],
            exercise=request.form["exercise"]

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

        patient.name = request.form["name"]
        patient.age = int(request.form["age"])
        patient.gender = request.form["gender"]

        patient.height = float(request.form["height"])
        patient.weight = float(request.form["weight"])

        patient.bmi = round(
            patient.weight / ((patient.height / 100) ** 2),
            2
        )

        patient.blood_pressure = request.form["blood_pressure"]

        blood_sugar = request.form["blood_sugar"]
        patient.blood_sugar = float(blood_sugar) if blood_sugar else None

        patient.smoking = request.form["smoking"]
        patient.exercise = request.form["exercise"]

        db.session.commit()

        return redirect(url_for("patients"))

    return render_template(
        "edit_patient.html",
        patient=patient
    )


# ---------------- DELETE PATIENT ---------------- #

@app.route("/delete/<int:id>")
def delete(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)

    db.session.commit()

    return redirect(url_for("patients"))

@app.route("/predict/<int:id>")
def predict(id):

    patient = Patient.query.get_or_404(id)

    recommendation = generate_health_recommendation(patient)

    patient.recommendation = recommendation

    db.session.commit()

    return render_template(
        "prediction.html",
        patient=patient,
        recommendation=recommendation
    )
# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)