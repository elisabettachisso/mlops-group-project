import pickle
import pandas as pd
from database import get_responses
import matplotlib.pyplot as plt

def load_model():
    """Carica il modello salvato dal file .pkl."""
    try:
        with open('model/random_forest_model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        raise FileNotFoundError("Il modello non è stato trovato. Assicurati che il file 'random_forest_model.pkl' sia nella directory corretta.")

def preprocess_data(gender, age, academic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts, study_hours, financial_stress, family_history):
    """
    Preprocessa i dati per il modello di Machine Learning.
    Converte i dati grezzi in un DataFrame compatibile con il modello.
    """
    # Mappature per le variabili categoriali
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

    # Codifica le variabili categoriali
    processed_data = {
        "Gender": [gender_mapping.get(gender, -1)],  # Default: -1 per valori sconosciuti
        "Age": [age],
        "Academic Pressure": [academic_pressure],
        "CGPA": [cgpa],
        "Study Satisfaction": [study_satisfaction],
        "Sleep Duration": [sleep_duration_mapping.get(sleep_duration, 0)],  # Codifica aggiornata
        "Dietary Habits": [dietary_habits_mapping.get(dietary_habits, -1)],
        "Degree": [degree_mapping.get(degree, -1)],
        "Have you ever had suicidal thoughts ?": [suicidal_thoughts_mapping.get(suicidal_thoughts, -1)],
        "Work/Study Hours": [study_hours],
        "Financial Stress": [financial_stress],
        "Family History of Mental Illness": [family_history_mapping.get(family_history, -1)]
    }

    # Converte in DataFrame
    df = pd.DataFrame(processed_data)
    return df

def predict_depression_risk(model, data):
    """
    Utilizza il modello per calcolare la probabilità di rischio di depressione.
    :param model: Modello ML caricato.
    :param data: Dati preprocessati come DataFrame.
    :return: Percentuale di rischio.
    """
    probability = model.predict_proba(data)[0][1]  # Probabilità della classe "Depresso"
    return round(probability * 100, 2)  # Converte in percentuale e arrotonda

def calculate_risk(gender, age, academic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts, study_hours, financial_stress, family_history):
    """
    Calcola il rischio di depressione basandosi sui dati dell'utente.
    :return: Percentuale di rischio di depressione.
    """
    # Carica il modello
    model = load_model()
    
    # Preprocessa i dati
    data = preprocess_data(
        gender, age, academic_pressure, cgpa, study_satisfaction,
        sleep_duration, dietary_habits, degree, suicidal_thoughts,
        study_hours, financial_stress, family_history
    )
    
    # Calcola il rischio
    risk_probability = model.predict_proba(data)[0][1]  # Probabilità della classe "Depresso"
    risk_percentage = round(risk_probability * 100, 2)  # Converti in percentuale e arrotonda
    
    return risk_percentage

def avarage_risk_percentage(user_id):
    responses = get_responses(user_id)

    #for i in range(len(responses)):
        #avarage = [0] * len(responses)
        #values = responses[0][2:14] 
        #avarage[i] = calculate_risk(responses[i][values])
    values = []
    for response in responses:
        selected_values = [response[2], response[3], response[4], response[5], response[6], response[7], response[8],
                           response[9], response[10], response[11], response[12], response[13]]
                           
        value = calculate_risk(*selected_values)
        values.append(value)
    avarage_risk = sum(values) / len(values)
    return avarage_risk

