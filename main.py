import streamlit as st
import os
import openai

from i18n import TRANSLATIONS

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_TEMPERATURE = os.getenv("MODEL_TEMPERATURE")
MODEL_FREQUENCY_PENALTY = os.getenv("MODEL_FREQUENCY_PENALTY")
MODEL_URL = os.getenv("MODEL_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_TIMEOUT = os.getenv("MODEL_TIMEOUT")

GROQ_API_KEY="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"
MODEL_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "openai/gpt-oss-20b"
MODEL_TIMEOUT = 320
MODEL_TEMPERATURE = 0.3
MODEL_FREQUENCY_PENALTY = 0.5


def get_model_response(user_notes):
    response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": user_notes}],
            temperature=MODEL_TEMPERATURE,
            frequency_penalty=MODEL_FREQUENCY_PENALTY
        )
    return response.choices[0].message.content


client = openai.OpenAI(
    base_url=MODEL_URL,
    api_key=GROQ_API_KEY,
    timeout=MODEL_TIMEOUT
)

SYSTEM_PROMPT = '''
You are a flashcard generator.
Your task is to analyze the provided notes and extract key facts into concise, atomic Q&A flashcards suitable for import into flashcard applications (Anki, Quizlet).

STRICT OUTPUT RULES:
1. Output ONLY raw Tab-Separated Values (TSV) text.
2. Do NOT include any greetings, intros, or summaries.
3. Separate the front and back of each card using a single Tab character.
5. Place each flashcard on a new line.
6. Create flashcards in the SAME language as the input notes, unless the user explicitly requests another language.
7. Missing Explanations: If the input contains only terms, concepts, or keywords without definitions, automatically generate concise, accurate explanations/definitions for them in the same language.

FORMAT BASED ON CONTENT TYPE:
1. For concepts: Term   Definition
2. For questions: Question  Answer
'''



langs_available = list(TRANSLATIONS.keys())

selected_lang = st.segmented_control(label="", options=langs_available, default=langs_available[0])
t = TRANSLATIONS[selected_lang]

st.title(t["title"])
st.markdown(t["description"])

with st.form(key="text_input"):
    user_notes = st.text_area(t["input_label"],
                              height=250,
                                placeholder=t["placeholder"])
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_btn = st.form_submit_button(t["button"], use_container_width=True)

if submit_btn:

    if user_notes.strip():

        with st.spinner(t["spinner"]):
            agent_response = get_model_response(user_notes)

        st.subheader(t["results_header"])
        st.write(t["copy_instruction"])
        st.code(agent_response,
                language="text",
                wrap_lines=True)
        st.write(t["download_instruction"])
        st.download_button(
            label=t["download_btn"],
            data=agent_response,
            file_name="flashcards.tsv",
            mime="text/tab-separated-values"
        )
        st.caption(t["caption"])