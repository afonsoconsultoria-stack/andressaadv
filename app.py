import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd

st.set_page_config(page_title="LexAI OAB - Direito Administrativo", layout="wide", initial_sidebar_state="expanded")

fundo_interativo = """
<script>
const parentDoc = window.parent.document;
if (!parentDoc.getElementById('bg-canvas-oab')) {
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
            radius: Math.random() * 2.5 + 1
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
            ctx.fillStyle = 'rgba(30, 58, 138, 0.35)';
            ctx.fill();

            for (let j = i + 1; j < particles.length; j++) {
                let p2 = particles[j];
                let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                if (dist < 130) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(30, 58, 138, ${0.18 - dist/750})`;
                    ctx.stroke();
                }
            }

            if (mouse.x && mouse.y) {
                let distMouse = Math.hypot(p.x - mouse.x, p.y - mouse.y);
                if (distMouse < 160) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(mouse.x, mouse.y);
                    ctx.strokeStyle = `rgba(217, 119, 6, ${0.4 - distMouse/400})`;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
}
</script>
"""
components.html(fundo_interativo, height=0, width=0)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
    }
    [data-testid="stAppViewContainer"] > .main {
        position: relative;
        z-index: 1;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(10px);
        z-index: 2;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border-left: 5px solid #1E3A8A;
    }
    .card-juridico {
        background-color: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(10px);
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid rgba(30, 58, 138, 0.15);
        margin-bottom: 18px;
    }
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #1e40af;
        color: white;
    }
    .gabarito-box {
        background-color: rgba(224, 242, 254, 0.92);
        padding: 18px;
        border-radius: 8px;
        border-left: 5px solid #0284C7;
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
        st.bar_chart(df_1fase.set_index("tema")["questoes"], color="#1E3A8A")
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
    
    st.markdown('<div class="card-juridico">', unsafe_allow_html=True)
    st.info(f"**Assunto:** {q_atual['tema']}")
    st.markdown(f"**Enunciado:**\n{q_atual['enunciado']}")
    
    alternativas_dict = q_atual["alternativas"]
    opcoes_radio = [
        f"A) {alternativas_dict['A']}",
        f"B) {alternativas_dict['B']}",
        f"C) {alternativas_dict['C']}",
        f"D) {alternativas_dict['D']}"
    ]
    
    resposta_usuario = st.radio("Marque sua resposta:", opcoes_radio, key=f"radio_{q_atual['id']}")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        validar = st.button("✅ Confirmar Resposta", key=f"btn_{q_atual['id']}")
    with col_btn2:
        marcar_dificuldade = st.button("🚩 Registrar Dificuldade neste Tema", key=f"dif_{q_atual['id']}")
        
    if marcar_dificuldade:
        if q_atual["tema"] not in st.session_state.temas_dificuldade:
            st.session_state.temas_dificuldade.append(q_atual["tema"])
        st.warning(f"Tema **{q_atual['tema']}** adicionado ao seu Plano de Revisão (Módulo 5)!")

    if validar:
        letra_marcada = resposta_usuario[0]
        
