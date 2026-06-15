#!/usr/bin/env python3
import mysql.connector
import ollama
import sys
import os
import subprocess
import re
import datetime
import psutil
import urllib.request
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Biblioteca nativa do Linux para controle de terminal (evita pulos de input)
try:
    import termios
except ImportError:
    termios = None

# 1. Conexão Base com o MariaDB
try:
    cnx = mysql.connector.connect(user='root', password='0073007', host='localhost')
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ChatbotDB")
    cursor.execute("USE ChatbotDB")
except mysql.connector.Error as err:
    print(f"❌ Erro no MariaDB: {err}")
    sys.exit(1)

print("🧠 [O.R.I.O.N.] Hiper-Motor Híbrido (Multi-Núcleos) com Bloqueio de Teclado Ativado.")

# Função crucial para limpar o buffer e garantir a espera do S/N
def limpar_buffer_entrada():
    if termios:
        try:
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except Exception:
            pass

# 2. Funções de Infraestrutura e Execução Física
def executar_bash_real(comando):
    if any(x in comando for x in ["rm -rf /", "mkfs", "dd if="]):
        return "⚠️ Bloqueado: Protocolo de proteção crítica."
    try:
        res = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=30)
        saida = res.stdout if res.stdout else res.stderr
        return saida.strip() if saida else "Comando executado com sucesso."
    except Exception as e:
        return f"Erro na execução física: {str(e)}"

def executar_sql_real(query):
    try:
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            colunas = [i[0] for i in cursor.description]
            resultados = cursor.fetchall()
            return f"Colunas: {colunas} | Registros: {resultados}"
        else:
            cnx.commit()
            return f"Query executada. Linhas afetadas: {cursor.rowcount}"
    except mysql.connector.Error as err:
        return f"Erro SQL físico: {err}"

def executar_python_real(codigo_bloco):
    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            exec(codigo_bloco, globals())
        saida = f.getvalue()
        return saida.strip() if saida else "Script Python rodou perfeitamente."
    except Exception as e:
        return f"Erro de execução no script Python: {str(e)}"

def pesquisar_web(url):
    if not BeautifulSoup:
        return "Erro: Biblioteca bs4 não instalada. Execute 'pip install beautifulsoup4'"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=15).read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:2000] + "... [TRUNCADO]"
    except Exception as e:
        return f"Erro ao acessar web: {str(e)}"

# Consciência Dinâmica (Data/Hora e Memória)
def obter_prompt_sistema():
    ram_livre = psutil.virtual_memory().available / (1024**3)
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return (f"Você é o O.R.I.O.N., conectado ao Debian 13 do Senhor Astral. "
            f"Ambiente em tempo real: Data/Hora: {data_hora} | RAM Livre: {ram_livre:.2f}GB. "
            f"Você tem permissão para ler arquivos, bancos de dados e compilar projetos de Minecraft e PHP. "
            f"Sempre que precisar rodar comandos, use os blocos de markdown ```bash, ```sql ou ```python. "
            f"Para navegar ou ler informações na internet, use o bloco ```web seguido da URL ```. "
            f"O sistema vai aguardar a confirmação do usuário e te devolver o resultado. Se o resultado for um erro, analise e corrija sozinho.")

# 3. Resgatar histórico de mensagens do MariaDB (Limitado para não estourar memória)
cursor.execute("SELECT role, message FROM (SELECT role, message, timestamp FROM Conversations ORDER BY timestamp DESC LIMIT 30) sub ORDER BY timestamp ASC")
rows = cursor.fetchall()
messages = [{"role": "system", "content": obter_prompt_sistema()}]
for role, msg in rows:
    messages.append({"role": role, "content": msg})

print("-" * 50)

# 4. Loop de Execução e Interceptação Contínua
feedback_interno = None

try:
    while True:
        if feedback_interno:
            user_input = feedback_interno
            print(f"\n⚙️ \033[96m[Auto-Correção / Feedback de Sistema]\033[0m Injetando dados de volta na IA...")
            feedback_interno = None
        else:
            limpar_buffer_entrada()
            user_input = input("\nVocê 👤 >>> ")
            if user_input.strip().lower() in ['sair', 'exit', 'quit', '/bye']:
                print("\n🤖 [O.R.I.O.N.] Entrando em modo stand-by. Até logo, Senhor.")
                break
            
            if not user_input.strip():
                continue

        cursor.execute("INSERT INTO Conversations (role, message) VALUES (%s, %s)", ('user', user_input))
        cnx.commit()
        messages.append({"role": "user", "content": user_input})

        # Atualiza o prompt do sistema no array na memória a cada rodada (Consciência em tempo real)
        messages[0]["content"] = obter_prompt_sistema()

        # Gatilho manual para execução rápida dos núcleos
        if "revisa um plugin" in user_input.lower() or "revisar" in user_input.lower():
            print("\n🤖 [O.R.I.O.N.] Ativando arquitetura de múltiplos núcleos em paralelo...")
            diretorio_teste = "/media/astral/7DFD-F7FB/AI-O-Go" 
            print("\n⚙️ [Núcleo B] Disparando b.py (Varredura)...")
            subprocess.run(["python3", "b.py", diretorio_teste])
            print("\n⚙️ [Núcleo C] Disparando c.py (Auditoria)...")
            subprocess.run(["python3", "c.py"])
            print("\n📝 [SISTEMA] 'log.txt' gerado fisicamente no disco.")
            continue

        print("🤖 O.R.I.O.N. 🧠 >>> ", end="", flush=True)
        
        response_stream = ollama.chat(model='llama3', messages=messages, stream=True)
        full_response = ""
        for chunk in response_stream:
            content = chunk['message']['content']
            print(content, end="", flush=True)
            full_response += content
        print()

        # Captura de blocos
        comandos_bash = re.findall(r'```bash\s+(.*?)\s+```', full_response, re.DOTALL)
        queries_sql = re.findall(r'```sql\s+(.*?)\s+```', full_response, re.DOTALL)
        codigos_py = re.findall(r'```python\s+(.*?)\s+```', full_response, re.DOTALL)
        comandos_web = re.findall(r'```web\s+(.*?)\s+```', full_response, re.DOTALL)

        relatorio_execucao = ""
        teve_erro = False

        # Processar Bash
        for cmd in comandos_bash:
            cmd_clean = cmd.strip()
            print(f"\n\033[93m⚠️ [SOLICITAÇÃO BASH] Executar no terminal:\033[0m\n👉 {cmd_clean}")
            limpar_buffer_entrada()
            decisao = input("\033[91mPermitir? (S/N): \033[0m").strip().upper()
            if decisao == 'S':
                saida = executar_bash_real(cmd_clean)
                print(f"\033[92m[RETORNO DISCO]:\033[0m\n{saida}")
                relatorio_execucao += f"\n[Bash Executado]. Comando: {cmd_clean}\nRetorno: {saida}"
                if "error" in saida.lower() or "not found" in saida.lower() or "erro" in saida.lower():
                    teve_erro = True
            else:
                print("❌ Comando Rejeitado.")
                relatorio_execucao += f"\n[Bash Rejeitado pelo Usuário]: {cmd_clean}"

        # Processar SQL
        for query in queries_sql:
            query_clean = query.strip()
            print(f"\n\033[93m⚠️ [SOLICITAÇÃO SQL] Executar no MariaDB:\033[0m\n👉 {query_clean}")
            limpar_buffer_entrada()
            decisao = input("\033[91mPermitir? (S/N): \033[0m").strip().upper()
            if decisao == 'S':
                saida = executar_sql_real(query_clean)
                print(f"\033[92m[RETORNO MARIADB]:\033[0m\n{saida}")
                relatorio_execucao += f"\n[SQL Executado]. Query: {query_clean}\nRetorno: {saida}"
                if "erro" in saida.lower() or "error" in saida.lower():
                    teve_erro = True
            else:
                print("❌ Query Rejeitada.")
                relatorio_execucao += f"\n[SQL Rejeitado pelo Usuário]: {query_clean}"

        # Processar Python
        for py_code in codigos_py:
            py_clean = py_code.strip()
            print(f"\n\033[93m⚠️ [SOLICITAÇÃO PYTHON] Executar Script Dinâmico:\033[0m\n{py_clean}")
            limpar_buffer_entrada()
            decisao = input("\033[91mPermitir? (S/N): \033[0m").strip().upper()
            if decisao == 'S':
                saida = executar_python_real(py_clean)
                print(f"\033[92m[RETORNO SCRIPT]:\033[0m\n{saida}")
                relatorio_execucao += f"\n[Python Executado]. Retorno: {saida}"
                if "erro" in saida.lower() or "exception" in saida.lower() or "traceback" in saida.lower():
                    teve_erro = True
            else:
                print("❌ Execução Rejeitada.")
                relatorio_execucao += f"\n[Python Rejeitado pelo Usuário]"

        # Processar Web
        for url in comandos_web:
            url_clean = url.strip()
            print(f"\n\033[93m🌐 [PESQUISA WEB] O.R.I.O.N. está lendo o link:\033[0m {url_clean}")
            saida = pesquisar_web(url_clean)
            relatorio_execucao += f"\n[Pesquisa Web]. Link: {url_clean}\nConteúdo: {saida}"

        cursor.execute("INSERT INTO Conversations (role, message) VALUES (%s, %s)", ('assistant', full_response))
        cnx.commit()
        messages.append({"role": "assistant", "content": full_response})

        # Alimenta o loop de auto-correção
        if relatorio_execucao:
            feedback_interno = f"Retorno do Sistema Operacional após sua solicitação:\n{relatorio_execucao}\n"
            if teve_erro:
                feedback_interno += "Foi detectado um ERRO na execução. Analise o erro acima e gere um código corrigido imediatamente."

finally:
    cursor.close()
    cnx.close()
