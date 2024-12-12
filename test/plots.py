import streamlit as st
from database import get_responses
import pandas as pd 
import plotly.graph_objects as go
from ml_utils import calculate_risk

def plot_sleep_duration(user_id):
    # Recupera le risposte dell'utente
    responses = get_responses(user_id)
    
    if responses:
        # Converte le risposte in un DataFrame
        columns = [
            "id", "user_id", "gender", "age", "academic_pressure", "cgpa",
            "study_satisfaction", "sleep_duration", "dietary_habits", "degree",
            "suicidal_thoughts", "study_hours", "financial_stress",
            "family_history", "timestamp"
        ]
        df = pd.DataFrame(responses, columns=columns)

        # Prepara i dati per il grafico
        sleep_duration_mapping = {
            '5-6 hours': 5.5,
            'Less than 5 hours': 4.5,
            '7-8 hours': 7.5,
            'More than 8 hours': 8.5,
            'Others': None
        }
        df['sleep_duration_numeric'] = df['sleep_duration'].map(sleep_duration_mapping)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Rimuove valori non validi
        df = df.dropna(subset=['sleep_duration_numeric'])

        # Ordina per timestamp
        df = df.sort_values(by='timestamp')

        # Creazione del grafico area chart
        st.line_chart(data=df, x='timestamp', y='sleep_duration')

    else:
        st.write("Non ci sono risposte disponibili per questo utente.")




def plot_risk_indicator(risk_percentage):


    # Determina il colore della barra
    barra_colore = "green" if risk_percentage < 50 else "red"

    # Crea il grafico a gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percentage,
        title={'text': "Il tuo rischio stimato di depressione rispetto al tuo ultimo questionario compilato è:"},
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': barra_colore},
            'steps': [
                {'range': [0, 100], 'color': "lightgray"}
            ]
        }
    ))

    # Visualizza il grafico
    st.plotly_chart(fig)


def plot_academic_pressure(user_id):

    # Recupera le risposte dell'utente
    responses = get_responses(user_id)

    if responses:
        # Converte le risposte in un DataFrame
        columns = [
            "id", "user_id", "gender", "age", "academic_pressure", "cgpa",
            "study_satisfaction", "sleep_duration", "dietary_habits", "degree",
            "suicidal_thoughts", "study_hours", "financial_stress",
            "family_history", "timestamp"
        ]
        df = pd.DataFrame(responses, columns=columns)

        # Assicura che "academic_pressure" sia un intero e converte il timestamp
        df['academic_pressure'] = pd.to_numeric(df['academic_pressure'], errors='coerce')
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Rimuove valori non validi
        df = df.dropna(subset=['academic_pressure'])

        # Ordina per timestamp
        df = df.sort_values(by='timestamp')

        # Creazione del grafico line chart
        st.line_chart(data=df, x='timestamp', y='academic_pressure')

    else:
        st.write("Non ci sono risposte disponibili per questo utente.")

def plot_academic_pressure(user_id):
    """
    Visualizza un grafico delle pressioni accademiche (academic pressure) per un utente specifico.

    Parameters:
        user_id (int): ID dell'utente.

    Returns:
        None
    """
    # Recupera le risposte dell'utente
    responses = get_responses(user_id)

    if responses:
        # Converte le risposte in un DataFrame
        columns = [
            "id", "user_id", "gender", "age", "academic_pressure", "cgpa",
            "study_satisfaction", "sleep_duration", "dietary_habits", "degree",
            "suicidal_thoughts", "study_hours", "financial_stress",
            "family_history", "timestamp"
        ]
        df = pd.DataFrame(responses, columns=columns)

        # Assicura che "academic_pressure" sia un intero, "cgpa" sia un float e converte il timestamp
        df['cgpa'] = pd.to_numeric(df['cgpa'], errors='coerce')
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Rimuove valori non validi
        df = df.dropna(subset=['academic_pressure', 'cgpa'])

        # Ordina per timestamp
        df = df.sort_values(by='timestamp')
        st.write("### Andamento della pressione accademica")
        # Creazione dei grafici line chart
        st.line_chart(data=df, x='timestamp', y='cgpa')

    else:
        st.write("Non ci sono risposte disponibili per questo utente.")
