# Funzione per verificare la sessione dell'utente
# def check_session():
#     """
#     Controlla se l'utente ha una sessione valida tramite i cookie e aggiorna lo stato di sessione.
#     """
    
#     if user_id:
#         log_timestamp = get_user_last_log(user_id) 
#         user = get_user(user_id)

#         if log_timestamp:
#             data_datetime = datetime.strptime(log_timestamp[0], '%Y-%m-%d %H:%M:%S')
#             log_life = datetime.now() - data_datetime - timedelta(hours=1)
#             if log_life < timedelta(minutes=1):
#                 st.sessiotime.sleep(0.5) n_state.clear()
#                 if "logged_in" not in st.session_state: 
#                     st.session_state.logged_in = True
#                 if "username" not in st.session_state: 
#                     st.session_state.username = user[0][1]
#                 if "user_id" not in st.session_state: 
#                     st.session_state.user_id = user_id
#                 if "page" not in st.session_state: 
#                     st.session_state.page = "main"
#             # Log ogni volta che l'utente accede alla sessione valida
#                 return True
#             else: 
#                 st.session_state.clear()
#                 if "logged_in" not in st.session_state: 
#                     st.session_state.logged_in = False 
#                 if "username" not in st.session_state: 
#                     st.session_state.username = None 
#                 if "user_id" not in st.session_state: 
#                     st.session_state.user_id = None 
#                 if "page" not in st.session_state: 
#                     st.session_state.page = "home"
#                 return False
#         else:
#             st.session_state.clear()
#             if "logged_in" not in st.session_state: 
#                 st.session_state.logged_in = False 
#             if "username" not in st.session_state: 
#                 st.session_state.username = None 
#             if "user_id" not in st.session_state: 
#                 st.session_state.user_id = None 
#             if "page" not in st.session_state: 
#                 st.session_state.page = "home"
#             return False
#     else:
#         st.session_state.logged_in = False
#         st.session_state.user_id = None
#         return False

