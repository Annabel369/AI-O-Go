#!/usr/bin/env python3
import mysql.connector
import ollama

def analisar_codigo_e_logs():
    try:
        cnx = mysql.connector.connect(user='root', password='0073007', host='localhost', database='ChatbotDB')
        cursor = cnx.cursor()
        cursor.execute("SELECT id, nome, caminho, linguagem FROM PluginAnalise WHERE status='pendente'")
        itens = cursor.fetchall()
        
        if not itens:
            print("🧠 [Núcleo C] Sem novos arquivos pendentes.")
            return

        # Captura os erros do log primeiro para ter contexto de IA
        contexto_erros = ""
        log_item = [x for x in itens if x[2] == "Minecraft Log"]
        if log_item:
            try:
                with open(log_item[0][2], 'r', encoding='utf-8', errors='ignore') as f:
                    # Pega as últimas 100 linhas do log (onde geralmente estão as stacktraces do comando /soltransfere)
                    contexto_erros = "\n".join(f.readlines()[-100:])
            except:
                pass

        print("🧠 [Núcleo C] Iniciando auditoria cruzada (Código vs Erros do PrismLauncher)...")
        with open('log.txt', 'w', encoding='utf-8') as log_file:
            log_file.write("=== RELATÓRIO TÉCNICO DE AUDITORIA: COMANDO /SOLTRANSFERE ===\n\n")
            
            for p_id, nome, caminho, lang in itens:
                if lang == "Minecraft Log":
                    continue
                
                with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo = f.read()
                
                # Só processa arquivos que tenham relação com a lógica que você citou
                if "soltransfere" in conteudo.lower() or "solana" in conteudo.lower() or lang == "Web/PHP/JS":
                    print(f"🔍 Avaliando impacto em: {nome}")
                    
                    prompt = (
                        f"Você é o núcleo especialista do O.R.I.O.N. Analise o arquivo '{nome}' ({lang}).\n"
                        f"O usuário reportou falhas no comando '/soltransfere'.\n"
                        f"Últimos erros do Prism Launcher:\n{contexto_erros}\n\n"
                        f"Código do arquivo:\n{conteudo[:2500]}\n\n"
                        f"Gere uma lista objetiva de onde corrigir e como melhorar a integração Web-Mod."
                    )
                    
                    response = ollama.chat(model='llama3', messages=[{"role": "user", "content": prompt}])
                    diagnostico = response['message']['content']
                    
                    log_file.write(f"📁 Arquivo: {caminho}\n")
                    log_file.write(f"🧬 Linguagem/Contexto: {lang}\n")
                    log_file.write(f"📝 Diagnóstico e Correção:\n{diagnostico}\n")
                    log_file.write("-" * 60 + "\n\n")
                
                cursor.execute("UPDATE PluginAnalise SET status='analisado' WHERE id=%s", (p_id,))
                
        cnx.commit()
        cursor.close()
        cnx.close()
        print("🧠 [Núcleo C] Auditoria consolidada no arquivo 'log.txt'.")
    except Exception as e:
        print(f"❌ Erro no Núcleo C: {e}")

if __name__ == "__main__":
    analisar_codigo_e_logs()
