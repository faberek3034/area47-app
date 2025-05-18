import streamlit as st
from cryptography.fernet import Fernet

# Schlüssel generieren (in Produktion anders lösen!)
key = Fernet.generate_key()
cipher = Fernet(key)

# Nachrichten speichern
if 'msgs' not in st.session_state:
    st.session_state.msgs = []

st.title("🔐 Area 47 – Verschlüsselter Chat")

# Anmeldung
username = st.sidebar.text_input("Benutzername")
contact = st.sidebar.text_input("E-Mail oder Handynummer")
if st.sidebar.button("Anmelden"):
    st.session_state.user = username
    st.success(f"Angemeldet als {username}")

# Nur wenn angemeldet
if 'user' in st.session_state:
    # Nachricht eingeben
    txt = st.text_input("Nachricht eingeben")
    if st.button("Senden"):
        enc = cipher.encrypt(txt.encode())
        st.session_state.msgs.append({'from': st.session_state.user, 'enc': enc})

    st.subheader("Nachrichten")
    for i, m in enumerate(st.session_state.msgs):
        st.write(f"Von: {m['from']}")
        if st.button(f"Entschlüsseln Nachricht {i+1}"):
            dec = cipher.decrypt(m['enc']).decode()
            st.write(f"→ {dec}")
        st.write("---")
