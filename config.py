import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = "health_prediction_secret"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "health.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False