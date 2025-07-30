#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - API Validator
Validador de chaves de API no startup
"""

import os
import logging
import requests
from typing import Dict, Any, List
import google.generativeai as genai
from services.groq_client import groq_client

logger = logging.getLogger(__name__)

class APIValidator:
    """Validador de chaves de API"""
    
    def __init__(self):
        self.validation_results = {}
        self.critical_apis = ['GEMINI_API_KEY']  # APIs críticas
        self.optional_apis = ['GROQ_API_KEY', 'GOOGLE_SEARCH_KEY', 'HUGGINGFACE_API_KEY']
    
    def validate_all_apis(self) -> Dict[str, Any]:
        """Valida todas as APIs configuradas"""
        
        logger.info("🔍 Iniciando validação de APIs...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'critical_apis': {},
            'optional_apis': {},
            'overall_status': 'unknown',
            'errors': [],
            'warnings': []
        }
        
        # Valida APIs críticas
        for api_name in self.critical_apis:
            try:
                if api_name == 'GEMINI_API_KEY':
                    result = self.validate_gemini()
                else:
                    result = {'valid': False, 'error': 'Validador não implementado'}
                
                results['critical_apis'][api_name] = result
                
                if not result['valid']:
                    results['errors'].append(f"API crítica {api_name} inválida: {result.get('error', 'Erro desconhecido')}")
                    
            except Exception as e:
                error_msg = f"Erro ao validar {api_name}: {str(e)}"
                results['critical_apis'][api_name] = {'valid': False, 'error': error_msg}
                results['errors'].append(error_msg)
        
        # Valida APIs opcionais
        for api_name in self.optional_apis:
            try:
                if api_name == 'GROQ_API_KEY':
                    result = self.validate_groq()
                elif api_name == 'GOOGLE_SEARCH_KEY':
                    result = self.validate_google_search()
                elif api_name == 'HUGGINGFACE_API_KEY':
                    result = self.validate_huggingface()
                else:
                    result = {'valid': False, 'error': 'Validador não implementado'}
                
                results['optional_apis'][api_name] = result
                
                if not result['valid']:
                    results['warnings'].append(f"API opcional {api_name} inválida: {result.get('error', 'Erro desconhecido')}")
                    
            except Exception as e:
                error_msg = f"Erro ao validar {api_name}: {str(e)}"
                results['optional_apis'][api_name] = {'valid': False, 'error': error_msg}
                results['warnings'].append(error_msg)
        
        # Determina status geral
        critical_valid = all(api['valid'] for api in results['critical_apis'].values())
        
        if critical_valid:
            results['overall_status'] = 'healthy'
            logger.info("✅ Todas as APIs críticas são válidas")
        else:
            results['overall_status'] = 'critical_error'
            logger.error("❌ APIs críticas inválidas - sistema pode não funcionar")
        
        # Log de warnings
        if results['warnings']:
            logger.warning(f"⚠️ {len(results['warnings'])} avisos de APIs opcionais")
        
        self.validation_results = results
        return results
    
    def validate_gemini(self) -> Dict[str, Any]:
        """Valida API do Gemini"""
        
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            return {'valid': False, 'error': 'GEMINI_API_KEY não configurada'}
        
        if len(api_key) < 20:
            return {'valid': False, 'error': 'GEMINI_API_KEY parece inválida (muito curta)'}
        
        try:
            # Configura e testa
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            response = model.generate_content(
                "Responda apenas: GEMINI_OK",
                generation_config={'max_output_tokens': 10}
            )
            
            if response.text and 'GEMINI_OK' in response.text:
                return {
                    'valid': True,
                    'model': 'gemini-1.5-flash',
                    'response_time': 'OK'
                }
            else:
                return {'valid': False, 'error': 'Resposta inesperada do Gemini'}
                
        except Exception as e:
            error_msg = str(e)
            
            if 'API_KEY_INVALID' in error_msg:
                return {'valid': False, 'error': 'Chave de API inválida'}
            elif 'quota' in error_msg.lower():
                return {'valid': False, 'error': 'Quota excedida'}
            else:
                return {'valid': False, 'error': f'Erro na conexão: {error_msg}'}
    
    def validate_groq(self) -> Dict[str, Any]:
        """Valida API do Groq"""
        
        if not groq_client.is_available():
            return {'valid': False, 'error': 'GROQ_API_KEY não configurada'}
        
        try:
            test_result = groq_client.test_connection()
            
            if test_result:
                return {
                    'valid': True,
                    'model': groq_client.model,
                    'response_time': 'OK'
                }
            else:
                return {'valid': False, 'error': 'Falha no teste de conexão'}
                
        except Exception as e:
            return {'valid': False, 'error': f'Erro na validação: {str(e)}'}
    
    def validate_google_search(self) -> Dict[str, Any]:
        """Valida Google Custom Search API"""
        
        api_key = os.getenv('GOOGLE_SEARCH_KEY')
        cse_id = os.getenv('GOOGLE_CSE_ID')
        
        if not api_key or not cse_id:
            return {'valid': False, 'error': 'GOOGLE_SEARCH_KEY ou GOOGLE_CSE_ID não configurados'}
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': cse_id,
                'q': 'teste',
                'num': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'items' in data:
                    return {'valid': True, 'quota_remaining': 'OK'}
                else:
                    return {'valid': False, 'error': 'Resposta sem resultados'}
            elif response.status_code == 403:
                return {'valid': False, 'error': 'Acesso negado - verifique chaves'}
            else:
                return {'valid': False, 'error': f'Status HTTP {response.status_code}'}
                
        except Exception as e:
            return {'valid': False, 'error': f'Erro na conexão: {str(e)}'}
    
    def validate_huggingface(self) -> Dict[str, Any]:
        """Valida HuggingFace API"""
        
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        
        if not api_key:
            return {'valid': False, 'error': 'HUGGINGFACE_API_KEY não configurada'}
        
        if len(api_key) < 20:
            return {'valid': False, 'error': 'HUGGINGFACE_API_KEY parece inválida'}
        
        try:
            # Testa endpoint simples
            url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            payload = {
                "inputs": "teste",
                "options": {"wait_for_model": False}
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                return {'valid': True, 'status': 'OK'}
            elif response.status_code == 401:
                return {'valid': False, 'error': 'Token inválido'}
            elif response.status_code == 503:
                return {'valid': True, 'status': 'Modelo carregando (normal)'}
            else:
                return {'valid': False, 'error': f'Status HTTP {response.status_code}'}
                
        except Exception as e:
            return {'valid': False, 'error': f'Erro na conexão: {str(e)}'}
    
    def get_validation_summary(self) -> str:
        """Retorna resumo da validação"""
        
        if not self.validation_results:
            return "Validação não executada"
        
        critical_count = len([api for api in self.validation_results['critical_apis'].values() if api['valid']])
        critical_total = len(self.validation_results['critical_apis'])
        
        optional_count = len([api for api in self.validation_results['optional_apis'].values() if api['valid']])
        optional_total = len(self.validation_results['optional_apis'])
        
        return f"APIs Críticas: {critical_count}/{critical_total} | APIs Opcionais: {optional_count}/{optional_total}"
    
    def is_system_healthy(self) -> bool:
        """Verifica se o sistema está saudável"""
        return self.validation_results.get('overall_status') == 'healthy'

# Instância global
api_validator = APIValidator()