# O.R.I.O.N. (Omniscient Routine Integrator & Operations Node)

Um sistema avançado de assistente de Inteligência Artificial baseado no modelo Llama 3 (via Ollama) operando totalmente offline. Projetado para atuar como um "Hiper-Motor Híbrido Multi-Núcleos", o sistema é capaz de interagir com o usuário, executar comandos no terminal (Bash), rodar consultas em banco de dados (SQL) e executar scripts (Python) com permissão prévia, além de analisar, auditar e compilar projetos de Minecraft (Forge) e aplicações Web (PHP/JS).

## 🚀 Funcionalidades

- **Interação Natural:** Chat alimentado pelo modelo `llama3` usando a infraestrutura do Ollama.
- **Execução Autônoma Segura:** A IA pode propor comandos de sistema, consultas SQL e scripts Python, que são executados localmente apenas após a confirmação (`S/N`) do usuário.
- **Arquitetura Multi-Núcleos:**
  - **Núcleo A (`a.py`):** Interface central de chat, memória (banco de dados) e execução de comandos físicos no sistema operativo.
  - **Núcleo B (`b.py`):** Módulo de varredura. Indexa códigos do Mod Forge, do Painel Web e captura logs críticos de execução (ex: PrismLauncher).
  - **Núcleo C (`c.py`):** Módulo de auditoria de código via IA. Realiza diagnóstico inteligente de bugs cruzando código-fonte com logs de erro, focando em otimizar a integração do sistema Solana-Minecraft.
  - **Núcleo D (`d.py`):** Módulo de automação. Compila o Mod (Gradle Build) e injeta o `.jar` diretamente na instância do PrismLauncher.

## ⚙️ Pré-requisitos

Para rodar este projeto na sua máquina (focado em ambiente Linux, como Debian), você precisará de:

1. **Python 3** (testado com 3.13)
2. **MariaDB** (ou MySQL)
3. **Ollama** (com o modelo `llama3` baixado localmente)
4. Bibliotecas Python: `mysql-connector-python`, `ollama`, `beautifulsoup4`, `psutil`

## 🛠️ Instalação

### 1. Preparando o Ambiente
Como este projeto está rodando em um disco externo/pendrive (que não suporta criação de ambientes virtuais do Linux nativamente), você deve instalar as bibliotecas forçando a instalação global no seu sistema operacional.

No terminal do Linux, execute:
```bash
pip install mysql-connector-python ollama beautifulsoup4 psutil --break-system-packages
```

### 2. Configurando o Banco de Dados (MariaDB)
O projeto depende de uma conexão com o MariaDB na máquina local para salvar o histórico de conversas e coordenar os núcleos de análise. 

1. Certifique-se de que o MariaDB está rodando.
2. O sistema espera o seguinte usuário padrão no código (pode ser ajustado em `a.py`, `b.py` e `c.py`):
   - **Usuário:** `root`
   - **Senha:** `0073007`
   - **Host:** `localhost`

Os bancos de dados e tabelas (`ChatbotDB`, `Conversations`, `PluginAnalise`) são criados e gerenciados automaticamente pelas aplicações Python assim que rodadas pela primeira vez.

### 3. Configurando o Ollama
Garanta que o Ollama esteja instalado e tenha o modelo `llama3` disponível:
```bash
ollama run llama3
```
*O script de inicialização assume que os modelos estão armazenados no caminho definido na variável `OLLAMA_MODELS` (padrão: `/media/astral/7DFD-F7FB/AI-O/models`).*

## 💻 Como Usar

### Iniciando o Assistente
Para iniciar o ecossistema completo de forma otimizada, use o script de start:
```bash
bash start_orion.sh
```
Este script irá fechar instâncias passadas, iniciar o servidor Ollama em background e executar o Núcleo A (`a.py`), iniciando a interface do O.R.I.O.N.

### Interagindo
- Converse normalmente.
- Se a IA sugerir a execução de algum código ou comando, o terminal irá congelar aguardando sua autorização explícita (`S` para Sim, `N` para Não).
- **Comando de Gatilho Rápido:** Digitar frases como `"revisa um plugin"` ou `"revisar"` acionará os Núcleos B e C em background, mapeando seu projeto atual, avaliando erros e gerando um relatório em disco chamado `log.txt`.

### Modo de Emergência
Se o sistema principal apresentar instabilidade e você precisar de acesso limpo à IA, utilize:
```bash
bash emergencia.sh
```
Isso desliga o núcleo Python e conecta você diretamente ao console puro do Ollama.

## 📂 Estrutura de Arquivos

| Arquivo/Diretório | Descrição |
| --- | --- |
| `start_orion.sh` | Inicializador mestre do servidor de IA e do bot. |
| `a.py` | Núcleo Principal (A) de conversação, memória em banco e execução de ações físicas na máquina. |
| `b.py` | Núcleo de Mapeamento (B). Varre projetos locais e registra arquivos pendentes para revisão no banco de dados. |
| `c.py` | Núcleo de Auditoria (C). Lê arquivos pendentes no banco e usa a IA para diagnosticar erros reportados nos logs. |
| `d.py` | Núcleo de Deploy (D). Automatiza o `gradle build` e instalação do mod no PrismLauncher. |
| `emergencia.sh` | Acesso purista direto ao CLI da IA em caso de falha do script principal. |
| `script.sh` | Utilitário rápido de substituição de IP em arquivos de configuração local (`sed`). |

---
**Nota de Segurança:** Este projeto executa comandos shell e executa queries baseadas na saída de um modelo de linguagem gerativo. O uso do protocolo de barreira e autorização manual (`S/N`) inserido no núcleo principal é de extrema importância para a segurança do sistema operacional.
