import streamlit as st

# Lista de utilizadores
users = [
    {"user": "Administrador", "pass": "adm.turmas001132", "numEscolar": "001013"},
    {"user": "maria", "pass": "abcd", "numEscolar": "67890"},
    {"user": "joao", "pass": "senha", "numEscolar": "54321"}
]

# Estado da sessão para login
if "userAtual" not in st.session_state:
    st.session_state.userAtual = None
if "login_ok" not in st.session_state:
    st.session_state.login_ok = False
if "verificacao_ok" not in st.session_state:
    st.session_state.verificacao_ok = False

st.title("APP Turmas")

# Etapa 1: Login
if not st.session_state.login_ok:
    st.header("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        encontrado = next((u for u in users if u["user"] == username and u["pass"] == password), None)
        if encontrado:
            st.session_state.userAtual = encontrado
            st.session_state.login_ok = True
            st.success("Login correto! Agora insere o número escolar.")
        else:
            st.error("Usuário ou senha incorretos.")

# Etapa 2: Verificação
elif not st.session_state.verificacao_ok:
    st.header("Verificação")
    numEscolar = st.text_input("Número Escolar")
    if st.button("Confirmar"):
        if numEscolar == st.session_state.userAtual["numEscolar"]:
            st.session_state.verificacao_ok = True
            st.success("Verificação correta! Bem-vindo ao Turmas.")
        else:
            st.error("Número escolar inválido.")

# Página principal (index)
else:
    st.header(f"Bem-vindo, {st.session_state.userAtual['user']} 👋")
    st.subheader("📚 Página Principal")

    # Secções
    st.markdown("### 📝 TPCs")
    st.write("Aqui podes ver e adicionar trabalhos de casa.")

    st.markdown("### 📊 Testes")
    st.write("Lista de testes e datas importantes.")

    st.markdown("### 📂 Trabalhos de Casa")
    st.write("Entrega e organização dos trabalhos.")

    st.markdown("### 💬 Chat")
    mensagem = st.text_input("Escreve uma mensagem para o chat")
    if st.button("Enviar"):
        st.write(f"Tu: {mensagem}")
