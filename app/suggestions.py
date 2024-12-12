import random
import sqlite3

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
    if response['academic_pressure'] in [1, 2]:
        levels['academic_pressure'] = 0
    elif response['academic_pressure'] == 3:
        levels['academic_pressure'] = 1
    else:  # [4, 5]
        levels['academic_pressure'] = 2

    # CGPA
    if 8.0 <= response['cgpa'] <= 10.0:
        levels['cgpa'] = 0
    elif 6.0 <= response['cgpa'] < 8.0:
        levels['cgpa'] = 1
    else:  # 1.0 <= cgpa < 6.0
        levels['cgpa'] = 2

    # Study Satisfaction
    if response['study_satisfaction'] in [4, 5]:
        levels['study_satisfaction'] = 0
    elif response['study_satisfaction'] == 3:
        levels['study_satisfaction'] = 1
    else:  # [1, 2]
        levels['study_satisfaction'] = 2

    # Sleep Duration
    if response['sleep_duration'] in ["7-8 hours", "More than 8 hours"]:
        levels['sleep_duration'] = 0
    elif response['sleep_duration'] == "5-6 hours":
        levels['sleep_duration'] = 1
    elif response['sleep_duration'] == "Less than 5 hours":
        levels['sleep_duration'] = 2

    # Dietary Habits
    if response['dietary_habits'] == "Healty":
        levels['dietary_habits'] = 0
    elif response['dietary_habits'] == "Moderate":
        levels['dietary_habits'] = 1
    else:  # "Unhealty"
        levels['dietary_habits'] = 2

    # Suicidal Thoughts
    if response['suicidal_thoughts'] == "No":
        levels['suicidal_thoughts'] = 0
    else:  # "Yes"
        levels['suicidal_thoughts'] = 1  # Trattiamo 1 e 2 come stesso livello

    # Study Hours
    if 0 <= response['study_hours'] <= 2:
        levels['study_hours'] = 0
    elif 3 <= response['study_hours'] <= 5:
        levels['study_hours'] = 1
    else:  # 6 <= study_hours <= 10
        levels['study_hours'] = 2

    # Financial Stress
    if response['financial_stress'] in [0, 1]:
        levels['financial_stress'] = 0
    elif response['financial_stress'] in [2, 3]:
        levels['financial_stress'] = 1
    else:  # [4, 5]
        levels['financial_stress'] = 2

    return levels

def select_random_suggestions(levels, db_path="db/mindhug.db"):
    """
    Seleziona 3 categorie casuali e un suggerimento casuale per ciascuna categoria in base al livello specificato.
    
    Parameters:
        levels (dict): Dizionario con le categorie e i livelli calcolati.
        db_path (str): Percorso al database SQLite con i suggerimenti.
        
    Returns:
        list: Lista di dizionari con i suggerimenti selezionati.
    """
    # Mappa degli ID categoria
    category_mapping = {
        1: "sleep-duration",
        2: "dietary-habits",
        3: "study-satisfaction",
        4: "study-hours",
        5: "academic-pressure",
        6: "cgpa",
        7: "financial-stress",
        8: "suicidal-thoughts"
    }
    
    # Inverti il mapping per ottenere ID categoria da nome
    category_to_id = {v: k for k, v in category_mapping.items()}
    
    # Seleziona 3 categorie casuali
    selected_categories = random.sample(list(levels.keys()), 3)
    
    # Connessione al database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    suggestions = []
    
    for category in selected_categories:
        # Ottieni il livello per la categoria
        level = levels[category]
        category_id = category_to_id[category]
        
        # Query per ottenere i suggerimenti
        query = """
        SELECT id, title, description 
        FROM suggestions 
        WHERE category_id = ? AND level = ?
        """
        cursor.execute(query, (category_id, level))
        results = cursor.fetchall()
        
        # Se ci sono risultati, seleziona uno a caso
        if results:
            suggestion = random.choice(results)
            suggestions.append({
                "category": category,
                "suggestion_id": suggestion[0],
                "title": suggestion[1],
                "description": suggestion[2]
            })
    
    # Chiudi la connessione
    conn.close()
    
    return suggestions