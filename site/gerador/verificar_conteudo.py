"""Confere se todo o texto e todo o código dos três materiais de origem estão no site gerado.

Compara, trecho a trecho, o texto normalizado de cada unidade de origem (célula do notebook,
parágrafo/item/célula de tabela dos guias, bloco de código) com o texto do HTML gerado em dist/.
Uso (a partir de site/, depois do build):  gerador/.venv/bin/python gerador/verificar_conteudo.py
Grava o resultado em ../docs/qualidade/verificacao-conteudo.json e sai com código 1 se faltar algo.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import nbformat
from bs4 import BeautifulSoup

import notebook

AQUI = Path(__file__).resolve().parent
DIST = AQUI.parent / "dist"
DOCS = AQUI.parent.parent / "docs" / "qualidade"


def norm(t: str) -> str:
    t = unicodedata.normalize("NFC", t)
    t = t.replace(" ", " ").replace("’", "'").replace("“", '"').replace("”", '"')
    for marca in ("⚠️", "🔹", "➕", "📘", "⚠"):
        t = t.replace(marca, " ")
    return re.sub(r"\s+", " ", t).strip()


def texto_site() -> str:
    partes = []
    for f in DIST.rglob("index.html"):
        if "pagefind" in f.parts:
            continue
        sopa = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
        for el in sopa.select("script, style, .lateral, .toc, .toc-movel"):
            el.decompose()
        # linhas de código separadas por quebra, como no original
        for ln in sopa.select(".ln"):
            ln.append("\n")
        partes.append(sopa.get_text(" "))
    return norm(" ".join(partes))


def trechos_markdown(fonte: str) -> list[str]:
    """Divide o Markdown em frases curtas comparáveis (sem a marcação)."""
    html = notebook.MD.render(fonte)
    sopa = BeautifulSoup(html, "html.parser")
    for m in sopa.select("math"):
        m.replace_with(" | ")          # fórmulas viram MathML: compara o texto antes e depois delas
    saida = []
    for el in sopa.find_all(["p", "li", "td", "th", "h1", "h2", "h3", "h4", "blockquote"]):
        if el.find(["p", "li", "ul", "ol"]):
            continue
        t = el.get_text(" ")
        for marca in ("➕", "🔹"):                  # viram selo ou ícone no site: separam o trecho
            t = t.replace(marca, " | ")
        t = norm(t)
        for frase in re.split(r"(?<=[.:;!?])\s+|\s*\|\s*", t):
            frase = frase.strip(" -*")
            if len(frase) >= 12:
                saida.append(frase)
    for pre in sopa.find_all("code"):
        if pre.parent.name == "pre":
            saida.extend(l.strip() for l in pre.get_text().splitlines() if len(l.strip()) >= 8)
    return saida


def presente(trecho: str, site: str, site_sem_espaco: str) -> bool:
    t = norm(trecho)
    if t in site:
        return True
    return re.sub(r"\s+", "", t) in site_sem_espaco


def main() -> None:
    site = texto_site()
    site_sem_espaco = re.sub(r"\s+", "", site)
    faltas: dict[str, list] = {"notebook": [], "guia_visualizacao": [], "guia_relatorio": [], "manual_ml": []}
    totais = {"notebook": 0, "guia_visualizacao": 0, "guia_relatorio": 0, "manual_ml": 0}

    # ---------------- notebook: todas as células
    nb = nbformat.read(notebook.ORIGEM, as_version=4)
    for i, c in enumerate(nb.cells):
        if c.cell_type == "code":
            unidades = [l.strip() for l in c.source.splitlines() if len(l.strip()) >= 4]
        else:
            unidades = trechos_markdown(c.source)
        for u in unidades:
            totais["notebook"] += 1
            if not presente(u, site, site_sem_espaco):
                faltas["notebook"].append({"celula": i, "trecho": u[:160]})

    # ---------------- guias: texto de cada elemento folha e cada linha de código
    def verificar_html(caminho: Path, chave: str, seletor_raiz: str):
        sopa = BeautifulSoup(caminho.read_text(encoding="utf-8"), "html.parser")
        raiz = sopa.select_one(seletor_raiz)
        for el in raiz.select("script, style, nav, .lateral, aside.sidebar, .mobile-top, .side-bottom, svg, .sec-head h2 span.tag"):
            el.decompose()          # etiquetas no título da seção viram selos à parte no site
        unidades = []
        for el in raiz.find_all(["p", "li", "td", "th", "h1", "h2", "h3", "h4", "h5", "summary", "blockquote", "label", "span", "figcaption", "button", "option"]):
            if el.find(["p", "li", "ul", "ol", "table", "div"]):
                continue
            t = norm(el.get_text(" "))
            if len(t) >= 12:
                unidades.append(t)
        for pre in raiz.find_all("pre"):
            unidades.extend(l.strip() for l in pre.get_text().splitlines() if len(l.strip()) >= 8)
        for u in dict.fromkeys(unidades):
            totais[chave] += 1
            if not presente(u, site, site_sem_espaco):
                faltas[chave].append({"trecho": u[:160]})

    verificar_html(AQUI / "origem" / "guia-matplotlib-seaborn" / "guia_matplotlib_seaborn.html", "guia_visualizacao", "main")
    verificar_html(AQUI / "origem" / "guia-relatorio-profissional" / "guia_relatorio_profissional_dados.html", "guia_relatorio", "main")

    # ---------------- manual de ML: HTML estático, dados dos 43 cartões e da matriz, skill, auditoria, scripts
    ml = AQUI / "origem" / "data-science-htlm"
    verificar_html(ml / "manual_machine_learning.html", "manual_ml", "main")
    import guia_ml
    d = guia_ml.dados()

    def conferir(chave, texto_html):
        t = norm(BeautifulSoup(texto_html, "html.parser").get_text(" "))
        for frase in re.split(r"(?<=[.:;!?·])\s+", t):
            frase = frase.strip()
            if len(frase) >= 12:
                totais[chave] += 1
                if not presente(frase, site, site_sem_espaco):
                    faltas[chave].append({"trecho": frase[:160]})
    for m in d["MODELS"]:
        for k, v in m.items():
            if k in ("id", "grupo", "tags"):
                continue
            if k == "cod":
                for ln in v.splitlines():
                    if len(ln.strip()) >= 8:
                        totais["manual_ml"] += 1
                        if not presente(ln.strip(), site, site_sem_espaco):
                            faltas["manual_ml"].append({"modelo": m["id"], "trecho": ln.strip()[:160]})
            else:
                conferir("manual_ml", str(v))
    for x in d["MATRIZ"].values():
        for v in x.values():
            conferir("manual_ml", str(v))
    for nome in ("skill_decisao_ml.md", "auditoria_ml.md", "README.md"):
        fonte = (ml / nome).read_text(encoding="utf-8")
        fm = re.match(r"^---\n(.*?)\n---\n", fonte, re.S)
        if fm:                      # cabeçalho YAML: vira a tabela "Metadados da skill"
            for ln in fm.group(1).splitlines():
                valor = ln.partition(":")[2].strip()
                totais["manual_ml"] += 1
                if not presente(valor, site, site_sem_espaco):
                    faltas["manual_ml"].append({"arquivo": nome, "trecho": valor[:160]})
            fonte = fonte[fm.end():]
        for u in trechos_markdown(fonte):
            totais["manual_ml"] += 1
            if not presente(u, site, site_sem_espaco):
                faltas["manual_ml"].append({"arquivo": nome, "trecho": u[:160]})
    for f in sorted((ml / "auditoria").iterdir()):
        for ln in f.read_text(encoding="utf-8").splitlines():
            if len(ln.strip()) >= 8:
                totais["manual_ml"] += 1
                if not presente(ln.strip(), site, site_sem_espaco):
                    faltas["manual_ml"].append({"arquivo": f.name, "trecho": ln.strip()[:160]})

    resultado = {"totais": totais, "ausentes": {k: len(v) for k, v in faltas.items()}, "detalhes": faltas}
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "verificacao-conteudo.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    for k in totais:
        print(f"{k}: {totais[k] - len(faltas[k])}/{totais[k]} trechos encontrados")
        for f in faltas[k][:40]:
            print("   faltando:", f)
    sys.exit(1 if any(faltas.values()) else 0)


if __name__ == "__main__":
    main()
