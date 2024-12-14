# MindHug

MindHug is a Streamlit-based application designed to promote mental well-being by analyzing lifestyle patterns and providing actionable suggestions. The application allows users to monitor their mental health, visualize their progress, and receive personalized recommendations based on data from self-assessment questionnaires.

---

## Table of Contents
- [MindHug](#mindhug)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Technologies Used](#technologies-used)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Key Features](#key-features)
  - [Future Improvements](#future-improvements)

---

## Features

- **User Authentication**: Secure login and registration system for personalized access.
- **Self-Assessment Questionnaires**: Users can input lifestyle data to evaluate their mental health risk factors.
- **Personalized Recommendations**: Based on questionnaire responses, the app suggests tailored tips for improvement.
- **Data Visualization**: Interactive charts and graphs to track progress over time.
- **Admin Features**: Administrators can manage users, suggestions, can visualize general statistics charts and download data in CSV format.
- **Analyst Features**: Analyst can visualize general statistics charts and download data in CSV format.
---

## Project Structure

The repository is organized as follows:

```
mlops-group-project\
├── app 
│   ├── __init__.py           # Marks this directory as a Python package
│   ├── __pycache__\          # Compiled Python cache files
│   ├── auth.py               # Handles user authentication 
│   ├── cookies.py            # Manages user session cookies
│   ├── database.py           # Manages SQLite database interactions
│   ├── images\              # Stores app-related images
│   │   └── logomindhug.png
│   ├── main.py               # Entry point for the Streamlit app
│   ├── mindhug.db            # SQLite database file
│   ├── ml_utils.py           # Machine learning utilities 
│   ├── model\               # Directory for storing ML models
│   │   └── random_forest_model.pkl
│   ├── pages.py              # Defines application pages
│   ├── plots.py              # Handles data visualization
│   ├── suggestions.py        # Logic for generating personalized suggestions
│   ├── utils.py              # Helper functions for data conversion
├── notebooks
└── README.md 
```

---

## Technologies Used

- **Programming Language**: Python
- **Web Framework**: Streamlit
- **Database**: SQLite
- **Data Visualization**: Plotly, Pandas
- **Machine Learning**: Scikit-learn (Random Forest Model)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mindhug.git
   cd mindhug
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Modify paths:
   - In pages.py: set `logo_path` = `images/logomindhug.png`
   - In ml_utils.py: set `model_path` = `model/random_forest_model.pkl` 

---

## Usage

Run the application locally:

```bash
cd app
streamlit run main.py
```

### Key Features

- **Users**: Complete self-assessment questionnaires, view personalized suggestions, and track mental health progress.
- **Admin**: Manage users, upload suggestions via CSV, and access overall statistics.
- **Analyst**: Download CSV data and view general statistics.

---

## Future Improvements

Here are some potential enhancements to the application:

- **Session Management**:
  - Refactor the cookie handling to make it more secure and scalable.

- **Database Enhancements**:
  - Implement database migrations for easier schema updates.

- **Machine Learning**:
  - Explore additional models to improve risk prediction accuracy.

- **User Experience**:
  - Add multi-language support.
  - Integrate notifications or email alerts for updates and reminders.