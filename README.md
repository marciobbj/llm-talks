# LLM Talks 🤖💬🤖

**LLM Talks** é uma ferramenta que coloca dois modelos de Inteligência Artificial para conversar entre si sobre qualquer assunto que você definir. 

O projeto foi desenhado para ser **extremamente flexível**, permitindo o uso de:
- **Modelos Locais** (via Ollama, LocalAI, etc.)
- **Modelos em Nuvem** (OpenRouter, OpenAI, etc.)
- **Configurações Híbridas** (ex: GPT-4 conversando com Llama 3 localmente)

Possui uma interface web moderna, focada na legibilidade e simplicidade.

## Funcionalidades

- **Batalha de IAs**: Coloque perspectivas diferentes (persona Curiosa vs Cética) para debater.
- **Interface Otimizada**: Design limpo, com fontes grandes e alto contraste para fácil leitura.
- **Flexibilidade Total**: Configure URLs base e chaves de API independentes para cada modelo.
- **Modo CLI**: Também pode ser executado diretamente no terminal.

## Instalação

1. **Clone o repositório** e entre na pasta:
   ```bash
   git clone https://github.com/seu-usuario/llm-talks.git
   cd llm-talks
   ```

2. **Crie um ambiente virtual (Recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o ambiente**:
   Copie o exemplo e edite com suas chaves:
   ```bash
   cp .env.example .env
   ```

## Configuração (.env)

O arquivo `.env` na raiz do projeto gerencia os modelos.

**Exemplo: Dois Modelos Locais (Ollama)**
```ini
# Modelo A
MODEL_A_NAME=llama3
MODEL_A_API_KEY=ollama
MODEL_A_BASE_URL=http://localhost:11434/v1

# Modelo B
MODEL_B_NAME=mistral
MODEL_B_API_KEY=ollama
MODEL_B_BASE_URL=http://localhost:11434/v1
```

## 🖥️ Como Usar

### Interface Web
1. Inicie o servidor Flask:
   ```bash
   python app.py
   ```
2. Acesse **[http://localhost:5000](http://localhost:5000)** no seu navegador.
3. Digite um tópico e inicie a conversa.

### Linha de Comando (CLI)
Para rodar rapidamente no terminal, sem interface gráfica:
```bash
python llm_talks.py --topic "A ética na clonagem humana"
```

## Estrutura do Projeto

- `app.py`: Servidor Backend (Flask).
- `llm_talks.py`: Lógica central de controle da conversa.
- `templates/index.html`: Interface do usuário.
- `static/css/styles.css`: Estilos otimizados.

## Contribuição

Sinta-se à vontade para abrir issues ou enviar PRs!
