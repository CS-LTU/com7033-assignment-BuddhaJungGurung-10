from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional

# patient stroke record form
class PatientStrokeRecordForm(FlaskForm):
    id = IntegerField("ID", validators=[DataRequired()])
    gender = SelectField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        validators=[DataRequired()],
    )
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=0, max=120)])
    hypertension = SelectField(
        "Hypertension",
        choices=[(0, "No hypertension"), (1, "Has hypertension")],
        validators=[InputRequired()],
        coerce=int,
    )
    heart_disease = SelectField(
        "Heart Disease",
        choices=[(0, "No heart disease"), (1, "Has heart disease")],
        validators=[InputRequired()],
        coerce=int,
    )
    ever_married = SelectField(
        "Ever Married",
        choices=[("Yes", "Yes"), ("No", "No")],
        validators=[DataRequired()],
    )
    work_type = SelectField(
        "Work Type",
        choices=[
            ("children", "Children"),
            ("Govt_job", "Government Job"),
            ("Never_worked", "Never Worked"),
            ("Private", "Private"),
            ("Self-employed", "Self Employed"),
        ],
        validators=[DataRequired()],
    )
    Residence_type = SelectField(
        "Residence Type",
        choices=[("Urban", "Urban"), ("Rural", "Rural")],
        validators=[DataRequired()],
    )
    avg_glucose_level = FloatField(
        "Average Glucose Level", validators=[DataRequired(), NumberRange(min=0)]
    )
    bmi = FloatField("BMI", validators=[Optional()])
    smoking_status = SelectField(
        "Smoking Status",
        choices=[
            ("formerly smoked", "Formerly Smoked"),
            ("never smoked", "Never Smoked"),
            ("smokes", "Smokes"),
            ("Unknown", "Unknown"),
        ],
        validators=[DataRequired()],
    )
    stroke = SelectField(
        "Stroke",
        choices=[(0, "No Stroke"), (1, "Had a Stroke")],
        validators=[InputRequired()],
        coerce=int,
    )

    submit = SubmitField("Submit")

# Form for deleting a patient record (csrf protection only)
class DeletePatientForm(FlaskForm):
    pass