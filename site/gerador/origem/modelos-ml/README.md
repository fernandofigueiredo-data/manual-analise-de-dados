# Notebooks modelo de Machine Learning

Templates genéricos derivados dos notebooks de `modelos/`, prontos para outros datasets. Cada um está associado a um cartão da seção Machine Learning do site, onde também pode ser baixado. A revisão que os originou está em `../REVISAO_NOTEBOOKS.md`.

| Template | Cartão no site | Precisa de |
|---|---|---|
| `modelo_ml_regressao_linear.ipynb` | Regressão Linear | scikit-learn |
| `modelo_ml_regressao_logistica.ipynb` | Regressão Logística | scikit-learn |
| `modelo_ml_rede_neural_binaria.ipynb` | Rede Neural (MLP) | Keras 3 |
| `modelo_ml_rede_neural_multiclasse.ipynb` | Rede Neural (MLP) | Keras 3 |
| `modelo_ml_regressao_polinomial_vies_variancia.ipynb` | Regressão Polinomial | scikit-learn; Keras 3 na parte B (opcional) |
| `modelo_ml_arvore_de_decisao.ipynb` | Decision Tree | scikit-learn |
| `modelo_ml_deteccao_anomalias_gaussiana.ipynb` | Gaussian Mixture Model (GMM) | scikit-learn |
| `modelo_ml_kmeans.ipynb` | K-Means | scikit-learn |
| `modelo_ml_recomendacao_conteudo_rede_neural.ipynb` | Filtragem baseada em conteúdo | Keras 3 |
| `modelo_ml_dqn.ipynb` | Deep Q-Network (DQN) | TensorFlow 2.16+ com Keras 3, Gymnasium |

## Como usar
1. Abra o notebook e edite **só** a célula `1. Configuração` (marcada `>>> ADAPTAR`): caminho do arquivo, coluna-alvo, features e hiperparâmetros.
2. Com o caminho em `None`, o notebook roda com dados sintéticos: execute uma vez assim para conhecer o fluxo.
3. Execute tudo em ordem (*Run All*).

## Manutenção
Depois de editar um template aqui, copie-o para `site/gerador/origem/modelos-ml/` e, em `site/`, rode `npm run gerar` e `npm run build`. O mapeamento template → cartão fica em `site/gerador/guia_ml.py` (`NOTEBOOKS_MODELO`).
