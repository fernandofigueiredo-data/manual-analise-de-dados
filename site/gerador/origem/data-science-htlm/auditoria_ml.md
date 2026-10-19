# Auditoria Técnica — Manual de ML e Skill de Decisão

**Papel assumido:** Principal ML Engineer revisando material de referência antes da publicação.
**Artefatos auditados:** `manual_machine_learning.html` (Etapas 1 e 3) e `skill_decisao_ml.md` (Etapa 2).
**Data da auditoria:** 11 de setembro de 2026. **Reexecução com a pilha de referência completa:** 12 de setembro de 2026.
**Método:** verificação **executada**, não declarativa — 4 scripts reproduzíveis em `auditoria/`, que introspeccionam a API instalada, conferem as fórmulas numericamente, executam cada trecho de código em processo isolado e cruzam os dois artefatos.

---

## 0. Estado atual (21/09/2026) — após a incorporação do roadmap de algoritmos

Depois da extensão de 18/09 (TensorFlow, recomendação, reforço — §8), o material incorporou um roadmap de algoritmos (§9): **18 seções, 43 modelos, 16 categorias**, a matriz dos sete critérios e as regras correspondentes na skill. Resultado consolidado das 6 baterias:

| Bateria | Resultado |
|---|---|
| 01 · APIs do scikit-learn | **25/25** |
| 02 · Fórmulas conferidas numericamente | **43/43** |
| 03 · Execução de todos os trechos de código | **69/69** sem erro |
| 04 · Consistência estrutural (taxonomia, métricas, pré-processamento, HTML ↔ MD, **matriz × card × escala da skill**, **YAML da skill**, **sementes do Gymnasium e do TensorFlow**) | **zero** achados |
| Reprodutibilidade · bateria 06 executada duas vezes em paralelo | **saídas idênticas** |
| 05 · APIs de TensorFlow, Gymnasium e mlxtend | **12/12** |
| 06 · Saídas que demonstram o que o texto afirma | **23/23** |

**Total de achados: 37**, todos corrigidos — 11 na auditoria original (§3), 12 na reauditoria da extensão (§8), 9 na incorporação do roadmap (§9) e 5 na primeira execução com os ambientes locais (§10).

---

## 1. Veredito

| Eixo exigido pela Etapa 4 | Resultado |
|---|---|
| Nenhuma classificação de categoria errada | **Aprovado** — 26/26 cards com categoria coerente; nenhuma perda, otimizador, framework ou métrica aparece como modelo |
| Fórmulas corretas | **Aprovado com 1 correção** — 21/21 conferidas numericamente; a escala 1/(2n) de Lasso/Elastic Net estava omitida |
| Código válido nas APIs atuais | **Aprovado com 2 correções** — **42/42** trechos executados sem erro na pilha de referência completa (contagem corrigida na §8 — antes publicada como 43/43); 1 quebrava (`cv="prefit"`) e 1 mascarava fallback de GPU |
| Ausência de afirmações absolutas | **Aprovado com 1 ajuste** — nenhuma afirmação de superioridade universal; 1 redação matemática imprecisa |
| Ressalva de generalização | **Aprovado** — presente e explícita nos dois artefatos |
| Métricas ligadas ao tipo de problema | **Aprovado com 2 correções** — 2 cards listavam métricas incompletas para as próprias tags |
| Modelos ligados ao tipo de dataset | **Aprovado com 1 correção** — 1 card divergia da tabela de pré-processamento da skill |
| Consistência HTML ↔ MD | **Aprovado com 3 correções** — versões, depreciações e hierarquia agora batem item a item |

**Total: 11 achados — 1 de severidade alta, 1 média, 8 baixas, 1 informativo. Todos corrigidos nesta etapa.**
Após as correções, as 4 baterias passam limpas: **18/18** afirmações de API confirmadas, **21/21** fórmulas conferidas numericamente, **42/42** trechos de código executados sem erro (corrigido de 43/43 — ver A-23) e **zero** achados estruturais. **Não há mais lacuna de cobertura de execução:** todas as bibliotecas citadas pelo material foram instaladas e exercitadas.

---

## 2. Ambiente de verificação

| Biblioteca | Versão exercitada | Referência dos artefatos | Situação |
|---|---|---|---|
| Python | 3.14.7 | — | — |
| scikit-learn | **1.9.1** | 1.9.1 | **Versão exata da referência** |
| XGBoost | **3.4.1** | 3.4.1 | **Versão exata da referência** |
| LightGBM | **4.7.0** | 4.x | Confere |
| CatBoost | **1.2.10** | 1.2.x | Confere |
| PyTorch | **2.14.0** | 2.x | Confere |
| Keras | **3.15.1** (backend torch) | 3 | Confere |
| numpy / pandas / scipy | 2.5.2 / 3.0.5 / 1.18.1 | — | — |

A primeira passagem da auditoria (11/09) rodou sem XGBoost, LightGBM, PyTorch e Keras — 5 trechos ficaram sem verificação empírica. Essa lacuna **foi fechada em 12/09**: instalado o runtime OpenMP (`brew install libomp`) e montado um ambiente isolado com a pilha completa. Duas observações de ambiente, necessárias para reproduzir:

- **`libomp` é keg-only no Homebrew** — não é ligado a `/opt/homebrew/lib`. Sem `export DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib`, o `import xgboost` continua falhando com `XGBoostError` e o `import lightgbm` com `OSError`.
- **Keras 3 exige um backend explícito** quando o TensorFlow não está instalado: o trecho do manual foi executado com `KERAS_BACKEND=torch`. O código do snippet é agnóstico de backend; o que a variável resolve é o ambiente, não o código.

> **Limitação declarada:** os trechos de XGBoost, LightGBM, PyTorch e Keras **não puderam ser executados**. Foram revisados estaticamente contra a documentação das versões citadas e contra as mudanças de API já conhecidas, mas **não têm verificação empírica**. Para fechar essa lacuna basta instalar o runtime OpenMP (`brew install libomp`) e rodar `auditoria/03_executar_snippets.py` de novo. O CatBoost, que era o caso mais sensível (comportamento do `eval_set`), foi verificado de fato.

---

## 3. Achados e correções

### ALTA

**A-01 · `CalibratedClassifierCV(..., cv="prefit")` não existe mais** — `manual_machine_learning.html`, Seção 4 (Calibração).
O parâmetro foi depreciado na 1.6 e **removido na 1.8**. O trecho publicado levantava exceção:

```
InvalidParameterError: The 'cv' parameter of CalibratedClassifierCV must be an int in the
range [2, inf), an object implementing 'split' and 'get_n_splits', an iterable or None.
Got 'prefit' instead.
```

*Correção aplicada:* substituído pelo caminho atual, com `FrozenEstimator`, e o motivo registrado em comentário. O mesmo trecho foi acrescentado aos snippets canônicos da skill (§10) e a remoção entrou na tabela de APIs (§9) dos dois artefatos.

```python
from sklearn.frozen import FrozenEstimator
cal = CalibratedClassifierCV(FrozenEstimator(modelo_ja_treinado), method="isotonic")
cal.fit(X_valid, y_valid)
```

### MÉDIA

**A-02 · Fórmulas de Lasso e Elastic Net sem a normalização 1/(2n)** — cards `lasso` e `elasticnet`.
O manual publicava `J(w) = Σ(y − Xw)² + α·Σ|wⱼ|`, mas o scikit-learn minimiza `(1/2n)·||y − Xw||² + α·||w||₁`. A diferença não é cosmética: **o α da fórmula publicada não é o α da biblioteca**. Verificação numérica (`auditoria/02_formulas.py`), com α = 0,1 e n = 200:

| Forma minimizada | Distância máxima para `Lasso.coef_` |
|---|---|
| Com 1/(2n) — a do scikit-learn | 2,2 × 10⁻⁹ |
| Sem 1/(2n) — a que estava publicada | **1,3 × 10⁻¹** |

*Correção aplicada:* fator 1/(2n) acrescentado às duas fórmulas, com aviso explícito de escala. Também foi documentado no card `ridge` que **Ridge não normaliza por n** no scikit-learn — portanto os α de Ridge e Lasso não são comparáveis entre si (esse ponto foi confirmado numericamente: a forma do Ridge publicada bate com a biblioteca com erro de 9,5 × 10⁻⁹).

### BAIXA

| ID | Onde | Achado | Correção |
|---|---|---|---|
| **A-03** | Card `catboost` + skill §9 | Afirmava que `eval_set` **deve** ser tupla única, "não lista de tuplas". Execução real no CatBoost 1.2.10: a lista com uma tupla **também é aceita** | Reescrito como "forma idiomática; lista com uma tupla também é aceita na 1.2.x" |
| **A-04** | Seção "Como usar" | Bloco de comandos de shell era processado pelo realce de sintaxe **Python**, sem indicação de linguagem | Bloco marcado com `data-lang="shell"`, realce condicional por linguagem e etiqueta visível no canto do bloco |
| **A-05** | Card `catboost`, bloco 09 | Dizia apenas "praticamente nenhum", divergindo da tabela §3.9 da skill, que classifica CatBoost como "não exige escala" | Bloco 09 agora afirma explicitamente que não exige padronização, aceita NaN e dispensa encoding |
| **A-06** | Card `extra-trees`, bloco 17 | Métricas delegadas ("as mesmas do Random Forest") — o card não se sustenta sozinho e não aparece em buscas por "RMSE" | Métricas nomeadas, com a ressalva de que OOB não está disponível com `bootstrap=False` |
| **A-07** | Card `svm`, bloco 17 | Card marcado também como **Regressão** (SVR), mas o bloco 17 listava só métricas de classificação | Acrescentadas MAE, RMSE e R² para o caso SVR |
| **A-08** | Seção 3.1, tabela do Elbow | "a inércia **sempre** cai com k" — a monotonicidade vale para a solução ótima; com k-means++ e mínimos locais pode oscilar | Redação precisada |
| **A-09** | Nota de auditoria (HTML) + skill §9 | Dizia que o default de `scoring` em `LogisticRegressionCV` é accuracy. O default real na 1.9.0 é o sentinela `'warn'` (estado de transição) | Redação corrigida nos dois arquivos, mantendo a recomendação de fixar `scoring` explicitamente |

### INFORMATIVO

**A-10 · Cobertura de execução — lacuna fechada.** Na primeira passagem, 37 dos 42 trechos reais foram executados (o relatório dizia 38 de 43 — ver A-23). Após instalar o runtime OpenMP e a pilha completa, **os 42 trechos publicados foram executados e todos passam**, incluindo os cards de XGBoost, LightGBM, CatBoost e Rede Neural (Keras 3 + PyTorch 2.x).

### BAIXA (encontrado na reexecução com GPU/boosting ativos)

**A-11 · `device="cuda"` não falha sem GPU — ele silenciosamente treina na CPU.** Card `xgboost`.
O snippet publicado fixa `device="cuda"`. Em máquina sem GPU, o XGBoost 3.4.1 **não levanta erro**: emite um `UserWarning` e troca o dispositivo.

```
UserWarning: WARNING: src/context.cc:218: Device is changed from GPU to CPU
as we couldn't find any available GPU on the system.
```

Isso é pior que um erro para quem estuda: o leitor supõe estar treinando em GPU e não está. *Correção aplicada:* comentário explícito no snippet e a linha da nota de auditoria reescrita nos dois artefatos, descrevendo o fallback e instruindo a conferir o aviso.

---

## 4. Evidências por eixo

### 4.1 Taxonomia (26 cards)
Nenhum card de modelo tem nome de função de perda, otimizador, framework ou métrica. Todo card declara no bloco 02 uma categoria compatível com suas etiquetas. Cross Entropy, Gradient Descent e os frameworks aparecem **exclusivamente** nas seções 7 (otimização e perdas) e 5 (frameworks), sempre rotulados como o que são, e os quatro mitos taxonômicos estão explicitamente negados nas seções 1.2 e 15 e na §1 da skill.

### 4.2 Fórmulas — 21/21 conferidas numericamente
Cada fórmula publicada foi implementada a partir do texto do manual e comparada com a referência da biblioteca:

| Fórmula | Referência de comparação | Resultado |
|---|---|---|
| Gini = 1 − Σpᵢ² | impureza calculada sobre amostra | confere |
| Entropia = −Σpᵢ·log₂pᵢ | `scipy.stats.entropy(base=2)` | confere |
| σ(z) = 1/(1+e⁻ᶻ) | `scipy.special.expit` | confere |
| softmax(zₖ) = e^zₖ/Σe^zⱼ | `scipy.special.softmax` | confere |
| Log Loss binária | `metrics.log_loss` | confere |
| Cross Entropy categórica | `metrics.log_loss` multiclasse | confere |
| MSE · MAE · RMSE · R² | `sklearn.metrics` | confere |
| Precision · Recall · F1 a partir de VN/FP/FN/VP | `precision/recall/f1_score` | confere |
| ∂MSE/∂w = −2·mean(X(y−ŷ)) | diferenças finitas | confere |
| Objetivo do Ridge | `Ridge.coef_` vs otimização direta | confere (9,5 × 10⁻⁹) |
| Objetivo do Lasso e do Elastic Net | `coef_` vs otimização direta | **corrigido** (ver A-02) |
| Inércia do K-Means | `KMeans.inertia_` | confere |
| PCA: λⱼ/Σλ | `explained_variance_ratio_` | confere |
| GMM: Σπₖ·N(x|μₖ,Σₖ) | `score_samples` | confere |
| exp(coef) = razão de chances | probabilidades preditas em x e x+1 | confere |
| Softmax multinomial com K ≥ 3 | `predict_proba` vs `softmax(decision_function)` | confere |
| Naive Bayes: log P(y) + Σx·log P(x|y) | `_joint_log_likelihood` | confere |
| KDE: 1/(n·h)·ΣK((x−xᵢ)/h) | `KernelDensity.score_samples` | confere |
| Var(média) = ρσ² + (1−ρ)σ²/B | simulação com correlação controlada | confere |

### 4.3 Convenções de detecção de anomalias — verificadas em execução
- `IsolationForest`: `predict` devolve +1/−1 e `score_samples` é **maior para pontos mais normais** (faixa observada: −0,798 a −0,365, todos negativos). O escore s(x) do artigo original equivale a `−score_samples`, e nele **s → 1 indica anomalia** — as duas afirmações do manual são verdadeiras, sobre grandezas diferentes.
- `LocalOutlierFactor`: com `novelty=False`, `fit_predict` existe e `predict` **não**; com `novelty=True`, `predict`/`decision_function`/`score_samples` existem e `fit_predict` **não**. Exatamente como o card descreve — confirmado pelas exceções `AttributeError` levantadas nos dois sentidos.

### 4.4 Linguagem absoluta — 39 ocorrências revisadas uma a uma
Classificação: **nenhuma** afirma superioridade universal de modelo. As ocorrências são de três tipos legítimos:
1. **Regras de método** ("sempre padronize antes de métodos baseados em gradiente", "nunca reporte só a média entre folds") — prescrições de processo, corretas.
2. **Mitos citados para serem negados** ("XGBoost é sempre melhor" → *falso*; "Deep Learning é sempre superior" → *falso*).
3. **Negações de absoluto** ("não existe melhor modelo universal", "qualquer modelo pode generalizar mal").

Uma única ocorrência era imprecisão técnica, não exagero retórico, e foi corrigida (A-08).

### 4.5 Ressalva de generalização
Presente e explícita: na Regra de Ouro da seção 15 do manual ("qualquer modelo, inclusive o mais moderno, pode generalizar mal"), na seção "Como usar" ("a skill não garante desempenho"), e como **regra de conduta nº 5** da skill, que a torna obrigatória em toda resposta do agente.

### 4.6 Métrica ↔ tipo de problema e modelo ↔ tipo de dataset
Checagem automatizada card a card: toda etiqueta `reg` exige MAE/RMSE/MSE/R²/MAPE no bloco 17; `clf` exige F1/ROC-AUC/PR-AUC/Log Loss/precision/recall; `clu` exige Silhouette/Davies-Bouldin/Calinski-Harabasz/BIC; detectores de anomalia exigem PR-AUC ou precision@k. Duas divergências encontradas (A-06, A-07) e corrigidas. O bloco 09 de cada card foi cruzado com a tabela §3.9 da skill (quem exige padronização e quem não exige): uma divergência (A-05), corrigida.

### 4.7 Consistência HTML ↔ MD
Cruzamento item a item de versões (1.9.1, 3.4.1, Keras 3, PyTorch 2.x), depreciações (`multi_class`, `root_mean_squared_error`, `sparse_output`, `n_alphas`, `from_dtype`, `sparse_interface`, `FrozenEstimator`), esquemas de validação (`TimeSeriesSplit`, `GroupKFold`), métrica para classe rara (PR-AUC) e composição dos 4 níveis da hierarquia. Após as correções, **nenhum termo aparece em um artefato e falta no outro**.

---

## 5. O que esta auditoria NÃO verificou

Declarado para que ninguém confunda cobertura com garantia:

1. **Execução em GPU** — o fallback do XGBoost para CPU foi observado, mas nenhum trecho foi exercitado com CUDA de fato; o caminho de GPU permanece verificado apenas pela documentação.
2. **Desempenho preditivo** — nenhum número de acurácia, PR-AUC ou RMSE é prometido pelos artefatos, e esta auditoria não mede desempenho em dados reais.
3. **As versões futuras** — as remoções previstas para 1.10, 1.11 e 1.12 ainda não ocorreram; a nota de auditoria as sinaliza como previsão, não como fato.
4. **Adequação pedagógica** — a auditoria é técnica; clareza didática não foi avaliada por terceiros.
5. **Comportamento em navegadores diversos** — o HTML foi validado estruturalmente (tags balanceadas, 58 ids, 40 âncoras internas, zero quebradas, JS sem erro de sintaxe) e exercitado num motor Chromium; não houve teste cruzado em Safari/Firefox.

---

## 6. Como reproduzir

**Ambientes locais (já criados em `htlm/`):**

| Pasta | Conteúdo | Para quê |
|---|---|---|
| `.venv-auditoria/` | Python 3.14 + scikit-learn, XGBoost, LightGBM, CatBoost, PyTorch, Keras, Gymnasium, mlxtend, PyYAML | Baterias 01–06 |
| `.venv-tf/` | Python 3.12 + TensorFlow, scikit-learn | Trechos de TensorFlow (sem pacote para 3.14) |
| `.uv-python/` | O interpretador Python 3.12 usado pelo `.venv-tf` | Mantém o ambiente de TF autocontido na pasta |

**Rodar tudo com um comando:**

```bash
bash auditoria/rodar_tudo.sh
```

O script ajusta `DYLD_LIBRARY_PATH` (o `libomp` é keg-only) e `AUDITORIA_PY_TF`, roda as 6 baterias, mostra só resumos e falhas e termina com `AUDITORIA LIMPA` (código de saída 0) ou `AUDITORIA COM FALHAS` (código 1).

**Recriar os ambientes do zero** (ex.: em outra máquina), a partir de `htlm/`:

```bash
brew install libomp
python3 -m venv .venv-auditoria
./.venv-auditoria/bin/pip install scikit-learn xgboost lightgbm catboost torch keras gymnasium mlxtend pandas scipy pyyaml uv
UV_PYTHON_INSTALL_DIR=$PWD/.uv-python ./.venv-auditoria/bin/uv venv -p 3.12 .venv-tf
VIRTUAL_ENV=$PWD/.venv-tf ./.venv-auditoria/bin/uv pip install tensorflow scikit-learn pandas scipy
```

Para remover tudo: apague as três pastas `.venv-auditoria/`, `.venv-tf/` e `.uv-python/` — nada foi instalado fora de `htlm/`, exceto o `libomp` do Homebrew e os caches padrão do pip.

Sem a venv completa, os scripts continuam rodando com o Python do sistema — os trechos de boosting e de rede neural apenas aparecem como `NAO_EXECUTAVEL` em vez de falhar.

Os scripts leem os artefatos diretamente: **se o manual mudar, a auditoria acompanha**. Qualquer edição futura deve ser seguida de uma nova execução dos quatro — é o critério de regressão deste material.

---

## 7. Recomendações de manutenção

1. **Rodar os 4 scripts a cada alteração** dos artefatos; tratar qualquer achado como bloqueante antes de republicar.
2. **Manter o ambiente de auditoria** com a pilha completa; se `import xgboost` voltar a falhar, o culpado costuma ser o `DYLD_LIBRARY_PATH` do `libomp`, não o código.
3. **Revisar a nota de versões quando sair a 1.10** (novembro de 2026): `penalty` de `LogisticRegression` está marcado para remoção, e o default de `scoring` em `LogisticRegressionCV` muda na 1.11.
4. **Reexaminar a recomendação sobre Deep Learning tabular** se surgir benchmark posterior a Grinsztajn et al. (2022) com conclusão diferente — a §4.3 da skill é o ponto único a alterar.
5. **Manter a regra de ouro**: o HTML explica, a skill decide; toda divergência entre os dois é defeito, e o script 04 é quem o detecta.


---

## 8. Reauditoria da extensão — TensorFlow, recomendação e reforço (18/09/2026)

### 8.1 O que foi acrescentado
- **Seção 5.1 — TensorFlow na prática**: `tf.data`, `tf.keras` (Keras 3), early stopping, `GradientTape` + `tf.function`, exportação SavedModel e conversão TFLite. TensorFlow continua fora dos cards de modelo: **é framework**, e a taxonomia foi preservada.
- **Seção 16 — Sistemas de recomendação**: 4 cards (colaborativa por vizinhança, fatoração de matrizes, baseada em conteúdo, híbrida), métricas de ranking @k, validação temporal, cold start e riscos de produção, e fatoração neural em TensorFlow.
- **Seção 17 — Aprendizagem por reforço**: 4 cards (bandits, Q-learning, DQN, policy gradient), MDP e equações de Bellman, taxonomia, avaliação off-policy (IPS/SNIPS), quando usar e quando não usar, e as ferramentas. A seção 1.1 deixou de declarar reforço "fora do escopo".
- **Skill**: classes especiais no Passo 2, regras §3.10 (recomendação) e §3.11 (reforço), métricas na §3.8, escadas específicas na §4.4, escalas na §5.1, 6 guardrails novos, 4 linhas de API e 2 snippets.
- **Integração** nas seções 12 (regras, matriz, confrontos, escadas), 13, 14 (2 casos), 15 (2 mitos) e "Como usar".

### 8.2 Ambiente adicional
| Biblioteca | Versão | Observação |
|---|---|---|
| TensorFlow | **2.21.0** | Em **Python 3.12.14**, num ambiente isolado: o TensorFlow **não publica pacote para Python 3.14** (`No matching distribution found`) |
| Keras (via TF) | 3.15.1 | `tf.keras` resolve para o Keras 3 |
| Gymnasium | **1.3.0** | Python 3.14.7 |
| Demais | scikit-learn 1.9.1, PyTorch 2.14.0, XGBoost 3.4.1, LightGBM 4.7.0, CatBoost 1.2.10 | Mesma pilha da §2 |

### 8.3 Achados da reauditoria

| ID | Sev. | Onde | Achado | Evidência | Correção |
|---|---|---|---|---|---|
| **A-12** | MÉDIA | Card `mf` | O exemplo de ALS **generalizava pior que o baseline trivial**: λ = 0,1 com ~10 notas por usuário memoriza o que foi observado | RMSE fora da amostra **2,775** × baseline (prever 0) **2,025** | Dados e λ recalibrados (200 × 150, λ = 1): fora da amostra **0,145** × baseline **2,244**; o próprio trecho agora imprime o baseline e explica a armadilha |
| **A-13** | MÉDIA | Card `dqn` | O agente **não aprendia** e a avaliação usava o último episódio *de treino*, contrariando a seção 17.3 do próprio manual | Retorno impresso: **9** | ε decaindo por passo, atualização suave da rede-alvo, lr 5e-4 e avaliação gulosa em 10 episódios separados: **500**. Na calibração, 3 sementes deram 418 ± 58 |
| **A-14** | MÉDIA | Seção 16.6 (TF) | A fatoração em TensorFlow treinava sobre **ruído puro**: não havia estrutura a aprender, então o exemplo não demonstrava nada | RMSE 0,957 ≈ desvio das próprias notas | Dados com estrutura latente e comparação explícita: RMSE **0,349** × baseline **0,914** |
| **A-15** | BAIXA | Card `policy-gradient` | Avaliação pelo último episódio de treino; nenhuma medida de variância entre execuções | — | Avaliação gulosa com **5 sementes**. Saída: [500, 104, 500, 153, 500], média 351 ± 183 — o trecho agora *demonstra* a regra das ≥ 5 sementes |
| **A-16** | BAIXA | Card `bandits` | Comparação de algoritmos com uma única execução; o UCB1 parecia pior que o acaso | Uma execução: UCB1 com regret 107 × aleatório esperado 83. Com 20 sementes: Thompson **19 ± 22**, UCB1 **68 ± 24**, aleatório **85 ± 19** | Comparação em 20 sementes com a política aleatória como referência. O card agora explica por que o UCB1 explora demais com taxas baixas: o bônus é calibrado para recompensas em [0, 1] |
| **A-17** | BAIXA | Seções 13 e 16.4 e cards | "**Nunca** recomendar o já consumido" é absoluto demais: em recompra (supermercado, consumíveis, música), repetir é o comportamento esperado | Revisão manual das 12 ocorrências novas de linguagem absoluta | Regra reescrita como padrão com exceção explícita, nos dois artefatos |
| **A-18** | BAIXA | Card `mf`, bloco 05 | A previsão incluía vieses (μ + bᵤ + bᵢ + pᵤᵀqᵢ), mas o objetivo publicado os omitia | Leitura das fórmulas | Objetivo reescrito sobre r̂_ui, com regularização dos vieses; o passo ALS identificado como a versão sem vieses, que é a do código |
| **A-19** | BAIXA | Seção 16.1 | "Mais de 99% da matriz é vazia" generalizava demais | MovieLens 1M: 1.000.209 notas / (6.040 × 3.706) ≈ 4,5% de densidade → ~95,5% vazia | Faixa de 95% a mais de 99%, com o exemplo |
| **A-20** | BAIXA | Card `dqn` | "Double DQN **corrige** a superestimação": o método reduz o viés, não o elimina | Revisão técnica | "reduz esse viés" |
| **A-21** | BAIXA | Card `hybrid` | A saída exibia `np.int64(2)` (representação do numpy 2) | Saída do trecho | Conversão para `int` |
| **A-22** | BAIXA | `auditoria/03` | O harness rodava os trechos com o diretório do projeto como `cwd`: o trecho de TensorFlow, que exporta modelos, gravaria arquivos dentro de `htlm/` | Revisão do harness antes de executar | Cada trecho agora roda num diretório temporário |
| **A-23** | — | **Este relatório** | O extrator capturava também o *template* JavaScript que renderiza os cards (`'<pre class="code"><code>' + highlightPy(...)`). Esse texto é uma expressão Python válida e "passava" trivialmente, **inflando todas as contagens anteriores em 1** | O trecho fantasma aparecia rotulado como "auditoria" / "s17-5" | Extração só fora do `<script>`. **A contagem correta da auditoria anterior é 42/42, não 43/43**; as §1, §3 e §4 foram corrigidas |

### 8.4 O que a bateria 06 acrescenta

As baterias 01 a 05 verificam se o código **roda** e se as fórmulas estão **certas**. A reauditoria mostrou que isso não basta: A-12, A-13 e A-14 eram trechos que rodavam sem erro e estavam errados como ensino. O modelo não aprendia, ou generalizava pior que o baseline, e o texto ao redor dizia o contrário. O script `06_saidas_esperadas.py` fixa, para cada trecho novo, **o que a saída precisa demonstrar**:

| Trecho | Critério | Saída verificada |
|---|---|---|
| Colaborativa item-based | não recomenda itens já consumidos | [2 3 5] |
| ALS | RMSE fora da amostra < 25% do baseline | 0,145 × 2,244 |
| Conteúdo | usuário "gamer" recebe o headset gamer em 1º | ✔ |
| Híbrido | usuário sem histórico → popularidade | [0, 1, 2] |
| Bandits | Thompson < UCB1 < aleatório (20 sementes) | 19,1 < 68,1 < 84,9 |
| Q-learning | sucesso ≥ 90% | 100% |
| DQN | retorno de avaliação gulosa ≥ 300 | 500 |
| REINFORCE | média de 5 sementes ≥ 200 | 351,4 |
| Métricas @k | NDCG manual = `sklearn.ndcg_score` | 0,7039 = 0,7039 |
| IPS | erro < 10% do valor real | 0,0465 × 0,045 |
| TensorFlow (pipeline) | PR-AUC de validação ≥ 0,9 | ✔ |
| TensorFlow (GradientTape) | perda final < 0,5 | 0,34 |
| Fatoração em TF | RMSE < 60% do baseline | 0,349 × 0,914 |

### 8.5 Fórmulas novas — 15 conferidas numericamente
Cosseno; escore item-based (fórmula = código); passo fechado da ALS (contra otimização direta); IDF do TF-IDF (`ln((1+n)/(1+df)) + 1`, contra `TfidfVectorizer.idf_`); normalização L2; NDCG@k (200 casos contra `ndcg_score`); AP (200 casos contra `average_precision_score`); Precision@k (200 casos); recursão do retorno descontado; Bellman de avaliação de política (contra `(I − γP_π)⁻¹R_π`); ponto fixo da Bellman ótima; convergência do Q-learning para Q* (MDP determinístico, erro máximo < 0,05); posterior Beta-Bernoulli do Thompson; teorema do gradiente de política (diferenças finitas); não viés do IPS.

**Declaradas como definicionais, sem verificação numérica independente:** a previsão user-based centrada na média, o bônus do UCB1, a perda do DQN, o objetivo recortado do PPO e a definição de regret. São definições de literatura, não identidades que um cálculo possa confirmar.

### 8.6 Limitações que permanecem
1. **Nada foi exercitado em GPU** (esta máquina não tem CUDA).
2. **TensorFlow só foi verificado em Python 3.12**. A afirmação "sem pacote para 3.14" é datada (setembro de 2026) e deve ser revista.
3. **Os limiares da bateria 06 valem para os dados sintéticos dos exemplos**, não para dados reais. Eles provam que o exemplo ensina o que diz, e não que o método funcionará no seu problema.
4. **PPO, SAC, two-tower e TensorFlow Recommenders aparecem só no texto**, sem trecho executável: o manual recomenda bibliotecas testadas (Stable-Baselines3, TFRS) em vez de reimplementá-los.


---

## 9. Incorporação do roadmap de algoritmos (21/09/2026)

### 9.1 Análise de lacunas

| Item do roadmap | Antes | Ação |
|---|---|---|
| Naive Bayes, Logística, KNN, Random Forest, SVM, Decision Tree | Cards completos | — |
| Regressão linear simples, Lasso | Cards completos | Card linear agora distingue simples e múltipla |
| **Regressão multivariada** | Ausente | Nota e trecho na seção 2.1 (vários alvos: Y matricial, `MultiOutputRegressor`, `RegressorChain`) |
| K-Means, DBSCAN, PCA, Isolation Forest | Cards completos | — |
| **ICA** | Ausente | Card novo + contraste com PCA na seção 3.2 |
| **Apriori, FP-Growth** | Ausentes | Seção 3.5 com 2 cards, métricas e riscos |
| **Z-score** | Ausente | Card novo (clássico e robusto por MAD) |
| **Self-Training, Co-Training** | Ausentes (semissupervisionado era uma linha) | Seção 18 com 3 cards (mais Label Spreading), pressupostos e protocolo de validação |
| Q-Learning, otimização de política | Cards completos | — |
| **Model-based: “given the model” / “learn the model”** | Só citado numa tabela | Seção 17.6 com 2 cards: programação dinâmica e Dyna-Q |
| Lição central do post: pressupostos, forças, limitações, requisitos, interpretabilidade, custo e métricas | Espalhados pelos 20 blocos dos cards | **Matriz dos sete critérios** (12.5) para os 43 modelos, gerada dos cards, filtrável; pressupostos também no topo de cada card |

### 9.2 Imprecisões do próprio roadmap (não incorporadas; explicadas na seção 1.5)
1. **PCA e ICA sob “Association”**: são redução de dimensionalidade. O texto do post corrige isso; a imagem, não.
2. **Self-Training → classificação e Co-Training → regressão**: os dois são essencialmente de classificação e ambos têm variantes para regressão.
3. **“Multivariate Regression”** é ambíguo: pode ser *múltipla* (várias features) ou *multivariada* (vários alvos).
4. **Z-score não é algoritmo de aprendizado**: é regra estatística univariada, sujeita a *masking*.
5. Omissão relevante: o roadmap **não menciona boosting**, o estado da arte prático em tabular. O manual o mantém.

### 9.3 Achados desta rodada

| ID | Sev. | Onde | Achado | Evidência | Correção |
|---|---|---|---|---|---|
| **A-24** | MÉDIA | Skill §5.1 × card PCA | A escala da skill dava interpretabilidade **0,80 (Alta)** ao PCA, agrupado com K-Means; o card dizia **Baixa** | Checagem nova de três pontos (matriz × bloco 14 × §5.1) aplicada aos arquivos anteriores | Linha dividida: K-Means 0,80; PCA 0,40 |
| **A-25** | MÉDIA | Skill §5.1 × cards IsolationForest e LOF | Skill: **0,35 (Baixa)** para os três detectores; cards de IsolationForest e LOF: **Média** | Idem | IsolationForest 0,45; LOF 0,45; OneClassSVM 0,20 |
| **A-26** | BAIXA | Card HistGB | Bloco 14 dizia **Média**, enquanto os outros três cards de boosting e a skill (0,40) diziam **Baixa** | Idem | Card alinhado: “Baixa nativamente” |
| **A-27** | BAIXA | Card Self-Training | O bloco 14 não declarava nenhum nível de interpretabilidade | Checagem de três pontos | Nível “Média” declarado e justificado |
| **A-28** | **ALTA** | Frontmatter da skill | Ao acrescentar os sete critérios à `description`, escrevi “critérios: pressupostos…” — **dois-pontos no YAML sem aspas tornam o frontmatter inválido** e impedem a skill de carregar no agente | `yaml.ScannerError: mapping values are not allowed here` | Reescrito; **guarda permanente** no script 04 (a guarda reprova a versão com defeito) |
| **A-29** | BAIXA | Card Label Spreading | O protótipo com grafo de 7 vizinhos ficou **abaixo do baseline em 3 de 5 sementes**. Minha hipótese inicial (grafo desconexo) foi **refutada**: o grafo era conexo em todas | F1 k-NN: 0,83–0,99; RBF (gamma = 20): 0,99–1,0; componentes conexos = 1 em todas as sementes | Card usa RBF e ensina a causa real: arestas-ponte entre as classes vazam rótulos |
| **A-30** | BAIXA | Card Dyna-Q | O protótipo com 30 episódios fixos mostrava sucesso de 0–2 em 10 sementes com ou sem planejamento: a métrica escondia o benefício | Com a métrica certa — episódios reais até resolver, 20 sementes — o Dyna-Q precisa de 48 (mediana) contra 106 do Q-learning | O trecho mede eficiência em amostras, que é o que o Dyna promete |
| **A-31** | INFO | mlxtend 0.25 | `association_rules` tem `num_itemsets` com **default 1**, suspeito à primeira vista | Todas as métricas foram comparadas com `num_itemsets=1` e com o número real de transações: **idênticas**; o parâmetro só entra com `null_values=True` | Documentado com precisão, sem alarme |
| **A-32** | BAIXA | Linguagem absoluta | 15 ocorrências novas de “sempre/nunca/garante” revisadas uma a uma | Todas são regras de método, mitos negados ou fatos demonstrados (ex.: convergência da programação dinâmica para γ < 1, verificada pela igualdade VI = PI) | Nenhuma correção necessária — registrado para rastreabilidade |

### 9.4 Novas verificações permanentes
- **Script 04, seção F**: toda linha da matriz tem os 7 campos preenchidos, todo card tem uma linha, e o nível de interpretabilidade coincide em três lugares — a matriz, o bloco 14 do card e a escala numérica da skill (Alta ≥ 0,75; Média 0,45–0,74; Baixa < 0,45).
- **Script 04, seção G**: o frontmatter da skill precisa ser YAML válido, com `name` e `description`.
- **Script 02**: +7 fórmulas — z-score, 0,6745 = Φ⁻¹(0,75), MAD/0,6745 como estimador de σ, as cinco métricas de associação (em todas as regras de uma base simulada), igualdade Apriori = FP-Growth, **forma fechada do Label Spreading contra o `label_distributions_` do scikit-learn** e VI = PI.
- **Script 06**: +10 saídas — ICA recupera as fontes (0,999 e 0,993) e supera o PCA (0,873 e 0,911); o z robusto acha 6 de 6 anomalias e o clássico, 3; Apriori e FP-Growth idênticos; Self-Training (0,913 → 0,933), Co-Training (0,729 → 0,891) e Label Spreading (0,913 → 0,993) contra o baseline; programação dinâmica com VI = PI e 74,1% de sucesso (o ótimo conhecido do FrozenLake escorregadio); Dyna-Q com 48 × 106 episódios reais; a regressão multivariada recupera os coeficientes.

### 9.5 Observações de reprodutibilidade
- ~~O DQN chegou a 500 numa execução e a 482,9 noutra: o PyTorch em CPU não é bit a bit determinístico entre execuções.~~ **Diagnóstico errado — corrigido em A-33 (§10).** A causa era `action_space.sample()` sem semente.
- Os ambientes de auditoria no diretório temporário da sessão foram apagados entre rodadas (dias sem uso). **Resolvido em 21/09/2026**: os ambientes agora vivem em `htlm/` (`.venv-auditoria`, `.venv-tf`, `.uv-python`) e `auditoria/rodar_tudo.sh` executa as 6 baterias com eles — ver §6.


---

## 10. Ambientes locais e primeira execução com `rodar_tudo.sh` (21/09/2026)

### 10.1 Ambientes criados em `htlm/`
| Pasta | Tamanho | Conteúdo |
|---|---|---|
| `.venv-auditoria/` | 1,3 GB | Python 3.14.7 · scikit-learn 1.9.1 · XGBoost 3.4.1 · LightGBM 4.7.0 · CatBoost 1.2.10 · PyTorch 2.14.0 · Gymnasium 1.3.0 · mlxtend 0.25.0 · PyYAML 6.0.3 |
| `.venv-tf/` | 1,5 GB | Python 3.12.14 · TensorFlow 2.21.0 · Keras 3.15.1 · scikit-learn 1.9.1 |
| `.uv-python/` | 71 MB | Interpretador Python 3.12 usado pelo `.venv-tf` |

Total: **~2,9 GB** — acima dos ~2 GB estimados antes da instalação; o TensorFlow sozinho ocupa 1,5 GB.

### 10.2 Achados

| ID | Sev. | Onde | Achado | Evidência | Correção |
|---|---|---|---|---|---|
| **A-33** | MÉDIA | Cards `dqn` e `q-learning` | **Exploração não reprodutível**: `env.reset(seed=…)` semeia o ambiente, mas **não** `env.action_space.sample()`. O card do DQN mandava “fixar sementes de ambiente, rede e amostragem”, e o próprio código não fixava. **Isso também corrige o diagnóstico que publiquei na §9.5**, que atribuía a variação ao PyTorch | Duas instâncias com `reset(seed=0)` sortearam ações diferentes; com `action_space.seed(0)`, idênticas. A mesma configuração deu 500, 482,9 e **104,5** em três execuções; com a semente, duas execuções deram exatamente o mesmo resultado (328 episódios, retorno 500) | `env.action_space.seed(…)` nos dois cards; armadilha documentada na seção 17.5, na nota de auditoria e na skill (§3.11 e §9); **guarda H** no script 04 (reprova a versão antiga nos dois cards) |
| **A-34** | BAIXA | Card `dqn` | Com o código já reprodutível, medi a robustez: **4 de 5 sementes** chegam a 491–500 e **1 fica em 64**. O card falava em instabilidade sem quantificá-la | Sementes 0 a 4: 500 · 491,3 · 500 · 500 · 63,9 | Bloco 13 do card traz os números; a bateria 06 roda a semente 0, agora determinística |
| **A-35** | MÉDIA | Card `q-learning` | Com a exploração enfim reprodutível, o card **falhou** (sucesso 0,0). Causa: com a tabela Q zerada, `np.argmax` desempata sempre pela ação 0 (esquerda). O agente repete a mesma ação até a exploração, por sorte, achar o objetivo. **O 1,0 publicado antes dependia dessa sorte**, escondida pela falta de semente (A-33) | 10 sementes: argmax puro resolve em **6/10**; desempate aleatório, **10/10** | Desempate aleatório no treino (como já fazia o card de Dyna-Q); armadilha descrita no bloco 12 do card |
| **A-36** | BAIXA | Seções 5.1 e 16.6 (3 trechos de TensorFlow) | Nenhum trecho de TensorFlow fixava semente: pesos iniciais e embaralhamento mudavam a cada execução. Os números passavam nos limiares, mas não eram reprodutíveis | Duas execuções paralelas: perda final 0,310 × 0,331; RMSE 0,352 × 0,349 | `tf.keras.utils.set_random_seed(...)` nos 3 trechos; **guarda I** no script 04 (reprova os 3 trechos antigos) |
| **A-37** | BAIXA | Card `apriori` e skill §10 | A ordem das regras empatadas em lift mudava entre execuções: a exibição de `frozenset` depende do *hash* de strings, que o Python sorteia a cada processo (`PYTHONHASHSEED`) | Duas execuções: “pao → manteiga” numa, “manteiga → pao” noutra, na primeira linha | Regras convertidas em texto ordenado (“pao -> manteiga”) e ordenação por lift e depois pelo texto |

### 10.3 Uma observação sobre o próprio processo
A falha só apareceu porque `rodar_tudo.sh` foi executado num processo novo, com os ambientes novos. A bateria 06 checa a saída, e não só a execução. Uma auditoria que se limitasse a “roda sem erro” continuaria aprovando o card do DQN com um resultado que dependia da sorte.

### 10.4 Reprodutibilidade como verificação permanente

A sequência A-33 → A-35 → A-36 → A-37 mostrou que “passa no limiar” não basta: um resultado que muda a cada execução pode passar hoje e falhar amanhã, como aconteceu com o DQN (500 → 482,9 → 104,5) e com o Q-learning (1,0 → 0,0). Duas proteções permanentes:

- **Guardas estáticas no script 04**: H reprova `action_space.sample()` sem `env.action_space.seed(...)`; I reprova trecho que importe TensorFlow sem `tf.keras.utils.set_random_seed(...)`.
- **`bash auditoria/rodar_tudo.sh --reprodutibilidade`**: roda a bateria 06 duas vezes em paralelo e exige saídas idênticas. A única linha excluída é o endereço de memória que o `model.export()` do TensorFlow imprime.

Com as sementes fixadas, os resultados de referência passam a ser fixos: DQN 328 episódios e retorno 500; Q-learning 100%; REINFORCE [500, 104, 500, 153, 500]; perda do `GradientTape` 0,422; fatoração em TF com RMSE 0,356 × 0,914. Os valores citados em §8 correspondem à execução de 18/09, anterior às sementes.
