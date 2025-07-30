// ARQV30 Enhanced v2.0 - Async Analysis JavaScript
// Sistema de análise assíncrona com dashboard interativo

class AsyncAnalysisManager {
    constructor() {
        this.currentTaskId = null;
        this.statusCheckInterval = null;
        this.dashboardData = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDashboard();
    }

    setupEventListeners() {
        // Botão de análise assíncrona
        const asyncAnalyzeBtn = document.getElementById('asyncAnalyzeBtn');
        if (asyncAnalyzeBtn) {
            asyncAnalyzeBtn.addEventListener('click', () => this.startAsyncAnalysis());
        }

        // Botão de validação de APIs
        const validateApisBtn = document.getElementById('validateApisBtn');
        if (validateApisBtn) {
            validateApisBtn.addEventListener('click', () => this.validateAPIs());
        }

        // Refresh dashboard
        const refreshDashboardBtn = document.getElementById('refreshDashboardBtn');
        if (refreshDashboardBtn) {
            refreshDashboardBtn.addEventListener('click', () => this.loadDashboard());
        }
    }

    async startAsyncAnalysis() {
        try {
            // Valida formulário
            if (!this.validateForm()) {
                this.showError('Por favor, preencha pelo menos o segmento de mercado.');
                return;
            }

            // Coleta dados do formulário
            const formData = this.collectFormData();
            
            // Inicia análise assíncrona
            const response = await fetch('/api/analyze_async', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`Erro na análise: ${response.status}`);
            }

            const result = await response.json();
            
            this.currentTaskId = result.task_id;
            
            // Mostra interface de progresso
            this.showAsyncProgress();
            
            // Inicia monitoramento
            this.startStatusMonitoring();
            
            this.showSuccess(`Análise iniciada! ID: ${result.task_id}`);

        } catch (error) {
            console.error('Erro na análise assíncrona:', error);
            this.showError(`Erro: ${error.message}`);
        }
    }

    validateForm() {
        const segmento = document.getElementById('segmento')?.value?.trim();
        return segmento && segmento.length > 0;
    }

    collectFormData() {
        return {
            segmento: document.getElementById('segmento')?.value?.trim() || '',
            produto: document.getElementById('produto')?.value?.trim() || '',
            preco: document.getElementById('preco')?.value || '',
            publico: document.getElementById('publico')?.value?.trim() || '',
            concorrentes: document.getElementById('concorrentes')?.value?.trim() || '',
            query: document.getElementById('query')?.value?.trim() || '',
            dados_adicionais: document.getElementById('dados_adicionais')?.value?.trim() || '',
            objetivo_receita: document.getElementById('objetivo_receita')?.value || '',
            orcamento_marketing: document.getElementById('orcamento_marketing')?.value || '',
            prazo_lancamento: document.getElementById('prazo_lancamento')?.value || '',
            session_id: this.getSessionId()
        };
    }

    getSessionId() {
        let sessionId = localStorage.getItem('arqv30_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('arqv30_session_id', sessionId);
        }
        return sessionId;
    }

    showAsyncProgress() {
        const progressArea = document.getElementById('asyncProgressArea');
        if (progressArea) {
            progressArea.style.display = 'block';
            progressArea.scrollIntoView({ behavior: 'smooth' });
        }

        // Esconde resultados anteriores
        const resultsArea = document.getElementById('resultsArea');
        if (resultsArea) {
            resultsArea.style.display = 'none';
        }
    }

    startStatusMonitoring() {
        if (!this.currentTaskId) return;

        this.statusCheckInterval = setInterval(async () => {
            try {
                const response = await fetch(`/api/task_status/${this.currentTaskId}`);
                const status = await response.json();

                this.updateProgressUI(status);

                if (status.state === 'SUCCESS') {
                    this.onAnalysisComplete(status.result);
                    this.stopStatusMonitoring();
                } else if (status.state === 'FAILURE') {
                    this.onAnalysisError(status.error);
                    this.stopStatusMonitoring();
                }

            } catch (error) {
                console.error('Erro ao verificar status:', error);
            }
        }, 2000); // Verifica a cada 2 segundos
    }

    stopStatusMonitoring() {
        if (this.statusCheckInterval) {
            clearInterval(this.statusCheckInterval);
            this.statusCheckInterval = null;
        }
    }

    updateProgressUI(status) {
        // Atualiza barra de progresso
        const progressBar = document.querySelector('#asyncProgressArea .progress-fill');
        if (progressBar) {
            const percentage = (status.current / status.total) * 100;
            progressBar.style.width = `${percentage}%`;
        }

        // Atualiza texto do status
        const statusText = document.getElementById('asyncCurrentStep');
        if (statusText) {
            statusText.textContent = status.status || 'Processando...';
        }

        // Atualiza contador
        const stepCounter = document.getElementById('asyncStepCounter');
        if (stepCounter) {
            stepCounter.textContent = `${status.current}/${status.total}`;
        }

        // Atualiza fase
        const phaseIndicator = document.getElementById('asyncPhase');
        if (phaseIndicator) {
            const phaseNames = {
                'validation': '🔍 Validação',
                'data_collection': '📊 Coleta de Dados',
                'ai_analysis': '🤖 Análise IA',
                'finalization': '✅ Finalização'
            };
            phaseIndicator.textContent = phaseNames[status.phase] || status.phase || '';
        }
    }

    onAnalysisComplete(result) {
        // Esconde progresso
        const progressArea = document.getElementById('asyncProgressArea');
        if (progressArea) {
            progressArea.style.display = 'none';
        }

        // Mostra resultados em dashboard interativo
        this.displayInteractiveDashboard(result);
        
        // Atualiza dashboard do usuário
        this.loadDashboard();
        
        this.showSuccess('Análise concluída com sucesso!');
    }

    onAnalysisError(error) {
        // Esconde progresso
        const progressArea = document.getElementById('asyncProgressArea');
        if (progressArea) {
            progressArea.style.display = 'none';
        }

        this.showError(`Erro na análise: ${error}`);
    }

    displayInteractiveDashboard(result) {
        const container = document.getElementById('interactiveDashboard');
        if (!container) return;

        container.style.display = 'block';
        container.scrollIntoView({ behavior: 'smooth' });

        // Gera dashboard interativo
        const dashboardHTML = this.generateInteractiveDashboard(result);
        container.innerHTML = dashboardHTML;

        // Adiciona funcionalidades interativas
        this.setupInteractiveDashboard(result);
    }

    generateInteractiveDashboard(result) {
        return `
            <div class="interactive-dashboard">
                <div class="dashboard-header">
                    <h2>📊 Relatório Interativo de Análise</h2>
                    <div class="dashboard-actions">
                        <button class="btn-secondary" onclick="asyncAnalysisManager.downloadReport('txt')">
                            <i class="fas fa-file-alt"></i> Download TXT
                        </button>
                        <button class="btn-secondary" onclick="asyncAnalysisManager.downloadReport('pdf')">
                            <i class="fas fa-file-pdf"></i> Download PDF
                        </button>
                        <button class="btn-secondary" onclick="asyncAnalysisManager.downloadReport('json')">
                            <i class="fas fa-code"></i> Download JSON
                        </button>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <!-- Avatar Section -->
                    <div class="dashboard-card">
                        <h3>🎯 Avatar Ultra-Detalhado</h3>
                        <div class="avatar-summary">
                            ${this.formatAvatarSummary(result.avatar_ultra_detalhado)}
                        </div>
                    </div>

                    <!-- Insights Section -->
                    <div class="dashboard-card">
                        <h3>✨ Insights Exclusivos</h3>
                        <div class="insights-list">
                            ${this.formatInsightsList(result.insights_exclusivos)}
                        </div>
                    </div>

                    <!-- Competition Section -->
                    <div class="dashboard-card">
                        <h3>⚔️ Análise de Concorrência</h3>
                        <div class="competition-summary">
                            ${this.formatCompetitionSummary(result.analise_concorrencia)}
                        </div>
                    </div>

                    <!-- Action Plan Section -->
                    <div class="dashboard-card">
                        <h3>📋 Plano de Ação</h3>
                        <div class="action-plan-summary">
                            ${this.formatActionPlanSummary(result.plano_acao)}
                        </div>
                    </div>

                    <!-- Metadata Section -->
                    <div class="dashboard-card">
                        <h3>📊 Informações da Análise</h3>
                        <div class="metadata-summary">
                            ${this.formatMetadataSummary(result.task_metadata)}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    formatAvatarSummary(avatar) {
        if (!avatar) return '<p>Dados não disponíveis</p>';

        const perfil = avatar.perfil_demografico || {};
        const dores = avatar.dores_principais || [];

        return `
            <div class="avatar-quick-view">
                <p><strong>Idade:</strong> ${perfil.idade || 'N/A'}</p>
                <p><strong>Renda:</strong> ${perfil.renda || 'N/A'}</p>
                <p><strong>Localização:</strong> ${perfil.localizacao || 'N/A'}</p>
                <p><strong>Principais Dores:</strong></p>
                <ul>
                    ${dores.slice(0, 3).map(dor => `<li>${dor}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    formatInsightsList(insights) {
        if (!insights || !Array.isArray(insights)) return '<p>Nenhum insight disponível</p>';

        return `
            <div class="insights-quick-view">
                ${insights.slice(0, 5).map((insight, index) => `
                    <div class="insight-item">
                        <span class="insight-number">${index + 1}</span>
                        <span class="insight-text">${insight}</span>
                    </div>
                `).join('')}
                ${insights.length > 5 ? `<p class="more-insights">+${insights.length - 5} insights adicionais</p>` : ''}
            </div>
        `;
    }

    formatCompetitionSummary(competition) {
        if (!competition || !Array.isArray(competition)) return '<p>Dados não disponíveis</p>';

        return `
            <div class="competition-quick-view">
                ${competition.slice(0, 2).map(comp => `
                    <div class="competitor-item">
                        <h4>${comp.nome || 'Concorrente'}</h4>
                        <p><strong>Forças:</strong> ${comp.forcas?.slice(0, 2).join(', ') || 'N/A'}</p>
                        <p><strong>Fraquezas:</strong> ${comp.fraquezas?.slice(0, 2).join(', ') || 'N/A'}</p>
                    </div>
                `).join('')}
            </div>
        `;
    }

    formatActionPlanSummary(actionPlan) {
        if (!actionPlan) return '<p>Dados não disponíveis</p>';

        return `
            <div class="action-plan-quick-view">
                ${actionPlan.fase_1 ? `
                    <div class="phase-item">
                        <h4>Fase 1 (${actionPlan.fase_1.duracao || '30 dias'})</h4>
                        <p>${actionPlan.fase_1.atividades?.slice(0, 2).join(', ') || 'N/A'}</p>
                    </div>
                ` : ''}
                ${actionPlan.fase_2 ? `
                    <div class="phase-item">
                        <h4>Fase 2 (${actionPlan.fase_2.duracao || '60 dias'})</h4>
                        <p>${actionPlan.fase_2.atividades?.slice(0, 2).join(', ') || 'N/A'}</p>
                    </div>
                ` : ''}
            </div>
        `;
    }

    formatMetadataSummary(metadata) {
        if (!metadata) return '<p>Dados não disponíveis</p>';

        return `
            <div class="metadata-quick-view">
                <p><strong>ID da Task:</strong> ${metadata.task_id || 'N/A'}</p>
                <p><strong>Processado em:</strong> ${new Date(metadata.processed_at).toLocaleString('pt-BR')}</p>
                <p><strong>Modo:</strong> ${metadata.processing_mode || 'N/A'}</p>
                <p><strong>Rodadas de Busca:</strong> ${metadata.search_rounds || 0}</p>
                <p><strong>IA Utilizada:</strong> ${metadata.ai_provider_used || 'N/A'}</p>
            </div>
        `;
    }

    setupInteractiveDashboard(result) {
        // Adiciona funcionalidades interativas aqui
        // Por exemplo: gráficos, filtros, expansão de seções, etc.
        
        // Salva resultado localmente
        localStorage.setItem('last_analysis_result', JSON.stringify(result));
    }

    async downloadReport(format) {
        if (!this.currentTaskId) {
            this.showError('Nenhuma análise disponível para download');
            return;
        }

        try {
            const result = JSON.parse(localStorage.getItem('last_analysis_result'));
            
            if (format === 'txt') {
                this.downloadTXT(result);
            } else if (format === 'pdf') {
                await this.downloadPDF(result);
            } else if (format === 'json') {
                this.downloadJSON(result);
            }

        } catch (error) {
            console.error('Erro no download:', error);
            this.showError(`Erro no download: ${error.message}`);
        }
    }

    downloadTXT(result) {
        const txtContent = this.generateTXTReport(result);
        const blob = new Blob([txtContent], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analise_${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    async downloadPDF(result) {
        const response = await fetch('/api/generate_pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(result)
        });

        if (!response.ok) {
            throw new Error('Erro ao gerar PDF');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analise_${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    downloadJSON(result) {
        const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analise_${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    generateTXTReport(result) {
        return `
ARQV30 Enhanced v2.0 - Relatório de Análise de Mercado
========================================================

Gerado em: ${new Date().toLocaleString('pt-BR')}
Task ID: ${result.task_metadata?.task_id || 'N/A'}

AVATAR ULTRA-DETALHADO:
${this.formatAvatarForTXT(result.avatar_ultra_detalhado)}

INSIGHTS EXCLUSIVOS:
${this.formatInsightsForTXT(result.insights_exclusivos)}

ANÁLISE DE CONCORRÊNCIA:
${this.formatCompetitionForTXT(result.analise_concorrencia)}

PLANO DE AÇÃO:
${this.formatActionPlanForTXT(result.plano_acao)}

========================================================
Relatório gerado pelo ARQV30 Enhanced v2.0
Processamento: ${result.task_metadata?.processing_mode || 'N/A'}
IA Utilizada: ${result.task_metadata?.ai_provider_used || 'N/A'}
`;
    }

    formatAvatarForTXT(avatar) {
        if (!avatar) return 'Dados não disponíveis';

        const perfil = avatar.perfil_demografico || {};
        const dores = avatar.dores_principais || [];
        const desejos = avatar.desejos_principais || [];

        return `
Perfil Demográfico:
- Idade: ${perfil.idade || 'N/A'}
- Renda: ${perfil.renda || 'N/A'}
- Localização: ${perfil.localizacao || 'N/A'}

Principais Dores:
${dores.map((dor, i) => `${i + 1}. ${dor}`).join('\n')}

Principais Desejos:
${desejos.map((desejo, i) => `${i + 1}. ${desejo}`).join('\n')}
`;
    }

    formatInsightsForTXT(insights) {
        if (!insights || !Array.isArray(insights)) return 'Nenhum insight disponível';

        return insights.map((insight, i) => `${i + 1}. ${insight}`).join('\n');
    }

    formatCompetitionForTXT(competition) {
        if (!competition || !Array.isArray(competition)) return 'Dados não disponíveis';

        return competition.map(comp => `
Concorrente: ${comp.nome || 'N/A'}
Forças: ${comp.forcas?.join(', ') || 'N/A'}
Fraquezas: ${comp.fraquezas?.join(', ') || 'N/A'}
`).join('\n');
    }

    formatActionPlanForTXT(actionPlan) {
        if (!actionPlan) return 'Dados não disponíveis';

        let txt = '';
        
        if (actionPlan.fase_1) {
            txt += `\nFase 1 (${actionPlan.fase_1.duracao || '30 dias'}):\n`;
            txt += actionPlan.fase_1.atividades?.map(ativ => `- ${ativ}`).join('\n') || 'N/A';
        }
        
        if (actionPlan.fase_2) {
            txt += `\n\nFase 2 (${actionPlan.fase_2.duracao || '60 dias'}):\n`;
            txt += actionPlan.fase_2.atividades?.map(ativ => `- ${ativ}`).join('\n') || 'N/A';
        }

        return txt;
    }

    async loadDashboard() {
        try {
            const response = await fetch('/api/dashboard');
            if (response.ok) {
                this.dashboardData = await response.json();
                this.updateDashboardUI();
            }
        } catch (error) {
            console.error('Erro ao carregar dashboard:', error);
        }
    }

    updateDashboardUI() {
        const container = document.getElementById('userDashboard');
        if (!container || !this.dashboardData) return;

        container.innerHTML = `
            <div class="dashboard-stats">
                <div class="stat-card">
                    <h4>Total de Análises</h4>
                    <span class="stat-number">${this.dashboardData.stats.total_analyses || 0}</span>
                </div>
                <div class="stat-card">
                    <h4>Análises Recentes</h4>
                    <span class="stat-number">${this.dashboardData.stats.recent_analyses || 0}</span>
                </div>
                <div class="stat-card">
                    <h4>Tasks Ativas</h4>
                    <span class="stat-number">${this.dashboardData.active_tasks?.length || 0}</span>
                </div>
            </div>

            <div class="dashboard-content">
                <div class="analyses-history">
                    <h3>📋 Histórico de Análises</h3>
                    ${this.formatAnalysesHistory()}
                </div>

                <div class="active-tasks">
                    <h3>⚡ Tasks em Andamento</h3>
                    ${this.formatActiveTasks()}
                </div>
            </div>
        `;
    }

    formatAnalysesHistory() {
        if (!this.dashboardData.analyses || this.dashboardData.analyses.length === 0) {
            return '<p>Nenhuma análise encontrada</p>';
        }

        return this.dashboardData.analyses.map(analysis => `
            <div class="analysis-history-item">
                <div class="analysis-info">
                    <h4>${analysis.nicho || 'Análise'}</h4>
                    <p>${analysis.produto || 'Produto não informado'}</p>
                    <small>Criado em: ${new Date(analysis.created_at).toLocaleString('pt-BR')}</small>
                </div>
                <div class="analysis-actions">
                    <button class="btn-small" onclick="asyncAnalysisManager.downloadAnalysis(${analysis.id}, 'json')">
                        <i class="fas fa-download"></i> JSON
                    </button>
                    <button class="btn-small" onclick="asyncAnalysisManager.downloadAnalysis(${analysis.id}, 'pdf')">
                        <i class="fas fa-file-pdf"></i> PDF
                    </button>
                </div>
            </div>
        `).join('');
    }

    formatActiveTasks() {
        if (!this.dashboardData.active_tasks || this.dashboardData.active_tasks.length === 0) {
            return '<p>Nenhuma task em andamento</p>';
        }

        return this.dashboardData.active_tasks.map(task => `
            <div class="active-task-item">
                <div class="task-info">
                    <h4>Task ${task.task_id}</h4>
                    <p>Status: ${task.status}</p>
                    <p>Progresso: ${task.progress}%</p>
                </div>
                <div class="task-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${task.progress}%"></div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    async downloadAnalysis(analysisId, format) {
        try {
            const response = await fetch(`/api/analysis/${analysisId}/download?format=${format}`);
            
            if (!response.ok) {
                throw new Error('Erro no download');
            }

            if (format === 'json') {
                const data = await response.json();
                this.downloadJSON(data);
            } else {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `analise_${analysisId}.${format}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }

        } catch (error) {
            console.error('Erro no download:', error);
            this.showError(`Erro no download: ${error.message}`);
        }
    }

    async validateAPIs() {
        try {
            const response = await fetch('/api/validate_apis', {
                method: 'POST'
            });

            if (response.ok) {
                const result = await response.json();
                this.showSuccess(`Validação de APIs iniciada. Task ID: ${result.task_id}`);
            } else {
                throw new Error('Erro na validação');
            }

        } catch (error) {
            console.error('Erro na validação de APIs:', error);
            this.showError(`Erro: ${error.message}`);
        }
    }

    showError(message) {
        if (window.app && window.app.showError) {
            window.app.showError(message);
        } else {
            console.error(message);
            alert(message);
        }
    }

    showSuccess(message) {
        if (window.app && window.app.showSuccess) {
            window.app.showSuccess(message);
        } else {
            console.log(message);
        }
    }
}

// Inicializa o gerenciador quando a página carrega
document.addEventListener('DOMContentLoaded', () => {
    window.asyncAnalysisManager = new AsyncAnalysisManager();
});