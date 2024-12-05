### Function
- deadline:
21 gennaio

Domanda: quante settimane di lavoro?

7 settimane di lavoro:
- 7 sprints
    - sprint 1 : Brainstoarming + enviroment
        - 1 brainstorming and all the possible tasks. tutti i non functional + first sprint
    - sprint 2: scopo, requirements, functional and non functional.

- libreria, se funziona o no va detto e spiegato
- backlog di task per organizzare le altre settimane.

- Parte di software, data, backend frontend databse
- Data science: 
- test sincroni o asincroni.
 
### Struttura base
#### Funzionalità
1. utenti accedono alla piattaforma 
2. utenti si registrano e fanno il login 
3. ogni utente può visualizzare la propria dashboard 
4. la dashboard contiene le info sull'utente, le statistiche degli storici e la possibilità di fare un nuovo questionario + sezione suggerimenti aggionata 

#### Piano A (tools)
- Streamlit: piattaforma cloud
- Github: version control + project managment
- vs code: debug e sviluppo locale 
- SQLite: database 
- Kaggle: dataset 

#### Step 
1. Problem Definition;
2. Clear definition of a software development method and software process model;
3. Identification of:
    * Software Requirements;
    * Software Development Methods (strategies, versioning control);
    * Software Test (plan and strategy);
4. Dataset Information (KPI, data exploration and statistical analysis);
5. Proposed Pipeline (overview, discussion, performance evaluation, and justification);
6. Software organization (UML component and class diagram);
7. Software functionalities (UML use case, activity diagra,m or sequence diagram);
8. MLOps approaches and Issues9. Proposal limitations;
    * se usiamo SQLite: non ideale per applicazioni distribuite 

##### Machine learning 
- decision tree
- random forest 
- KNN


## LINK UTILI
https://github.com/mkhorasani/Streamlit-Authenticator


### struttura home page 
home: 
- statistiche
barra laterale con: 
- statistiche (home page)
- nuovo questionario 
- suggerimenti 

# Come gestire il database: brainstorming
- Logs? 
- Tabella dei questionari e basta? 
- Come gestire i nuovi questionari? 

Decisione: 
- tabella con questionari, ogni risposta al questionario ha associato
    - id utente che ha risposto 
    - orario 
- per le statische si usano tutti i questionari fatti dall'utente 
- per i suggerimenti si usa solo l'ultimo questionario compilato 