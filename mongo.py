import pymongo

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
database = mongo_client['test_db']
appointment_col = database["patient_appointment"]


def insert_appointment(appointment_dict):
    appointment_col.insert_one(appointment_dict)
    print("Appointment inserted!")
