import streamlit as st
from datetime import date

# --------------------------------------------------------------------
# "Base de dados" simples em memória (apenas para exemplo)
# Em produção isto deve vir de uma BD real (SQLite, PostgreSQL, etc.)
# --------------------------------------------------------------------
USERS_DB = {
    "aluno1": {
        "password": "1234",
        "numero_escolar": "2023001",
        "nome": "João Silva"
    },
    "aluna2": {
        "password": "abcd",
        "numero_escolar": "2023002",
        "nome": "Maria Costa"
    },
    "professor1": {
        "password": "prof123",
        "numero_escolar": "900001",
        "nome": "Professor António"
    }
}

# --------------------------------------------------------------------
# Funções auxiliares
# --------------------------------------------------------------------
def init_session_state():
    """Inicializa variáveis na sessão, se ainda não existirem."""
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
    if "numero_verificado" not in st.session_state:
        st.session_state.numero_verificado = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "tpcs" not in st.session_state:
        st.session_state.tpcs = []  # lista de dicionários
    if "testes" not in st.session_state:
        st.session_state.testes = []  # lista de dicionários


def login(username: str, password: str) -> bool:
    """Valida username e password na 'base de dados'."""
    user = USERS_DB.get(username)
    if not user:
        return False
    if user["password"] != password:
        return False
    st.session_state.is_authenticated = True
    st.session_state.current_user = username
    return True


def verificar_numero_escolar(numero: str) -> bool:
    """Verifica se o número escolar corresponde ao utilizador autenticado."""
    username = st.session_state.current_user
    if not username:
        return False
    user = USERS_DB.get(username)
    if not user:
        return False
    if user["numero_escolar"] == numero:
        st.session_state.numero_verificado = True
        return True
    return False


def logout():
    """Termina sessão do utilizador."""
    st.session_state.is_authenticated = False
    st.session_state.numero_verificado = False
    st.session_state.current_user = None


# --------------------------------------------------------------------
# Interfaces (páginas)
# --------------------------------------------------------------------
def pagina_login():
    st.title("Portal da Escola - Login")

    st.write("Por favor, faz login com o teu utilizador e senha.")

    with st.form("login_form"):
        username = st.text_input("Utilizador")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

    if submit:
        if login(username, password):
            st.success("Login efetuado com sucesso!")
        else:
            st.error("Utilizador ou senha incorretos.")


def pagina_verificacao_numero():
    st.title("Verificação do Número Escolar")

    username = st.session_state.current_user
    user = USERS_DB.get(username)
    st.write(f"Olá, **{user['nome']}** ({username}).")
    st.write("Para continuar, insere o teu **número escolar** para verificação.")

    with st.form("numero_escolar_form"):
        numero = st.text_input("Número escolar")
        submit = st.form_submit_button("Verificar")

    if submit:
        if verificar_numero_escolar(numero):
            st.success("Número escolar verificado com sucesso! Já podes aceder às páginas da plataforma.")
        else:
            st.error("Número escolar inválido para este utilizador.")


def pagina_registar_tpcs():
    st.header("Registar TPCs (Trabalhos de Casa)")

    with st.form("form_tpc"):
        disciplina = st.text_input("Disciplina")
        descricao = st.text_area("Descrição do TPC")
        data_entrega = st.date_input("Data de entrega", value=date.today())
        submit = st.form_submit_button("Guardar TPC")

    if submit:
        if not disciplina or not descricao:
            st.error("Por favor preenche todos os campos antes de guardar.")
        else:
            novo_tpc = {
                "disciplina": disciplina,
                "descricao": descricao,
                "data_entrega": data_entrega,
                "autor": st.session_state.current_user
            }
            st.session_state.tpcs.append(novo_tpc)
            st.success("TPC registado com sucesso!")

    st.subheader("Lista de TPCs registados")
    if not st.session_state.tpcs:
        st.info("Ainda não existem TPCs registados.")
    else:
        for i, tpc in enumerate(st.session_state.tpcs, start=1):
            st.markdown(f"**TPC {i}**")
            st.write(f"**Disciplina:** {tpc['disciplina']}")
            st.write(f"**Descrição:** {tpc['descricao']}")
            st.write(f"**Data de entrega:** {tpc['data_entrega']}")
            st.write(f"**Registado por:** {tpc['autor']}")
            st.markdown("---")


def pagina_registar_testes():
    st.header("Registar Testes")

    with st.form("form_teste"):
        disciplina = st.text_input("Disciplina do teste")
        temas = st.text_area("Temas do teste")
        data_teste = st.date_input("Data do teste", value=date.today())
        tipo = st.selectbox("Tipo de avaliação", ["Teste", "Ficha de avaliação", "Exame", "Outro"])
        submit = st.form_submit_button("Guardar Teste")

    if submit:
        if not disciplina or not temas:
            st.error("Por favor preenche todos os campos antes de guardar.")
        else:
            novo_teste = {
                "disciplina": disciplina,
                "temas": temas,
                "data": data_teste,
                "tipo": tipo,
                "autor": st.session_state.current_user
            }
            st.session_state.testes.append(novo_teste)
            st.success("Teste registado com sucesso!")

    st.subheader("Lista de testes registados")
    if not st.session_state.testes:
        st.info("Ainda não existem testes registados.")
    else:
        for i, teste in enumerate(st.session_state.testes, start=1):
            st.markdown(f"**Teste {i}**")
            st.write(f"**Disciplina:** {teste['disciplina']}")
            st.write(f"**Temas:** {teste['temas']}")
            st.write(f"**Data:** {teste['data']}")
            st.write(f"**Tipo:** {teste['tipo']}")
            st.write(f"**Registado por:** {teste['autor']}")
            st.markdown("---")


# --------------------------------------------------------------------
# Layout principal da app
# --------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Portal da Escola", page_icon="🎓", layout="wide")
    init_session_state()

    # Barra lateral
    with st.sidebar:
        st.title("Portal da Escola")
        if st.session_state.is_authenticated:
            user = USERS_DB.get(st.session_state.current_user)
            st.write(f"**Utilizador:** {user['nome']}")
            st.write(f"**Número escolar:** {user['numero_escolar']}")
            if st.button("Terminar sessão"):
                logout()
                st.experimental_rerun()
        else:
            st.write("Não autenticado.")

        st.markdown("---")
        # Navegação (só aparece se já estiver autenticado e com número verificado)
        if st.session_state.is_authenticated and st.session_state.numero_verificado:
            pagina = st.radio(
                "Navegação",
                ["Registar TPCs", "Registar Testes"]
            )
        else:
            pagina = None

    # Conteúdo principal
    if not st.session_state.is_authenticated:
        pagina_login()
    elif not st.session_state.numero_verificado:
        pagina_verificacao_numero()
    else:
        if pagina == "Registar TPCs":
            pagina_registar_tpcs()
        elif pagina == "Registar Testes":
            pagina_registar_testes()
        else:
            st.write("Seleciona uma opção na barra lateral.")


if __name__ == "__main__":
    main()
