// Gerado por gerador/guia_ml.py a partir de manual_machine_learning.html (não editar).
// Função de realce usada pelo diagnóstico para o código inicial.
const esc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
// realce de sintaxe Python (aplicado sobre texto já escapado)
const PY_KW = "from|import|as|def|return|for|in|if|elif|else|while|class|with|not|and|or|None|True|False|lambda|try|except|finally|break|continue|pass|yield|global|assert|del|raise|is|print";
function highlightPy(escaped){
  const re = new RegExp(
    "(#[^\\n]*)" +                                   // comentário
    "|(\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?'''|\"(?:[^\"\\\\\\n]|\\\\.)*\"|'(?:[^'\\\\\\n]|\\\\.)*')" + // string
    "|\\b(" + PY_KW + ")\\b" +                       // palavra-chave
    "|\\b(\\d+\\.?\\d*(?:e-?\\d+)?)\\b" +            // número
    "|([A-Za-z_][A-Za-z0-9_]*)(?=\\()",              // chamada de função
    "g");
  return escaped.replace(re, (m, c, s, k, n, f) => {
    if (c) return '<span class="tok-c">' + c + '</span>';
    if (s) return '<span class="tok-s">' + s + '</span>';
    if (k) return '<span class="tok-k">' + k + '</span>';
    if (n) return '<span class="tok-n">' + n + '</span>';
    if (f) return '<span class="tok-f">' + f + '</span>';
    return m;
  });
}


globalThis.highlightPy = highlightPy;
