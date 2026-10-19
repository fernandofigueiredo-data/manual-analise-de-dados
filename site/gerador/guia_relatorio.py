"""Guia do relatório profissional -> páginas do site.

Lê o HTML original, separa as sete seções (início e etapas 1 a 6) e converte a marcação para os
componentes do site. O texto não é alterado.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

from comum import PUBLICO, bloco_codigo, callout, icone, selo

AQUI = Path(__file__).resolve().parent
ORIGEM = AQUI / "origem" / "guia-relatorio-profissional"
DOCX = "modelo_relatorio_dados.docx"

# cores fixas dos gráficos SVG -> classes (os valores ficam em tokens --chart-rel-*)
SVG_CLASSES = {
    "#1F5FAD": "rel-destaque",     # o dado que importa ("em azul", segundo o texto)
    "#B8BFC9": "rel-contexto",     # barras de contexto ("cinza nos demais")
    "#2B2F36": "rel-texto",
    "#5B6470": "rel-texto-sec",
    "#C9CFD8": "rel-eixo",
    "#D9534F": "rel-pizza-1",      # pizza da versão fraca: três cores que competem
    "#E8C547": "rel-pizza-2",
    "#5CB85C": "rel-pizza-3",
}


def _svg(sec) -> None:
    for el in sec.select("svg [fill], svg [stroke]"):
        classes = el.get("class") or []
        for attr, pref in (("fill", "p"), ("stroke", "c")):
            v = el.get(attr)
            if v and v.upper() in SVG_CLASSES:
                classes.append(f"{pref}-{SVG_CLASSES[v.upper()]}")
                del el[attr]
        if classes:
            el["class"] = classes
    for svg in sec.find_all("svg"):
        if svg.get("role") == "img":
            svg["class"] = (svg.get("class") or []) + ["grafico-rel"]


def _botoes(sec) -> None:
    for el in sec.select(".btn"):
        cls = [c for c in el["class"] if c not in ("btn", "btn-ghost", "btn-sm", "dl-link")]
        novo = ["botao"]
        novo.append("botao--fantasma" if "btn-ghost" in el["class"] else "botao--primario")
        if "btn-sm" in el["class"]:
            novo.append("botao--pequeno")
        el["class"] = novo + cls
    for a in sec.select(f'a[href="{DOCX}"]'):
        a["href"] = f"/downloads/{DOCX}"
        svg = a.find("svg")
        if svg:
            svg.replace_with(BeautifulSoup(icone("download"), "html.parser"))


def _selos(sec) -> None:
    for t in sec.select("span.tag"):
        texto = t.get_text(strip=True)
        tipo = "ficticio" if "tag-fict" in (t.get("class") or []) else "complemento"
        t.replace_with(BeautifulSoup(selo(tipo, texto), "html.parser"))


def _callouts(sec) -> None:
    for al in sec.select("div.alerta"):
        t = al.find("p", class_="alerta-t")
        titulo = t.get_text(strip=True)
        t.decompose()
        al.replace_with(BeautifulSoup(callout("atencao", al.decode_contents(), titulo), "html.parser"))
    for c in sec.select("div.callout"):
        c.replace_with(BeautifulSoup(callout("nota", c.decode_contents()), "html.parser"))


def _codigo(sec) -> None:
    for pre in sec.select("pre.code"):
        pre.replace_with(BeautifulSoup(bloco_codigo(pre.get_text(), "python"), "html.parser"))


def _tabelas(sec) -> None:
    for w in sec.select("div.tbl-wrap"):
        w["class"] = ["tabela"]
        w["role"] = "region"
        w["tabindex"] = "0"
        ant = w.find_previous(["h3", "h4", "h5", "p"])
        rot = ant.get_text(" ", strip=True) if ant else "Tabela"
        w["aria-label"] = rot[:120]
        t = w.find("table")
        t["class"] = ["tabela-dados"]
        for th in t.select("thead th"):
            th["scope"] = "col"


def _estilos_inline(sec) -> None:
    for el in sec.find_all(style=True):
        estilo = el["style"].replace(" ", "")
        if el.name == "p" and "fig-title" in (el.get("class") or []) and "font-weight:400" in estilo:
            el["class"].append("fig-title--fraco")
        del el["style"]


def _titulos(sec) -> None:
    # o título da etapa vira o h1 da página; h3 -> h2, h4 -> h3, h5 (achados do relatório-modelo) -> h3
    for h in sec.find_all(["h3", "h4", "h5"]):
        h.name = {"h3": "h2", "h4": "h3", "h5": "h3"}[h.name]


def paginas() -> dict:
    html = (ORIGEM / "guia_relatorio_profissional_dados.html").read_text(encoding="utf-8")
    sopa = BeautifulSoup(html, "html.parser")
    saida = {}
    for sec in sopa.select("main section.etapa"):
        ident = sec["id"]
        sobre = sec.find("p", class_="eyebrow")
        complemento = bool(sobre.find("span", class_="tag"))
        if sobre.find("span"):
            sobre.find("span").decompose()
        sobretitulo = sobre.get_text(" ", strip=True)
        sobre.decompose()
        tit = sec.find(["h1", "h2"])
        titulo = tit.get_text(" ", strip=True)
        tit.decompose()
        _svg(sec)
        _botoes(sec)
        _selos(sec)
        _callouts(sec)
        _codigo(sec)
        _tabelas(sec)
        _estilos_inline(sec)
        _titulos(sec)
        for f in sec.find_all("footer", class_="end"):
            f["class"] = ["rodape-guia"]
        saida[ident] = {"titulo": titulo, "sobretitulo": sobretitulo, "complemento": complemento,
                        "html": sec.decode_contents()}
    return saida


def barra_ferramentas() -> str:
    """Ações que ficavam no rodapé da barra lateral do guia, presentes em todas as suas páginas."""
    return (f'<div class="ferramentas-guia" data-pagefind-ignore>'
            f'<a class="botao botao--secundario botao--pequeno" href="/downloads/{DOCX}" download>{icone("download")}Baixar modelo de relatório (.docx)</a>'
            f'<button class="botao botao--fantasma botao--pequeno" type="button" data-imprimir>{icone("imprimir")}Imprimir ou salvar em PDF</button>'
            f'</div>')


def copiar_downloads() -> None:
    destino = PUBLICO / "downloads"
    destino.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ORIGEM / DOCX, destino / DOCX)
    shutil.copy2(AQUI / "origem" / "Notebook_Mestre_Analise_de_Dados.ipynb",
                 destino / "Notebook_Mestre_Analise_de_Dados.ipynb")
