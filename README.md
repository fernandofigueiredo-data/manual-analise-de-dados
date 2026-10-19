# Manual de Análise de Dados

**Guia de referência em português para quem recebe um dataset e precisa ir da importação ao relatório. Todo o código é executado na geração do site e um manual ajuda a decidir qual modelo de Machine Learning usar.**

**[Abrir o site](https://manual-analise-de-dados.vercel.app)** · [Estudo de caso com dados reais](#estudo-de-caso-aviação-comercial-com-dados-da-anac) · [Notebooks](#notebooks) · [Decisões técnicas](docs/DECISOES.md) · [Limites conhecidos](#limites-conhecidos)

![Página inicial do manual no tema escuro: trilha de 7 módulos, 58 páginas, 289 blocos de código e 98 gráficos](docs/capturas/inicio-1440-escuro.png)

## O problema

Quem trabalha com dados em português costuma achar o material espalhado: um tutorial de pandas aqui, um guia de gráficos ali, um template de relatório em outro lugar. Quase sempre o código aparece sem a saída, e nada ajuda a decidir qual modelo usar. Na prática, cada projeto novo começa reconstruindo a mesma base.

Este projeto junta quatro materiais que escrevi numa **trilha única**, que segue a ordem real de um projeto: *importar → conhecer → limpar → descrever → explorar → testar → modelar → comunicar*. Cada trecho de código pode ser copiado e reaproveitado sem retrabalho.

## Estudo de caso: aviação comercial com dados da ANAC

A trilha aplicada a dados reais: **2,75 milhões de voos domésticos** (VRA, jan/2023 a ago/2026), passageiros pagos dos Dados Estatísticos e **238 mil reclamações** do consumidor.gov.br contra Azul, Gol e LATAM, que somam mais de 99 % dos passageiros domésticos.

> **Atraso e cancelamento explicam as reclamações? Quanto cada ponto de pontualidade reduz as reclamações por 100 mil passageiros, e qual companhia converte mais problema operacional em reclamação não resolvida?**

**Três achados**

1. **Cancelar custa caro em reclamação; atrasar 15 minutos, pouco.** No painel companhia × mês, com efeitos de companhia × ano e de mês do calendário, cada ponto percentual a mais de voos cancelados acompanha **+7,0 reclamações por 100 mil passageiros** (IC 95 %: 3,0 a 11,0; cerca de 9 % da média de 80). Um ponto a mais de chegadas atrasadas acompanha +0,41 (IC 95 %: −0,55 a 1,37), que não se distingue de zero. O teste placebo passa: as reclamações de cobrança não respondem ao cancelamento (+0,79; IC 95 %: −0,59 a 2,17).
2. **Quem mais move as reclamações é a companhia no ano, não a operação do mês.** Companhia × ano e mês do calendário explicam 81 % da variação; atraso e cancelamento explicam 28 % do restante. A Azul subiu de 71 para 120 reclamações por 100 mil passageiros entre 2023 e 2025 com pontualidade estável; a Gol melhorou a pontualidade e caiu de 82 para 57.
3. **A Azul é quem mais converte problema operacional em reclamação não resolvida:** 19,8 por mil voos cancelados ou atrasados, contra 18,5 da Gol e 15,6 da LATAM (27 % a mais que a LATAM; IC 95 % da Azul: 19,1 a 20,5). A diferença está no volume de reclamações por voo com problema, não no atendimento: a fração não resolvida é a mesma da LATAM (13,4 %).

![À esquerda, dispersão das reclamações por 100 mil passageiros contra o percentual de voos cancelados, um ponto por companhia e mês, com tendência crescente. À direita, barras com as reclamações operacionais não resolvidas por mil voos com problema: Azul 19,8, Gol 18,5 e LATAM 15,6.](site/public/img/estudo-de-caso/celula-081.webp)

**Recomendações:** para um diretor de operações, tratar o cancelamento como o indicador de experiência que mais pesa (cerca de 194 reclamações a menos por mês para cada ponto evitado, numa companhia média) e usar o modelo de risco de atraso, cujos 10 % de voos de maior risco atrasam 2,1 vezes mais que a média. Para o regulador, voltar a exigir o código de justificativa do atraso no VRA e acompanhar a conversão de voo com problema em reclamação não resolvida.

**Como foi feito:** download reproduzível com tamanho e SHA-256 de cada arquivo ([`baixar_dados.py`](site/gerador/estudo-de-caso/baixar_dados.py)); modelo estrela em DuckDB com o SQL versionado ([`sql/`](site/gerador/estudo-de-caso/sql/)); correção de um defeito real do VRA (horários reais registrados com a data do dia anterior); testes de proporções e qui-quadrado com tamanho de efeito; regressão em painel com erros-padrão HAC e teste placebo; classificador de risco de atraso só com variáveis da malha, validação temporal (teste em jan–ago/2026) e comparação com linhas de base (ROC-AUC 0,65 contra 0,60 da regra companhia × hora).

**[Ler o estudo de caso no site](https://manual-analise-de-dados.vercel.app/estudo-de-caso/aviacao-comercial/)** · [Notebook executado](site/gerador/estudo-de-caso/Estudo_de_Caso_Aviacao_ANAC.ipynb) · [Como reproduzir](site/gerador/estudo-de-caso/LEIAME.md) · Fonte: ANAC (dados abertos)

## O que este projeto demonstra

| Competência | Evidência | Onde ver |
|---|---|---|
| **Diagnosticar falhas em modelos de ML** | revisão de 10 notebooks de estudo com **59 problemas registrados e corrigidos**, entre eles vazamento de dados (escalonadores e médias calculados antes da divisão treino/teste), avaliação feita no próprio treino, softmax numericamente instável e gradiente descendente que não convergia | [`docs/NOTEBOOKS-MODELO.md`](docs/NOTEBOOKS-MODELO.md) |
| **Desenhar validação de modelos** | divisão treino/validação/teste, pré-processamento ajustado só no treino, métricas adequadas ao tipo de problema e comparação com a implementação de referência (scikit-learn ou Keras), em 10 templates validados em **30 cenários** de dados; no estudo de caso, validação temporal sem vazamento e comparação com linhas de base (ROC-AUC, PR-AUC e Brier) | [Notebooks](#notebooks) · [Estudo de caso](https://manual-analise-de-dados.vercel.app/estudo-de-caso/prever-atrasos/) |
| **Análise de negócio com dado real** | 2,75 milhões de voos e 238 mil reclamações da ANAC: pergunta de negócio, KPIs, funil da reclamação, três achados quantificados, recomendações e limites declarados | [Estudo de caso](https://manual-analise-de-dados.vercel.app/estudo-de-caso/aviacao-comercial/) |
| **SQL e modelagem de dados** | modelo estrela em DuckDB (3 fatos, 3 dimensões e uma tabela analítica) com o SQL versionado; regras de qualidade explícitas, como a correção da virada de dia no horário real | [`sql/`](site/gerador/estudo-de-caso/sql/) |
| **Estatística inferencial** | escolha do teste e verificação de pressupostos, testes para dois ou mais grupos, proporções e testes A/B, tamanho de efeito; no estudo de caso, regressão em painel com efeitos fixos, erros-padrão HAC e teste placebo | [Inferir](https://manual-analise-de-dados.vercel.app/inferir/conceitos-e-pressupostos/) · [Estudo de caso](https://manual-analise-de-dados.vercel.app/estudo-de-caso/inferir/) |
| **Métricas de negócio** | KPIs gerais e por segmento, funil, coortes e curva de retenção | [Métricas de negócio](https://manual-analise-de-dados.vercel.app/explorar/metricas-de-negocio/) |
| **Comunicar resultados** | do pedido à entrega: briefing, estrutura do relatório, storytelling com dados e um modelo de relatório em `.docx` | [Comunicar](https://manual-analise-de-dados.vercel.app/comunicar/estruturar-o-relatorio/) |
| **Pipeline reprodutível** | gerador que executa os notebooks e o código dos guias e grava as páginas, com verificação automática de que **10.292 de 10.292** trechos de origem estão no site | [`site/gerador/`](site/gerador/) |

## Notebooks

O notebook mestre e os templates de ML rodam do início ao fim sem configuração, com **dados sintéticos de exemplo**; o estudo de caso usa dados reais da ANAC. Para usar com um dataset próprio, basta preencher a única célula de configuração (caminho do arquivo, coluna-alvo e features).

| Notebook | O que faz | Resultado na validação |
|---|---|---|
| [Estudo de caso: aviação comercial (ANAC)](site/gerador/estudo-de-caso/Estudo_de_Caso_Aviacao_ANAC.ipynb) | a trilha com dados reais: download com hash, modelo estrela em DuckDB, KPIs, funil, testes, regressão em painel e classificador de risco de atraso | executado do download ao relatório em cerca de 2 minutos; versionado com as saídas, sem os dados brutos |
| [Notebook mestre de análise de dados](site/gerador/origem/Notebook_Mestre_Analise_de_Dados.ipynb) | a trilha completa: importação (arquivos e SQL), limpeza, estatística descritiva, análise exploratória, outliers, análise temporal, métricas de negócio, testes de hipótese e checklist | executado inteiro sem erros na geração do site; as saídas e os 98 gráficos estão nas páginas |
| [Regressão linear](site/gerador/origem/modelos-ml/modelo_ml_regressao_linear.ipynb) | gradiente descendente vetorizado para *n* features, com MAE, RMSE, R² e análise de resíduos | coincide com `LinearRegression`; acusa quando o gradiente descendente não chegou ao ótimo |
| [Regressão logística](site/gerador/origem/modelos-ml/modelo_ml_regressao_logistica.ipynb) | sigmoide e log loss com regularização L2, ROC-AUC, PR-AUC, F1 e escolha do limiar | coeficientes iguais aos do scikit-learn (diferença ≤ 0,001) |
| [Rede neural binária](site/gerador/origem/modelos-ml/modelo_ml_rede_neural_binaria.ipynb) | MLP em NumPy e em Keras 3, com early stopping | ROC-AUC 0,97; NumPy e Keras com diferença de ~1e-7 |
| [Rede neural multiclasse](site/gerador/origem/modelos-ml/modelo_ml_rede_neural_multiclasse.ipynb) | softmax numericamente estável, rótulos de texto, matriz de confusão | acurácia 0,93 nos dígitos de 0 a 9 |
| [Regressão polinomial: viés × variância](site/gerador/origem/modelos-ml/modelo_ml_regressao_polinomial_vies_variancia.ipynb) | escolha de grau e λ na validação, com o teste usado uma única vez | reproduz o sobreajuste do modelo complexo |
| [Árvore de decisão](site/gerador/origem/modelos-ml/modelo_ml_arvore_de_decisao.ipynb) | implementação do zero com entropia ou Gini, features numéricas e regras SE…ENTÃO | acurácia próxima à do scikit-learn |
| [Detecção de anomalias gaussiana](site/gerador/origem/modelos-ml/modelo_ml_deteccao_anomalias_gaussiana.ipynb) | densidade em log (sem underflow), limiar escolhido na validação e avaliado no teste | F1 de teste 1,0 nos três cenários rotulados; equivale ao `GaussianMixture` |
| [K-Means](site/gerador/origem/modelos-ml/modelo_ml_kmeans.ipynb) | k-means++, várias inicializações, cotovelo e silhouette, compressão de imagem | índice de Rand ajustado 1,0; inércia igual à do scikit-learn |
| [Recomendação por conteúdo](site/gerador/origem/modelos-ml/modelo_ml_recomendacao_conteudo_rede_neural.ipynb) | rede de duas torres, sem vazamento, com precision@k, recall@k e NDCG@k | NDCG@10 de 0,054 contra 0,020 da recomendação por popularidade |
| [Deep Q-Network](site/gerador/origem/modelos-ml/modelo_ml_dqn.ipynb) | DQN com replay e rede-alvo em Gymnasium, checkpoint dos melhores pesos | retorno 500 (o máximo) no CartPole com 3 sementes |

Os 10 notebooks de ML foram reescritos a partir de exercícios de um curso, com a origem indicada no cabeçalho de cada um. Os detalhes estão em [`docs/NOTEBOOKS-MODELO.md`](docs/NOTEBOOKS-MODELO.md).

## O que o site entrega

| Material | Conteúdo |
|---|---|
| **Notebook mestre de análise de dados** | a espinha dorsal da trilha, com o código e as saídas da execução |
| **Guia matplotlib e seaborn** | fundamentos, catálogo de 16 gráficos, antes e depois, storytelling com dados e erros comuns |
| **Guia do relatório profissional** | briefing, listas de verificação, modelos de texto e modelo de relatório em `.docx` |
| **Manual de Machine Learning** | 43 modelos em cartões de 20 blocos, árvore e matriz de decisão, validação, skill de decisão e auditoria técnica |
| **Diagnóstico de dataset no navegador** | lê um CSV, XLSX ou JSON e devolve um diagnóstico e um código inicial; o arquivo **não sai do computador** de quem usa |

## Qualidade do site

- **Fidelidade:** 10.292 de 10.292 trechos de texto e código dos materiais estão no site, nenhum ausente ([`verificacao-conteudo.json`](docs/qualidade/verificacao-conteudo.json)).
- **Acessibilidade (WCAG 2.2 AA):** axe-core em 73 páginas e nos dois temas, 0 violações; 21 de 21 passos de navegação por teclado ([`acessibilidade-axe.json`](docs/qualidade/acessibilidade-axe.json)).
- **Lighthouse** em 9 páginas, celular e desktop: desempenho de 98 a 99; acessibilidade, boas práticas e SEO 100 ([`RESUMO.md`](docs/qualidade/lighthouse/RESUMO.md)).
- **Consistência visual:** o build falha se aparecer qualquer cor, fonte ou espaçamento fora dos tokens do design system ([`verificar-tokens.mjs`](site/scripts/verificar-tokens.mjs)).

## Decisões técnicas

| Decisão | Por quê |
|---|---|
| **Astro** em modo estático, sem framework de interface no navegador | HTML puro e rápido; só o JavaScript de cada página é enviado. Starlight e Docusaurus foram descartados porque trazem CSS próprio, o que violaria a regra de "nenhum valor fora dos tokens" |
| **Pagefind** para a busca | índice estático gerado no build, carregado sob demanda, com radical da língua portuguesa e destaque do termo na página de destino. Não precisa de servidor |
| **Gerador em Python** (com um extrator em Node) | os materiais são notebooks, scripts e HTML. O gerador executa o código e grava as páginas em JSON, sem reescrever o conteúdo; o código exibido é sempre o original |
| **Conteúdo gerado versionado** | `npm run build` não depende de Python nem de rede, o que deixa o deploy na Vercel simples e reprodutível |
| **Diagnóstico 100 % no navegador** | privacidade: o dataset de quem usa nunca é enviado a um servidor |

Registro completo, com alternativas descartadas: [`docs/DECISOES.md`](docs/DECISOES.md).

## Como funciona

```mermaid
flowchart LR
    A["Materiais de origem<br/>notebook, guias, manual de ML"] --> B["Gerador Python + Node<br/>executa o código"]
    B --> C["Páginas JSON<br/>+ 108 gráficos WebP"]
    C --> D["Astro<br/>site estático"]
    D --> E["Pagefind<br/>índice de busca"]
    E --> F["Vercel"]
```

## Como este projeto foi feito

Os quatro materiais de origem e o design system são de minha autoria. O site, o gerador, as auditorias e a revisão dos notebooks de ML foram construídos com o **Claude Code** (assistente de programação da Anthropic), sob a minha direção. Por isso o Claude aparece como co-autor nos commits.

As decisões foram minhas:

- o recorte: reunir os quatro materiais numa trilha única, com o notebook mestre como espinha dorsal;
- a regra de preservar o conteúdo dos materiais sem perda, que a verificação automática de 10.292 trechos garante;
- o design system e a exigência de que nenhum valor visual fique fora dos tokens;
- as mudanças de escopo no meio do projeto: incluir o manual de Machine Learning, trocar o design system e regenerar os gráficos no tema escuro;
- o que fica fora do repositório público: os exercícios originais do curso, que não pertencem a mim, e os dados brutos da ANAC, que são baixados por script;
- o estudo de caso com dados da ANAC, escolhido entre cinco fontes públicas, e a pergunta de negócio que ele responde.

Tudo o que entrou passou pelas verificações descritas em [Qualidade do site](#qualidade-do-site), e os limites estão declarados logo abaixo.

## Limites conhecidos

Declarados de propósito, com detalhes em [`docs/OBSERVACOES.md`](docs/OBSERVACOES.md):

- **O manual roda sobre dados sintéticos.** O notebook mestre e os templates de ML usam dados de exemplo gerados por código; o dado real fica no [estudo de caso](#estudo-de-caso-aviação-comercial-com-dados-da-anac), que é um só.
- **Limites do estudo de caso:** o VRA não informa a causa do atraso desde 2020 (não dá para separar clima de gestão); voos e reclamações só se ligam no nível companhia × mês (risco de falácia ecológica); 49,6 % das reclamações de 2025 não foram avaliadas pelo consumidor; o painel tem 108 observações, porque as reclamações publicadas vão até dez/2025.
- O site reproduz os materiais **como estão**: os erros e as duplicações encontrados foram registrados, não corrigidos no conteúdo. A consolidação dos trechos repetidos ainda não foi feita.
- Os scripts da auditoria do manual de ML não foram reexecutados na montagem do site; os números da auditoria são os declarados nela.
- O diagnóstico de dataset foi testado com CSV; ainda falta testar com arquivos XLSX e JSON reais.
- Cinco trechos do guia de visualização atribuídos a referências externas estão marcados como "a confirmar".

## Estrutura do repositório

```
manual-analise-de-dados/
├── site/                  site Astro (pasta publicada na Vercel)
│   ├── src/               páginas, layout, componentes, estilos e conteúdo gerado
│   ├── public/            gráficos, fontes e downloads (.ipynb, .docx, .md)
│   ├── gerador/           gerador Python/Node
│   │   ├── origem/        materiais de origem: notebook mestre, guias e modelos-ml/
│   │   └── estudo-de-caso/ notebook, SQL, download e agregados do estudo de caso (ANAC)
│   ├── scripts/           verificação de tokens, acessibilidade, Lighthouse e capturas
│   └── design-system/     especificação do design system
└── docs/                  decisões, arquitetura, design system, inventário,
                           observações, revisão dos notebooks e resultados das auditorias
```

## Rodar localmente

Requisito: Node 20 ou mais recente (testado com o 24).

```bash
cd site
npm ci
npm run build
npm run preview
```

O site abre em `http://localhost:4321`. Para regenerar o conteúdo a partir dos materiais de origem (exige Python) e rodar as auditorias, veja [`site/README.md`](site/README.md).

## Licença

- **Código** (site, gerador, scripts e todo bloco de código dos materiais): [MIT](LICENSE).
- **Conteúdo** (textos, gráficos, guias, modelo de relatório e documentação): [CC BY 4.0](LICENSE-CONTEUDO.md).
- Exceções de terceiros (fontes e origem dos notebooks modelo) estão em [`LICENSE-CONTEUDO.md`](LICENSE-CONTEUDO.md).

## Autor

**Fernando Figueiredo**, autor dos quatro materiais e do site.
