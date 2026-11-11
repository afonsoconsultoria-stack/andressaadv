import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="LexAI OAB - Direito Administrativo", layout="wide", initial_sidebar_state="expanded")

# ESTILO VISUAL CLARO E LIMPO (LEGAL DESIGN)
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #1E3A8A;
    }
    .quadro-destaque {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 6px solid #1E3A8A;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
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
        background-color: #E0F2FE;
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
        col_g1.bar_chart(df_1fase.set_index("tema")["questoes"], color="#1E3A8A")
        col_g1.caption("Número absoluto de questões auditadas (2022–2026).")
        
        col_g2.subheader("Percentual de Incidência (%)")
        col_g2.bar_chart(df_1fase.set_index("tema")["porcentagem"], color="#0284C7")
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
        if q_atual["tema"] not in st.session_state.temas_dificuldade:
            st.session_state.temas_dificuldade.append(q_atual["tema"])
        st.warning(f"Tema **{q_atual['tema']}** adicionado ao seu Plano de Revisão (Módulo 5)!")

    if validar:
        letra_marcada = resposta_usuario[0]
        
        if q_atual["id"] not in st.session_state.respondidas:
            st.session_state.respondidas.append(q_atual["id"])
            if letra_marcada == q_atual["correta"]:
                st.session_state.acertos += 1
            else:
                st.session_state.erros += 1
                if q_atual["tema"] not in st.session_state.temas_dificuldade:
                    st.session_state.temas_dificuldade.append(q_atual["tema"])
        
        if letra_marcada == q_atual["correta"]:
            st.success("🟢 **Resposta CORRETA!** Pontuação contabilizada no seu painel lateral.")
        else:
            st.error(f"🔴 **Resposta INCORRETA.** A alternativa correta da FGV é a Letra **{q_atual['correta']}**. Este tema foi salvo na sua lista de revisão.")
        
        st.markdown(f"""
        <div class="gabarito-box">
            <h5 style="color:#0369a1; margin:0 0 8px 0;">💡 Fundamentação Legal e Gabarito Oficial</h5>
            <p style="color:#0c4a6e; font-size:15px; margin:0;">{q_atual['gabarito_comentado']}</p>
        </div>
        """, unsafe_allow_html=True)

# MODULO 4: CORRETOR DINAMICO DE 2a FASE
elif modulo == "🤖 Módulo 4: Corretor Inteligente":
    st.title("🤖 Corretor Pedagógico de Peças (2ª Fase)")
    st.markdown("### Avaliação Automatizada Baseada no Espelho Oficial FGV")
    
    st.markdown("""
    <div class="quadro-destaque">
        <h4>📄 Caso Prático Proposto: Mandado de Segurança</h4>
        <p><strong>Situação:</strong> Candidato aprovado dentro das vagas em concurso público estadual foi ilegalmente eliminado na fase documental por ato do Secretário de Administração. Redija os tópicos principais do <strong>Mandado de Segurança</strong> cabível.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📋 Critérios do Espelho Oficial (5,00 Pontos)")
    st.code("""1. Endereçamento ao Juízo da Vara da Fazenda Pública Estadual (1,00 pt)
2. Fundamentação legal: Art. 5º, LXIX da CF e Lei 12.016/09 (1,00 pt)
3. Demonstração do Direito Líquido e Certo violado (1,00 pt)
4. Pedido de Medida Liminar: Fumus Boni Iuris e Periculum in Mora (1,50 pt)
5. Pedido de notificação da Autoridade Coatora e intimação do MP (0,50 pt)""", language="text")
    
    st.markdown("---")
    resposta_aluno = st.text_area("✍️ Escreva ou cole sua resposta jurídica abaixo para correção em tempo real:", height=180, placeholder="Ex: Excelentíssimo Senhor Doutor Juiz de Direito da Vara da Fazenda Pública... Com fundamento na Lei 12.016/09, vem impetrar Mandado de Segurança com pedido de liminar...")
    
    if st.button("🚀 Executar Correção Inteligente"):
        if len(resposta_aluno.strip()) < 15:
            st.warning("Por favor, digite uma resposta mais completa para que o corretor possa avaliar os requisitos jurídicos.")
        else:
            texto = resposta_aluno.lower()
            
            c1 = any(p in texto for p in ["fazenda pública", "fazenda publica", "juiz de direito"])
            c2 = any(p in texto for p in ["12.016", "lxix", "5º", "mandado de segurança"])
            c3 = any(p in texto for p in ["líquido e certo", "liquido e certo", "ilegal", "direito"])
            c4 = any(p in texto for p in ["liminar", "fumus", "periculum", "urgência", "urgencia"])
