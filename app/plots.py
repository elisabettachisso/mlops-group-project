import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def plot_stimated_depression_indicator(risk_percentage):

    barra_colore = "green" if risk_percentage < 50 else "red"
    # create the gauge chart
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
    return fig_risk

def statistic_plots(df, risk_percentage):

    fig_academic = px.line(
        df,
        x='timestamp',
        y='academic_pressure',
        title="Academic Pressure",
        labels={'timestamp': "Time", 'academic_pressure': "Academic Pressure"}
    )

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

    fig_sleep = px.line(
        df,
        x='timestamp',
        y='sleep_duration_numeric',
        title="Sleep Duration (h)",
        labels={'timestamp': "Time", 'sleep_duration_numeric': "Durata del Sonno (ore)"},
    )

    st.plotly_chart(plot_stimated_depression_indicator(risk_percentage))  
            
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

