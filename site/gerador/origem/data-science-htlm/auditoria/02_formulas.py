"""Auditoria 2/4 - confere numericamente cada formula publicada no manual."""
import numpy as np, warnings; warnings.filterwarnings("ignore")
from scipy.special import expit, softmax
from scipy.stats import entropy as sp_entropy, multivariate_normal as mvn
from scipy.optimize import minimize
from sklearn import metrics
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KernelDensity

rng = np.random.default_rng(0); res = []
t = lambda n, c, d="": res.append((c, n, d))

p3 = np.array([.3, .5, .2])
t("Gini = 1 - sum(p^2)", np.isclose(1 - np.sum(p3**2), 0.62))
t("Entropia = -sum(p*log2 p)", np.isclose(-np.sum(p3*np.log2(p3)), sp_entropy(p3, base=2)))
z = rng.normal(size=200)
t("sigmoide = 1/(1+e^-z)", np.allclose(1/(1+np.exp(-z)), expit(z)))
Z = rng.normal(size=(50, 4))
t("softmax(zk) = e^zk / sum e^zj", np.allclose(np.exp(Z)/np.exp(Z).sum(1, keepdims=True), softmax(Z, axis=1)))
yb, pb = rng.integers(0, 2, 300), np.clip(rng.random(300), 1e-6, 1-1e-6)
t("LogLoss = -[y log p + (1-y) log(1-p)]", np.isclose(-np.mean(yb*np.log(pb)+(1-yb)*np.log(1-pb)), metrics.log_loss(yb, pb)))
K = 4; ym = rng.integers(0, K, 300); P = softmax(rng.normal(size=(300, K)), axis=1)
t("CategoricalCE = -sum yk log pk", np.isclose(-np.mean(np.log(P[np.arange(300), ym])), metrics.log_loss(ym, P, labels=range(K))))
yt = rng.normal(size=300); yp = yt + rng.normal(0, .4, 300)
t("MSE / MAE / RMSE", np.isclose(np.mean((yt-yp)**2), metrics.mean_squared_error(yt, yp)) and
                      np.isclose(np.mean(np.abs(yt-yp)), metrics.mean_absolute_error(yt, yp)) and
                      np.isclose(np.sqrt(np.mean((yt-yp)**2)), metrics.root_mean_squared_error(yt, yp)))
t("R2 = 1 - SSres/SStot", np.isclose(1-np.sum((yt-yp)**2)/np.sum((yt-yt.mean())**2), metrics.r2_score(yt, yp)))
yv, yh = rng.integers(0, 2, 400), rng.integers(0, 2, 400)
tn, fp, fn, tp = metrics.confusion_matrix(yv, yh).ravel()
Pr, Rc = tp/(tp+fp), tp/(tp+fn)
t("Precision/Recall/F1 a partir da matriz de confusao",
  np.isclose(Pr, metrics.precision_score(yv, yh)) and np.isclose(Rc, metrics.recall_score(yv, yh))
  and np.isclose(2*Pr*Rc/(Pr+Rc), metrics.f1_score(yv, yh)))
X1 = np.linspace(0, 5, 200); y1 = 2.3*X1 + 1.1 + rng.normal(0, .2, 200); w, b, h = .7, -.2, 1e-6
J = lambda w, b: np.mean((y1-(w*X1+b))**2)
t("gradiente do MSE: dJ/dw = -2*mean(X*(y-yhat))",
  np.isclose(-2*np.mean(X1*(y1-(w*X1+b))), (J(w+h, b)-J(w-h, b))/(2*h), rtol=1e-4))
n, p = 200, 5
X = rng.normal(size=(n, p)); y = X @ np.array([2., -1., .5, 0, 0]) + rng.normal(0, .3, n)
Xc, yc = X-X.mean(0), y-y.mean()
r = Ridge(alpha=2.0, fit_intercept=False).fit(Xc, yc)
t("Ridge minimiza ||y-Xw||^2 + alpha*||w||^2 (sem 1/n)",
  np.allclose(r.coef_, minimize(lambda w: np.sum((yc-Xc@w)**2)+2.0*np.sum(w**2), np.zeros(p)).x, atol=1e-3))
l = Lasso(alpha=.1, fit_intercept=False).fit(Xc, yc)
o = minimize(lambda w: np.sum((yc-Xc@w)**2)/(2*n)+.1*np.sum(np.abs(w)), np.zeros(p), method="Powell",
             options={"xtol": 1e-10, "ftol": 1e-12}).x
t("Lasso do sklearn normaliza o erro por 1/(2n)", np.allclose(l.coef_, o, atol=1e-3))
en = ElasticNet(alpha=.1, l1_ratio=.5, fit_intercept=False).fit(Xc, yc)
o = minimize(lambda w: np.sum((yc-Xc@w)**2)/(2*n)+.05*np.sum(np.abs(w))+.025*np.sum(w**2), np.zeros(p),
             method="Powell", options={"xtol": 1e-10, "ftol": 1e-12}).x
t("ElasticNet: rho*L1 + (1-rho)/2*L2 com 1/(2n)", np.allclose(en.coef_, o, atol=1e-3))
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
t("Inercia = sum ||xi - mu_c(i)||^2", np.isclose(np.sum((X-km.cluster_centers_[km.labels_])**2), km.inertia_))
pca = PCA().fit(X); lam = np.sort(np.linalg.eigvalsh(np.cov(X, rowvar=False)))[::-1]
t("PCA: variancia explicada = lambda_j / sum(lambda)", np.allclose(pca.explained_variance_ratio_, lam/lam.sum(), atol=1e-8))
gm = GaussianMixture(n_components=2, covariance_type="full", random_state=0).fit(X)
dens = np.sum([gm.weights_[k]*mvn(gm.means_[k], gm.covariances_[k]).pdf(X) for k in range(2)], axis=0)
t("GMM: p(x) = sum pi_k N(x|mu_k,Sigma_k)", np.allclose(np.log(dens), gm.score_samples(X), atol=1e-8))
Xb = rng.normal(size=(500, 1)); yb2 = (rng.random(500) < expit(1.4*Xb[:, 0]-.3)).astype(int)
lr = LogisticRegression().fit(Xb, yb2)
p0, p1 = lr.predict_proba([[0.]])[0, 1], lr.predict_proba([[1.]])[0, 1]
t("exp(coef) = razao de chances", np.isclose((p1/(1-p1))/(p0/(1-p0)), np.exp(lr.coef_[0, 0])))
Xm = rng.normal(size=(300, 4)); ymc = rng.integers(0, 3, 300)
lm = LogisticRegression(max_iter=1000).fit(Xm, ymc)
t("K>=3 usa softmax (multinomial, sem multi_class)",
  np.allclose(lm.predict_proba(Xm), softmax(lm.decision_function(Xm), axis=1), atol=1e-8))
Xn = rng.integers(0, 5, (200, 6)); yn = rng.integers(0, 2, 200)
nb = MultinomialNB(alpha=1.0).fit(Xn, yn)
t("NB: log P(y|x) ~ log P(y) + sum xj log P(xj|y)",
  np.allclose(nb.class_log_prior_ + Xn @ nb.feature_log_prob_.T, nb._joint_log_likelihood(Xn), atol=1e-10))
Xk = rng.normal(size=(300, 1)); hh = .4
kde = KernelDensity(kernel="gaussian", bandwidth=hh).fit(Xk)
g = np.linspace(-2, 2, 25)
man = np.array([np.mean(np.exp(-.5*((v-Xk[:, 0])/hh)**2)/(hh*np.sqrt(2*np.pi))) for v in g])
t("KDE: p(x) = 1/(n h) sum K((x-xi)/h)", np.allclose(np.log(man), kde.score_samples(g.reshape(-1, 1)), atol=1e-8))
B, rho = 400, .3
L = np.linalg.cholesky(rho*np.ones((B, B))+(1-rho)*np.eye(B))
t("RF: Var(media) = rho*s2 + (1-rho)*s2/B", np.isclose((L@rng.normal(size=(B, 4000))).mean(0).var(), rho+(1-rho)/B, rtol=.08))

# ================= Extensao: sistemas de recomendacao =================
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import ndcg_score, average_precision_score, precision_score

Rm = (rng.random((30, 12)) < .3).astype(float)
man = (Rm.T @ Rm) / np.outer(np.linalg.norm(Rm, axis=0), np.linalg.norm(Rm, axis=0)).clip(1e-12)
t("cosseno: sim(i,j) = ri.rj / (|ri||rj|)", np.allclose(man, cosine_similarity(Rm.T)))
S = cosine_similarity(Rm.T); np.fill_diagonal(S, 0)
u = 0
t("item-based: score(u,i) = sum_{j in Iu} sim(i,j)*r_uj (formula = codigo do card)",
  np.allclose(Rm[u] @ S, [sum(S[i, j]*Rm[u, j] for j in range(12)) for i in range(12)]))

k, lam = 4, .3
Qm = rng.normal(size=(15, k)); obs = rng.random(15) < .6; ru = rng.normal(size=15)
Qu = Qm[obs]; pu = np.linalg.solve(Qu.T @ Qu + lam*np.eye(k), Qu.T @ ru[obs])
o = minimize(lambda w: np.sum((ru[obs]-Qu@w)**2) + lam*np.sum(w**2), np.zeros(k)).x
t("ALS: p_u = (Qu'Qu + lam I)^-1 Qu' r_u minimiza o objetivo do usuario", np.allclose(pu, o, atol=1e-4))

docs = ["cafe torrado especial", "cafe em capsula", "caneca termica", "moedor de cafe manual"]
v = TfidfVectorizer(); Xt = v.fit_transform(docs)
df_ = np.array((Xt > 0).sum(axis=0)).ravel()
t("TF-IDF: idf = ln((1+n)/(1+df)) + 1 (padrao do scikit-learn)", np.allclose(np.log((1+len(docs))/(1+df_))+1, v.idf_))
t("TF-IDF: linhas com norma L2 = 1", np.allclose(np.sqrt(np.asarray(Xt.multiply(Xt).sum(axis=1))).ravel(), 1))

ok_ndcg = ok_ap = ok_prec = True
for rep in range(200):
    n_it = 12; kk = int(rng.integers(1, 8))
    rel = (rng.random(n_it) < .35).astype(int)
    if rel.sum() == 0: rel[rng.integers(n_it)] = 1
    sc = rng.random(n_it); ordem = np.argsort(-sc)
    ac = rel[ordem][:kk]
    dcg = np.sum(ac/np.log2(np.arange(2, kk+2)))
    ideal = np.sort(rel)[::-1][:kk]; idcg = np.sum(ideal/np.log2(np.arange(2, kk+2)))
    ok_ndcg &= np.isclose(dcg/idcg, ndcg_score(rel[None], sc[None], k=kk))
    acf = rel[ordem]
    ap = np.sum([acf[:j+1].sum()/(j+1) for j in range(n_it) if acf[j]]) / rel.sum()
    ok_ap &= np.isclose(ap, average_precision_score(rel, sc))
    pred_topk = np.zeros(n_it, int); pred_topk[ordem[:kk]] = 1
    ok_prec &= np.isclose(ac.sum()/kk, precision_score(rel, pred_topk, zero_division=0))
t("NDCG@k = DCG/IDCG, DCG = sum rel_j/log2(j+1) (200 casos)", bool(ok_ndcg))
t("AP = media da precisao nos pontos de acerto (k = n; 200 casos)", bool(ok_ap))
t("Precision@k = acertos no top-k / k (200 casos)", bool(ok_prec))

# ================= Extensao: aprendizagem por reforco =================
gam = .9
rs = rng.random(50); G = 0.0; ret = []
for r_ in reversed(rs):
    G = r_ + gam*G; ret.insert(0, G)
t("retorno: recursao G_t = r + gamma*G_{t+1} == sum gamma^k r_{t+k+1}",
  np.isclose(ret[0], np.sum(gam**np.arange(50)*rs)))

nS, nA = 6, 3
Pm = rng.random((nS, nA, nS)); Pm /= Pm.sum(axis=2, keepdims=True)
Rsa = rng.normal(size=(nS, nA))
pol = rng.random((nS, nA)); pol /= pol.sum(axis=1, keepdims=True)
P_pi = np.einsum("sa,sat->st", pol, Pm); R_pi = np.sum(pol*Rsa, axis=1)
V_fech = np.linalg.solve(np.eye(nS)-gam*P_pi, R_pi)
V = np.zeros(nS)
for _ in range(2000):
    V = np.sum(pol*(Rsa + gam*np.einsum("sat,t->sa", Pm, V)), axis=1)
t("Bellman (avaliacao de politica): V = (I - gamma P_pi)^-1 R_pi", np.allclose(V, V_fech, atol=1e-8))
Qs = np.zeros((nS, nA))
for _ in range(3000):
    Qs = Rsa + gam*np.einsum("sat,t->sa", Pm, Qs.max(axis=1))
t("Bellman otima: Q* e ponto fixo de R + gamma*sum P max Q*",
  np.allclose(Qs, Rsa + gam*np.einsum("sat,t->sa", Pm, Qs.max(axis=1)), atol=1e-10))

nxt = rng.integers(0, nS, (nS, nA))                   # MDP deterministico
Rd = rng.normal(size=(nS, nA))
Qstar = np.zeros((nS, nA))
for _ in range(3000):
    Qstar = Rd + gam*Qstar[nxt].max(axis=2)
Ql = np.zeros((nS, nA)); s_ = 0
for passo in range(200_000):
    a_ = int(rng.integers(nA))                        # exploracao uniforme (off-policy)
    s2 = nxt[s_, a_]
    alfa = 1/(1+passo/2000)
    Ql[s_, a_] += alfa*(Rd[s_, a_] + gam*Ql[s2].max() - Ql[s_, a_])
    s_ = s2 if rng.random() > .05 else int(rng.integers(nS))
t("Q-learning converge para Q* (MDP deterministico, exploracao uniforme)", np.allclose(Ql, Qstar, atol=5e-2),
  f"max dif={np.abs(Ql-Qstar).max():.3f}")

from scipy.stats import beta as beta_dist
s_suc, f_fal = 7, 13
th = np.linspace(1e-4, 1-1e-4, 20001)
post = th**s_suc*(1-th)**f_fal; post /= np.trapezoid(post, th)
t("Thompson: posteriori Beta(1+s, 1+f) com priori Beta(1,1)", np.allclose(post, beta_dist(1+s_suc, 1+f_fal).pdf(th), atol=1e-3))

th_p = rng.normal(size=4); rb = rng.normal(size=4)
pi_ = lambda th: np.exp(th)/np.exp(th).sum()
J_ = lambda th: pi_(th) @ rb
num = np.array([(J_(th_p+1e-6*np.eye(4)[i])-J_(th_p-1e-6*np.eye(4)[i]))/2e-6 for i in range(4)])
p_ = pi_(th_p); grad_log = np.eye(4) - p_                # d log pi(a) / d theta = e_a - pi
teo = np.sum(p_[:, None]*grad_log*rb[:, None], axis=0)
t("Policy gradient: grad E[r] = E[grad log pi(a) * r]", np.allclose(num, teo, atol=1e-6))

pl, pn, pc = np.array([.5, .25, .25]), np.array([.1, .8, .1]), np.array([.02, .05, .03])
t("IPS e nao viesado: E_log[(pi_nova/pi_log) r] = sum pi_nova p", np.isclose(np.sum(pl*(pn/pl)*pc), pn @ pc))

# ================= Extensao: roadmap (associacao, anomalias, semissupervisionado, RL baseado em modelo) =================
from scipy import stats
from scipy.stats import norm
xs = rng.normal(5, 2, 400)
t("z-score: (x - media)/desvio (ddof=0) == scipy.stats.zscore", np.allclose((xs-xs.mean())/xs.std(), stats.zscore(xs)))
t("z robusto: 0,6745 = Phi^-1(0,75)", np.isclose(norm.ppf(.75), .6745, atol=1e-4))
xg = rng.normal(0, 3, 200_000)
mad = np.median(np.abs(xg-np.median(xg)))
t("MAD/0,6745 estima o desvio-padrao sob normalidade", np.isclose(mad/.6745, 3, rtol=.01), f"{mad/.6745:.3f} vs 3")

import importlib.util
if importlib.util.find_spec("mlxtend"):
    import pandas as pd
    from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
    B = pd.DataFrame(rng.random((300, 6)) < [.5, .4, .3, .3, .2, .6], columns=list("abcdef"))
    B["b"] = B["b"] | (B["a"] & (rng.random(300) < .5))            # cria associacao a -> b
    regras = association_rules(apriori(B, min_support=.05, use_colnames=True), metric="support", min_threshold=0)
    ok = True
    for _, rg in regras.iterrows():
        A_, C_ = list(rg["antecedents"]), list(rg["consequents"])
        sA, sC, sAC = B[A_].all(axis=1).mean(), B[C_].all(axis=1).mean(), B[A_+C_].all(axis=1).mean()
        conf = sAC/sA
        ok &= np.isclose(rg["support"], sAC) and np.isclose(rg["confidence"], conf) and np.isclose(rg["lift"], conf/sC)
        ok &= np.isclose(rg["leverage"], sAC - sA*sC)
        ok &= (np.isinf(rg["conviction"]) if conf == 1 else np.isclose(rg["conviction"], (1-sC)/(1-conf)))
    t(f"associacao: suporte, confianca, lift, leverage, conviction ({len(regras)} regras)", bool(ok))
    fa = set(map(frozenset, apriori(B, min_support=.05, use_colnames=True)["itemsets"]))
    ff = set(map(frozenset, fpgrowth(B, min_support=.05, use_colnames=True)["itemsets"]))
    t("FP-Growth encontra exatamente os itemsets do Apriori", fa == ff, f"{len(fa)} itemsets")
else:
    res.append((True, "associacao (mlxtend ausente: SKIP)", ""))

from sklearn.semi_supervised import LabelSpreading
from sklearn.metrics.pairwise import rbf_kernel
Xl = rng.normal(size=(60, 2)); yl = np.full(60, -1); yl[:4] = [0, 1, 0, 1]
alfa, gama = .2, .5
ls = LabelSpreading(kernel="rbf", gamma=gama, alpha=alfa, max_iter=100000, tol=1e-12).fit(Xl, yl)
W = rbf_kernel(Xl, gamma=gama); np.fill_diagonal(W, 0)
d = W.sum(axis=1); S = W/np.sqrt(np.outer(d, d))
Y0 = np.zeros((60, 2)); Y0[np.arange(4), yl[:4]] = 1
F = np.linalg.solve(np.eye(60)-alfa*S, (1-alfa)*Y0); F = F/F.sum(axis=1, keepdims=True)
t("Label Spreading: F* = (1-alpha)(I - alpha S)^-1 Y, S = D^-1/2 W D^-1/2", np.allclose(F, ls.label_distributions_, atol=1e-6))

nS2, nA2, g2 = 5, 2, .9
P2 = rng.random((nS2, nA2, nS2)); P2 /= P2.sum(axis=2, keepdims=True); R2 = rng.normal(size=(nS2, nA2))
V2 = np.zeros(nS2)
for _ in range(5000): V2 = (R2 + g2*np.einsum("sat,t->sa", P2, V2)).max(axis=1)
pol = np.zeros(nS2, int)
for _ in range(100):
    Pp = P2[np.arange(nS2), pol]; Rp = R2[np.arange(nS2), pol]
    Vp = np.linalg.solve(np.eye(nS2)-g2*Pp, Rp)
    nova = (R2 + g2*np.einsum("sat,t->sa", P2, Vp)).argmax(axis=1)
    if np.array_equal(nova, pol): break
    pol = nova
t("value iteration e policy iteration chegam ao mesmo V*", np.allclose(V2, Vp, atol=1e-8))

for c, n_, d in res: print(("OK   " if c else "FALHA"), f"{n_:72s} {d}")
print(f"\n{sum(c for c, _, _ in res)}/{len(res)} formulas conferidas numericamente")
