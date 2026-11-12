import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="LexAI OAB - Direito Administrativo",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILO DARK DINAMICO DE ALTA LEGIBILIDADE (VISUAL LAW & LEGAL DESIGN)
st.markdown("""
<style>
@keyframes gradienteDinamico {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stApp {
    background: linear-gradient(-45deg, #04060b, #0a1324, #07101e, #030508) !important;
    background-size: 400% 400% !important;
    animation: gradienteDinamico 14s ease infinite !important;
}
[data-testid="stSidebar"] {
    background-color: #080d19 !important;
    border-right: 1px solid #1e293b !important;
}
h1, h2 { color: #38bdf8 !important; }
h3, h4 { color: #facc15 !important; }
.card-visual {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-left: 5px solid #38bdf8;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 16px;
}
.card-visual h4 { color: #facc15 !important; margin: 0 0 8px 0; }
.card-visual p { color: #f8fafc !important; margin: 4px 0; font-size: 15px; }
.gabarito-visual {
    background-color: #091e16;
    border: 1px solid #15803d;
    border-left: 5px solid #4ade80;
    border-radius: 8px;
    padding: 16px;
    margin-top: 14px;
}
.gabarito-visual h5 { color: #4ade80 !important; margin: 0 0 6px 0; }
.gabarito-visual p { color: #ecfdf5 !important; margin: 0; }
</style>
""", unsafe_allow_html=True)

# MEMORIA INTERATIVA DA SESSAO
if "acertos" not in st.session_state:
    st.session_state.acertos = 0
if "erros" not in st.session_state:
    st.session_state.erros = 0
if "respondidas" not in st.session_state:
    st.session_state.respondidas = []
if "temas_dificuldade" not in st.session_state:
    st.session_state.temas_dificuldade = []

# CARREGAMENTO DOS DADOS AUDITADOS (2022-2026)
try:
    with open("dados_oab.json", "r", encoding="utf-8") as f:
        db = json.load(f)
except Exception as e:
    st.error(f"Erro ao carregar dados_oab.json: {e}")
    st.stop()

# MENU LATERAL (OS 5 MODULOS DO EDITAL - PAGINA 8)
st.sidebar.title("⚖️ LexAI OAB")
st.sidebar.caption("Direito Administrativo | UNAMA")
st.sidebar.markdown("---")

modulo = st.sidebar.radio("Selecione o Módulo:", [
    "📊 Módulo 1: Estatísticas (2022–2026)",
    "📝 Módulo 2: Banco de Questões (1ª Fase)",
    "✍️ Módulo 3: Questões Discursivas (2ª Fase)",
    "🤖 Módulo 4: Corretor Inteligente com IA",
    "📅 Módulo 5: Plano de Estudos Personalizado"
])

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Painel de Desempenho")
st.sidebar.write(f"✅ Acertos: **{st.session_state.acertos}**")
st.sidebar.write(f"❌ Erros: **{st.session_state.erros}**")

if st.sidebar.button("🔄 Reiniciar Simulado"):
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.respondidas = []
    st.session_state.temas_dificuldade = []
    st.rerun()

# MODULO 1: ESTATISTICAS DA OAB 2022-2026
if modulo == "📊 Módulo 1: Estatísticas (2022–2026)":
    st.title("📊 Análise Estatística OAB (2022–2026)")
    st.markdown("### Mapeamento Auditado até o 47º Exame de Ordem Unificado")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Tema Líder (1ª Fase)", "Agentes & Improbidade", "25,0% de incidência")
    c2.metric("Destaque Legislativo", "Lei 14.133/21", "21,4% (Tendência Alta)")
    c3.metric("Peça Campeã (2ª Fase)", "Mandado de Segurança", "5 cobranças no período")
    
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📈 Gráficos Dinâmicos (1ª Fase)", "📋 Ranking Completo (1ª Fase)", "🏛️ Peças Processuais (2ª Fase)"])
    df_1fase = pd.DataFrame(db["estatisticas_1a_fase"])
    
    with tab1:
        g1, g2 = st.columns(2)
        g1.subheader("Questões Cobradas por Tema")
        g1.bar_chart(df_1fase.set_index("tema")["questoes"], color="#38bdf8")
        g2.subheader("Percentual de Incidência (%)")
        g2.bar_chart(df_1fase.set_index("tema")["porcentagem"], color="#facc15")
        
    with tab2:
        st.subheader("Tabela Quantitativa da Prova Objetiva")
        filtro = st.multiselect("Filtrar por tendência:", options=["Alta", "Estável", "Queda"], default=["Alta", "Estável", "Queda"])
        st.dataframe(df_1fase[df_1fase["tendencia"].isin(filtro)], use_container_width=True)
        
    with tab3:
        st.subheader("Levantamento Histórico de Peças (2ª Fase)")
        st.dataframe(pd.DataFrame(db["pecas_recorrentes_2a_fase"]), use_container_width=True)

# MODULO 2: BANCO DE QUESTOES OBJETIVAS COM GABARITOS
elif modulo == "📝 Módulo 2: Banco de Questões (1ª Fase)":
    st.title("📝 Banco Inteligente de Questões (1ª Fase)")
    st.markdown("### Simulado Interativo com 10 Questões Reais dos Temas Recorrentes")
    
    questoes = db["questoes_simulado"]
    total_q = len(questoes)
    progresso = len(st.session_state.respondidas) / total_q if total_q > 0 else 0
    st.progress(progresso)
    st.write(f"Progresso: **{len(st.session_state.respondidas)} de {total_q}** questões respondidas")
    
    temas = ["Todos os Temas"] + sorted(list(set([q["tema"] for q in questoes])))
    tema_sel = st.selectbox("Filtrar questões por assunto jurídico:", temas)
    filtradas = questoes if tema_sel == "Todos os Temas" else [q for q in questoes if q["tema"] == tema_sel]
    
    titulos = [f"Questão {q['id']} — {q['tema']}" for q in filtradas]
    escolha = st.selectbox("Selecione a questão:", titulos)
    q_atual = filtradas[titulos.index(escolha)]
    
    st.markdown(f'<div class="card-visual"><h4>📌 Assunto: {q_atual["tema"]}</h4><p><strong>Enunciado:</strong> {q_atual["enunciado"]}</p></div>', unsafe_allow_html=True)
    
    alt = q_atual["alternativas"]
    opcoes = [f"A) {alt['A']}", f"B) {alt['B']}", f"C) {alt['C']}", f"D) {alt['D']}"]
    resp = st.radio("Escolha sua alternativa:", opcoes, key=f"rad_{q_atual['id']}")
    
    b1, b2 = st.columns(2)
    btn_validar = b1.button("✅ Validar Resposta", key=f"val_{q_atual['id']}")
    btn_dif = b2.button("🚩 Registrar Dificuldade neste Tema", key=f"dif_{q_atual['id']}")
    
    if btn_dif:
        if q_atual["tema"] not in st.session_state.temas_dificuldade:
            st.session_state.temas_dificuldade.append(q_atual["tema"])
        st.warning(f"Dificuldade em **{q_atual['tema']}** registrada no Módulo 5!")
        
    if btn_validar:
        letra = resp.split(")").strip()
        if q_atual["id"] not in st.session_state.respondidas:
            st.session_state.respondidas.append(q_atual["id"])
            if letra == q_atual["correta"]:
                st.session_state.acertos += 1
            else:
                st.session_state.erros += 1
                if q_atual["tema"] not in st.session_state.temas_dificuldade:
                    st.session_state.temas_dificuldade.append(q_atual["tema"])
                    
        if letra == q_atual["correta"]:
            st.success("🟢 **Resposta CORRETA!** Pontuação somada ao placar.")
        else:
            st.error(f"🔴 **Resposta INCORRETA.** O gabarito oficial FGV é a letra **{q_atual['correta']}**.")
            
        st.markdown(f'<div class="gabarito-visual"><h5>💡 Gabarito Comentado e Fundamentação Legal</h5><p>{q_atual["gabarito_comentado"]}</p></div>', unsafe_allow_html=True)

# MODULO 3: QUESTOES DISCURSIVAS POR ASSUNTO (2a FASE)
elif modulo == "✍️ Módulo 3: Questões Discursivas (2ª Fase)":
    st.title("✍️ Banco de Peças e Questões Discursivas (2ª Fase)")
    st.markdown("### Estudo Dirigido com Padrões de Resposta e Espelhos Oficiais")
    
    discursivas = db.get("questoes_discursivas", [])
    titulos_disc = [f"Caso {d['id']} — {d['tema']}" for d in discursivas]
    escolha_d = st.selectbox("Selecione a peça ou questão discursiva:", titulos_disc)
    d_atual = discursivas[titulos_disc.index(escolha_d)]
    
    st.markdown(f'<div class="card-visual"><h4>⚖️ {d_atual["tema"]}</h4><p><strong>Proposta Oficial:</strong> {d_atual["enunciado"]}</p></div>', unsafe_allow_html=True)
    
    if st.checkbox("👁️ Exibir Espelho Oficial de Correção FGV", key=f"esp_{d_atual['id']}"):
        st.code(d_atual["espelho"], language="text")

# MODULO 4: CORRETOR INTELIGENTE COM PROMPT E ESPELHOS OFICIAIS
elif modulo == "🤖 Módulo 4: Corretor Inteligente com IA":
    st.title("🤖 Corretor Pedagógico Inteligente (2ª Fase)")
    st.markdown("### Avaliação Estruturada nos 5 Passos do Prompt de Correção")
    
    discursivas = db.get("questoes_discursivas", [])
    titulos_disc = [f"Caso {d['id']} — {d['tema']}" for d in discursivas]
    escolha_c = st.selectbox("Escolha o caso prático para treinar:", titulos_disc)
    c_atual = discursivas[titulos_disc.index(escolha_c)]
    
    st.markdown(f'<div class="card-visual"><h4>📄 Enunciado para Resposta</h4><p>{c_atual["enunciado"]}</p></div>', unsafe_allow_html=True)
    
    with st.expander("🔍 Ver Prompt Pedagógico Aplicado (Etapa 3 do Edital)"):
        st.code("1. Identificar o assunto jurídico da questão\n2. Analisar e comparar a resposta com o padrão oficial\n3. Verificar fundamentos legais e processuais exigidos\n4. Identificar acertos, erros, omissões e argumentos incompletos\n5. Atribuir pontuação simulada e sugerir melhorias e revisões", language="text")
    
    texto_aluno = st.text_area("✍️ Redija sua resposta jurídica abaixo:", height=180, placeholder="Digite aqui a fundamentação jurídica, artigos da Constituição/Leis e os pedidos cabíveis...")
    
    if st.button("🚀 Submeter Resposta para Correção"):
        if len(texto_aluno.strip()) < 15:
