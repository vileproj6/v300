#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Async Analysis Routes
Rotas para análise assíncrona e dashboard do usuário
"""

import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
from tasks.analysis_tasks import process_market_analysis, validate_apis
from celery.result import AsyncResult
from database import db_manager

logger = logging.getLogger(__name__)

async_bp = Blueprint('async', __name__)

@async_bp.route('/analyze_async', methods=['POST'])
def start_async_analysis():
    """Inicia análise assíncrona"""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Dados não fornecidos'
            }), 400
        
        # Validação básica
        if not data.get('segmento'):
            return jsonify({
                'error': 'Segmento é obrigatório'
            }), 400
        
        # Inicia task assíncrona
        task = process_market_analysis.delay(data)
        
        logger.info(f"🚀 Análise assíncrona iniciada: {task.id}")
        
        return jsonify({
            'task_id': task.id,
            'status': 'STARTED',
            'message': 'Análise iniciada com sucesso',
            'estimated_time': '5-15 minutos'
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar análise assíncrona: {str(e)}")
        return jsonify({
            'error': 'Erro interno',
            'message': str(e)
        }), 500

@async_bp.route('/task_status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Obtém status de uma task"""
    
    try:
        task = AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Aguardando processamento...',
                'current': 0,
                'total': 4
            }
        elif task.state == 'PROGRESS':
            response = {
                'task_id': task_id,
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 4),
                'status': task.info.get('status', ''),
                'phase': task.info.get('phase', '')
            }
        elif task.state == 'SUCCESS':
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Análise concluída com sucesso!',
                'result': task.result,
                'current': 4,
                'total': 4
            }
        else:  # FAILURE
            response = {
                'task_id': task_id,
                'state': task.state,
                'status': 'Erro no processamento',
                'error': str(task.info),
                'current': 0,
                'total': 4
            }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter status da task: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter status',
            'message': str(e)
        }), 500

@async_bp.route('/dashboard', methods=['GET'])
def user_dashboard():
    """Dashboard do usuário com histórico de análises"""
    
    try:
        # Parâmetros de paginação
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        
        if not db_manager.available:
            return jsonify({
                'error': 'Banco de dados não disponível'
            }), 503
        
        # Busca análises do usuário
        analyses = db_manager.list_analyses(limit, offset)
        
        # Estatísticas do usuário
        stats = db_manager.get_stats()
        
        # Tasks em andamento (simulado - em produção viria do Redis)
        active_tasks = get_active_tasks()
        
        return jsonify({
            'analyses': analyses,
            'stats': stats,
            'active_tasks': active_tasks,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'has_more': len(analyses) == limit
            }
        })
        
    except Exception as e:
        logger.error(f"❌ Erro no dashboard: {str(e)}")
        return jsonify({
            'error': 'Erro ao carregar dashboard',
            'message': str(e)
        }), 500

@async_bp.route('/analysis/<int:analysis_id>/download', methods=['GET'])
def download_analysis(analysis_id):
    """Download de análise específica"""
    
    try:
        if not db_manager.available:
            return jsonify({
                'error': 'Banco de dados não disponível'
            }), 503
        
        analysis = db_manager.get_analysis(analysis_id)
        
        if not analysis:
            return jsonify({
                'error': 'Análise não encontrada'
            }), 404
        
        # Formato solicitado
        format_type = request.args.get('format', 'json')
        
        if format_type == 'json':
            return jsonify(analysis)
        elif format_type == 'txt':
            return generate_txt_report(analysis)
        elif format_type == 'pdf':
            return generate_pdf_report(analysis)
        else:
            return jsonify({
                'error': 'Formato não suportado'
            }), 400
        
    except Exception as e:
        logger.error(f"❌ Erro no download: {str(e)}")
        return jsonify({
            'error': 'Erro no download',
            'message': str(e)
        }), 500

@async_bp.route('/validate_apis', methods=['POST'])
def validate_api_keys():
    """Valida todas as chaves de API"""
    
    try:
        # Inicia validação assíncrona
        task = validate_apis.delay()
        
        return jsonify({
            'task_id': task.id,
            'message': 'Validação de APIs iniciada'
        })
        
    except Exception as e:
        logger.error(f"❌ Erro na validação de APIs: {str(e)}")
        return jsonify({
            'error': 'Erro na validação',
            'message': str(e)
        }), 500

def get_active_tasks():
    """Obtém tasks ativas (simulado)"""
    # Em produção, isso viria do Redis/Celery
    return [
        {
            'task_id': 'example_task_1',
            'status': 'PROGRESS',
            'phase': 'data_collection',
            'progress': 60,
            'started_at': datetime.now().isoformat()
        }
    ]

def generate_txt_report(analysis):
    """Gera relatório em formato TXT"""
    from flask import Response
    
    txt_content = f"""
ARQV30 Enhanced v2.0 - Relatório de Análise de Mercado
========================================================

Análise ID: {analysis.get('id', 'N/A')}
Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

SEGMENTO: {analysis.get('nicho', 'N/A')}
PRODUTO: {analysis.get('produto', 'N/A')}
PREÇO: R$ {analysis.get('preco', 'N/A')}

AVATAR ULTRA-DETALHADO:
{format_avatar_for_txt(analysis.get('avatar_data', {}))}

INSIGHTS EXCLUSIVOS:
{format_insights_for_txt(analysis.get('comprehensive_analysis', {}).get('insights_exclusivos', []))}

========================================================
Relatório gerado pelo ARQV30 Enhanced v2.0
"""
    
    return Response(
        txt_content,
        mimetype='text/plain',
        headers={
            'Content-Disposition': f'attachment; filename=analise_{analysis.get("id", "unknown")}.txt'
        }
    )

def generate_pdf_report(analysis):
    """Gera relatório em formato PDF"""
    from routes.pdf_generator import pdf_generator
    from flask import send_file
    import tempfile
    
    try:
        # Gera PDF
        pdf_buffer = pdf_generator.generate_analysis_report(analysis)
        
        # Salva arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_buffer.getvalue())
            tmp_file_path = tmp_file.name
        
        return send_file(
            tmp_file_path,
            as_attachment=True,
            download_name=f"analise_{analysis.get('id', 'unknown')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {str(e)}")
        return jsonify({'error': 'Erro ao gerar PDF'}), 500

def format_avatar_for_txt(avatar_data):
    """Formata dados do avatar para TXT"""
    if not avatar_data:
        return "Dados não disponíveis"
    
    perfil = avatar_data.get('perfil_demografico', {})
    dores = avatar_data.get('dores_principais', [])
    
    txt = f"""
Perfil Demográfico:
- Idade: {perfil.get('idade', 'N/A')}
- Renda: {perfil.get('renda', 'N/A')}
- Localização: {perfil.get('localizacao', 'N/A')}

Principais Dores:
"""
    
    for i, dor in enumerate(dores, 1):
        txt += f"{i}. {dor}\n"
    
    return txt

def format_insights_for_txt(insights):
    """Formata insights para TXT"""
    if not insights:
        return "Nenhum insight disponível"
    
    txt = ""
    for i, insight in enumerate(insights, 1):
        txt += f"{i}. {insight}\n"
    
    return txt