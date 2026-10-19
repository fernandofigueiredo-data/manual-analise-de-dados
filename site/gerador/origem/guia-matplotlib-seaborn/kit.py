"""Motor do guia: executa cada bloco de código, captura a figura e gera o HTML."""
import base64
import html
import io
import json
import re
import textwrap
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

NAV = []          # (nivel, id, rotulo, attrs)
WARN_LOG = []
STATS = {"imagens": 0, "bytes": 0}
_uid = [0]

PRE_MPL = '''import matplotlib.pyplot as plt
import numpy as np

# Estilo do guia: cinza para contexto, azul para destaque, laranja para alerta
CINZA, AZUL, LARANJA = "#A6A6A6", "#1F5FA8", "#D9731A"
plt.rcParams.update({
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#BFBFBF", "axes.labelcolor": "#595959",
    "xtick.color": "#595959", "ytick.color": "#595959",
    "axes.titlelocation": "left", "axes.titlesize": 13, "font.size": 10.5,
})'''

PRE_SNS = '''import matplotlib.pyplot as plt
import seaborn as sns

# Estilo do guia: cinza para contexto, azul para destaque, laranja para alerta
CINZA, AZUL, LARANJA = "#A6A6A6", "#1F5FA8", "#D9731A"
sns.set_theme(style="white", font_scale=0.95, rc={
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#BFBFBF", "axes.labelcolor": "#595959",
    "xtick.color": "#595959", "ytick.color": "#595959",
    "axes.titlelocation": "left", "axes.titlesize": 13,
})'''


def code(src):
    """Normaliza um bloco e expande os preâmbulos de estilo."""
    src = textwrap.dedent(src).strip("\n")
    src = src.replace("<<MPL>>", PRE_MPL).replace("<<SNS>>", PRE_SNS)
    return src + "\n"


def uid(prefix="b"):
    _uid[0] += 1
    return f"{prefix}{_uid[0]}"


# ---------------------------------------------------------------- execução
def run(src, nome=""):
    """Executa exatamente o código exibido e devolve a figura em PNG base64."""
    matplotlib.rcdefaults()
    plt.close("all")
    capt = []
    original = plt.show

    def fake_show(*a, **k):
        capt.append(plt.gcf())

    plt.show = fake_show
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            exec(compile(src, f"<{nome}>", "exec"), {"__name__": "__main__"})
            for item in w:
                WARN_LOG.append(f"{nome}: {item.category.__name__}: {item.message}")
    finally:
        plt.show = original
    fig = capt[-1] if capt else plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", pad_inches=0.15)
    plt.close("all")
    img = Image.open(io.BytesIO(buf.getvalue())).convert("RGB")
    out = io.BytesIO()
    img.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(
        out, format="PNG", optimize=True)
    data = out.getvalue()
    STATS["imagens"] += 1
    STATS["bytes"] += len(data)
    return base64.b64encode(data).decode(), img.size


# ---------------------------------------------------------------- eixos
EIXOS = {
    "contexto": "Entender o contexto",
    "visual": "Escolher um visual eficaz",
    "desordem": "Eliminar a desordem",
    "atencao": "Focar a atenção",
    "designer": "Pensar como designer",
    "historia": "Contar uma história",
}

PADROES = {
    "visual": r"\.(plot|bar|barh|scatter|hist|boxplot|violinplot|imshow|pie|fill_between|hlines|vlines)\(|sns\.(lineplot|barplot|scatterplot|histplot|boxplot|violinplot|heatmap|pairplot|regplot|lmplot|jointplot|relplot|kdeplot|stripplot)\(",
    "desordem": r"spines|grid|despine|tick_params|set_visible|legend=False|set_yticks\(\[\]\)|set_xticks\(\[\]\)|frameon|set_ylabel\(\"\"\)|set_xlabel\(\"\"\)|cbar=False|linewidth=0|edgecolor=\"white\"|axis\(\"off\"\)",
    "atencao": r"AZUL|LARANJA|fontweight=\"bold\"|zorder|alpha=",
    "designer": r"bar_label|set_xticks\(|set_yticks\(|set_xlim|set_ylim|ha=\"|va=\"|figsize|FuncFormatter|replace\(\"\.\", \",\"\)|tight_layout|sharex|invert_yaxis",
    "historia": r"set_title|suptitle|annotate|fig\.text|ax\.text|axvspan|axhline",
}


def mapa_eixos(src):
    linhas = src.rstrip("\n").split("\n")
    res = {}
    for eixo, pad in PADROES.items():
        rx = re.compile(pad)
        hits = [i + 1 for i, ln in enumerate(linhas)
                if rx.search(ln) and not ln.lstrip().startswith("#")]
        if hits:
            res[eixo] = hits
    return res


# ---------------------------------------------------------------- render
LIBNOME = {"mpl": "matplotlib", "sns": "seaborn"}


def codeblock(src, lib):
    axes = mapa_eixos(src)
    return (f'<div class="codeblock" data-axes=\'{json.dumps(axes)}\'>'
            f'<div class="codebar"><span>python · {LIBNOME.get(lib, lib)}</span>'
            f'<button class="copy" type="button" aria-label="Copiar código">Copiar</button></div>'
            f'<pre><code class="py">{html.escape(src)}</code></pre></div>')


def figura(src, nome, alt, lib):
    b64, (w, h) = run(src, nome)
    return (f'<figure class="fig"><img loading="lazy" width="{w}" height="{h}" '
            f'alt="{html.escape(alt)}" src="data:image/png;base64,{b64}"></figure>')


def duo(src, nome, alt, lib):
    return f'<div class="duo">{figura(src, nome, alt, lib)}{codeblock(src, lib)}</div>'


def switcher(nome, variantes, kind="tabs", alt=""):
    """variantes: lista de dicts com label, lib, code e (opcional) texto."""
    sid = uid("sw")
    botoes, panes = [], []
    for i, v in enumerate(variantes):
        sel = "true" if i == 0 else "false"
        botoes.append(f'<button type="button" role="tab" aria-selected="{sel}" data-i="{i}" '
                      f'data-lib="{v.get("lib", "mpl")}">{html.escape(v["label"])}</button>')
        texto = f'<div class="pane-text">{v["texto"]}</div>' if v.get("texto") else ""
        panes.append(f'<div class="pane" role="tabpanel" data-i="{i}" data-lib="{v.get("lib", "mpl")}"'
                     f'{"" if i == 0 else " hidden"}>{texto}'
                     f'{duo(v["code"], f"{nome}-{i}", alt + " (" + v["label"] + ")", v.get("lib", "mpl"))}</div>')
    nav = ""
    if kind == "steps":
        nav = ('<div class="stepnav"><button type="button" class="prev">Anterior</button>'
               '<button type="button" class="next">Próximo</button></div>')
    return (f'<div class="switch {kind}" id="{sid}"><div class="seg" role="tablist">{"".join(botoes)}</div>'
            f'{"".join(panes)}{nav}</div>')


def nav(nivel, id_, rotulo, **attrs):
    NAV.append((nivel, id_, rotulo, attrs))


def chips_eixos(eixos):
    return "".join(f'<button type="button" class="chip eixo" data-axis="{e}">{EIXOS[e]}</button>'
                   for e in eixos)


def k(txt):
    """Selo de ideia atribuída a Knaflic."""
    return f'<span class="selo knaflic">Knaflic</span> {txt}'


def r(txt):
    """Selo de recomendação técnica do guia."""
    return f'<span class="selo tec">Recomendação técnica</span> {txt}'


CONFIRMAR = '<span class="selo confirmar">a confirmar no livro</span>'
