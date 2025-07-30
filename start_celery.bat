@echo off
REM ARQV30 Enhanced v2.0 - Celery Starter para Windows

echo ========================================
echo ARQV30 Enhanced v2.0 - Celery Worker
echo ========================================
echo.

REM Ativa ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo 🔄 Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

REM Verifica se Celery está instalado
python -c "import celery" >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Celery não encontrado!
    echo Execute: pip install celery redis
    pause
    exit /b 1
)

REM Verifica se Redis está rodando
echo 🔍 Verificando Redis...
python -c "import redis; r=redis.Redis(); r.ping()" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ AVISO: Redis não encontrado!
    echo Instale e inicie o Redis para usar processamento assíncrono
    echo.
)

echo 🚀 Iniciando Celery Worker...
echo.
echo 📊 Monitoramento: http://localhost:5555 (Flower)
echo 🛑 Para parar: Ctrl+C
echo.

REM Inicia worker
celery -A src.celery_app worker --loglevel=info --concurrency=2 --queues=analysis,validation

pause