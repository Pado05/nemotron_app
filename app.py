from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st


load_dotenv(override=True)

API_KEY = os.getenv('OPENAI_API_KEY')
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)


richiesta = st.text_area("Scrivi la tua richiesta a Nemotron:")

completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "Sei un assistente per lo studio. Sei cortese e aiuti gli utenti con i loro compiti."},
        {"role": "user", "content": richiesta}
    ]
)
risposta = completion.choices[0].message.content


st.write(risposta)
                

