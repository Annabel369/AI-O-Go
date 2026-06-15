#!/usr/bin/env python3
import os
import sys
import mysql.connector

def mapear_projeto_completo():
    try:
        cnx = mysql.connector.connect(user='root', password='0073007', host='localhost', database='ChatbotDB')
        cursor = cnx.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PluginAnalise (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255),
                caminho TEXT,
                linguagem VARCHAR(50),
                status VARCHAR(50) DEFAULT 'pendente'
            )
        """)
        cursor.execute("TRUNCATE TABLE PluginAnalise")
        
        # Mapeamento do Mod (Forge 1.20.1)
        dir_mod = "/home/astral/SolanaDevMinecraftForge1.20.1"
        print(f"⚙️ [Núcleo B] Indexando código do Mod Forge...")
        for root, _, files in os.walk(dir_mod):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.java', '.toml', '.kt']:
                    cursor.execute("INSERT INTO PluginAnalise (nome, caminho, linguagem) VALUES (%s, %s, %s)",
                                   (file, os.path.join(root, file), 'Java/Forge'))

        # Mapeamento do Diretório Web
        dir_web = "/var/www/html/web_sol"
        print(f"⚙️ [Núcleo B] Indexando código do painel Web...")
        if os.path.exists(dir_web):
            for root, _, files in os.walk(dir_web):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in ['.php', '.js', '.json', '.html']:
                        cursor.execute("INSERT INTO PluginAnalise (nome, caminho, linguagem) VALUES (%s, %s, %s)",
                                       (file, os.path.join(root, file), 'Web/PHP/JS'))

        # Captura do Log de Erro mais recente do Prism Launcher
        dir_logs = "/home/astral/.var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher/instances/1.20.1/minecraft"
        log_latest = os.path.join(dir_logs, "logs", "latest.log")
        if os.path.exists(log_latest):
            print(f"⚙️ [Núcleo B] Log de execução detectado e adicionado à fila.")
            cursor.execute("INSERT INTO Conversations (role, message) VALUES (%s, %s)", 
                           ('system', f"[SISTEMA LOG CRÍTICO]: Arquivo de log capturado em {log_latest}"))
            # Adiciona o próprio arquivo de log para ser analisado pelo núcleo C
            cursor.execute("INSERT INTO PluginAnalise (nome, caminho, linguagem, status) VALUES (%s, %s, %s, %s)",
                           ("latest.log", log_latest, "Minecraft Log", "pendente"))

        cnx.commit()
        cursor.close()
        cnx.close()
        print("⚙️ [Núcleo B] Mapeamento de ambiente concluído com sucesso.")
    except Exception as e:
        print(f"❌ Erro no Núcleo B: {e}")

if __name__ == "__main__":
    mapear_projeto_completo()
