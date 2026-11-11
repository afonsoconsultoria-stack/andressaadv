import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd

st.set_page_config(page_title="LexAI OAB - Direito Administrativo", layout="wide", initial_sidebar_state="expanded")

# 🌌 FUNDO INTERATIVO ESCURO COM PARTÍCULAS VERDE CLARO E VERMELHAS
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
for (let i = 0; i < 70; i++) {
    particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.9,
        vy: (Math.random() - 0.5) * 0.9,
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
        ctx.fillStyle = p.isGreen ? 'rgba(74, 222, 128, 0.65)' : 'rgba(248, 113, 113, 0.65)';
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
            let p2 = particles[j];
            let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
            if (dist < 135) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = p.isGreen 
                    ? `rgba(74, 222, 128, ${0.25 - dist/550})` 
                    : `rgba(248, 113, 113, ${0.25 - dist/550})`;
                ctx.stroke();
            }
        }

        if (mouse.x && mouse.y) {
            let distMouse = Math.hypot(p.x - mouse.x, p.y - mouse.y);
            if (distMouse < 170) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(mouse.x, mouse.y);
                ctx.strokeStyle = p.isGreen 
                    ? `rgba(74, 222, 128, ${0.55 - distMouse/320})` 
                    : `rgba(248, 113, 113, ${0.55 - distMouse/320})`;
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

# 🎨 TEMA ESCURO COM 100% DOS TEXTOS EM VERDE CLARO E VERMELHO
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #05080f 0%, #0b1324 100%);
    }
    [data-testid="stAppViewContainer"] > .main {
        position: relative;
        z-index: 1;
    }
    [data-testid="stHeader"] {
        background-color: rgba(5, 8, 15, 0.6);
    }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 28, 0.92);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(74, 222, 128, 0.3);
        z-index: 2;
    }
    /* Títulos em Verde Claro e Subtítulos em Vermelho Claro */
    h1, h2 {
        color: #4ade80 !important;
        text-shadow: 0 0 12px rgba(74, 222, 128, 0.25);
    }
    h3, h4, h5, h6 {
        color: #f87171 !important;
    }
    /* Todos os demais textos, listas, opções e células de tabela em Verde Claro */
    p, span, label, li, div, td, th, code, pre, .stMarkdown, [data-testid="stRadio"] label, [data-testid="stCheckbox"] label {
        color: #86efac !important;
    }
    /* Destaques em negrito e legendas em Vermelho Claro para contraste */
    strong, b, .stCaption, [data-testid="stCaptionContainer"] p {
        color: #f87171 !important;
    }
    /* Tabelas escuras */
    table, thead, tbody, tr, th, td {
        background-color: rgba(13, 20, 36, 0.92) !important;
        border-color: rgba(74, 222, 128, 0.3) !important;
    }
    th {
        color: #f87171 !important;
        font-weight: bold !important;
    }
    /* Abas (Tabs) */
    button[data-baseweb="tab"] p {
        color: #86efac !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #f87171 !important;
        font-weight: bold !important;
    }
    /* Métricas */
    .stMetric {
        background-color: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(8px);
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        border-left: 5px solid #4ade80;
        border-top: 1px solid rgba(248, 113, 113, 0.25);
    }
    [data-testid="stMetricValue"] div {
        color: #4ade80 !important;
    }
    [data-testid="stMetricDelta"] div {
        color: #f87171 !important;
    }
    /* Cartões translúcidos */
    .card-juridico {
        background-color: rgba(13, 20, 36, 0.88);
        backdrop-filter: blur(10px);
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(74, 222, 128, 0.35);
        margin-bottom: 18px;
    }
    /* Botões */
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
    /* Caixa de Gabarito */
    .gabarito-box {
        background-color: rgba(15, 23, 42, 0.95);
        padding: 18px;
        border-radius: 8px;
        border-left: 5px solid #f87171;
        border-top: 1px solid rgba(74, 222, 128, 0.3);
        margin-top: 15px;
    }
    /* Inputs e Selectboxes */
    textarea, input, div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        color: #86efac !important;
        border: 1px solid #4ade80 !important;
    }
    ul[role="listbox"] li {
        background-color: #0f172a !important;
        color: #86efac !important;
    }
    /* Alertas (st.info, st.warning, st.success, st.error) */
    [data-testid="stAlert"] {
        background-color: rgba(15, 23, 42, 0.92) !important;
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

if modulo == "📊 Módulo 1: Estatísticas (2022–2026)":
    st.title("📊 Análise Estatística OAB (2022–2026)")
    st.markdown("### Mapeamento Metodológico de Direito Administrativo")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Tema Líder (1ª Fase) 🔝", value="Agentes & Improbidade", delta="25,0% de incidência")
    with col2:
        st.metric(label="Destaque Legislativo", value="Lei 14.133/21", delta="Tendência de Alta")
    with col3:
        st.metric(label="Peça Campeã (2ª Fase)", value="Mandado de Segurança", delta="5 cobranças no período")

    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📈 Gráficos Interativos (1ª Fase)", "📋 Tabela Detalhada (1ª Fase)", "🏛️ Peças Processuais (2ª Fase)"])
    df_1fase = pd.DataFrame(db["estatisticas_1a_fase"])
    
    with tab1:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown('<div class="card-juridico">', unsafe_allow_html=True)
            st.subheader("Quantidade de Questões por Tema")
            st.bar_chart(df_1fase.set_index("tema")["questoes"], color="#4ade80")
            st.caption("Número absoluto de questões auditadas (2022–2026).")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_g2:
            st.markdown('<div class="card-juridico">', unsafe_allow_html=True)
            st.subheader("Percentual de Incidência (%)")
            st.bar_chart(df_1fase.set_index("tema")["porcentagem"], color="#f87171")
            st.caption("Peso proporcional de cada tema na prova objetiva.")
            st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
