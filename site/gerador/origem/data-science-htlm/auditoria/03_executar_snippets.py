"""Auditoria 3/4 - extrai TODOS os trechos de codigo dos dois artefatos e executa cada um
num processo isolado, sobre dados sinteticos. Trechos que dependem de bibliotecas ausentes
sao marcados como NAO_EXECUTAVEL (verificacao apenas estatica).
Uso: python3 auditoria/03_executar_snippets.py"""
import io, re, sys, json, html, subprocess, tempfile, os, importlib.util
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = io.open(os.path.join(BASE, "manual_machine_learning.html"), encoding="utf-8").read()
MD = io.open(os.path.join(BASE, "skill_decisao_ml.md"), encoding="utf-8").read()

snips = []
for m in re.finditer(r"cod:`(.*?)`,\s*\n\s*met:", HTML, re.S):
    nome = re.findall(r'nome:"([^"]+)"', HTML[:m.start()])[-1]
    snips.append({"origem": "HTML/card", "ref": nome, "code": m.group(1)})
# blocos estaticos: procurar FORA do <script> (o template JS que renderiza os cards tambem contem "<pre class=code>")
HTML_SEM_JS = re.sub(r"<script>.*?</script>", "", HTML, flags=re.S)
for m in re.finditer(r'<pre class="code"(?: data-lang="(\w+)")?><code(?: data-lang="\w+")?>(.*?)</code></pre>', HTML_SEM_JS, re.S):
    if m.group(1) == "shell":
        continue
    sec = re.findall(r'id="(s\d+[^"]*|comousar[^"]*|auditoria)"', HTML_SEM_JS[:m.start()])
    snips.append({"origem": "HTML/secao", "ref": sec[-1] if sec else "?", "code": html.unescape(m.group(2))})
for m in re.finditer(r"```python\n(.*?)```", MD, re.S):
    sec = re.findall(r"\n## ([^\n]+)", MD[:m.start()])
    snips.append({"origem": "MD", "ref": sec[-1][:40] if sec else "?", "code": m.group(1)})

PRE = """
import numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
rng = np.random.default_rng(0)
Xa, ya = make_classification(n_samples=400, n_features=8, n_informative=5, weights=[.85,.15], random_state=0)
X = pd.DataFrame(Xa, columns=[f"f{i}" for i in range(8)]); y = pd.Series(ya); df = X.copy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=.3, random_state=0, stratify=y_train)
X_valid, y_valid = X_val, y_val
X_scaled = StandardScaler().fit_transform(X); X_normal = X_scaled[:200]
n_features = X.shape[1]; cat_idx = []
textos_train = ["produto bom","pessimo atendimento","recomendo","nao gostei"]*25
y_texto = pd.Series([1,0,1,0]*25)
from sklearn.cluster import KMeans; km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X_scaled)
from sklearn.linear_model import LogisticRegression; clf = LogisticRegression(max_iter=1000).fit(X_train, y_train)
modelo_treinado = modelo_ja_treinado = clf
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline as _P; pipeline = _P([("clf", GradientBoostingClassifier(random_state=0))])
periodos_ate_o_rotulo_amadurecer = 3
cand = pd.DataFrame({"score_medio":[.1,.2],"desvio_folds":[.01,.02],"tempo_s":[1,2],
                     "interpretabilidade":[1,.4],"adequacao":[.6,1.],"manutencao":[.9,.6],"negocio":[.5,1.]})
"""
PRE_MISTO = """
num_cols = num = ["idade","renda","tempo_casa"]; cat_cols = cat = ["uf","canal","produto"]
_n = 400
X = pd.DataFrame({"idade": rng.integers(18,80,_n).astype(float), "renda": rng.normal(5000,1500,_n),
                  "tempo_casa": rng.integers(0,240,_n).astype(float), "uf": rng.choice(["SP","RJ","MG","BA"],_n),
                  "canal": rng.choice(["app","web","loja"],_n), "produto": rng.choice(["A","B","C"],_n)})
X.loc[X.sample(40, random_state=1).index, "renda"] = np.nan
y = pd.Series((X["renda"].fillna(0) > 5200).astype(int))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=.3, random_state=0, stratify=y_train)
cat_idx = [X.columns.get_loc(c) for c in cat_cols]
"""
PRE_1D = "\nX = np.linspace(0,5,200); y = 2.3*X + 1.1 + rng.normal(0,.2,200)\n"
PRE_TORCH = """
import os; os.environ.setdefault("KERAS_BACKEND", "torch")
import torch
from torch.utils.data import TensorDataset, DataLoader
_xt = torch.tensor(X_train.to_numpy(), dtype=torch.float32)
_yt = torch.tensor(y_train.to_numpy(), dtype=torch.float32).unsqueeze(1)
train_loader = DataLoader(TensorDataset(_xt, _yt), batch_size=32, shuffle=True)
X_train, y_train = X_train.to_numpy(), y_train.to_numpy()
"""
AUSENTES = ("xgboost", "lightgbm", "catboost", "torch", "keras", "tensorflow", "gymnasium", "mlxtend", "imblearn", "shap")
# TensorFlow ainda nao tem pacote para Python 3.14: aponte AUDITORIA_PY_TF para um Python 3.12/3.13 com TF
PY_TF = os.environ.get("AUDITORIA_PY_TF")

res, tmp = [], tempfile.mkdtemp(prefix="auditoria_ml_")
for i, s in enumerate(snips):
    libs = sorted({l for l in AUSENTES if re.search(r"\b"+l+r"\b", s["code"])})
    usa_tf = "tensorflow" in libs
    interp = PY_TF if (usa_tf and PY_TF) else sys.executable
    faltando = [] if (usa_tf and PY_TF) else [l for l in libs if importlib.util.find_spec(l) is None]
    if faltando:
        res.append({**s, "status": "NAO_EXECUTAVEL", "detalhe": "biblioteca ausente: " + ",".join(faltando)})
    else:
        usa_misto = "ColumnTransformer" in s["code"] or '"uf"' in s["code"]
        pre = PRE + (PRE_1D if "dw = -2" in s["code"] else PRE_MISTO if usa_misto else "")
        if "textos_train" in s["code"]:
            pre += "\ny_train = y_texto\n"
        if "train_loader" in s["code"]:
            pre += PRE_TORCH
        path = os.path.join(tmp, f"s{i}.py")
        io.open(path, "w", encoding="utf-8").write(pre + "\n# ---- trecho auditado ----\n" + s["code"] + "\n")
        env = dict(os.environ, TF_CPP_MIN_LOG_LEVEL="3")
        if usa_tf:
            env["KERAS_BACKEND"] = "tensorflow"
        # cwd isolado: trechos que salvam arquivos (modelos exportados) nao sujam o projeto
        p = subprocess.run([interp, path], capture_output=True, text=True, timeout=900, cwd=tmp, env=env)
        erro = [l for l in p.stderr.strip().split("\n") if l.strip()]
        res.append({**s, "status": "OK" if p.returncode == 0 else "ERRO",
                    "detalhe": "" if p.returncode == 0 else erro[-1][:220]})
    print(f"[{i:02d}] {res[-1]['status']:14s} {s['origem']:11s} {s['ref'][:32]:32s} {res[-1]['detalhe'][:80]}", flush=True)

print("\nRESUMO:", dict(Counter(r["status"] for r in res)))
print("scripts temporarios em", tmp)
