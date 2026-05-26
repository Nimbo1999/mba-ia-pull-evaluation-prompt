# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Desafio do MBA em Engenharia de Software com IA — otimização de prompts usando técnicas avançadas de Prompt Engineering, com avaliação automatizada via LangSmith.

---

## Sumário

- [Técnicas Aplicadas (Fase 2)](#técnicas-aplicadas-fase-2)
- [Resultados Finais](#resultados-finais)
- [Como Executar](#como-executar)

---

## Técnicas Aplicadas (Fase 2)

### 1. Role Prompting (Persona)

**O que é:** Atribuir ao modelo uma identidade específica com expertise no domínio da tarefa.

**Por que escolhi:** Bugs são relatos técnicos que precisam ser traduzidos em User Stories seguindo convenções de times ágeis. Ao definir a persona de *"Gestor de Projeto sênior especializado em metodologias ágeis"*, o modelo passa a gerar outputs com vocabulário, estrutura e nível de detalhe condizente com o que um PM experiente entregaria — reduzindo respostas genéricas.

**Como apliquei:**
```
Você é um Gestor de Projeto (Project Manager) sênior especializado em metodologias ágeis.
Sua responsabilidade é transformar relatos de bugs em User Stories bem estruturadas,
claras e acionáveis para o time de desenvolvimento.
```

---

### 2. Few-Shot Learning (obrigatório)

**O que é:** Fornecer exemplos concretos de entrada → saída dentro do prompt para que o modelo aprenda o padrão esperado por indução.

**Por que escolhi:** O modelo precisa entender não apenas o formato da User Story, mas também como inferir o perfil de usuário correto, quando usar Gherkin, quando usar bullet points, e quais seções incluir ou omitir. Exemplos cobrem isso melhor do que qualquer instrução textual isolada.

**Como apliquei:** Incluí 3 exemplos no prompt cobrindo cenários distintos:
- **Exemplo simples** (bug de UI): mostra o caso mínimo — apenas descrição + Critérios de Aceitação.
- **Exemplo médio** (e-commerce com race condition): demonstra uso de Critérios de Prevenção e identificação correta do perfil "cliente".
- **Exemplo complexo** (performance com SQL): ilustra Critérios Técnicos com code blocks e agrupamento por subtema.

## Resultados Finais

### Dashboard LangSmith

🔗 **[Link do dataset e experimentos](https://smith.langchain.com/public/c6e739b4-5d35-4dc7-aad9-b7e9cd686d95/d)**

### Screenshots

**Resultado da avaliação via CLI:**

![CLI Result](screenshots/cli-result.png)

**Dashboard de experimentos no LangSmith:**

![LangSmith UI](screenshots/LangSmith-UI.png)

### Métricas Finais — `nimbo/bug_to_user_story_v2`

| Métrica | v1 (inicial) | v2 (otimizado) | Meta | Status |
|---|---|---|---|---|
| Helpfulness | 0.45 | **0.97** | ≥ 0.9 | ✅ |
| Correctness | 0.52 | **0.96** | ≥ 0.9 | ✅ |
| F1-Score | 0.48 | **0.94** | ≥ 0.9 | ✅ |
| Clarity | 0.50 | **0.96** | ≥ 0.9 | ✅ |
| Precision | 0.46 | **0.98** | ≥ 0.9 | ✅ |
| **Média** | **0.48** | **0.9624** | ≥ 0.9 | ✅ |

> ✅ **STATUS: APROVADO** — Todas as métricas ≥ 0.9

### Jornada de Iterações

| Iteração | Problema identificado | Ação tomada |
|---|---|---|
| v1 | Todas as métricas < 0.6 — prompt vago, sem estrutura | Reescrita completa com Role Prompting + seções condicionais |
| v2 | Perfil de usuário incorreto em bugs de backend | Adicionada hierarquia de decisão com regra do "teste decisivo" |
| v3 | Seções sendo omitidas em bugs médios | Adicionada instrução de releitura e checklist de seções |
| v4 | Clareza baixa em bugs de performance | Adicionados exemplos Few-shot para cenários técnicos com SQL |
| v5 | Precision abaixo de 0.9 em edge cases | Refinadas regras de formato (Gherkin vs bullet points por seção) |

---

## Como Executar

### Pré-requisitos

- Python 3.9+, Versão usada no exercício: Python 3.13.5
- Conta no [LangSmith](https://smith.langchain.com/) (gratuita)
- API Key da [OpenAI](https://platform.openai.com/api-keys)

### 1. Clonar e configurar o ambiente

```bash
git clone <seu-fork>
cd mba-ia-pull-evaluation-prompt

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais:

```env
LANGCHAIN_API_KEY=sua_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Prompt optimization challenge

# Escolha um provider:
OPENAI_API_KEY=sua_openai_key          # OpenAI
# ou
GOOGLE_API_KEY=sua_google_key          # Gemini (gratuito)
```

### Modelos utilizados

| Provider | Resposta | Avaliação |
|---|---|---|
| OpenAI | `gpt-4o-mini` | `gpt-4o` |
