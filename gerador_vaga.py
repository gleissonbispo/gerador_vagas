# =============================
# 🤖 Gerador Inteligente de Descrições de Vagas com LLM Local
# =============================

# 📦 Bibliotecas
from gerencia_db import init_db, get_company, update_company, add_benefit, remove_benefit
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from time import sleep

# =============================
# ✨ Configurações Iniciais
# =============================
DB_PATH = "db_empresa.db"
llm = ChatOllama(model="gemma3:12b")

prompt = PromptTemplate(
    input_variables=[
        "empresa", "missao", "visao", "valores", "beneficios",
        "titulo", "departamento", "descricao"
    ],
    template="""
Você é um(a) especialista em RH e copywriter de atração de talentos. Com base nas informações abaixo, gere **apenas** a descrição da vaga em **Markdown**, sem comentários extras, seguindo esta estrutura e tom:

## {titulo} - {departamento}

### Sobre a Empresa
Escreva um parágrafo breve e impactante apresentando **{empresa}**, incorporando sua missão, visão e valores.

### Visão Geral da Função
Explique de forma cativante o propósito estratégico desta posição e o que esperamos que esse(a) colaborador(a) realize no dia a dia.

### Responsabilidades
- Liste de 4 a 6 responsabilidades principais, em bullet points.

### Requisitos
- Liste de 4 a 6 requisitos essenciais (formação, experiência, habilidades técnicas e comportamentais).

### Diferenciais
- Destaque 3 a 5 qualificações ou experiências desejáveis que agregam valor.

### Benefícios e Cultura
- Liste cada benefício (ex.: Vale-refeição - R$ 35,00 dia) em bullet points.
- Inclua um parágrafo curto sobre a cultura da empresa, reforçando um ambiente inclusivo e colaborativo.

**Tom de voz:** apaixonante, convidativo e inclusivo.

---
**Dados**  
Empresa: {empresa}  
Missão: {missao}  
Visão: {visao}  
Valores: {valores}  
Benefícios: {beneficios}  

Título da vaga: {titulo}  
Departamento: {departamento}  
Breve descrição da função: {descricao}
"""
)

# =============================
# 🎨 Configuração da Interface Streamlit
# =============================
st.set_page_config(page_title="Gerador de Vagas LLM", page_icon="📝", layout="centered")
init_db(DB_PATH)

# --- Sidebar de Configuração ---
st.sidebar.header("⚙️ Configurações da Empresa")
info = get_company(DB_PATH)
with st.sidebar.form("cfg_form", clear_on_submit=False):
    name = st.text_input("Nome", value=info["nome"])
    mission = st.text_area("Missão", value=info["missao"])
    vision = st.text_area("Visão", value=info["visao"])
    vals = st.text_area("Valores (vírgula)", value=", ".join(info["valores"]))
    if st.form_submit_button("💾 Salvar"):
        new_vals = [v.strip() for v in vals.split(",") if v.strip()]
        update_company(DB_PATH, nome=name, missao=mission, visao=vision, valores=new_vals)
        st.success("✅ Informações atualizadas!")

st.sidebar.markdown("---")
st.sidebar.subheader("🛡️ Benefícios")
for b in info["beneficios"]:
    col1, col2 = st.sidebar.columns([4,1])
    col1.write(f"- {b}")
    if col2.button("❌", key=f"rm_{b}"):
        remove_benefit(DB_PATH, desc=b)
        st.rerun()

with st.sidebar.form("add_benefit_form", clear_on_submit=True):
    new_b = st.text_input("Novo benefício")
    submitted = st.form_submit_button("➕ Adicionar")
    if submitted:
        if new_b.strip() == "":
            st.error("❗️ Por favor, digite um benefício antes de adicionar.")
        elif new_b.strip() in info["beneficios"]:
            st.error("❗️ Benefício já consta na lista.")
        else:
            add_benefit(DB_PATH, desc=new_b.strip())
            st.success("✅ Benefício adicionado!")

# --- Main Content ---
st.title("🔍 Gerador de Descrição de Vagas")
titulo_vaga      = st.text_input("Título da vaga")
departamento_vaga = st.text_input("Departamento")
descricao_vaga   = st.text_area("Breve descrição da função")

if st.button("🌀 Gerar Vaga", use_container_width=True):
    with st.status("💭 Escrevendo a vaga...", expanded=True) as status:
        resposta = llm.invoke(
            prompt.format(
                empresa=info["nome"],
                missao=info["missao"],
                visao=info["visao"],
                valores=", ".join(info["valores"]),
                beneficios=", ".join(info["beneficios"]),
                titulo=titulo_vaga,
                departamento=departamento_vaga,
                descricao=descricao_vaga
            )
        )
        sleep(1.5)
        status.update(label="✅ Vaga Gerada", state="complete")

    # =============================
    # 📈 Exibição da Descrição Gerada
    # =============================
    st.markdown("---")
    st.subheader("📋 Descrição Desenvolvida")
    st.markdown(resposta.content)
