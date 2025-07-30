#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Analysis Tasks
Tasks assíncronas para processamento de análises
"""

import os
import sys
import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, List
from celery import current_task
from celery_app import celery_app

# Adiciona src ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.ai_manager import ai_manager
from services.production_search_manager import production_search_manager
from services.production_content_extractor import production_content_extractor
from services.groq_client import groq_client
from database import db_manager

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def process_market_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processa análise de mercado de forma assíncrona com progresso em tempo real
    """
    try:
        task_id = self.request.id
        logger.info(f"🚀 Iniciando análise assíncrona: {task_id}")
        
        # Fase 1: Validação e preparação (10%)
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 1,
                'total': 4,
                'status': 'Validando dados e preparando análise...',
                'phase': 'validation'
            }
        )
        
        # Valida dados de entrada
        if not analysis_data.get('segmento'):
            raise ValueError("Segmento é obrigatório")
        
        time.sleep(2)  # Simula processamento
        
        # Fase 2: Coleta de dados (40%)
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 2,
                'total': 4,
                'status': 'Coletando dados da web com busca inteligente...',
                'phase': 'data_collection'
            }
        )
        
        # Executa busca limitada (máximo 2 rodadas)
        search_results = perform_limited_search(analysis_data)
        
        # Fase 3: Análise com IA (30%)
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 3,
                'total': 4,
                'status': 'Processando com Inteligência Artificial...',
                'phase': 'ai_analysis'
            }
        )
        
        # Tenta Gemini primeiro, depois Groq como fallback
        analysis_result = perform_ai_analysis_with_fallback(analysis_data, search_results)
        
        # Fase 4: Finalização (20%)
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 4,
                'total': 4,
                'status': 'Finalizando relatório e salvando resultados...',
                'phase': 'finalization'
            }
        )
        
        # Salva no banco de dados
        if db_manager.available:
            saved_analysis = db_manager.create_analysis(analysis_result)
            if saved_analysis:
                analysis_result['database_id'] = saved_analysis['id']
        
        # Adiciona metadados da task
        analysis_result['task_metadata'] = {
            'task_id': task_id,
            'processed_at': datetime.now().isoformat(),
            'processing_mode': 'async',
            'search_rounds': len(search_results.get('rounds', [])),
            'ai_provider_used': analysis_result.get('ai_provider', 'unknown')
        }
        
        logger.info(f"✅ Análise assíncrona concluída: {task_id}")
        return analysis_result
        
    except Exception as e:
        logger.error(f"❌ Erro na análise assíncrona: {str(e)}", exc_info=True)
        self.update_state(
            state='FAILURE',
            meta={
                'error': str(e),
                'phase': 'error'
            }
        )
        raise

def perform_limited_search(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Executa busca limitada a 2 rodadas máximo"""
    
    search_results = {
        'rounds': [],
        'total_results': 0,
        'extracted_content': []
    }
    
    # Gera queries de busca otimizadas
    queries = generate_optimized_queries(analysis_data)
    
    # Máximo 2 rodadas de busca
    for round_num, query in enumerate(queries[:2], 1):
        logger.info(f"🔍 Rodada {round_num}/2: {query}")
        
        try:
            # Busca com múltiplos provedores
            results = production_search_manager.search_with_fallback(query, max_results=10)
            
            if results:
                # Extrai conteúdo das top 5 páginas
                extracted = []
                for result in results[:5]:
                    content = production_content_extractor.extract_content(result.url)
                    if content:
                        extracted.append({
                            'url': result.url,
                            'title': result.title,
                            'content': content[:3000],  # Limita tamanho
                            'source': result.source
                        })
                
                search_results['rounds'].append({
                    'round': round_num,
                    'query': query,
                    'results_count': len(results),
                    'extracted_count': len(extracted)
                })
                
                search_results['extracted_content'].extend(extracted)
                search_results['total_results'] += len(results)
                
                logger.info(f"✅ Rodada {round_num}: {len(results)} resultados, {len(extracted)} extraídos")
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            logger.error(f"❌ Erro na rodada {round_num}: {str(e)}")
            continue
    
    return search_results

def generate_optimized_queries(analysis_data: Dict[str, Any]) -> List[str]:
    """Gera queries otimizadas para busca"""
    
    segmento = analysis_data.get('segmento', '')
    produto = analysis_data.get('produto', '')
    
    queries = []
    
    # Query principal
    if produto:
        queries.append(f"mercado {segmento} {produto} Brasil 2024 análise tendências")
    else:
        queries.append(f"mercado {segmento} Brasil 2024 análise oportunidades")
    
    # Query de concorrência
    queries.append(f"concorrentes {segmento} Brasil principais empresas market share")
    
    # Query personalizada do usuário
    if analysis_data.get('query'):
        queries.append(analysis_data['query'])
    
    return queries[:2]  # Máximo 2 queries

def perform_ai_analysis_with_fallback(analysis_data: Dict[str, Any], search_results: Dict[str, Any]) -> Dict[str, Any]:
    """Executa análise com IA usando Gemini primeiro, Groq como fallback"""
    
    # Prepara contexto de busca usando MapReduce
    search_context = prepare_mapreduce_context(search_results)
    
    # Constrói prompt otimizado
    prompt = build_optimized_prompt(analysis_data, search_context)
    
    # Tenta Gemini primeiro
    try:
        logger.info("🤖 Tentando análise com Gemini...")
        ai_response = ai_manager.generate_analysis(prompt, max_tokens=8192)
        
        if ai_response and len(ai_response) > 500:
            logger.info("✅ Análise concluída com Gemini")
            result = process_ai_response(ai_response, analysis_data)
            result['ai_provider'] = 'gemini'
            return result
        else:
            raise Exception("Resposta insuficiente do Gemini")
            
    except Exception as e:
        logger.warning(f"⚠️ Gemini falhou: {str(e)}")
        
        # Fallback para Groq
        try:
            logger.info("🔄 Tentando fallback com Groq...")
            
            if groq_client.is_available():
                groq_response = groq_client.generate_analysis(prompt, max_tokens=8192)
                
                if groq_response and len(groq_response) > 500:
                    logger.info("✅ Análise concluída com Groq")
                    result = process_ai_response(groq_response, analysis_data)
                    result['ai_provider'] = 'groq'
                    return result
                else:
                    raise Exception("Resposta insuficiente do Groq")
            else:
                raise Exception("Groq não disponível")
                
        except Exception as groq_error:
            logger.error(f"❌ Groq também falhou: {str(groq_error)}")
            
            # Fallback final - análise básica
            return generate_fallback_analysis(analysis_data, search_results)

def prepare_mapreduce_context(search_results: Dict[str, Any]) -> str:
    """Prepara contexto usando abordagem MapReduce"""
    
    extracted_content = search_results.get('extracted_content', [])
    
    if not extracted_content:
        return "Nenhum conteúdo extraído disponível."
    
    # Map: Resume cada artigo individualmente
    summaries = []
    
    for i, content_item in enumerate(extracted_content[:10], 1):  # Máximo 10 artigos
        try:
            # Resume cada artigo
            article_summary = f"""
FONTE {i}: {content_item['title']}
URL: {content_item['url']}
RESUMO: {content_item['content'][:1000]}...
"""
            summaries.append(article_summary)
            
        except Exception as e:
            logger.warning(f"Erro ao processar artigo {i}: {str(e)}")
            continue
    
    # Reduce: Combina resumos
    combined_context = f"""
PESQUISA REALIZADA - {len(summaries)} FONTES ANALISADAS:

{chr(10).join(summaries)}

ESTATÍSTICAS DA PESQUISA:
- Total de rodadas: {len(search_results.get('rounds', []))}
- Total de resultados: {search_results.get('total_results', 0)}
- Conteúdo extraído: {len(extracted_content)} páginas
"""
    
    return combined_context[:15000]  # Limita tamanho total

def build_optimized_prompt(analysis_data: Dict[str, Any], search_context: str) -> str:
    """Constrói prompt otimizado para análise"""
    
    return f"""
# ANÁLISE ULTRA-DETALHADA DE MERCADO - ARQV30 ENHANCED v2.0

Você é um especialista em análise de mercado. Gere uma análise completa em formato JSON.

## DADOS DO PROJETO:
- Segmento: {analysis_data.get('segmento', 'Não informado')}
- Produto: {analysis_data.get('produto', 'Não informado')}
- Preço: R$ {analysis_data.get('preco', 'Não informado')}
- Público: {analysis_data.get('publico', 'Não informado')}

## CONTEXTO DE PESQUISA:
{search_context[:10000]}

## INSTRUÇÕES:
Gere uma análise em formato JSON com as seguintes seções:

```json
{{
  "avatar_ultra_detalhado": {{
    "perfil_demografico": {{
      "idade": "Faixa etária específica",
      "renda": "Faixa de renda mensal",
      "localizacao": "Principais regiões"
    }},
    "dores_principais": ["Lista de 5-8 dores específicas"],
    "desejos_principais": ["Lista de 5-8 desejos específicos"]
  }},
  "analise_concorrencia": [
    {{
      "nome": "Nome do concorrente",
      "forcas": ["Principais forças"],
      "fraquezas": ["Principais fraquezas"]
    }}
  ],
  "estrategia_palavras_chave": {{
    "primarias": ["5-10 palavras-chave principais"],
    "secundarias": ["10-15 palavras-chave secundárias"]
  }},
  "insights_exclusivos": [
    "Lista de 10-15 insights únicos e valiosos"
  ],
  "plano_acao": {{
    "fase_1": {{
      "duracao": "30 dias",
      "atividades": ["Lista de atividades específicas"]
    }},
    "fase_2": {{
      "duracao": "60 dias", 
      "atividades": ["Lista de atividades específicas"]
    }}
  }}
}}
```

IMPORTANTE: Responda APENAS com o JSON válido, sem texto adicional.
"""

def process_ai_response(ai_response: str, original_data: Dict[str, Any]) -> Dict[str, Any]:
    """Processa resposta da IA"""
    try:
        # Limpa resposta
        clean_text = ai_response.strip()
        
        if "```json" in clean_text:
            start = clean_text.find("```json") + 7
            end = clean_text.rfind("```")
            clean_text = clean_text[start:end].strip()
        elif "```" in clean_text:
            start = clean_text.find("```") + 3
            end = clean_text.rfind("```")
            clean_text = clean_text[start:end].strip()
        
        # Parse JSON
        analysis = json.loads(clean_text)
        
        # Adiciona metadados
        analysis['metadata'] = {
            'generated_at': datetime.now().isoformat(),
            'processing_mode': 'async',
            'version': '2.0.0'
        }
        
        return analysis
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ Erro ao parsear JSON: {str(e)}")
        return generate_fallback_analysis(original_data, {})

def generate_fallback_analysis(analysis_data: Dict[str, Any], search_results: Dict[str, Any]) -> Dict[str, Any]:
    """Gera análise de fallback quando IA falha"""
    
    segmento = analysis_data.get('segmento', 'Negócios')
    
    return {
        "avatar_ultra_detalhado": {
            "perfil_demografico": {
                "idade": "25-45 anos",
                "renda": "R$ 3.000 - R$ 15.000",
                "localizacao": "Grandes centros urbanos"
            },
            "dores_principais": [
                f"Dificuldades no mercado de {segmento}",
                "Concorrência acirrada",
                "Falta de diferenciação"
            ],
            "desejos_principais": [
                "Crescimento sustentável",
                "Reconhecimento no mercado",
                "Liberdade financeira"
            ]
        },
        "insights_exclusivos": [
            f"Mercado de {segmento} em transformação",
            "Oportunidades digitais crescentes",
            "⚠️ Análise gerada em modo fallback - IAs indisponíveis"
        ],
        "ai_provider": "fallback",
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "processing_mode": "async_fallback",
            "note": "Análise básica - IAs indisponíveis"
        }
    }

@celery_app.task
def validate_apis() -> Dict[str, Any]:
    """Valida todas as chaves de API"""
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'apis': {}
    }
    
    # Valida Gemini
    try:
        if ai_manager.providers['gemini']['available']:
            test_result = ai_manager._generate_with_gemini("Teste", 10)
            results['apis']['gemini'] = {
                'available': bool(test_result),
                'status': 'OK' if test_result else 'FAILED'
            }
        else:
            results['apis']['gemini'] = {
                'available': False,
                'status': 'NOT_CONFIGURED'
            }
    except Exception as e:
        results['apis']['gemini'] = {
            'available': False,
            'status': f'ERROR: {str(e)}'
        }
    
    # Valida Groq
    try:
        if groq_client.is_available():
            test_result = groq_client.test_connection()
            results['apis']['groq'] = {
                'available': test_result,
                'status': 'OK' if test_result else 'FAILED'
            }
        else:
            results['apis']['groq'] = {
                'available': False,
                'status': 'NOT_CONFIGURED'
            }
    except Exception as e:
        results['apis']['groq'] = {
            'available': False,
            'status': f'ERROR: {str(e)}'
        }
    
    # Valida Google Search
    try:
        google_key = os.getenv('GOOGLE_SEARCH_KEY')
        google_cse = os.getenv('GOOGLE_CSE_ID')
        
        if google_key and google_cse:
            # Testa busca simples
            test_results = production_search_manager.search_google_custom("teste", 1)
            results['apis']['google_search'] = {
                'available': len(test_results) > 0,
                'status': 'OK' if test_results else 'FAILED'
            }
        else:
            results['apis']['google_search'] = {
                'available': False,
                'status': 'NOT_CONFIGURED'
            }
    except Exception as e:
        results['apis']['google_search'] = {
            'available': False,
            'status': f'ERROR: {str(e)}'
        }
    
    # Valida HuggingFace
    try:
        hf_key = os.getenv('HUGGINGFACE_API_KEY')
        if hf_key:
            results['apis']['huggingface'] = {
                'available': True,
                'status': 'CONFIGURED'
            }
        else:
            results['apis']['huggingface'] = {
                'available': False,
                'status': 'NOT_CONFIGURED'
            }
    except Exception as e:
        results['apis']['huggingface'] = {
            'available': False,
            'status': f'ERROR: {str(e)}'
        }
    
    return results