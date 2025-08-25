import subprocess
import webbrowser
import time
import sys
from database import init_db

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    try:
        import flask
        return True
    except ImportError:
        print("❌ Flask não encontrado!")
        print("📦 Execute: pip install -r requirements.txt")
        return False

def main():
    print("🌈💖 BANCO LUIS & MACHADO")
    print("=" * 40)
    
    if not verificar_dependencias():
        return
    
    # Inicializa o banco de dados
    print("🗄️ Inicializando banco de dados...")
    init_db()
    
    print("🚀 Iniciando servidor...")
    print("📍 URL: http://localhost:5000")
    print("⏹️ Para parar: Ctrl+C")
    print("=" * 40)
    
    # Abre o navegador automaticamente
    time.sleep(2)
    webbrowser.open('http://localhost:5000')
    
    # Executa a aplicação
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado!")

if __name__ == "__main__":
    main()