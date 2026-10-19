# Notebooks modelo de Machine Learning: revisão e generalização

Revisão feita em 06/10/2026. Dez notebooks de estudo foram analisados, comparados com o cartão do modelo correspondente na seção **Machine Learning** do site, corrigidos e transformados em templates genéricos (`site/gerador/origem/modelos-ml/`), que podem ser baixados no cartão de cada modelo e na página **Sobre**.

Os originais são exercícios da *Machine Learning Specialization* (DeepLearning.AI e Stanford Online). Eles **não foram alterados** e, por serem material do curso, **não estão neste repositório**; os nomes dos arquivos aparecem abaixo só para indicar a origem de cada template.

## 1. Resumo

| Notebook original | O que é | Cartão no sistema | Problemas | Template genérico |
|---|---|---|:---:|---|
| `C1_W2_Linear_Regression.ipynb` | regressão linear com 1 variável, gradiente descendente do zero | *Regressão Linear* (`/modelar/aprendizado-supervisionado/#m-linear-regression`) | 6 | `modelo_ml_regressao_linear.ipynb` |
| `C1_W3_Logistic_Regression.ipynb` | regressão logística do zero, sem e com regularização L2 | *Regressão Logística* (`#m-logistic`) | 6 | `modelo_ml_regressao_logistica.ipynb` |
| `C2_W1_Assignment.ipynb` | rede neural binária (dígitos 0 e 1) em TensorFlow e NumPy | *Rede Neural (MLP)* (`/modelar/redes-neurais-e-deep-learning/#m-mlp`) | 5 | `modelo_ml_rede_neural_binaria.ipynb` |
| `C2_W2_Assignment.ipynb` | rede neural multiclasse (dígitos 0 a 9), ReLU e softmax | *Rede Neural (MLP)* (`#m-mlp`) | 5 | `modelo_ml_rede_neural_multiclasse.ipynb` |
| `C2_W3_Assignment.ipynb` | avaliação de modelos: treino/CV/teste, viés × variância, grau, λ, complexidade de rede | *Regressão Polinomial* (`/modelar/aprendizado-supervisionado/#m-polynomial`) | 7 | `modelo_ml_regressao_polinomial_vies_variancia.ipynb` |
| `C2_W4_Decision_Tree_with_Markdown.ipynb` | árvore de decisão do zero (entropia, ganho de informação) | *Decision Tree* (`#m-decision-tree`) | 5 | `modelo_ml_arvore_de_decisao.ipynb` |
| `C3_W1_Anomaly_Detection.ipynb` | detecção de anomalias por densidade gaussiana | *Gaussian Mixture Model (GMM)* (`/modelar/aprendizado-nao-supervisionado/#m-gmm`) | 5 | `modelo_ml_deteccao_anomalias_gaussiana.ipynb` |
| `C3_W1_KMeans_Assignment.ipynb` | K-Means do zero e compressão de imagem | *K-Means* (`#m-kmeans`) | 6 | `modelo_ml_kmeans.ipynb` |
| `C3_W2_RecSysNN_Assignment.ipynb` | recomendação baseada em conteúdo com rede de duas torres | *Filtragem baseada em conteúdo* (`/modelar/sistemas-de-recomendacao/#m-content-based`) | 7 | `modelo_ml_recomendacao_conteudo_rede_neural.ipynb` |
| `C3_W3_A1_Assignment.ipynb` | Deep Q-Learning no Lunar Lander | *Deep Q-Network (DQN)* (`/modelar/aprendizagem-por-reforco/#m-dqn`) | 7 | `modelo_ml_dqn.ipynb` |

**Nenhum modelo novo foi criado no sistema.** Os 10 notebooks correspondem a 9 cartões já existentes (as duas redes neurais ficam no mesmo cartão, MLP).

**Todos os 10 notebooks tinham problemas**, então nenhum foi generalizado "como estava": primeiro os problemas foram registrados (seção 3) e corrigidos, e só então o notebook foi generalizado.

## 2. Problemas comuns a todos

São exercícios da *Machine Learning Specialization* (DeepLearning.AI e Stanford Online), entregues com as respostas preenchidas. Por isso, todos:

1. **Dependem de arquivos que não estão na pasta:** `utils.py`/`autils.py`/`assigment_utils.py`/`recsysNN_utils.py`, `public_tests.py`, as pastas `data/` e `images/`. Nenhum roda como está.
2. Trazem **instruções do corretor automático** ("não edite nem apague células", como destravar células) e dicas com a resposta, que não fazem sentido num template.
3. Estão **em inglês**, enquanto o sistema é em português do Brasil.
4. Têm o dataset fixo no código (caminhos, nomes de colunas, formas como `(20, 20)`, índices como `X[500]`, unidades como "população em dezenas de milhares").
5. Avaliam, na maioria, **no próprio conjunto de treino**, sem as métricas que os cartões do sistema recomendam.

## 3. Problemas por notebook e como foram corrigidos

### 3.1 `C1_W2_Linear_Regression.ipynb` → Regressão Linear
**Coerência com o cartão:** o modelo é o mesmo (combinação linear ajustada por mínimos quadrados); o cartão usa a forma fechada e o notebook, gradiente descendente, que é outro otimizador para o mesmo custo. Faltavam a avaliação e as métricas do cartão.

| # | Problema | Correção |
|---|---|---|
| 1 | `compute_cost` definida **duas vezes** na mesma célula; a primeira, sem `return`, é sobrescrita | uma única versão, vetorizada |
| 2 | `compute_gradient` com o mesmo problema | idem |
| 3 | Só aceita **uma** feature (`f = w·x + b` escalar) | vetorização para *n* features |
| 4 | Sem divisão treino/teste e sem métricas (só o custo no treino) | treino/teste, MAE, RMSE, R², gráficos de resíduos |
| 5 | Sem padronização (o gradiente descendente converge mal com escalas diferentes) | padronização ajustada só no treino, inclusive das dummies |
| 6 | **Não convergiu:** o resultado "esperado" pelo exercício não é o ótimo dado pela forma fechada | comparação automática com `LinearRegression` e aviso quando o gradiente descendente não chegou ao ótimo |

### 3.2 `C1_W3_Logistic_Regression.ipynb` → Regressão Logística
**Coerência com o cartão:** mesmo modelo (sigmoide + log loss, L2). O cartão exige padronização e métricas de probabilidade e ranking (ROC-AUC, PR-AUC, F1, log loss, Brier), ausentes no notebook.

| # | Problema | Correção |
|---|---|---|
| 1 | `compute_cost` pode calcular `log(0)` quando a sigmoide satura | probabilidades limitadas a [1e-15, 1 − 1e-15] e recorte de `z` |
| 2 | `compute_gradient` perdeu a documentação de argumentos e retorno | documentação restaurada |
| 3 | Avalia só a acurácia **no treino** | teste estratificado + métricas do cartão + tabela para escolher o limiar |
| 4 | `map_feature` (do `utils.py`) fixo em 2 features e grau 6 | `PolynomialFeatures` com grau configurável e qualquer número de features |
| 5 | Sem padronização | padronização antes e depois da expansão polinomial |
| 6 | Duas implementações separadas (com e sem λ) ligadas por `*argv` | um único custo/gradiente com `lambda_` (λ = 0 → sem regularização) |

### 3.3 `C2_W1_Assignment.ipynb` → Rede Neural (MLP), binária
**Coerência com o cartão:** mesma arquitetura (densa, BCE, Adam). O cartão usa ReLU, Keras 3, validação e curvas de treino × validação.

| # | Problema | Correção |
|---|---|---|
| 1 | Treina e "avalia" no **mesmo conjunto** (inclusive `X[0]` e `X[500]`) | treino/validação/teste estratificados, early stopping, métricas no teste |
| 2 | Camadas ocultas com **sigmoide** (o cartão usa ReLU) | ReLU por padrão; sigmoide disponível como opção |
| 3 | `sigmoid` usada sem definição (vem do `from autils import *`) | definida no notebook |
| 4 | Arquitetura e forma da imagem fixas (400-25-15-1, 20×20, `.T`) | `CAMADAS_OCULTAS`, `FORMATO_IMAGEM` e `TRANSPOR_IMAGEM` configuráveis |
| 5 | `tf.keras` antigo; o cartão usa Keras 3 | `import keras`, `model.save(".keras")` |

### 3.4 `C2_W2_Assignment.ipynb` → Rede Neural (MLP), multiclasse
| # | Problema | Correção |
|---|---|---|
| 1 | `my_softmax` **numericamente instável**: com logits ≥ ~710, `exp` estoura e o resultado é `nan` | subtrai `max(z)` antes da exponencial; aceita lotes (m, N) |
| 2 | Erros contados **no treino** ("15 errors out of 5000 images") | erros e métricas no teste (acurácia, F1 macro, log loss, matriz de confusão) |
| 3 | Número de classes fixo (`Dense(10)`), rótulos só numéricos | K vem do alvo; `LabelEncoder` aceita rótulos de texto |
| 4 | `%matplotlib widget` (exige `ipympl`), `deeplearning.mplstyle`, `lab_utils_softmax.py`, `autils.py` | gráficos estáticos e funções próprias |
| 5 | Sem validação nem early stopping | incluídos |

### 3.5 `C2_W3_Assignment.ipynb` → Regressão Polinomial (viés × variância)
**Coerência com o cartão:** o modelo principal é exatamente o do cartão (`PolynomialFeatures` + padronização + `Ridge`), com a escolha de grau e λ que o cartão lista como hiperparâmetros. A parte de redes ilustra os conceitos das seções 6, 8 e 9 do manual.

| # | Problema | Correção |
|---|---|---|
| 1 | `eval_mse` divide por **2m** mas se chama "erro quadrático médio" (o sistema define MSE com 1/m) | MSE de fato, conferido com `mean_squared_error` |
| 2 | Indentação inconsistente em `eval_cat_err` (funciona por acaso) | versão vetorizada |
| 3 | Modelo regularizado criado com `name=None`, mas o esperado é `ComplexRegularized` | nome corrigido |
| 4 | Marcadores `### START CODE HERE ###` no lugar de `### END CODE HERE ###` | removidos (template sem marcadores do corretor) |
| 5 | Erro de **teste** da rede regularizada calculado e nunca exibido | teste usado uma vez, no fim de cada parte, para o modelo escolhido na validação |
| 6 | Teste de `eval_mse` com argumentos trocados (`eval_mse(y_hat, y_tmp)`) | inofensivo (simétrico); a nova verificação usa a ordem certa |
| 7 | Dados, modelos e gráficos vêm de `assigment_utils.py` e só aceitam 1 feature | reescritos para qualquer número de features, com limite de termos polinomiais |

### 3.6 `C2_W4_Decision_Tree_with_Markdown.ipynb` → Decision Tree
**Coerência com o cartão:** mesmo algoritmo (impureza, ganho, divisão recursiva). O cartão cita Gini, regressão, poda, previsão e avaliação; o notebook só imprime a árvore.

| # | Problema | Correção |
|---|---|---|
| 1 | **Erro:** se nenhuma feature tem ganho positivo, `get_best_split` devolve `-1` e `split_dataset` divide pela **última coluna** (`X[i][-1]`) sem aviso | o nó vira folha |
| 2 | Só features binárias 0/1 e alvo binário | limiares para features numéricas, alvo multiclasse, entropia ou Gini |
| 3 | Sem previsão: a árvore é só impressa numa lista global `tree` | estrutura de nós, `predict`, regras SE…ENTÃO, avaliação treino × teste |
| 4 | Um único critério de parada (profundidade) | também mínimo de amostras, nó puro e ganho mínimo |
| 5 | Células de código vazias no fim | removidas |

### 3.7 `C3_W1_Anomaly_Detection.ipynb` → Gaussian Mixture Model (GMM)
**Por que este cartão:** o modelo do notebook é uma densidade gaussiana com features independentes, que é exatamente um GMM com **1 componente** e covariância **diagonal**. O template prova a equivalência (diferença de log-densidade ~1e-11 em relação ao `GaussianMixture`) e estende para K componentes pelo BIC, como no cartão. O cartão *Z-score* não serve: ele é univariado e diz explicitamente que não se aplica a anomalias multivariadas.

| # | Problema | Correção |
|---|---|---|
| 1 | `select_threshold` divide por zero quando `tp + fp = 0` (avisos e `nan`) | F1 = 0 nesses limiares |
| 2 | Risco de **underflow**: com 11 features o ε já é 1,4 × 10⁻¹⁸ | tudo em log-densidade |
| 3 | ε é escolhido e o F1 é reportado **no mesmo conjunto** de validação | conjunto de teste separado (precisão, recall, F1, PR-AUC) |
| 4 | Em empates do F1, fica o menor ε (colado nas anomalias da validação) | ε do meio do intervalo empatado (na validação, recall de teste 0,70 → 1,00 no cenário de 11 features) |
| 5 | `m, n = X.shape` repetido; eixos fixos `[0, 30]`; `multivariate_gaussian` e `visualize_fit` no `utils.py` | reescrito; covariância diagonal ou completa |

### 3.8 `C3_W1_KMeans_Assignment.ipynb` → K-Means
| # | Problema | Correção |
|---|---|---|
| 1 | Grupo vazio gera **`nan`** em `compute_centroids` | centroide reposicionado no ponto mais distante |
| 2 | Sem padronização (o cartão a considera obrigatória) | `StandardScaler` |
| 3 | 10 iterações fixas, uma inicialização, sem escolha de k | convergência, `N_INICIALIZACOES`, k-means++, cotovelo e silhouette |
| 4 | `run_kMeans` cria uma figura vazia quando não desenha (saída "Figure … with 0 Axes") | figura só quando pedida e em 2-D |
| 5 | Arquivo de imagem fixo (`bird_small.png`) e conversão de JPG manual | `CAMINHO_IMAGEM` opcional; `/255` e canal alfa automáticos |
| 6 | Células vazias no fim | removidas |

### 3.9 `C3_W2_RecSysNN_Assignment.ipynb` → Filtragem baseada em conteúdo
**Coerência com o cartão:** mesma família (perfil do usuário × atributos do item). O cartão mostra a versão com TF-IDF; o notebook usa vetores aprendidos por rede neural, que o cartão prevê em "Representação (TF-IDF, embeddings)". Faltavam as métricas de ranking do cartão.

| # | Problema | Correção |
|---|---|---|
| 1 | **Vazamento:** escalonadores ajustados com todas as linhas **antes** da divisão | divisão primeiro; ajuste só no treino |
| 2 | **Vazamento:** médias por gênero e por filme calculadas com todas as avaliações | calculadas só com o treino |
| 3 | Três `train_test_split` separados contando com a mesma semente para alinhar linhas | uma divisão por índices |
| 4 | **Erro:** a tabela de itens semelhantes mostra os gêneros do filme 1 nas duas colunas | gêneros do item 2 |
| 5 | Matriz de distâncias com dois laços Python (n² chamadas) | operação vetorizada |
| 6 | `Input(shape=(n))` com inteiro e `tf.linalg.l2_normalize` no modelo funcional (falham no Keras 3) | `Input(shape=(n,))` e `UnitNormalization` |
| 7 | Só o MSE na escala normalizada | RMSE/MAE em notas, baseline, precision@k, recall@k e NDCG@k |

### 3.10 `C3_W3_A1_Assignment.ipynb` → Deep Q-Network (DQN)
| # | Problema | Correção |
|---|---|---|
| 1 | API do `gym` 0.24, descontinuada: `reset()` sem `info`, `step()` com 4 valores, `render(mode=...)`; `LunarLander-v2` não existe mais | Gymnasium; `LunarLander-v3` |
| 2 | **Erro de alvo:** `done` mistura fim real com corte por tempo, zerando o futuro em cortes | o buffer guarda `terminated`; o episódio acaba em `terminated or truncated` |
| 3 | Treino salvo **interrompido no episódio 236** (média −113, meta 200); gráfico e vídeo nunca gerados | template validado de ponta a ponta |
| 4 | `utils.py` ausente (ação, amostragem, atualização da rede-alvo, ε, gráficos, vídeo) e `pyvirtualdisplay` | funções escritas no notebook; GIF opcional com Pillow |
| 5 | `q_network.save('….h5')`, formato legado no Keras 3 | `.keras` |
| 6 | **Hiperparâmetros do Lunar Lander não servem a outros ambientes:** aplicados ao CartPole, o agente terminou 700 episódios com média ~10 (pior que aleatório) | padrão do cartão (ε por passo, aquecimento do buffer, τ = 0,005, Huber); valores do original documentados na configuração |
| 7 | O DQN regride depois de um bom momento (uma semente: média 315 no episódio 600, 43 no 1500) | checkpoint dos melhores pesos; avaliação gulosa separada |

## 4. Como os templates foram generalizados

Todos seguem a mesma estrutura, em português:

1. Cabeçalho com o **cartão correspondente** no sistema, a origem, o tipo de problema, as dependências e a lista do que mudou.
2. **Uma única célula de configuração** (marcada `>>> ADAPTAR`): caminho do arquivo, separador, cabeçalho, coluna-alvo, features e hiperparâmetros. Nenhuma outra célula depende de nomes de colunas.
3. Com o caminho em `None`, o notebook gera **dados sintéticos** no formato esperado e roda de ponta a ponta.
4. Leitura de CSV/TXT/TSV, Excel, Parquet ou JSON; imputação, one-hot e padronização ajustados **só no treino**.
5. A implementação do zero do original (corrigida e vetorizada), com **verificações automáticas** no lugar do `public_tests.py` (gradiente numérico, saídas esperadas do original, equivalências).
6. Avaliação com as **métricas do cartão** e comparação com a implementação de referência (scikit-learn ou Keras).
7. Previsão para novos dados e próximos passos tirados do cartão ("quando preferir outro").

## 5. Validação

Cada template foi executado de ponta a ponta, em 30 cenários (todos sem erro) mais 3 treinos completos do DQN (Python 3.12, NumPy 2, pandas, scikit-learn 1.9.1, TensorFlow 2.21, Keras 3.15, Gymnasium 1.4) em cenários diferentes, para garantir que não depende do dataset original: o sintético padrão, o próprio dataset original quando disponível e datasets com outro formato (separador `;`, colunas categóricas, faltantes, alvo de texto, arquivo sem cabeçalho, imagens).

| Template | Cenários | Resultado-chave |
|---|---|---|
| Regressão linear | sintético; `ex1data1.txt` original sem cabeçalho; imóveis (`;`, categórica, faltantes) | reproduz o resultado do original e acusa que ele não convergiu; nos outros cenários coincide com `LinearRegression` |
| Regressão logística | sintético; clientes (alvo "sim"/"nao"); fronteira circular com grau 6 e λ = 0,01 | coeficientes iguais ao scikit-learn (dif. ≤ 0,001); no grau 6, 97,5 % de concordância e aviso de convergência incompleta |
| Rede binária | sintético; clientes; dígitos 0/1 em imagem 8×8 | NumPy = Keras (dif. ~1e-7); ROC-AUC 0,97 |
| Rede multiclasse | sintético; sensores (4 classes de texto); dígitos 0–9 | softmax estável = Keras; acurácia 0,93 nos dígitos |
| Polinomial / viés × variância | sintético; imóveis + sensores; sem a parte de redes | grau e λ escolhidos na validação; modelo complexo sobreajusta como no original |
| Árvore de decisão | sintético multiclasse; clientes; sensores com Gini | reproduz os ganhos de informação do original; acurácia ≈ scikit-learn |
| Anomalias gaussianas | 2-D diagonal; 2-D completa; 11 features + log; sem rótulo | log-densidade = `GaussianMixture` (dif. ~1e-11); F1 de teste 1,0 nos três cenários rotulados |
| K-Means | sintético 3-D; clientes; CSV sem cabeçalho + PNG com alfa; JPG | inércia = scikit-learn; índice de Rand ajustado 1,0 |
| Recomendação | sintético; formato MovieLens com outros nomes de coluna | RMSE 0,61 × 0,81 do baseline; NDCG@10 0,054 × 0,020 da popularidade |
| DQN | CartPole rápido; Acrobot com Huber; CartPole completo com 3 sementes | retorno guloso 500 ± 0 (máximo) nas sementes 0, 1 e 2 |

## 6. Integração com o site

- Fonte dos templates para o gerador: `site/gerador/origem/modelos-ml/`.
- `site/gerador/guia_ml.py`: mapa `NOTEBOOKS_MODELO` (id do cartão → arquivos); bloco **Notebook modelo** com botão de download dentro do cartão; selo "notebook modelo" no índice dos modelos; cópia para `site/public/downloads/`.
- `site/gerador/gerar.py` e `site/src/pages/sobre.astro`: lista dos 10 notebooks na página Sobre, com link para o cartão.
- `site/src/styles/ml.css`: estilo do bloco, só com tokens do design system (`npm run verificar` sem violações).
- Verificado no navegador: os 10 links respondem 200 com `.ipynb` válido; o bloco aparece nos 9 cartões certos; sem rolagem horizontal a 375 px; temas claro e escuro.

Para atualizar um template: edite em `site/gerador/origem/modelos-ml/` e rode `npm run gerar` e `npm run build` em `site/`.

## 7. Pontos de atenção

- **Origem dos templates:** os templates foram reescritos e indicam a origem no cabeçalho; os exercícios originais pertencem aos autores do curso e não fazem parte deste repositório.
- **TensorFlow:** os templates de rede neural, recomendação, a parte B do de viés × variância e o DQN exigem TensorFlow com Keras 3. Os demais rodam só com scikit-learn.
- **Lunar Lander:** exige `pip install swig "gymnasium[box2d]"`; o padrão do template é o CartPole.
