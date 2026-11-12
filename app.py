import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="LexAI OAB - Direito Administrativo",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@keyframes pulsoFundo {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stApp {
    background: linear-gradient(-45deg, #05070a, #0a1120, #070d17, #040609) !important;
    background-size: 400% 400% !important;
    animation: pulsoFundo 15s ease infinite !important;
}
[data-testid="stSidebar"] {
    background-color: #090e1a !important;
    border-right: 1px solid #1e293b !important;
}
h1, h2 { color: #38bdf8 !important; }
h3, h4 { color: #facc15 !important; }
.quadro-oab {
    background-color: #111827;
    border: 1px solid #334155;
    border-left: 5px solid #38bdf8;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 16px;
    color: #f8fafc;
}
.quadro-oab p { color: #f8fafc !important; margin: 4px 0; }
.quadro-oab h4 { color: #facc15 !important; margin: 4px 0; }
.gabarito-oab {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-left: 5px solid #4ade80;
    border-radius: 8px;
    padding: 16px;
    margin-top: 14px;
    color: #f8fafc;
}
.gabarito-oab h5 { color: #4ade80 !important; margin: 0 0 8px 0; }
.gabarito-oab p { color: #e2e8f0 !important; margin: 0; }
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
    with open("dados_oab.json", "r", encoding="utf-8") as f:
        db = json.load(f)
except Exception as e:
    st.error(f"Erro ao ler dados_oab.json: {e}")
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
    c1, c2, c3 = st.columns(3)
    c1.metric("Tema Líder (1ª Fase)", "Agentes & Improbidade", "25,0% de incidência")
    c2.metric("Destaque Legislativo", "Lei 14.133/21", "Tendência de Alta")
    c3.metric("Peça Campeã (2ª Fase)", "Mandado de Segurança", "5 cobranças no período")
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📈 Gráficos Interativos (1ª Fase)", "📋 Tabela Detalhada (1ª Fase)", "🏛️ Peças Processuais (2ª Fase)"])
    df_1fase = pd.DataFrame(db["estatisticas_1a_fase"])
    with tab1:
        g1, g2 = st.columns(2)
        g1.subheader("Quantidade de Questões por Tema")
        g1.bar_chart(df_1fase.set_index("tema")["questoes"], color="#38bdf8")
        g2.subheader("Percentual de Incidência (%)")
        g2.bar_chart(df_1fase.set_index("tema")["porcentagem"], color="#facc15")
    with tab2:
        st.subheader("Dados Auditados da Prova Objetiva")
        filtro = st.multiselect("Filtrar por tendência:", options=["Alta", "Estável", "Queda"], default=["Alta", "Estável", "Queda"])
        st.dataframe(df_1fase[df_1fase["tendencia"].isin(filtro)], use_container_width=True)
    with tab3:
        st.subheader("Mapeamento de Peças Prático-Profissionais")
        st.dataframe(pd.DataFrame(db["pecas_recorrentes_2a_fase"]), use_container_width=True)

elif modulo == "📝 Módulos 2 e 3: Simulador Interativo":
    st.title("📝 Banco Inteligente de Questões (1ª Fase)")
    st.markdown("### Simulador Dinâmico de Direito Administrativo")
    questoes = db["questoes_simulado"]
    total_q = len(questoes)
    progresso = len(st.session_state.respondidas) / total_q if total_q > 0 else 0
    st.progress(progresso)
    st.write(f"Progresso do Simulado: **{len(st.session_state.respondidas)} de {total_q}** questões respondidas")
    temas = ["Todos os Temas"] + list(set([q["tema"] for q in questoes]))
    tema_sel = st.selectbox("Filtrar por assunto jurídico:", temas)
    filtradas = questoes if tema_sel == "Todos os Temas" else [q for q in questoes if q["tema"] == tema_sel]
    titulos = [f"Questão {q['id']} - {q['tema']}" for q in filtradas]
    escolha = st.selectbox("Selecione a questão:", titulos)
    q_atual = filtradas[titulos.index(escolha)]
    st.markdown(f'<div class="quadro-oab"><h4>📌 Tema: {q_atual["tema"]}</h4><p><strong>Enunciado:</strong> {q_atual["enunciado"]}</p></div>', unsafe_allow_html=True)
    alt = q_atual["alternativas"]
    opcoes = [f"A) {alt['A']}", f"B) {alt['B']}", f"C) {alt['C']}", f"D) {alt['D']}"]
    resp = st.radio("Marque sua resposta:", opcoes, key=f"rad_{q_atual['id']}")
    b1, b2 = st.columns(2)
    btn_validar = b1.button("✅ Confirmar Resposta", key=f"val_{q_atual['id']}")
    btn_dif = b2.button("🚩 Registrar Dificuldade neste Tema", key=f"dif_{q_atual['id']}")
    if btn_dif:
        if q_atual["tema"] not in st.session_state.temas_dificuldade:
            st.session_state.temas_dificuldade.append(q_atual["tema"])
        st.warning(f"Tema **{q_atual['tema']}** adicionado ao Plano de Revisão (Módulo 5)!")
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
            st.success("🟢 **Resposta CORRETA!** Pontuação contabilizada no painel lateral.")
        else:
            st.error(f"🔴 **Resposta INCORRETA.** A alternativa correta da FGV é a Letra **{q_atual['correta']}**.")
        st.markdown(f'<div class="gabarito-oab"><h5>💡 Fundamentação Legal e Gabarito Oficial</h5><p>{q_atual["gabarito_comentado"]}</p></div>', unsafe_allow_html=True)

elif modulo == "🤖 Módulo 4: Corretor Inteligente":
    st.title("🤖 Corretor Pedagógico de Peças (2ª Fase)")
    st.markdown("### Avaliação Automatizada Baseada no Espelho Oficial FGV")
    st.markdown('<div class="quadro-oab"><h4>📄 Caso Prático Proposto: Mandado de Segurança</h4><p><strong>Situação:</strong> Candidato aprovado dentro das vagas em concurso público estadual foi ilegalmente eliminado na fase documental por ato do Secretário de Administração. Redija os tópicos principais do <strong>Mandado de Segurança</strong> cabível.</p></div>', unsafe_allow_html=True)
    st.subheader("📋 Critérios do Espelho Oficial (5,00 Pontos)")
    st.code("1. Endereçamento ao Juízo da Vara da Fazenda Pública Estadual (1,00 pt)\n2. Fundamentação legal: Art. 5º, LXIX da CF e Lei 12.016/09 (1,00 pt)\n3. Demonstração do Direito Líquido e Certo violado (1,00 pt)\n4. Pedido de Medida Liminar: Fumus Boni Iuris e Periculum in Mora (1,50 pt)\n5. Pedido de notificação da Autoridade Coatora e intimação do MP (0,50 pt)", language="text")
    texto_aluno = st.text_area("✍️ Escreva ou cole sua resposta jurídica abaixo para correção em tempo real:", height=180, placeholder="Ex: Excelentíssimo Senhor Doutor Juiz de Direito da Vara da Fazenda Pública... Com fundamento na Lei 12.016/09, vem impetrar Mandado de Segurança com pedido de liminar...")
    if st.button("🚀 Executar Correção Inteligente"):
        if len(texto_aluno.strip()) < 15:
            st.warning("Por favor, digite uma resposta mais completa para avaliação.")
        else:
            t = texto_aluno.lower()
            c1 = any(p in t for p in ["fazenda pública", "fazenda publica", "juiz de direito"])
            c2 = any(p in t for p in ["12.016", "lxix", "5º", "mandado de segurança"])
            c3 = any(p in t for p in ["líquido e certo", "liquido e certo", "ilegal", "direito"])
            c4 = any(p in t for p in ["liminar", "fumus", "periculum", "urgência", "urgencia"])
            c5 = any(p in t for p in ["notificação", "notificacao", "autoridade coatora", "ministério público", "ministerio publico"])
            nota = (1.0 if c1 else 0.0) + (1.0 if c2 else 0.0) + (1.0 if c3 else 0.0) + (1.5 if c4 else 0.0) + (0.5 if c5 else 0.0)
            st.subheader(f"🎯 Nota Final Simulada: {nota:.2f} / 5,00 pontos")
            if nota >= 3.0:
                st.success("🎉 **APROVADO NA SIMULAÇÃO!** Você atingiu a pontuação mínima exigida pela OAB.")
            else:
                st.error("⚠️ **NOTA INSUFICIENTE.** Revise os itens omitidos abaixo.")
                if "Mandado de Segurança (2ª Fase)" not in st.session_state.temas_dificuldade:
                    st.session_state.temas_dificuldade.append("Mandado de Segurança (2ª Fase)")
            res = pd.DataFrame({
                "Critério Oficial": [
                    "1. Endereçamento (Vara da Fazenda Pública)",
                    "2. Fundamentação (CF Art. 5º, LXIX e Lei 12.016/09)",
                    "3. Mérito (Direito Líquido e Certo)",
                    "4. Pedido de Medida Liminar",
                    "5. Notificação da Autoridade e MP"
                ],                "Status": [
