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
                