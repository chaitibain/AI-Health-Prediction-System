from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    bmi = db.Column(db.Float)

    blood_pressure = db.Column(db.String(30))
    blood_sugar = db.Column(db.Float)

    smoking = db.Column(db.String(20))
    exercise = db.Column(db.String(50))

    prediction = db.Column(db.Text)
    recommendation = db.Column(db.Text)

    def __repr__(self):
        return f"<Patient {self.name}>"