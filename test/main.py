import streamlit as st
from auth import login, registration
from database import initialize_database
from route import go_to_login, go_to_register, logout

initialize_database()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if "page" not in st.session_state:
    st.session_state.page = "home"



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

    # Bottone per analizzare i dati
    if st.button("Calcola il tuo stato"):
        # Esempio 
        if stress_level == "Alto" or exercise == "No":
            st.error("Attenzione: il tuo livello di benessere potrebbe essere a rischio.")
            st.write("Ti consigliamo di prendere una pausa e considerare tecniche di rilassamento.")
        else:
            st.success("Ottimo! Il tuo benessere mentale sembra in buone condizioni.")
            st.write("Continua così e non dimenticare di prenderti del tempo per te stesso.")

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

def main():
    if st.session_state.logged_in:
        main_page()
    else:
        if st.session_state.page == "home":
            home_page()
        elif st.session_state.page == "login":
            if login():
                st.session_state.page = "main"
                st.rerun()
        elif st.session_state.page == "register":
            registration()


if __name__ == "__main__":
    main()