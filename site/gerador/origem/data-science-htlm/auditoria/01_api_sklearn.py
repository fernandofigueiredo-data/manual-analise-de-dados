"""Auditoria 1/4 - confere, por introspeccao, cada afirmacao de API feita nos dois artefatos.
Uso: python3 auditoria/01_api_sklearn.py"""
import inspect, sklearn, warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, LassoCV, ElasticNetCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import HistGradientBoostingClassifier, IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.calibration import CalibratedClassifierCV
from sklearn import metrics, model_selection

params = lambda c: set(inspect.signature(c.__init__).parameters) - {"self"}
chk = []
t = lambda nome, cond, det="": chk.append(("OK " if cond else "FALHA", nome, det))

t("LogisticRegression sem 'multi_class' (removido na 1.8)", "multi_class" not in params(LogisticRegression))
t("LogisticRegressionCV sem 'multi_class'", "multi_class" not in params(LogisticRegressionCV))
t("LogisticRegression mantem 'penalty' (dep. 1.8, remocao 1.10)", "penalty" in params(LogisticRegression))
t("LogisticRegression tem 'l1_ratio' e 'C'", {"l1_ratio", "C"} <= params(LogisticRegression))
t("mean_squared_error sem 'squared' (removido na 1.6)", "squared" not in inspect.signature(metrics.mean_squared_error).parameters)
t("root_mean_squared_error existe", hasattr(metrics, "root_mean_squared_error"))
t("OneHotEncoder usa 'sparse_output' (renomeado na 1.2)", "sparse_output" in params(OneHotEncoder) and "sparse" not in params(OneHotEncoder))
t("LassoCV sem 'n_alphas' (removido na 1.9)", "n_alphas" not in params(LassoCV))
t("ElasticNetCV sem 'n_alphas'", "n_alphas" not in params(ElasticNetCV))
d = inspect.signature(HistGradientBoostingClassifier.__init__).parameters["categorical_features"].default
t("HistGB categorical_features default 'from_dtype' (1.6)", d == "from_dtype", f"default={d!r}")
t("OneClassSVM sem 'random_state'", "random_state" not in params(OneClassSVM))
t("LocalOutlierFactor tem 'novelty'", "novelty" in params(LocalOutlierFactor))
t("TunedThresholdClassifierCV em model_selection", hasattr(model_selection, "TunedThresholdClassifierCV"))
t("FixedThresholdClassifier em model_selection", hasattr(model_selection, "FixedThresholdClassifier"))
sc = inspect.signature(model_selection.TunedThresholdClassifierCV.__init__).parameters["scoring"].default
t("TunedThresholdClassifierCV scoring='balanced_accuracy'", sc == "balanced_accuracy", f"default={sc!r}")
t("config global 'sparse_interface' existe", "sparse_interface" in inspect.signature(sklearn.set_config).parameters)
t("CalibratedClassifierCV usa 'estimator' (nao 'base_estimator')", "estimator" in params(CalibratedClassifierCV))
try:
    from sklearn.frozen import FrozenEstimator; ok_frozen = True
except ImportError:
    ok_frozen = False
t("sklearn.frozen.FrozenEstimator disponivel (substitui cv='prefit')", ok_frozen)
t("metrics.ndcg_score existe (metricas de ranking)", hasattr(metrics, "ndcg_score"))
t("ndcg_score aceita o parametro k", "k" in inspect.signature(metrics.ndcg_score).parameters)
from sklearn.semi_supervised import SelfTrainingClassifier, LabelSpreading, LabelPropagation
from sklearn.decomposition import FastICA
from sklearn.multioutput import MultiOutputRegressor, RegressorChain
t("SelfTrainingClassifier usa 'estimator' (nao 'base_estimator')", "estimator" in params(SelfTrainingClassifier) and "base_estimator" not in params(SelfTrainingClassifier))
t("SelfTrainingClassifier tem threshold/criterion/k_best", {"threshold","criterion","k_best"} <= params(SelfTrainingClassifier))
t("LabelSpreading/LabelPropagation aceitam kernel rbf|knn", "kernel" in params(LabelSpreading) and "kernel" in params(LabelPropagation))
t("FastICA aceita whiten='unit-variance'", FastICA(whiten="unit-variance").whiten == "unit-variance")
t("MultiOutputRegressor e RegressorChain existem", MultiOutputRegressor is not None and RegressorChain is not None)
sc2 = inspect.signature(LogisticRegressionCV.__init__).parameters["scoring"].default
chk.append(("INFO", "LogisticRegressionCV scoring default", repr(sc2)))

print("scikit-learn", sklearn.__version__)
for s, n, d in chk:
    print(f"{s:5s} {n:58s} {d}")
falhas = sum(1 for s, *_ in chk if s == "FALHA")
print(f"\n{len(chk)-falhas-1}/{len(chk)-1} afirmacoes confirmadas | falhas: {falhas}")
