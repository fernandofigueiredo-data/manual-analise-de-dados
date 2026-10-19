"""Auditoria 6/6 - "rodar sem erro" nao basta: executa os trechos de recomendacao, reforco e TensorFlow
e confere se a SAIDA demonstra o que o texto afirma (o modelo aprende, supera o baseline, a metrica bate).
Uso: python3 auditoria/06_saidas_esperadas.py
     (TensorFlow: defina AUDITORIA_PY_TF com um Python 3.12/3.13 que tenha tensorflow)"""
import io, re, os, sys, html, subprocess, tempfile, importlib.util
import numpy as np
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = io.open(os.path.join(BASE, "manual_machine_learning.html"), encoding="utf-8").read()
HS = re.sub(r"<script>.*?</script>", "", H, flags=re.S)
PY_TF = os.environ.get("AUDITORIA_PY_TF")
tmp = tempfile.mkdtemp(prefix="auditoria_saidas_")

def card(cid):
    return re.search(r'id:"' + re.escape(cid) + r'".*?cod:`(.*?)`,\s*\n\s*met:', H, re.S).group(1)

def bloco(sec_id, n=1):
    i = HS.index(f'id="{sec_id}"')
    return html.unescape(re.findall(r'<pre class="code"><code>(.*?)</code></pre>', HS[i:], re.S)[n - 1])

def rodar(code):
    tf = "tensorflow" in code
    if tf and not PY_TF and importlib.util.find_spec("tensorflow") is None:
        return None
    path = os.path.join(tmp, f"t{abs(hash(code))}.py"); io.open(path, "w", encoding="utf-8").write(code)
    env = dict(os.environ, TF_CPP_MIN_LOG_LEVEL="3", KERAS_BACKEND="tensorflow" if tf else "torch")
    p = subprocess.run([PY_TF if (tf and PY_TF) else sys.executable, path], capture_output=True, text=True,
                       cwd=tmp, env=env, timeout=900)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip().split("\n")[-1][:200])
    return p.stdout

num = lambda padrao, txt: float(re.search(padrao, txt).group(1))
casos = [
 ("Item-based nao recomenda o ja consumido (itens 0, 1, 4)", lambda: card("cf-knn"),
  lambda o: set(map(int, re.findall(r"\d+", o.strip().split("\n")[-1]))).isdisjoint({0, 1, 4})),
 ("ALS generaliza: RMSE fora da amostra << baseline", lambda: card("mf"),
  lambda o: num(r"nao observado: ([\d.]+)", o) < 0.25 * num(r"baseline \(prever 0\): ([\d.]+)", o)),
 ("Conteudo: usuario 'gamer' recebe o headset gamer em 1o", lambda: card("content-based"),
  lambda o: re.search(r"\['headset gamer", o) is not None),
 ("Hibrido: usuario sem historico cai na popularidade", lambda: card("hybrid"),
  lambda o: o.strip().endswith("[0, 1, 2]")),
 ("Bandits: Thompson < UCB1 < aleatorio (media de 20 sementes)", lambda: card("bandits"),
  lambda o: num(r"thompson\s+regret medio\s+([\d.]+)", o) < num(r"ucb1\s+regret medio\s+([\d.]+)", o)
            < num(r"aleatorio\s+regret medio\s+([\d.]+)", o)),
 ("Q-learning resolve o FrozenLake deterministico (>= 90%)", lambda: card("q-learning"),
  lambda o: num(r"taxa de sucesso: ([\d.]+)", o) >= 0.9),
 ("DQN aprende: retorno medio de avaliacao gulosa >= 300", lambda: card("dqn"),
  lambda o: num(r"retorno medio de avaliacao: ([\d.]+)", o) >= 300),
 ("REINFORCE aprende: media de 5 sementes >= 200", lambda: card("policy-gradient"),
  lambda o: num(r"\| media: ([\d.]+)", o) >= 200),
 ("Metricas @k: NDCG manual == sklearn.ndcg_score", lambda: bloco("s16-3"),
  lambda o: len(set(o.split()[-2:])) == 1),
 ("IPS estima o valor real com erro < 10%", lambda: bloco("s17-3"),
  lambda o: abs(num(r"IPS: ([\d.]+)", o) - num(r"valor real: ([\d.]+)", o)) < 0.1 * num(r"valor real: ([\d.]+)", o)),
 ("TensorFlow: PR-AUC de validacao >= 0.9", lambda: bloco("s5-tf", 1),
  lambda o: num(r"melhor PR-AUC de validacao: ([\d.]+)", o) >= 0.9),
 ("TensorFlow GradientTape: a perda cai (< 0.5)", lambda: bloco("s5-tf", 2),
  lambda o: num(r"perda final: ([\d.]+)", o) < 0.5),
 ("Fatoracao em TF supera o baseline de media global (< 60%)", lambda: bloco("s16-6"),
  lambda o: num(r"RMSE teste: ([\d.]+)", o) < 0.6 * num(r"baseline \(media global\): ([\d.]+)", o)),
 ("Regressao multivariada recupera os coeficientes (erro < 0.05)", lambda: bloco("s2-1"),
  lambda o: num(r"erro maximo vs verdadeiro: ([\d.]+)", o) < 0.05 and "(2, 4)" in o and "(3, 2)" in o),
 ("ICA separa as fontes (corr > 0.95) e supera o PCA", lambda: card("ica"),
  lambda o: min(map(float, re.search(r"ICA recupera as fontes: \[([^\]]+)\]", o).group(1).split())) > 0.95
            and np.mean(list(map(float, re.search(r"ICA recupera as fontes: \[([^\]]+)\]", o).group(1).split())))
              > np.mean(list(map(float, re.search(r"PCA: \[([^\]]+)\]", o).group(1).split())))),
 ("Z robusto acha as 6 anomalias; o classico sofre masking", lambda: card("zscore"),
  lambda o: num(r"z robusto \(\|z\| > 3.5\): (\d+)", o) == 6 and num(r"z classico \(\|z\| > 3\): (\d+)", o) < 6),
 ("Apriori: a regra de maior lift tem lift > 1", lambda: card("apriori"),
  lambda o: float(o.strip().split("\n")[1].split()[-1]) > 1),
 ("FP-Growth encontra os mesmos itemsets do Apriori", lambda: card("fpgrowth"),
  lambda o: "identicos aos do Apriori: True" in o),
 ("Self-Training nao piora o baseline so-rotulados", lambda: card("self-training"),
  lambda o: num(r"self-training: ([\d.]+)", o) >= num(r"so com os 20 rotulados: ([\d.]+)", o)),
 ("Co-Training supera o baseline em >= 0,10 de F1", lambda: card("co-training"),
  lambda o: num(r"co-training: ([\d.]+)", o) >= num(r"so com os 10 rotulados: ([\d.]+)", o) + 0.10),
 ("Label Spreading (RBF) supera o baseline so-rotulados", lambda: card("label-spreading"),
  lambda o: num(r"label spreading: ([\d.]+)", o) > num(r"so com os 20 rotulados: ([\d.]+)", o)),
 ("Programacao dinamica: VI = PI e sucesso ~ otimo (> 0.7)", lambda: card("dp"),
  lambda o: "mesmo valor otimo: True" in o and num(r"taxa de sucesso: ([\d.]+)", o) > 0.7),
 ("Dyna-Q precisa de menos episodios reais que o Q-learning", lambda: card("dyna-q"),
  lambda o: num(r"planejamento = 50: mediana de (\d+)", o) < num(r"planejamento =  0: mediana de (\d+)", o)),
]
ok = fal = skip = 0
for nome, fonte, criterio in casos:
    try:
        saida = rodar(fonte())
        if saida is None:
            print(f"SKIP  {nome}  (tensorflow indisponivel)"); skip += 1; continue
        passou = bool(criterio(saida))
        ultima = saida.strip().split("\n")[-1][:90]
        print(f"{'OK   ' if passou else 'FALHA'} {nome:62s} | {ultima}")
        ok += passou; fal += not passou
    except Exception as e:
        print(f"ERRO  {nome}: {e}"); fal += 1
print(f"\n{ok}/{ok+fal} saidas demonstram o que o texto afirma | falhas: {fal} | skip: {skip}")
