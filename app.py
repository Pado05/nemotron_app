from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st
import requests


load_dotenv(override=True)

API_KEY = os.getenv('OPENAI_API_KEY')
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

richiesta = st.input_text("Inserisci la tua richiesta")

completion = client.chat.completions.create(
                                            model=MODEL,
                                            messages=[
                                                {"role": "system", "content": "Sei un assistente per lo studio. Cortesemente aiutami con i compiti"},
                                                {"role": "user", "content": richiesta}
                                            ]
                                            )
st.write(completion.choices[0].message.content)

