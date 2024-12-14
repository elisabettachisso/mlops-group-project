import pickle
import pandas as pd
from database import get_responses, get_all_responses
import matplotlib.pyplot as plt
import streamlit as st

model_path = 'model/random_forest_model.pkl'

def load_model():
    #load the saved model from the file. .pkl
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        raise FileNotFoundError("The model was not found. Make sure the file 'random_forest_model.pkl' is in the correct directory.")

def preprocess_data(gender, age, academic_pressure, cgpa, study_satisfaction, sleep_duration, 
                    dietary_habits, degree, suicidal_thoughts, study_hours, financial_stress, family_history):
    """
        Preprocess the data for the Machine Learning model.  
        Convert raw data into a DataFrame compatible with the model.
    """
    # mappings for categorical variables
    gender_mapping = {"Male": 0, "Female": 1}
    dietary_habits_mapping = {"Unhealthy": 0, "Moderate": 1, "Healthy": 2}
    degree_mapping = {"Diploma": 0, "Bachelor degree": 1, "Master degree": 2, "PhD": 3}
    suicidal_thoughts_mapping = {"Yes": 1, "No": 0}
    family_history_mapping = {"Yes": 1, "No": 0}
    sleep_duration_mapping = {
        '5-6 hours': 5.5,
        'Less than 5 hours': 4.5,
        '7-8 hours': 7.5,
        'More than 8 hours': 8.5,
        'Others': 0
    }

    # encode the categorical variables
    processed_data = {
        "Gender": [gender_mapping.get(gender, -1)],  # default: -1 for unknown values
        "Age": [age],
        "Academic Pressure": [academic_pressure],
        "CGPA": [cgpa],
        "Study Satisfaction": [study_satisfaction],
        "Sleep Duration": [sleep_duration_mapping.get(sleep_duration, 0)],  # updated encoding
        "Dietary Habits": [dietary_habits_mapping.get(dietary_habits, -1)],
        "Degree": [degree_mapping.get(degree, -1)],
        "Have you ever had suicidal thoughts ?": [suicidal_thoughts_mapping.get(suicidal_thoughts, -1)],
        "Work/Study Hours": [study_hours],
        "Financial Stress": [financial_stress],
        "Family History of Mental Illness": [family_history_mapping.get(family_history, -1)]
    }

    # convert to DataFrame
    df = pd.DataFrame(processed_data)
    return df

def predict_depression_risk(model, data):
    """
        Use the model to calculate the depression risk probability.  
        :param model: Loaded ML model.  
        :param data: Preprocessed data as a DataFrame.  
        :return: Risk percentage.       
    """
    probability = model.predict_proba(data)[0][1]  # probability of the "Depressed" class
    return round(probability * 100, 2)  # convert to percentage and round

def calculate_risk(gender, age, academic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, 
                   degree, suicidal_thoughts, study_hours, financial_stress, family_history):
    """
        Calculate the depression risk based on the user's data.  
        :return: Depression risk percentage.
    """
    # load the model
    model = load_model()
    
    # preprocess the data
    data = preprocess_data(
        gender, age, academic_pressure, cgpa, study_satisfaction,
        sleep_duration, dietary_habits, degree, suicidal_thoughts,
        study_hours, financial_stress, family_history
    )
    
    # calculate the risk
    risk_probability = model.predict_proba(data)[0][1]  # probability of the "Depressed" class
    risk_percentage = round(risk_probability * 100, 2)  # convert to percentage and round
    
    return risk_percentage

def avarage_risk_percentage(user_id):
    responses = get_responses(user_id)
    values = []
    for response in responses:
        selected_values = [response[2], response[3], response[4], response[5], response[6], response[7], response[8],
                           response[9], response[10], response[11], response[12], response[13]]               
        value = calculate_risk(*selected_values)
        values.append(value)
    if values:
        avarage_risk = sum(values) / len(values)
        return avarage_risk
    else:
        st.error("No questionnaire has been filled out yet!")    

def avarage_risk_percentage_allusers():
    responses = get_all_responses()
    if responses:
        values = []
        for response in responses:
            selected_values = [response[2], response[3], response[4], response[5], response[6], response[7], response[8],
                            response[9], response[10], response[11], response[12], response[13]]
                            
            value = calculate_risk(*selected_values)
            values.append(value)
        avarage_risk = sum(values) / len(values)
        return avarage_risk
    else: 
        return False

def preprocess_responses_user(user_id):
    responses = get_responses(user_id)

    sleep_duration_mapping = {
        '5-6 hours': 5.5,
        'Less than 5 hours': 4.5,
        '7-8 hours': 7.5,
        'More than 8 hours': 8.5,
        'Others': None
    }

    if responses:
        # convert the responses into a DataFrame
        columns = [
            "id", "user_id", "gender", "age", "academic_pressure", "cgpa",
            "study_satisfaction", "sleep_duration", "dietary_habits", "degree",
            "suicidal_thoughts", "study_hours", "financial_stress",
            "family_history", "timestamp"
        ]
        df = pd.DataFrame(responses, columns=columns)

        # ensure that "academic_pressure" is an integer, "cgpa" is a float, and convert the timestamp
        df['academic_pressure'] = pd.to_numeric(df['academic_pressure'], errors='coerce')
        df['cgpa'] = pd.to_numeric(df['cgpa'], errors='coerce')
        df['study_satisfaction'] = pd.to_numeric(df['study_satisfaction'], errors='coerce')
        df['study_hours'] = pd.to_numeric(df['study_hours'], errors='coerce')
        df['financial_stress'] = pd.to_numeric(df['financial_stress'], errors='coerce')
        df['sleep_duration_numeric'] = df['sleep_duration'].map(sleep_duration_mapping)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # remove invalid values
        df = df.dropna(subset=['academic_pressure', 'cgpa', 'study_satisfaction', 'study_hours', 'financial_stress'])
        df = df.dropna(subset=['sleep_duration_numeric'])
        # sort by timestamp
        df = df.sort_values(by='timestamp')

        return df
    else:
        st.error("No questionnaire has been filled out yet!")

def preprocess_all_responses():

    responses = get_all_responses()

    sleep_duration_mapping = {
        '5-6 hours': 5.5,
        'Less than 5 hours': 4.5,
        '7-8 hours': 7.5,
        'More than 8 hours': 8.5,
        'Others': None
    }

    if responses:
 
        columns = [
            "id", "user_id", "gender", "age", "academic_pressure", "cgpa",
            "study_satisfaction", "sleep_duration", "dietary_habits", "degree",
            "suicidal_thoughts", "study_hours", "financial_stress",
            "family_history", "timestamp"
        ]
        df = pd.DataFrame(responses, columns=columns)

        df['academic_pressure'] = pd.to_numeric(df['academic_pressure'], errors='coerce')
        df['cgpa'] = pd.to_numeric(df['cgpa'], errors='coerce')
        df['study_satisfaction'] = pd.to_numeric(df['study_satisfaction'], errors='coerce')
        df['study_hours'] = pd.to_numeric(df['study_hours'], errors='coerce')
        df['financial_stress'] = pd.to_numeric(df['financial_stress'], errors='coerce')
        df['sleep_duration_numeric'] = df['sleep_duration'].map(sleep_duration_mapping)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        df = df.dropna(subset=['academic_pressure', 'cgpa', 'study_satisfaction', 'study_hours', 'financial_stress'])

        df = df.sort_values(by='timestamp')

        return df
    
    else:
        st.error("No questionnaire has been filled out yet!")
