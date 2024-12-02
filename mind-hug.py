import streamlit as st

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


st.image("logomindhug.png", width=200)  

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
