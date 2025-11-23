"""
Script to load patient records from a csv file into the MongoDB database.
"""
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.extensions import mongo
from flask import current_app


def load_patient_recoreds(file_path: str) -> None:
    """This function loads the patient data from a csv file to the MongoDB database."""

    app = create_app()

    with app.app_context():
        try:
            mongo.cx.admin.command("ping")  # checking mongodb connection
            print("Connected to MongoDB successfully.")
            df = pd.read_csv(file_path)

            # #  replace values with nan with none 
            # df['bmi']  = df['bmi'].apply(lambda bmi: None if pd.isna(bmi) else bmi)
            # Load data into MongoDB
            patient_records = df.to_dict(orient="records")

            if not patient_records:
                print("No records found in the CSV file.")
                return
            patient_record_collection = mongo.db.get_collection("records")
            patient_record_collection.insert_many(patient_records)
            print(
                f"Successfully loaded {len(patient_records)} records into the database."
            )

        except FileNotFoundError:
            print(f"The file {file_path} was not found in the given path, try providing correct path.")

        except Exception as e:
            print(f"Error : {e}")


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "../dataset/patient_records.csv")
    load_patient_recoreds(file_path)
