import streamlit as st
import os
from database import initialize_database, add_response, get_responses, get_last_response
from route import go_to_login, go_to_register, logout
from ml_utils import calculate_risk
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from plots import plot_risk_indicator, statistic_plots
initialize_database()

def home_page():
    st.title("Benvenuti nella Web App")
    st.write("Seleziona un'opzione:")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Vai al Login", on_click=go_to_login)
    with col2:
        st.button("Vai alla Registrazione", on_click=go_to_register)

def main_page():
    # Configurazione della pagina
    st.set_page_config(
        page_title="MindHug",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    title = "MindHug"
    logo_path = os.path.join(os.getcwd(), "images", "logomindhug.png")

    col1, col2 = st.columns([1, 5])  

    with col1:
        st.image(logo_path, width=200) 

    with col2:
        st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)

    #st.title("🧠 MindHug")
    st.subheader("Il tuo supporto per il benessere mentale")
    st.write(
        "Benvenuto in **MindHug**, un'app progettata per aiutarti a monitorare il tuo benessere mentale "
        "e fornire suggerimenti personalizzati per prenderti cura di te stesso."
    )
    #st.image("images/logomindhug.png", width=200)  

    # Barra laterale per navigare 
    with st.sidebar: 
        selection = st.radio("Navigazione", ["Home", "Suggerimenti", "Compila Questionario"])

    if selection == "Home": 
        display_statistics()
    elif selection == "Suggerimenti": 
        display_suggestions() 
    elif selection == "Compila Questionario": 
        fill_questionnaire()
    
    st.markdown("### Risorse Utili")
    st.write(
        "- [Esercizi di mindfulness](https://www.headspace.com)\n"
        "- [Tecniche di gestione dello stress](https://www.helpguide.org/articles/stress/stress-management.htm)"
    )
    
    # Footer
    st.markdown("---")
    st.write("© 2024 MindHug. Tutti i diritti riservati.")

    if st.button("Logout"):
        logout()
        st.rerun()

def display_statistics(): 
        st.header("Statistiche") 
        responses = get_responses(st.session_state.user_id)
        last_response = get_last_response(st.session_state.user_id)
        if last_response:
            risk_percentage = calculate_risk(
                last_response[0][2], last_response[0][3], last_response[0][4],
                last_response[0][5], last_response[0][6], last_response[0][7],
                last_response[0][8], last_response[0][9], last_response[0][10],
                last_response[0][11], last_response[0][12], last_response[0][13]
            )
            plot_risk_indicator(risk_percentage)
        else:
            st.write("Non è ancora stato compilato alcun questionario")
        statistic_plots(st.session_state.user_id)

def display_suggestions(): 
        st.header("Suggerimenti") 
        st.write("Ecco alcuni suggerimenti utili:") 
        last_response = get_last_response(st.session_state.user_id)


def fill_questionnaire(): 
    st.markdown("### Compila il questionario")
    gender = st.radio("Gender", ("Male", "Female"))
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    accademic_pressure = st.slider("Accademic Pressure", min_value=1, max_value=5, step=1)
    cgpa = st.number_input("CGPA", min_value=1.00, max_value=10.00, step=0.01)
    study_satisfaction = st.slider("Study satisfaction", min_value=1, max_value=5, step=1)
    sleep_duration = st.selectbox(
        "How much do you sleep?",
        ["5-6 hours", "Less than 5 hours", "7-8 hours", "More than 8 hours", "Others"]
    )
    dietary_habits = st.selectbox(
        "dietary habits",
        ["Healty", "Moderate", "Unhealty"]
    )
    degree = st.selectbox(
        "degree",
        ["Diploma", "Bachelor", "Master", "PhD"]
    )
    suicidal_thoughts = st.radio("Suicidal", ("Yes", "No"))
    study_hours = st.slider("Quante ore studi al giorno?", min_value=0, max_value=10, step=1)
    financial_stress = st.slider("Financial stress", min_value=0, max_value=5, step=1)
    family_history = st.radio("Fam History", ("Yes", "No"))

    if st.button("Invia risposta"):
        if add_response(st.session_state.user_id, gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts,
                        study_hours, financial_stress, family_history):  
            st.success("Risposta inviata con successo!") 
        else: 
            st.error("Si è verificato un errore durante l'invio della risposta.")
    # Calcolo del rischio
    risk_percentage = calculate_risk(gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts, study_hours, financial_stress, family_history)

    plot_risk_indicator(risk_percentage)
    
    #responses = get_responses(st.session_state.user_id) 
    
    #for res in responses: 
      #  st.write(res)





