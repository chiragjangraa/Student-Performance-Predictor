from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd
import joblib

app = FastAPI(title="Student Performance Predictor API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "student_performance_model.pkl"
CSV_PATH = BASE_DIR / "StudentPerformanceFactors.csv"

model = joblib.load(MODEL_PATH)
data = pd.read_csv(CSV_PATH)


class PredictionInput(BaseModel):
    Hours_Studied: float
    Attendance: float
    Parental_Involvement: str
    Access_to_Resources: str
    Extracurricular_Activities: str
    Sleep_Hours: float
    Previous_Scores: float
    Motivation_Level: str
    Internet_Access: str
    Tutoring_Sessions: float
    Family_Income: str
    Teacher_Quality: str
    School_Type: str
    Peer_Influence: str
    Physical_Activity: float
    Learning_Disabilities: str
    Parental_Education_Level: str
    Distance_from_Home: str
    Gender: str
    Grade_Level: int
    Current_Semester: int
    Class_Participation_Score: float


low_medium_high = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

yes_no = {
    "No": 0,
    "Yes": 1
}

gender_map = {
    "Male": 0,
    "Female": 1
}

school_map = {
    "Public": 0,
    "Private": 1
}

peer_map = {
    "Negative": 0,
    "Neutral": 1,
    "Positive": 2
}

education_map = {
    "High School": 0,
    "College": 1,
    "Postgraduate": 2
}

distance_map = {
    "Near": 0,
    "Moderate": 1,
    "Far": 2
}


def create_features(x: PredictionInput):

    parental = low_medium_high[x.Parental_Involvement]
    resources = low_medium_high[x.Access_to_Resources]
    motivation = low_medium_high[x.Motivation_Level]
    income = low_medium_high[x.Family_Income]
    teacher = low_medium_high[x.Teacher_Quality]

    extracurricular = yes_no[x.Extracurricular_Activities]
    internet = yes_no[x.Internet_Access]
    disabilities = yes_no[x.Learning_Disabilities]

    gender = gender_map[x.Gender]
    school = school_map[x.School_Type]
    peer = peer_map[x.Peer_Influence]
    education = education_map[x.Parental_Education_Level]
    distance = distance_map[x.Distance_from_Home]

    age = 18 + x.Grade_Level

    cumulative_gpa = 2.0 + (x.Previous_Scores - 60) * 0.04

    study_motivation_interaction = (
        x.Hours_Studied * motivation
    ) / 3

    attendance_parental_interaction = (
        x.Attendance * parental
    ) / 200

    resources_quality_interaction = resources * teacher

    hours_studied_squared = x.Hours_Studied ** 2

    sleep_hours_squared = (x.Sleep_Hours - 7) ** 2

    engagement_score = (
        (x.Attendance / 100) * 25
        + extracurricular * 25
        + x.Class_Participation_Score / 4
    )

    support_index = (
        parental
        + internet
        + income / 2
    )

    health_wellness_score = (
        (10 - abs(x.Sleep_Hours - 7))
        + x.Physical_Activity * 1.5
    )

    sleep_distance_from_optimal = abs(x.Sleep_Hours - 7)

    is_senior = 1 if x.Current_Semester >= 7 else 0

    is_sophomore = (
        1 if 3 <= x.Current_Semester < 5 else 0
    )

    return pd.DataFrame([{
        "Hours_Studied": x.Hours_Studied,
        "Attendance": x.Attendance,
        "Parental_Involvement": parental,
        "Access_to_Resources": resources,
        "Extracurricular_Activities": extracurricular,
        "Sleep_Hours": x.Sleep_Hours,
        "Previous_Scores": x.Previous_Scores,
        "Motivation_Level": motivation,
        "Internet_Access": internet,
        "Tutoring_Sessions": x.Tutoring_Sessions,
        "Family_Income": income,
        "Teacher_Quality": teacher,
        "School_Type": school,
        "Peer_Influence": peer,
        "Physical_Activity": x.Physical_Activity,
        "Learning_Disabilities": disabilities,
        "Parental_Education_Level": education,
        "Distance_from_Home": distance,
        "Gender": gender,
        "Grade_Level": x.Grade_Level,
        "Current_Semester": x.Current_Semester,
        "Age": age,
        "Class_Participation_Score": x.Class_Participation_Score,
        "Cumulative_GPA": cumulative_gpa,
        "Study_Motivation_Interaction": study_motivation_interaction,
        "Attendance_Parental_Interaction": attendance_parental_interaction,
        "Resources_Quality_Interaction": resources_quality_interaction,
        "Hours_Studied_Squared": hours_studied_squared,
        "Sleep_Hours_Squared": sleep_hours_squared,
        "Engagement_Score": engagement_score,
        "Support_Index": support_index,
        "Health_Wellness_Score": health_wellness_score,
        "Sleep_Distance_from_Optimal": sleep_distance_from_optimal,
        "Is_Senior": is_senior,
        "Is_Sophomore": is_sophomore
    }])


@app.get("/")
def home():
    return {
        "message": "Student Performance Predictor API is running",
        "status": "success"
    }


@app.post("/api/predict")
def predict_student(x: PredictionInput):

    features = create_features(x)

    prediction = float(model.predict(features)[0])

    if prediction >= 90:
        category = "Excellent"
    elif prediction >= 75:
        category = "Good"
    elif prediction >= 60:
        category = "Needs Improvement"
    else:
        category = "At Risk"

    return {
        "prediction": round(prediction, 2),
        "category": category
    }


@app.get("/api/model-details")
def model_details():

    return {
        "model": "Linear Regression",
        "features": 35,
        "description": "Student Performance Prediction Model"
    }