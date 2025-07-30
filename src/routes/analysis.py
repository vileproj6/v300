#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Rotas de Análise
Endpoints para análise de mercado ultra-detalhada
"""

import os
import logging
import json
import time
from datetime import datetime
from flask import Blueprint, request, jsonify
from services.enhanced_analysis_engine import enhanced_analysis_engine
from services.attachment_service import attachment_service
from database import db_manager

logger = logging.getLogger(__name__)

# Cria blueprint
analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_market():
    """Endpoint principal para análise de mercado"""
    
    try:
        # Coleta dados do formulário
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Dados não fornecidos',
                'message': 'Envie os dados da análise no corpo da requisição'
            }), 400
        
        # Validação básica
        if not data.get('segmento'):
            return jsonify({
                'error': 'Segmento obrigatório',
                'message': 'O campo segmento é obrigatório para análise'
            }), 400
        
        logger.info(f"🚀 Iniciando análise para segmento: {data.get('segmento')}")
        start_time = time.time()
        
        # Gera análise usando o motor enhanced
        session_id = data.get('session_id')
        analysis_result = enhanced_analysis_engine.generate_comprehensive_analysis(data, session_id)
        
        # Salva no banco se disponível
        try:
            if analysis_result and db_manager.available:
                saved_analysis = db_manager.create_analysis(analysis_result)
                if saved_analysis:
                    analysis_result['database_id'] = saved_analysis['id']
                    logger.info(f"✅ Análise salva no banco com ID: {saved_analysis['id']}")
        except Exception as e:
            logger.warning(f"⚠️ Erro ao salvar no banco: {str(e)}")
            # Continua mesmo se não conseguir salvar no banco
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Adiciona metadados de processamento
        if 'metadata' not in analysis_result:
            analysis_result['metadata'] = {}
        
        analysis_result['metadata'].update({
            'processing_time_seconds': processing_time,
            'processing_time_formatted': f"{int(processing_time // 60)}m {int(processing_time % 60)}s",
            'endpoint': '/api/analyze',
            'timestamp': datetime.now().isoformat(),
            'success': True
        })
        
        logger.info(f"✅ Análise concluída em {processing_time:.2f} segundos")
        
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"❌ Erro na análise: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Erro interno na análise',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@analysis_bp.route('/upload_attachment', methods=['POST'])
def upload_attachment():
    """Endpoint para upload de anexos"""
    
    try:
        # Verifica se há arquivo
        if 'file' not in request.files:
            return jsonify({
                'error': 'Nenhum arquivo enviado',
                'message': 'Envie um arquivo no campo "file"'
            }), 400
        
        file = request.files['file']
        session_id = request.form.get('session_id', 'default_session')
        
        if file.filename == '':
            return jsonify({
                'error': 'Arquivo vazio',
                'message': 'Selecione um arquivo válido'
            }), 400
        
        logger.info(f"📎 Processando anexo: {file.filename}")
        
        # Processa arquivo
        result = attachment_service.process_attachment(file, session_id)
        
        if result['success']:
            logger.info(f"✅ Anexo processado: {file.filename}")
            return jsonify(result)
        else:
            logger.error(f"❌ Erro no anexo: {result.get('error')}")
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"❌ Erro no upload: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Erro no processamento do anexo',
            'message': str(e)
        }), 500

@analysis_bp.route('/analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Recupera análise por ID"""
    
    try:
        if not db_manager.available:
            return jsonify({
                'error': 'Banco de dados não disponível',
                'message': 'Configure o Supabase para usar esta funcionalidade'
            }), 503
        
        analysis = db_manager.get_analysis(analysis_id)
        
        if analysis:
            return jsonify(analysis)
        else:
            return jsonify({
                'error': 'Análise não encontrada',
                'message': f'Análise com ID {analysis_id} não existe'
            }), 404
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar análise {analysis_id}: {str(e)}")
        return jsonify({
            'error': 'Erro ao buscar análise',
            'message': str(e)
        }), 500

@analysis_bp.route('/analyses', methods=['GET'])
def list_analyses():
    """Lista análises com paginação"""
    
    try:
        if not db_manager.available:
            return jsonify({
                'error': 'Banco de dados não disponível',
                'message': 'Configure o Supabase para usar esta funcionalidade'
            }), 503
        
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        
        analyses = db_manager.list_analyses(limit, offset)
        
        return jsonify({
            'analyses': analyses,
            'limit': limit,
            'offset': offset,
            'count': len(analyses)
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar análises: {str(e)}")
        return jsonify({
            'error': 'Erro ao listar análises',
            'message': str(e)
        }), 500

@analysis_bp.route('/analysis/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    """Remove análise"""
    
    try:
        if not db_manager.available:
            return jsonify({
                'error': 'Banco de dados não disponível',
                'message': 'Configure o Supabase para usar esta funcionalidade'
            }), 503
        
        success = db_manager.delete_analysis(analysis_id)
        
        if success:
            return jsonify({
                'message': f'Análise {analysis_id} removida com sucesso'
            })
        else:
            return jsonify({
                'error': 'Falha ao remover análise',
                'message': f'Não foi possível remover análise {analysis_id}'
            }), 400
        
    except Exception as e:
        logger.error(f"❌ Erro ao remover análise {analysis_id}: {str(e)}")
        return jsonify({
            'error': 'Erro ao remover análise',
            'message': str(e)
        }), 500

@analysis_bp.route('/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas do sistema"""
    
    try:
        stats = db_manager.get_stats()
        
        # Adiciona informações do sistema
        system_info = {
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'database_available': db_manager.available
        }
        
        return jsonify({
            'database_stats': stats,
            'system_info': system_info
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter estatísticas',
            'message': str(e)
        }), 500

@analysis_bp.route('/validate', methods=['POST'])
def validate_analysis_data():
    """Valida dados antes da análise"""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'valid': False,
                'errors': ['Dados não fornecidos']
            }), 400
        
        errors = []
        warnings = []
        
        # Validações obrigatórias
        if not data.get('segmento'):
            errors.append('Segmento é obrigatório')
        
        # Validações opcionais com avisos
        if not data.get('produto'):
            warnings.append('Produto não informado - análise será mais genérica')
        
        if not data.get('publico'):
            warnings.append('Público-alvo não informado - avatar será mais genérico')
        
        if not data.get('preco'):
            warnings.append('Preço não informado - projeções financeiras serão limitadas')
        
        # Validações de formato
        if data.get('preco'):
            try:
                float(data['preco'])
            except (ValueError, TypeError):
                errors.append('Preço deve ser um número válido')
        
        if data.get('objetivo_receita'):
            try:
                float(data['objetivo_receita'])
            except (ValueError, TypeError):
                errors.append('Objetivo de receita deve ser um número válido')
        
        if data.get('orcamento_marketing'):
            try:
                float(data['orcamento_marketing'])
            except (ValueError, TypeError):
                errors.append('Orçamento de marketing deve ser um número válido')
        
        is_valid = len(errors) == 0
        
        return jsonify({
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Erro na validação: {str(e)}")
        return jsonify({
            'valid': False,
            'errors': [f'Erro interno: {str(e)}']
        }), 500

@analysis_bp.route('/preview', methods=['POST'])
def preview_analysis():
    """Gera preview da análise sem processamento completo"""
    
    try:
        data = request.get_json()
        
        if not data or not data.get('segmento'):
            return jsonify({
                'error': 'Dados insuficientes',
                'message': 'Segmento é obrigatório para preview'
            }), 400
        
        # Gera preview básico
        preview = {
            'segmento': data.get('segmento'),
            'produto': data.get('produto', 'Produto/Serviço'),
            'estimated_sections': [
                'Avatar Ultra-Detalhado',
                'Análise de Concorrência',
                'Estratégia de Posicionamento',
                'Palavras-Chave',
                'Métricas de Performance',
                'Plano de Ação',
                'Insights Exclusivos'
            ],
            'estimated_processing_time': '2-5 minutos',
            'estimated_pages': '15-25 páginas',
            'data_sources': [
                'Google Search',
                'Bing Search',
                'DuckDuckGo',
                'Análise com IA'
            ],
            'preview_generated_at': datetime.now().isoformat()
        }
        
        # Adiciona informações específicas baseadas nos dados
        if data.get('preco'):
            preview['financial_projections'] = True
        
        if data.get('concorrentes'):
            preview['competition_analysis'] = 'Detalhada'
        else:
            preview['competition_analysis'] = 'Genérica'
        
        if data.get('query'):
            preview['web_research'] = 'Personalizada'
        else:
            preview['web_research'] = 'Automática'
        
        return jsonify(preview)
        
    except Exception as e:
        logger.error(f"❌ Erro no preview: {str(e)}")
        return jsonify({
            'error': 'Erro ao gerar preview',
            'message': str(e)
        }), 500