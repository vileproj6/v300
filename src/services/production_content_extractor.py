#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Production Content Extractor
Extrator de conteúdo robusto para produção com múltiplas estratégias
"""

import os
import logging
import time
import requests
import hashlib
import sqlite3
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
from datetime import datetime
import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import chardet

logger = logging.getLogger(__name__)

class ProductionContentExtractor:
    """Extrator de conteúdo robusto para produção"""
    
    def __init__(self):
        """Inicializa o extrator de conteúdo para produção"""
        self.jina_api_key = os.getenv('JINA_API_KEY')
        self.jina_reader_url = "https://r.jina.ai/"
        self.request_timeout = int(os.getenv('REQUEST_TIMEOUT', 30))
        
        # Cache para conteúdo extraído
        self.cache_dir = "cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_db = os.path.join(self.cache_dir, "content_cache.db")
        self._init_cache_db()
        
        # User agents rotativos
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        
        # Estratégias de extração em ordem de prioridade
        self.extraction_strategies = [
            'jina_reader_api',
            'readability_extraction',
            'content_specific_extraction',
            'fallback_extraction'
        ]
        
        logger.info("🚀 Production Content Extractor inicializado")
    
    def _init_cache_db(self):
        """Inicializa banco de dados para cache de conteúdo"""
        try:
            with sqlite3.connect(self.cache_db) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS content_cache (
                        url_hash TEXT PRIMARY KEY,
                        url TEXT NOT NULL,
                        content TEXT NOT NULL,
                        metadata TEXT,
                        timestamp REAL NOT NULL,
                        ttl INTEGER DEFAULT 3600
                    )
                """)
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_content_timestamp ON content_cache(timestamp)
                """)
                conn.commit()
        except Exception as e:
            logger.error(f"Erro ao inicializar cache de conteúdo: {e}")
    
    def _get_url_hash(self, url: str) -> str:
        """Gera hash único para URL"""
        return hashlib.sha256(url.encode('utf-8')).hexdigest()
    
    def _get_cached_content(self, url: str) -> Optional[str]:
        """Recupera conteúdo do cache"""
        if not os.getenv('CACHE_ENABLED', 'true').lower() == 'true':
            return None
        
        try:
            url_hash = self._get_url_hash(url)
            
            with sqlite3.connect(self.cache_db) as conn:
                cursor = conn.execute(
                    "SELECT content, timestamp, ttl FROM content_cache WHERE url_hash = ?",
                    (url_hash,)
                )
                row = cursor.fetchone()
                
                if row:
                    content, timestamp, ttl = row
                    
                    # Verifica se não expirou
                    if time.time() - timestamp < ttl:
                        logger.info(f"📦 Cache hit para URL: {url[:50]}...")
                        return content
                    else:
                        # Remove entrada expirada
                        conn.execute("DELETE FROM content_cache WHERE url_hash = ?", (url_hash,))
                        conn.commit()
                
                return None
                
        except Exception as e:
            logger.error(f"Erro ao recuperar cache de conteúdo: {e}")
            return None
    
    def _cache_content(self, url: str, content: str, metadata: Dict[str, Any] = None):
        """Armazena conteúdo no cache"""
        if not os.getenv('CACHE_ENABLED', 'true').lower() == 'true':
            return
        
        try:
            url_hash = self._get_url_hash(url)
            timestamp = time.time()
            ttl = int(os.getenv('CACHE_TTL', 3600))
            metadata_str = str(metadata) if metadata else ""
            
            with sqlite3.connect(self.cache_db) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO content_cache 
                    (url_hash, url, content, metadata, timestamp, ttl) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (url_hash, url, content, metadata_str, timestamp, ttl))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Erro ao salvar cache de conteúdo: {e}")
    
    def _get_headers(self, referer: str = None) -> Dict[str, str]:
        """Gera headers otimizados para extração"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8,en-US;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Cache-Control': 'max-age=0'
        }
        
        if referer:
            headers['Referer'] = referer
        
        return headers
    
    def extract_content(self, url: str) -> Optional[str]:
        """Extrai conteúdo usando múltiplas estratégias robustas"""
        
        if not url or not url.startswith('http'):
            return None
        
        logger.info(f"🔍 Extraindo conteúdo de: {url[:80]}...")
        
        # Verifica cache primeiro
        cached_content = self._get_cached_content(url)
        if cached_content:
            return cached_content
        
        # Tenta cada estratégia em ordem de prioridade
        for strategy in self.extraction_strategies:
            try:
                logger.debug(f"🔧 Tentando estratégia: {strategy}")
                
                if strategy == 'jina_reader_api' and self.jina_api_key:
                    content = self._extract_with_jina_api(url)
                elif strategy == 'readability_extraction':
                    content = self._extract_with_readability(url)
                elif strategy == 'content_specific_extraction':
                    content = self._extract_content_specific(url)
                elif strategy == 'fallback_extraction':
                    content = self._extract_fallback(url)
                else:
                    continue
                
                if content and len(content.strip()) > 100:  # Conteúdo substancial
                    logger.info(f"✅ Conteúdo extraído com {strategy}: {len(content)} caracteres")
                    
                    # Salva no cache
                    self._cache_content(url, content, {'strategy': strategy})
                    
                    return content
                    
            except Exception as e:
                logger.warning(f"⚠️ Estratégia {strategy} falhou para {url}: {str(e)}")
                continue
        
        logger.error(f"❌ Todas as estratégias falharam para {url}")
        return None
    
    def _extract_with_jina_api(self, url: str) -> Optional[str]:
        """Extrai conteúdo usando Jina Reader API"""
        try:
            if not self.jina_api_key:
                return None
            
            headers = {
                **self._get_headers(),
                "Authorization": f"Bearer {self.jina_api_key}",
                "X-Return-Format": "text"
            }
            
            jina_url = f"{self.jina_reader_url}{url}"
            
            response = requests.get(
                jina_url,
                headers=headers,
                timeout=self.request_timeout
            )
            
            if response.status_code == 200:
                content = response.text
                
                # Valida se é conteúdo real
                if len(content) > 50 and not content.startswith('Error'):
                    # Limita tamanho para otimização
                    if len(content) > 20000:
                        content = content[:20000] + "... [conteúdo truncado para otimização]"
                    
                    return content
                else:
                    logger.warning(f"⚠️ Jina retornou conteúdo suspeito: {content[:100]}")
                    return None
            else:
                logger.warning(f"⚠️ Jina API retornou status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na Jina API: {e}")
            return None
    
    def _extract_with_readability(self, url: str) -> Optional[str]:
        """Extrai conteúdo usando algoritmo de readability"""
        try:
            headers = self._get_headers()
            
            # Delay anti-detecção
            time.sleep(random.uniform(0.5, 1.5))
            
            response = requests.get(
                url,
                headers=headers,
                timeout=self.request_timeout,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                # Detecta encoding automaticamente
                detected_encoding = chardet.detect(response.content)
                if detected_encoding['encoding']:
                    response.encoding = detected_encoding['encoding']
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Remove elementos desnecessários
                for element in soup(["script", "style", "nav", "footer", "header", 
                                   "form", "aside", "iframe", "noscript", "advertisement",
                                   "ads", "sidebar", "menu", "breadcrumb", "comment"]):
                    element.decompose()
                
                # Algoritmo de readability melhorado
                candidates = []
                
                # Busca elementos com conteúdo substancial
                content_selectors = [
                    'main', 'article', '[role="main"]',
                    '.content', '.main-content', '.post-content',
                    '.entry-content', '.article-content', '.page-content',
                    '#content', '#main-content', '#post-content',
                    '.container .content', '.wrapper .content'
                ]
                
                for selector in content_selectors:
                    elements = soup.select(selector)
                    for element in elements:
                        text = element.get_text()
                        if len(text) > 200:
                            # Score baseado em densidade de parágrafos e tamanho
                            paragraphs = element.find_all('p')
                            score = len(text) + (len(paragraphs) * 100)
                            candidates.append((score, text, selector))
                
                if candidates:
                    # Pega o elemento com maior score
                    candidates.sort(key=lambda x: x[0], reverse=True)
                    best_content = candidates[0][1]
                    
                    # Limpa o texto
                    cleaned_content = self._clean_extracted_text(best_content)
                    
                    if len(cleaned_content) > 100:
                        return cleaned_content
                
                # Fallback para body completo se não encontrou conteúdo principal
                body = soup.find('body')
                if body:
                    text = body.get_text()
                    cleaned_text = self._clean_extracted_text(text)
                    
                    if len(cleaned_text) > 100:
                        return cleaned_text
                
                return None
            else:
                logger.warning(f"⚠️ Readability: Status {response.status_code} para {url}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na extração readability: {e}")
            return None
    
    def _extract_content_specific(self, url: str) -> Optional[str]:
        """Extração específica baseada no domínio/tipo de site"""
        try:
            domain = urlparse(url).netloc.lower()
            
            # Estratégias específicas por tipo de site
            if any(news_domain in domain for news_domain in [
                'g1.com', 'folha.uol.com', 'estadao.com.br', 'valor.com.br',
                'exame.com', 'canaltech.com.br', 'tecmundo.com.br'
            ]):
                return self._extract_news_content(url)
            
            elif any(blog_domain in domain for blog_domain in [
                'medium.com', 'wordpress.com', 'blogspot.com'
            ]):
                return self._extract_blog_content(url)
            
            elif any(ecommerce_domain in domain for ecommerce_domain in [
                'mercadolivre.com', 'amazon.com', 'americanas.com'
            ]):
                return self._extract_ecommerce_content(url)
            
            else:
                return self._extract_generic_content(url)
                
        except Exception as e:
            logger.error(f"❌ Erro na extração específica: {e}")
            return None
    
    def _extract_news_content(self, url: str) -> Optional[str]:
        """Extrai conteúdo de sites de notícias"""
        try:
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.request_timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Seletores específicos para sites de notícias
                content_selectors = [
                    '.content-text', '.article-body', '.post-content',
                    '.entry-content', '.news-content', '.article-content',
                    '[itemprop="articleBody"]', '.story-body'
                ]
                
                for selector in content_selectors:
                    content_elem = soup.select_one(selector)
                    if content_elem:
                        text = content_elem.get_text()
                        cleaned_text = self._clean_extracted_text(text)
                        if len(cleaned_text) > 200:
                            return cleaned_text
                
                return None
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na extração de notícias: {e}")
            return None
    
    def _extract_blog_content(self, url: str) -> Optional[str]:
        """Extrai conteúdo de blogs"""
        try:
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.request_timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Seletores específicos para blogs
                content_selectors = [
                    '.post-content', '.entry-content', '.blog-content',
                    '.article-content', '.content', 'article'
                ]
                
                for selector in content_selectors:
                    content_elem = soup.select_one(selector)
                    if content_elem:
                        text = content_elem.get_text()
                        cleaned_text = self._clean_extracted_text(text)
                        if len(cleaned_text) > 200:
                            return cleaned_text
                
                return None
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na extração de blog: {e}")
            return None
    
    def _extract_ecommerce_content(self, url: str) -> Optional[str]:
        """Extrai conteúdo de sites de e-commerce"""
        try:
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.request_timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Seletores específicos para e-commerce
                content_selectors = [
                    '.product-description', '.item-description',
                    '.product-details', '.description', '.specs'
                ]
                
                content_parts = []
                
                for selector in content_selectors:
                    elements = soup.select(selector)
                    for elem in elements:
                        text = elem.get_text()
                        if len(text.strip()) > 50:
                            content_parts.append(text.strip())
                
                if content_parts:
                    combined_content = "\n\n".join(content_parts)
                    cleaned_text = self._clean_extracted_text(combined_content)
                    return cleaned_text
                
                return None
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na extração de e-commerce: {e}")
            return None
    
    def _extract_generic_content(self, url: str) -> Optional[str]:
        """Extração genérica robusta"""
        try:
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=self.request_timeout)
            
            if response.status_code == 200:
                # Detecta encoding
                detected_encoding = chardet.detect(response.content)
                if detected_encoding['encoding']:
                    response.encoding = detected_encoding['encoding']
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Remove elementos desnecessários
                for element in soup(["script", "style", "nav", "footer", "header", 
                                   "form", "aside", "iframe", "noscript"]):
                    element.decompose()
                
                # Busca conteúdo principal
                main_content = (
                    soup.find('main') or 
                    soup.find('article') or 
                    soup.find('div', class_=re.compile(r'content|main|article|post|entry|body')) or
                    soup.find('div', id=re.compile(r'content|main|article|post|entry|body')) or
                    soup.find('section', class_=re.compile(r'content|main|article|post|entry'))
                )
                
                if main_content:
                    text = main_content.get_text()
                else:
                    # Fallback para body completo
                    body = soup.find('body')
                    text = body.get_text() if body else soup.get_text()
                
                # Limpa o texto
                cleaned_text = self._clean_extracted_text(text)
                
                if len(cleaned_text) > 100:
                    return cleaned_text
                
                return None
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro na extração genérica: {e}")
            return None
    
    def _extract_fallback(self, url: str) -> Optional[str]:
        """Extração de fallback mais agressiva"""
        try:
            headers = self._get_headers()
            
            # Múltiplas tentativas com diferentes configurações
            configs = [
                {'timeout': 15, 'allow_redirects': True},
                {'timeout': 30, 'allow_redirects': False},
                {'timeout': 10, 'allow_redirects': True, 'stream': True}
            ]
            
            for config in configs:
                try:
                    response = requests.get(url, headers=headers, **config)
                    
                    if response.status_code == 200:
                        # Detecta encoding
                        if 'stream' in config:
                            content = b''
                            for chunk in response.iter_content(chunk_size=8192):
                                content += chunk
                                if len(content) > 1024 * 1024:  # 1MB limit
                                    break
                            response._content = content
                        
                        detected_encoding = chardet.detect(response.content)
                        if detected_encoding['encoding']:
                            response.encoding = detected_encoding['encoding']
                        
                        soup = BeautifulSoup(response.content, "html.parser")
                        
                        # Remove apenas elementos críticos
                        for element in soup(["script", "style", "noscript"]):
                            element.decompose()
                        
                        # Pega todo o texto disponível
                        text = soup.get_text()
                        
                        # Limpa o texto
                        cleaned_text = self._clean_extracted_text(text)
                        
                        if len(cleaned_text) > 100:
                            return cleaned_text
                            
                except Exception as e:
                    logger.debug(f"Config fallback falhou: {e}")
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro na extração fallback: {e}")
            return None
    
    def _clean_extracted_text(self, text: str) -> str:
        """Limpa e normaliza o texto extraído com robustez"""
        if not text:
            return ""
        
        # Normaliza encoding
        if isinstance(text, bytes):
            detected = chardet.detect(text)
            encoding = detected['encoding'] or 'utf-8'
            text = text.decode(encoding, errors='ignore')
        
        # Remove quebras de linha excessivas
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove espaços excessivos
        text = re.sub(r' +', ' ', text)
        
        # Remove caracteres de controle
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Remove caracteres especiais problemáticos mas mantém acentos
        text = re.sub(r'[^\w\s\.,;:!?\-\(\)%$€£¥\n\u00C0-\u017F]', '', text)
        
        # Quebra em linhas
        lines = (line.strip() for line in text.splitlines())
        
        # Remove linhas muito curtas (provavelmente menu/navegação)
        meaningful_lines = []
        for line in lines:
            if len(line) > 15:  # Linhas com pelo menos 15 caracteres
                meaningful_lines.append(line)
        
        # Junta linhas significativas
        cleaned_text = '\n'.join(meaningful_lines)
        
        # Remove linhas duplicadas consecutivas
        lines = cleaned_text.split('\n')
        deduplicated_lines = []
        prev_line = ""
        
        for line in lines:
            if line != prev_line:
                deduplicated_lines.append(line)
                prev_line = line
        
        cleaned_text = '\n'.join(deduplicated_lines)
        
        # Limita tamanho final
        if len(cleaned_text) > 15000:
            cleaned_text = cleaned_text[:15000] + "... [conteúdo truncado para otimização]"
        
        return cleaned_text.strip()
    
    def extract_metadata(self, url: str) -> Dict[str, Any]:
        """Extrai metadados da página com robustez"""
        try:
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                metadata = {
                    'title': '',
                    'description': '',
                    'keywords': '',
                    'author': '',
                    'published_date': '',
                    'language': '',
                    'canonical_url': url,
                    'og_title': '',
                    'og_description': '',
                    'og_image': '',
                    'twitter_title': '',
                    'twitter_description': ''
                }
                
                # Título
                title_tag = soup.find('title')
                if title_tag:
                    metadata['title'] = title_tag.get_text().strip()
                
                # Meta tags
                meta_tags = soup.find_all('meta')
                for tag in meta_tags:
                    name = tag.get('name', '').lower()
                    property_attr = tag.get('property', '').lower()
                    content = tag.get('content', '')
                    
                    if name == 'description' or property_attr == 'og:description':
                        if not metadata['description']:
                            metadata['description'] = content
                    elif name == 'keywords':
                        metadata['keywords'] = content
                    elif name == 'author':
                        metadata['author'] = content
                    elif name == 'language' or name == 'lang':
                        metadata['language'] = content
                    elif property_attr == 'article:published_time':
                        metadata['published_date'] = content
                    elif property_attr == 'og:title':
                        metadata['og_title'] = content
                    elif property_attr == 'og:description':
                        metadata['og_description'] = content
                    elif property_attr == 'og:image':
                        metadata['og_image'] = content
                    elif name == 'twitter:title':
                        metadata['twitter_title'] = content
                    elif name == 'twitter:description':
                        metadata['twitter_description'] = content
                
                # URL canônica
                canonical = soup.find('link', rel='canonical')
                if canonical:
                    metadata['canonical_url'] = canonical.get('href', url)
                
                return metadata
            else:
                return {'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def batch_extract(self, urls: List[str], max_workers: int = 5) -> Dict[str, Optional[str]]:
        """Extrai conteúdo de múltiplas URLs em paralelo"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self.extract_content, url): url for url in urls}
            
            for future in as_completed(future_to_url, timeout=120):
                url = future_to_url[future]
                try:
                    content = future.result()
                    results[url] = content
                except Exception as e:
                    logger.error(f"❌ Erro na extração batch para {url}: {e}")
                    results[url] = None
        
        return results
    
    def clear_cache(self):
        """Limpa cache de conteúdo"""
        try:
            if os.path.exists(self.cache_db):
                with sqlite3.connect(self.cache_db) as conn:
                    conn.execute("DELETE FROM content_cache")
                    conn.commit()
                logger.info("🗑️ Cache de conteúdo limpo")
        except Exception as e:
            logger.error(f"Erro ao limpar cache de conteúdo: {e}")

# Instância global para produção
production_content_extractor = ProductionContentExtractor()