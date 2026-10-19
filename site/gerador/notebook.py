"""Notebook mestre -> páginas do site.

1. Executa uma cópia do notebook com o tema do design system (célula oculta após a 1.2) e
   com as cores fixadas no código trocadas pelas equivalentes do tema. O código exibido no
   site é sempre o original.
2. Converte cada célula: Markdown em HTML (tabelas, fórmulas em MathML, callouts) e código
   em bloco realçado seguido das saídas (texto, tabela, figura).
"""
from __future__ import annotations

import base64
import copy
import json
import os
import re
import tempfile
from pathlib import Path

import nbformat
from bs4 import BeautifulSoup, NavigableString
from latex2mathml.converter import convert as latex_para_mathml
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from nbclient import NotebookClient

import tema
from alt_notebook import ALT
from comum import (PUBLICO, bloco_codigo, callout, esc, figura, icone, salvar_imagem, selo, slug, tabela)

AQUI = Path(__file__).resolve().parent
ORIGEM = AQUI / "origem" / "Notebook_Mestre_Analise_de_Dados.ipynb"
CACHE = AQUI / "cache" / "notebook_executado.ipynb"
CELULA_APOS_TEMA = 7          # 1.2 Opções de exibição e estilo dos gráficos

SUBSTITUICOES: list[dict] = []   # registro das trocas de cor feitas na execução


# ------------------------------------------------------------------ execução
def _codigo_execucao(i: int, fonte: str) -> str:
    novo = fonte
    for antigo, troca in {**tema.EQUIVALENCIAS_PALETA, **tema.EQUIVALENCIAS}.items():
        if antigo in novo:
            SUBSTITUICOES.append({"celula": i, "de": antigo, "para": troca, "vezes": novo.count(antigo)})
            novo = novo.replace(antigo, troca)
    return novo


def executar(forcar: bool = False) -> nbformat.NotebookNode:
    """Executa o notebook (ou lê do cache) e devolve o notebook executado, alinhado ao original."""
    original = nbformat.read(ORIGEM, as_version=4)
    if CACHE.exists() and not forcar and CACHE.stat().st_mtime > ORIGEM.stat().st_mtime:
        executado = nbformat.read(CACHE, as_version=4)
        for i, c in enumerate(original.cells):
            if c.cell_type == "code":
                _codigo_execucao(i, c.source)     # repovoa o registro de substituições
        return executado

    nb = copy.deepcopy(original)
    for i, c in enumerate(nb.cells):
        c.metadata["indice_original"] = i
        if c.cell_type == "code":
            c.source = _codigo_execucao(i, c.source)
    oculta = nbformat.v4.new_code_cell(tema.CELULA_TEMA)
    oculta.metadata["indice_original"] = None
    nb.cells.insert(CELULA_APOS_TEMA + 1, oculta)

    env_kernel = AQUI / ".venv" / "share" / "jupyter"
    os.environ["JUPYTER_PATH"] = str(env_kernel) + os.pathsep + os.environ.get("JUPYTER_PATH", "")
    with tempfile.TemporaryDirectory() as pasta:
        cliente = NotebookClient(nb, timeout=600, kernel_name="analise-de-dados", allow_errors=False,
                                 resources={"metadata": {"path": pasta}})
        cliente.execute()
    nb.cells = [c for c in nb.cells if c.metadata.get("indice_original") is not None]
    assert len(nb.cells) == len(original.cells)
    CACHE.parent.mkdir(exist_ok=True)
    nbformat.write(nb, CACHE)
    return nb


# ------------------------------------------------------------------ Markdown
def _math(self, tokens, idx, options, env):
    return latex_para_mathml(tokens[idx].content.strip())


def _math_bloco(self, tokens, idx, options, env):
    return latex_para_mathml(tokens[idx].content.strip(), display="block")


def _fence(self, tokens, idx, options, env):
    tok = tokens[idx]
    lang = (tok.info or "").strip().split()[0] if tok.info else "text"
    if lang in ("python", "sql"):
        return bloco_codigo(tok.content, lang)
    return bloco_codigo(tok.content, "text", rotulo="bash" if lang in ("bash", "sh") else "texto")


MD = (MarkdownIt("commonmark", {"html": False})
      .enable("table")
      .use(dollarmath_plugin, allow_space=True, allow_digits=False, double_inline=True)
      .use(tasklists_plugin, enabled=True, label=True))
MD.add_render_rule("math_inline", _math)
MD.add_render_rule("math_block", _math_bloco)
MD.add_render_rule("fence", _fence)
MD.add_render_rule("code_block", _fence)

MARCA_ATENCAO = "⚠️"
MARCA_ALT = "🔹"
MARCA_COMPL = "➕"


def _id_titulo(texto: str, usados: set[str]) -> str:
    m = re.match(r"^(\d+(?:\.\d+)?)\.?\s", texto)
    base = "secao-" + m.group(1).replace(".", "-") if m else slug(texto)
    ident, n = base, 2
    while ident in usados:
        ident, n = f"{base}-{n}", n + 1
    usados.add(ident)
    return ident


def _marcador(tipo: str, rotulo: str, titulo: str, so_icone: bool) -> str:
    if so_icone:
        return (f'<span class="marcador marcador--{tipo}" title="{titulo}">'
                f'{icone("complemento" if tipo == "complemento" else "alternativa")}</span>')
    return selo(tipo, rotulo, titulo)


def _substituir_marcas_inline(sopa: BeautifulSoup) -> None:
    """➕ e 🔹 viram selos (ou só o ícone, quando o texto seguinte já diz 'Complemento'/'Alternativa');
    o 📘 do título é removido."""
    marcas = {MARCA_COMPL: ("complemento", "Complemento", "Técnica que não estava no material de estudo original"),
              MARCA_ALT: ("alternativa", "Alternativa", "Outra forma válida de fazer a mesma tarefa")}
    for no in list(sopa.find_all(string=True)):
        if no.find_parent(["code", "pre"]):
            continue
        texto = str(no)
        if not any(m in texto for m in (*marcas, "📘")):
            continue
        texto = texto.replace("📘", "")
        partes = re.split(f"({MARCA_COMPL}|{MARCA_ALT})", texto)
        html = []
        for j, parte in enumerate(partes):
            if parte in marcas:
                tipo, rotulo, titulo = marcas[parte]
                depois = "".join(partes[j + 1:]).strip()
                if not depois and no.next_sibling is not None:
                    depois = (no.next_sibling.get_text() if hasattr(no.next_sibling, "get_text")
                              else str(no.next_sibling)).strip()
                html.append(_marcador(tipo, rotulo, titulo, depois.startswith(rotulo)))
            else:
                html.append(esc(parte))
        no.replace_with(BeautifulSoup("".join(html).strip(), "html.parser"))


def _callouts(sopa: BeautifulSoup) -> None:
    """Parágrafos que começam com ⚠️ ou 🔹 viram callouts, levando listas e códigos seguintes."""
    for p in list(sopa.find_all("p", recursive=False)):
        texto = p.get_text()
        if texto.startswith(MARCA_ATENCAO):
            tipo, marca = "atencao", MARCA_ATENCAO
        elif texto.startswith(MARCA_ALT):
            tipo, marca = "alternativa", MARCA_ALT
        else:
            continue
        primeiro = p.find(string=True)
        primeiro.replace_with(str(primeiro).replace(marca, "", 1).lstrip())
        seguintes = []
        no = p.next_sibling
        while no is not None:
            if isinstance(no, NavigableString):
                if no.strip():
                    break
                no = no.next_sibling
                continue
            if no.name in ("ul", "ol") or (no.name == "div" and "codigo" in (no.get("class") or [])):
                seguintes.append(no)
                no = no.next_sibling
                continue
            break
        corpo = "".join(str(x) for x in [p] + seguintes)
        p.insert_before(BeautifulSoup(callout(tipo, corpo), "html.parser"))
        for x in [p] + seguintes:
            x.extract()


def _callouts_observar(html: str) -> str:
    """'⚠️ **O que observar**' seguido de lista: trata antes do BeautifulSoup geral."""
    padrao = re.compile(r"<p>⚠️ <strong>([^<]+)</strong></p>\s*(<ul>.*?</ul>|<ol>.*?</ol>)", re.S)
    return padrao.sub(lambda m: callout("atencao", m.group(2), m.group(1)), html)


def markdown_para_html(fonte: str, usados: set[str]) -> str:
    html = MD.render(fonte)
    html = _callouts_observar(html)
    sopa = BeautifulSoup(html, "html.parser")
    _callouts(sopa)
    _substituir_marcas_inline(sopa)
    for h in sopa.find_all(["h1", "h2", "h3", "h4"]):
        h["id"] = _id_titulo(h.get_text(" ", strip=True), usados)
    for t in sopa.find_all("table"):
        if t.find_parent("div", class_="tabela"):
            continue
        anterior = t.find_previous(["h2", "h3", "strong"])
        rot = anterior.get_text(" ", strip=True) if anterior else "Tabela"
        t.wrap(BeautifulSoup(tabela("", rot), "html.parser").div)
    for blockquote in sopa.find_all("blockquote"):
        blockquote["class"] = ["destaque"]
    return str(sopa)


# ------------------------------------------------------------------ saídas
NUMERO = re.compile(r"^[-+−]?[\d.,]+%?$|^NaN$|^<NA>$|^None$|^(True|False)$")


def _tabela_dataframe(html: str, rotulo: str) -> str:
    sopa = BeautifulSoup(html, "html.parser")
    for st in sopa.find_all("style"):
        st.decompose()
    t = sopa.find("table")
    for attr in ("border", "class", "style"):
        t.attrs.pop(attr, None)
    t["class"] = ["tabela-dados"]
    for el in t.find_all(True):
        el.attrs.pop("style", None)
        el.attrs.pop("halign", None)
        if el.name in ("td", "th") and NUMERO.match(el.get_text(strip=True) or "x"):
            el["class"] = ["num"]
    for th in t.select("thead th"):
        th["scope"] = "col"
    for th in t.select("tbody th"):
        th["scope"] = "row"
    return tabela(str(t), rotulo)


def _saidas(i: int, celula, pagina_img: str, contador: list[int]) -> str:
    partes = []
    n_fig = 0
    for o in celula.get("outputs", []):
        if o.output_type == "stream":
            if o.name == "stderr":
                raise RuntimeError(f"Célula {i} escreveu em stderr: {o.text[:300]}")
            partes.append(f'<pre class="saida__texto" tabindex="0">{esc(o.text.rstrip())}</pre>')
        elif o.output_type in ("execute_result", "display_data"):
            dados = o.get("data", {})
            if "image/png" in dados:
                chave = (i, n_fig)
                if chave not in ALT:
                    raise KeyError(f"Falta texto alternativo para a figura {chave}")
                n_fig += 1
                contador[0] += 1
                nome = f"celula-{i:03d}" + (f"-{n_fig}" if n_fig > 1 else "") + ".webp"
                destino = PUBLICO / "img" / "notebook" / nome
                w, h = salvar_imagem(base64.b64decode(dados["image/png"]), destino)
                partes.append(figura(f"/img/notebook/{nome}", w, h, ALT[chave]))
            elif "text/html" in dados:
                partes.append(_tabela_dataframe(dados["text/html"], "Saída em tabela"))
            elif "text/plain" in dados:
                partes.append(f'<pre class="saida__texto" tabindex="0">{esc(dados["text/plain"])}</pre>')
        elif o.output_type == "error":
            raise RuntimeError(f"Erro na célula {i}: {o.ename}: {o.evalue}")
    if not partes:
        return ""
    return ('<div class="saida" data-pagefind-ignore><p class="saida__rotulo">Saída</p>'
            + "".join(partes) + "</div>")


# ------------------------------------------------------------------ páginas
def cabecalho_abertura(nb) -> dict:
    """Título, subtítulo e pergunta de abertura da célula 0 (vão para a página inicial)."""
    fonte = nb.cells[0].source
    antes, _, _ = fonte.partition("Cada tópico segue o formato:")
    titulo = re.search(r"^# (.+)$", antes, re.M).group(1).replace("📘", "").strip()
    subtitulo = re.search(r"^### (.+)$", antes, re.M).group(1).strip()
    citacao = re.search(r"^> (.+)$", antes, re.M).group(1).strip()
    return {"titulo": titulo, "subtitulo": subtitulo,
            "citacao_html": MD.renderInline(citacao)}


def indice_secoes(nb) -> list[dict]:
    """Linhas da tabela do índice (célula 1): número, seção, pergunta."""
    linhas = []
    for ln in nb.cells[1].source.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", ln)
        if m:
            linhas.append({"numero": m.group(1), "secao": m.group(2), "pergunta": m.group(3)})
    return linhas


ORIGINAL = nbformat.read(ORIGEM, as_version=4)


def renderizar_pagina(nb, pagina: dict, contador_fig: list[int]) -> str:
    """nb = notebook executado (fonte das saídas); texto e código vêm sempre do original."""
    ini, fim = pagina["celulas"]
    usados: set[str] = set()
    partes = []
    for i in range(ini, fim + 1):
        c = ORIGINAL.cells[i]
        if c.cell_type == "markdown":
            fonte = c.source
            if i == 0:
                fonte = "Cada tópico segue o formato:" + fonte.partition("Cada tópico segue o formato:")[2]
            fonte = re.sub(r"^---\s*$", "", fonte, flags=re.M)            # separadores de seção
            fonte = re.sub(r"^# \d+\. .+$", "", fonte, count=1, flags=re.M)  # título da seção -> h1 da página
            if pagina["slug"] == "comecar/roteiro-rapido":
                fonte = re.sub(r"^## .+$", "", fonte, count=1, flags=re.M)  # idem para a seção 0 (marcada com ##)
            partes.append(markdown_para_html(fonte, usados))
        else:
            partes.append(bloco_codigo(c.source, "python"))
            partes.append(_saidas(i, nb.cells[i], pagina["slug"], contador_fig))
    return "\n".join(p for p in partes if p)
