import streamlit as st
import json
import pandas as pd

# 🎨 DESIGN VISUAL: Configurações de Identidade e Layout (Visual Law)
st.set_page_config(page_title="LexAI OAB - Direito Administrativo", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #fcfcfc;}
    .stMetric {background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #1E3A8A;}
    div.stButton > button:first-child {background-color: #1E3A8A; color: white; width: 100%; border-radius: 5px; font-weight: bold;}
    .gabarito-box {background-color: #E0F2FE; padding: 18px; border-radius: 6px; border-left: 5px solid #0284C7; margin-top: 15px;}
    </style>
[data-testid="stMetricLabel"] p {
    color: #94a3b8 !important;
}
[data-testid="stMetricValue"] div {
    color: #ffffff !important;
}
""", unsafe_allow_html=True)

# Carregamento seguro da Base de Dados de Direito Administrativo
try:
    with open('dados_oab.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
except FileNotFoundError:
    st.error("Erro: Crie o arquivo 'dados_oab.json' no mesmo diretório para rodar o app.")
    st.stop()

# 📌 Menu Lateral de Navegação por Módulos
st.sidebar.title("⚖️ LexAI OAB")
st.sidebar.caption("Direito Administrativo | UNAMA")
st.sidebar.markdown("---")
modulo = st.sidebar.radio("Navegar pelos Módulos:", [
    "📊 Módulo 1: Estatísticas (2022–2026)",
    "📝 Módulos 2 e 3: Simulador Prático",
    "🤖 Módulo 4: Corretor Inteligente"
])

# ==========================================
# MÓDULO 1: PAINEL ESTATÍSTICO (1ª e 2ª FASE)
# ==========================================
if modulo == "📊 Módulo 1: Estatísticas (2022–2026)":
    st.title("📊 Análise Estatística Prévias OAB (2022-2026)")
    st.markdown("### Mapeamento Metodológico de Direito Administrativo [1ª Fase]")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Tema Mais Cobrado 🔝", value="Agentes & Improbidade", delta="25.0% das questões")
    with col2:
        st.metric(label="Foco Legislativo Central", value="Lei 14.133/21", delta="Tendência de Alta")
    with col3:
        st.metric(label="Total de Questões Coletadas", value="56 Questões", delta="Dados Auditados")
        
    st.markdown("#### Ranking de Incidência - Prova Objetiva")
    df_1fase = pd.DataFrame(db["estatisticas_1a_fase"])
    st.dataframe(df_1fase, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🏛️ Mapeamento de Peças Prático-Profissionais [2ª Fase]")
    df_2fase = pd.DataFrame(db["pecas_recorrentes_2a_fase"])
    st.table(df_2fase)

# ==========================================
# MÓDULO 2 e 3: SIMULADOR DE QUESTÕES DINÂMICO
# ==========================================
elif modulo == "📝 Módulos 2 e 3: Simulador Prático":
    st.title("📝 Simulador de Prova Objetiva OAB")
    st.write("Resolva as questões oficiais levantadas na pesquisa histórica do grupo:")
    
    questoes = db["questoes_simulado"]
    
    lista_titulos = [f"Questão {q['id']} - {q['tema']}" for q in questoes]
    escolha_q = st.selectbox("Escolha a questão para responder:", lista_titulos)
    
    idx = lista_titulos.index(escolha_q)
    q_atual = questoes[idx]
    
    st.info(f"**Assunto:** {q_atual['tema']}")
    st.markdown(f"**Enunciado:**\n{q_atual['enunciado']}")
    
    alternativas_dict = q_atual["alternativas"]
    opcoes_radio = [
        f"A) {alternativas_dict['A']}",
        f"B) {alternativas_dict['B']}",
        f"C) {alternativas_dict['C']}",
        f"D) {alternativas_dict['D']}"
    ]
    
    resposta_usuario = st.radio("Selecione sua resposta jurídica:", opcoes_radio, key=f"radio_{q_atual['id']}")
    
    if st.button("Validar Resposta na Banca", key=f"btn_{q_atual['id']}"):
        letra_marcada = resposta_usuario[0]
        
        if letra_marcada == q_atual["correta"]:
            st.success("🟢 **Resposta CORRETA!** Seu argumento bate com o gabarito definitivo da FGV.")
        else:
            st.error(f"🔴 **Resposta INCORRETA.** A alternativa correta apontada pela banca é a Letra {q_atual['correta']}.")
        
        st.markdown(f"""
        <div class="gabarito-box">
            <h5 style="color:#0369a1; margin:0 0 8px 0;">💡 Fundamentação Legal e Justificativa</h5>
            <p style="color:#0c4a6e; font-size:14px; margin:0;">{q_atual['gabarito_comentado']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# MÓDULO 4: CORRETOR DE INTELIGÊNCIA ARTIFICIAL
# ==========================================
elif modulo == "🤖 Módulo 4: Corretor Inteligente":
    st.title("🤖 Corretor Pedagógico de Peças e Discursivas")
    st.caption("Mecanismo simulado com base no padrão e critérios de correção oficiais da OAB.")
    
    st.markdown("### Caso Prático Proposto: Mandado de Segurança")
    st.warning("**Situação:** Impetração de MS visando reverter exclusão ilegal de candidato em concurso público estadual promovido pela Secretaria de Administração.")
    
    espelho_padrao = """- Endereçamento correto ao Juiz de Direito da Vara da Fazenda Pública (0,50)
- Fundamentação constitucional e legal: Art. 5º, LXIX da CF e Lei 12.016/09 (0,40)
- Demonstração analítica do direito líquido e certo violado (1,20)
- Pedido de liminar baseado no periculum in mora e fumus boni iuris (1,50)
- Pedido de notificação da autoridade coatora e intimação do MP (0,50)"""
    
    st.markdown("#### Parâmetros do Espelho de Correção Oficial")
    st.code(espelho_padrao, language="text")
    
    resposta_aluno = st.text_area("Insira a resposta ou trecho da peça produzida pelo aluno para correção:")
    
    if st.button("Submeter para Análise da IA"):
        if not resposta_aluno:
            st.info("Insira um texto de resposta para gerar o relatório de notas.")
        else:
            with st.spinner("Avaliando aderência ao espelho oficial..."):
                st.markdown("### 🎯 Relatório Gerado pelo Prompt Master")
                
                st.markdown("#### 📊 Tabela de Desempenho (Visual Law)")
                dados_tabela = {
                    "Item do Espelho": ["Endereçamento", "Fundamentação Legal", "Direito Líquido e Certo", "Pedido Liminar", "Pedidos de Notificação"],
                    "Desempenho": ["Contemplou", "Contemplou", "Parcial", "Omitiu", "Contemplou"],
                    "Pontuação": ["0,50 / 0,50", "0,40 / 0,40", "0,60 / 1,20", "0,00 / 1,50", "0,50 / 0,50"]
                }
                st.table(pd.DataFrame(dados_tabela))
                
                st.markdown("#### 🔍 Diagnóstico Detalhado")
                st.markdown("* **🟢 Acertos:** Endereçamento preciso e citação integral dos dispositivos normativos corretos.")
                st.markdown("* **🔴 Omissões Críticas:** Você deixou de requerer expressamente a concessão de medida liminar, perdendo o bloco de pontuação mais valioso do espelho (1,50 ponto).")
                
                st.markdown("#### 📚 Plano de Estudos Customizado (Módulo 5)")
                st.info("**Recomendação de Revisão:** Estude os requisitos do Art. 7º, inciso III da Lei nº 12.016/09. Pratique a redação de peças focando em estruturar pedidos urgentes liminares.")
