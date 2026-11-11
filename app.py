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

# 🎨 TEMA ESCURO COM LETRAS VERDE CLARAS E VERMELHAS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #05080f 0%, #0b1324 100%);
        color: #86efac;
    }
    [data-testid="stAppViewContainer"] > .main {
        position: relative;
        z-index: 1;
    }
    [data-testid="stHeader"] {
        background-color: rgba(5, 8, 15, 0.6);
    }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 28, 0.90);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(74, 222, 128, 0.25);
        z-index: 2;
    }
    h1, h2 {
        color: #4ade80 !important;
        text-shadow: 0 0 12px rgba(74, 222, 128, 0.25);
    }
    h3, h4, h5 {
        color: #f87171 !important;
    }
    p, label, span, li, .stMarkdown {
        color: #86efac !important;
    }
    .stCaption {
        color: #fca5a5 !important;
    }
    .stMetric {
        background-color: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(8px);
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        border-left: 5px solid #4ade80;
        border-top: 1px solid rgba(248, 113, 113, 0.25);
    }
    [data-testid="stMetricValue"] {
        color: #4ade80 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #f87171 !important;
    }
    .card-juridico {
        background-color: rgba(13, 20, 36, 0.88);
        backdrop-filter: blur(10px);
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(74, 222, 128, 0.3);
        margin-bottom: 18px;
    }
    div.stButton > button:first-child {
        background-color: #14532d;
        color: #86efac !important;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
        border: 1px solid #4ade80;
    }
    div.stButton > button:first-child:hover {
        background-color: #7f1d1d;
        color: #fca5a5 !important;
        border: 1px solid #f87171;
    }
    .gabarito-box {
        background-color: rgba(15, 23, 42, 0.95);
        padding: 18px;
        border-radius: 8px;
        border-left: 5px solid #f87171;
        border-top: 1px solid rgba(74, 222, 128, 0.3);
        margin-top: 15px;
    }
    textarea, input, select {
        background-color: #0f172a !important;
        color: #86efac !important;
        border: 1px solid #4ade80 !important;
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
    
    tab1, tab2, tab3 = st.tabs(["📈 Gráfico Interativo (1ª Fase)", "📋 Tabela Detalhada (1ª Fase)", "🏛️ Peças Processuais (2ª Fase)"])
    df_1fase = pd.DataFrame(db["estatisticas_1a_fase"])
    
    with tab1:
        st.markdown('<div class="card-juridico">', unsafe_allow_html=True)
        st.subheader("Incidência de Questões por Tema Jurídico")
        st.bar_chart(df_1fase.set_index("tema")["questoes"], color="#4ade80")
        st.caption("Passe o cursor sobre as barras para visualizar o número exato de questões cobradas entre 2022 e 2026.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown('<div class="card-juridico">', unsafe_allow_html=True)
        st.subheader("Dados Auditados da Prova Objetiva")
        filtro_tendencia = st.multiselect("Filtrar por tendência de cobrança:", options=["Alta", "Estável", "Queda"], default=["Alta", "Estável", "Queda"])
        df_filtrado = df_1fase[df_1fase["tendencia"].isin(filtro_tendencia)]
        st.dataframe(df_filtrado, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab3:
        st.markdown('<div class="card-juridico">', unsafe_allow_html=True)
        st.subheader("Mapeamento de Peças Prático-Profissionais")
        df_2fase = pd.DataFrame(db["pecas_recorrentes_2a_fase"])
        st.table(df_2fase)
        st.markdown('</div>', unsafe_allow_html=True)

elif modulo == "📝 Módulos 2 e 3: Simulador Interativo":
    st.title("📝 Banco Inteligente de Questões (1ª Fase)")
    
    questoes = db["questoes_simulado"]
    total_q = len(questoes)
    
    progresso = len(st.session_state.respondidas) / total_q
    st.progress(progresso)
    st.caption(f"Progresso do Simulado: **{len(st.session_state.respondidas)} de {total_q}** questões respondidas")
    
    temas_disponiveis = ["Todos os Temas"] + list(set([q["tema"] for q in questoes]))
    tema_escolhido = st.selectbox("Filtrar questões por assunto jurídico:", temas_disponiveis)
    
    questoes_filtradas = questoes if tema_escolhido == "Todos os Temas" else [q for q in questoes if q["tema"] == tema_escolhido]
    
    lista_titulos = [f"Questão {q['id']} - {q['tema']}" for q in questoes_filtradas]
    escolha_q = st.selectbox("Selecione a questão:", lista_titulos)
    
    idx = lista_titulos.index(escolha_q)
    q_atual = questoes_filtradas[idx]
    
