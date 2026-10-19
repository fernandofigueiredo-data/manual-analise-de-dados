"""Tema dos gráficos do notebook, derivado do Design System — Developer / Data Science / AI
(design-system/design-system-visual.md, seções 1, 5 e 6; docs/DESIGN-SYSTEM.md, seção 6).

Dark-first: figura no Grafite (camada 2), texto primário e secundário, grade no Grafite secundário,
séries na ordem categórica Ciano → Verde → Roxo → Âmbar; da quinta série em diante, variações de
luminância das mesmas quatro (nunca uma cor nova).
"""
from pathlib import Path

FONTES = sorted(str(p) for p in (Path(__file__).parent / "fontes").glob("*.ttf"))

NAVY = "#101522"
GRAFITE = "#151C2B"
GRAFITE_2 = "#202938"
CIANO = "#00E5FF"
VERDE = "#39FF88"
ROXO = "#A970FF"
AMBAR = "#FFB84D"
TEXTO = "#F2F7FF"
TEXTO_2 = "#AAB8CC"


def mistura(a: str, b: str, p: float) -> str:
    """p de a + (1 - p) de b, em sRGB (o mesmo que color-mix(in srgb, a p%, b))."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p * x + (1 - p) * y):02X}" for x, y in zip(ca, cb))


EIXO = mistura(TEXTO_2, GRAFITE, 0.5)

CATEGORICA = [CIANO, VERDE, ROXO, AMBAR,
              mistura(CIANO, NAVY, 0.55), mistura(VERDE, NAVY, 0.55),
              mistura(ROXO, NAVY, 0.6), mistura(AMBAR, NAVY, 0.55)]
SEQUENCIAL = [mistura(ROXO, GRAFITE, 0.12), mistura(ROXO, GRAFITE, 0.55), ROXO, mistura(ROXO, TEXTO, 0.45)]
DIVERGENTE = [AMBAR, GRAFITE_2, CIANO]
ESCURA = [mistura(ROXO, NAVY, 0.45), mistura(ROXO, NAVY, 0.6), mistura(ROXO, NAVY, 0.75)]

# Cores fixadas no código do notebook -> cor equivalente do design system.
# Aplicadas só no código executado; o código exibido no site continua o original.
EQUIVALENCIAS = {
    "'steelblue'": f"'{CIANO}'",
    "'#2a9d8f'": f"'{CIANO}'",
    "'#453698'": f"'{TEXTO_2}'",
    "'red'": f"'{AMBAR}'",
    "'green'": f"'{VERDE}'",
    "'#efab02'": f"'{AMBAR}'",
    "'black'": f"'{TEXTO}'",
    "'gray'": f"'{TEXTO_2}'",
    "'lightgray'": f"'{GRAFITE_2}'",
    "linecolor='white'": f"linecolor='{GRAFITE}'",
    "'viridis'": "'ds_seq'",
    "'Blues'": "'ds_seq'",
    "'magma'": "'ds_seq'",
    "'YlGnBu'": "'ds_seq'",
    "'RdBu_r'": "'ds_div'",
    "'coolwarm'": "'ds_div'",
}

# palette='viridis' em barras com rótulo branco centralizado: variações escuras do Roxo
EQUIVALENCIAS_PALETA = {
    "palette='viridis'": "palette='ds_escura'",
    # barras de erro do seaborn saem em cinza escuro (".26"), invisíveis no Grafite: texto secundário
    "capsize=0.1,": f"capsize=0.1, err_kws={{'color': '{TEXTO_2}'}},",
}

CELULA_TEMA = f'''
import matplotlib as _mpl
from matplotlib import font_manager as _fm
from matplotlib.colors import LinearSegmentedColormap as _LSC
for _f in {FONTES!r}:
    _fm.fontManager.addfont(_f)
for _nome, _cores in (("ds_seq", {SEQUENCIAL!r}), ("ds_div", {DIVERGENTE!r}), ("ds_escura", {ESCURA!r})):
    if _nome not in _mpl.colormaps:
        _mpl.colormaps.register(_LSC.from_list(_nome, _cores))
sns.set_theme(style='whitegrid', context='notebook', palette={CATEGORICA!r}, rc={{
    'font.family': ['JetBrains Mono', 'DejaVu Sans'],
    'text.color': '{TEXTO}', 'axes.labelcolor': '{TEXTO}', 'axes.titlecolor': '{TEXTO}',
    'axes.edgecolor': '{EIXO}', 'grid.color': '{GRAFITE_2}',
    'xtick.color': '{TEXTO_2}', 'ytick.color': '{TEXTO_2}',
    'figure.facecolor': '{GRAFITE}', 'axes.facecolor': '{GRAFITE}', 'savefig.facecolor': '{GRAFITE}',
    'legend.facecolor': '{GRAFITE_2}', 'legend.edgecolor': '{GRAFITE_2}', 'legend.labelcolor': '{TEXTO}',
    'image.cmap': 'ds_seq', 'patch.edgecolor': '{GRAFITE}',
    'lines.color': '{TEXTO}', 'boxplot.flierprops.markeredgecolor': '{TEXTO_2}',
}})
plt.rcParams['figure.figsize'] = (10, 5)
get_ipython().run_line_magic('config', "InlineBackend.print_figure_kwargs = {{'bbox_inches': 'tight', 'dpi': 150, 'facecolor': '{GRAFITE}'}}")
'''
