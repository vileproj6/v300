@@ .. @@
 ## 🚀 Como Usar

+### Modo Assíncrono (Recomendado)
+
+1. **Inicie o Redis** (necessário para processamento assíncrono):
+   ```bash
+   # Linux/Mac
+   redis-server
+   
+   # Windows (se instalado)
+   redis-server.exe
+   ```
+
+2. **Inicie o Celery Worker**:
+   ```bash
+   # Linux/Mac
+   python start_celery.py
+   
+   # Windows
+   start_celery.bat
+   ```
+
+3. **Inicie a aplicação**:
+   ```bash
+   python src/run.py
+   ```
+
+4. **Acesse**: http://localhost:5000
+   - Use o botão "Análise Assíncrona" para processamento em segundo plano
+   - Monitore o progresso em tempo real
+   - Acesse o dashboard para ver histórico e downloads
+
+### Modo Síncrono (Tradicional)
+
 1. **Execute a instalação**:
    ```bash
    # Linux/Mac
@@ .. @@
 
 4. **Acesse**: http://localhost:5000
 
+### Monitoramento
+
+- **Flower** (monitoramento Celery): http://localhost:5555
+- **Dashboard do usuário**: Integrado na aplicação principal
+
 ## 📊 Funcionalidades
 
 ### ✨ Análise Ultra-Detalhada
@@ -75,6 +108,15 @@ python src/run.py
 - **Métricas de Performance**: KPIs e projeções financeiras
 - **Plano de Ação**: Roadmap detalhado de 90 dias
 
+### 🚀 Processamento Assíncrono
+- **Análise em segundo plano**: Não trava a interface
+- **Progresso em tempo real**: 4 fases com status detalhado
+- **Dashboard interativo**: Visualização rica dos resultados
+- **Múltiplos formatos**: Download em TXT, PDF e JSON
+- **Cache inteligente**: Reutiliza dados para análises similares
+- **Fallback automático**: Gemini → Groq → Análise básica
+- **Validação de APIs**: Verifica chaves no startup
+
 ### 🔍 Pesquisa Profunda REAL
 - **Múltiplos Provedores**: Google, Bing, DuckDuckGo
 - **Extração Inteligente**: Jina AI + BeautifulSoup