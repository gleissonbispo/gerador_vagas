# 🤖 Gerador de Descrições de Vagas com LLM Local

**Automatize a criação de descrições de vagas de trabalho** com um fluxo completo:  
- **CRUD** de informações fixas (empresa, missão, visão, valores, benefícios) em SQLite  
- **Interface** intuitiva de configuração e geração com Streamlit  
- **Geração** de vaga em Markdown, com seções padronizadas e tom apaixonante  
- **LLM rodando localmente** via Ollama integrado com LangChain  

---

## 🚀 Demonstração

![Vagas-LLM-Preview](/geradordevaga.gif)

---

## 🧰 Tecnologias Utilizadas

| Categoria            | Ferramentas & Bibliotecas                                         |
|----------------------|-------------------------------------------------------------------|
| **LLM Local**        | [Ollama](https://ollama.com) · Modelos: `gemma3:12b` |
| **Orquestração**     | LangChain · PromptTemplate                                        |
| **Frontend**         | Streamlit                                                         |
| **Banco de Dados**   | SQLite (via `sqlite3` Python)                                     |
| **Backend**          | Python                                                            |

---

## 🧱 Funcionalidades

### ⚙️ Configuração da Empresa
- CRUD de **nome**, **missão**, **visão** e **valores**  
- Listagem e gerenciamento de **benefícios**, com valores (ex.: Vale‑refeição – R$ 35,00)  
- Tudo editável pela **Sidebar** do Streamlit  

### 🔍 Geração de Vagas
- Input de **Título**, **Departamento** e **Breve descrição**  
- Produção automática da vaga em Markdown, com seções:
  1. **Título**  
  2. **Sobre a Empresa**  
  3. **Visão Geral da Função**  
  4. **Responsabilidades**  
  5. **Requisitos**  
  6. **Diferenciais**  
  7. **Benefícios e Cultura**  
- Tom de voz **apaixonante**, **convidativo** e **inclusivo**  

### 📥 Exportação & Copy/Paste
- Saída pronta para colar no LinkedIn, site de vagas ou GitHub 

---

## 🧪 Exemplo de Uso

```bash
git clone https://github.com/gleissonbispo/gerador_vagas.git
cd gerador_vagas
pip install -r requirements.txt
streamlit run gerador_vaga.py
