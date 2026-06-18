from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Patient
from prediction_service import generate_health_prediction

from datetime import datetime
from email_validator import validate_email, EmailNotValidError


app = Flask(__name__)

CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


with app.app_context():
    db.create_all()



def validate_patient(data):

    required_fields = [
        "full_name",
        "date_of_birth",
        "email",
        "glucose",
        "haemoglobin",
        "cholesterol"
    ]

    for field in required_fields:
        if field not in data:
            return f"{field} is required"


    try:
        validate_email(data["email"])

    except EmailNotValidError:
        return "Invalid Email"


    dob = datetime.strptime(
        data["date_of_birth"],
        "%Y-%m-%d"
    )


    if dob.date() > datetime.today().date():
        return "DOB cannot be future date"


    return None



# Patient webpage
@app.route("/")
def home():
    return render_template("index.html")



# Get all patients
@app.route("/patients", methods=["GET"])
def get_patients():

    patients = Patient.query.all()

    return jsonify(
        [patient.to_dict() for patient in patients]
    )



# Get single patient
@app.route("/patients/<int:id>", methods=["GET"])
def get_patient(id):

    patient = Patient.query.get_or_404(id)

    return jsonify(patient.to_dict())



# Save patient
@app.route("/patients", methods=["POST"])
def create_patient():

    data = request.get_json()

    print("DATA RECEIVED:", data)


    if not data:
        return jsonify({
            "error": "No data received"
        }), 400



    error = validate_patient(data)

    if error:
        return jsonify({
            "error": error
        }), 400



    remarks = generate_health_prediction(
        float(data["glucose"]),
        float(data["haemoglobin"]),
        float(data["cholesterol"])
    )



    patient = Patient(

        full_name=data["full_name"],

        date_of_birth=data["date_of_birth"],

        email=data["email"],

        glucose=float(data["glucose"]),

        haemoglobin=float(data["haemoglobin"]),

        cholesterol=float(data["cholesterol"]),

        remarks=remarks
    )



    db.session.add(patient)

    db.session.commit()



    print("SAVED PATIENT:", patient.to_dict())


    return jsonify(patient.to_dict()), 201




# Update patient
@app.route("/patients/<int:id>", methods=["PUT"])
def update_patient(id):

    patient = Patient.query.get_or_404(id)

    data = request.get_json()


    error = validate_patient(data)

    if error:
        return jsonify({
            "error": error
        }), 400



    patient.full_name = data["full_name"]
    patient.date_of_birth = data["date_of_birth"]
    patient.email = data["email"]

    patient.glucose = float(data["glucose"])
    patient.haemoglobin = float(data["haemoglobin"])
    patient.cholesterol = float(data["cholesterol"])


    patient.remarks = generate_health_prediction(
        float(data["glucose"]),
        float(data["haemoglobin"]),
        float(data["cholesterol"])
    )


    db.session.commit()


    return jsonify(patient.to_dict())




# Delete patient
@app.route("/patients/<int:id>", methods=["DELETE"])
def delete_patient(id):

    patient = Patient.query.get_or_404(id)


    db.session.delete(patient)

    db.session.commit()


    return jsonify({
        "message": "Patient Deleted Successfully"
    })



if __name__ == "__main__":
    app.run(debug=True)