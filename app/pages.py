import streamlit as st
from database import initialize_database, add_response, get_all_responses, get_last_response, add_suggestions, add_user, get_users_logs
from ml_utils import calculate_risk, avarage_risk_percentage, avarage_risk_percentage_allusers
from plots import plot_stimated_depression_indicator, statistic_plots
from ml_utils import preprocess_responses_user, preprocess_all_responses
from auth import logout
from utils import convert_df_to_csv, display_table
from streamlit_option_menu import option_menu
from PIL import Image
from suggestions import select_random_suggestions
import pandas as pd
import time

initialize_database()

logo_path = "app/images/logomindhug.png"

def home_page():

    # upload the logo.
    logo = Image.open(logo_path)

    # set the page style
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
    # main container
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    # logo and title
    st.image(logo, width=200)
    st.markdown("<h1>Welcome to <span style='color:#0d6efd';'>MindHug</span></h1>", unsafe_allow_html=True)
    st.markdown(
        "<p>Your personalized companion for mental well-being. Navigate through our tools to enhance your wellness and track your progress.</p>",
        unsafe_allow_html=True,
    )
    # container for bottons
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Go to Login"):
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("Go to Registration"):
            st.session_state.page = "register"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p>© 2024 MindHug. All rights reserved.</p>", unsafe_allow_html=True)

def main_page_admin():

    st.write(f"Ciao, {st.session_state.username} 🙂")

    selection = navigation_bar_admin()
    if selection == "Home": 
        display_home_users()
    if selection == "Fill Questionnaire":
        fill_questionnaire_user()
    if selection == "Tips":
        display_suggestions_user()
    if selection == "Personal Statistics":
        display_statistics_user()
    if selection == "General Statistics": 
        display_general_statistics()
    if selection == "CSV downloads":
        display_csv_download()
    if selection == "Users":
        display_users_logs()
        st.subheader("Add New User")
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
                st.success("Registration successful!")
                time.sleep(0.5) 
                st.rerun()
            else:
                st.error("Username already exists. Please try another one.")
    if selection == "Add suggestions":
        display_add_suggestions()

    if st.button("Logout"):
         logout()
         st.rerun()

    # Footer
    st.markdown("---")
    st.write("© 2024 MindHug. All rights reserved.")
    
def main_page_analyst():

    st.write(f"Ciao, {st.session_state.username} 🙂")
    selection = navigation_bar_analyst()
        
    if selection == "General Statistics": 
        display_general_statistics()
    if selection == "CSV downloads":
        display_csv_download()
    
    if st.button("Logout"):
        logout()        
        st.rerun()

    # Footer
    st.markdown("---")
    st.write("© 2024 MindHug. All rights reserved.")

def main_page_users():
    st.write(f"Ciao, {st.session_state.username} 🙂")
    selection = navigation_bar_users()
        
    if selection == "Home": 
        display_home_users()
    if selection == "Fill Questionnaire":
        fill_questionnaire_user()
    if selection == "Tips":
        display_suggestions_user()
    if selection == "Statistics":
        display_statistics_user()
    
    if st.button("Logout"):
         logout()
         st.rerun()

    # Footer
    st.markdown("---")
    st.write("© 2024 MindHug. All rights reserved.")

def display_general_statistics(): 
    st.header("All users statistics") 
    avarage_risk = avarage_risk_percentage_allusers()
    if avarage_risk:
        df = preprocess_all_responses()
        statistic_plots(df, avarage_risk)

def display_statistics_user(): 
    st.header("Your personal statistics, based on the questionnaires you have completed:") 
    avarage_risk= avarage_risk_percentage(st.session_state.user_id)

    if avarage_risk:
        df = preprocess_responses_user(st.session_state.user_id)
        statistic_plots(df, avarage_risk)

def display_suggestions_user(): 
    st.header("Tips") 
    last_response = get_last_response(st.session_state.user_id)
    if last_response:
        st.write("Here are some helpful tips based on the results of your last questionnaire:") 
        responses = select_random_suggestions(last_response)
        for response in responses:
            st.markdown(f"**{response[1]}**" + "\n  - " + response[2])
    else:
        st.error("No questionnaire has been filled out yet!")
    st.markdown("### Useful Resources")
    st.write(
         "- [Mindfulness Exercises](https://www.headspace.com)\n"
         "- [Stress Management Techniques](https://www.helpguide.org/articles/stress/stress-management.htm)")
        
def fill_questionnaire_user(): 

    st.markdown("### Fill out the questionnaire")
    gender = st.radio("Gender:", ("Male", "Female"))
    age = st.number_input("Age:", min_value=1, max_value=100, step=1)
    accademic_pressure = st.slider("How much academic pressure do you feel on a scale of 1 to 5?", 
                                   min_value=1, max_value=5, step=1)
    cgpa = st.number_input("What is your CGPA (Cumulative Grade Point Average, the average of all the earned grades)?", 
                           min_value=1.00, max_value=10.00, step=0.01)
    study_satisfaction = st.slider("How satisfied are you with your academic results?", 
                                   min_value=1, max_value=5, step=1)
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
        if add_response(st.session_state.user_id, gender, age, accademic_pressure, cgpa, study_satisfaction, 
                        sleep_duration, dietary_habits, degree, suicidal_thoughts,
                        study_hours, financial_stress, family_history):  
            st.success("Answer submitted successfully!") 
        else: 
            st.error("An error occurred while submitting the answer.")

    risk_percentage = calculate_risk(gender, age, accademic_pressure, cgpa, study_satisfaction, sleep_duration, 
                                     dietary_habits, degree, suicidal_thoughts, study_hours, financial_stress, family_history)

    st.plotly_chart(plot_stimated_depression_indicator(risk_percentage))

def navigation_bar_users():
    selected = option_menu(
        menu_title=None,  # Non mostrare un titolo (barra orizzontale)
        options=["Home", "Fill Questionnaire", "Tips", "Statistics"],  # Opzioni di navigazione
        icons=["house", "file-text", "lightbulb", "bar-chart"],  # Icone da FontAwesome
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

def navigation_bar_admin():
    selected = option_menu(
        menu_title=None,  
        options=["Home", "Fill Questionnaire", "Tips", "Personal Statistics",
                  "General Statistics", "CSV downloads", "Users", "Add suggestions"],  
        icons=["house", "file-text", "lightbulb", "bar-chart", "bar-chart","cloud-download", "person-plus","lightbulb"],  
        menu_icon="cast",  
        default_index=0, 
        orientation="horizontal",  
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "lightblue"},
            "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
        },
    )
    return selected

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

def display_home_users():
    title = "MindHug"  

    col1, col2 = st.columns([1, 5])  

    with col1:
        st.image(logo_path, width=200)  
    with col2:
        st.markdown(f"<h1>Welcome to <span style='color:#0d6efd' ;'>{title}</span></h1>", unsafe_allow_html=True)
        
    st.subheader("Your support for mental well-being")

    # Introduction text
    st.write("""
        This app is designed to help you take control of your physical and mental health by providing insights and personalized advice based on your lifestyle.
        With our simple yet powerful features, you can track your well-being and make informed decisions to live a healthier, happier life.
        """)

    # Key Features Section
    st.subheader("Key Features:")

    # Feature 1: Self-assessment Questionnaire
    st.write("""
        1. **Self-assessment Questionnaire:**  
        Start by completing a quick questionnaire that evaluates your current physical and mental well-being. 
        The questions are tailored to give you a comprehensive view of your lifestyle.
        """)

        # Feature 2: Personalized Recommendations
    st.write("""
        2. **Personalized Recommendations:**  
        Based on your responses, the app offers personalized tips and advice to help you improve your overall well-being. 
        Whether it’s adjusting daily habits or finding new ways to cope with stress, you'll receive valuable insights to guide you along the way.
        """)

        # Feature 3: Visualize Your Progress
    st.write("""
        3. **Visualize Your Progress:**  
        With beautifully designed charts and graphs, you can track your progress over time. 
        The app stores your historical data, allowing you to see how your well-being evolves and identify trends that may need attention.
        """)

        # Goal Section
    st.subheader("The Goal:")

    st.write("""
        The aim of this app is to raise awareness about how your lifestyle choices impact your mental health, particularly the risk of depression. 
        With real-time updates on percentages and actionable areas for improvement, you’ll always know where you stand and how to take proactive steps toward a better life.
        """)

        # How to Use Section
    st.subheader("How to Use It:")

    st.write("""
        The app is designed to be used periodically. By completing a new questionnaire each time, you can monitor your progress, see improvements, 
        and make adjustments to continue enhancing your well-being. It’s a powerful tool for building a healthier, more balanced life one step at a time.
        """)

    last_response = get_last_response(st.session_state.user_id)
    if last_response:
        values = last_response[0][2:14]  
        risk_percentage = calculate_risk(*values)  
        st.plotly_chart(plot_stimated_depression_indicator(risk_percentage))
    else: 
        st.error("No questionnaire has been filled out yet!")
        
def display_add_suggestions():
    st.title("Carica un file CSV")
    uploaded_file = st.file_uploader("Scegli un file CSV", type=["csv"])
    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.write("Dati caricati:")
        st.dataframe(df)  

        data_list = df.values.tolist()

        if st.button("Add suggestions"):
            if add_suggestions(data_list):
                st.success("Suggestions added correctly!")
            else: 
                st.error("There is a problem with the upload. Check the file format, the columns must be 4: title, description, category_id, and level.")
        else:
            st.write("Carica un file CSV per visualizzarne i dati.")

def display_csv_download():
    column_names =["id", "user_id", "gender", "age", "accademic_pressure", "cgpa", "study_satisfaction", "sleep_duration", "dietary_habits", "degree", "suicidal_thoughts", "study_hours", "financial_stress",
                   "family_history", "timestamp"]
    data = get_all_responses()
    df = pd.DataFrame(data, columns=column_names)
    csv_data = convert_df_to_csv(df)
    display_table(df)
    st.download_button(
        label="Download CSV file",
        data=csv_data,
        file_name="data.csv",
        mime="text/csv"
    )

def display_users_logs():
    column_names =["id", "user_id", "username", "name", "timestamp"]
    data = get_users_logs()
    df = pd.DataFrame(data, columns=column_names)
    csv_data = convert_df_to_csv(df)
    display_table(df)
    st.download_button(
        label="Download CSV file",
        data=csv_data,
        file_name="logs.csv",
        mime="text/csv"
    )



