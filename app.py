from openai import OpenAI
import os
#from dotenv import load_dotenv
import streamlit as st


API_KEY = st.secrets["OPENAI_API_KEY"]
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Titolo
st.title("🤖 Chat con Nemotron")
st.markdown("Assistente AI per lo studio - Conversazione in memoria")

# Inizializza la cronologia messaggi nel session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Contenitore per visualizzare i messaggi
messages_container = st.container()

# Visualizza tutti i messaggi precedenti
with messages_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message["content"])

# Input per il nuovo messaggio
user_input = st.chat_input("Scrivi il tuo messaggio...", key="chat_input")

# Elabora il messaggio dell'utente
if user_input:
    # Aggiungi il messaggio dell'utente alla cronologia
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Visualizza il messaggio dell'utente
    with messages_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
    
    # Spinner durante l'elaborazione
    with st.spinner("🤔 Nemotron sta pensando..."):
        try:
            # Prepara i messaggi per l'API (include tutta la cronologia)
            api_messages = [
                {"role": "system", "content": "Sei un assistente utile per lo studio. Sei cortese, preciso e aiuti gli utenti con i loro compiti e domande."}
            ]
            # Aggiungi tutti i messaggi della cronologia
            api_messages.extend(st.session_state.messages)
            
            # Chiama l'API Nemotron
            completion = client.chat.completions.create(
                model=MODEL,
                messages=api_messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Estrai la risposta
            assistant_response = completion.choices[0].message.content
            
            # Aggiungi la risposta alla cronologia
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Visualizza la risposta
            with messages_container:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(assistant_response)
            
        except Exception as e:
            st.error(f"❌ Errore: {str(e)}")

# Sidebar con opzioni
with st.sidebar:
    st.title("⚙️ Opzioni")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Cancella chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Mostra il numero di messaggi
    num_messages = len(st.session_state.messages)
    st.info(f"📊 Messaggi in chat: {num_messages}")
    
    st.divider()
    st.markdown("### ℹ️ Info")
    st.markdown("""
    - **Modello**: Nvidia Nemotron 3 Super 120B
    - **Provider**: OpenRouter
    - **La conversazione è memorizzata** nella sessione attuale
    """)


