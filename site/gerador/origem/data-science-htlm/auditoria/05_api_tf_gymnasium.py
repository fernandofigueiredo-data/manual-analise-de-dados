"""Auditoria 5/5 - afirmacoes de API do TensorFlow/Keras 3 e do Gymnasium feitas nos artefatos.
Roda com qualquer interpretador; o que nao estiver instalado aparece como SKIP.
Uso: python3 auditoria/05_api_tf_gymnasium.py   (TensorFlow exige Python <= 3.13)"""
import os, importlib.util, inspect, sys
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
chk = []
t = lambda nome, cond, det="": chk.append(("OK " if cond else "FALHA", nome, det))
skip = lambda nome, det: chk.append(("SKIP", nome, det))

if importlib.util.find_spec("tensorflow"):
    import tensorflow as tf, keras
    t("tf.keras e o Keras 3 (TF >= 2.16)", keras.__version__.startswith("3.") and tf.keras.Sequential is keras.Sequential,
      f"tensorflow {tf.__version__} | keras {keras.__version__}")
    t("Keras 3: Model.export existe (SavedModel de inferencia)", hasattr(keras.Model, "export"))
    t("tf.lite.TFLiteConverter.from_saved_model existe", hasattr(tf.lite.TFLiteConverter, "from_saved_model"))
    t("Normalization.adapt existe", hasattr(keras.layers.Normalization, "adapt"))
    t("metrics.AUC aceita curve='PR'", "curve" in inspect.signature(keras.metrics.AUC.__init__).parameters)
    t("Optimizer.build existe (estado criado fora do tf.function)", hasattr(keras.optimizers.Adam, "build"))
    t("layers.Rescaling aceita offset", "offset" in inspect.signature(keras.layers.Rescaling.__init__).parameters)
else:
    skip("TensorFlow", f"nao instalado neste interpretador (Python {sys.version.split()[0]})")

if importlib.util.find_spec("gymnasium"):
    import gymnasium as gym
    env = gym.make("CartPole-v1")
    out = env.reset(seed=0)
    t("gymnasium reset() devolve (obs, info)", isinstance(out, tuple) and len(out) == 2, f"gymnasium {gym.__version__}")
    out = env.step(env.action_space.sample())
    t("gymnasium step() devolve 5 valores (obs, r, terminated, truncated, info)", len(out) == 5)
    t("FrozenLake-v1 aceita is_slippery", gym.make("FrozenLake-v1", is_slippery=False) is not None)
else:
    skip("Gymnasium", "nao instalado neste interpretador")

if importlib.util.find_spec("mlxtend"):
    import mlxtend
    from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
    sig = inspect.signature(association_rules).parameters
    t("mlxtend: association_rules tem num_itemsets (default 1)", "num_itemsets" in sig and sig["num_itemsets"].default == 1, f"mlxtend {mlxtend.__version__}")
    t("mlxtend: apriori e fpgrowth aceitam min_support e use_colnames",
      all(k in inspect.signature(f).parameters for f in (apriori, fpgrowth) for k in ("min_support", "use_colnames")))
else:
    skip("mlxtend", "nao instalado neste interpretador")

for s_, n, d in chk:
    print(f"{s_:5s} {n:62s} {d}")
ok = sum(1 for s_, *_ in chk if s_.strip() == "OK"); fal = sum(1 for s_, *_ in chk if s_ == "FALHA")
print(f"\n{ok} confirmadas | falhas: {fal} | skip: {sum(1 for s_, *_ in chk if s_ == 'SKIP')}")
