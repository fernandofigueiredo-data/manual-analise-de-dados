# Arquitetura da informação

## 1. Princípio

O site é uma **trilha de aprendizado de análise de dados** com o notebook mestre como espinha dorsal: a ordem dos módulos e das páginas segue a ordem das seções do notebook (0 a 15), que já é a ordem de um projeto real (importar → conhecer → limpar → descrever → explorar → testar → comunicar). Os outros três materiais entram nos pontos em que se aplicam:

- o **guia do relatório profissional** acompanha o projeto do começo ao fim: a introdução e a etapa 1 (entender a demanda) abrem a trilha, antes de qualquer código; as etapas 2 e 3 fecham os módulos “Preparar” e “Inferir” como versão “para o relatório” do que acabou de ser feito; as etapas 4 a 6 formam o módulo “Comunicar” junto com a seção 14 do notebook;
- o **guia de matplotlib e seaborn** forma o módulo “Visualizar”, logo depois da seção 11 do notebook (“Visualização: referência técnica”), que é o ponto em que o notebook para de usar gráficos como ferramenta e passa a tratá-los como assunto;
- o **manual de Machine Learning** (com a skill de decisão e a auditoria) forma o módulo “Machine Learning”, entre “Inferir” e “Comunicar”: depois da regressão linear como ferramenta estatística (seção 13 do notebook), a trilha passa à modelagem preditiva, e só então volta à comunicação dos resultados (seção 14). Dentro do módulo, a ordem é a do próprio manual (Início; Partes I a V), seguida da skill e da auditoria.

Depois do módulo “Comunicar”, o **estudo de caso** (módulo 7) percorre a mesma trilha com dados reais da ANAC: é o único conteúdo escrito para o site, e o seu notebook fica em `site/gerador/estudo-de-caso/`.

O conteúdo dos quatro materiais não foi reescrito. Páginas novas (início, abertura de módulo, sobre) contêm apenas navegação, títulos e informações sobre o próprio site.

## 2. Mapa do site

```text
/                                        Início
├── /comecar/                            Módulo 0 · Começar
│   ├── como-usar/                       Como usar este manual            (notebook: abertura)
│   ├── roteiro-rapido/                  0. Roteiro rápido                 (notebook §0)
│   ├── relatorio-profissional/          O relatório como fio condutor     (guia de relatório: início)
│   └── entender-a-demanda/              Entender a demanda                (guia de relatório: etapa 1)
├── /preparar/                           Módulo 1 · Preparar os dados
│   ├── configuracao-do-ambiente/        1. Configuração do ambiente       (notebook §1)
│   ├── importacao-dos-dados/            2. Importação dos dados           (notebook §2.1–2.2)
│   ├── consultas-sql/                   2.3 Consultas SQL                 (notebook §2.3)
│   ├── primeira-inspecao/               3. Primeira inspeção              (notebook §3)
│   ├── limpeza-e-tratamento/            4. Limpeza e tratamento           (notebook §4)
│   └── preparar-os-dados-no-relatorio/  Preparar os dados (relatório)     (guia de relatório: etapa 2)
├── /explorar/                           Módulo 2 · Explorar
│   ├── estatistica-descritiva/          5. Estatística descritiva         (notebook §5)
│   ├── analise-univariada/              6. Análise univariada             (notebook §6)
│   ├── outliers/                        7. Outliers                       (notebook §7)
│   ├── analise-bivariada-e-multivariada/ 8. Bivariada e multivariada      (notebook §8)
│   ├── analise-temporal/                9. Análise temporal               (notebook §9)
│   └── metricas-de-negocio/             10. Métricas de negócio           (notebook §10)
├── /visualizar/                         Módulo 3 · Visualizar
│   ├── referencia-tecnica/              11. Visualização: referência técnica (notebook §11)
│   ├── guia-matplotlib-seaborn/         Guia matplotlib e seaborn         (guia de visualização: como usar)
│   ├── fundamentos/                     Parte 1 · Fundamentos
│   ├── eixos-de-knaflic/                Parte 2 · Os seis eixos de Knaflic
│   ├── catalogo-de-graficos/            Parte 3 · Catálogo de gráficos
│   ├── antes-e-depois/                  Parte 4 · Antes e depois
│   ├── roteiro-de-montagem/             Parte 5 · Roteiro de montagem
│   ├── erros-comuns/                    Parte 6 · Erros comuns
│   └── referencia-rapida/               Parte 7 · Referência rápida
├── /inferir/                            Módulo 4 · Inferir
│   ├── conceitos-e-pressupostos/        12.1–12.3                         (notebook §12)
│   ├── testes-de-hipotese/              12.4–12.7                         (notebook §12)
│   ├── proporcoes-e-testes-ab/          12.8                              (notebook §12)
│   ├── efeito-e-automacao/              12.9–12.11                        (notebook §12)
│   ├── regressao-linear/                13. Regressão linear              (notebook §13)
│   └── analisar-no-relatorio/           Analisar (relatório)              (guia de relatório: etapa 3)
├── /modelar/                            Módulo 5 · Machine Learning
│   ├── manual-de-machine-learning/      Apresentação, legenda e Como usar   (manual de ML: início e “Como usar”)
│   ├── diagnostico-do-dataset/          Diagnóstico do seu dataset          (manual de ML: ferramenta no navegador)
│   ├── fundamentos/                     1. Fundamentos                      (Parte I — Base)
│   ├── aprendizado-supervisionado/      2. Aprendizado supervisionado       (Parte II — Modelos; 15 cartões)
│   ├── aprendizado-nao-supervisionado/  3. Não supervisionado               (13 cartões)
│   ├── metodos-probabilisticos/         4. Métodos probabilísticos          (1 cartão)
│   ├── redes-neurais-e-deep-learning/   5. Redes neurais e Deep Learning    (1 cartão)
│   ├── regularizacao/                   6. Regularização                    (Parte III — Treinamento)
│   ├── otimizacao-e-funcoes-de-perda/   7. Otimização e funções de perda
│   ├── avaliacao-e-validacao/           8. Avaliação e validação
│   ├── selecao-de-modelos/              9. Seleção de modelos e tuning
│   ├── feature-engineering/             10. Feature Engineering
│   ├── pipeline-ponta-a-ponta/          11. Pipeline ponta a ponta
│   ├── arvore-de-decisao-de-modelos/    12. Árvore de decisão de modelos    (Parte IV — Decisão; matriz dos 7 critérios)
│   ├── estrategias-por-dataset/         13. Estratégias por dataset
│   ├── casos-praticos/                  14. Casos práticos empresariais
│   ├── checklist-profissional/          15. Checklist profissional e nota de auditoria
│   ├── sistemas-de-recomendacao/        16. Sistemas de recomendação        (Parte V; 4 cartões)
│   ├── aprendizagem-por-reforco/        17. Aprendizagem por reforço        (6 cartões)
│   ├── aprendizagem-semissupervisionada/ 18. Semissupervisionado            (3 cartões)
│   ├── skill-de-decisao/                Skill de decisão                    (skill_decisao_ml.md)
│   └── auditoria-tecnica/               Auditoria técnica                   (auditoria_ml.md e scripts)
├── /comunicar/                          Módulo 6 · Comunicar
│   ├── insights-e-comunicacao/          14. Insights e comunicação        (notebook §14)
│   ├── estruturar-o-relatorio/          Estruturar o relatório            (guia de relatório: etapa 4)
│   ├── comunicar-resultados/            Comunicar                         (guia de relatório: etapa 5)
│   ├── revisar-e-entregar/              Revisar e entregar                (guia de relatório: etapa 6)
│   └── checklist-final/                 15. Checklist final               (notebook §15)
├── /estudo-de-caso/                     Módulo 7 · Estudo de caso: aviação (dados reais da ANAC)
│   ├── aviacao-comercial/               Pergunta, achados e limites         (notebook do estudo de caso: §0, §11 e §12)
│   ├── preparar-os-dados/               Preparar: download, SQL e qualidade (§1 a §4)
│   ├── explorar/                        Explorar: KPIs e funil              (§5 a §7)
│   ├── inferir/                         Inferir: testes e regressão         (§8 e §9)
│   └── prever-atrasos/                  Machine Learning: risco de atraso   (§10)
├── /sobre/                              Sobre o site e os materiais de origem
└── /downloads/                          modelo_relatorio_dados.docx · Notebook_Mestre_Analise_de_Dados.ipynb · skill_decisao_ml.md · auditoria_ml.md
                                         · 10 notebooks modelo de ML (modelo_ml_*.ipynb, seção 5.5)
                                         · Estudo_de_Caso_Aviacao_ANAC.ipynb (executado, com as saídas)
```

Total: 1 página inicial, 8 aberturas de módulo, 63 páginas de conteúdo (21 do notebook, 9 do guia de visualização, 6 do guia de relatório, 22 do pacote de Machine Learning e 5 do estudo de caso), 1 página “Sobre” e 1 página 404.

## 3. Navegação

| Elemento | Comportamento |
|---|---|
| Cabeçalho fixo | marca (leva ao início), busca global (botão e atalhos `/` e `Ctrl/⌘ K`), alternador de tema, botão de menu abaixo de 768 px |
| Navegação lateral | oito módulos na ordem da trilha (os sete da trilha e o estudo de caso), cada um recolhível, com as páginas numeradas como no material de origem; no módulo Machine Learning, as páginas ficam agrupadas pelas partes do manual (Início, Parte I a V, Skill e auditoria); página atual marcada com `aria-current="page"`; “Sobre” no fim. No celular, gaveta com véu, fecha com Esc |
| Índice da página | lista dos h2 e h3 da página, com realce da seção visível; coluna à direita a partir de 1200 px, bloco recolhível “Nesta página” abaixo disso |
| Trilha de navegação | “Início › Módulo › Página” no topo de cada página |
| Anterior / próxima | no fim de cada página, na ordem da trilha, atravessando módulos |
| Origem | rodapé de cada página indica de qual material e de qual trecho veio o conteúdo |
| Referências cruzadas | “Seção 4.2” e “Seções 6.4 e 12.3” do notebook viram links para a âncora correspondente; links internos dos guias (`#r-estilo`, `#modelo-secoes`…) são reescritos para a página certa |
| Busca | índice estático (Pagefind) com todas as páginas; resultados com título, trecho e link para a âncora mais próxima; na página de destino, os termos buscados ficam destacados e os cartões de modelo que os contêm abrem sozinhos (como na busca do manual de ML original) |

## 4. Páginas e tipos de conteúdo

| Tipo | Páginas | Componentes principais |
|---|---|---|
| Início | `/` | herói, indicadores, trilha (índice do notebook com links), materiais de origem |
| Abertura de módulo | `/comecar/` … `/comunicar/` | lista das páginas do módulo com a pergunta que cada uma responde |
| Notebook | 21 páginas | texto, tabelas, fórmulas (MathML), blocos de código com copiar, saídas (texto, tabela, figura), callouts “O que observar”, “Alternativa”, “Complemento” |
| Guia de visualização | 9 páginas | cartões de gráfico com abas matplotlib/seaborn, realce de linhas por eixo, antes/depois, passos, filtros do catálogo |
| Guia de relatório | 6 páginas | listas de verificação com progresso, briefing com resumo copiável, comparativos fraco × forte, modelos copiáveis, relatório-modelo, gráficos SVG |
| Manual de ML | 20 páginas | seções estáticas, 43 cartões de modelo recolhíveis (20 blocos cada), legenda de categorias que filtra o índice dos modelos, matriz dos sete critérios, expandir/recolher |
| Diagnóstico de dataset | 1 página | ferramenta original do manual, que roda no navegador: arquivo CSV/TSV/JSON/XLSX → diagnóstico de 16 itens e código inicial |
| Skill e auditoria | 2 páginas | documentos Markdown, cabeçalho YAML da skill, scripts da auditoria recolhíveis, downloads |
| Sobre | `/sobre/` | créditos, como o site é gerado, nota sobre as figuras, materiais para download |

## 5. Correspondência origem → página

Todo trecho dos quatro materiais aparece em exatamente uma página. Onde o conteúdo foi dividido, a divisão acompanha os títulos de origem.

### 5.1 Notebook mestre (267 células)

| Células | Trecho de origem | Página |
|---|---|---|
| 0 | Título, subtítulo e pergunta de abertura | `/` (herói) |
| 0 | Formato dos tópicos, convenções do template, tabelas de colunas e de tabelas auxiliares, legenda 🔹/➕ | `/comecar/como-usar/` |
| 1 | Índice (seções 0 a 15 e perguntas) | `/` (trilha) e aberturas de módulo (pergunta de cada seção) |
| 2 | 0. Roteiro rápido | `/comecar/roteiro-rapido/` |
| 3–12 | 1. Configuração do ambiente (1.1–1.4) | `/preparar/configuracao-do-ambiente/` |
| 13–16 | 2. Importação dos dados: 2.1 Leitura, parâmetros de leitura, 2.2 Dicionário | `/preparar/importacao-dos-dados/` |
| 17–29 | 2.3 Consultas SQL ➕ e equivalências SQL ↔ pandas | `/preparar/consultas-sql/` |
| 30–49 | 3. Primeira inspeção (3.1–3.6) | `/preparar/primeira-inspecao/` |
| 50–78 | 4. Limpeza e tratamento (4.1–4.10) | `/preparar/limpeza-e-tratamento/` |
| 79–102 | 5. Estatística descritiva (5.1–5.7) | `/explorar/estatistica-descritiva/` |
| 103–118 | 6. Análise univariada (6.1–6.5) | `/explorar/analise-univariada/` |
| 119–129 | 7. Outliers (7.1–7.4) | `/explorar/outliers/` |
| 130–163 | 8. Análise bivariada e multivariada (8.1–8.6) | `/explorar/analise-bivariada-e-multivariada/` |
| 164–176 | 9. Análise temporal (9.1–9.4) | `/explorar/analise-temporal/` |
| 177–190 | 10. Métricas de negócio ➕ (10.1–10.4) | `/explorar/metricas-de-negocio/` |
| 191–202 | 11. Visualização: referência técnica (11.1–11.5) | `/visualizar/referencia-tecnica/` |
| 203–211 | 12. Estatística inferencial: 12.1 Conceitos, 12.2 Qual teste, 12.3 Pressupostos | `/inferir/conceitos-e-pressupostos/` |
| 212–226 | 12.4 Um grupo, 12.5 Dois grupos, 12.6 Três ou mais, 12.7 Qui-quadrado ➕ | `/inferir/testes-de-hipotese/` |
| 227–231 | 12.8 Proporções e testes A/B ➕ | `/inferir/proporcoes-e-testes-ab/` |
| 232–243 | 12.9 Efeito e IC, 12.10 Fluxo automatizado, 12.11 pingouin | `/inferir/efeito-e-automacao/` |
| 244–255 | 13. Regressão linear (13.1–13.4) | `/inferir/regressao-linear/` |
| 256–265 | 14. Insights e comunicação (14.1–14.5) | `/comunicar/insights-e-comunicacao/` |
| 266 | 15. Checklist final | `/comunicar/checklist-final/` |
| arquivo | `Notebook_Mestre_Analise_de_Dados.ipynb` | `/downloads/` (cópia sem alterações, link em `/sobre/`) |

### 5.2 Guia matplotlib e seaborn

| Trecho de origem | Página |
|---|---|
| Como usar este guia (`inicio`): apresentação, três cartões, convenções | `/visualizar/guia-matplotlib-seaborn/` |
| Parte 1 · Fundamentos: anatomia, interfaces, estilos e rcParams, seaborn sobre matplotlib, quando usar cada um, atualizações de API (8 figuras) | `/visualizar/fundamentos/` |
| Parte 2 · Os seis eixos de Knaflic: seis cartões com “onde aparece no código” | `/visualizar/eixos-de-knaflic/` |
| Parte 3 · Catálogo: introdução, situações, 16 cartões (29 figuras), filtros e busca da barra lateral | `/visualizar/catalogo-de-graficos/` |
| Parte 4 · Antes e depois: bordas, cor, rótulos, título, anotações (10 figuras) | `/visualizar/antes-e-depois/` |
| Parte 5 · Roteiro de montagem: contexto, grande ideia, storyboard, narrativa, montagem (5 figuras) | `/visualizar/roteiro-de-montagem/` |
| Parte 6 · Erros comuns: eixo truncado, 3D, eixo secundário, excesso de cores (8 figuras) | `/visualizar/erros-comuns/` |
| Parte 7 · Referência rápida: pergunta → gráfico, estilo reutilizável (2 figuras), checklist, fontes e créditos | `/visualizar/referencia-rapida/` |
| Rodapé do guia (gerado em Python, crédito a Knaflic) | `/visualizar/guia-matplotlib-seaborn/` (fim da página) |
| `README.md`: conteúdo, estrutura do repositório, como gerar, versões, créditos | `/sobre/` |
| Código-fonte (`build.py`, `kit.py`, módulos, `estilo.css`, `app.js`) | não publicado como página; reutilizado pelo gerador do site (`site/gerador/`) |

### 5.3 Guia do relatório profissional

| Trecho de origem | Página |
|---|---|
| Como usar este guia: apresentação, modelo `.docx`, as seis etapas, como usar, nota sobre os dados | `/comecar/relatorio-profissional/` |
| Etapa 1 · Entender a demanda: perguntas, declaração do problema, exemplo, briefing, escopo e prazo, lista de verificação | `/comecar/entender-a-demanda/` |
| Etapa 2 · Preparar os dados: fontes, inspeção, limpeza, validações, outliers, registro de premissas, lista | `/preparar/preparar-os-dados-no-relatorio/` |
| Etapa 3 · Analisar: descrever, escolher a análise, qual teste, roteiro, sustenta/não sustenta, armadilhas, exemplo, insight, lista | `/inferir/analisar-no-relatorio/` |
| Etapa 4 · Estruturar o relatório: anatomia, modelo de texto por seção, relatório-modelo fictício, lista | `/comunicar/estruturar-o-relatorio/` |
| Etapa 5 · Comunicar: narrativa, títulos, gráficos e tabelas, linguagem, detalhamento técnico, lista | `/comunicar/comunicar-resultados/` |
| Etapa 6 · Revisar e entregar: revisão, formato e canal, apresentar, ajustes, lista final, rodapé | `/comunicar/revisar-e-entregar/` |
| Barra lateral: progresso geral, baixar modelo, imprimir | cabeçalho de cada página do guia (baixar e imprimir); progresso por lista |
| `modelo_relatorio_dados.docx` | `/downloads/` (cópia sem alterações, links nas páginas do guia) |
| `README.md`: arquivos, como usar, observações | `/sobre/` |

### 5.4 Manual e guia de data science (`data-science-htlm.zip`)

| Trecho de origem | Página |
|---|---|
| `manual_machine_learning.html`, cabeçalho (marca, versão, busca, expandir/recolher, tema) | sobretítulo da página de apresentação; busca global; botões “Expandir/Recolher” nas páginas com cartões; tema no cabeçalho do site |
| Início: título, apresentação, indicadores, aviso de versões, legenda de categorias e filtros | `/modelar/manual-de-machine-learning/` (com o índice dos 43 modelos, que a legenda filtra) |
| Como usar este manual (§1 a §4, atalhos, trilhas, consulta, agente, convenções) | `/modelar/manual-de-machine-learning/#comousar` |
| Diagnóstico do seu dataset (texto, formulário e script do diagnóstico) | `/modelar/diagnostico-do-dataset/` |
| Seção 1 · Fundamentos | `/modelar/fundamentos/` |
| Seção 2 · Supervisionado + cartões dos grupos lineares, árvores, ensemble, boosting, instância | `/modelar/aprendizado-supervisionado/` |
| Seção 3 · Não supervisionado + cartões de clustering, redução, anomalias, densidade, associação | `/modelar/aprendizado-nao-supervisionado/` |
| Seção 4 · Probabilísticos + cartão | `/modelar/metodos-probabilisticos/` |
| Seção 5 · Redes neurais, 5.1 TensorFlow + cartão | `/modelar/redes-neurais-e-deep-learning/` |
| Seções 6 a 11 | `/modelar/regularizacao/`, `/otimizacao-e-funcoes-de-perda/`, `/avaliacao-e-validacao/`, `/selecao-de-modelos/`, `/feature-engineering/`, `/pipeline-ponta-a-ponta/` |
| Seção 12 · Árvore de decisão, regras IF/THEN, matriz de decisão, comparações, 12.5 matriz dos sete critérios (gerada dos dados `MATRIZ`) | `/modelar/arvore-de-decisao-de-modelos/` |
| Seções 13 e 14 | `/modelar/estrategias-por-dataset/`, `/modelar/casos-praticos/` |
| Seção 15 · Checklist, mitos, nota de auditoria de versões, referências | `/modelar/checklist-profissional/` |
| Seção 16 · Recomendação + cartões | `/modelar/sistemas-de-recomendacao/` |
| Seção 17 · Reforço + cartões de reforço e reforço baseado em modelo, referências das seções 16 e 17 | `/modelar/aprendizagem-por-reforco/` |
| Seção 18 · Semissupervisionado + cartões | `/modelar/aprendizagem-semissupervisionada/` |
| Dados `MODELS` (43 modelos × 20 blocos, nome, resumo, etiquetas) e `CATS`/`BLOCKS` | cartões nas páginas das seções 2, 3, 4, 5, 16, 17 e 18; índice dos modelos na apresentação |
| `skill_decisao_ml.md` (cabeçalho YAML e §0 a §11) | `/modelar/skill-de-decisao/` e `/downloads/skill_decisao_ml.md` |
| `auditoria_ml.md` (§0 a §10) | `/modelar/auditoria-tecnica/` e `/downloads/auditoria_ml.md` |
| `auditoria/01` a `06` e `rodar_tudo.sh` | `/modelar/auditoria-tecnica/#scripts-da-auditoria` |
| `README.md` e `.gitignore` do pacote | `/sobre/` |

### 5.5 Notebooks modelo de Machine Learning

10 notebooks de estudo (exercícios da *Machine Learning Specialization*, que não estão neste repositório) foram revisados, corrigidos e transformados em templates genéricos (`site/gerador/origem/modelos-ml/`). Cada template fica para download no cartão do modelo correspondente, num bloco “Notebook modelo” no topo do cartão, e na página Sobre. Nenhum cartão novo foi criado. Revisão completa: `docs/NOTEBOOKS-MODELO.md`.

| Notebook de origem | Template (`/downloads/`) | Cartão |
|---|---|---|
| `C1_W2_Linear_Regression.ipynb` | `modelo_ml_regressao_linear.ipynb` | `/modelar/aprendizado-supervisionado/#m-linear-regression` |
| `C1_W3_Logistic_Regression.ipynb` | `modelo_ml_regressao_logistica.ipynb` | `/modelar/aprendizado-supervisionado/#m-logistic` |
| `C2_W1_Assignment.ipynb` | `modelo_ml_rede_neural_binaria.ipynb` | `/modelar/redes-neurais-e-deep-learning/#m-mlp` |
| `C2_W2_Assignment.ipynb` | `modelo_ml_rede_neural_multiclasse.ipynb` | `/modelar/redes-neurais-e-deep-learning/#m-mlp` |
| `C2_W3_Assignment.ipynb` | `modelo_ml_regressao_polinomial_vies_variancia.ipynb` | `/modelar/aprendizado-supervisionado/#m-polynomial` |
| `C2_W4_Decision_Tree_with_Markdown.ipynb` | `modelo_ml_arvore_de_decisao.ipynb` | `/modelar/aprendizado-supervisionado/#m-decision-tree` |
| `C3_W1_Anomaly_Detection.ipynb` | `modelo_ml_deteccao_anomalias_gaussiana.ipynb` | `/modelar/aprendizado-nao-supervisionado/#m-gmm` |
| `C3_W1_KMeans_Assignment.ipynb` | `modelo_ml_kmeans.ipynb` | `/modelar/aprendizado-nao-supervisionado/#m-kmeans` |
| `C3_W2_RecSysNN_Assignment.ipynb` | `modelo_ml_recomendacao_conteudo_rede_neural.ipynb` | `/modelar/sistemas-de-recomendacao/#m-content-based` |
| `C3_W3_A1_Assignment.ipynb` | `modelo_ml_dqn.ipynb` | `/modelar/aprendizagem-por-reforco/#m-dqn` |

## 6. URLs e âncoras

- URLs em minúsculas, sem acento, com barra final.
- Âncoras do notebook: `secao-<número>` (por exemplo `#secao-4-2`), criadas a partir dos títulos “## 4.2 …”, para que “Seção 4.2” sempre aponte para o mesmo lugar.
- Âncoras dos guias: as originais (`#g-linha`, `#modelo-secoes`, `#etapa-3`…), preservadas para que links antigos continuem válidos dentro das páginas.
- Âncoras do manual de ML: as originais (`#s8-4`, `#comousar-agente`, `#auditoria`, `#matriz7`) e as dos cartões (`#m-xgboost`, `#m-kmeans`…), como no manual. Títulos que não tinham âncora ganharam uma a partir do texto. Links para `skill_decisao_ml.md` e `manual_machine_learning.html#…` apontam para as páginas correspondentes.
