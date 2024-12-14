import streamlit as st

def convert_df_to_csv(df):
    # Usa io.StringIO per creare un buffer in memoria
    csv = df.to_csv(index=False)
    return csv

def display_table(df):
    st.subheader("Data:")
    st.dataframe(df)
