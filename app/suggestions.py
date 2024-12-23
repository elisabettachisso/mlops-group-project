import random
from database import get_suggestions

def map_response_to_levels(response):

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
        levels['suicidal_thoughts'] = 1 

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

    # category ID map
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

    # select 3 random categories
    selected_categories = random.sample(range(1, 9), 3)
    # load all the suggestions from the database
    responses = get_suggestions()

    if responses:
        final_3suggestions = []

        for category in selected_categories:
            suggestions = [
                response
                for response in responses
                if response[3] == category and levels[category_mapping[category]] == response[4]
            ]
            if suggestions:  # check if there are any suggestions available.
                final_3suggestions.append(random.choice(suggestions))
            else:
                # add a message or an alternative suggestion if no data is available
                final_3suggestions.append(("No suggestions available", "Consider exploring more general tips.", None))

        return final_3suggestions
    else:
        # if no responses are available, return a fallback value.
        return [("No data", "No suggestions found in the database.", None)]
