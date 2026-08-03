# 📌 HANDOVER E GUIA DE CONTINUIDADE DO PROJETO — ROUANETCONCILIA SAAS

**Nome do Projeto:** RouanetConcilia — SaaS B2B de Conciliação Financeira para Lei Rouanet & SALIC/MinC  
**Data da Documentação:** 03/08/2026  
**Finalidade:** Permitir a rápida continuidade, reprodução e evolução do projeto em qualquer outra máquina ou por qualquer outro desenvolvedor/agente.

---

## 🚀 1. Visão Geral e Estado Atual do Projeto

O **RouanetConcilia** é uma plataforma SaaS voltada para produtores culturais e controllers corporativos realizarem a conciliação financeira de projetos incentivados pela **Lei Rouanet** com validação automática para prestação de contas no **SALIC/MinC**.

### O que já está implementado e pronto:
1. **Diagnóstico UX/UI Completo:** Relatório de usabilidade cobrindo ingestão OFX/XML, redução de carga cognitiva e exportação SALIC (`diagnostico_ux_conciliacao_rouanet.md`).
2. **Protótipo HTML5/CSS3/JS Interativo Standalone:** Localizado em `rouanet-ux-demo/index.html` com 0 dependências externas de CDN (funciona 100% offline via `file:///`).
3. **Seção DOCUMENTOS & Checklist de Anexos:** Tabela reestruturada com exibição da Rubrica SALIC, lista de anexos validados (`✓`) e faltantes (`⚠️`), e coluna de status do checklist (`🟢 Completo`, `🟠 Incompleto`, `🔷 Parcial`).
4. **Slide-Over Drawer Lateral (Zero-Context-Switching):** Painel deslizante para anexar comprovantes, simular OCR (99.4% match) e conciliar em tempo real sem trocar de tela.
5. **Pre-Flight Check SALIC Modal:** Simulação da validação pré-voo de compliance antes da exportação do pacote ZIP padronizado para o Ministério da Cultura.
6. **Métricas e Estado Sincronizados:** Estado JS centralizado (`STATE`) onde a resolução de pendências recalcula automaticamente todos os cards KPI do topo, percentual de prontidão e badges de filtro.

---

## 🛠️ 2. Arquitetura Técnica e Estrutura de Arquivos

```
C:\Users\kATE\.gemini\antigravity\scratch\rouanet-ux-demo\
├── index.html                           # Protótipo Interativo Completo (HTML5 + CSS3 + JS Puro)
└── PROJETO_ROUANETCONCILIA_HANDOVER.md  # Este Guia de Continuidade
```

### Tecnologias Utilizadas:
- **HTML5 Semântico:** Estrutura responsiva com suporte a tabelas de alta densidade.
- **Vanilla CSS3 (Design System próprio):** Variáveis CSS (`:root`), Glassmorphism, paleta escura (WCAG AA), flexbox/grid e animações suaves.
- **Vanilla JavaScript (ES6+):** Manipulação de DOM nativa, motor de busca textual, ordenação por datas/valores e atualização reativa do objeto `STATE`.
- **Zero Dependências Externas:** SVG/Unicode nativo embutido para garantir funcionamento offline em qualquer navegador via `file:///`.

---

## 🎨 3. Design System & Tokens Visuais

### Paleta de Cores (Tema Escuro B2B)
- **Fundo Principal (`--bg-body`):** `#0b0f19`
- **Cards & Data Grid (`--bg-card`):** `#151c2c`
- **Inputs & Elementos Internos (`--bg-input`):** `#0f172a`
- **Bordas Divisórias (`--border-color`):** `#26334d`
- **Texto Principal (`--text-main`):** `#f8fafc`
- **Texto Secundário (`--text-muted`):** `#94a3b8`

### Matriz Semântica de Status

| Status de Auditoria | Fundo (Soft) | Cor Texto | Borda | Significado SALIC / MinC |
| :--- | :--- | :--- | :--- | :--- |
| **`CONCILIADO_OK`** | `rgba(16, 185, 129, 0.15)` | `#34d399` | `rgba(52, 211, 153, 0.3)` | 🟢 Lançamento e comprovantes 100% batidos. |
| **`ALERTA_DOCUMENTO_FALTANTE`** | `rgba(245, 158, 11, 0.15)` | `#fbbf24` | `rgba(251, 191, 36, 0.3)` | 🟠 Falta anexo de Nota Fiscal, RPA ou Recibo. |
| **`ALERTA_PJ_INTERMEDIARIA`** | `rgba(59, 130, 246, 0.15)` | `#60a5fa` | `rgba(96, 165, 250, 0.3)` | 🔷 Nota emitida por Agenciador/Produtora. |
| **`DIVERGENCIA_VALOR`** | `rgba(239, 68, 68, 0.15)` | `#f87171` | `rgba(248, 113, 113, 0.3)` | 🚨 Valor do extrato diverge do orçamento. |

---

## 📊 4. Datasets Pré-Configurados

### Dataset Ativo: PRONAC 23-4921 (Festival Cultural de Teatro)
- **Proponente:** Assoc. Arte & Vida (CNPJ: 24.891.012/0001-55)
- **Conta Captação:** Banco do Brasil | Agência: 3210-9 | C/C: 14.209-1
- **Exercício:** 2026
- **Total Auditado:** `R$ 450.000,00` (160 movimentações)
- **Lançamentos Conciliados:** `R$ 396.000,00` (142 itens ok - 88.7%)
- **Alertas Pendentes:** `R$ 54.000,00` (18 itens: 8 Doc. Faltante + 10 PJ Intermediária)
- **Prontidão SALIC:** `88.7% Concluído`

### Dataset Alternativo Auditado: PRONAC 20.7457 (Projeto 1961 - Cinema)
- **Proponente:** Circunstância Cinematográfica Ltda (CNPJ: 11.400.274/0001-94)
- **Conta Captação:** Banco do Brasil | Agência: 4328-1 | C/C: 8768-8
- **Exercício:** 2022 – 2025
- **Total Auditado:** `R$ 835.000,00` (184 movimentações)
- **Lançamentos Conciliados:** `R$ 831.743,99` (172 itens ok - 93.5%)
- **Alertas Pendentes:** `R$ 66.015,16` (12 itens: 2 Doc. Faltante + 10 PJ Intermediária)
- **Prontidão SALIC:** `93.5% Concluído`

---

## 💻 5. Instruções para Rodar e Continuar em Outra Máquina

### Como Abrir o Protótipo no Navegador:
1. Copie a pasta `rouanet-ux-demo` para a nova máquina.
2. Dê dois cliques em `index.html` ou abra qualquer navegador (Chrome/Edge/Firefox) e acesse:
   ```text
   file:///caminho/para/rouanet-ux-demo/index.html
   ```

### Executar via Servidor HTTP Local (Opcional):
- **Via Python:** `python -m http.server 8080 --directory ./rouanet-ux-demo`
- **Via Node/npx:** `npx serve ./rouanet-ux-demo -p 8080`

---

## 🔮 6. Próximos Passos de Desenvolvimento Recomendados

1. **Integração do Parser de OFX:** Conectar biblioteca `ofxparser` no backend Node/Python para transformar extratos reais em linhas da tabela `STATE`.
2. **Parser Automático de XML NF-e:** Implementar leitura da chave de acesso de 44 dígitos da NF-e para conferência automática de CNPJ do favorecido e valor.
3. **Motor de OCR para Recibos/RPA:** Integrar Tesseract.js ou AWS Textract para leitura de recibos em PDF/Imagem.
4. **Gerador de Relatório ZIP SALIC:** Desenvolver módulo no backend que empacote o CSV formatado no padrão SALIC junto com os PDFs renomeados no padrão MinC (`[PRONAC]_[ID]_[RUBRICA].pdf`).
