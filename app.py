import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd

st.set_page_config(page_title="LexAI OAB - Direito Administrativo", layout="wide", initial_sidebar_state="expanded")

# FUNDO INTERATIVO ESCURO COM PARTICULAS VERDE CLARO E VERMELHAS
fundo_interativo = """
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
for (let i = 0; i < 65; i++) {
    particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.8,
        vy: (Math.random() - 0.5) * 0.8,
        radius: Math.random() * 2.5 + 1.2,
        isGreen: i % 2 === 0
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
        ctx.fillStyle = p.isGreen ? 'rgba(74, 222, 128, 0.55)' : 'rgba(248, 113, 113, 0.55)';
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
            let p2 = particles[j];
            let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
            if (dist < 130) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = p.isGreen 
                    ? `rgba(74, 222, 128, ${0.22 - dist/600})` 
                    : `rgba(248, 113, 113, ${0.22 - dist/600})`;
                ctx.stroke();
            }
        }

        if (mouse.x && mouse.y) {
            let distMouse = Math.hypot(p.x - mouse.x, p.y - mouse.y);
            if (distMouse < 160) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(mouse.x, mouse.y);
                ctx.strokeStyle = p.isGreen 
                    ? `rgba(74, 222, 128, ${0.5 - distMouse/350})` 
                    : `rgba(248, 113, 113, ${0.5 - distMouse/350})`;
                ctx.stroke();
            }
        }
    }
    requestAnimationFrame(animate);
}
animate();
</script>
"""
components.html(fundo_interativo, height=0, width=0)

# ESTILO VISUAL ESCURO COM TEXTOS EM VERDE CLARO E VERMELHO
st.markdown("""
    <style>
    .stApp {
        background-color: #060a12 !important;
    }
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
        position: relative;
        z-index: 2 !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(6, 10, 18, 0.7) !important;
        z-index: 3 !important;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 16, 30, 0.94) !important;
        border-right: 1px solid rgba(74, 222, 128, 0.35) !important;
        z-index: 3 !important;
    }
    h1, h2 {
        color: #4ade80 !important;
    }
    h3, h4, h5, h6 {
        color: #f87171 !important;
    }
    p, span, label, li, td, th, code, pre, .stMarkdown, [data-testid="stRadio"] label p, [data-testid="stCheckbox"] label p {
        color: #86efac !important;
    }
    strong, b, .stCaption, [data-testid="stCaptionContainer"] p {
        color: #f87171 !important;
    }
    .quadro-destaque {
        background-color: rgba(13, 21, 38, 0.92);
        border: 1px solid #4ade80;
        border-left: 6px solid #f87171;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
    }
    table, thead, tbody, tr, th, td {
        background-color: rgba(13, 21, 38, 0.95) !important;
        border-color: rgba(74, 222, 128, 0.35) !important;
    }
    th {
        color: #f87171 !important;
    }
    button[data-baseweb="tab"] p {
        color: #86efac !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #f87171 !important;
        font-weight: bold !important;
    }
    .stMetric {
        background-color: rgba(15, 23, 42, 0.9) !important;
        padding: 18px !important;
        border-radius: 12px !important;
        border-left: 5px solid #4ade80 !important;
        border-top: 1px solid rgba(248, 113, 113, 0.3) !important;
    }
    [data-testid="stMetricValue"] div {
        color: #4ade80 !important;
    }
    [data-testid="stMetricDelta"] div {
        color: #f87171 !important;
    }
    div.stButton > button:first-child {
        background-color: #14532d !important;
        color: #86efac !important;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
        border: 1px solid #4ade80 !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #7f1d1d !important;
        color: #fca5a5 !important;
        border: 1px solid #f87171 !important;
    }
    textarea, input, div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        color: #86efac !important;
        border: 1px solid #4ade80 !important;
    }
    ul[role="listbox"] li {
        background-color: #0f172a !important;
        color: #86efac !important;
    }
    [data-testid="stAlert"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border: 1px solid #f87171 !important;
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
        col_g1.bar_chart(df_1fase.set_index("tema")["questoes"], color="#4ade80")
        col_g1.caption("Número absoluto de questões auditadas (2022–2026).")
        
        col_g2.subheader("Percentual de Incidência (%)")
        col_g2.bar_chart(df_1fase.set_index("tema")["porcentagem"], color="#f87171")
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
