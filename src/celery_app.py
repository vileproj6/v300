#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Celery Configuration
Configuração do Celery para processamento assíncrono
"""

import os
from celery import Celery
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do Celery
celery_app = Celery(
    'arqv30_enhanced',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    include=['tasks.analysis_tasks']
)

# Configurações do Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60,  # 25 minutos
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    result_expires=3600,  # 1 hora
    task_routes={
        'tasks.analysis_tasks.process_market_analysis': {'queue': 'analysis'},
        'tasks.analysis_tasks.validate_apis': {'queue': 'validation'},
    }
)

if __name__ == '__main__':
    celery_app.start()