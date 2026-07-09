from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import re

from config import Config
from models import db, Patient
from ai import generate_health_recommendation

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

def is_valid_email(email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    return re.match(pattern, email)

@app.route("/")
def home():

    total = Patient.query.count()

    return render_template(
        "index.html",
        total=total
    )

@app.route("/patients")
def patients():

    all_patients = Patient.query.order_by(
        Patient.id.desc()
    ).all()


    return render_template(
        "patients.html",
        patients=all_patients
    )

@app.route("/add-patient", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        full_name = request.form["full_name"].strip()

        date_of_birth = request.form["date_of_birth"]

        email = request.form["email"].strip()

        if not is_valid_email(email):

            return "Invalid Email! Please enter a valid email like example@gmail.com"

        existing_patient = Patient.query.filter_by(
            email=email
        ).first()


        if existing_patient:

            return "Email already exists! Please use a different email."

        if datetime.strptime(
            date_of_birth,
            "%Y-%m-%d"
        ).date() > datetime.today().date():


            return "Date of Birth cannot be in the future."

        try:

            glucose = float(
                request.form["glucose"]
            )

            haemoglobin = float(
                request.form["haemoglobin"]
            )

            cholesterol = float(
                request.form["cholesterol"]
            )

        except ValueError:

            return "Health values must be numbers only."

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

        return redirect(
            url_for("patients")
        )

    return render_template(
        "add_patient.html"
    )

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):


    patient = Patient.query.get_or_404(id)

    if request.method == "POST":

        email = request.form["email"].strip()

        if not is_valid_email(email):

            return "Invalid Email! Please enter a valid email like example@gmail.com"


        existing_patient = Patient.query.filter(

            Patient.email == email,

            Patient.id != id

        ).first()



        if existing_patient:

            return "Email already exists! Please use a different email."




        if datetime.strptime(

            request.form["date_of_birth"],

            "%Y-%m-%d"

        ).date() > datetime.today().date():


            return "Date of Birth cannot be in the future."


        try:


            patient.glucose = float(
                request.form["glucose"]
            )


            patient.haemoglobin = float(
                request.form["haemoglobin"]
            )


            patient.cholesterol = float(
                request.form["cholesterol"]
            )



        except ValueError:


            return "Health values must be numbers only."



        patient.full_name = request.form["full_name"].strip()


        patient.date_of_birth = request.form["date_of_birth"]


        patient.email = email





        db.session.commit()




        return redirect(
            url_for("patients")
        )





    return render_template(

        "edit_patient.html",

        patient=patient

    )



@app.route("/delete/<int:id>")
def delete(id):


    patient = Patient.query.get_or_404(id)


    db.session.delete(patient)


    db.session.commit()



    return redirect(
        url_for("patients")
    )




@app.route("/predict/<int:id>")
def predict(id):



    patient = Patient.query.get_or_404(id)




    remarks = generate_health_recommendation(
        patient
    )



    patient.remarks = remarks



    db.session.commit()




    return render_template(

        "prediction.html",

        patient=patient,

        recommendation=remarks

    )


if __name__ == "__main__":


    app.run(debug=True)