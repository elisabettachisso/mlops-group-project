import streamlit as st
from database import initialize_database, add_categories, add_response, get_responses, get_last_response, add_suggestions
from route import go_to_login, go_to_register
from ml_utils import calculate_risk
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from plots import plot_risk_indicator, statistic_plots
from auth import logout
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
initialize_database()

def home_page():
    st.set_page_config(
        page_title="Welcome to Mindhug",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    st.title("Welcome to Mindhug")
    st.write("Select an option:")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Go to Login", on_click=go_to_login)
    with col2:
        st.button("Go to Registration", on_click=go_to_register)

def main_page():
  
    st.set_page_config(
        page_title="Mindhug",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    #st.image("images/logomindhug.png", width=200)  

    # Barra laterale per navigare 
    #with st.sidebar: 
     #   selection = st.radio("Navigazione", ["Home", "Suggerimenti", "Compila Questionario"])

# Sidebar con menu
    with st.sidebar:
        selection = option_menu(
            menu_title="Navigation",  # Titolo del menu
            options=["Home", "Statistics", "Tips", "Fill Questionnaire"],  # Opzioni
            icons=["house", "bar-chart","lightbulb", "file-text"],  # Icone da FontAwesome
            menu_icon="compass",  # Icona del menu
            default_index=0,  # Prima opzione selezionata
        )

    if selection == "Home":
            # Definisci il titolo e il logo
        title = "MindHug"
        logo_path = "app/images/logomindhug.png"  # Sostituisci con il percorso del tuo logo

    # Usa st.columns per posizionare il logo e il titolo accanto
        col1, col2 = st.columns([1, 5])  # Colonna per il logo e colonna per il titolo

        with col1:
            # Mostra il logo nella prima colonna
            st.image(logo_path, width=200)  # Imposta la larghezza del logo

        with col2:
            # Mostra il titolo nella seconda colonna
            st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)

        #st.title("🧠 MindHug")
        st.subheader("Your support for mental well-being")
        st.write(
            "Welcome to **MindHug**, an app designed to help you track your mental well-being" 
            "and provide personalized suggestions to take care of yourself."
        )
    if selection == "Statistics": 
        display_statistics()
    elif selection == "Tips": 
        display_suggestions() 
    elif selection == "Fill Questionnaire": 
        fill_questionnaire()
    
    if st.button("Logout"):
        logout()
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.write("© 2024 MindHug. All rights reserved.")



def display_statistics(): 
        st.header("Your personal statistics, based on the questionnaires you have completed:") 
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
            statistic_plots(st.session_state.user_id, risk_percentage)
        else:
            st.write("No questionnaire has been completed yet!")

def display_suggestions(): 
        st.header("Tips") 
        st.write("Here are some helpful tips:") 
        last_response = get_last_response(st.session_state.user_id)
        if st.button("Aggiungi Suggestions"):
            try:
                add_suggestions()
                st.success("Suggestions added successfully!")
            except Exception as e:
                st.error(f"An error occurred while adding suggestions: {e}")
        if st.button("Aggiungi Categorie"):
            try:
                add_categories()
                st.success("categories added successfully!")
            except Exception as e:
                st.error(f"An error occurred while adding suggestions: {e}")
        st.markdown("### Useful Resources")
        st.write(
        "- [Mindfulness Exercises](https://www.headspace.com)\n"
        "- [Stress Management Techniques](https://www.helpguide.org/articles/stress/stress-management.htm)")


def fill_questionnaire(): 
    st.markdown("### Fill out the questionnaire")
    gender = st.radio("Gender:", ("Male", "Female"))
    age = st.number_input("Age:", min_value=1, max_value=100, step=1)
    accademic_pressure = st.slider("How much academic pressure do you feel on a scale of 1 to 5?", min_value=1, max_value=5, step=1)
    cgpa = st.number_input("What is your CGPA (Cumulative Grade Point Average, the average of all the earned grades)?", min_value=1.00, max_value=10.00, step=0.01)
    study_satisfaction = st.slider("How satisfied are you with your academic results?", min_value=1, max_value=5, step=1)
    sleep_duration = st.selectbox(
        "How much do you sleep?",
        ["5-6 hours", "Less than 5 hours", "7-8 hours", "More than 8 hours", "Others"]
    )
    dietary_habits = st.selectbox(
        "What are your dietary habits like?",
        ["Healty", "Moderate", "Unhealty"]
    )
    degree = st.selectbox(
        "What is your level of study?",
        ["Diploma", "Bachelor", "Master", "PhD"]
    )
    suicidal_thoughts = st.radio("Have you ever had suicidal thoughts?", ("Yes", "No"))
    study_hours = st.slider("How many hours do you study per day?", min_value=0, max_value=10, step=1)
    financial_stress = st.slider("How stressed are you financially?", min_value=0, max_value=5, step=1)
    family_history = st.radio("Do you have any cases of mental illness in your family?", ("Yes", "No"))

    if st.button("Submit answer"):
        if add_response(st.session_state.user_id, gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts,
                        study_hours, financial_stress, family_history):  
            st.success("Answer submitted successfully!") 
        else: 
            st.error("An error occurred while submitting the answer.")
    # Calcolo del rischio
    risk_percentage = calculate_risk(gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts, study_hours, financial_stress, family_history)

    st.plotly_chart(plot_risk_indicator(risk_percentage))
    
    #responses = get_responses(st.session_state.user_id) 
    
    #for res in responses: 
      #  st.write(res)

def centered_container(content):
    st.markdown(
        """
        <style>
        .centered-container {
            max-width: 600px;
            margin: auto;
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)





