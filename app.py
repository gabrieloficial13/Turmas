import streamlit as st

# Lista de utilizadores (alunos e professores)
users = [
    {"user": "gabriel", "pass": "1234", "numEscolar": "12345", "role": "aluno"},
    {"user": "maria", "pass": "abcd", "numEscolar": "67890", "role": "aluno"},
    {"user": "joao", "pass": "senha", "numEscolar": "54321", "role": "aluno"},
    {"user": "prof_carlos", "pass": "prof123", "role": "professor"},
    {"user": "Administrador", "pass": "passwordprivadogabriel2013", "role": "professor"}
]

# Estado da sessão
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
            if encontrado["role"] == "aluno":
                st.success("Login correto! Agora insere o número escolar.")
            else:
                st.session_state.verificacao_ok = True  # Professores não precisam de número escolar
                st.success("Login correto! Bem-vindo professor.")
        else:
            st.error("Usuário ou senha incorretos.")

# Etapa 2: Verificação (só para alunos)
elif not st.session_state.verificacao_ok and st.session_state.userAtual["role"] == "aluno":
    st.header("Verificação")
    numEscolar = st.text_input("Número Escolar")
    if st.button("Confirmar"):
        if numEscolar == st.session_state.userAtual["numEscolar"]:
            st.session_state.verificacao_ok = True
            st.success("Verificação correta! Bem-vindo ao Turmas.")
        else:
            st.error("Número escolar inválido.")

# Página principal
else:
    role = st.session_state.userAtual["role"]

    if role == "aluno":
        st.header(f"Área do Aluno: {st.session_state.userAtual['user']}")
        st.markdown("### 📝 TPCs")
        st.write("Lista de trabalhos de casa atribuídos.")
        st.markdown("### 📊 Testes")
        st.write("Datas e notas dos testes.")
        st.markdown("### 📂 Trabalhos de Casa")
        st.write("Entrega e organização dos trabalhos.")
        st.markdown("### 💬 Chat")
        mensagem = st.text_input("Mensagem para o chat")
        if st.button("Enviar"):
            st.write(f"Tu: {mensagem}")

    elif role == "professor":
        st.header(f"Área do Professor: {st.session_state.userAtual['user']}")
        st.markdown("### ➕ Criar TPC")
        novo_tpc = st.text_area("Descrição do TPC")
        if st.button("Publicar TPC"):
            st.success("TPC publicado com sucesso!")

        st.markdown("### ➕ Criar Teste")
        novo_teste = st.text_input("Título do Teste")
        if st.button("Publicar Teste"):
            st.success("Teste publicado com sucesso!")

        st.markdown("### 💬 Chat com Alunos")
        mensagem_prof = st.text_input("Mensagem para os alunos")
        if st.button("Enviar Mensagem"):
            st.write(f"Professor: {mensagem_prof}")
