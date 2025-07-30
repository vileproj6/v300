#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Mental Drivers Architect
Arquiteto de Drivers Mentais Ultra-Avançado
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class MentalDriversArchitect:
    """Arquiteto de Drivers Mentais Ultra-Avançado"""
    
    def __init__(self):
        """Inicializa o arquiteto de drivers mentais"""
        self.universal_drivers = self._load_universal_drivers()
        logger.info(f"Mental Drivers Architect inicializado com {len(self.universal_drivers)} drivers universais")
    
    def _load_universal_drivers(self) -> Dict[str, Any]:
        """Carrega drivers mentais universais"""
        return {
            "urgencia": {
                "nome": "Urgência",
                "gatilho_central": "Tempo limitado",
                "definicao_visceral": "Medo de perder oportunidade única",
                "momento_ideal": "Apresentação da oferta",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Você já perdeu uma oportunidade por hesitar?",
                    "historia_analogia": "Como um trem que passa apenas uma vez",
                    "metafora_visual": "Relógio correndo contra você",
                    "comando_acao": "Decida agora antes que seja tarde"
                },
                "frases_ancoragem": [
                    "Apenas hoje",
                    "Últimas vagas",
                    "Oferta por tempo limitado",
                    "Não perca esta chance"
                ],
                "prova_logica": {
                    "estatistica": "87% das pessoas se arrependem de não agir",
                    "caso_exemplo": "Cliente que esperou e perdeu desconto",
                    "demonstracao": "Timer visual contando tempo"
                }
            },
            "escassez": {
                "nome": "Escassez",
                "gatilho_central": "Quantidade limitada",
                "definicao_visceral": "Medo de ficar sem",
                "momento_ideal": "Momento da decisão",
                "roteiro_ativacao": {
                    "pergunta_abertura": "O que você faria se soubesse que só restam 3 vagas?",
                    "historia_analogia": "Como ingressos para show do artista favorito",
                    "metafora_visual": "Estoque diminuindo em tempo real",
                    "comando_acao": "Garante sua vaga agora"
                },
                "frases_ancoragem": [
                    "Apenas 10 vagas",
                    "Estoque limitado",
                    "Exclusivo para poucos",
                    "Acesso restrito"
                ],
                "prova_logica": {
                    "estatistica": "Produtos limitados vendem 3x mais rápido",
                    "caso_exemplo": "Turma anterior esgotou em 2 horas",
                    "demonstracao": "Contador de vagas disponíveis"
                }
            },
            "autoridade": {
                "nome": "Autoridade",
                "gatilho_central": "Credibilidade do especialista",
                "definicao_visceral": "Confiança em quem já provou",
                "momento_ideal": "Apresentação pessoal",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Você seguiria conselhos de quem já teve sucesso?",
                    "historia_analogia": "Como médico especialista vs. Dr. Google",
                    "metafora_visual": "Diplomas e certificações na parede",
                    "comando_acao": "Confie na experiência comprovada"
                },
                "frases_ancoragem": [
                    "15 anos de experiência",
                    "Especialista reconhecido",
                    "Autoridade no assunto",
                    "Resultados comprovados"
                ],
                "prova_logica": {
                    "estatistica": "95% confiam mais em especialistas",
                    "caso_exemplo": "Certificações e prêmios recebidos",
                    "demonstracao": "Portfólio de casos de sucesso"
                }
            },
            "prova_social": {
                "nome": "Prova Social",
                "gatilho_central": "Outros já fizeram",
                "definicao_visceral": "Se outros fizeram, é seguro",
                "momento_ideal": "Superação de objeções",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Você faria algo que 1000 pessoas já aprovaram?",
                    "historia_analogia": "Como restaurante sempre cheio vs. vazio",
                    "metafora_visual": "Multidão seguindo mesma direção",
                    "comando_acao": "Junte-se aos que já decidiram"
                },
                "frases_ancoragem": [
                    "Mais de 1000 clientes",
                    "Aprovado por especialistas",
                    "Comunidade ativa",
                    "Depoimentos reais"
                ],
                "prova_logica": {
                    "estatistica": "78% seguem decisões da maioria",
                    "caso_exemplo": "Depoimentos em vídeo",
                    "demonstracao": "Contador de clientes satisfeitos"
                }
            },
            "reciprocidade": {
                "nome": "Reciprocidade",
                "gatilho_central": "Retribuir favor recebido",
                "definicao_visceral": "Obrigação moral de retribuir",
                "momento_ideal": "Após entregar valor gratuito",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Quando alguém te ajuda, você sente vontade de retribuir?",
                    "historia_analogia": "Como presente que gera obrigação de retribuir",
                    "metafora_visual": "Balança equilibrando dar e receber",
                    "comando_acao": "Agora é sua vez de investir em você"
                },
                "frases_ancoragem": [
                    "Conteúdo gratuito",
                    "Sem compromisso",
                    "Para retribuir",
                    "Troca justa"
                ],
                "prova_logica": {
                    "estatistica": "Reciprocidade aumenta conversão em 42%",
                    "caso_exemplo": "Amostra grátis que gerou venda",
                    "demonstracao": "Valor entregue vs. investimento solicitado"
                }
            },
            "compromisso": {
                "nome": "Compromisso e Consistência",
                "gatilho_central": "Manter coerência com decisões",
                "definicao_visceral": "Necessidade de ser consistente",
                "momento_ideal": "Após pequeno compromisso",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Você se considera uma pessoa de palavra?",
                    "historia_analogia": "Como promessa que deve ser cumprida",
                    "metafora_visual": "Assinatura em contrato",
                    "comando_acao": "Mantenha sua decisão"
                },
                "frases_ancoragem": [
                    "Você decidiu",
                    "Seja consistente",
                    "Honre seu compromisso",
                    "Palavra empenhada"
                ],
                "prova_logica": {
                    "estatistica": "89% mantêm decisões públicas",
                    "caso_exemplo": "Cliente que cumpriu meta após compromisso",
                    "demonstracao": "Registro público da decisão"
                }
            },
            "aversao_perda": {
                "nome": "Aversão à Perda",
                "gatilho_central": "Medo de perder o que tem",
                "definicao_visceral": "Dor de perder é maior que prazer de ganhar",
                "momento_ideal": "Apresentação de riscos",
                "roteiro_ativacao": {
                    "pergunta_abertura": "O que você perderia se não agir?",
                    "historia_analogia": "Como dinheiro saindo do bolso",
                    "metafora_visual": "Oportunidades escorrendo pelos dedos",
                    "comando_acao": "Não deixe escapar"
                },
                "frases_ancoragem": [
                    "Você pode perder",
                    "Não deixe escapar",
                    "Oportunidade única",
                    "Sem isso você fica para trás"
                ],
                "prova_logica": {
                    "estatistica": "Aversão à perda é 2x mais forte que ganho",
                    "caso_exemplo": "Concorrente que ganhou mercado",
                    "demonstracao": "Cálculo do custo de não agir"
                }
            },
            "ancoragem": {
                "nome": "Ancoragem",
                "gatilho_central": "Primeira impressão de valor",
                "definicao_visceral": "Referência inicial influencia tudo",
                "momento_ideal": "Apresentação de preços",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Quanto você pagaria por liberdade total?",
                    "historia_analogia": "Como preço de casa influencia negociação",
                    "metafora_visual": "Âncora fixando navio no lugar",
                    "comando_acao": "Compare com o valor real"
                },
                "frases_ancoragem": [
                    "Normalmente custa",
                    "Valor de mercado",
                    "Comparado com",
                    "Investimento mínimo"
                ],
                "prova_logica": {
                    "estatistica": "Primeira informação influencia 67% da decisão",
                    "caso_exemplo": "Preço premium que justifica desconto",
                    "demonstracao": "Tabela comparativa de valores"
                }
            },
            "curiosidade": {
                "nome": "Curiosidade",
                "gatilho_central": "Necessidade de saber",
                "definicao_visceral": "Coceira mental que precisa ser coçada",
                "momento_ideal": "Abertura da apresentação",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Quer saber o segredo que mudou tudo?",
                    "historia_analogia": "Como caixa misteriosa que precisa ser aberta",
                    "metafora_visual": "Porta entreaberta mostrando luz",
                    "comando_acao": "Descubra agora"
                },
                "frases_ancoragem": [
                    "Segredo revelado",
                    "Método oculto",
                    "Descoberta surpreendente",
                    "Informação exclusiva"
                ],
                "prova_logica": {
                    "estatistica": "Curiosidade aumenta engajamento em 73%",
                    "caso_exemplo": "Informação que mudou resultado",
                    "demonstracao": "Prévia do conteúdo exclusivo"
                }
            },
            "pertencimento": {
                "nome": "Pertencimento",
                "gatilho_central": "Fazer parte do grupo",
                "definicao_visceral": "Necessidade tribal de inclusão",
                "momento_ideal": "Convite para comunidade",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Você quer fazer parte do grupo de elite?",
                    "historia_analogia": "Como clube exclusivo de membros VIP",
                    "metafora_visual": "Círculo interno de pessoas especiais",
                    "comando_acao": "Seja aceito no grupo"
                },
                "frases_ancoragem": [
                    "Comunidade exclusiva",
                    "Grupo seleto",
                    "Membros VIP",
                    "Acesso especial"
                ],
                "prova_logica": {
                    "estatistica": "Pertencimento aumenta retenção em 85%",
                    "caso_exemplo": "Membro que transformou vida",
                    "demonstracao": "Benefícios exclusivos da comunidade"
                }
            },
            "novidade": {
                "nome": "Novidade",
                "gatilho_central": "Atração pelo novo",
                "definicao_visceral": "Excitação com descobertas",
                "momento_ideal": "Lançamento de produto",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Quer ser o primeiro a experimentar?",
                    "historia_analogia": "Como iPhone no primeiro dia de lançamento",
                    "metafora_visual": "Produto saindo da caixa pela primeira vez",
                    "comando_acao": "Seja pioneiro"
                },
                "frases_ancoragem": [
                    "Lançamento exclusivo",
                    "Primeira vez",
                    "Inovação revolucionária",
                    "Método inédito"
                ],
                "prova_logica": {
                    "estatistica": "Novidades geram 3x mais interesse",
                    "caso_exemplo": "Primeiro cliente com resultado inédito",
                    "demonstracao": "Comparação com métodos antigos"
                }
            },
            "simplicidade": {
                "nome": "Simplicidade",
                "gatilho_central": "Facilidade de execução",
                "definicao_visceral": "Alívio de não ser complicado",
                "momento_ideal": "Explicação do processo",
                "roteiro_ativacao": {
                    "pergunta_abertura": "E se fosse mais simples do que imagina?",
                    "historia_analogia": "Como apertar um botão e pronto",
                    "metafora_visual": "Caminho reto sem obstáculos",
                    "comando_acao": "Siga os passos simples"
                },
                "frases_ancoragem": [
                    "Apenas 3 passos",
                    "Simples assim",
                    "Sem complicação",
                    "Fácil de seguir"
                ],
                "prova_logica": {
                    "estatistica": "Simplicidade aumenta adesão em 67%",
                    "caso_exemplo": "Cliente que conseguiu em 1 semana",
                    "demonstracao": "Passo a passo visual"
                }
            },
            "transformacao": {
                "nome": "Transformação",
                "gatilho_central": "Mudança de vida",
                "definicao_visceral": "Esperança de vida melhor",
                "momento_ideal": "Apresentação de benefícios",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Como seria sua vida transformada?",
                    "historia_analogia": "Como lagarta virando borboleta",
                    "metafora_visual": "Antes e depois dramático",
                    "comando_acao": "Inicie sua transformação"
                },
                "frases_ancoragem": [
                    "Transformação total",
                    "Nova vida",
                    "Mudança radical",
                    "Renascimento profissional"
                ],
                "prova_logica": {
                    "estatistica": "Transformação motiva 91% das decisões",
                    "caso_exemplo": "Cliente que mudou de vida",
                    "demonstracao": "Depoimento de transformação"
                }
            },
            "status": {
                "nome": "Status",
                "gatilho_central": "Elevação social",
                "definicao_visceral": "Desejo de ser admirado",
                "momento_ideal": "Apresentação de benefícios sociais",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Como seria ser reconhecido como expert?",
                    "historia_analogia": "Como médico respeitado na comunidade",
                    "metafora_visual": "Subindo degraus de uma escada",
                    "comando_acao": "Eleve seu status"
                },
                "frases_ancoragem": [
                    "Status de expert",
                    "Reconhecimento",
                    "Prestígio",
                    "Admiração dos pares"
                ],
                "prova_logica": {
                    "estatistica": "Status influencia 84% das decisões B2B",
                    "caso_exemplo": "Cliente que virou referência",
                    "demonstracao": "Benefícios de status elevado"
                }
            },
            "seguranca": {
                "nome": "Segurança",
                "gatilho_central": "Redução de riscos",
                "definicao_visceral": "Proteção contra incertezas",
                "momento_ideal": "Apresentação de garantias",
                "roteiro_ativacao": {
                    "pergunta_abertura": "E se você tivesse garantia total?",
                    "historia_analogia": "Como seguro que protege patrimônio",
                    "metafora_visual": "Escudo protetor contra riscos",
                    "comando_acao": "Invista com segurança"
                },
                "frases_ancoragem": [
                    "Garantia total",
                    "Sem riscos",
                    "Proteção completa",
                    "Segurança garantida"
                ],
                "prova_logica": {
                    "estatistica": "Garantias aumentam conversão em 58%",
                    "caso_exemplo": "Cliente que usou garantia e ficou",
                    "demonstracao": "Termos da garantia"
                }
            },
            "prazer": {
                "nome": "Prazer",
                "gatilho_central": "Busca por satisfação",
                "definicao_visceral": "Antecipação de sensação boa",
                "momento_ideal": "Apresentação de benefícios emocionais",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Como seria sentir prazer no trabalho?",
                    "historia_analogia": "Como hobby que virou profissão",
                    "metafora_visual": "Sorriso de satisfação genuína",
                    "comando_acao": "Experimente o prazer"
                },
                "frases_ancoragem": [
                    "Prazer em trabalhar",
                    "Satisfação garantida",
                    "Alegria no processo",
                    "Diversão garantida"
                ],
                "prova_logica": {
                    "estatistica": "Prazer aumenta produtividade em 73%",
                    "caso_exemplo": "Cliente que ama o que faz",
                    "demonstracao": "Depoimento de satisfação"
                }
            },
            "dor": {
                "nome": "Dor",
                "gatilho_central": "Fuga do sofrimento",
                "definicao_visceral": "Urgência de parar a dor",
                "momento_ideal": "Identificação de problemas",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Até quando vai aguentar essa dor?",
                    "historia_analogia": "Como dor de dente que não passa",
                    "metafora_visual": "Espinho cravado que precisa sair",
                    "comando_acao": "Pare de sofrer agora"
                },
                "frases_ancoragem": [
                    "Pare de sofrer",
                    "Fim da dor",
                    "Alívio imediato",
                    "Solução definitiva"
                ],
                "prova_logica": {
                    "estatistica": "Dor motiva 2x mais que prazer",
                    "caso_exemplo": "Cliente que sofria e se libertou",
                    "demonstracao": "Antes e depois da solução"
                }
            },
            "exclusividade": {
                "nome": "Exclusividade",
                "gatilho_central": "Acesso especial",
                "definicao_visceral": "Sentir-se especial e único",
                "momento_ideal": "Convite para oferta especial",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Quer acesso ao que poucos têm?",
                    "historia_analogia": "Como convite para evento VIP",
                    "metafora_visual": "Porta dourada que poucos atravessam",
                    "comando_acao": "Aceite o convite exclusivo"
                },
                "frases_ancoragem": [
                    "Apenas para você",
                    "Acesso exclusivo",
                    "Convite especial",
                    "Selecionado pessoalmente"
                ],
                "prova_logica": {
                    "estatistica": "Exclusividade aumenta valor percebido em 89%",
                    "caso_exemplo": "Membro exclusivo com resultados únicos",
                    "demonstracao": "Benefícios que só você terá"
                }
            },
            "progresso": {
                "nome": "Progresso",
                "gatilho_central": "Evolução constante",
                "definicao_visceral": "Satisfação de avançar",
                "momento_ideal": "Apresentação de jornada",
                "roteiro_ativacao": {
                    "pergunta_abertura": "Quer ver seu progresso dia após dia?",
                    "historia_analogia": "Como game que você quer zerar",
                    "metafora_visual": "Barra de progresso enchendo",
                    "comando_acao": "Comece sua jornada"
                },
                "frases_ancoragem": [
                    "Evolução constante",
                    "Progresso visível",
                    "Avanço garantido",
                    "Crescimento contínuo"
                ],
                "prova_logica": {
                    "estatistica": "Progresso visível aumenta engajamento em 76%",
                    "caso_exemplo": "Cliente que evoluiu passo a passo",
                    "demonstracao": "Sistema de acompanhamento"
                }
            }
        }
    
    def generate_complete_drivers_system(
        self, 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera sistema completo de drivers mentais customizados"""
        
        logger.info("🧠 Gerando sistema completo de drivers mentais...")
        
        # Seleciona drivers mais relevantes para o avatar
        relevant_drivers = self._select_relevant_drivers(avatar_data, context_data)
        
        # Customiza drivers para o avatar específico
        customized_drivers = self._customize_drivers_for_avatar(relevant_drivers, avatar_data, context_data)
        
        # Cria sequência de ativação
        activation_sequence = self._create_activation_sequence(customized_drivers, avatar_data)
        
        # Gera roteiros específicos
        specific_scripts = self._generate_specific_scripts(customized_drivers, avatar_data, context_data)
        
        return {
            "drivers_selecionados": customized_drivers,
            "sequencia_ativacao": activation_sequence,
            "roteiros_especificos": specific_scripts,
            "sistema_anti_objecao": self._create_anti_objection_system(avatar_data),
            "arsenal_emergencia": self._create_emergency_arsenal(avatar_data),
            "metricas_efetividade": self._create_effectiveness_metrics(),
            "guia_implementacao": self._create_implementation_guide(customized_drivers)
        }
    
    def _select_relevant_drivers(
        self, 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> List[str]:
        """Seleciona drivers mais relevantes para o avatar"""
        
        # Analisa características do avatar
        dores = avatar_data.get('dores_viscerais', [])
        desejos = avatar_data.get('desejos_secretos', [])
        objecoes = avatar_data.get('objecoes_reais', [])
        perfil_psico = avatar_data.get('perfil_psicografico', {})
        
        # Score de relevância para cada driver
        driver_scores = {}
        
        for driver_name, driver_data in self.universal_drivers.items():
            score = 0
            
            # Score baseado em dores
            for dor in dores:
                if isinstance(dor, str):
                    dor_lower = dor.lower()
                    if driver_name == 'dor' and any(word in dor_lower for word in ['sofrer', 'dor', 'problema']):
                        score += 3
                    elif driver_name == 'urgencia' and any(word in dor_lower for word in ['tempo', 'rápido', 'urgente']):
                        score += 2
                    elif driver_name == 'seguranca' and any(word in dor_lower for word in ['medo', 'risco', 'incerteza']):
                        score += 2
            
            # Score baseado em desejos
            for desejo in desejos:
                if isinstance(desejo, str):
                    desejo_lower = desejo.lower()
                    if driver_name == 'status' and any(word in desejo_lower for word in ['reconhecido', 'autoridade', 'prestígio']):
                        score += 3
                    elif driver_name == 'transformacao' and any(word in desejo_lower for word in ['transformar', 'mudar', 'novo']):
                        score += 2
                    elif driver_name == 'exclusividade' and any(word in desejo_lower for word in ['exclusivo', 'especial', 'único']):
                        score += 2
            
            # Score baseado no perfil psicográfico
            if isinstance(perfil_psico, dict):
                personalidade = perfil_psico.get('personalidade', '').lower()
                if driver_name == 'autoridade' and any(word in personalidade for word in ['ambicioso', 'determinado']):
                    score += 2
                elif driver_name == 'progresso' and 'orientado a resultados' in personalidade:
                    score += 2
            
            # Score baseado no contexto
            segmento = context_data.get('segmento', '').lower()
            if 'medicina' in segmento or 'saúde' in segmento:
                if driver_name in ['autoridade', 'seguranca', 'prova_social']:
                    score += 2
            elif 'digital' in segmento or 'online' in segmento:
                if driver_name in ['novidade', 'simplicidade', 'transformacao']:
                    score += 2
            
            driver_scores[driver_name] = score
        
        # Seleciona top 8 drivers
        sorted_drivers = sorted(driver_scores.items(), key=lambda x: x[1], reverse=True)
        selected_drivers = [driver[0] for driver in sorted_drivers[:8]]
        
        # Garante que drivers essenciais estejam incluídos
        essential_drivers = ['urgencia', 'prova_social', 'autoridade', 'aversao_perda']
        for essential in essential_drivers:
            if essential not in selected_drivers:
                selected_drivers.append(essential)
        
        return selected_drivers[:10]  # Máximo 10 drivers
    
    def _customize_drivers_for_avatar(
        self, 
        selected_drivers: List[str], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Customiza drivers para o avatar específico"""
        
        customized = []
        
        for driver_name in selected_drivers:
            if driver_name not in self.universal_drivers:
                continue
            
            base_driver = self.universal_drivers[driver_name].copy()
            
            # Customiza baseado no avatar
            segmento = context_data.get('segmento', 'negócios')
            produto = context_data.get('produto', 'produto/serviço')
            
            # Customiza frases de ancoragem
            if driver_name == 'urgencia':
                base_driver['frases_ancoragem'] = [
                    f"Últimas vagas para {produto}",
                    f"Oferta especial em {segmento} por tempo limitado",
                    "Não perca esta oportunidade única",
                    "Decida hoje, comece amanhã"
                ]
            elif driver_name == 'autoridade':
                base_driver['frases_ancoragem'] = [
                    f"Especialista em {segmento} há 15+ anos",
                    f"Autoridade reconhecida em {produto}",
                    "Resultados comprovados no mercado",
                    "Método testado e aprovado"
                ]
            elif driver_name == 'prova_social':
                base_driver['frases_ancoragem'] = [
                    f"Mais de 1000 profissionais de {segmento}",
                    f"Comunidade ativa de {produto}",
                    "Depoimentos reais de clientes",
                    "Aprovado por especialistas"
                ]
            
            # Customiza roteiro de ativação
            base_driver['roteiro_ativacao']['pergunta_abertura'] = base_driver['roteiro_ativacao']['pergunta_abertura'].replace(
                'você', f'você, profissional de {segmento},'
            )
            
            customized.append(base_driver)
        
        return customized
    
    def _create_activation_sequence(
        self, 
        drivers: List[Dict[str, Any]], 
        avatar_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cria sequência de ativação dos drivers"""
        
        return {
            "fase_1_atencao": {
                "drivers": ["curiosidade", "novidade"],
                "objetivo": "Capturar atenção inicial",
                "tempo": "0-30 segundos",
                "tecnicas": ["Pergunta intrigante", "Estatística surpreendente"]
            },
            "fase_2_interesse": {
                "drivers": ["autoridade", "prova_social"],
                "objetivo": "Estabelecer credibilidade",
                "tempo": "30 segundos - 2 minutos",
                "tecnicas": ["Apresentação de credenciais", "Casos de sucesso"]
            },
            "fase_3_desejo": {
                "drivers": ["transformacao", "status", "prazer"],
                "objetivo": "Criar desejo intenso",
                "tempo": "2-5 minutos",
                "tecnicas": ["Visão do futuro", "Benefícios emocionais"]
            },
            "fase_4_acao": {
                "drivers": ["urgencia", "escassez", "aversao_perda"],
                "objetivo": "Motivar ação imediata",
                "tempo": "5-7 minutos",
                "tecnicas": ["Oferta limitada", "Consequências de não agir"]
            }
        }
    
    def _generate_specific_scripts(
        self, 
        drivers: List[Dict[str, Any]], 
        avatar_data: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera roteiros específicos para cada situação"""
        
        segmento = context_data.get('segmento', 'negócios')
        produto = context_data.get('produto', 'produto/serviço')
        
        return {
            "abertura_apresentacao": f"Você, profissional de {segmento}, já se perguntou por que alguns colegas conseguem resultados extraordinários com {produto} enquanto outros lutam para sobreviver?",
            
            "transicao_credibilidade": f"Nos últimos 15 anos, ajudei mais de 1000 profissionais de {segmento} a transformarem seus resultados com {produto}. E hoje vou compartilhar exatamente como você pode fazer o mesmo.",
            
            "apresentacao_solucao": f"Este {produto} foi desenvolvido especificamente para profissionais de {segmento} que querem sair da mesmice e alcançar resultados extraordinários.",
            
            "criacao_urgencia": f"Mas atenção: esta oportunidade é limitada. Apenas 50 profissionais de {segmento} terão acesso a este {produto} nesta turma.",
            
            "fechamento_acao": f"Se você é um profissional de {segmento} sério sobre transformar seus resultados com {produto}, clique no botão abaixo agora. As vagas estão se esgotando rapidamente.",
            
            "superacao_objecoes": {
                "preco": f"Eu entendo que o investimento pode parecer alto. Mas pense assim: quanto você está perdendo por mês sem ter o {produto} funcionando perfeitamente?",
                "tempo": f"Sei que você está ocupado. Por isso este {produto} foi criado para profissionais de {segmento} que têm pouco tempo mas querem máximos resultados.",
                "ceticismo": f"É normal ter dúvidas. Eu também teria. Por isso ofereço garantia total: se em 30 dias você não estiver completamente satisfeito com os resultados do {produto}, devolvemos 100% do seu investimento."
            }
        }
    
    def _create_anti_objection_system(self, avatar_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria sistema anti-objeção baseado no avatar"""
        
        objecoes = avatar_data.get('objecoes_reais', [])
        
        return {
            "objecoes_universais": {
                "preco_alto": {
                    "objecao": "Está muito caro",
                    "raiz_emocional": "Medo de perder dinheiro",
                    "contra_ataque": "O que é mais caro: investir agora ou continuar perdendo oportunidades?"
                },
                "falta_tempo": {
                    "objecao": "Não tenho tempo",
                    "raiz_emocional": "Sobrecarga e stress",
                    "contra_ataque": "Exatamente por isso você precisa disso - para ter mais tempo livre"
                },
                "nao_funciona": {
                    "objecao": "Isso não vai funcionar para mim",
                    "raiz_emocional": "Medo do fracasso",
                    "contra_ataque": "Por isso oferecemos garantia total e suporte personalizado"
                }
            },
            "arsenal_emergencia": [
                "Entendo perfeitamente sua preocupação...",
                "Muitos clientes pensaram exatamente isso...",
                "Deixe-me mostrar algo que vai mudar sua perspectiva...",
                "E se eu garantir que isso não vai acontecer?",
                "Posso fazer uma pergunta? O que você tem a perder?"
            ]
        }
    
    def _create_emergency_arsenal(self, avatar_data: Dict[str, Any]) -> List[str]:
        """Cria arsenal de emergência para situações difíceis"""
        
        return [
            "Pausa estratégica: 'Deixe-me fazer uma pergunta...'",
            "Redirecionamento: 'Isso me lembra de um cliente que...'",
            "Validação: 'Entendo perfeitamente, eu pensaria igual...'",
            "Prova social: 'Sabe o que outros clientes me disseram?'",
            "Garantia: 'E se eu assumir todo o risco?'",
            "Escassez: 'Infelizmente só posso ajudar poucos...'",
            "Autoridade: 'Em 15 anos fazendo isso, aprendi que...'",
            "Futuro: 'Imagine como será daqui a 6 meses...'",
            "Consequência: 'O que acontece se você não fizer nada?'",
            "Simplicidade: 'Na verdade é mais simples do que parece...'"
        ]
    
    def _create_effectiveness_metrics(self) -> Dict[str, Any]:
        """Cria métricas de efetividade dos drivers"""
        
        return {
            "metricas_conversao": {
                "taxa_abertura": "Percentual que assiste primeiros 30 segundos",
                "taxa_engajamento": "Percentual que assiste mais de 50%",
                "taxa_conversao": "Percentual que toma ação",
                "tempo_decisao": "Tempo médio para decidir"
            },
            "indicadores_driver": {
                "urgencia": "Redução no tempo de decisão",
                "autoridade": "Aumento na confiança",
                "prova_social": "Redução em objeções",
                "escassez": "Aumento na velocidade de ação"
            },
            "benchmarks": {
                "taxa_conversao_media": "2-5%",
                "taxa_conversao_otima": "8-15%",
                "tempo_decisao_medio": "3-7 dias",
                "tempo_decisao_otimo": "24-48 horas"
            }
        }
    
    def _create_implementation_guide(self, drivers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Cria guia de implementação dos drivers"""
        
        return {
            "preparacao": {
                "estudo_avatar": "Analise profundamente seu avatar antes de aplicar",
                "teste_mensagens": "Teste diferentes versões das mensagens",
                "preparacao_objecoes": "Prepare respostas para objeções comuns",
                "treinamento_equipe": "Treine equipe nos drivers selecionados"
            },
            "implementacao": {
                "sequencia_correta": "Siga a sequência de ativação recomendada",
                "timing_perfeito": "Respeite o timing de cada driver",
                "adaptacao_contexto": "Adapte para cada situação específica",
                "monitoramento_resultados": "Monitore resultados constantemente"
            },
            "otimizacao": {
                "teste_ab": "Teste diferentes versões dos drivers",
                "analise_dados": "Analise dados de conversão regularmente",
                "refinamento": "Refine baseado nos resultados",
                "escalabilidade": "Escale o que funciona melhor"
            }
        }

# Instância global
mental_drivers_architect = MentalDriversArchitect()