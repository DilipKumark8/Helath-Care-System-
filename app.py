from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Database Models
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    medical_history = db.Column(db.Text)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    amount = db.Column(db.Float)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

# Patient Management
@app.route('/patients')
def view_patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        medical_history = request.form['medical_history']
        new_patient = Patient(name=name, age=age, medical_history=medical_history)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('view_patients'))
    return render_template('add_patient.html')

# Doctor Management
@app.route('/doctors')
def view_doctors():
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        new_doctor = Doctor(name=name, specialization=specialization)
        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('view_doctors'))
    return render_template('add_doctor.html')

# Appointment Management
@app.route('/appointments')
def view_appointments():
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
        new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('view_appointments'))
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('add_appointment.html', patients=patients, doctors=doctors)

# Billing Management
@app.route('/billings')
def view_billings():
    billings = Billing.query.all()
    return render_template('billings.html', billings=billings)

@app.route('/add_billing', methods=['GET', 'POST'])
def add_billing():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        amount = request.form['amount']
        new_billing = Billing(appointment_id=appointment_id, amount=amount)
        db.session.add(new_billing)
        db.session.commit()
        return redirect(url_for('view_billings'))
    appointments = Appointment.query.all()
    return render_template('add_billing.html', appointments=appointments)

# Delete Patient
@app.route('/delete_patient/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get(id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
    return redirect(url_for('view_patients'))

# Delete Doctor
@app.route('/delete_doctor/<int:id>', methods=['POST'])
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
    return redirect(url_for('view_doctors'))

# Delete Appointment
@app.route('/delete_appointment/<int:id>', methods=['POST'])
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
    return redirect(url_for('view_appointments'))

# Delete Billing
@app.route('/delete_billing/<int:id>', methods=['POST'])
def delete_billing(id):
    billing = Billing.query.get(id)
    if billing:
        db.session.delete(billing)
        db.session.commit()
    return redirect(url_for('view_billings'))


# Run the app
if __name__ == '__main__':
    with app.app_context():  # Ensure app context is available
        db.create_all()  # Creates the database tables
    app.run(debug=True)
