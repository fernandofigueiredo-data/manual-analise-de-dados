#!/usr/bin/env bash
# Roda as 6 baterias da auditoria com os ambientes locais de htlm/.
# Uso (a partir de qualquer pasta):  bash htlm/auditoria/rodar_tudo.sh [--reprodutibilidade]
set -u
cd "$(dirname "$0")/.."                       # pasta htlm/

PY=./.venv-auditoria/bin/python               # Python 3.14: sklearn, boosting, torch, gymnasium, mlxtend
PY_TF=./.venv-tf/bin/python                   # Python 3.12: TensorFlow (sem pacote para 3.14)
for p in "$PY" "$PY_TF"; do
  [ -x "$p" ] || { echo "Ambiente ausente: $p (veja a secao 6 de auditoria_ml.md)"; exit 1; }
done

export DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}  # libomp e keg-only
export AUDITORIA_PY_TF="$PWD/.venv-tf/bin/python"
export TF_CPP_MIN_LOG_LEVEL=3

falhou=0
rodar() {                                     # rodar <rotulo> <interpretador> <script>
  echo; echo "=== $1 ==="
  saida=$("$2" "$3" 2>&1); code=$?
  echo "$saida" | grep -E "FALHA|ERRO " || true
  echo "$saida" | grep -E "RESUMO|confirmadas|conferidas|demonstram|^nenhum$|^ - " || echo "$saida" | tail -1
  if [ $code -ne 0 ] || echo "$saida" | grep -qE "FALHA|ERRO |falhas: [1-9]"; then falhou=1; fi
}
rodar "01 APIs do scikit-learn"             "$PY"    auditoria/01_api_sklearn.py
rodar "02 Formulas"                         "$PY"    auditoria/02_formulas.py
rodar "03 Execucao dos trechos"             "$PY"    auditoria/03_executar_snippets.py
rodar "04 Consistencia estrutural"          "$PY"    auditoria/04_consistencia.py
rodar "05 APIs TensorFlow"                  "$PY_TF" auditoria/05_api_tf_gymnasium.py
rodar "05 APIs Gymnasium e mlxtend"         "$PY"    auditoria/05_api_tf_gymnasium.py
rodar "06 Saidas esperadas"                 "$PY"    auditoria/06_saidas_esperadas.py

# opcional: roda a bateria 06 duas vezes em paralelo e exige saidas identicas
if [ "${1:-}" = "--reprodutibilidade" ]; then
  echo; echo "=== Reprodutibilidade (06 executada duas vezes) ==="
  t=$(mktemp -d)
  ( "$PY" auditoria/06_saidas_esperadas.py > "$t/a" 2>&1 & "$PY" auditoria/06_saidas_esperadas.py > "$t/b" 2>&1 & wait )
  # o export do TensorFlow imprime um endereco de memoria: unica linha que pode legitimamente variar
  if diff <(grep -v TensorSpec "$t/a") <(grep -v TensorSpec "$t/b") > "$t/diff"; then
    echo "execucoes identicas"
  else
    echo "SAIDAS DIFERENTES entre execucoes:"; cat "$t/diff"; falhou=1
  fi
fi

# a bateria 04 imprime "nenhum" quando esta limpa
"$PY" auditoria/04_consistencia.py | sed -n '4p' | grep -q "nenhum" || { echo "04: ha achados estruturais"; falhou=1; }

echo
if [ $falhou -eq 0 ]; then echo "AUDITORIA LIMPA"; else echo "AUDITORIA COM FALHAS"; fi
exit $falhou
