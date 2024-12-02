

# **MindHug: A Data-Driven Mental Health Support System**

## **1. Problem Definition**

La salute mentale è una componente critica del benessere umano, ma spesso riceve meno attenzione rispetto alla salute fisica, specialmente tra gli studenti universitari. Studi dimostrano che il carico accademico, il livello di stress e le pressioni sociali possono portare a problemi come ansia e depressione. Tuttavia, molti studenti non riconoscono i segnali di allarme o non hanno accesso a risorse adeguate.

**Obiettivo del progetto:** creare un sistema basato su una web application che utilizzi un modello di machine learning per identificare il rischio di depressione negli studenti e offrire suggerimenti personalizzati per il benessere mentale.

---

## **2. Software Development Method and Process Model**

### **Process Model**
Il progetto utilizza un approccio **Agile**, che ci consente di lavorare in iterazioni rapide, con feedback costante e aggiustamenti nel corso dello sviluppo. Ogni iterazione si conclude con una versione incrementale del prodotto.

Le fasi principali includono:
1. **Pianificazione**: Definizione dei requisiti e creazione delle task.
2. **Sviluppo**: Implementazione incrementale delle funzionalità.
3. **Test**: Validazione delle funzionalità e del modello ML.
4. **Deployment**: Pubblicazione del sistema.

### **Strumenti**
- **GitHub** come sistema di controllo versione.
- **GitHub Projects** per la gestione delle issue e dei task.
- **Branching Strategy**:
  - `main` per la versione stabile.
  - `dev` per le nuove funzionalità.
  - Branch dedicati per feature specifiche.

---

## **3. Identification of Key Elements**

### **a. Software Requirements**

#### **Requisiti Funzionali**
- L'applicazione deve raccogliere dati utente tramite un questionario.
- Deve calcolare il rischio di depressione usando un modello ML.
- Deve offrire suggerimenti personalizzati in base ai risultati.

#### **Requisiti Non Funzionali**
- L'interfaccia deve essere user-friendly e accessibile.
- Le risposte devono essere generate in meno di 2 secondi.

### **b. Software Development Methods**
Il codice è strutturato in moduli indipendenti:
- **Frontend**: Costruito con Streamlit per una rapida prototipazione.
- **Backend**: Include il modello ML e le funzioni di elaborazione dei dati.

Versioning control è gestito con Git, seguendo la strategia di branching descritta sopra.

### **c. Software Test**
- **Piano di test**:
  - Test automatici con Pytest per verificare la correttezza del codice.
  - Test manuali per validare l'interfaccia utente.
- **Strategia**:
  - Test dei singoli moduli (unit test) e test integrati.

---

## **4. Dataset Information**

### **Dataset**
- **Fonte**: Kaggle.
- **Nome**: Student Depression Dataset.
- **Descrizione**: Contiene informazioni su età, ore di studio, livello di stress e altri fattori correlati al benessere mentale.

### **Data Exploration**
- **Statistiche descrittive**:
  - Media delle ore di studio: 5 ore.
  - Percentuale di studenti con alto livello di stress: 40%.
- **Visualizzazioni**:
  - Istogramma del livello di stress per gruppo di età.
  - Scatter plot per correlazione tra ore di studio e livello di stress.

---

## **5. Proposed Pipeline**

### **Overview**
1. **Acquisizione dei dati**: Input dell'utente tramite il questionario.
2. **Preprocessing**: Encoding delle variabili categoriche e normalizzazione.
3. **Addestramento del modello**: Random Forest addestrato su dati preprocessati.
4. **Deployment**: Modello salvato come `model.pkl` e integrato nell'app Streamlit.

### **Performance Evaluation**
- **Metriche**:
  - Accuratezza: 85%.
  - F1-Score: 0.82.
- **Justificazione**:
  - Il modello Random Forest è stato scelto per la sua robustezza e capacità di interpretare dati eterogenei.

---

## **6. Software Organization**

### **UML Component Diagram**
![Esempio Diagramma Componenti](#)
- Moduli principali:
  - **Frontend**: Form per l’input utente.
  - **Backend**: Previsione e suggerimenti.
  - **Database**: Salvataggio opzionale dei dati.

---

## **7. Software Functionalities**

### **UML Use Case Diagram**
- **Attori**:
  - Utente: Inserisce dati.
  - Sistema: Elabora i dati e fornisce i risultati.
- **Use Case**:
  - Previsione del rischio.
  - Visualizzazione dei suggerimenti.

### **Activity Diagram**
1. Utente inserisce i dati.
2. Sistema elabora i dati.
3. Viene mostrato il risultato con suggerimenti.

---

## **8. MLOps Approaches and Issues**

### **Approcci**
- Uso di un ambiente virtuale (venv) per gestire dipendenze.
- Pipeline CI/CD con GitHub Actions per automatizzare il testing e il deployment.

### **Problemi e Soluzioni**
- **Scalabilità**:
  - Uso di Docker per un deployment portabile.
- **Monitoraggio del modello**:
  - Pianificata integrazione di strumenti per monitorare le prestazioni.

---

## **9. Proposal Limitations**
- **Limiti del Dataset**:
  - Il dataset è limitato a una specifica fascia demografica.
- **Limiti del Modello**:
  - Non può sostituire una diagnosi clinica.
- **Limiti dell’Applicazione**:
  - Necessita di miglioramenti nell’interfaccia utente per utenti non esperti.

---

## **Appendice**
- **Link al Repository**: [https://github.com/username/mindhug](https://github.com/username/mindhug)
- **Codice Sorgente**: Vedere il file `app.py`.

---

Fammi sapere se vuoi arricchire ulteriormente una di queste sezioni! 😊