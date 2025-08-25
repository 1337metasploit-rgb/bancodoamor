import os
import subprocess
import sys

def criar_estrutura_projeto():
    """Cria a estrutura de pastas do projeto"""
    pastas = ['static', 'templates']
    
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"✅ Pasta '{pasta}' criada!")

def instalar_dependencias():
    """Instala as dependências automaticamente"""
    try:
        print("📦 Instalando dependências...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências. Execute manualmente: pip install -r requirements.txt")

def main():
    print("🌈💖 CONFIGURAÇÃO DO BANCO LUIS & MACHADO")
    print("=" * 50)
    
    criar_estrutura_projeto()
    
    resposta = input("\n📦 Deseja instalar as dependências automaticamente? (s/n): ")
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        instalar_dependencias()
    
    print("\n🎉 Configuração concluída!")
    print("🚀 Para iniciar o sistema, execute: python app.py")
    print("📍 Depois acesse: http://localhost:5000")

if __name__ == "__main__":
    main()