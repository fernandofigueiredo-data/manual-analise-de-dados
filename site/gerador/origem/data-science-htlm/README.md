# Manual de Machine Learning

Manual de estudo, consulta e decisão em Machine Learning, num único arquivo HTML estático: taxonomia rigorosa, 43 modelos no mesmo template de 20 blocos, matrizes de decisão, métricas, validação, pipeline e checklist profissional — com as APIs de setembro de 2026 (scikit-learn 1.9.1, XGBoost 3.4.1, LightGBM 4.x, CatBoost 1.2.x, Keras 3, PyTorch 2.x).

## Como abrir

Abra `manual_machine_learning.html` no navegador. Não há build, backend nem dependências externas; para publicar, basta servir a pasta como site estático (GitHub Pages, Netlify, qualquer servidor de arquivos).

## Arquivos

| Arquivo | Papel |
|---|---|
| `manual_machine_learning.html` | O manual: estudo e consulta, com busca, filtros por categoria e tema claro/escuro |
| `skill_decisao_ml.md` | A skill de decisão: regras IF/THEN, hierarquia de complexidade, Model Fit Score e diagnóstico de 16 itens |
| `auditoria_ml.md` | Relatório da auditoria técnica (APIs, fórmulas, execução dos trechos de código) |
| `auditoria/` | Scripts que reproduzem a auditoria (`bash auditoria/rodar_tudo.sh`) |

## Diagnóstico do seu dataset

A seção **Diagnóstico do seu dataset** do manual recebe um arquivo CSV, TSV, JSON/JSON Lines ou XLSX e devolve o diagnóstico de 16 itens da skill: tipo de problema, modelos candidatos e frameworks, pré-processamento, métrica, validação, alertas sobre o dataset e um código Python inicial. As regras são determinísticas e rodam inteiramente no navegador: o arquivo não é enviado a nenhum servidor. O módulo não treina modelos — devolve um plano de experimentos.

## Reproduzir a auditoria

Os ambientes Python não fazem parte do repositório. Para recriá-los e rodar as seis baterias, siga a seção 6 de `auditoria_ml.md`:

```bash
bash auditoria/rodar_tudo.sh
```
