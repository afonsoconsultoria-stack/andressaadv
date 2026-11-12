import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd

st.set_page_config(page_title="LexAI OAB - Direito Administrativo", layout="wide", initial_sidebar_state="expanded")

# FUNDO BLACK DINAMICO COM PARTICULAS SUTIS
fundo_dinamico = """
<script>
const parentDoc = window.parent.document;
const oldCanvas = parentDoc.getElementById('bg-canvas-oab');
if (oldCanvas) oldCanvas.remove();

const canvas = parentDoc.createElement('canvas');
canvas.id = 'bg-canvas-oab';
canvas.style.position = 'fixed';
canvas.style.top = '0';
canvas.style.left = '0';
canvas.style.width = '100vw';
canvas.style.height = '100vh';
canvas.style.zIndex = '0';
canvas.style.pointerEvents = 'none';
parentDoc.body.appendChild(canvas);

const ctx = canvas.getContext('2d');
let width = canvas.width = window.parent.innerWidth;
let height = canvas.height = window.parent.innerHeight;

window.parent.addEventListener('resize', () => {
    width = canvas.width = window.parent.innerWidth;
    height = canvas.height = window.parent.innerHeight;
});

const mouse = { x: null, y: null };
window.parent.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

const particles = [];
for (let i = 0; i < 60; i++) {
    particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.7,
        vy: (Math.random() - 0.5) * 0.7,
        radius: Math.random() * 2 + 1
    });
}

function animate() {
    ctx.clearRect(0, 0, width, height);
    for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(56, 189, 248, 0.5)';
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
            let p2 = particles[j];
            let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
            if (dist < 130) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = `rgba(56, 189, 248, ${0.2 - dist/650})`;
                ctx.stroke();
            }
        }

        if (mouse.x && mouse.y) {
            let distMouse = Math.hypot(p.x - mouse.x, p.y - mouse.y);
            if (distMouse < 160) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(mouse.x, mouse.y);
                ctx.strokeStyle = `rgba(250, 204, 21, ${0.45 - distMouse/360})`;
                ctx.stroke();
            }
        }
    }
    requestAnimationFrame(animate);
}
animate();
</script>
"""
components.html(fundo_dinamico, height=0, width=0)

# ESTILO BLACK COM ALTA LEGIBILIDADE PARA LEITURA E GRAFICOS
st.markdown("""
    <style>
    .stApp {
        background-color: #050505 !important;
    }
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
        position: relative;
        z-index: 2 !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(5, 5, 5, 0.8) !important;
        z-index: 3 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0c0c0e !important;
        border-right: 1px solid #27272a !important;
        z-index: 3 !important;
    }
    h1, h2 {
        color: #38bdf8 !important;
    }
    h3, h4, h5, h6 {
        color: #facc15 !important;
    }
    p, span, label, li, td, th, code, pre, .stMarkdown, [data-testid="stRadio"] label p, [data-testid="stCheckbox"] label p {
        color: #f4f4f5 !important;
    }
    strong, b {
        color: #38bdf8 !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #a1a1aa !important;
    }
    .quadro-destaque {
        background-color: #111115;
        border: 1px solid #27272a;
        border-left: 5px solid #38bdf8;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.7);
    }
    table, thead, tbody, tr, th, td {
        background-color: #111115 !important;
        border-color: #27272a !important;
        color: #f4f4f5 !important;
    }
    th {
        color: #facc15 !important;
        font-weight: bold !important;
    }
    button[data-baseweb="tab"] p {
        color: #a1a1aa !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #38bdf8 !important;
        font-weight: bold !important;
    }
    .stMetric {
        background-color: #111115 !important;
        padding: 18px !important;
        border-radius: 12px !important;
        border: 1px solid #27272a !important;
        border-left: 5px solid #38bdf8 !important;
    }
    [data-testid="stMetricValue"] div {
        color: #ffffff !important;
    }
    [data-testid="stMetricDelta"] div {
        color: #4ade80 !important;
    }
    div.stButton > button:first-child {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
        border: none !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #0369a1 !important;
        color: #ffffff !important;
    }
    .gabarito-box {
        background-color: #111115;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #27272a;
        border-left: 5px solid #4ade80;
        margin-top: 15px;
    }
    textarea, input, div[data-baseweb="select"] > div {
        background-color: #111115 !important;
        color: #f4f4f5 !important;
        border: 1px solid #3f3f46 !important;
    }
    ul[role="listbox"] li {
        background-color: #111115 !important;
        color: #f4f4f5 !important;
    }
    [data-testid="stAlert"] {
        background-color: #111115 !important;
        border: 1px solid #3f3f46 !important;
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

try:
    with open('dados_oab.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
except FileNotFoundError:
    st.error("Erro: Arquivo 'dados_oab.json' não encontrado no repositório.")
    st.stop()

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

# MODULO 1: PAINEL ESTATISTICO INTERATIVO
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

# MODULOS 2 e 3: SIMULADOR INTERATIVO
elif modulo == "📝 Módulos 2 e 3: Simulador Interativo":
    st.title("📝 Banco Inteligente de Questões (1ª Fase)")
    st.markdown("### Simulador Dinâmico de Direito Administrativo")
    
    questoes = db["questoes_simulado"]
    total_q = len(questoes)
    
    progresso = len(st.session_state.respondidas) / total_q
    st.progress(progresso)
    st.caption(f"Progresso do Simulado: **{len(st.session_state.respondidas)} de {total_q}** questões respondidas")
    
    temas_disponiveis = ["Todos os Temas"] + list(set([q["tema"] for q in questoes]))
    tema_escolhido = st.selectbox("Filtrar questões por assunto jurídico:", temas_disponiveis)
    
