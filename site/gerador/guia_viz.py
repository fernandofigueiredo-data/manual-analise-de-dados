"""Guia matplotlib e seaborn -> páginas do site.

Reaproveita o código do próprio guia (origem/guia-matplotlib-seaborn): os módulos de conteúdo
(fundamentos, catalogo, story, referencia) e as funções de montagem de build.py são usados sem
alteração. Só a camada de renderização do kit.py é trocada, para que blocos de código, figuras e
abas usem os componentes do site e as imagens sejam gravadas como arquivos WebP.

Cada imagem continua sendo produzida executando exatamente o código exibido ao lado dela, com o
estilo do próprio guia (cinza, azul e laranja).
"""
from __future__ import annotations

import base64
import html as H
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

import tema
from comum import PUBLICO, bloco_codigo, esc, figura, salvar_imagem

AQUI = Path(__file__).resolve().parent
ORIGEM = AQUI / "origem" / "guia-matplotlib-seaborn"
sys.path.insert(0, str(ORIGEM))

import kit  # noqa: E402  (o kit original do guia)

_kit_run = kit.run

# ------------------------------------------------------------------ tema escuro do design system (só na execução)
# As figuras são geradas no tema do site, como as do notebook: o código exibido continua o original
# e as cores fixadas nele são trocadas pelas equivalentes do design system apenas no código executado.
CONTEXTO = tema.mistura(tema.TEXTO_2, tema.GRAFITE, 0.5)        # cinza de contexto: recua no fundo escuro
CONTEXTO_CLARO = tema.mistura(tema.TEXTO_2, tema.GRAFITE, 0.3)
EIXO = tema.mistura(tema.TEXTO_2, tema.GRAFITE, 0.45)
CORES_GUIA = {
    "#A6A6A6": CONTEXTO,              # CINZA: contexto
    "#1F5FA8": tema.CIANO,            # AZUL: destaque (primeira cor categórica)
    "#D9731A": tema.AMBAR,            # LARANJA: alerta
    "#595959": tema.TEXTO_2, "#7F7F7F": tema.TEXTO_2, "#404040": tema.TEXTO_2,
    "#262626": tema.TEXTO,
    "#BFBFBF": EIXO,
    "#EDEDED": tema.GRAFITE_2, "#EEF2F7": tema.GRAFITE_2,
    "#E6E6E6": CONTEXTO_CLARO, "#D9D9D9": CONTEXTO_CLARO, "#D4D4D4": CONTEXTO_CLARO, "#C8C8C8": CONTEXTO_CLARO,
}
ESCURO = {
    "figure.facecolor": tema.GRAFITE, "axes.facecolor": tema.GRAFITE, "savefig.facecolor": tema.GRAFITE,
    "text.color": tema.TEXTO, "axes.labelcolor": tema.TEXTO_2, "axes.titlecolor": tema.TEXTO,
    "axes.edgecolor": EIXO, "xtick.color": tema.TEXTO_2, "ytick.color": tema.TEXTO_2,
    "grid.color": tema.GRAFITE_2, "legend.facecolor": tema.GRAFITE_2, "legend.edgecolor": tema.GRAFITE_2,
    "legend.labelcolor": tema.TEXTO, "patch.edgecolor": tema.GRAFITE, "boxplot.flierprops.markeredgecolor": tema.TEXTO_2,
    "font.family": ["JetBrains Mono", "DejaVu Sans"],
}
PRELUDIO = f'''
import matplotlib as _mpl
from matplotlib import font_manager as _fm
from cycler import cycler as _cycler
for _f in {tema.FONTES!r}:
    _fm.fontManager.addfont(_f)
_ESCURO = {ESCURO!r}
_ESCURO["axes.prop_cycle"] = _cycler(color={tema.CATEGORICA!r})
_mpl.rcParams.update(_ESCURO)
import seaborn as _sns
if not getattr(_sns, "_tema_site", False):
    for _nome in ("set_theme", "set_style", "set"):
        def _envolver(_orig):
            def _novo(*a, **k):
                _orig(*a, **k)
                _mpl.rcParams.update(_ESCURO)
            return _novo
        setattr(_sns, _nome, _envolver(getattr(_sns, _nome)))
    _sns._tema_site = True
    # jointplot(kind="hex") monta a escala do branco ao preto; no fundo escuro ela parte do Grafite secundário
    import seaborn.axisgrid as _ag
    _blend_orig = _ag.blend_palette
    def _blend(cores, *a, **k):
        if k.get("as_cmap") and len(cores) == 12:
            cores = ["{tema.GRAFITE_2}", cores[7], cores[5], cores[3]]
        return _blend_orig(cores, *a, **k)
    _ag.blend_palette = _blend
'''
SUBSTITUICOES_GUIA: list[dict] = []


def _codigo_execucao(src: str, nome: str) -> str:
    novo = src
    # texto escolhido pelo valor da célula sobre a escala "Blues" (que não muda): manter as cores do texto
    texto_por_celula = "imshow(" in src and "limiar" in src
    for antigo, troca in CORES_GUIA.items():
        if texto_por_celula and antigo == "#262626":
            continue
        for aspas in ('"', "'"):
            alvo = f"{aspas}{antigo}{aspas}"
            if alvo in novo:
                SUBSTITUICOES_GUIA.append({"figura": nome, "de": antigo, "para": troca, "vezes": novo.count(alvo)})
                novo = novo.replace(alvo, f"{aspas}{troca}{aspas}")
    # "white" como cor de fundo, borda ou texto sobre cor de destaque -> Grafite;
    # nunca como nome de estilo do seaborn (style="white", lista de estilos)
    def _branco(m):
        antes = novo_ref[max(0, m.start() - 12):m.start()]
        if antes.rstrip().endswith("style=") or "whitegrid" in novo_ref[max(0, m.start() - 30):m.start()]:
            return m.group(0)
        if texto_por_celula and "color=" in antes:
            return m.group(0)
        contagem[0] += 1
        return f"{m.group(1)}{tema.GRAFITE}{m.group(1)}"
    contagem = [0]
    novo_ref = novo
    novo = re.sub(r"([\"'])white\1", _branco, novo)
    if contagem[0]:
        SUBSTITUICOES_GUIA.append({"figura": nome, "de": "white", "para": tema.GRAFITE, "vezes": contagem[0]})
    return PRELUDIO + "\n" + novo


# ------------------------------------------------------------------ renderização trocada
def _codeblock(src, lib):
    import json
    eixos = kit.mapa_eixos(src)
    return bloco_codigo(src, "python", rotulo=f"python · {kit.LIBNOME.get(lib, lib)}",
                        extra_attrs=f" data-axes='{json.dumps(eixos)}'", classe_extra="codeblock")


def _figura(src, nome, alt, lib):
    b64, _ = _kit_run(_codigo_execucao(src, nome), nome)
    arquivo = f"{nome}.webp"
    w, h = salvar_imagem(base64.b64decode(b64), PUBLICO / "img" / "visualizacao" / arquivo)
    return figura(f"/img/visualizacao/{arquivo}", w, h, alt)


def _switcher(nome, variantes, kind="tabs", alt=""):
    sid = kit.uid("sw")
    botoes, panes = [], []
    for i, v in enumerate(variantes):
        sel = "true" if i == 0 else "false"
        lib = v.get("lib", "mpl")
        botoes.append(f'<button type="button" role="tab" id="{sid}-t{i}" aria-controls="{sid}-p{i}" '
                      f'aria-selected="{sel}" tabindex="{0 if i == 0 else -1}" data-i="{i}" data-lib="{lib}">'
                      f'{H.escape(v["label"])}</button>')
        texto = f'<div class="pane-text">{v["texto"]}</div>' if v.get("texto") else ""
        panes.append(f'<div class="pane" role="tabpanel" id="{sid}-p{i}" aria-labelledby="{sid}-t{i}" '
                     f'data-i="{i}" data-lib="{lib}"{"" if i == 0 else " hidden"}>{texto}'
                     f'{kit.duo(v["code"], f"{nome}-{i}", alt + " (" + v["label"] + ")", lib)}</div>')
    nav = ""
    if kind == "steps":
        nav = ('<div class="stepnav"><button type="button" class="botao botao--secundario prev">Anterior</button>'
               '<button type="button" class="botao botao--secundario next">Próximo</button></div>')
    rot = "Variantes" if kind == "tabs" else ("Passos" if kind == "steps" else "Versões")
    return (f'<div class="switch {kind}" id="{sid}"><div class="seg" role="tablist" aria-label="{rot}">'
            f'{"".join(botoes)}</div>{"".join(panes)}{nav}</div>')


kit.codeblock = _codeblock
kit.figura = _figura
kit.switcher = _switcher

import catalogo  # noqa: E402
import fundamentos  # noqa: E402
import referencia  # noqa: E402
import story  # noqa: E402


def _funcoes_build() -> dict:
    """Executa build.py só até a montagem, para obter card_html, catalogo_html, inicio_html etc."""
    fonte = (ORIGEM / "build.py").read_text(encoding="utf-8")
    corte = fonte.index("# ------------------------------------------------------------------ montagem")
    ns = {"__file__": str(ORIGEM / "build.py"), "__name__": "build_guia"}
    exec(compile(fonte[:corte], str(ORIGEM / "build.py"), "exec"), ns)
    return ns


# ------------------------------------------------------------------ montagem (mesma ordem de build.py)
def gerar_partes() -> dict:
    b = _funcoes_build()
    coleta_nav = b["coleta_nav"]
    partes = {}
    partes["inicio"] = coleta_nav(b["inicio_html"])
    partes["fund"] = coleta_nav(fundamentos.html)
    partes["cat"] = coleta_nav(b["catalogo_html"])
    partes["ad"] = coleta_nav(story.antes_depois_html)
    partes["rot"] = coleta_nav(story.roteiro_html)
    partes["err"] = coleta_nav(story.erros_html)
    partes["ref"] = coleta_nav(referencia.html, b["VERSOES"])
    registro = ([x for x in story.REG if x[0].startswith("g-")]
                + [x for x in story.REG if not x[0].startswith("g-")])
    partes["eixos"] = coleta_nav(story.eixos_html, registro)
    saida = {}
    for chave, (conteudo, _) in partes.items():
        saida[chave] = conteudo.replace("{VERSOES}", b["VERSOES"])
    saida["_rodape"] = ('<p>Guia gerado em Python; cada imagem foi produzida pelo código exibido ao lado dela. '
                        'Ideias de storytelling: Cole Nussbaumer Knaflic, <em>Storytelling com Dados</em>.</p>')
    saida["_sit"] = catalogo.SIT
    saida["_avisos"] = list(kit.WARN_LOG)
    saida["_versoes"] = b["VERSOES"]
    saida["_substituicoes"] = SUBSTITUICOES_GUIA
    return saida


AMOSTRAS = {"#A6A6A6": "cinza", "#1F5FA8": "azul", "#D9731A": "laranja"}


def _filtros_catalogo(sit: dict) -> str:
    """Busca e filtros que ficavam na barra lateral do guia, trazidos para o topo do catálogo."""
    bts_sit = "".join(f'<button type="button" class="filtro" data-grupo="sit" data-valor="{k}" aria-pressed="false">{v}</button>'
                      for k, v in sit.items())
    return f'''<div class="filtros-catalogo" data-pagefind-ignore>
  <label class="campo"><span class="campo__rotulo">Buscar gráfico</span>
    <input type="search" id="busca-catalogo" class="campo__entrada" placeholder="Buscar gráfico ou seção" autocomplete="off"></label>
  <div class="filtros" role="group" aria-label="Filtrar catálogo por situação">
    <p class="filtros-rot">Situação</p>
    <button type="button" class="filtro" data-grupo="sit" data-valor="todas" aria-pressed="true">Todas</button>{bts_sit}
  </div>
  <div class="filtros" role="group" aria-label="Filtrar catálogo por biblioteca">
    <p class="filtros-rot">Biblioteca</p>
    <button type="button" class="filtro" data-grupo="lib" data-valor="todas" aria-pressed="true">Todas</button><button type="button" class="filtro" data-grupo="lib" data-valor="mpl" aria-pressed="false">matplotlib</button><button type="button" class="filtro" data-grupo="lib" data-valor="sns" aria-pressed="false">seaborn</button>
  </div>
  <p class="contagem" aria-live="polite"></p>
</div>'''


def pagina(parte_html: str, chave: str, extras: dict) -> dict:
    """Transforma uma <section> do guia em página: título, sobretítulo, corpo."""
    sopa = BeautifulSoup(parte_html, "html.parser")
    sec = sopa.find("section")
    sobre = sec.find("p", class_="sobretitulo")
    sobretitulo = sobre.get_text(strip=True) if sobre else ""
    if sobre:
        sobre.decompose()
    tit = sec.find(["h1", "h2"])
    titulo = tit.get_text(" ", strip=True)
    tit.decompose()
    # hierarquia: h3 -> h2, h4 -> h3 (o título da parte virou o h1 da página)
    for h in sec.find_all(["h3", "h4", "h5"]):
        h.name = {"h3": "h2", "h4": "h3", "h5": "h4"}[h.name]
    for h in sec.find_all("h2"):
        if not h.get("id"):
            pai = h.find_parent(["article", "div"], id=True)
            if pai is not None and pai.find(["h2"]) is h:
                h["data-ancora"] = pai["id"]
    # amostras de cor com estilo inline -> classes com tokens de conteúdo
    for el in sec.find_all(style=True):
        m = re.match(r"background:(#[0-9A-Fa-f]{6})", el["style"])
        if m and m.group(1).upper() in AMOSTRAS:
            el["class"] = (el.get("class") or []) + [f"amostra--{AMOSTRAS[m.group(1).upper()]}"]
            del el["style"]
        else:
            raise ValueError(f"estilo inline inesperado: {el['style']}")
    # tabelas do guia: rótulo acessível na região rolável
    for w in sec.find_all("div", class_="tabela-wrap"):
        w["role"] = "region"
        w["tabindex"] = "0"
        ant = w.find_previous(["h2", "h3"])
        w["aria-label"] = ant.get_text(" ", strip=True) if ant else "Tabela"
    corpo = "".join(str(x) for x in sec.contents)
    if chave == "cat":
        i = corpo.index('<p class="vazio"')
        corpo = corpo[:i] + _filtros_catalogo(extras["_sit"]) + corpo[i:]
    if chave == "inicio":
        corpo += f'<footer class="rodape-guia">{extras["_rodape"]}</footer>'
    return {"titulo": titulo, "sobretitulo": sobretitulo, "html": corpo}
