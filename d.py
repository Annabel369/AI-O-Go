#!/usr/bin/env python3
import subprocess
import os
import shutil

def compilar_e_instalar():
    path_projeto = "/home/astral/SolanaDevMinecraftForge1.20.1"
    path_mods_prism = "/home/astral/.var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher/instances/1.20.1/minecraft/mods"
    
    print("🛠️ [Núcleo D] Executando Gradle Build para Forge 1.20.1...")
    
    # Executa o compilador do Gradle nativo do projeto Forge
    os.chdir(path_projeto)
    # Dá permissão ao gradlew se necessário
    subprocess.run(["chmod", "+x", "./gradlew"], capture_output=True)
    res = subprocess.run(["./gradlew", "build"], capture_output=True, text=True)
    
    if res.returncode == 0:
        print("✅ [Núcleo D] Mod compilado com sucesso pelo Gradle!")
        
        # Encontra o arquivo .jar gerado na pasta build/libs
        pasta_libs = os.path.join(path_projeto, "build", "libs")
        if os.path.exists(pasta_libs):
            jars = [x for x in os.listdir(pasta_libs) if x.endswith(".jar") and not x.endswith("-sources.jar")]
            if jars:
                jar_final = os.path.join(pasta_libs, jars[0])
                print(f"📦 Movendo {jars[0]} para a pasta de mods do PrismLauncher...")
                os.makedirs(path_mods_prism, exist_ok=True)
                shutil.copy(jar_final, os.path.join(path_mods_prism, jars[0]))
                print("🚀 [Núcleo D] Deploy concluído! Pronto para iniciar o Minecraft no Launcher.")
                return
        print("⚠️ [Núcleo D] Build concluído, mas o arquivo .jar não foi localizado em build/libs.")
    else:
        print(f"❌ [Núcleo D] Falha na compilação do Forge:\n{res.stderr}")

if __name__ == "__main__":
    compilar_e_instalar()
