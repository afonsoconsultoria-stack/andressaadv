import streamlit as st
import json
import pandas as pd

# 🎨 CONFIGURAÇÃO VISUAL (LEGAL DESIGN)
st.set_page_config(page_title="LexAI OAB - Direito Administrativo", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #f8fafc;}
    .stMetric {background-color: #ffffff; padding: 18px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); border-left: 5px solid #1E3A8A;}
    div.stButton > button:first-child {background-color: #1E3A8A; color: white; width: 100%; border-radius: 6px; font-weight: bold; padding: 10px;}
    div.stButton > button:first-child:hover {background-color: #1e40af; color: white;}
    .gabarito-box {background-color: #E0F2FE; padding: 18px; border-radius: 8px; border-left: 5px solid #0284C7; margin-top: 15px;}
    </style>
""", unsafe_allowed_html=True)

# Inicialização da Memória Interativa (Session State)
if "acertos" not in st.session_state:
    st.session_state.acertos = 0
if "erros" not in st.session_state:
    st.session_state.erros = 0
if "respondidas" not in st.session_state:
    st.session_state.respondidas = []
if "temas_dificuldade" not in st.session_state:
    st.session_state.temas_dificuldade = []

# Carregamento da Base de Dados
try:
    with open('dados_oab.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
except FileNotFoundError:
    st.error("Erro: Arquivo 'dados_oab.json' não encontrado no repositório.")
    st.stop()

# 📌 MENU LATERAL INTERATIVO
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
st.sidebar.subheader("📈 Seu Desempenho Ao Vivo")
st.sidebar.write(f"✅ Acertos: **{st.session_state.acertos}**")
st.sidebar.write(f"❌ Erros: **{st.session_state.erros}**")

if st.sidebar.button("🔄 Zerar Progresso"):
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.respondidas = []
    st.session_state.temas_dificuldade = []
    st.rerun()

# ==========================================
# MÓDULO 1: PAINEL ESTATÍSTICO INTERATIVO
# ==========================================
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
    
    # Abas interativas para alternar visualização
    tab1, tab2, tab3 = st.tabs(["📈 Gráfico Interativo (1ª Fase)", "📋 Tabela Detalhada (1ª Fase)", "🏛️ Peças Processuais (2ª Fase)"])
    
    df_1fase = pd.DataFrame(db["estatisticas_1a_fase"])
    
    with tab1:
        st.subheader("Incidência de Questões por Tema Jurídico")
        st.bar_chart(df_1fase.set_index("tema")["questoes"], color="#1E3A8A")
        st.caption("Passe o cursor sobre as barras para visualizar o número exato de questões cobradas entre 2022 e 2026.")
        
    with tab2:
        st.subheader("Dados Auditados da Prova Objetiva")
        filtro_tendencia = st.multiselect("Filtrar por tendência de cobrança:", options=["Alta", "Estável", "Queda"], default=["Alta", "Estável", "Queda"])
        df_filtrado = df_1fase[df_1fase["tendencia"].isin(filtro_tendencia)]
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
        
    with tab3:
        st.subheader("Mapeamento de Peças Prático-Profissionais")
        df_2fase = pd.DataFrame(db["pecas_recorrentes_2a_fase"])
        st.dataframe(df_2fase, use_container_width=True, hide_index=True)

# ==========================================
# MÓDULOS 2 e 3: SIMULADOR INTERATIVO
# ==========================================
elif modulo == "📝 Módulos 2 e 3: Simulador Interativo":
    st.title("📝 Banco Inteligente de Questões (1ª Fase)")
    
    questoes = db["questoes_simulado"]
    total_q = len(questoes)
    
    # Barra de Progresso
    progresso = len(st.session_state.respondidas) / total_q
    st.progress(progresso, text=f"Progresso do Simulado: {len(st.session_state.respondidas)} de {total_q} questões respondidas")
    
    # Filtro por Tema
    temas_disponiveis = ["Todos os Temas"] + list(set([q["tema"] for q in questoes]))
    tema_escolhido = st.selectbox("Filtrar questões por assunto jurídico:", temas_disponiveis)
    
    questoes_filtradas = questoes if tema_escolhido == "Todos os Temas" else [q for q in questoes if q["tema"] == tema_escolhido]
    
    lista_titulos = [f"Questão {q['id']} - {q['tema']}" for q in questoes_filtradas]
    escolha_q = st.selectbox("Selecione a questão:", lista_titulos)
    
    idx = lista_titulos.index(escolha_q)
    q_atual = questoes_filtradas[idx]
    
    with st.container(border=True):
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

# ==========================================
# MÓDULO 4: CORRETOR DINÂMICO DE 2ª FASE
# ==========================================
elif modulo == "🤖 Módulo 4: Corretor Inteligente":
    st.title("🤖 Corretor Pedagógico de Peças (2ª Fase)")
    st.caption("Avaliação automatizada baseada nos critérios reais do espelho da banca FGV.")
    
    with st.expander("📄 Ver Caso Prático e Espelho Oficial (Clique para expandir)", expanded=True):
        st.warning("**Enunciado da Peça:** Candidato aprovado dentro das vagas em concurso público estadual foi ilegalmente eliminado na fase documental por ato do Secretário de Administração. Redija os tópicos principais do **Mandado de Segurança** cabível.")
        st.code("""CRITÉRIOS DO ESPELHO OFICIAL (5,00 PONTOS):
1. Endereçamento ao Juízo da Vara da Fazenda Pública Estadual (1,00 pt)
2. Fundamentação legal: Art. 5º, LXIX da CF e Lei 12.016/09 (1,00 pt)
3. Demonstração do Direito Líquido e Certo violado (1,00 pt)
4. Pedido de Medida Liminar: Fumus Boni Iuris e Periculum in Mora (1,50 pt)
5. Pedido de notificação da Autoridade Coatora e intimação do MP (0,50 pt)""", language="text")
    
    resposta_aluno = st.text_area("✍️ Escreva ou cole sua resposta jurídica abaixo para correção em tempo real:", height=180, placeholder="Ex: Excelentíssimo Senhor Doutor Juiz de Direito da Vara da Fazenda Pública... Com fundamento na Lei 12.016/09, vem impetrar Mandado de Segurança com pedido de liminar...")
    
    if st.button("🚀 Executar Correção Inteligente"):
        if len(resposta_aluno.strip()) < 15:
            st.warning("Por favor, digite uma resposta mais completa para que o corretor possa avaliar os requisitos jurídicos.")
        else:
            texto = resposta_aluno.lower()
            
            # Análise real de palavras-chave jurídicas do espelho
            c1 = any(p in texto for p in ["fazenda pública", "fazenda publica", "juiz de direito"])
            c2 = any(p in texto for p in ["12.016", "lxix", "5º", "mandado de segurança"])
            c3 = any(p in texto for p in ["líquido e certo", "liquido e certo", "ilegal", "direito"])
            c4 = any(p in texto for p in ["liminar", "fumus", "periculum", "urgência", "urgencia"])
