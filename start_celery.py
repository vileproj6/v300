#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Celery Starter
Script para iniciar workers do Celery
"""

import os
import sys
import subprocess
import logging
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def start_celery_worker():
    """Inicia worker do Celery"""
    
    print("🚀 Iniciando Celery Worker...")
    
    # Comando para iniciar worker
    cmd = [
        'celery', '-A', 'src.celery_app', 'worker',
        '--loglevel=info',
        '--concurrency=2',
        '--queues=analysis,validation',
        '--hostname=worker@%h'
    ]
    
    try:
        # Inicia worker
        subprocess.run(cmd, cwd=os.getcwd())
        
    except KeyboardInterrupt:
        print("\n🛑 Parando Celery Worker...")
    except Exception as e:
        print(f"❌ Erro ao iniciar Celery Worker: {e}")

def start_celery_flower():
    """Inicia Flower para monitoramento"""
    
    print("🌸 Iniciando Flower...")
    
    cmd = [
        'celery', '-A', 'src.celery_app', 'flower',
        '--port=5555'
    ]
    
    try:
        subprocess.run(cmd, cwd=os.getcwd())
        
    except KeyboardInterrupt:
        print("\n🛑 Parando Flower...")
    except Exception as e:
        print(f"❌ Erro ao iniciar Flower: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'flower':
        start_celery_flower()
    else:
        start_celery_worker()