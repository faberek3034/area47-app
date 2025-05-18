import streamlit as st
from cryptography.fernet import Fernet

# Schlüssel generieren oder aus Session laden
if 'cipher_key' not in st.session_state:
    st.session_state.cipher_key = Fernet.generate_key()
    st.session_state.cipher_suite = Fernet(st.session_state.cipher_key)

# Benutzer-Login
st.title("🛡️ Area 47 – Verschlüsselter Chat")

if 'user' not in st.session_state:
    user = st.selectbox("Wähle deinen Nutzer", ["User1", "User2"])
    if st.button("Anmelden"):
        st.session_state.user = user
        st.success(f"Angemeldet als {user}")
        st.experimental_rerun()

if 'user' in st.session_state:
    st.write(f"👋 Hallo, **{st.session_state.user}**!")

    # Nachrichten initialisieren
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    st.write("### ✉️ Neue Nachricht senden")
    msg = st.text_input("Nachricht eingeben")

    if st.button("🔐 Verschlüsselt senden") and msg:
        encrypted_msg = st.session_state.cipher_suite.encrypt(msg.encode()).decode()
        st.session_state.messages.append({
            'sender': st.session_state.user,
            'encrypted_msg': encrypted_msg
        })
        st.success("Nachricht wurde verschlüsselt gesendet!")

    st.write("---")
    st.write("### 🗂️ Chatverlauf (verschlüsselte Nachrichten)")

    for idx, message in enumerate(st.session_state.messages):
        st.write(f"📨 Von {message['sender']}:")
        st.code(message['encrypted_msg'], language='text')

        if st.button(f"🔓 Entschlüsseln Nachricht {idx+1}"):
            try:
                decrypted = st.session_state.cipher_suite.decrypt(message['encrypted_msg'].encode()).decode()
                st.success(f"🔍 Entschlüsselte Nachricht: {decrypted}")
            except Exception as e:
                st.error(f"❌ Fehler beim Entschlüsseln: {e}")
import streamlit as st
from cryptography.fernet import Fernet

# Schlüssel erstellen (für Demo: global gleich)
if 'cipher_key' not in st.session_state:
    st.session_state.cipher_key = Fernet.generate_key()
    st.session_state.cipher_suite = Fernet(st.session_state.cipher_key)

# Login per Handynummer
st.title("📱 Area 47 – Sicherer Freundes-Chat")

if 'user' not in st.session_state:
    phone = st.text_input("📞 Deine Handynummer eingeben", max_chars=15)
    if st.button("🔐 Einloggen") and phone:
        st.session_state.user = phone
        st.success(f"Willkommen {phone}!")
        st.experimental_rerun()

# Nach Login: Chat anzeigen
if 'user' in st.session_state:
    st.write(f"👋 Eingeloggt als **{st.session_state.user}**")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Neue Nachricht senden
    st.write("### ✉️ Neue Nachricht")
    msg = st.text_input("Nachricht schreiben")

    if st.button("📤 Senden") and msg:
        encrypted = st.session_state.cipher_suite.encrypt(msg.encode()).decode()
        st.session_state.messages.append({
            'sender': st.session_state.user,
            'encrypted_msg': encrypted
        })
        st.success("Nachricht wurde gesendet und verschlüsselt!")

    st.write("---")
    st.write("### 💬 Chatverlauf")

    for i, msg in enumerate(st.session_state.messages):
        st.write(f"📨 **{msg['sender']}** schreibt:")
        st.code(msg['encrypted_msg'])

        if st.button(f"🔓 Entschlüsseln {i+1}"):
            try:
                decrypted = st.session_state.cipher_suite.decrypt(msg['encrypted_msg'].encode()).decode()
                st.success(f"🔓 Entschlüsselte Nachricht: {decrypted}")
            except:
                st.error("❌ Fehler beim Entschlüsseln")