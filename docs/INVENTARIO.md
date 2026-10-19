# Inventário dos materiais de origem

Levantamento feito em 01/10/2026 sobre cópias dos arquivos da pasta `sistema-completo/` (os três materiais iniciais e, depois, o pacote de data science, seção 4). Os originais não foram alterados. As cópias usadas pelo gerador do site estão em `site/gerador/origem/`.

| Material | Arquivo | Tamanho | Formato |
|---|---|---|---|
| Notebook mestre | `Notebook_Mestre_Analise_de_Dados.ipynb` | 189 KB | Jupyter (nbformat 4), 267 células: 139 de texto (Markdown) e 128 de código |
| Guia de visualização | `guia-matplotlib-seaborn.zip` | 1,2 MB | pacote com HTML autocontido (1,76 MB, 62 imagens PNG em base64) e o código Python que o gera |
| Guia de relatório | `guia-relatorio-profissional.zip` | 45 KB | HTML autocontido (103 KB) e modelo de relatório em Word (`.docx`, 19 KB) |
| Manual e guia de data science | `data-science-htlm.zip` | 204 KB | manual de Machine Learning em HTML autocontido (450 KB), skill de decisão (`.md`, 61 KB), relatório de auditoria (`.md`, 39 KB), 7 scripts de auditoria, README e `.gitignore` |

---

## 1. Notebook mestre de análise de dados

**Título:** “Notebook Mestre de Análise de Dados: manual prático e template de referência”.
**Proposta:** responder “Recebi um novo dataset. Por onde começo?” seguindo a ordem de um projeto: importar → conhecer → limpar → descrever → explorar → testar → comunicar.
**Formato de cada tópico:** O que faz · Quando usar · Código · ⚠️ O que observar.
**Marcadores próprios:** 🔹 Alternativa (outra forma válida de fazer a mesma tarefa) e ➕ Complemento (técnica que não estava no material de estudo original).
**Dados:** sintéticos, gerados por duas funções (`gerar_dados_exemplo`, `gerar_tabelas_auxiliares`) com semente fixa (`SEED = 42`). Três tabelas: `df` (1.005 linhas com 5 duplicadas propositais), `tabela_categorias` (dimensão com 4 categorias) e `eventos` (funil e pedidos de 3.000 clientes).
**Saídas salvas:** nenhuma. O arquivo foi entregue sem saídas executadas, portanto sem tabelas, textos impressos ou gráficos gravados. Para o site, as saídas foram geradas executando o próprio notebook (ver `docs/DECISOES.md`).
**Bibliotecas:** pandas, numpy, matplotlib, seaborn, scipy, statistics, statsmodels, sqlite3, pingouin (opcional), scikit-posthocs (opcional), openpyxl (exportação).

### Estrutura, célula a célula

| Seção | Células | Subseções | Código | Gráficos gerados ao executar |
|---|---|---|---|---|
| Abertura | 0 | apresentação, formato dos tópicos, convenções do template, tabelas de nomes de colunas e tabelas auxiliares, legenda 🔹/➕ | 0 | 0 |
| Índice | 1 | tabela das seções 0 a 15 com a pergunta que cada uma responde | 0 | 0 |
| 0. Roteiro rápido | 2 | cinco perguntas da EDA, diagrama da sequência de trabalho, o que observar | 0 | 0 |
| 1. Configuração do ambiente | 3–12 | 1.1 Bibliotecas · 1.2 Opções de exibição e estilo · 1.3 Parâmetros do projeto · 1.4 Datasets sintéticos | 6 | 0 |
| 2. Importação dos dados | 13–29 | 2.1 Leitura do arquivo (tabela de parâmetros de leitura) · 2.2 Dicionário de dados · 2.3 Consultas SQL ➕ (selecionar, agregar, JOIN, CASE/CTE/janela, equivalências SQL ↔ pandas) | 9 | 0 |
| 3. Primeira inspeção | 30–49 | 3.1 Estrutura · 3.2 Tipos de dados (dtypes e tipos estatísticos) · 3.3 Nulos · 3.4 Duplicadas ➕ · 3.5 Valores únicos · 3.6 Diagnóstico em uma tabela | 10 | 1 (célula 40) |
| 4. Limpeza e tratamento | 50–78 | 4.1 Nomes de colunas · 4.2 Conversão de tipos · 4.3 Nulos · 4.4 Duplicados ➕ · 4.5 Recodificação · 4.6 Texto e multivaloradas · 4.7 Filtros · 4.8 Criação de colunas · 4.9 Log · 4.10 Junção de tabelas ➕ | 14 | 0 |
| 5. Estatística descritiva | 79–102 | 5.1 `describe()` · 5.2 Tendência central · 5.3 Dispersão · 5.4 Separatrizes e forma · 5.5 Tabela descritiva completa · 5.6 Frequências · 5.7 Escore Z | 12 | 0 |
| 6. Análise univariada | 103–118 | 6.1 Histograma · 6.2 KDE e rugplot · 6.3 Boxplot, violino e painel · 6.4 Normalidade visual · 6.5 Categóricas | 7 | 7 (células 104, 108, 110, 111, 114 ×2, 117) |
| 7. Outliers | 119–129 | 7.1 IQR · 7.2 Z-score · 7.3 Inspeção · 7.4 Tratamento | 6 | 1 (121) |
| 8. Bivariada e multivariada | 130–163 | 8.1 Num × num · 8.2 `jointplot` · 8.3 Num × cat · 8.4 Cat × cat · 8.5 Segmentação · 8.6 Visão multivariada | 18 | 12 (131, 135, 138, 139, 145, 146, 148, 149, 153, 157, 160, 162) |
| 9. Análise temporal | 164–176 | 9.1 Componentes de data · 9.2 Evolução · 9.3 Sazonalidade · 9.4 Variação entre períodos ➕ | 6 | 3 (168, 171, 175) |
| 10. Métricas de negócio ➕ | 177–190 | 10.1 Base por cliente · 10.2 KPIs · 10.3 Funil · 10.4 Coorte e retenção | 7 | 2 (185, 188) |
| 11. Visualização: referência técnica | 191–202 | 11.1 Qual gráfico usar · 11.2 Estrutura matplotlib · 11.3 Axes-level × figure-level · 11.4 Estilos e cores · 11.5 Funções desatualizadas | 5 | 5 (192, 194, 197, 198, 199) |
| 12. Estatística inferencial | 203–243 | 12.1 Conceitos · 12.2 Qual teste · 12.3 Pressupostos · 12.4 Um grupo · 12.5 Dois grupos · 12.6 Três ou mais · 12.7 Qui-quadrado ➕ · 12.8 Proporções e A/B ➕ · 12.9 Efeito e IC · 12.10 Fluxo automatizado · 12.11 🔹 pingouin | 24 | 0 |
| 13. Regressão linear | 244–255 | 13.1 `scipy` · 13.2 Impacto dos outliers · 13.3 `seaborn` · 13.4 `statsmodels` ➕ | 6 | 4 (246, 248, 250, 251) |
| 14. Insights e comunicação | 256–265 | 14.1 Extrair insights · 14.2 Reportar resultados · 14.3 Gráfico com significância · 14.4 Estrutura do relatório · 14.5 Exportação e pipeline | 3 | 1 (260) |
| 15. Checklist final | 266 | Antes de começar · Dados · Exploração · Inferência · Comunicação | 0 | 0 |

Total: 36 figuras geradas na execução, em 35 células de código (a célula 114 gera duas).

### Elementos de conteúdo que exigem tratamento no site

- Fórmulas em LaTeX inline (`$\bar{x}$`, `$\frac{s}{\sqrt{n}}$`, `$Q1 - k \cdot IQR$`, `$F = \frac{...}{...}$` etc.) nas seções 5, 7, 12 e 13.
- Tabelas Markdown em quase todas as seções (são o principal formato de referência do notebook).
- Blocos de código dentro do texto (cercas ```` ```python ```` e ```` ```text ````) nas células 2, 15, 16, 17, 216, 261, 262 e 265, que não são executados.
- Lista de tarefas com `- [ ]` na célula 266 (checklist).
- Emojis usados como marcadores: 📘 (título), ⚠️ (O que observar), 🔹 (Alternativa), ➕ (Complemento).
- Referências cruzadas no texto (“Seção 4.2”, “Seções 6.4 e 12.3”), que no site viram links.
- Uma célula que grava arquivos (`output/grafico_aaaa.png`, `output/tabela_aaaa.xlsx` e `.csv`).

---

## 2. Guia matplotlib e seaborn com storytelling de dados

**Pacote:** `guia_matplotlib_seaborn.html` (resultado do build) mais o código que o gera: `build.py` (montagem), `kit.py` (motor: preâmbulos de estilo, execução dos exemplos, compressão das imagens, mapa de “eixos” por linha de código), `fundamentos.py`, `catalogo.py`, `story.py`, `referencia.py`, `estilo.css`, `app.js`, `requirements.txt`, `README.md`.
**Princípio declarado:** cada imagem é produzida executando exatamente o código exibido ao lado dela.
**Dados:** sintéticos (marcados no texto) ou conjuntos do seaborn (`tips`, `flights`, `iris`, baixados da internet na primeira execução).
**Convenção de cor:** cinza `#A6A6A6` para contexto, azul `#1F5FA8` para destaque e laranja `#D9731A` para alerta, declarada no texto e em todo o código (`CINZA, AZUL, LARANJA`).
**Selos de autoria:** “Knaflic” (ideia da autora, parafraseada), “Recomendação técnica” (sugestão do guia) e “a confirmar no livro” (5 ocorrências).

### Estrutura

| Parte | Âncora | Conteúdo | Imagens | Blocos de código |
|---|---|---|---|---|
| Como usar este guia | `inicio` | apresentação, três cartões de entrada, convenções (cores, código completo, dados, quem disse o quê) | 0 | 0 |
| 1. Fundamentos | `fundamentos` | anatomia de uma figura; interfaces pyplot e orientada a objetos (com `add_axes`); estilos e rcParams; seaborn sobre matplotlib (funções de eixo e de figura); quando usar cada um (tabela); atualizações de API (tabela) | 8 | 8 |
| 2. Os seis eixos de Knaflic | `eixos` | contexto, visual eficaz, desordem, atenção, designer, história; cada cartão lista onde o eixo aparece no código (128 links) | 0 | 0 |
| 3. Catálogo de gráficos | `catalogo` | 16 cartões: linha, barras verticais, barras horizontais, empilhadas 100%, dispersão, histograma, boxplot, violino, mapa de calor, inclinação, cascata, pizza e rosca, pairplot, regressão, distribuição conjunta, texto simples. Cada um com objetivo, quando escolher, quando evitar, botões de realce por eixo, variantes matplotlib e seaborn, notas e base | 29 | 29 |
| 4. Antes e depois | `antes-depois` | bordas e grades, cor como destaque, rótulos diretos, título com a conclusão, anotações | 10 | 10 |
| 5. Roteiro de montagem | `roteiro` | contexto (quem, o quê, como), grande ideia, storyboard, estrutura narrativa, montagem do gráfico em cinco passos | 5 | 5 |
| 6. Erros comuns | `erros` | eixo truncado em barras, 3D, eixo secundário, excesso de cores | 8 | 8 |
| 7. Referência rápida | `referencia` | tabela pergunta → gráfico, estilo reutilizável (funções `estilo_explicativo`, `titulo`, `destacar`, `rotular_fim`, `sem_eixo`, `numero_br`), checklist, fontes e créditos | 2 | 2 |

Interatividade original: busca e filtros (situação e biblioteca) na barra lateral, abas entre variantes, alternador antes/depois, navegação por passos, realce de linhas de código por eixo, copiar código, menu móvel e seção ativa na navegação.

---

## 3. Guia do relatório profissional em dados

**Pacote:** `guia_relatorio_profissional_dados.html` (HTML, CSS e JavaScript no mesmo arquivo) e `modelo_relatorio_dados.docx` (modelo em branco com a mesma estrutura de seções).
**Dados:** fictícios, sobre a “Empresa Exemplo”. Trechos marcados “Complemento” cobrem etapas que o material de estudo original não detalha (briefing, revisão, entrega).

### Estrutura

| Seção | Âncora | Conteúdo |
|---|---|---|
| Como usar este guia | `inicio` | apresentação, link do modelo `.docx`, fluxo das seis etapas, como usar, nota sobre dados fictícios |
| Etapa 1. Entender a demanda (Complemento) | `etapa-1` | perguntas ao demandante (4 grupos), molde de declaração do problema, exemplo fraco × forte, alerta, questionário de briefing com resumo copiável, escopo/prazo/quem decide, lista de verificação (6 itens) |
| Etapa 2. Preparar os dados | `etapa-2` | fontes e dicionário (tabela de leitura), inspeção (5 passos e código), limpeza (tabela de estratégias para nulos), validações, alerta sobre outliers, registro de premissas e limitações (tabela de exemplo), lista de verificação (8 itens) |
| Etapa 3. Analisar | `etapa-3` | descrever antes de comparar (código `descritivas`), da pergunta à análise (duas tabelas), roteiro de qualquer teste, código pingouin, o que o dado sustenta e não sustenta, armadilhas, exemplo fraco × forte, do resultado ao insight, lista de verificação (8 itens) |
| Etapa 4. Estruturar o relatório | `etapa-4` | anatomia (9 partes), modelo de texto por seção (9 blocos recolhíveis com “Copiar modelo”), relatório-modelo completo fictício (capa, 7 seções, 2 figuras SVG, 1 tabela, 4 comparações fraco × forte), lista de verificação (6 itens) |
| Etapa 5. Comunicar | `etapa-5` | ordem da narrativa, títulos-conclusão (fraco × forte), escolha de gráficos (tabela), regras para todo gráfico, linguagem para leitor não técnico (Complemento, tabela e exemplo), como reportar no detalhamento técnico (tabela), lista de verificação (6 itens) |
| Etapa 6. Revisar e entregar | `etapa-6` | revisão em três passadas, formato e canal, como apresentar (tabela de tempos), perguntas e ajustes (todas Complemento), lista de verificação final (7 itens), rodapé |

**Imagens:** nenhuma imagem raster. Três gráficos em SVG inline no relatório-modelo: Figura 1 (barras de recompra), Figura 2 “versão forte” (barras de taxa de atraso com linha de média) e Figura 2 “versão fraca” (pizza colorida, exemplo do que evitar). Os demais SVG são ícones (busca, download, impressão).
**Interatividade original:** busca no menu, listas de verificação com contador por etapa e progresso geral, briefing com resumo automático e botão copiar, alternadores fraco × forte, abrir/fechar todos os modelos, copiar modelos, imprimir ou salvar em PDF, menu móvel. As marcações não são persistidas (voltam ao início ao recarregar).

### Modelo `.docx`

Capa (título, subtítulo, campos de identificação), sumário automático, controle de versões, seções 1 a 7 (resumo executivo, contexto, achados com espaços para figuras e tabela, implicações, ações com tabela, premissas e limitações com tabela, detalhamento técnico), Anexo A (dicionário de dados) e Anexo B (método, testes, reprodutibilidade). Estilos próprios (`TituloCapa`, `Instrucao`, `Legenda`, `Fonte`). Sem imagens. No site, o arquivo é oferecido para download sem alterações.

---

## 4. Manual e guia de data science (`data-science-htlm.zip`)

**Pacote:** `manual_machine_learning.html` (estudo e consulta), `skill_decisao_ml.md` (regras de decisão para um agente ou checklist humano), `auditoria_ml.md` (auditoria técnica com 37 achados corrigidos), pasta `auditoria/` (`01_api_sklearn.py`, `02_formulas.py`, `03_executar_snippets.py`, `04_consistencia.py`, `05_api_tf_gymnasium.py`, `06_saidas_esperadas.py`, `rodar_tudo.sh`), `README.md` e `.gitignore`.
**Versão:** v1.0, setembro de 2026; APIs de referência: scikit-learn 1.9.1, XGBoost 3.4.1, LightGBM 4.x, CatBoost 1.2.x, Keras 3, PyTorch 2.x.
**Imagens:** nenhuma. Um único SVG (ícone de busca do cabeçalho).

### 4.1 Estrutura do manual

| Seção | Âncora | Conteúdo | Cartões de modelo |
|---|---|---|---|
| Início | `inicio` | apresentação, 7 indicadores, aviso de versões, legenda de 16 categorias com filtros | – |
| Como usar este manual | `comousar` | tabela de arquivos, trilhas de leitura, como ler um cartão, atalhos, consulta rápida (19 perguntas), uso da skill por agente, convenções | – |
| Diagnóstico do seu dataset | `diagnostico` | ferramenta que lê CSV/TSV/JSON/XLSX no navegador e devolve o diagnóstico de 16 itens e um código inicial; script próprio de 113 KB, com leitor de XLSX e CSV de exemplo | – |
| Parte I · 1. Fundamentos | `s1` | o que é ML, taxonomia, como um modelo aprende, viés–variância, mapa de paradigmas | – |
| Parte II · 2 a 5 | `s2`–`s5` | supervisionado (2.1–2.7), não supervisionado (3.1–3.5), probabilísticos (calibração), redes neurais e TensorFlow (5.1) | 15 + 13 + 1 + 1 |
| Parte III · 6 a 11 | `s6`–`s11` | regularização, otimização e perdas, avaliação e validação (métricas, threshold, validação, leakage), seleção e Model Fit Score, feature engineering, pipeline | – |
| Parte IV · 12 a 15 | `s12`–`s15` | árvore de decisão (hierarquia, IF/THEN, matriz, confrontos, matriz dos sete critérios), estratégias por dataset, 8 casos empresariais, checklist, mitos, nota de auditoria de versões, referências | – |
| Parte V · 16 a 18 | `s16`–`s18` | recomendação, reforço (inclusive baseado em modelo), semissupervisionado | 4 + 6 + 3 |

**Gerado em JavaScript no original:** os 43 cartões de modelo (dados `MODELS`, 20 blocos cada: O que é, Categoria, Problema, Como funciona, Matemática, Quando usar, Quando não usar, Dados, Pré-processamento, Hiperparâmetros, Vantagens, Limitações, Overfitting, Interpretabilidade, Custo, Código Python, Métricas, Concorrentes, Quando preferir outro, Exemplo empresarial), a matriz dos sete critérios (`MATRIZ`) e a legenda (`CATS`, 16 categorias). Total: 860 blocos de cartão, 43 trechos de código nos cartões e 15 blocos de código nas seções.
**Interatividade original:** busca com destaque e abertura de cartões, filtros por categoria combináveis, expandir/recolher, tema claro/escuro, copiar código, cartão aberto por link (`#m-xgboost`), cartões expandidos na impressão, navegação ativa.

### 4.2 Skill e auditoria

- `skill_decisao_ml.md`: cabeçalho YAML (`name`, `description`) e seções 0 a 11 — contrato de execução, restrições taxonômicas, algoritmo de 9 passos, regras IF/THEN (3.1 a 3.13), hierarquia de complexidade, Model Fit Score, template do diagnóstico de 16 itens, exemplo preenchido, guardrails, nota de versões, snippets canônicos e correspondência com o manual.
- `auditoria_ml.md`: estado atual, veredito, ambiente, achados (alta, média, baixa, informativo), evidências, limites, como reproduzir, manutenção e três rodadas posteriores (§8 a §10).

## 5. Sobreposições entre os materiais

| Tema | Notebook | Guia de visualização | Guia de relatório | Relação |
|---|---|---|---|---|
| Sequência de trabalho e iteração | 0 (roteiro rápido) | – | Início (“O trabalho não é linear”) | mesma ideia, textos diferentes |
| Parâmetros de leitura (`sep`, `encoding`, `decimal`…) | 2.1 (tabela com 7 linhas) | – | Etapa 2, fontes (tabela com 5 linhas) | o guia resume a tabela do notebook |
| Dicionário de dados | 2.2 | – | Etapa 2, fontes; modelo Anexo A | complementares |
| Inspeção (estrutura, tipos, nulos, duplicados, categorias) | 3.1–3.6 | – | Etapa 2, inspeção (código resumido) | o guia condensa a seção 3 |
| Estratégias para nulos | 4.3 (tabela com coluna “Código”) | – | Etapa 2, limpeza (mesma tabela sem a coluna de código) | duplicação quase literal |
| Outliers: detectar é técnico, decidir é do negócio | 7 (introdução e 7.4) | – | Etapa 2, alerta “Outliers” | duplicação de ideia |
| Registro de decisões | 0 e 14.4 (detalhamento técnico) | – | Etapa 2, registro de premissas | complementares |
| Tabela descritiva `descritivas()` | 5.5 (versão completa com IQR e lista de colunas) | – | Etapa 3 (versão reduzida, sem IQR) | duas versões da mesma função |
| Escolha da análise pelo tipo das variáveis | 8 (tabela) | – | Etapa 3 (tabela) | o guia resume |
| Qual teste usar | 12.2 (tabela com pós-testes e A/B) | – | Etapa 3 (tabela reduzida) | o guia resume |
| Roteiro de qualquer teste | 12.2 | – | Etapa 3 | quase literal |
| pingouin | 12.11 | – | Etapa 3 (código) | mesmas funções |
| Correlação não é causa, amostras grandes, Shapiro com n grande | 8.1, 12.3 | – | Etapa 3, armadilhas | duplicação de ideia |
| Do resultado ao insight (O quê? É real? Por quê? E daí?) | 14.1 | – | Etapa 3, insights | quase literal |
| Estrutura do relatório | 14.4 (bloco de texto) | – | Etapa 4, anatomia e modelos; `.docx` | o guia expande o notebook |
| Como reportar resultados (modelos de frase) | 14.2 (6 linhas, inclui Correlação) | – | Etapa 5 (5 linhas, sem Correlação) | duplicação parcial |
| Qual gráfico usar | 11.1 (tabela) | Referência rápida, pergunta → gráfico; catálogo | Etapa 5 (tabela) | três tabelas com recortes diferentes |
| Barras em vez de pizza; destaque com cor forte e cinza no resto; evitar arco-íris | 6.5, 11.4 | Partes 3, 4 e 6 | Etapa 5, regras | mesma regra nos três |
| Títulos como conclusão | 14.4 | Antes e depois, “título com a conclusão” | Etapa 5, títulos | mesma regra nos três |
| Estilos, `set_theme`, `despine`, contexto | 1.2, 11.4 | Fundamentos, estilos e rcParams | – | complementares |
| Funções desatualizadas do seaborn/pandas | 11.5 | Fundamentos, atualizações de API | – | listas parcialmente coincidentes |
| Axes-level × figure-level | 11.3 | Fundamentos, seaborn sobre matplotlib | – | complementares |
| Checklist final | 15 | Referência rápida, checklist | listas de verificação das 6 etapas | coincidências parciais |


### 5.1 Sobreposições com o manual de Machine Learning

| Tema | Notebook | Guia de visualização | Guia de relatório | Manual de ML | Relação |
|---|---|---|---|---|---|
| Pré-processamento (escalonamento, codificação, nulos, outliers, criação de features, log) | 4.2–4.9, 7 | – | – | Manual de ML 10.1–10.4 | o manual trata sob a ótica do modelo (quem exige escala, codificação de alta cardinalidade) |
| Regressão linear | 13 (scipy, seaborn, OLS) | Parte 3, cartão “Regressão” | – | Manual de ML 2.1 e cartão “Regressão Linear” | o notebook a usa como ferramenta estatística; o manual, como modelo preditivo |
| Métricas, validação e vazamento | 12 (testes), 4.10 (junções), 9.4 (períodos) | – | – | Manual de ML 8.1–8.4 | complementares; o manual cobre validação de modelos e data leakage |
| Testes A/B e bandits | 12.8 | – | – | Manual de ML 17.4 (“Bandits, A/B ou reforço completo?”) | complementares |
| Pipeline reprodutível | 14.5 | – | – | Manual de ML 11 | mesma ideia em escopos diferentes (exportação × pipeline à prova de vazamento) |
| Checklist final | 15 | Referência rápida | listas de verificação | Manual de ML 15 | quatro checklists com focos distintos |
| Outliers e anomalias | 7 | – | – | Manual de ML 3.3 e 10.3 | o notebook detecta e trata; o manual modela anomalias |

Essas sobreposições foram mantidas no site, porque a regra do projeto é preservar o conteúdo. Cada página que repete um tema aponta para as outras. Divergências pontuais estão registradas em `docs/OBSERVACOES.md`.
