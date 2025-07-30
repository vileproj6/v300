#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Configuração do Banco de Dados
Integração com Supabase PostgreSQL
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from supabase.client import create_client, Client
import json

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de conexão e operações com Supabase"""
    
    def __init__(self):
        """Inicializa conexão com Supabase"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        # Verifica se as credenciais estão configuradas
        self.available = bool(self.supabase_url and self.supabase_key)
        
        if not self.available:
            logger.warning("⚠️ Credenciais do Supabase não configuradas - Banco de dados indisponível")
            self.client = None
            self.admin_client = None
            return
        
        # Cliente principal (anon key)
        try:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
            # Testa conexão básica
            test_result = self.client.table('analyses').select('id').limit(1).execute()
            logger.info("✅ Conexão com Supabase testada com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro ao criar cliente Supabase: {str(e)}")
            self.available = False
            self.client = None
            self.admin_client = None
            return
        
        # Cliente admin (service role)
        if self.service_role_key:
            try:
                self.admin_client: Client = create_client(self.supabase_url, self.service_role_key)
                logger.info("✅ Cliente admin Supabase inicializado")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao criar cliente admin Supabase: {str(e)}")
                self.admin_client = self.client
        else:
            self.admin_client = self.client
        
        if self.available:
            logger.info("✅ DatabaseManager inicializado com Supabase")
        else:
            logger.warning("⚠️ DatabaseManager inicializado sem banco de dados")
    
    def test_connection(self) -> bool:
        """Testa conexão com o banco"""
        if not self.available or not self.client:
            return False
            
        try:
            # Tenta fazer uma query simples
            result = self.client.table('analyses').select('id').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Erro ao testar conexão: {str(e)}")
            return False
    
    def create_analysis(self, analysis_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria nova análise no banco"""
        if not self.available or not self.client:
            logger.warning("⚠️ Banco de dados não disponível - análise não será salva")
            return None
            
        try:
            # Prepara dados para inserção
            insert_data = {
                'nicho': analysis_data.get('segmento', ''),
                'produto': analysis_data.get('produto', ''),
                'descricao': analysis_data.get('descricao', ''),
                'preco': float(analysis_data.get('preco', 0)) if analysis_data.get('preco') and str(analysis_data.get('preco')).replace('.', '').isdigit() else None,
                'publico': analysis_data.get('publico', ''),
                'concorrentes': analysis_data.get('concorrentes', ''),
                'dados_adicionais': analysis_data.get('dados_adicionais', ''),
                'objetivo_receita': float(analysis_data.get('objetivo_receita', 0)) if analysis_data.get('objetivo_receita') and str(analysis_data.get('objetivo_receita')).replace('.', '').isdigit() else None,
                'orcamento_marketing': float(analysis_data.get('orcamento_marketing', 0)) if analysis_data.get('orcamento_marketing') and str(analysis_data.get('orcamento_marketing')).replace('.', '').isdigit() else None,
                'prazo_lancamento': analysis_data.get('prazo_lancamento', ''),
                'status': analysis_data.get('status', 'completed'),
                'avatar_data': json.dumps(analysis_data.get('avatar_ultra_detalhado', {}), ensure_ascii=False) if analysis_data.get('avatar_ultra_detalhado') else None,
                'positioning_data': json.dumps(analysis_data.get('estrategia_posicionamento', {}), ensure_ascii=False) if analysis_data.get('estrategia_posicionamento') else None,
                'competition_data': json.dumps(analysis_data.get('analise_concorrencia_profunda', {}), ensure_ascii=False) if analysis_data.get('analise_concorrencia_profunda') else None,
                'marketing_data': json.dumps(analysis_data.get('estrategia_palavras_chave', {}), ensure_ascii=False) if analysis_data.get('estrategia_palavras_chave') else None,
                'metrics_data': json.dumps(analysis_data.get('metricas_performance', {}), ensure_ascii=False) if analysis_data.get('metricas_performance') else None,
                'comprehensive_analysis': json.dumps(analysis_data, ensure_ascii=False),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Remove campos None
            insert_data = {k: v for k, v in insert_data.items() if v is not None}
            
            # Insere no banco
            result = self.client.table('analyses').insert(insert_data).execute()
            
            if result.data:
                logger.info(f"Análise criada com ID: {result.data[0]['id']}")
                return result.data[0]
            else:
                logger.error("Erro ao criar análise: resultado vazio")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao criar análise: {str(e)}")
            return None
    
    def update_analysis(self, analysis_id: int, update_data: Dict[str, Any]) -> bool:
        """Atualiza análise existente"""
        if not self.available or not self.client:
            logger.warning("⚠️ Banco de dados não disponível")
            return False
            
        try:
            # Adiciona timestamp de atualização
            update_data['updated_at'] = datetime.now().isoformat()
            
            # Converte dados JSON para string se necessário
            for key, value in update_data.items():
                if isinstance(value, (dict, list)):
                    update_data[key] = json.dumps(value, ensure_ascii=False)
            
            # Atualiza no banco
            result = self.client.table('analyses').update(update_data).eq('id', analysis_id).execute()
            
            if result.data:
                logger.info(f"Análise {analysis_id} atualizada com sucesso")
                return True
            else:
                logger.error(f"Erro ao atualizar análise {analysis_id}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao atualizar análise {analysis_id}: {str(e)}")
            return False
    
    def get_analysis(self, analysis_id: int) -> Optional[Dict[str, Any]]:
        """Busca análise por ID"""
        if not self.available or not self.client:
            logger.warning("⚠️ Banco de dados não disponível")
            return None
            
        try:
            result = self.client.table('analyses').select('*').eq('id', analysis_id).execute()
            
            if result.data:
                analysis = result.data[0]
                
                # Converte campos JSON de volta para objetos
                json_fields = [
                    'avatar_data', 'positioning_data', 'competition_data',
                    'marketing_data', 'metrics_data', 'funnel_data',
                    'market_intelligence', 'action_plan', 'comprehensive_analysis'
                ]
                
                for field in json_fields:
                    if analysis.get(field) and isinstance(analysis[field], str):
                        try:
                            analysis[field] = json.loads(analysis[field])
                        except json.JSONDecodeError:
                            pass
                
                return analysis
            else:
                return None
                
        except Exception as e:
            logger.error(f"Erro ao buscar análise {analysis_id}: {str(e)}")
            return None
    
    def list_analyses(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista análises com paginação"""
        if not self.available or not self.client:
            logger.warning("⚠️ Banco de dados não disponível")
            return []
            
        try:
            result = self.client.table('analyses')\
                .select('id, nicho, produto, status, created_at, updated_at')\
                .order('created_at', desc=True)\
                .range(offset, offset + limit - 1)\
                .execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Erro ao listar análises: {str(e)}")
            return []
    
    def delete_analysis(self, analysis_id: int) -> bool:
        """Remove análise do banco"""
        if not self.available or not self.client:
            logger.warning("⚠️ Banco de dados não disponível")
            return False
            
        try:
            result = self.client.table('analyses').delete().eq('id', analysis_id).execute()
            
            if result.data:
                logger.info(f"Análise {analysis_id} removida com sucesso")
                return True
            else:
                logger.error(f"Erro ao remover análise {analysis_id}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao remover análise {analysis_id}: {str(e)}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do banco"""
        if not self.available or not self.client:
            return {
                'total_analyses': 0,
                'status_counts': {},
                'recent_analyses': 0,
                'error': 'Banco de dados não disponível',
                'available': False
            }
            
        try:
            # Total de análises
            total_result = self.client.table('analyses').select('id', count='exact').execute()
            total_analyses = total_result.count if total_result.count else 0
            
            # Análises por status
            status_result = self.client.table('analyses')\
                .select('status', count='exact')\
                .execute()
            
            status_counts = {}
            if status_result.data:
                for item in status_result.data:
                    status = item.get('status', 'unknown')
                    status_counts[status] = status_counts.get(status, 0) + 1
            
            # Análises recentes (últimos 7 dias)
            from datetime import timedelta
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            
            recent_result = self.client.table('analyses')\
                .select('id', count='exact')\
                .gte('created_at', week_ago)\
                .execute()
            
            recent_count = recent_result.count if recent_result.count else 0
            
            return {
                'total_analyses': total_analyses,
                'status_counts': status_counts,
                'recent_analyses': recent_count,
                'timestamp': datetime.now().isoformat(),
                'available': True
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            return {
                'total_analyses': 0,
                'status_counts': {},
                'recent_analyses': 0,
                'error': str(e),
                'available': False
            }

# Instância global do gerenciador
try:
    db_manager = DatabaseManager()
except Exception as e:
    logger.error(f"❌ Erro ao inicializar DatabaseManager: {str(e)}")
    # Cria um manager mock para evitar erros
    class MockDatabaseManager:
        def __init__(self):
            self.available = False
            logger.warning("⚠️ Usando MockDatabaseManager - banco de dados indisponível")
        
        def test_connection(self):
            return False
        
        def create_analysis(self, analysis_data):
            return None
        
        def update_analysis(self, analysis_id, update_data):
            return False
        
        def get_analysis(self, analysis_id):
            return None
        
        def list_analyses(self, limit=50, offset=0):
            return []
        
        def delete_analysis(self, analysis_id):
            return False
        
        def get_stats(self):
            return {
                'total_analyses': 0,
                'status_counts': {},
                'recent_analyses': 0,
                'error': 'Banco de dados não configurado',
                'available': False
            }
    
    db_manager = MockDatabaseManager()

