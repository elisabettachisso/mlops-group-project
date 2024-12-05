import streamlit as st
from database import initialize_database, add_response, get_responses
from route import go_to_login, go_to_register, logout

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

    # Intestazione
    st.title("🧠 MindHug")
    st.subheader("Il tuo supporto per il benessere mentale")
    st.write(
        "Benvenuto in **MindHug**, un'app progettata per aiutarti a monitorare il tuo benessere mentale "
        "e fornire suggerimenti personalizzati per prenderti cura di te stesso."
    )


    st.image("images/logomindhug.png", width=200)  

    # Sezione di input
    st.markdown("### Compila il questionario")
    age = st.number_input("Quanti anni hai?", min_value=1, max_value=100, step=1)
    study_hours = st.slider("Quante ore studi al giorno?", min_value=0, max_value=16, step=1)
    stress_level = st.selectbox(
        "Come descriveresti il tuo livello di stress?",
        ["Basso", "Moderato", "Alto"]
    )
    exercise = st.selectbox(
        "Fai esercizio fisico regolarmente?",
        ["Sì", "No"]
    )
    if st.button("Invia risposta"): 
        if add_response(st.session_state.user_id, age, study_hours, stress_level, exercise): 
            st.success("Risposta inviata con successo!") 
        else: st.error("Si è verificato un errore durante l'invio della risposta.")
    st.write("Risposte al questionario:") 
    responses = get_responses() 
    for res in responses: 
        st.write(res)

    # Sezione aggiuntiva
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