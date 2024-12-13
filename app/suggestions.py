import random
import sqlite3
from database import get_suggestions

def map_response_to_levels(response):
    """
    Mappa i valori delle 8 categorie nei rispettivi livelli (0, 1, 2).

    Args:
        response (dict): Un dizionario con i valori delle 8 categorie da mappare.

    Returns:
        dict: Un dizionario con i livelli associati a ciascuna categoria.
    """
    levels = {}

    # Academic Pressure
    if response[0][4] in [1, 2]:
        levels['academic_pressure'] = 0
    elif response[0][4] == 3:
        levels['academic_pressure'] = 1
    else:  # [4, 5]
        levels['academic_pressure'] = 2

    # CGPA
    if 8.0 <= response[0][5] <= 10.0:
        levels['cgpa'] = 0
    elif 6.0 <= response[0][5] < 8.0:
        levels['cgpa'] = 1
    else:  # 1.0 <= cgpa < 6.0
        levels['cgpa'] = 2

    # Study Satisfaction
    if response[0][6] in [4, 5]:
        levels['study_satisfaction'] = 0
    elif response[0][6] == 3:
        levels['study_satisfaction'] = 1
    else:  # [1, 2]
        levels['study_satisfaction'] = 2

    # Sleep Duration
    if response[0][7] in ["7-8 hours", "More than 8 hours"]:
        levels['sleep_duration'] = 0
    elif response[0][7] == "5-6 hours":
        levels['sleep_duration'] = 1
    elif response[0][7] == "Less than 5 hours":
        levels['sleep_duration'] = 2
    else:
        levels['sleep_duration'] = 0

    # Dietary Habits
    if response[0][9] == "Healty":
        levels['dietary_habits'] = 0
    elif response[0][9] == "Moderate":
        levels['dietary_habits'] = 1
    else:  # "Unhealty"
        levels['dietary_habits'] = 2

    # Suicidal Thoughts
    if response[0][10] == "No":
        levels['suicidal_thoughts'] = 0
    else:  # "Yes"
        levels['suicidal_thoughts'] = 1  # Trattiamo 1 e 2 come stesso livello

    # Study Hours
    if 0 <= response[0][11] <= 2:
        levels['study_hours'] = 0
    elif 3 <= response[0][11] <= 5:
        levels['study_hours'] = 1
    else:  # 6 <= study_hours <= 10
        levels['study_hours'] = 2

    # Financial Stress
    if response[0][12] in [0, 1]:
        levels['financial_stress'] = 0
    elif response[0][12] in [2, 3]:
        levels['financial_stress'] = 1
    else:  # [4, 5]
        levels['financial_stress'] = 2

    return levels

def select_random_suggestions(last_response):
    """
    Seleziona 3 categorie casuali e un suggerimento casuale per ciascuna categoria in base al livello specificato.
    
    Parameters:
        levels (dict): Dizionario con le categorie e i livelli calcolati.
        db_path (str): Percorso al database SQLite con i suggerimenti.
        
    Returns:
        list: Lista di dizionari con i suggerimenti selezionati.
    """
    # Mappa degli ID categoria
    levels = map_response_to_levels(last_response)

    category_mapping = {
        1: "sleep_duration",
        2: "dietary_habits",
        3: "study_satisfaction",
        4: "study_hours",
        5: "academic_pressure",
        6: "cgpa",
        7: "financial_stress",
        8: "suicidal_thoughts"
    }
    
    # Inverti il mapping per ottenere ID categoria da nome
    category_to_id = {v: k for k, v in category_mapping.items()}
    
    # Seleziona 3 categorie casuali
    selected_categories = random.sample(range(1, 9), 3)
    
    # Connessione al database
    responses = get_suggestions()
    

    suggestions = []
    final_3suggestions = []
    
    for category in selected_categories:
        suggestions.clear()
        for response in responses: 
            if response[3] == category:
                if levels[category_mapping[category]] == response[4]:
                    suggestions.append(response)
        final_3suggestions.append(random.choice(suggestions))
    
    return final_3suggestions