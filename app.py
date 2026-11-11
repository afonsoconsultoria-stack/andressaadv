import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="LexAI OAB - Direito Administrativo", layout="wide", initial_sidebar_state="expanded")

# FUNDO PRETO DINAMICO EM CSS PURO + TEMA ESCURO COM LETRAS BRANCAS
st.markdown("""
    <style>
    :root {
        --primary-color: #38bdf8;
        --background-color: #07090f;
        --secondary-background-color: #111827;
        --text-color: #ffffff;
        --font: sans-serif;
    }

    @keyframes moverGrade {
        0% { background-position: 0px 0px, 0px 0px, 0% 50%; }
        50% { background-position: 40px 40px, 40px 40px, 100% 50%; }
        100% { background-position: 80px 80px, 80px 80px, 0% 50%; }
    }

    .stApp {
        background-color: #07090f !important;
        background-image: 
            radial-gradient(circle at 20% 25%, rgba(56, 189, 248, 0.14) 0%, transparent 45%),
            radial-gradient(circle at 80% 75%, rgba(250, 204, 21, 0.10) 0%, transparent 45%),
            linear-gradient(rgba(56, 189, 248, 0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.06) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px !important;
        animation: moverGrade 14s linear infinite !important;
        color: #ffffff !important;
    }

    [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: transparent !important;
        position: relative !important;
        z-index: 1 !important;
    }

    [data-testid="stHeader"] {
        background-color: rgba(7, 9, 15, 0.85) !important;
        z-index: 2 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0d1322 !important;
        border-right: 1px solid #1e293b !important;
        z-index: 2 !important;
    }

    /* Títulos e Textos em Branco e Destaques Claros */
    h1, h2 {
        color: #38bdf8 !important;
    }
    h3, h4, h5, h6 {
        color: #facc15 !important;
    }
    p, span, label, li, div, td, th, code, pre, .stMarkdown {
        color: #ffffff !important;
    }
    strong, b {
        color: #7dd3fc !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #cbd5e1 !important;
    }

    /* Quadros e Cartões */
    .quadro-destaque {
        background-color: rgba(17, 24, 39, 0.92);
        border: 1px solid #334155;
        border-left: 5px solid #38bdf8;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.65);
    }

    /* Tabelas */
    table, thead, tbody, tr, th, td {
        background-color: #111827 !important;
        border-color: #334155 !important;
        color: #ffffff !important;
    }
    th {
        color: #facc15 !important;
        font-weight: bold !important;
    }

    /* Abas */
    button[data-baseweb="tab"] p {
        color: #cbd5e1 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #38bdf8 !important;
        font-weight: bold !important;
    }

    /* Cards de Métricas */
    .stMetric {
        background-color: rgba(17, 24, 39, 0.92) !important;
        padding: 18px !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        border-left: 5px solid #38bdf8 !important;
    }
    [data-testid="stMetricValue"] div {
        color: #ffffff !important;
    }
    [data-testid="stMetricDelta"] div {
        color: #4ade80 !important;
    }

    /* Botões */
    div.stButton > button {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
        border: 1px solid #38bdf8 !important;
    }
    div.stButton > button:hover {
        background-color: #0369a1 !important;
        color: #ffffff !important;
    }

    /* Caixas de Seleção, Inputs e Alertas */
    textarea, input, div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
    }
    ul[role="listbox"], ul[role="listbox"] li {
        background-color: #111827 !important;
        color: #ffffff !important;
    }
    [data-testid="stAlert"] {
        background-color: #111827 !important;
        border: 1px solid #38bdf8 !important;
        color: #ffffff !important;
    }
    .gabarito-box {
        background-color: #0f172a;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #334155;
        border-left: 5px solid #4ade80;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

if "acertos" not in st.session_state:
    st.session_state.acertos = 0
if "erros" not in st.session_state:
    st.session_state.erros = 0
if "respondidas" not in st.session_state:
    st.session_state.respondidas = []
if "temas_dificuldade" not in st.session_state:
    st.session_state.temas_dificuldade = []

# Carregamento seguro do JSON
try:
    with open('dados_oab.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
except Exception as e:
    st.error(f"Erro ao carregar 'dados_oab.json': {e}")
    st.stop()

# MENU LATERAL
st.sidebar.title("⚖️ LexAI OAB")
st.sidebar.caption("Direito Administrativo | UNAMA")
st.sidebar.markdown("---")

modulo = st.sidebar.radio("Navegar pelos Módulos:", [
    "📊 Módulo 1: Estatísticas (2022–2026)",
    "📝 Módulos 2 e 3: Simulador Interativo",
    "🤖 Módulo 4: Corretor Inteligente",
    "📅 Módulo 5: Plano de Revisão"
])

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Desempenho Ao Vivo")
st.sidebar.write(f"✅ Acertos: **{st.session_state.acertos}**")
st.sidebar.write(f"❌ Erros: **{st.session_state.erros}**")

if st.sidebar.button("🔄 Zerar Progresso"):
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.respondidas = []
    st.session_state.temas_dificuldade = []
    st.rerun()

# ==========================================
# MODULO 1: PAINEL ESTATISTICO INTERATIVO
# ==========================================
if modulo == "📊 Módulo 1: Estatísticas (2022–2026)":
    st.title("📊 Análise Estatística OAB (2022–2026)")
    st.markdown("### Mapeamento Metodológico de Direito Administrativo")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Tema Líder (1ª Fase) 🔝", value="Agentes & Improbidade", delta="25,0% de incidência")
    col2.metric(label="Destaque Legislativo", value="Lei 14.133/21", delta="Tendência de Alta")
    col3.metric(label="Peça Campeã (2ª Fase)", value="Mandado de Segurança", delta="5 cobranças no período")

    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📈 Gráficos Interativos (1ª Fase)", "📋 Tabela Detalhada (1ª Fase)", "🏛️ Peças Processuais (2ª Fase)"])
    df_1fase = pd.DataFrame(db["estatisticas_1a_fase"])
    
    with tab1:
        col_g1, col_g2 = st.columns(2)
        col_g1.subheader("Quantidade de Questões por Tema")
        col_g1.bar_chart(df_1fase.set_index("tema")["questoes"], color="#38bdf8")
        col_g1.caption("Número absoluto de questões auditadas (2022–2026).")
        
        col_g2.subheader("Percentual de Incidência (%)")
        col_g2.bar_chart(df_1fase.set_index("tema")["porcentagem"], color="#facc15")
        col_g2.caption("Peso proporcional de cada tema na prova objetiva.")
        
    with tab2:
        st.subheader("Dados Auditados da Prova Objetiva")
        filtro_tendencia = st.multiselect("Filtrar por tendência de cobrança:", options=["Alta", "Estável", "Queda"], default=["Alta", "Estável", "Queda"])
        df_filtrado = df_1fase[df_1fase["tendencia"].isin(filtro_tendencia)]
        st.table(df_filtrado)
        
    with tab3:
        st.subheader("Mapeamento de Peças Prático-Profissionais")
        df_2fase = pd.DataFrame(db["pecas_recorrentes_2a_fase"])
        st.table(df_2fase)

# ==========================================
# MODULOS 2 e 3: SIMULADOR INTERATIVO
# ==========================================
elif modulo == "📝 Módulos 2 e 3: Simulador Interativo":
    st.title("📝 Banco Inteligente de Questões (1ª Fase)")
    st.markdown("### Simulador Dinâmico de Direito Administrativo")
    
    questoes = db["questoes_simulado"]
    total_q = len(questoes)
    
    progresso = len(st.session_state.respondidas) / total_q if total_q > 0 else 0
    st.progress(progresso)
    st.caption(f"Progresso do Simulado: **{len(st.session_state.respondidas)} de {total_q}** questões respondidas")
    
    temas_disponiveis = ["Todos os Temas"] + list(set([q["tema"] for q in questoes]))
    tema_escolhido = st.selectbox("Filtrar questões por assunto jurídico:", temas_disponiveis)
    
    questoes_filtradas = questoes if tema_escolhido == "Todos os Temas" else [q for q in questoes if q["tema"] == tema_escolhido]
    
    lista_titulos = [f"Questão {q['id']} - {q['tema']}" for q in questoes_filtradas]
    escolha_q = st.selectbox("Selecione a questão:", lista_titulos)
    
    idx = lista_titulos.index(escolha_q)
    q_atual = questoes_filtradas[idx]
    
    st.markdown("---")
    st.markdown(f"""
    <div class="quadro-destaque">
        <h4>📌 Tema: {q_atual['tema']}</h4>
        <p><strong>Enunciado:</strong> {q_atual['enunciado']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    alternativas_dict = q_atual["alternativas"]
    opcoes_radio = [
        f"A) {alternativas_dict['A']}",
        f"B) {alternativas_dict['B']}",
        f"C) {alternativas_dict['C']}",
        f"D) {alternativas_dict['D']}"
    ]
    
    resposta_usuario = st.radio("Marque sua resposta:", opcoes_radio, key=f"radio_{q_atual['id']}")
    
    col_btn1, col_btn2 = st.columns(2)
    validar = col_btn1.button("✅ Confirmar Resposta", key=f"btn_{q_atual['id']}")
    marcar_dificuldade = col_btn2.button("🚩 Registrar Dificuldade neste Tema", key=f"dif_{q_atual['id']}")
        
    if marcar_dificuldade:
