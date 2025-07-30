#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Groq Client
Cliente para integração com Groq API como fallback do Gemini
"""

import os
import logging
from typing import Optional, Dict, Any
from groq import Groq

logger = logging.getLogger(__name__)

class GroqClient:
    """Cliente para integração com Groq API"""
    
    def __init__(self):
        """Inicializa cliente Groq"""
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = "llama3-70b-8192"  # Modelo mais capaz
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.available = True
            logger.info("✅ Groq client inicializado com sucesso")
        else:
            self.client = None
            self.available = False
            logger.warning("⚠️ GROQ_API_KEY não encontrada")
    
    def is_available(self) -> bool:
        """Verifica se o cliente está disponível"""
        return self.available
    
    def generate_analysis(
        self, 
        prompt: str, 
        max_tokens: int = 8192,
        temperature: float = 0.7,
        timeout: int = 60
    ) -> Optional[str]:
        """Gera análise usando Groq"""
        
        if not self.available:
            logger.warning("⚠️ Groq não está disponível")
            return None
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em análise de mercado ultra-detalhada. Responda sempre em português brasileiro."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout
            )
            
            content = response.choices[0].message.content
            if content:
                logger.info(f"✅ Groq gerou {len(content)} caracteres")
                return content
            else:
                logger.error("❌ Groq retornou resposta vazia")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na requisição Groq: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """Testa conexão com Groq"""
        
        if not self.available:
            return False
        
        try:
            test_result = self.generate_analysis(
                "Responda apenas: GROQ_OK", 
                max_tokens=10, 
                timeout=30
            )
            return test_result is not None and "GROQ_OK" in test_result
        except Exception as e:
            logger.error(f"❌ Erro no teste de conexão Groq: {str(e)}")
            return False

# Instância global
groq_client = GroqClient()