import streamlit as st
from database import get_responses, get_all_responses
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px


def plot_risk_indicator(risk_percentage):


    # Determina il colore della barra
    barra_colore = "green" if risk_percentage < 50 else "red"

    # Crea il grafico a gauge
    fig_risk = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percentage,
        title={'text': "Your estimated risk of depression based on your last completed questionnaire is:"},
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
    return fig_risk

def plot_avarage_indicator(risk_percentage):


    # Determina il colore della barra
    barra_colore = "green" if risk_percentage < 50 else "red"

    # Crea il grafico a gauge
    fig_risk_avarage = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percentage,
        title={'text': "On average, based on all the questionnaires you have completed, your risk of depression is:"},
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': barra_colore},
            'steps': [
                {'range': [0, 100], 'color': "lightgray"}
            ]
        }
    ))
    return fig_risk_avarage


def plots(user_id, risk_percentage):

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
            title="Academic Pressure",
            labels={'timestamp': "Time", 'academic_pressure': "Academic Pressure"}
        )

        # Creazione del grafico per "cgpa"
        fig_cgpa = px.line(
            df,
            x='timestamp',
            y='cgpa',
            title="CGPA",
            labels={'timestamp': "Time", 'cgpa': "CGPA"}
        )

        fig_study_satisfaction = px.line(
            df,
            x='timestamp',
            y='study_satisfaction',
            title="Study satisfaction",
            labels={'timestamp': "Time", 'study_satisfaction': "Study satisfaction"}
        )


        fig_study_hours = px.line(
            df,
            x='timestamp',
            y='study_hours',
            title="Study hours",
            labels={'timestamp': "Time", 'study_hours': "Study hours"}
        )


        fig_finantial_stress = px.line(
            df,
            x='timestamp',
            y='financial_stress',
            title="Finantial stress",
            labels={'timestamp': "Time", 'financial_stress': "Finantial stress"}
        )

        if df['dietary_habits'].notna().sum() > 0:
            dietary_counts = df['dietary_habits'].value_counts()

            # Crea il grafico a torta
            fig_dietary_habits = go.Figure(
                data=[go.Pie(
                    labels=dietary_counts.index,
                    values=dietary_counts.values,
                    hole=0.3  # Aggiungi il foro al centro per un grafico a ciambella
                )]
            )
            fig_dietary_habits.update_layout(
                title_text="Dietary habits",
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
            title="Sleep Duration (h)",
            labels={'timestamp': "Time", 'sleep_duration_numeric': "Durata del Sonno (ore)"},
        )

        st.plotly_chart(plot_avarage_indicator(risk_percentage))  
            
        col2, col3, col4 = st.columns(3)

        with col2:
            st.plotly_chart(fig_academic)

        with col3:
            st.plotly_chart(fig_study_satisfaction)

        with col4:
            st.plotly_chart(fig_cgpa, use_container_width=True)
        
        col5, col6, col7 = st.columns(3)

        with col5:
            st.plotly_chart(fig_study_hours, use_container_width=True)

        with col6:
            st.plotly_chart(fig_finantial_stress, use_container_width=True)

        with col7:
            st.plotly_chart(fig_sleep, use_container_width=True)
        

def plots_analyst(risk_percentage):

    # Recupera le risposte dell'utente
    responses = get_all_responses()
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
            title="Academic Pressure",
            labels={'timestamp': "Time", 'academic_pressure': "Academic Pressure"}
        )

        # Creazione del grafico per "cgpa"
        fig_cgpa = px.line(
            df,
            x='timestamp',
            y='cgpa',
            title="CGPA",
            labels={'timestamp': "Time", 'cgpa': "CGPA"}
        )

        fig_study_satisfaction = px.line(
            df,
            x='timestamp',
            y='study_satisfaction',
            title="Study satisfaction",
            labels={'timestamp': "Time", 'study_satisfaction': "Study satisfaction"}
        )


        fig_study_hours = px.line(
            df,
            x='timestamp',
            y='study_hours',
            title="Study hours",
            labels={'timestamp': "Time", 'study_hours': "Study hours"}
        )


        fig_finantial_stress = px.line(
            df,
            x='timestamp',
            y='financial_stress',
            title="Finantial stress",
            labels={'timestamp': "Time", 'financial_stress': "Finantial stress"}
        )

        if df['dietary_habits'].notna().sum() > 0:
            dietary_counts = df['dietary_habits'].value_counts()

            # Crea il grafico a torta
            fig_dietary_habits = go.Figure(
                data=[go.Pie(
                    labels=dietary_counts.index,
                    values=dietary_counts.values,
                    hole=0.3  # Aggiungi il foro al centro per un grafico a ciambella
                )]
            )
            fig_dietary_habits.update_layout(
                title_text="Dietary habits",
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
            title="Sleep Duration (h)",
            labels={'timestamp': "Time", 'sleep_duration_numeric': "Durata del Sonno (ore)"},
        )

        st.plotly_chart(plot_avarage_indicator(risk_percentage))  
            
        col2, col3, col4 = st.columns(3)

        with col2:
            st.plotly_chart(fig_academic)

        with col3:
            st.plotly_chart(fig_study_satisfaction)

        with col4:
            st.plotly_chart(fig_cgpa, use_container_width=True)
        
        col5, col6, col7 = st.columns(3)

        with col5:
            st.plotly_chart(fig_study_hours, use_container_width=True)

        with col6:
            st.plotly_chart(fig_finantial_stress, use_container_width=True)

        with col7:
            st.plotly_chart(fig_sleep, use_container_width=True)
        



def plot_dietary_habits(user_id):

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
            fig_dietary_habits = go.Figure(
                data=[go.Pie(
                    labels=dietary_counts.index,
                    values=dietary_counts.values,
                    hole=0.3  # Aggiungi il foro al centro per un grafico a ciambella
                )]
            )
            fig_dietary_habits.update_layout(
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
        else:
            st.write("⚠️ Nessun dato valido per Abitudini Alimentari.") 



def statistic_plots(user_id, risk_percentage):
    plots(user_id, risk_percentage)
    
def statistic_plots_analyst(risk_percentage):
    plots(risk_percentage)

