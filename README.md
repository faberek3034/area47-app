# 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
import streamlit as st
from cryptography.fernet import Fernet

# Generiere einen Schlüssel (normalerweise für jeden Chat individuell)
# Für Demo hier ein fixer Schlüssel
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Einfacher Nutzer-Login (simuliert)
st.title("Area 47 - Verschlüsselter Chat")

if 'user' not in st.session_state:
    user = st.selectbox("Wähle deinen Nutzer", ["User1", "User2"])
    if st.button("Anmelden"):
        st.session_state.user = user
        st.experimental_rerun()

if 'user' in st.session_state:
    st.write(f"Hallo, {st.session_state.user}!")

    # Chatnachrichten speichern (für Demo in Session State)
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Eingabe für neue Nachricht
    msg = st.text_input("Neue Nachricht")

    if st.button("Senden") and msg:
        # Nachricht verschlüsseln
        encrypted_msg = cipher_suite.encrypt(msg.encode()).decode()
        # Nachricht speichern mit Sender und verschlüsseltem Text
        st.session_state.messages.append({
            'sender': st.session_state.user,
            'encrypted_msg': encrypted_msg
        })

    st.write("### Chatverlauf (verschlüsselt):")
    for i, message in enumerate(st.session_state.messages):
        st.write(f"{message['sender']}: {message['encrypted_msg']}")
        # Button zum Entschlüsseln
        if st.button(f"Entschlüsseln Nachricht {i}"):
            decrypted_msg = cipher_suite.decrypt(message['encrypted_msg'].encode()).decode()
            st.success(f"Entschlüsselte Nachricht: {decrypted_msg}")