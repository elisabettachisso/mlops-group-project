import streamlit as st
from database import initialize_database, add_response, get_responses, get_all_responses, get_last_response, add_suggestions, add_categories, add_user, get_suggestions
from route import go_to_login, go_to_register
from ml_utils import calculate_risk, avarage_risk_percentage, avarage_risk_percentage_allusers
from plots import plot_risk_indicator, statistic_plots, plots_analyst
from auth import logout
from streamlit_option_menu import option_menu
from PIL import Image
from suggestions import select_random_suggestions
import pandas as pd
import io
import time
initialize_database()

logo_path = "images/logomindhug.png"

def home_page():

    # Carica un'immagine o logo
    logo = Image.open(logo_path)  # Cambia il percorso se necessario

    # Centra il contenuto sulla pagina
    st.markdown(
        """
        <style>
        .centered-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 2rem;
        }
        .button-container {
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 2rem;
            margin-top: 2rem;
        }
        .custom-button {
            padding: 0.75rem 2rem;
            font-size: 1.25rem;
            font-weight: bold;
            color: white;
            background-color: #4CAF50;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .custom-button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Contenitore principale
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)

    # Logo e titolo
    st.image(logo, width=200)
    st.markdown("<h1>Welcome to <span style='color:#0d6efd';'>MindHug</span></h1>", unsafe_allow_html=True)
    st.markdown(
        "<p>Your personalized companion for mental well-being. Navigate through our tools to enhance your wellness and track your progress.</p>",
        unsafe_allow_html=True,
    )

    # Contenitore per i pulsanti
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Go to Login"):
            go_to_login()

    with col2:
        if st.button("Go to Registration"):
            go_to_register()

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p>© 2024 MindHug. All rights reserved.</p>", unsafe_allow_html=True)


def main_page():

    st.write(f"Ciao, {st.session_state.username} 🙂")

    def navigation_bar():
        selected = option_menu(
            menu_title=None,  # Non mostrare un titolo (barra orizzontale)
            options=["Home", "Fill Questionnaire", "Tips", "Statistics"],  # Opzioni di navigazione
            icons=["house", "file-text", "lightbulb", "bar-chart",],  # Icone da FontAwesome
            menu_icon="cast",  # Icona del menu (non visibile in modalità orizzontale)
            default_index=0,  # Indice dell'opzione selezionata di default
            orientation="horizontal",  # Modalità orizzontale
            styles={
                "container": {"padding": "0!important"},
                "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "lightblue"},
                "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
            },
        )
        return selected

    # Mostra la barra di navigazione
    selection = navigation_bar()


    if selection == "Home":
        title = "MindHug"  

        col1, col2 = st.columns([1, 5])  # Colonna per il logo e colonna per il titolo

        with col1:
            st.image(logo_path, width=200)  # Imposta la larghezza del logo

        with col2:
            st.markdown(f"<h1>Welcome to <span style='color:#0d6efd' ;'>{title}</span></h1>", unsafe_allow_html=True)
        
        st.subheader("Your support for mental well-being")

        # Introduction text
        st.write("""
        This app is designed to help you take control of your physical and mental health by providing insights and personalized advice based on your lifestyle. With our simple yet powerful features, you can track your well-being and make informed decisions to live a healthier, happier life.
        """)

        # Key Features Section
        st.subheader("Key Features:")

        # Feature 1: Self-assessment Questionnaire
        st.write("""
        1. **Self-assessment Questionnaire:**  
        Start by completing a quick questionnaire that evaluates your current physical and mental well-being. The questions are tailored to give you a comprehensive view of your lifestyle.
        """)

        # Feature 2: Personalized Recommendations
        st.write("""
        2. **Personalized Recommendations:**  
        Based on your responses, the app offers personalized tips and advice to help you improve your overall well-being. Whether it’s adjusting daily habits or finding new ways to cope with stress, you'll receive valuable insights to guide you along the way.
        """)

        # Feature 3: Visualize Your Progress
        st.write("""
        3. **Visualize Your Progress:**  
        With beautifully designed charts and graphs, you can track your progress over time. The app stores your historical data, allowing you to see how your well-being evolves and identify trends that may need attention.
        """)

        # Goal Section
        st.subheader("The Goal:")

        st.write("""
        The aim of this app is to raise awareness about how your lifestyle choices impact your mental health, particularly the risk of depression. With real-time updates on percentages and actionable areas for improvement, you’ll always know where you stand and how to take proactive steps toward a better life.
        """)

        # How to Use Section
        st.subheader("How to Use It:")

        st.write("""
        The app is designed to be used periodically. By completing a new questionnaire each time, you can monitor your progress, see improvements, and make adjustments to continue enhancing your well-being. It’s a powerful tool for building a healthier, more balanced life one step at a time.
        """)

        last_response = get_last_response(st.session_state.user_id)
        if last_response:
            values = last_response[0][2:14]  # Crea una lista con i valori da last_response
            risk_percentage = calculate_risk(*values)  # Usa l'unpacking per passare i valori come argomenti separati
            st.plotly_chart(plot_risk_indicator(risk_percentage))
        else: 
            st.error("No questionnaire has been filled out yet!")
        
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

def main_page_analyst():

    st.write(f"Ciao, {st.session_state.username} 🙂")

    def navigation_bar_analyst():
        selected = option_menu(
            menu_title=None,  # Non mostrare un titolo (barra orizzontale)
            options=["General Statistics", "CSV downloads"],  # Opzioni di navigazione
            icons=["bar-chart","cloud-download" ],  # Icone da FontAwesome
            menu_icon="cast",  # Icona del menu (non visibile in modalità orizzontale)
            default_index=0,  # Indice dell'opzione selezionata di default
            orientation="horizontal",  # Modalità orizzontale
            styles={
                "container": {"padding": "0!important"},
                "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "lightblue"},
                "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
            },
        )
        return selected

    # Mostra la barra di navigazione
    selection = navigation_bar_analyst()
        
    if selection == "General Statistics": 
        display_statistics_analyst()
    if selection == "CSV downloads":

        column_names =["id", "user_id", "gender", "age", "accademic_pressure", "cgpa", "study_satisfaction", "sleep_duration", "dietary_habits", "degree", "suicidal_thoughts", "study_hours", "financial_stress",
                       "family_history", "timestamp"]
        data = get_all_responses()
        df = pd.DataFrame(data, columns=column_names)
        def convert_df_to_csv(df):
        # Usa io.StringIO per creare un buffer in memoria
            csv = df.to_csv(index=False)
            return csv
        csv_data = convert_df_to_csv(df)
        def display_table(df):
            st.subheader("Dati:")
            st.dataframe(df)
        display_table(df)
        st.download_button(
            label="Scarica il file CSV",
            data=csv_data,
            file_name="dati.csv",
            mime="text/csv"
        )

        

    if st.button("Logout"):
         logout()
         st.rerun()

    
    # Footer
    st.markdown("---")
    st.write("© 2024 MindHug. All rights reserved.")

def display_statistics_analyst(): 
        st.header("All users statistics") 
        #responses = get_all_responses()
        # risk_values = []
        # for response in responses:
        #     risk_percentage = calculate_risk(response[2], response[3], response[4], response[5], response[6], response[7], response[8],
        #                    response[9], response[10], response[11], response[12], response[13])
        #     risk_values.append(risk_percentage)
        avarage_risk = avarage_risk_percentage_allusers()
        plots_analyst(avarage_risk)


def display_statistics(): 
        st.header("Your personal statistics, based on the questionnaires you have completed:") 
        responses = get_responses(st.session_state.user_id)
        last_response = get_last_response(st.session_state.user_id)
        if last_response:
            values = last_response[0][2:14]  # Crea una lista con i valori da last_response
            risk_percentage = calculate_risk(*values)  # Usa l'unpacking per passare i valori come argomenti separati

            avarage_risk= avarage_risk_percentage(st.session_state.user_id)
            statistic_plots(st.session_state.user_id, avarage_risk)
        else:
            st.error("No questionnaire has been filled out yet!")

def display_suggestions(): 
        st.header("Tips") 
        last_response = get_last_response(st.session_state.user_id)
        if last_response:
            st.write("Here are some helpful tips based on the results of your last questionnaire:") 
            responses = select_random_suggestions(last_response)
            for response in responses:
                st.markdown(f"**{response[1]}**" + "\n  - " + response[2])
        else:
            st.error("No questionnaire has been filled out yet!")
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
    suicidal_thoughts = st.radio("Have you ever had suicidal thoughts?", ("No", "Yes"))
    study_hours = st.slider("How many hours do you study per day?", min_value=0, max_value=10, step=1)
    financial_stress = st.slider("How stressed are you financially?", min_value=0, max_value=5, step=1)
    family_history = st.radio("Do you have any cases of mental illness in your family?", ("No", "Yes"))

    if st.button("Submit answer"):
        if add_response(st.session_state.user_id, gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts,
                        study_hours, financial_stress, family_history):  
            st.success("Answer submitted successfully!") 
        else: 
            st.error("An error occurred while submitting the answer.")

    risk_percentage = calculate_risk(gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, dietary_habits, degree, suicidal_thoughts, study_hours, financial_stress, family_history)

    st.plotly_chart(plot_risk_indicator(risk_percentage))


def main_page_admin():
        def navigation_bar_admin():
            selected = option_menu(
                menu_title=None,  # Non mostrare un titolo (barra orizzontale)
                options=["Add users", "Add suggestions"],  # Opzioni di navigazione
                icons=["bar-chart","cloud-download" ],  # Icone da FontAwesome
                menu_icon="cast",  # Icona del menu (non visibile in modalità orizzontale)
                default_index=0,  # Indice dell'opzione selezionata di default
                orientation="horizontal",  # Modalità orizzontale
                styles={
                    "container": {"padding": "0!important"},
                    "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "lightblue"},
                    "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
                },
            )
            return selected
        
        selection = navigation_bar_admin()
        if selection == "Add users":
            with st.form("registration_form"):
                username = st.text_input("Username")
                name = st.text_input("Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                password_confirm = st.text_input("Confirm Password", type="password")
                register_button = st.form_submit_button("Register")

            if register_button:
                if password != password_confirm:
                    st.error("Passwords do not match")
                elif add_user(username, name, email, password):
                    st.success("Registration successful! Please login.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Username already exists. Please try another one.")
                    time.sleep(0.5)


        if selection == "Add suggestions":
            st.title("Carica un file CSV")
            uploaded_file = st.file_uploader("Scegli un file CSV", type=["csv"])
            if uploaded_file is not None:
                # Leggi il file CSV in un DataFrame
                df = pd.read_csv(uploaded_file)

                # Mostra i dati del CSV in Streamlit
                st.write("Dati caricati:")
                st.dataframe(df)  # Visualizza il DataFrame in una tabella interattiva

                data_list = df.values.tolist()

                if st.button("Add suggestions"):
                    if add_suggestions(data_list):
                        st.success("Suggestions added correctly!")
                    else: 
                        st.error("There is a problem with the upload")
            
            else:
                st.write("Carica un file CSV per visualizzarne i dati.")



        

        

    





