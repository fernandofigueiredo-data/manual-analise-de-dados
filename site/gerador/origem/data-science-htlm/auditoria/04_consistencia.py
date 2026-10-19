"""Auditoria 4/4 - checagens estruturais: taxonomia, metrica x problema, pre-processamento x familia,
consistencia HTML<->MD e varredura de linguagem absoluta.
Uso: python3 auditoria/04_consistencia.py"""
import io, re, os, html, unicodedata
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = io.open(os.path.join(BASE, "manual_machine_learning.html"), encoding="utf-8").read()
M = io.open(os.path.join(BASE, "skill_decisao_ml.md"), encoding="utf-8").read()
na = lambda s: "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()

js = re.search(r"<script>(.*)</script>", H, re.S).group(1)
cards = []
for parte in re.split(r'\n\s*id:"', js)[1:]:
    cid = parte[:parte.index('"')]
    corpo = parte[:parte.find("\n},")] if "\n}," in parte else parte
    tags = re.search(r"tags:\[([^\]]*)\]", corpo).group(1)
    campos = dict(re.findall(r'\s(q|cat|prob|como|mat|quando|nao|dados|prep|hp|vant|lim|over|interp|custo|met|conc|pref|emp|resumo|nome):\s*"((?:[^"\\]|\\.)*)"', corpo))
    cards.append({"id": cid, "tags": [t.strip().strip('"') for t in tags.split(",")], **campos})

falhas = []
# A. taxonomia
PROIBIDOS = {"cross entropy","log loss","gradient descent","adam","rmsprop","sgd","tensorflow","pytorch","keras","scikit-learn","mse","mae","accuracy","f1"}
for c in cards:
    if na(c.get("nome", "")) in PROIBIDOS:
        falhas.append(("A-taxonomia", c["id"], "card com nome de perda/otimizador/framework/metrica"))
    cat = na(c.get("cat", ""))
    if "sup" in c["tags"] and "supervisionado" not in cat:
        falhas.append(("A-taxonomia", c["id"], "bloco 02 nao declara Supervisionado"))
    if "nsup" in c["tags"] and "nao supervisionado" not in cat:
        falhas.append(("A-taxonomia", c["id"], "bloco 02 nao declara Nao supervisionado"))
    if "rec" in c["tags"] and "sistema de recomendacao" not in cat:
        falhas.append(("A-taxonomia", c["id"], "bloco 02 nao declara Sistema de recomendacao"))
    if "rl" in c["tags"] and "aprendizagem por reforco" not in cat:
        falhas.append(("A-taxonomia", c["id"], "bloco 02 nao declara Aprendizagem por reforco"))
    if "asc" in c["tags"] and "regras de associacao" not in cat:
        falhas.append(("A-taxonomia", c["id"], "bloco 02 nao declara Regras de associacao"))
    if "semi" in c["tags"] and "semissupervisionado" not in cat:
        falhas.append(("A-taxonomia", c["id"], "bloco 02 nao declara Semissupervisionado"))
# B. metrica x tipo de problema
REGRAS = {"reg": ["mae","rmse","mse","r2","r²","mape"], "clf": ["f1","roc-auc","pr-auc","log loss","precision","recall"], "clu": ["silhouette","davies","calinski","bic"],
          "rec": ["ndcg","map@k","recall@k","precision@k","hit rate"], "rl": ["retorno","regret","valor da politica"],
          "asc": ["suporte","confianca","lift"]}
for c in cards:
    met = na(c.get("met", ""))
    for tag, termos in REGRAS.items():
        if tag in c["tags"] and not any(t in met for t in termos):
            falhas.append(("B-metrica", c["id"], f"tag {tag} sem metrica compativel no bloco 17"))
    if c["id"] in {"isolation-forest","lof","ocsvm"} and not any(t in met for t in ["pr-auc","precision@k"]):
        falhas.append(("B-metrica", c["id"], "detector de anomalia sem PR-AUC/precision@k"))
# C. pre-processamento x familia (espelha a tabela 3.9 da skill)
EXIGE = {"ridge","lasso","elasticnet","logistic","svm","knn","kmeans","gmm","pca","kde","lof","ocsvm","mlp"}
NAO_EXIGE = {"decision-tree","random-forest","extra-trees","histgb","xgboost","lightgbm","catboost","isolation-forest"}
for c in cards:
    prep = na(c.get("prep", ""))
    if c["id"] in EXIGE and "padroniza" not in prep:
        falhas.append(("C-preproc", c["id"], "familia exige escala e o bloco 09 nao diz"))
    if c["id"] in NAO_EXIGE and not any(t in prep for t in ["nao exige","sem escala","minimo","praticamente nenhum"]):
        falhas.append(("C-preproc", c["id"], "familia nao exige escala e o bloco 09 nao diz"))
# D. consistencia HTML <-> MD
for termo in ["1.9.1","3.4.1","Keras 3","PyTorch 2.x","multi_class","root_mean_squared_error","sparse_output",
              "n_alphas","from_dtype","sparse_interface","FrozenEstimator","TimeSeriesSplit","GroupKFold","PR-AUC",
              "NDCG","cold start","Popularidade","Thompson","Q-learning","DQN","PPO","IPS","SNIPS","Gymnasium",
              "terminated","truncated","model.export","KERAS_BACKEND","Stable-Baselines3",
              "Apriori","FP-Growth","lift","ICA","MAD","Self-Training","Co-Training","Label Spreading",
              "Dyna-Q","Programação dinâmica","multivariada","MultiOutputRegressor","num_itemsets","holdout rotulado"]:
    if (termo in H) != (termo in M):
        falhas.append(("D-consistencia", termo, f"HTML={termo in H} MD={termo in M}"))
for nivel, termos in {"1": ["Dummy","Logistic"], "2": ["Decision Tree","Random Forest"],
                      "3": ["XGBoost","LightGBM","CatBoost"], "4": ["CNN","Transformer"]}.items():
    for t in termos:
        if t not in H or t not in M:
            falhas.append(("D-hierarquia", f"nivel {nivel}: {t}", "ausente em um dos arquivos"))

# F. matriz dos 7 criterios: completa e coerente com o card e com a escala 5.1 da skill
mm = re.search(r"const MATRIZ = \{(.*?)\n\};", js, re.S)
if not mm:
    falhas.append(("F-matriz", "-", "objeto MATRIZ ausente"))
else:
    entradas = dict(re.findall(r'\n "([^"]+)":\{(.*?)\},?(?=\n|$)', mm.group(1)))
    campos7 = ["pres", "forte", "fraco", "dados", "i", "c", "met"]
    for c in cards:
        e = entradas.get(c["id"])
        if e is None:
            falhas.append(("F-matriz", c["id"], "modelo sem linha na matriz")); continue
        faltam = [k for k in campos7 if not re.search(r"\b" + k + r':"[^"]+"', e)]
        if faltam: falhas.append(("F-matriz", c["id"], "campos vazios: " + ",".join(faltam)))
    for mid in entradas:
        if mid not in {c["id"] for c in cards}: falhas.append(("F-matriz", mid, "linha da matriz sem card"))
    # escala 5.1 da skill -> nivel qualitativo
    escala = {}
    for lin in re.findall(r"^\| ([^|]+?) \| (\d,\d\d)[^|]*\| [\d,]+ \|$", M, re.M):
        escala[lin[0].strip()] = float(lin[1].replace(",", "."))
    nivel = lambda v: "Alta" if v >= 0.75 else ("Media" if v >= 0.45 else "Baixa")
    MAPA = {"linear-regression":"Linear / Logistic / Ridge / Lasso / Elastic Net","ridge":"Linear / Logistic / Ridge / Lasso / Elastic Net",
      "lasso":"Linear / Logistic / Ridge / Lasso / Elastic Net","elasticnet":"Linear / Logistic / Ridge / Lasso / Elastic Net",
      "logistic":"Linear / Logistic / Ridge / Lasso / Elastic Net","polynomial":"Regressão polinomial","naive-bayes":"Naive Bayes",
      "decision-tree":"Decision Tree (profundidade ≤ 4)","random-forest":"Random Forest / Extra Trees","extra-trees":"Random Forest / Extra Trees",
      "histgb":"HistGB / XGBoost / LightGBM / CatBoost","xgboost":"HistGB / XGBoost / LightGBM / CatBoost","lightgbm":"HistGB / XGBoost / LightGBM / CatBoost",
      "catboost":"HistGB / XGBoost / LightGBM / CatBoost","svm":"SVM-RBF","knn":"KNN","kmeans":"K-Means","pca":"PCA","gmm":"GMM / DBSCAN","dbscan":"GMM / DBSCAN",
      "hierarchical":"Clustering hierárquico","isolation-forest":"IsolationForest","lof":"LOF","ocsvm":"OneClassSVM","kde":"KDE","mlp":"MLP",
      "cf-knn":"Colaborativa por vizinhança","content-based":"Filtragem baseada em conteúdo","mf":"Fatoração de matrizes","hybrid":"Recomendação híbrida",
      "bandits":"Bandits","q-learning":"Q-learning tabular","dqn":"DQN / PPO","policy-gradient":"DQN / PPO","ica":"ICA","zscore":"Z-score / Z robusto (MAD)",
      "apriori":"Apriori / FP-Growth","fpgrowth":"Apriori / FP-Growth","self-training":"Self-Training","co-training":"Co-Training",
      "label-spreading":"Label Spreading / Propagation","dp":"Programação dinâmica","dyna-q":"Dyna-Q"}
    for c in cards:
        e = entradas.get(c["id"], "")
        mi = re.search(r'\bi:"([^"]+)"', e)
        if not mi: continue
        i_matriz = na(mi.group(1)).capitalize()
        rot = MAPA.get(c["id"])
        if rot is None or rot not in escala:
            falhas.append(("F-interp", c["id"], f"sem linha correspondente na escala 5.1 da skill ({rot})")); continue
        i_skill = nivel(escala[rot])
        m14 = re.search(r"\b(maxima|alta|media|baixa)\b", na(re.sub(r"<[^>]+>", "", c.get("interp", ""))))
        i_card = {"maxima": "Alta"}.get(m14.group(1), m14.group(1).capitalize()) if m14 else "?"
        if not (i_matriz == i_skill == i_card):
            falhas.append(("F-interp", c["id"], f"matriz={i_matriz} | card(bloco 14)={i_card} | skill 5.1={i_skill} ({escala[rot]:.2f})"))

# G. frontmatter da skill precisa ser YAML valido (senao a skill nao carrega no agente)
try:
    import yaml
    fm = yaml.safe_load(M.split("---", 2)[1])
    if not (isinstance(fm, dict) and fm.get("name") and fm.get("description")):
        falhas.append(("G-frontmatter", "skill", "name/description ausentes"))
except ImportError:
    pass
except Exception as e:
    falhas.append(("G-frontmatter", "skill", "YAML invalido: " + str(e).split(chr(10))[0]))
# H. reprodutibilidade: action_space.sample() sem action_space.seed() gera exploracao nao reprodutivel
for cid, cod in re.findall(r'\n\s*id:"([^"]+)", grupo:.*?cod:`(.*?)`,', js, re.S):
    if "action_space.sample()" in cod and "action_space.seed(" not in cod:
        falhas.append(("H-semente", cid, "usa action_space.sample() sem env.action_space.seed(...)"))
# I. reprodutibilidade em TensorFlow: todo trecho que importa tensorflow precisa fixar a semente
import html as _html
_estaticos = re.findall(r'<pre class="code"(?: data-lang="\w+")?><code(?: data-lang="\w+")?>(.*?)</code></pre>',
                        re.sub(r"<script>.*?</script>", "", H, flags=re.S), re.S)
_trechos = [_html.unescape(x) for x in _estaticos] + [c for _, c in re.findall(r'\n\s*id:"([^"]+)", grupo:.*?cod:`(.*?)`,', js, re.S)]
_trechos += re.findall(r"```python\n(.*?)```", M, re.S)
for i_, cod in enumerate(_trechos):
    if re.search(r"^\s*import tensorflow", cod, re.M) and "set_random_seed" not in cod:
        falhas.append(("I-semente-tf", f"trecho {i_}", "importa tensorflow sem tf.keras.utils.set_random_seed(...)"))
print("cards auditados:", len(cards))
print("\n=== ACHADOS ESTRUTURAIS ===")
for f in falhas: print(" -", " | ".join(f))
if not falhas: print("nenhum")
# E. linguagem absoluta (exige revisao humana de cada ocorrencia)
def texto(h):
    h = re.sub(r"<script>.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<style>.*?</style>", "", h, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", h))
corpo = texto(H) + "\n" + "\n".join(str(v) for c in cards for v in c.values()) + "\n" + M
hits = re.findall(r"\b(sempre|nunca|jamais|garant\w*|melhor modelo|superior a todos|infal\w*)\b", corpo, re.I)
print(f"\n=== LINGUAGEM ABSOLUTA: {len(hits)} ocorrencias (revisar manualmente; regras de metodo e mitos citados para negacao sao legitimos) ===")
from collections import Counter
print(dict(Counter(h.lower() for h in hits)))
