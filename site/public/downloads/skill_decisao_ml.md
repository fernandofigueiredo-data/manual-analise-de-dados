---
name: decisao-ml
description: Algoritmo de decisão para escolher, validar e justificar modelos de Machine Learning a partir de um dataset. Use quando alguém pedir "qual modelo usar", entregar um dataset (CSV/Parquet/DataFrame) para modelar, pedir diagnóstico de um problema de ML, definição de métrica, estratégia de validação, checagem de data leakage, comparação entre modelos candidatos ou revisão de uma escolha de modelo já feita. Cobre supervisionado (regressão e classificação), não supervisionado (clustering, redução de dimensionalidade, anomalias, densidade) e a decisão de quando NÃO usar Deep Learning. Cobre também sistemas de recomendação (filtragem colaborativa, baseada em conteúdo, fatoração de matrizes, híbridos), aprendizagem por reforço (bandits, Q-learning, DQN, policy gradient) e implementação em TensorFlow, PyTorch e scikit-learn. Inclui regras de associação (Apriori, FP-Growth), aprendizagem semissupervisionada (Self-Training, Co-Training, Label Spreading), ICA, Z-score robusto, regressão multivariada e reforço baseado em modelo (programação dinâmica, Dyna-Q), e exige que toda recomendação cubra os sete critérios — pressupostos, pontos fortes, limitações, requisitos de dados, interpretabilidade, custo e métricas.
---

# Skill — Decisão de Modelos de Machine Learning

Documento **operacional**, não didático. É o algoritmo que o agente executa para sair de "aqui está um dataset" até "este é o modelo, esta é a métrica, esta é a validação, estes são os riscos". O material de estudo correspondente é `manual_machine_learning.html`; as definições conceituais são idênticas nos dois — este arquivo não as reexplica, apenas as aplica.

---

## 0. Contrato de execução

**Entrada mínima aceitável:** um dataset (ou o schema + amostra) e uma frase sobre o objetivo de negócio.

**Onde esta skill se encaixa:** ver `manual_machine_learning.html#comousar` — estudar é o HTML, consultar são as tabelas, decidir é este arquivo.

**Saída obrigatória:** o *Diagnóstico do Dataset* da §6, com os 16 itens preenchidos. Nenhum item pode ser omitido; itens sem informação suficiente recebem `INDETERMINADO — falta: <o que falta>`.

**Regras de conduta do agente:**

1. **Nunca recomendar um modelo antes de executar os passos 1 a 6 da §2.** Escolha de algoritmo é a penúltima decisão, não a primeira.
2. **Nunca afirmar superioridade universal.** Toda recomendação é condicional aos dados descritos e ao objetivo declarado. Não existe melhor modelo universal.
3. **Sempre declarar a incerteza.** Se o diagnóstico depende de algo não observado (disponibilidade de uma feature em produção, custo de erro, volume futuro), diga explicitamente e proponha como verificar.
4. **Sempre propor o baseline antes do candidato complexo**, e nunca pular níveis da hierarquia da §4 sem a regra de promoção da §4.2.
5. **Qualquer modelo pode generalizar mal.** A recomendação é um plano de experimentos, não uma garantia de desempenho.
6. **Cobrir os sete critérios** para cada candidato recomendado: pressupostos (e se os dados os satisfazem), pontos fortes, limitações, requisitos de dados, interpretabilidade, custo computacional e métricas — a matriz 12.5 do manual traz os sete para os 43 modelos.
7. **Não inventar números.** Métricas, tamanhos e cardinalidades vêm de inspeção real do dado; se não foi possível inspecionar, marque como `NÃO INSPECIONADO`.

---

## 1. Restrições taxonômicas invioláveis

O agente nunca pode trocar estas categorias entre si. Confundi-las invalida o diagnóstico inteiro.

| Categoria | Papel | Exemplos |
|---|---|---|
| **Modelo / algoritmo** | Aprende um mapeamento de X para y (ou a estrutura de X) | Linear/Logistic Regression, Decision Tree, Random Forest, XGBoost, LightGBM, CatBoost, SVM, KNN, Naive Bayes, K-Means, GMM, DBSCAN, PCA, IsolationForest |
| **Função de perda** | É otimizada durante o treino; não "prevê" | MSE, MAE, Huber, Log Loss (Binary Cross Entropy), Categorical Cross Entropy, Hinge |
| **Otimizador** | Minimiza a perda ajustando parâmetros | Gradient Descent, SGD, Mini-Batch, Momentum, RMSProp, Adam |
| **Regularização** | Restringe complexidade | L1 (Lasso), L2 (Ridge), Elastic Net, dropout, early stopping, poda |
| **Framework** | Software para construir e treinar | Scikit-Learn, Keras, TensorFlow, PyTorch, XGBoost, LightGBM, CatBoost |
| **Métrica** | Avalia modelo já treinado | Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, MAE, RMSE, R², Silhouette |

**Proibições explícitas:** tratar Cross Entropy, Gradient Descent, Adam, TensorFlow ou PyTorch como "modelo"; apresentar uma métrica como função de perda otimizada (ou vice-versa) sem dizer qual é qual; chamar regularização de algoritmo.

---

## 2. Algoritmo de decisão — 9 passos

Execute em ordem. Cada passo produz um artefato que alimenta o seguinte.

### Passo 1 — RECEBER e INSPECIONAR o dataset
Colete e registre: número de linhas e colunas, tipo de cada coluna, percentual de ausentes por coluna, cardinalidade das categóricas, **unidade de observação** (uma linha é o quê?), existência de coluna temporal e de identificador de entidade (cliente, loja, paciente, máquina).

```python
import pandas as pd
print(df.shape)
print(df.dtypes.value_counts())
print((df.isna().mean() * 100).round(2).sort_values(ascending=False).head(20))
print(df.select_dtypes("object").nunique().sort_values(ascending=False).head(20))
print(df.duplicated().sum())
```

**Saída do passo:** ficha técnica do dataset (itens 2 e 3 do template).

### Passo 2 — IDENTIFICAR o TARGET

**Antes de procurar uma coluna-alvo, verifique se o problema pertence a uma classe especial** — elas não se encaixam em regressão nem classificação e têm dado, métrica e validação próprios:
- **SE** o objetivo é **ordenar itens para cada usuário** a partir de interações (compras, cliques, notas) → **sistema de recomendação** → siga a §3.10.
- **SE** a decisão é **repetida**, a recompensa é **imediata** e é preciso **explorar** alternativas durante a operação → **bandits** → §3.11.
- **SE** há **decisões sequenciais** em que **a ação altera o estado futuro** e a recompensa pode ser atrasada → **aprendizagem por reforço** → §3.11.

Caso contrário:
- **SE** existe uma coluna que representa o que se quer prever **E** ela está rotulada para as linhas históricas → **supervisionado**.
- **SENÃO** → **não supervisionado**: decidir entre clustering (agrupar), redução de dimensionalidade (comprimir/visualizar; **ICA** se o objetivo for separar sinais misturados), **regras de associação** (descobrir itens que ocorrem juntos — §3.13), detecção de anomalias (isolar o raro) ou estimação de densidade (descrever a distribuição), conforme o objetivo declarado.
- **SE** o alvo existe mas só para uma parte pequena das linhas e há muitos dados sem rótulo da mesma distribuição → **semissupervisionado** (§3.12). O baseline obrigatório é o modelo supervisionado treinado só com os rotulados; o semissupervisionado só é adotado se o superar num holdout **rotulado**.

**Ponto de parada obrigatório:** se o objetivo de negócio não permitir definir o alvo com **evento, janela de observação e janela de previsão** explícitos, pare e peça essa definição. Sem isso, nenhuma métrica é interpretável.

### Passo 3 — CLASSIFICAR o tipo de problema
- Supervisionado **E** target numérico contínuo → **regressão**.
- Supervisionado **E** target categórico com 2 classes → **classificação binária**.
- Supervisionado **E** target categórico com K ≥ 3 classes mutuamente exclusivas → **multiclasse** (perda multinomial/softmax).
- Supervisionado **E** várias classes simultâneas por linha → **multirrótulo** (uma sigmoide por rótulo; métricas por rótulo e agregadas).
- Supervisionado **E** vários alvos numéricos simultâneos → **regressão multivariada** (multi-output): `LinearRegression`, `Ridge`, árvores e KNN aceitam Y matricial; `MultiOutputRegressor` (um modelo por alvo) ou `RegressorChain` (alvos dependentes) para os demais. Não confundir com regressão *múltipla* (várias features, um alvo).
- Target inteiro de contagem → regressão de contagem (Poisson/Tweedie), **não** regressão linear comum.
- Target contínuo mas usado com corte de decisão → modele como regressão **ou** classificação, nunca as duas ao mesmo tempo; a escolha depende de onde está o custo do erro.

### Passo 4 — CARACTERIZAR os dados
Preencher, com os limiares da §3.2:

| Dimensão | Valores possíveis |
|---|---|
| Tamanho | pequeno / médio / grande / muito grande |
| Tipos | numérico / categórico / misto / texto / imagem / áudio / temporal / grafo |
| Ausentes | nenhum / moderado / severo / informativo |
| Outliers | irrelevantes / relevantes / dominantes |
| Desbalanceamento | leve / moderado / extremo (só classificação) |
| Multicolinearidade | baixa / alta |
| Dimensionalidade | baixa / alta (p/n) |
| Não linearidade | aparente / não aparente |
| Interpretabilidade exigida | não / desejável / obrigatória (regulatória) |
| Latência de inferência | livre / restrita / tempo real |

### Passo 5 — VERIFICAR leakage e DEFINIR a validação
Rodar o checklist da §3.6 **antes** de qualquer treino. Depois, escolher o esquema de validação pela árvore da §3.7. Um modelo validado com o esquema errado tem métrica inválida — não é um "resultado otimista", é um número sem significado.

### Passo 6 — ESCOLHER a métrica principal
Aplicar as regras da §3.8. A métrica principal é **uma só** e decorre do custo do erro; as secundárias existem para descrever o que a principal esconde.

### Passo 7 — BASELINE
Obrigatório e sempre reportado: `DummyClassifier(strategy="prior")` ou `DummyRegressor(strategy="median")`, **mais** um modelo de Nível 1 (linear/logístico regularizado). Nenhum modelo de nível superior pode ser recomendado sem superar esse piso pela regra de promoção da §4.2.

### Passo 8 — LISTAR CANDIDATOS
Selecionar 2 a 4 candidatos usando as regras da §3 e a hierarquia da §4. Sempre incluir pelo menos um modelo de nível inferior ao melhor candidato, para provar que a complexidade extra se paga.

### Passo 9 — VALIDAR, COMPARAR, TUNAR, SELECIONAR, INTERPRETAR, VALIDAR COM O NEGÓCIO
- Mesma partição e mesma métrica para todos os candidatos.
- Reportar **média e desvio-padrão entre folds**, nunca só a média.
- Tuning por `RandomizedSearchCV` (ou otimização bayesiana) sobre o **pipeline completo**.
- Seleção pelo **Model Fit Score** da §5, não pela métrica isolada.
- Interpretação: coeficientes, `permutation_importance`, SHAP, dependência parcial.
- Validação de negócio: o erro que o modelo comete é aceitável para quem vai usar a decisão?
- O conjunto de teste é tocado **uma única vez**, no fim.

---

## 3. Regras IF / THEN

### 3.1 Do tipo de problema para a família de modelos

| SE | ENTÃO candidatos | Baseline obrigatório |
|---|---|---|
| Regressão, relação aparentemente linear | Linear Regression; Ridge se houver multicolinearidade | Dummy (mediana) + Linear |
| Regressão, não linearidade aparente | HistGradientBoosting, XGBoost, LightGBM, Random Forest | Dummy + Ridge |
| Regressão de contagem | `PoissonRegressor`, `TweedieRegressor`, boosting com `objective="count:poisson"` | Dummy + Poisson |
| Classificação binária tabular | LightGBM/XGBoost/CatBoost, Random Forest | Dummy (prior) + Logistic |
| Classificação multiclasse | LogisticRegression (multinomial), boosting, Random Forest | Dummy + Logistic |
| Classificação multirrótulo | `OneVsRestClassifier` sobre logística ou boosting | Dummy por rótulo |
| Texto como entrada principal | TF-IDF + LinearSVC/LogisticRegression/ComplementNB | TF-IDF + Naive Bayes |
| Imagem, áudio, vídeo | CNN com transfer learning (Nível 4) | Modelo pré-treinado congelado + cabeça linear |
| Sem target, objetivo = agrupar | K-Means; GMM se fronteiras suaves; DBSCAN/HDBSCAN se houver ruído e forma irregular | — |
| Sem target, objetivo = comprimir | PCA (linear); TruncatedSVD se esparso | — |
| Sem target, objetivo = separar sinais misturados | ICA (FastICA) — exige fontes não gaussianas | PCA (para mostrar que não separa) |
| Sem target, objetivo = itens que ocorrem juntos | FP-Growth (Apriori em bases pequenas) + regras filtradas por lift | Contagem de pares mais frequentes |
| Sem target, objetivo = achar o raro | IsolationForest; LOF se a anomalia é local; OneClassSVM se o treino é reconhecidamente limpo | Z-score robusto (MAD) por variável |
| Alerta numa única métrica | **Z-score robusto (MAD)**, limiar 3,5; z clássico só com dados limpos e simétricos | — |
| Sem target, objetivo = descrever distribuição | KDE (baixa dimensão), GMM (dimensão moderada) | — |
| Recomendação com histórico de interações | Colaborativa item-based, fatoração de matrizes (ALS), híbrido | **Popularidade** no período recente |
| Recomendação com cold start (itens ou usuários novos) | Filtragem baseada em conteúdo, híbrido com chaveamento, bandits para itens novos | Popularidade |
| Decisão repetida com recompensa imediata | Thompson Sampling, UCB; LinUCB se houver contexto | Teste A/B ou regra fixa atual |
| Decisões sequenciais, estados discretos e poucos | Q-learning tabular; programação dinâmica se o modelo for conhecido | Política/regra de negócio atual |
| Decisões sequenciais, estados contínuos | DQN (ações discretas), PPO/SAC (ações contínuas) | Política/regra de negócio atual |
| Decisões sequenciais com modelo do ambiente conhecido | Programação dinâmica (value/policy iteration) | Política/regra de negócio atual |
| Decisões sequenciais, interação real cara, ambiente modelável | Dyna-Q / RL baseado em modelo aprendido | Q-learning sem modelo |
| Poucos rótulos, muitos não rotulados | Self-Training; Co-Training (duas visões); Label Spreading (vizinhança informativa) | **Supervisionado só com os rotulados** |
| Vários alvos numéricos | Regressão multivariada (Y matricial, `MultiOutputRegressor`, `RegressorChain`) | Um modelo simples por alvo |

### 3.2 Do tamanho e da dimensionalidade

Limiares operacionais (n = linhas, p = colunas após encoding):

| Faixa | Definição | Consequência |
|---|---|---|
| Pequeno | n < 1.000 | Nível 1 com regularização forte; CV repetida (`RepeatedStratifiedKFold`); **Deep Learning proibido sem justificativa escrita** |
| Médio | 1.000 ≤ n < 100.000 | Níveis 2 e 3; boosting é o candidato natural |
| Grande | 100.000 ≤ n < 1.000.000 | LightGBM/HistGB; amostrar para prototipar |
| Muito grande | n ≥ 1.000.000 | LightGBM, lineares com `SGDClassifier`; Deep Learning passa a ser considerável se o sinal for complexo |
| Alta dimensionalidade | p/n > 0,1 **ou** p > 1.000 | Linear regularizado (L1/Elastic Net) ou PCA + modelo; KNN e distância degradam |
| p ≫ n | p > n | Regularização forte obrigatória; Lasso seleciona no máximo n features |

**Regras derivadas:**
- **SE** n < 1.000 **E** p > n/10 → **ENTÃO** Ridge/Lasso/Elastic Net ou Naive Bayes; evitar ensembles grandes e qualquer rede neural.
- **SE** n ≥ 1.000.000 **E** o tipo de dado é tabular → **ENTÃO** LightGBM primeiro; Deep Learning só se o boosting saturar com margem medida.
- **SE** p > 1.000 e os dados são esparsos (texto) → **ENTÃO** modelos lineares; **não** usar árvores como primeira escolha.

### 3.3 Do tipo de dado

| SE o dado tem… | ENTÃO |
|---|---|
| Categóricas de alta cardinalidade (níveis > 50) | CatBoost, ou categóricas nativas em LightGBM/XGBoost/HistGB, ou `TargetEncoder` **dentro do pipeline**. Nunca One-Hot puro acima de ~50 níveis |
| Categóricas de baixa cardinalidade | One-Hot é adequado; `handle_unknown="infrequent_if_exist"` |
| Mistura de numéricas e categóricas | HistGradientBoosting ou CatBoost (menos pré-processamento) |
| Coluna temporal relevante | Features de lag, janelas móveis, componentes de data, codificação cíclica + `TimeSeriesSplit` |
| Identificador de entidade repetido | `GroupKFold`/`StratifiedGroupKFold` obrigatório; agregações por entidade como features |
| Texto livre | TF-IDF (n-gramas 1–2) + linear/NB; Transformers só com volume e infraestrutura |
| Imagem | CNN + transfer learning; augmentation |
| Geoespacial | DBSCAN com métrica haversine; features de distância |

### 3.4 Da qualidade dos dados

| SE | ENTÃO |
|---|---|
| Ausentes moderados (< 20% por coluna) | `SimpleImputer` dentro do pipeline, com `add_indicator=True` se a ausência puder ser informativa |
| Ausentes severos (> 40% na coluna) | Considerar descartar a coluna; se mantida, usar modelo com NaN nativo e documentar |
| Ausência informativa (padrão não aleatório) | **Não imputar cegamente**: criar o indicador de ausência como feature |
| Modelo escolhido é HistGB/XGBoost/LightGBM/CatBoost | Imputação é **opcional** — esses modelos tratam NaN nativamente e imputar pode piorar |
| Outliers relevantes | `RobustScaler`, perda Huber, winsorização ou modelos de árvore; investigar origem antes de remover |
| Duplicatas | Deduplicar antes do split; duplicata cruzando treino/teste é leakage |
| Desbalanceamento leve (positivo > 10%) | Métrica F1/ROC-AUC; sem intervenção especial |
| Desbalanceamento moderado (1% ≤ positivo ≤ 10%) | `class_weight="balanced"` ou `scale_pos_weight`; métrica PR-AUC; ajustar threshold |
| Desbalanceamento extremo (positivo < 1%) | PR-AUC + precision@k; `scale_pos_weight`; considerar detecção de anomalias; **accuracy é proibida como métrica principal** |
| Reamostragem (SMOTE/undersampling) | Só **dentro** do fold de treino (`imblearn.pipeline.Pipeline`); nunca antes do split; sempre comparar contra `class_weight` antes de adotar |
| Multicolinearidade alta | Ridge/Elastic Net; ou remover redundância; **não** interpretar coeficientes de um OLS colinear |

### 3.5 Das restrições não funcionais

| SE | ENTÃO |
|---|---|
| Explicação exigida por regulação (crédito, saúde, RH) | Nível 1 ou árvore rasa como modelo final; boosting só com SHAP, documentação e aprovação; registrar limitações |
| Explicação desejável, não obrigatória | Boosting + `permutation_importance` + SHAP + dependência parcial |
| Latência de tempo real (< 10 ms) | Linear, árvore rasa ou boosting com poucas árvores; evitar KNN, SVM-RBF e ensembles grandes |
| Inferência em lote, sem restrição | Qualquer nível |
| Equipe sem MLOps / sem GPU | Scikit-Learn puro (HistGB); evitar Deep Learning |
| Probabilidade usada para preço, limite ou corte financeiro | **Calibrar** (`CalibratedClassifierCV`) e reportar Brier + curva de confiabilidade |
| Necessidade de retreino frequente | Preferir modelos baratos e estáveis; medir custo de treino no Model Fit Score |
| Dados sensíveis / risco de viés | Avaliar métricas por subgrupo; documentar disparidades antes do deploy |

### 3.6 Checklist de leakage (executar antes de treinar)

Responda "sim" a todas antes de prosseguir; qualquer "não" bloqueia o experimento.

1. Toda feature existirá, com o mesmo valor, **no momento da previsão** em produção?
2. Nenhuma feature é consequência do alvo (estorno, cancelamento, diagnóstico posterior)?
3. Todo pré-processamento (imputação, escala, encoding, seleção, reamostragem, PCA) está **dentro** do `Pipeline`, ajustado só no treino?
4. O split respeita o tempo, quando há tempo?
5. O split respeita os grupos, quando a mesma entidade aparece várias vezes?
6. Não há duplicatas cruzando treino e teste?
7. Agregações e janelas usam **apenas o passado** em relação a cada linha?
8. O conjunto de teste nunca foi usado para escolher nada?

**Sintoma de alerta:** desempenho muito acima do esperado pelo domínio (por exemplo ROC-AUC > 0,98 em churn) é presunção de leakage até prova em contrário — investigue antes de comemorar.

### 3.7 Da estrutura para o esquema de validação

```
Há ordem temporal relevante?
├── SIM  → TimeSeriesSplit (+ gap se houver latência de coleta)
└── NÃO  → A mesma entidade aparece em várias linhas?
           ├── SIM  → GroupKFold (classificação: StratifiedGroupKFold)
           └── NÃO  → É classificação?
                      ├── SIM  → StratifiedKFold(5, shuffle=True, random_state=42)
                      │           └── n < 1.000 → RepeatedStratifiedKFold(5, n_repeats=5)
                      └── NÃO  → KFold(5, shuffle=True, random_state=42)
```

O número reportado ao negócio deve vir de **nested CV** quando houve tuning intensivo; caso contrário, declare que a métrica pode estar otimista.

### 3.8 Da natureza do erro para a métrica

| SE | ENTÃO métrica principal | Secundárias |
|---|---|---|
| Classificação, positivo raro (< 10%) e caro | **PR-AUC** (`average_precision`) | precision@k, recall no threshold, ROC-AUC, matriz de confusão |
| Classificação, falso negativo muito mais caro | **Recall** com precision mínima contratada | PR-AUC, F1 |
| Classificação, falso positivo muito mais caro | **Precision** com recall mínimo contratado | PR-AUC, F1 |
| Classificação equilibrada, custos simétricos | **F1** ou accuracy | ROC-AUC, Log Loss |
| Probabilidade entra na decisão financeira | **Log Loss** ou **Brier** | curva de calibração, PR-AUC |
| Multiclasse com classes desiguais | **F1 macro** | F1 por classe, matriz de confusão |
| Regressão, erros grandes desproporcionalmente caros | **RMSE** | MAE, R², resíduos |
| Regressão, custo linear no erro | **MAE** | RMSE, MAPE |
| Regressão com escalas heterogêneas entre séries | **MAPE** ou **WAPE** | MAE por série |
| Clustering | **Silhouette** | Davies-Bouldin (menor melhor), Calinski-Harabasz (maior melhor), validação de negócio |
| Anomalias com rótulo parcial | **PR-AUC** | precision@k, taxa de alerta |
| Anomalias sem rótulo | Taxa de alerta + revisão amostrada | estabilidade do score no tempo |
| Recomendação (ranking) | **NDCG@k** (ou recall@k se só importa acertar algo no topo) | MAP@k, precision@k, hit rate, cobertura de catálogo, diversidade, novidade |
| Recomendação com nota explícita | NDCG@k — RMSE/MAE só como secundárias | RMSE, MAE |
| Bandits | **Regret acumulado** | recompensa média, % de jogadas no braço ótimo |
| Reforço | **Retorno médio em avaliação sem exploração, com média e desvio entre ≥ 5 sementes** | eficiência em amostras, taxa de sucesso |
| Política nova avaliada em dados logados | **IPS / SNIPS** (avaliação off-policy) | variância do estimador, tamanho efetivo da amostra |
| Regras de associação | **Lift** (acima de 1) com suporte mínimo | confiança, leverage, conviction; **estabilidade das regras no período seguinte** |
| Semissupervisionado | A métrica do problema (F1, PR-AUC…) num **holdout rotulado**, contra o baseline só-rotulados | ganho médio e desvio entre sementes |
| Separação de fontes (ICA) | Utilidade das componentes na tarefa seguinte | estabilidade entre sementes; recuperação de fontes conhecidas, se houver |
| Reforço baseado em modelo | Retorno em função dos **passos reais** | valor da política; erro do modelo aprendido |

**Proibido:** usar accuracy como métrica principal com desbalanceamento moderado ou extremo; usar R² como único número em regressão; comparar modelos com métricas diferentes.

### 3.9 Pré-processamento obrigatório por família

| Família | Escala | Encoding | NaN | Observação |
|---|---|---|---|---|
| Linear / Logistic / Ridge / Lasso / Elastic Net | **Obrigatória** | One-Hot ou Target | Imputar | A penalização depende da escala |
| SVM | **Obrigatória** | One-Hot | Imputar | Kernel é baseado em distância |
| KNN, K-Means, PCA, KDE, LOF | **Obrigatória** | Cuidadoso | Imputar | Tudo depende de distância |
| Naive Bayes | Não | Vetorização (TF-IDF/contagem) | Imputar | Suavização `alpha` |
| Decision Tree, Random Forest, Extra Trees | **Não exige** | Necessário no scikit-learn | Imputar (não aceita NaN) | Invariante a transformação monotônica |
| HistGB, XGBoost, LightGBM, CatBoost | **Não exige** | Nativo | **Nativo** | Menor pré-processamento; não imputar por hábito |
| IsolationForest | Não exige | Necessário | Imputar | — |
| Redes neurais | **Obrigatória** | Embedding ou One-Hot | Imputar | Também normalizar o alvo em regressão |

---

### 3.10 Regras para sistemas de recomendação

| SE | ENTÃO |
|---|---|
| Qualquer projeto de recomendação | **Baseline de popularidade** calculado só com interações anteriores ao corte; nenhum modelo sem superá-lo |
| Validação | **Split temporal global** (treino até a data de corte, teste depois). Leave-last-out por usuário só em recomendação sequencial. **Split aleatório de interações é proibido** — usa o futuro |
| Feedback implícito | Tratar ausência de interação como “não observado”, não como negativo; ALS implícito com pesos de confiança |
| Feedback explícito | Centralizar pela média do usuário; mesmo assim avaliar o ranking (NDCG@k), não só o RMSE |
| Itens já consumidos pelo usuário | Excluir das recomendações **por padrão**; em domínios de recompra (supermercado, consumíveis, música) mantê-los e avaliar recompra como tarefa própria |
| Muitos itens novos | Filtragem por conteúdo ou híbrido; cota de exploração com bandits |
| Usuários novos | Chaveamento para popularidade, onboarding ou features de contexto |
| Catálogo grande | Arquitetura em estágios: geração de candidatos (vizinhança, embeddings com ANN) → ranqueamento (boosting com objetivo de ranking) → re-ranqueamento de negócio |
| Avaliação com negativos amostrados | Declarar o protocolo; preferir ranquear o catálogo completo — amostragem infla métricas e pode inverter a ordem entre modelos |
| Métricas de concentração ruins (baixa cobertura) | Re-ranquear por diversidade e penalizar popularidade |
| Decisão final | Métrica offline escolhe candidatos; **teste A/B** decide |

### 3.11 Regras para bandits e aprendizagem por reforço

| SE | ENTÃO |
|---|---|
| A ação não altera o estado futuro e há rótulo histórico | **Não use RL**: modelo supervisionado |
| Decisão repetida, recompensa imediata | Bandits (Thompson como padrão); contextuais se houver features |
| Ações registradas em log | Registrar a **probabilidade** de cada ação exibida — sem ela, avaliação off-policy é impossível |
| Estados e ações discretos e poucos, simulador disponível | Q-learning tabular |
| Estados contínuos, ações discretas | DQN com replay buffer e rede-alvo |
| Ações contínuas | PPO ou SAC; preferir implementações testadas (Stable-Baselines3) a código próprio |
| Sem simulador e exploração real arriscada | RL offline apenas com avaliação off-policy rigorosa; frequentemente regras + supervisionado é mais seguro |
| Qualquer resultado de RL | **≥ 5 sementes**, média e desvio; avaliação sem exploração em episódios separados |
| Gymnasium | `step()` devolve 5 valores; **só zerar o bootstrap quando `terminated`**, nunca em `truncated` |
| Reprodutibilidade em Gymnasium | `reset(seed=…)` **não** semeia `action_space.sample()`: chamar `env.action_space.seed(…)`, além de `torch.manual_seed`, `random.seed` e `np.random.seed` |
| Modelo do ambiente conhecido (P e R) | **Programação dinâmica**: policy iteration costuma convergir em poucas iterações; nada de exploração |
| Interação real cara e ambiente modelável | Dyna-Q ou RL baseado em modelo; validar a política no ambiente **real**, porque o agente pode explorar erros do próprio modelo |
| Desenho da recompensa | Revisar com o negócio; testar se o agente consegue “ganhar” sem atingir a intenção (reward hacking) |

### 3.12 Regras para aprendizagem semissupervisionada

| SE | ENTÃO |
|---|---|
| Qualquer projeto | Separar um **holdout rotulado antes de tudo**; nunca medir desempenho sobre pseudo-rótulos |
| Comparação | Baseline obrigatório: supervisionado só com os rotulados, no mesmo holdout, em ≥ 5 sementes; adotar o semissupervisionado só se ganhar acima do ruído (regra §4.2) |
| Classes bem separadas e classificador com probabilidades razoáveis | **Self-Training** (`SelfTrainingClassifier`, limiar alto, ex.: 0,9) |
| Features divisíveis em duas visões suficientes e ~independentes | **Co-Training** (implementação própria — não há no scikit-learn) |
| Estrutura de vizinhança clara, até dezenas de milhares de pontos | **Label Spreading**; testar a construção do grafo (RBF × k vizinhos) — a escolha muda o resultado |
| Não rotulados de outra distribuição | **Não usar** semissupervisionado: introduz viés |
| É possível pedir rótulos | Comparar com *active learning* antes de pseudo-rotular |

### 3.13 Regras para regras de associação

| SE | ENTÃO |
|---|---|
| Base transacional grande ou suporte mínimo baixo | FP-Growth (mesmo resultado do Apriori, muito mais rápido) |
| Itens onipresentes (sacola, frete) | Remover antes de minerar |
| Muitas regras | Filtrar por **lift > 1** e relevância de negócio, não só por confiança |
| Regra vai virar ação (combo, promoção, layout) | Validar no período seguinte e, se possível, por teste A/B — **lift não é causalidade** |
| A ordem dos eventos importa | Mineração de sequências, não regras de associação |
| O objetivo é personalizar por usuário | Sistema de recomendação (§3.10), não regras globais |

## 4. Hierarquia de complexidade

### 4.1 Os quatro níveis

| Nível | Modelos | Papel | Custo de manutenção |
|---|---|---|---|
| **1 — Baseline** | `DummyClassifier`/`DummyRegressor`, Linear/Logistic Regression, Ridge, Lasso, Elastic Net, Naive Bayes | Piso de desempenho e leitura do sinal linear | Muito baixo |
| **2 — Árvores e bagging** | Decision Tree, Random Forest, Extra Trees | Não linearidade e interações com pouco tuning | Baixo |
| **3 — Boosting e especializados** | HistGradientBoosting, XGBoost, LightGBM, CatBoost, SVM | Melhor desempenho em tabular; exige early stopping e tuning | Médio |
| **4 — Deep Learning** | MLP, CNN, RNN/LSTM, Transformer, autoencoder | **Somente com justificativa**: imagem, texto, áudio, vídeo, sequência, grafo ou volume muito grande com sinal complexo | Alto |

### 4.2 Regra de promoção de nível

Suba de nível **apenas** quando o ganho for maior que o ruído:

```
promover = (score_novo - score_atual) > max(0.01 * |score_atual|, desvio_padrao_entre_folds_do_atual)
```

- O ganho é medido na **métrica principal**, na **mesma partição**, com o **mesmo pipeline de pré-processamento**.
- Se `promover` for falso, **fique no nível inferior** e diga isso explicitamente no diagnóstico: modelo mais simples com desempenho equivalente é o vencedor.
- Nível 4 exige, além da regra acima, uma das condições da §4.3.

### 4.3 Condições que autorizam Deep Learning

Autorize o Nível 4 apenas se **pelo menos uma** for verdadeira e estiver escrita no diagnóstico:

1. O dado é não estruturado (imagem, áudio, vídeo, texto livre com semântica relevante, grafo).
2. n ≥ 1.000.000 **e** o boosting bem tunado saturou, com ganho medido para a rede.
3. Existe modelo pré-treinado adequado e transfer learning é o caminho mais curto.
4. O problema exige aprendizado de representação reutilizável (embeddings usados por outros sistemas).
5. É sequência com dependência longa que features de lag não capturam.

**SE nenhuma for verdadeira E os dados forem tabulares de porte pequeno ou médio → ENTÃO recomendar Nível 3 e registrar:** "Deep Learning não é recomendado aqui; em dados tabulares de porte médio, modelos baseados em árvores permanecem competitivos ou superiores (Grinsztajn, Oyallon & Varoquaux, 2022, benchmark com 45 datasets)."

### 4.4 Escadas específicas

| Classe | Nível 1 | Nível 2 | Nível 3 | Nível 4 |
|---|---|---|---|---|
| Recomendação | Popularidade recente | Colaborativa por vizinhança / conteúdo | Fatoração de matrizes (ALS), híbrido | Two-tower / modelos neurais sequenciais |
| Decisão com exploração | Regra fixa ou teste A/B | Bandits (Thompson, UCB) | Bandits contextuais (LinUCB) | RL completo (só se a ação alterar o futuro) |
| Controle sequencial | Regra de negócio / heurística | Programação dinâmica (modelo conhecido) | Q-learning tabular ou Dyna-Q (modelo aprendido) | DQN, PPO, SAC |
| Poucos rótulos | Supervisionado só com os rotulados | Self-Training | Co-Training / Label Spreading | Active learning, modelos pré-treinados |
| Co-ocorrência de itens | Contagem de pares | Apriori | FP-Growth | Recomendador personalizado (§3.10) |

A regra de promoção da §4.2 vale igualmente: suba de nível só com ganho acima do ruído — em RL, o ruído é o desvio entre sementes.

---

## 5. Model Fit Score

Ranqueia candidatos considerando o que a métrica isolada esconde. Todos os critérios são normalizados em [0, 1], onde 1 é melhor.

| # | Critério | Peso | Como normalizar |
|---|---|---|---|
| 1 | Desempenho na métrica principal | **0,30** | Min-max entre os candidatos avaliados |
| 2 | Generalização / estabilidade entre folds | **0,20** | `1 − (desvio_padrão / desvio_padrão_máximo observado)` |
| 3 | Interpretabilidade | **0,15** | Tabela §5.1 |
| 4 | Custo computacional / latência | **0,10** | Min-max invertido do tempo de treino + inferência |
| 5 | Adequação ao tipo de dado **e aos pressupostos do modelo** | **0,10** | Checklist §3.9 e §3.3 mais os pressupostos da matriz 12.5 do manual: fração atendida sem gambiarra |
| 6 | Complexidade / manutenção | **0,10** | Tabela §5.1 (inverso do custo de manutenção) |
| 7 | Alinhamento ao negócio | **0,05** | Avaliação do stakeholder (0, 0,5 ou 1) |

```
MFS = 0.30·D + 0.20·G + 0.15·I + 0.10·C + 0.10·A + 0.10·M + 0.05·N
```

**Os pesos são contextuais e devem ser reajustados — e o reajuste declarado:**
- Crédito, saúde, RH ou qualquer contexto regulado → interpretabilidade de 0,15 para **0,25–0,30** (retirar de desempenho).
- Sistema de tempo real → custo/latência de 0,10 para **0,20**.
- Domínio com drift forte → estabilidade de 0,20 para **0,30**.
- Prova de conceito exploratória → desempenho de 0,30 para **0,45**, manutenção para 0,05.

### 5.1 Escalas fixas de interpretabilidade e manutenção

| Modelo | Interpretabilidade (I) | Manutenção (M) |
|---|---|---|
| Dummy | 1,00 | 1,00 |
| Linear / Logistic / Ridge / Lasso / Elastic Net | 1,00 | 0,95 |
| Naive Bayes | 0,85 | 0,95 |
| Decision Tree (profundidade ≤ 4) | 0,95 | 0,90 |
| Decision Tree profunda | 0,50 | 0,85 |
| Random Forest / Extra Trees | 0,50 | 0,75 |
| HistGB / XGBoost / LightGBM / CatBoost | 0,40 (0,60 com SHAP documentado) | 0,60 |
| SVM linear | 0,70 | 0,70 |
| SVM-RBF | 0,20 | 0,55 |
| KNN | 0,45 | 0,70 |
| K-Means | 0,80 | 0,85 |
| PCA | 0,40 | 0,85 |
| GMM / DBSCAN | 0,60 | 0,70 |
| IsolationForest | 0,45 | 0,70 |
| LOF | 0,45 | 0,65 |
| OneClassSVM | 0,20 | 0,55 |
| MLP | 0,15 | 0,35 |
| CNN / RNN / Transformer | 0,10 | 0,25 |
| Popularidade (baseline de recomendação) | 1,00 | 1,00 |
| Colaborativa por vizinhança | 0,85 | 0,75 |
| Filtragem baseada em conteúdo | 0,85 | 0,80 |
| Fatoração de matrizes | 0,30 | 0,65 |
| Recomendação híbrida | 0,55 | 0,50 |
| Bandits | 0,90 | 0,85 |
| Q-learning tabular | 0,75 | 0,70 |
| DQN / PPO | 0,10 | 0,25 |
| Regressão polinomial | 0,60 | 0,85 |
| Clustering hierárquico | 0,80 | 0,75 |
| KDE | 0,75 | 0,80 |
| ICA | 0,50 | 0,75 |
| Z-score / Z robusto (MAD) | 1,00 | 1,00 |
| Apriori / FP-Growth | 0,90 | 0,80 |
| Self-Training | 0,50 | 0,70 |
| Co-Training | 0,45 | 0,55 |
| Label Spreading / Propagation | 0,30 | 0,60 |
| Programação dinâmica | 0,85 | 0,80 |
| Dyna-Q | 0,75 | 0,65 |

**Faixas qualitativas usadas na matriz 12.5 do manual:** Alta ≥ 0,75 · Média 0,45 a 0,74 · Baixa < 0,45. A auditoria confere, modelo a modelo, que o nível da matriz, o bloco 14 do card e esta tabela concordam.
### 5.2 Cálculo de referência

```python
import numpy as np, pandas as pd

PESOS = {"desempenho": .30, "estabilidade": .20, "interpretabilidade": .15,
         "custo": .10, "adequacao": .10, "manutencao": .10, "negocio": .05}

def minmax(v, maior_melhor=True):
    v = np.asarray(v, dtype=float)
    if v.max() == v.min():
        return np.ones_like(v)
    z = (v - v.min()) / (v.max() - v.min())
    return z if maior_melhor else 1 - z

def model_fit_score(cand: pd.DataFrame, pesos=PESOS) -> pd.DataFrame:
    """cand: colunas = score_medio, desvio_folds, tempo_s, interpretabilidade,
       adequacao, manutencao, negocio (as quatro ultimas ja em [0,1])."""
    out = cand.copy()
    out["desempenho"]   = minmax(cand["score_medio"])
    out["estabilidade"] = minmax(cand["desvio_folds"], maior_melhor=False)
    out["custo"]        = minmax(cand["tempo_s"], maior_melhor=False)
    out["MFS"] = sum(out[c] * p for c, p in pesos.items())
    return out.sort_values("MFS", ascending=False)
```

**Regra de desempate:** com MFS equivalente (diferença < 0,02), vence o modelo de **nível mais baixo** da §4.

---

## 6. Template de resposta — Diagnóstico do Dataset (16 itens)

Copie e preencha. Os 16 itens são obrigatórios.

```markdown
## Diagnóstico do Dataset — <nome/objetivo>

**1. Tipo de problema:** <supervisionado/não supervisionado/recomendação/reforço> · <regressão | classificação binária | multiclasse | multirrótulo | clustering | anomalias | redução | densidade | ranking de itens | bandits | controle sequencial>

**2. Target:** <coluna> · <tipo e distribuição> · janela de observação: <X> · janela de previsão: <Y> · corte temporal: <data>
   (Não supervisionado: "não há target"; declarar o objetivo substituto.)

**3. Características dos dados:**
   - Tamanho: n = <linhas>, p = <colunas> → <pequeno|médio|grande|muito grande>
   - Tipos: <numérico/categórico/misto/texto/temporal>; categóricas de alta cardinalidade: <lista ou nenhuma>
   - Ausentes: <coluna: %> · padrão: <aleatório|informativo>
   - Outliers: <irrelevantes|relevantes|dominantes>
   - Desbalanceamento: <taxa da classe positiva> → <leve|moderado|extremo>
   - Multicolinearidade: <baixa|alta> · Dimensionalidade p/n: <valor>
   - Estrutura: <temporal? entidade repetida? agrupamento?>

**4. Riscos identificados:** <leakage, viés amostral, drift, features indisponíveis em produção, rótulo ruidoso, subgrupos sub-representados>

**5. Pré-processamento recomendado:** <por tipo de coluna, tudo dentro do Pipeline> — justificar cada escolha pela família de modelo da §3.9

**6. Baseline:** <Dummy(estratégia) + modelo de Nível 1> · valor esperado da métrica principal: <número ou "a medir">

**7. Modelos recomendados**
   1. <Modelo> — **por quê:** <regra IF/THEN aplicada> · **pressupostos e se os dados os satisfazem:** <…> · **vantagens:** <…> · **limitações:** <…> · nível <1-4>
   2. <Modelo> — **por quê:** … · **vantagens:** … · **limitações:** … · nível <1-4>
   3. <Modelo> — **por quê:** … · **vantagens:** … · **limitações:** … · nível <1-4>
   (Pelo menos um candidato de nível inferior ao melhor.)

**8. Estratégia de validação:** <esquema> · <n_splits> · <estratificação/grupo/gap> · **por quê:** <regra da §3.7>

**9. Métrica principal:** <métrica> · **por quê:** <custo do erro que ela captura>

**10. Métricas secundárias:** <lista> · **o que cada uma revela:** <…>

**11. Hiperparâmetros a explorar:** <por modelo, com faixas e método de busca>

**12. Critério de escolha:** Model Fit Score com pesos <lista> · ajustes de peso: <se houver, justificar> · regra de promoção de nível aplicada: <sim/não>

**13. Modelo final proposto:** <modelo> · **condições que o mantêm válido:** <volume, distribuição, disponibilidade das features> · **quando reavaliar:** <gatilho>

**14. Riscos de overfitting:** <onde nasce neste caso> · **controles:** <early stopping, regularização, poda, limite de capacidade> · **sinal de alerta:** <diferença treino × validação aceitável>

**15. Riscos de leakage:** <itens do checklist §3.6 que exigem atenção> · **como foram mitigados:** <…>

**16. Próximos experimentos:** <lista priorizada, do mais barato ao mais caro, com hipótese e critério de sucesso de cada um>
```

---

## 7. Exemplo preenchido (referência de formato e de nível de detalhe)

```markdown
## Diagnóstico do Dataset — Fraude em transações de cartão

**1. Tipo de problema:** supervisionado · classificação binária (positivo raro)

**2. Target:** `is_fraude` · binário · 0,17% positivos · janela de observação: 90 dias de histórico por cartão ·
   janela de previsão: no ato da transação · corte temporal: treino ≤ 2026-06-30, teste ≥ 2026-07-01

**3. Características dos dados:**
   - Tamanho: n = 2.400.000, p = 48 → muito grande
   - Tipos: misto; alta cardinalidade em `merchant_id` (38.000 níveis) e `mcc` (320)
   - Ausentes: `score_bureau` 23% (padrão informativo — ausente para conta nova), demais < 2%
   - Outliers: relevantes em `valor` (cauda longa legítima)
   - Desbalanceamento: 0,17% → **extremo**
   - Multicolinearidade: baixa · p/n ≈ 0,00002
   - Estrutura: temporal **e** entidade repetida (`cartao_id`)

**4. Riscos identificados:** leakage por campos preenchidos após a contestação (`estorno`, `motivo_contestacao`);
   drift sazonal; rótulo atrasado (fraude confirmada só após 60 dias) → o período recente tem rótulo incompleto.

**5. Pré-processamento recomendado:** nenhum scaler (modelo de árvore); `merchant_id` e `mcc` como categóricas
   nativas do CatBoost/LightGBM; `score_bureau` **sem imputação** + indicador de ausência; features de janela
   por cartão (contagem e valor nas últimas 1h/24h/7d) calculadas apenas com o passado. Tudo dentro do Pipeline.

**6. Baseline:** `DummyClassifier(strategy="prior")` (PR-AUC ≈ 0,0017) + LogisticRegression com `class_weight="balanced"`.

**7. Modelos recomendados**
   1. **LightGBM** — por quê: tabular muito grande com categóricas de alta cardinalidade e NaN nativo (§3.2, §3.3).
      Vantagens: mais rápido da categoria, categóricas nativas. Limitações: overfitta se `num_leaves` for alto; exige early stopping. Nível 3.
   2. **CatBoost** — por quê: 38.000 níveis em `merchant_id` favorecem a codificação ordenada (§3.3).
      Vantagens: menos leakage no encoding, bons defaults. Limitações: treino mais lento. Nível 3.
   3. **LogisticRegression (balanced)** — por quê: candidato de nível inferior obrigatório (§2 passo 8).
      Vantagens: interpretável, barato, latência mínima. Limitações: não captura interações. Nível 1.

**8. Estratégia de validação:** `TimeSeriesSplit(n_splits=5, gap=<60 dias>)` · o gap cobre o atraso de confirmação do rótulo ·
   por quê: há ordem temporal (§3.7) e o rótulo amadurece com atraso.

**9. Métrica principal:** **PR-AUC** (`average_precision`) · por quê: positivo < 1% e o custo está em capturar fraude
   sem inundar a operação de falsos positivos (§3.8).

**10. Métricas secundárias:** precision@k (k = capacidade diária de análise), recall no threshold operacional,
   matriz de confusão, custo esperado (R$) por threshold. ROC-AUC apenas como referência comparativa.

**11. Hiperparâmetros a explorar:** LightGBM — `num_leaves` 31–127, `min_child_samples` 50–500,
   `learning_rate` 0,02–0,1 (log), `feature_fraction` 0,6–1,0, `lambda_l2` 0–10, `n_estimators` até 5.000 com
   `early_stopping(100)`. Busca: `RandomizedSearchCV` com 60 amostras.

**12. Critério de escolha:** Model Fit Score com estabilidade elevada para 0,30 (drift sazonal) e desempenho em 0,25;
   demais pesos padrão. Regra de promoção aplicada: sim — LightGBM só substitui a logística se o ganho em PR-AUC
   superar o desvio entre folds.

**13. Modelo final proposto:** LightGBM com early stopping, threshold definido pela capacidade operacional.
   Válido enquanto a taxa base de fraude e o mix de canais se mantiverem; reavaliar a cada trimestre ou se o PSI das
   features principais ultrapassar 0,2.

**14. Riscos de overfitting:** alto — boosting em classe extremamente rara memoriza padrões de poucos positivos.
   Controles: early stopping por PR-AUC de validação, `min_child_samples` alto, `feature_fraction` < 1,
   monitorar diferença treino × validação (alerta se PR-AUC de treino for > 2× o de validação).

**15. Riscos de leakage:** campos pós-contestação (removidos); janelas móveis (recalculadas só com o passado);
   `cartao_id` repetido (coberto pelo split temporal, que separa períodos, não cartões — documentar essa escolha);
   rótulo imaturo no fim da janela (tratado com `gap`).

**16. Próximos experimentos:**
   1. Baseline logístico com features de janela — custo baixo, hipótese: PR-AUC ≥ 0,10. 
   2. LightGBM com categóricas nativas — hipótese: ganho ≥ 30% sobre o baseline.
   3. CatBoost com `merchant_id` ordenado — hipótese: ganho adicional ≥ 5%.
   4. Ajuste de threshold por custo — hipótese: mesmo recall com 20% menos alertas.
   5. IsolationForest como sinal complementar para fraudes de padrão novo (sem rótulo).
```

---

## 8. Guardrails — o que invalida um diagnóstico

O agente deve recusar, corrigir ou sinalizar explicitamente qualquer um destes:

| Erro | Por que invalida |
|---|---|
| Recomendar modelo antes de definir target, validação e métrica | Inverte a ordem causal do problema |
| Accuracy como métrica principal sob desbalanceamento | Prever sempre a classe majoritária já atinge valor alto |
| K-Fold embaralhado em dados temporais | Usa o futuro para prever o passado |
| `fit` de scaler/imputer/encoder/PCA/SMOTE fora do fold de treino | Vazamento de pré-processamento |
| Reportar só a média entre folds | Esconde instabilidade; o desvio é parte do resultado |
| Usar o conjunto de teste para escolher modelo ou threshold | Converte teste em validação e infla a estimativa |
| Threshold fixo em 0,5 sem justificativa | O corte é decisão de negócio, não constante |
| Afirmar que Random Forest não sofre overfitting | Falso: é mais robusto que uma árvore isolada, não imune |
| Afirmar que XGBoost/Deep Learning é sempre melhor | Falso: depende de dado, tamanho, tuning e restrições |
| Deep Learning em tabular pequeno/médio sem justificativa | Contraria a evidência de benchmark e o custo de manutenção |
| Adicionar features sem hipótese | Ruído e maldição da dimensionalidade |
| Interpretar coeficientes de OLS com multicolinearidade alta | Coeficientes instáveis e sem significado marginal |
| Tratar perda, otimizador ou framework como modelo | Erro taxonômico da §1 |
| Prometer desempenho antes de medir | Qualquer modelo pode generalizar mal |
| Split aleatório de interações em recomendação | Treina com o futuro; resultado otimista |
| Avaliar recomendador só por RMSE de nota | O usuário vê um ranking, não uma nota |
| Popularidade calculada com o período inteiro | Vazamento temporal no baseline |
| Concluir algo em RL com uma única semente | Variância entre execuções é da ordem do efeito medido |
| Tratar `truncated` como `terminated` (Gymnasium) | Zera o valor futuro indevidamente e enviesa Q |
| Usar RL quando a ação não altera o futuro | Complexidade e risco sem benefício — supervisionado ou bandits bastam |
| Tratar lift alto como causalidade | Co-ocorrência não é efeito; a ação precisa de validação |
| Medir semissupervisionado sobre pseudo-rótulos | Mede a concordância do modelo consigo mesmo, não o acerto |
| Adotar semissupervisionado sem comparar com o baseline só-rotulados | O ganho pode ser nulo ou negativo |
| Z-score clássico em dados contaminados | Os outliers inflam média e desvio e se escondem (*masking*) |
| Chamar PCA/ICA de “associação” ou regressão *múltipla* de *multivariada* | Erro taxonômico: leva a métodos e métricas errados |
---

## 9. Nota de versões e APIs (setembro de 2026)

Referência: scikit-learn **1.9.1** · XGBoost **3.4.1** · LightGBM 4.x · CatBoost 1.2.x · Keras 3 · PyTorch 2.x · TensorFlow 2.x (2.21 verificado) · Gymnasium 1.x · mlxtend 0.25.
**Confirme as versões instaladas antes de executar qualquer snippet.**

As linhas desta tabela foram conferidas **por execução** contra a pilha completa — scikit-learn 1.9.1, XGBoost 3.4.1, LightGBM 4.7.0, CatBoost 1.2.10, PyTorch 2.14.0, Keras 3.15.1, TensorFlow 2.21.0 (Python 3.12), Gymnasium 1.3.0, mlxtend 0.25.0. Os 69 trechos de código desta skill e do manual foram executados sem erro; ver `auditoria_ml.md`.

| Item | Status | Ação |
|---|---|---|
| `multi_class` em `LogisticRegression`/`LogisticRegressionCV` | Removido na 1.8 | Com K ≥ 3 usa multinomial automaticamente; para OvR use `OneVsRestClassifier(LogisticRegression(...))` |
| `squared` em `mean_squared_error` | Removido na 1.6 | Usar `root_mean_squared_error` |
| `sparse` em `OneHotEncoder` | Renomeado na 1.2 | Usar `sparse_output` |
| `penalty` em `LogisticRegression` | Depreciado na 1.8, remoção prevista para 1.10 | Orientação oficial: usar `l1_ratio` e `C` |
| `n_alphas` em `ElasticNetCV`/`LassoCV`/`MultiTask*CV` | Removido na 1.9 | Passar a grade `alphas` explicitamente |
| `categorical_features="from_dtype"` em `HistGradientBoosting*` | Padrão desde a 1.6 | Marcar colunas como `category` |
| `random_state` em `OneClassSVM` | Ausente na assinatura atual | Não passar |
| `cv="prefit"` em `CalibratedClassifierCV` | Depreciado na 1.6, **removido na 1.8** | Envolver o modelo treinado em `FrozenEstimator` e chamar sem `cv` |
| `scoring` em `LogisticRegressionCV` | Em transição: default atual é o sentinela `"warn"`; muda em 1.11 (accuracy → `neg_log_loss`) | **Fixar `scoring` explicitamente** |
| `sparse_interface` (config global) | Novo | Retorno esparso migrará de `spmatrix` para `sparray` |
| `device="cuda"` no XGBoost | Substitui `tree_method="gpu_hist"`; sem GPU **não falha** — emite `UserWarning` e cai para CPU | Depende de build com CUDA; confira o aviso antes de supor que está na GPU |
| LightGBM early stopping | Via `callbacks` | `callbacks=[lgb.early_stopping(50), lgb.log_evaluation(100)]` |
| CatBoost `eval_set` | Tupla única é a forma idiomática (uma lista com uma tupla também é aceita na 1.2.x) | `eval_set=(X_val, y_val)` |
| PyTorch | — | `optimizer.zero_grad()` antes de `loss.backward()` a cada iteração |
| TensorFlow ≥ 2.16 | `tf.keras` **é o Keras 3** | Código `tf.keras` e `keras` é o mesmo; TensorFlow ainda não publica pacote para Python 3.14 (use 3.12/3.13) |
| Keras 3 — salvar × exportar | `model.save("x.keras")` ≠ `model.export("dir")` | `.keras` para retomar treino; `export()` gera o SavedModel de inferência (TF Serving) |
| Keras 3 sem TensorFlow instalado | O backend padrão é `tensorflow` | Definir `KERAS_BACKEND=torch` ou `jax` antes do `import keras` |
| Gymnasium (sucessor do Gym) | `reset()` → `(obs, info)`; `step()` → `(obs, r, terminated, truncated, info)` | Código do Gym antigo (4 valores) quebra ou confunde truncamento com término; `reset(seed=…)` não semeia `action_space.sample()` — use `env.action_space.seed(…)` |
| mlxtend 0.25 `association_rules` | `num_itemsets` tem default 1 e **só é usado com `null_values=True`** | Com dados faltantes, passe o número de transações |
| `SelfTrainingClassifier` | Classificador de base no parâmetro `estimator`; não rotulados marcados com `-1` | Exige `predict_proba` no classificador de base |
| `FastICA` | `whiten="unit-variance"` | Ordem, sinal e escala das fontes são indeterminados |
| `LabelSpreading` / `LabelPropagation` | `kernel="rbf"` (grafo denso) ou `"knn"` | O grafo decide o resultado; RBF usa memória O(n²) |
---

## 10. Snippets canônicos

**Pipeline à prova de vazamento (classificação tabular mista):**
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
import numpy as np

pre = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median", add_indicator=True)),
                      ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("ohe", OneHotEncoder(handle_unknown="infrequent_if_exist"))]), cat_cols),
])
pipe = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
cv = StratifiedKFold(5, shuffle=True, random_state=42)
res = cross_validate(pipe, X, y, cv=cv, scoring=["average_precision", "roc_auc", "f1"])
print({k: (np.mean(v).round(4), np.std(v).round(4)) for k, v in res.items() if k.startswith("test_")})
```

**Validação temporal com atraso de rótulo:**
```python
from sklearn.model_selection import TimeSeriesSplit
cv = TimeSeriesSplit(n_splits=5, gap=periodos_ate_o_rotulo_amadurecer)
```

**Boosting com early stopping (referência das três bibliotecas):**
```python
# XGBoost 3.x — early stopping no construtor
from xgboost import XGBClassifier
xgb = XGBClassifier(n_estimators=2000, learning_rate=0.05, max_depth=6,
                    subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0,
                    early_stopping_rounds=50, eval_metric="aucpr",
                    enable_categorical=True, n_jobs=-1, random_state=42)
xgb.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=100)

# LightGBM — early stopping por callbacks
import lightgbm as lgb
lgbm = lgb.LGBMClassifier(n_estimators=3000, learning_rate=0.05, num_leaves=63,
                          min_child_samples=40, n_jobs=-1, random_state=42)
lgbm.fit(X_train, y_train, eval_set=[(X_val, y_val)], eval_metric="average_precision",
         callbacks=[lgb.early_stopping(50), lgb.log_evaluation(100)])

# CatBoost — eval_set como TUPLA unica
from catboost import CatBoostClassifier
cb = CatBoostClassifier(iterations=3000, learning_rate=0.05, depth=6,
                        eval_metric="PRAUC", auto_class_weights="Balanced",
                        random_seed=42, verbose=False)
cb.fit(X_train, y_train, cat_features=cat_idx, eval_set=(X_val, y_val),
       early_stopping_rounds=50)
```

**Calibração de probabilidade (quando a probabilidade entra na decisão):**
```python
from sklearn.calibration import CalibratedClassifierCV, CalibrationDisplay
from sklearn.frozen import FrozenEstimator          # cv="prefit" foi removido na 1.8
cal = CalibratedClassifierCV(FrozenEstimator(modelo_treinado), method="isotonic")
cal.fit(X_valid, y_valid)
CalibrationDisplay.from_estimator(cal, X_test, y_test)
```

**Ajuste de threshold:**
```python
from sklearn.model_selection import TunedThresholdClassifierCV
tuned = TunedThresholdClassifierCV(clf, scoring="f1").fit(X_train, y_train)
print(tuned.best_threshold_)
```

**Clustering com escolha de k:**
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
Xs = StandardScaler().fit_transform(X)
for k in range(2, 11):
    lab = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(Xs)
    print(k, round(silhouette_score(Xs, lab), 3), round(davies_bouldin_score(Xs, lab), 3))
```

**Métricas de recomendação @k (conferência com o scikit-learn):**
```python
import numpy as np
from sklearn.metrics import ndcg_score
relevantes, ranking, k = {2, 5, 7}, [5, 1, 2, 9, 3, 7, 4, 0, 6, 8], 5
acertos = [1 if i in relevantes else 0 for i in ranking[:k]]
precision_k, recall_k = sum(acertos) / k, sum(acertos) / len(relevantes)
y_true = np.array([[1 if i in relevantes else 0 for i in range(10)]])
y_score = np.zeros((1, 10)); y_score[0, ranking] = np.arange(10, 0, -1)
print(precision_k, recall_k, ndcg_score(y_true, y_score, k=k))
```

**Avaliação off-policy (IPS / SNIPS) a partir de log:**
```python
import numpy as np
rng = np.random.default_rng(7)
pi_log, pi_nova = np.array([.5, .25, .25]), np.array([.1, .8, .1])
acoes = rng.choice(3, size=20000, p=pi_log)
r = (rng.random(20000) < np.array([.02, .05, .03])[acoes]).astype(float)
peso = pi_nova[acoes] / pi_log[acoes]
print("IPS:", np.mean(peso * r), "| SNIPS:", np.sum(peso * r) / np.sum(peso))
```

**Regras de associação (FP-Growth):**
```python
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
cestas = [["pao", "leite", "manteiga"], ["pao", "manteiga"], ["leite", "cafe"], ["pao", "leite", "manteiga", "cafe"]]
te = TransactionEncoder()
df = pd.DataFrame(te.fit(cestas).transform(cestas), columns=te.columns_)
regras = association_rules(fpgrowth(df, min_support=0.5, use_colnames=True), metric="lift", min_threshold=1.0)
regras["regra"] = [", ".join(sorted(a)) + " -> " + ", ".join(sorted(c)) for a, c in zip(regras["antecedents"], regras["consequents"])]
print(regras.sort_values(["lift", "regra"], ascending=[False, True])[["regra", "support", "confidence", "lift"]])   # ordem reprodutivel
```

**Protocolo semissupervisionado (holdout rotulado + baseline):**
```python
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.semi_supervised import SelfTrainingClassifier
from sklearn.svm import SVC
from sklearn.metrics import f1_score
X, y = make_moons(1000, noise=0.1, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)  # holdout ROTULADO
rot = np.zeros(len(y_tr), bool); rot[np.random.default_rng(0).choice(len(y_tr), 20, replace=False)] = True
base = SVC(probability=True).fit(X_tr[rot], y_tr[rot])
semi = SelfTrainingClassifier(SVC(probability=True), threshold=0.9).fit(X_tr, np.where(rot, y_tr, -1))
print(f1_score(y_te, base.predict(X_te)), f1_score(y_te, semi.predict(X_te)))   # adote so se ganhar
```

**Anomalias sem rótulo:**
```python
from sklearn.ensemble import IsolationForest
iso = IsolationForest(n_estimators=200, contamination=0.01, random_state=42, n_jobs=-1).fit(X_train)
pred = iso.predict(X_test)          # +1 inlier, -1 outlier
score = iso.score_samples(X_test)   # quanto MAIOR, mais normal
```

---

## 11. Consistência com o manual HTML

Esta skill decide; o `manual_machine_learning.html` explica. A divisão de uso dos dois arquivos (estudar / consultar / decidir) está descrita na seção **“Como usar este manual”** (`manual_machine_learning.html#comousar`), que também traz as formas de instalar esta skill em um agente. Quando o usuário pedir contexto conceitual, aponte a seção correspondente em vez de reescrevê-la.

| Assunto | Aqui | No manual |
|---|---|---|
| Taxonomia e mitos | §1, §8 | Seções 1.2 e 15 |
| Famílias de modelos e template de 20 blocos | §3.1 | Seções 2 a 5 (cards) |
| Regularização e otimização | §3.9, §4 | Seções 6 e 7 |
| Métricas, validação e leakage | §3.6–3.8 | Seção 8 |
| Seleção de modelos e Model Fit Score | §5 | Seção 9 |
| Pré-processamento e feature engineering | §3.4, §3.9 | Seção 10 |
| Pipeline ponta a ponta | §10 | Seção 11 |
| Árvore de decisão e matrizes | §2, §3 | Seções 12 e 13 |
| Casos empresariais | §7 | Seção 14 |
| Versões e APIs | §9 | Seção 15 (nota de auditoria) |
| TensorFlow na prática | §9 | Seção 5.1 |
| Sistemas de recomendação | Passo 2, §3.10, §4.4 | Seção 16 (4 cards) |
| Bandits e aprendizagem por reforço | Passo 2, §3.11, §4.4 | Seção 17 (6 cards, incluindo 17.6 — baseado em modelo) |
| Mapa de paradigmas e correções de roadmaps | Passo 2 e §8 | Seção 1.5 |
| Regressão multivariada | Passo 3 | Seção 2.1 |
| Regras de associação | §3.13 | Seção 3.5 (2 cards) |
| ICA e Z-score robusto | §3.1 | Seções 3.2 e 3.3 |
| Semissupervisionado | Passo 2, §3.12, §4.4 | Seção 18 (3 cards) |
| Sete critérios por modelo | Conduta nº 6, §5 | Seção 12.5 (matriz de 43 modelos) |
| Relatório de auditoria técnica | — | `auditoria_ml.md` + scripts em `auditoria/` |

**Referências usadas nas justificativas:** Breiman (2001); Chen & Guestrin (2016); Grinsztajn, Oyallon & Varoquaux (2022); Kaufman, Rosset, Perlich & Stitelman (2012); Saito & Rehmsmeier (2015).
