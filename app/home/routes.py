#  Url routes for home and dashboard


from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User
from app.extensions import db, login_manager, mongo
from . import bp
from app.auth.forms import RegisterForm, DeleteUserForm

from .forms import PatientStrokeRecordForm, DeletePatientForm

import math

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# general home route for all user in the system
@bp.route("/", methods=["GET"])
@login_required
def index():

    # pagination part
    page = int(request.args.get("page", 1))
    per_page_records = 10

    skip_records = (page - 1) * per_page_records



    try:
        patient_records  = mongo.db.records.find().skip(skip_records).limit(per_page_records)
        total_page = mongo.db.records.count_documents({}) // per_page_records 
    except Exception as e:
        flash("Error fetching patient records: " + str(e), "danger")
        patient_records = []


    next_page = page + 1    
    previous_page = page - 1 if page > 1 else 1

    return render_template(
        "home/index.html",
        patient_records=patient_records,
        next_page=next_page,
        previous_page=previous_page,
        current_page=page,
        total_page=total_page,
    )


#  specific dashboard route designed for admin.
@bp.route("admin-dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("home.index"))
    user_register_form = RegisterForm()
    user_delete_form = DeleteUserForm()
    users = User.query.all()
    return render_template("admin/admin-content.html", user_register_form=user_register_form, user_delete_form=user_delete_form, users=users)


# pateint detail route
@bp.route("/patient/<patient_id>", methods=["GET"])
@login_required
def patient_detail(patient_id):

    record = mongo.db.records.find_one({"id": int(patient_id)})

    if not record:
        flash("No Record Found", "warning")
        return redirect(url_for("home.index"))

    form = PatientStrokeRecordForm(data=record)
    delete_form = DeletePatientForm()

    return render_template("home/patient-detail.html", record=record, form=form, delete_form=delete_form)



# api for searching patient by id
@bp.route("/search-patient", methods=["GET"])
@login_required
def search_patient():
    patient_id = request.args.get("search_patient", None)
    if not patient_id:
        flash("Please provide a patient id to search.", "warning")
        return redirect(url_for("home.index"))
    
    record = mongo.db.records.find_one({"id": int(patient_id)})
    if not record:
        flash("No Record Found", "warning")
        return redirect(url_for("home.index"))
    
    return redirect(url_for("home.patient_detail", patient_id=patient_id))


# api route for updating patient record
@bp.route("/update-patient/<patient_id>", methods=["GET", "POST"])
@login_required
def update_patient_record(patient_id):
    patient_detail_form = PatientStrokeRecordForm(request.form)

    if patient_detail_form.validate_on_submit():
        # print(patient_detail_form.data)
        # Get current record from database to compare
        current_record = mongo.db.records.find_one({"id": int(patient_id)})
        
        if not current_record:
            flash("Patient record not found.", "danger")
            return redirect(url_for("home.index"))
        
        updated_patient_record = {
            "id": patient_detail_form.id.data,
            "gender": patient_detail_form.gender.data,
            "age": patient_detail_form.age.data,
            "hypertension": patient_detail_form.hypertension.data,
            "heart_disease": patient_detail_form.heart_disease.data,
            "ever_married": patient_detail_form.ever_married.data,
            "work_type": patient_detail_form.work_type.data,
            "Residence_type": patient_detail_form.Residence_type.data,
            "avg_glucose_level": patient_detail_form.avg_glucose_level.data,
            "bmi": patient_detail_form.bmi.data,
            "smoking_status": patient_detail_form.smoking_status.data,
            "stroke": patient_detail_form.stroke.data,
        }

        # check if there are any changes between current_record and updated_patient_record        
        has_changes = False
        for key, new_value in updated_patient_record.items():
            old_value = current_record.get(key)
            
            # Helper function to check if a value is null/None/NaN
            def is_null_or_nan(value):
                if value is None:
                    return True
                if isinstance(value, float) and math.isnan(value):
                    return True
                return False
            
            # for null/None/NaN values especially bmi that has nan in csv and soted nam but on updating form it is null - no change
            if is_null_or_nan(old_value) and is_null_or_nan(new_value):
                continue
        
            if is_null_or_nan(old_value) != is_null_or_nan(new_value):
                has_changes = True
                break
            
           
            if isinstance(new_value, (int, float)) and isinstance(old_value, (int, float)):
                if float(old_value) != float(new_value):
                    has_changes = True
                    break
            
            # Direct comparison for non-numeric values
            elif old_value != new_value:
                has_changes = True
                break
        
        if not has_changes:
            flash("No changes made to the patient record.", "info")
            return redirect(url_for("home.patient_detail", patient_id=patient_id))

        # print("Updating patient record:", updated_patient_record)

        result = mongo.db.records.update_one(
            {"id": int(patient_id)},
            {"$set": updated_patient_record}
        )

        # print(result.raw_result)
        # print("Modified Count:", result.modified_count)

        flash("Patient record updated successfully.", "success")
        
        return redirect(url_for("home.patient_detail", patient_id=patient_id))
    
    flash("Invalid Data please check and try again.", "danger")
    return redirect(url_for("home.patient_detail", patient_id=patient_id))    



# api for adding new patient record
@bp.route("/add-patient", methods=["GET", "POST"])
@login_required
def add_patient_record():
    patient_record_form = PatientStrokeRecordForm(request.form)

    if patient_record_form.validate_on_submit():
        # find id record already exists
        existing_record = mongo.db.records.find_one({"id": patient_record_form.id.data})
        if existing_record:
            flash("Patient record with this ID already exists.", "danger")
            return redirect(url_for("home.add_patient_record"))
        
        new_patient_record = {
            "id": patient_record_form.id.data,
            "gender": patient_record_form.gender.data,
            "age": patient_record_form.age.data,
            "hypertension": patient_record_form.hypertension.data,
            "heart_disease": patient_record_form.heart_disease.data,
            "ever_married": patient_record_form.ever_married.data,
            "work_type": patient_record_form.work_type.data,
            "Residence_type": patient_record_form.Residence_type.data,
            "avg_glucose_level": patient_record_form.avg_glucose_level.data,
            "bmi": patient_record_form.bmi.data,
            "smoking_status": patient_record_form.smoking_status.data,
            "stroke": patient_record_form.stroke.data,
        }

        result = mongo.db.records.insert_one(new_patient_record)

        flash("New patient record added successfully.", "success")
        return redirect(url_for("home.patient_detail", patient_id=new_patient_record["id"]))
    
    return render_template("home/add_record.html", form=patient_record_form)



# api for deleting patient record
@bp.route("/delete-patient/<patient_id>", methods=["POST"])
@login_required
def delete_patient_record(patient_id):
    if current_user.role != "admin":
        flash("Access denied. Only admin can delete patient records.", "danger")
        return redirect(url_for("home.index"))
    delete_form = DeletePatientForm()

    if not delete_form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("home.patient_detail", patient_id=patient_id))
    
    result = mongo.db.records.delete_one({"id": int(patient_id)})

    if result.deleted_count == 0:
        flash("Patient record not found.", "danger")
    else:
        flash("Patient record deleted successfully.", "success")
    
    return redirect(url_for("home.index"))