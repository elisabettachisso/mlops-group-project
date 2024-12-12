import streamlit as st
from database import get_responses
import pandas as pd 
import plotly.graph_objects as go
from ml_utils import calculate_risk
import plotly.express as px


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


def plot_sleep_duration(user_id):
    """
    Visualizza un grafico della durata del sonno (sleep_duration) per un utente specifico.

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

        # Prepara i dati per la durata del sonno
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

        # Creazione del grafico per "sleep_duration"
        fig_sleep = px.line(
            df,
            x='timestamp',
            y='sleep_duration_numeric',
            title="Andamento della Durata del Sonno",
            labels={'timestamp': "Time", 'sleep_duration_numeric': "Durata del Sonno (ore)"},
        )
        st.plotly_chart(fig_sleep)





def plots(user_id):
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
        df['academic_pressure'] = pd.to_numeric(df['academic_pressure'], errors='coerce')
        df['cgpa'] = pd.to_numeric(df['cgpa'], errors='coerce')
        df['study_satisfaction'] = pd.to_numeric(df['study_satisfaction'], errors='coerce')
        df['study_hours'] = pd.to_numeric(df['study_hours'], errors='coerce')
        df['financial_stress'] = pd.to_numeric(df['financial_stress'], errors='coerce')
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Rimuove valori non validi
        df = df.dropna(subset=['academic_pressure', 'cgpa', 'study_satisfaction', 'study_hours', 'financial_stress'])

        # Ordina per timestamp
        df = df.sort_values(by='timestamp')

        # Creazione del grafico per "academic_pressure"
        fig_academic = px.line(
            df,
            x='timestamp',
            y='academic_pressure',
            title="Andamento della Pressione Accademica",
            labels={'timestamp': "Time", 'academic_pressure': "Academic Pressure"}
        )
        st.plotly_chart(fig_academic)

        # Creazione del grafico per "cgpa"
        fig_cgpa = px.line(
            df,
            x='timestamp',
            y='cgpa',
            title="Andamento del CGPA",
            labels={'timestamp': "Time", 'cgpa': "CGPA"}
        )
        st.plotly_chart(fig_cgpa)

        fig_academic = px.line(
            df,
            x='timestamp',
            y='study_satisfaction',
            title="Soddisfazione studio",
            labels={'timestamp': "Time", 'study_satisfaction': "Soddisfazione studio"}
        )
        st.plotly_chart(fig_academic)


        fig_academic = px.line(
            df,
            x='timestamp',
            y='study_hours',
            title="Ore di studio",
            labels={'timestamp': "Time", 'study_hours': "Ore di studio"}
        )
        st.plotly_chart(fig_academic)

        fig_academic = px.line(
            df,
            x='timestamp',
            y='financial_stress',
            title="Finantial stress",
            labels={'timestamp': "Time", 'financial_stress': "Finantial stress"}
        )
        st.plotly_chart(fig_academic)

def plot_dietary_habits(user_id):
    """
    Visualizza un grafico a torta delle abitudini alimentari per un utente specifico.

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

        # Controlla se ci sono dati per "dietary_habits"
        if df['dietary_habits'].notna().sum() > 0:
            dietary_counts = df['dietary_habits'].value_counts()

            # Crea il grafico a torta
            fig = go.Figure(
                data=[go.Pie(
                    labels=dietary_counts.index,
                    values=dietary_counts.values,
                    hole=0.3  # Aggiungi il foro al centro per un grafico a ciambella
                )]
            )
            fig.update_layout(
                title_text="Distribuzione delle Abitudini Alimentari",
                annotations=[
                    dict(
                        text="Dietary Habits",
                        x=0.5,
                        y=0.5,
                        font_size=20,
                        showarrow=False
                    )
                ]
            )

            # Mostra il grafico con Streamlit
            st.plotly_chart(fig)
        else:
            st.write("⚠️ Nessun dato valido per Abitudini Alimentari.") 


def statistic_plots(user_id):
    plot_sleep_duration(user_id)
    plots(user_id)
    plot_dietary_habits(user_id)