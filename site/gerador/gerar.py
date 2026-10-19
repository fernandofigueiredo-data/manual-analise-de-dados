"""Gera o conteúdo do site a partir das cópias dos materiais em gerador/origem/ e do estudo de caso.

Uso (a partir de site/):  npm run gerar      ou   gerador/.venv/bin/python gerador/gerar.py [--reexecutar] [--estudo-de-caso]

--reexecutar      executa de novo o notebook mestre (senão usa gerador/cache/)
--estudo-de-caso  baixa os dados da ANAC que faltarem e executa de novo o notebook do estudo de caso

Saídas:
  src/conteudo/paginas/*.json   uma página por arquivo (HTML do corpo, índice, metadados)
  src/conteudo/navegacao.json   módulos, ordem da trilha, dados da página inicial
  public/img/notebook/*.webp    figuras do notebook (executado com o tema do design system)
  public/img/visualizacao/*.webp figuras do guia de visualização (executadas pelo código do guia)
  public/img/estudo-de-caso/*.webp figuras do estudo de caso (notebook em gerador/estudo-de-caso/)
  public/downloads/             modelo .docx e notebook, sem alterações
  gerador/cache/relatorio.json  registro de substituições de cor, avisos e contagens
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

sys.path.insert(0, str(Path(__file__).resolve().parent))

import estrutura  # noqa: E402
import estudo_caso  # noqa: E402
import guia_ml  # noqa: E402
import guia_relatorio  # noqa: E402
import notebook  # noqa: E402
from comum import CONTEUDO, PUBLICO, esc  # noqa: E402

AQUI = Path(__file__).resolve().parent


def limpar_saidas() -> None:
    for pasta in (PUBLICO / "img" / "notebook", PUBLICO / "img" / "visualizacao", PUBLICO / "img" / "estudo-de-caso",
                  CONTEUDO / "paginas"):
        if pasta.exists():
            shutil.rmtree(pasta)
        pasta.mkdir(parents=True)


def texto_simples(html: str, limite: int = 158) -> str:
    t = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    t = re.sub(r"\s+", " ", t)
    if len(t) <= limite:
        return t
    corte = t[:limite].rsplit(" ", 1)[0].rstrip(",;:")
    return corte + "…"


# ------------------------------------------------------------------ links
RX_SECAO = re.compile(r"(Seç(?:ão|ões)\s+)(\d+(?:\.\d+)?(?:(?:,\s*|\s+e\s+|\s+ou\s+)\d+(?:\.\d+)?)*)")
RX_PAREN = re.compile(r"\((\d{1,2}\.\d{1,2})\)")
RX_NUM = re.compile(r"\d+(?:\.\d+)?")


def ligar_secoes(sopa: BeautifulSoup, secoes: dict, slug_atual: str) -> None:
    """'Seção 4.2', 'Seções 6.4 e 12.3' e '(6.1)' viram links para a seção do notebook."""
    def href(num):
        alvo = secoes.get(num)
        if not alvo:
            return None
        slug, ancora = alvo
        if slug == slug_atual:
            return f"#{ancora}" if ancora else "#conteudo"
        return f"/{slug}/" + (f"#{ancora}" if ancora else "")

    for no in list(sopa.find_all(string=True)):
        if no.find_parent(["a", "code", "pre", "h1", "h2", "h3", "h4", "script", "style", "math"]):
            continue
        texto = str(no)
        if "Seç" not in texto and "(" not in texto:
            continue
        novo = esc(texto)
        mudou = False

        def troca_grupo(m):
            nonlocal mudou
            numeros = m.group(2)

            def troca_num(n):
                nonlocal mudou
                h = href(n.group(0))
                if not h:
                    return n.group(0)
                mudou = True
                return f'<a href="{h}">{n.group(0)}</a>'
            return m.group(1) + RX_NUM.sub(troca_num, numeros)

        novo = RX_SECAO.sub(troca_grupo, novo)

        def troca_paren(m):
            nonlocal mudou
            h = href(m.group(1))
            if not h:
                return m.group(0)
            mudou = True
            return f'(<a href="{h}">{m.group(1)}</a>)'
        novo = RX_PAREN.sub(troca_paren, novo)
        if mudou:
            no.replace_with(BeautifulSoup(novo, "html.parser"))


def reescrever_ancoras(sopa: BeautifulSoup, mapa: dict, slug_atual: str, ids_pagina: set) -> None:
    for a in sopa.find_all("a", href=True):
        h = a["href"]
        if not h.startswith("#") or len(h) < 2:
            continue
        alvo = h[1:]
        if alvo in ids_pagina:
            continue
        if alvo not in mapa:
            raise KeyError(f"âncora #{alvo} em {slug_atual} não encontrada")
        slug, nivel_pagina = mapa[alvo]
        if slug == slug_atual:
            a["href"] = "#conteudo"
        else:
            a["href"] = f"/{slug}/" + ("" if nivel_pagina else f"#{alvo}")


def normalizar_titulos(sopa: BeautifulSoup) -> None:
    """Nenhum título pula nível (h1 da página → h2 → h3…): um título que pularia sobe até o nível seguinte
    ao anterior. Acontece no manual de ML, em seções cujo primeiro subtítulo era h4 no original."""
    anterior = 1
    for h in sopa.find_all(["h2", "h3", "h4", "h5"]):
        nivel = int(h.name[1])
        if nivel > anterior + 1:
            nivel = anterior + 1
            h.name = f"h{nivel}"
        anterior = nivel


def indice_da_pagina(sopa: BeautifulSoup) -> list[dict]:
    toc = []
    for h in sopa.find_all(["h2", "h3"]):
        if h.find_parent(class_=["callout", "paper", "check", "fold"]) or h.find_parent(attrs={"hidden": True}):
            continue
        ident = h.get("id") or h.get("data-ancora")
        if not ident:
            pai = h.find_parent(["div", "article", "section"], id=True)
            if pai is not None and pai.find(["h2", "h3"]) is h:
                ident = pai["id"]
                h["data-ancora"] = ident
        if not ident:
            continue
        copia = BeautifulSoup(str(h), "html.parser")
        for s in copia.select(".selo, .sr-only"):
            s.decompose()
        texto = copia.get_text(" ", strip=True) or h.get_text(" ", strip=True)   # título que é só uma etiqueta
        toc.append({"id": ident, "texto": texto, "nivel": int(h.name[1])})
    return toc


def readme_html(caminho: Path) -> str:
    """README dos pacotes de origem, com títulos rebaixados dois níveis (entram sob 'Materiais de origem')."""
    html = notebook.MD.render(caminho.read_text(encoding="utf-8"))
    sopa = BeautifulSoup(html, "html.parser")
    for h in sopa.find_all(["h1", "h2", "h3"]):
        h.name = {"h1": "h3", "h2": "h4", "h3": "h5"}[h.name]
    for t in sopa.find_all("table"):
        t["class"] = ["tabela-dados"]
        t.wrap(BeautifulSoup('<div class="tabela" role="region" tabindex="0" aria-label="Arquivos do pacote"></div>', "html.parser").div)
    return str(sopa)


FERRAMENTAS_CARTOES = ('<div class="ferramentas-guia" data-pagefind-ignore>'
                       '<button type="button" class="botao botao--secundario botao--pequeno" data-expandir title="Expandir todos os cards">Expandir</button>'
                       '<button type="button" class="botao botao--secundario botao--pequeno" data-recolher title="Recolher todos os cards">Recolher</button></div>')


def montar_ml(p: dict, secoes: dict, d: dict, pagina_do_grupo: dict) -> dict:
    parte = p["parte"]
    if parte == "skill":
        info = guia_ml.pagina_skill()
        return {"titulo": info["titulo"], "sobretitulo": "Skill de decisão · Machine Learning", "html": info["html"], "recursos": []}
    if parte == "auditoria":
        info = guia_ml.pagina_auditoria()
        return {"titulo": info["titulo"], "sobretitulo": "Auditoria técnica · Machine Learning", "html": info["html"], "recursos": []}
    if parte == "inicio":
        ini, uso = secoes["inicio"], secoes["comousar"]
        html = ini["html"].replace('<div class="legend" id="legend"></div>',
                                   f'<div class="legend filtros" id="legend" role="group" aria-label="Filtrar modelos por categoria">{guia_ml.legenda_e_indice(d)}</div>')
        html += guia_ml.indice_modelos(d, pagina_do_grupo)
        html += f'<h2 id="comousar">{uso["titulo"]}</h2>' + uso["html"]
        return {"titulo": ini["titulo"], "sobretitulo": "Manual de Machine Learning · v1.0 · set/2026",
                "html": html, "recursos": ["ml"]}
    sec = secoes[parte]
    num = parte[1:] if parte.startswith("s") else ""
    titulo = f"{num}. {sec['titulo']}" if num else sec["titulo"]
    html = sec["html"]
    if parte == "diagnostico":
        # o script do diagnóstico só roda dentro do contêiner #diagnostico (a seção original)
        html = '<div id="diagnostico">' + guia_ml.diagnostico_ajustes(html) + '</div>'
    tem_cartoes = 'class="modelo"' in html
    if tem_cartoes:
        html = FERRAMENTAS_CARTOES + html
    sobre = "Manual de Machine Learning · " + p["grupo"] + (f" · {sec['sobretitulo'].title()}" if parte == "diagnostico" else "")
    tags = [d["CATS"][t] for t in sec["tags"] if t in d["CATS"]]
    return {"titulo": titulo, "sobretitulo": sobre, "html": html, "tags": tags,
            "recursos": ["ml"] + (["diagnostico"] if parte == "diagnostico" else [])}


# ------------------------------------------------------------------ principal
def main() -> None:
    reexecutar = "--reexecutar" in sys.argv
    limpar_saidas()

    print("1/6 notebook: executando…")
    nb = notebook.executar(forcar=reexecutar)
    abertura = notebook.cabecalho_abertura(nb)
    indice = notebook.indice_secoes(nb)
    figs_nb = [0]

    print("2/6 guia de visualização: executando os exemplos…")
    import guia_viz  # importa aqui: executa o kit do guia
    partes_viz = guia_viz.gerar_partes()

    print("3/6 guia de relatório…")
    partes_rel = guia_relatorio.paginas()
    guia_relatorio.copiar_downloads()

    print("4/6 manual de machine learning…")
    dados_ml = guia_ml.dados()
    secoes_ml = guia_ml.secoes(dados_ml)
    guia_ml.gerar_scripts()
    guia_ml.copiar_downloads()
    pagina_do_grupo = {}                     # grupo de modelos -> página que tem os cartões
    for p in estrutura.PAGINAS:
        if p["tipo"] != "ml" or p["parte"] not in secoes_ml:
            continue
        for m in dados_ml["MODELS"]:
            if f'id="m-{m["id"]}"' in secoes_ml[p["parte"]]["html"]:
                pagina_do_grupo[m["grupo"]] = p["slug"]

    caso = "--estudo-de-caso" in sys.argv     # baixa ~1 GB da ANAC na primeira vez: só quando pedido
    print("5/6 estudo de caso (ANAC)" + (": baixando os dados e executando…" if caso else ": notebook já executado…"))
    nb_caso = estudo_caso.executar(forcar=caso)
    estudo_caso.copiar_downloads()
    figs_caso = [0]

    print("6/6 montando páginas…")
    paginas = []
    for p in estrutura.PAGINAS:
        pg = dict(p)
        if p["tipo"] == "nb":
            pg["html"] = notebook.renderizar_pagina(nb, p, figs_nb)
            pg["sobretitulo"] = "Notebook mestre"
            pg["recursos"] = []
        elif p["tipo"] == "viz":
            info = guia_viz.pagina(partes_viz[p["parte"]], p["parte"], partes_viz)
            pg.update(titulo=info["titulo"], sobretitulo=info["sobretitulo"] or "Guia matplotlib e seaborn",
                      html=info["html"], recursos=["viz"] + (["catalogo"] if p["parte"] == "cat" else []))
        elif p["tipo"] == "ml":
            pg.update(montar_ml(p, secoes_ml, dados_ml, pagina_do_grupo))
        elif p["tipo"] == "caso":
            pg["html"] = estudo_caso.renderizar_pagina(nb_caso, p, figs_caso)
            pg["sobretitulo"] = "Estudo de caso · dados abertos da ANAC"
            pg["recursos"] = []
        else:
            info = partes_rel[p["parte"]]
            pg.update(titulo=info["titulo"], sobretitulo=info["sobretitulo"] or "Guia do relatório",
                      html=guia_relatorio.barra_ferramentas() + info["html"], recursos=["rel"],
                      complemento=info["complemento"])
        paginas.append(pg)

    # mapa de seções do notebook: número -> (slug, âncora)
    secoes = {}
    for pg in paginas:
        if pg["tipo"] != "nb":
            continue
        if pg.get("secao") and pg["secao"] not in secoes and "." not in pg["secao"]:
            secoes[pg["secao"]] = (pg["slug"], None)
        for m in re.finditer(r'id="secao-([\d-]+)"', pg["html"]):
            num = m.group(1).replace("-", ".")
            secoes.setdefault(num, (pg["slug"], f"secao-{m.group(1)}"))

    # mapas de âncoras por material (para links internos dos guias)
    mapas = {"viz": {}, "rel": {}, "nb": {}, "ml": {}, "caso": {}}
    for pg in paginas:
        mapa = mapas[pg["tipo"]]
        for ident in re.findall(r'\sid="([^"]+)"', pg["html"]):
            mapa.setdefault(ident, (pg["slug"], False))
        chave = pg.get("parte")
        if pg["tipo"] == "viz":
            ids_sec = {"inicio": "inicio", "fund": "fundamentos", "cat": "catalogo", "ad": "antes-depois",
                       "rot": "roteiro", "err": "erros", "ref": "referencia", "eixos": "eixos"}
            mapa[ids_sec[chave]] = (pg["slug"], True)
        elif pg["tipo"] == "rel":
            mapa[chave] = (pg["slug"], True)
        elif pg["tipo"] == "ml":
            mapa[chave] = (pg["slug"], True)
            if chave == "inicio":
                mapa["comousar"] = (pg["slug"], False)

    perguntas = {l["numero"]: l["pergunta"] for l in indice}
    sobre = {"readme_viz": readme_html(AQUI / "origem" / "guia-matplotlib-seaborn" / "README.md"),
             "readme_rel": readme_html(AQUI / "origem" / "guia-relatorio-profissional" / "README.md"),
             "readme_ml": guia_ml.readme_html(),
             "notebooks_ml": guia_ml.lista_notebooks(dados_ml, pagina_do_grupo)}
    total_codigos = total_tabelas = 0
    for pg in paginas:
        sopa = BeautifulSoup(pg["html"], "html.parser")
        ids = {t["id"] for t in sopa.find_all(id=True)}
        if pg["tipo"] == "nb":
            ligar_secoes(sopa, secoes, pg["slug"])
        reescrever_ancoras(sopa, mapas[pg["tipo"]], pg["slug"], ids)
        normalizar_titulos(sopa)
        pg["toc"] = indice_da_pagina(sopa)
        pg["html"] = str(sopa)
        total_codigos += len(sopa.select("div.codigo"))
        total_tabelas += len(sopa.select("table"))
        if pg["tipo"] == "nb" and pg.get("secao") in perguntas:
            pg["descricao"] = perguntas[pg["secao"]]
        else:
            lead = sopa.find("p", class_="lead") or sopa.find("p")
            pg["descricao"] = texto_simples(str(lead))
        if pg["slug"] == "comecar/como-usar":
            pg["descricao"] = "Formato dos tópicos, convenções do template e tabelas usadas como exemplo em todo o manual."

    # índice do notebook (célula 1) com links para as páginas
    linhas_indice = []
    for l in indice:
        alvo = secoes.get(l["numero"])
        linhas_indice.append({**l, "url": f"/{alvo[0]}/" if alvo else None})

    figs_viz = len(list((PUBLICO / "img" / "visualizacao").glob("*.webp")))
    nav = {
        "modulos": [{**m, "paginas": [pg["slug"] for pg in paginas if pg["modulo"] == m["id"]]}
                    for m in estrutura.MODULOS],
        "abertura": abertura,
        "indice": linhas_indice,
        "estatisticas": {
            "paginas": len(paginas),
            "figuras": figs_nb[0] + figs_viz + figs_caso[0],
            "codigos": total_codigos,
            "tabelas": total_tabelas,
        },
        "versoes_guia": partes_viz["_versoes"],
        "sobre": sobre,
    }
    for pg in paginas:
        dados = {k: pg.get(k) for k in ("slug", "modulo", "tipo", "titulo", "nav", "sobretitulo", "descricao",
                                         "origem", "html", "toc", "recursos", "complemento", "grupo", "tags")}
        dados["origem"] = {"material": pg["origem"][0], "trecho": pg["origem"][1]}
        destino = CONTEUDO / "paginas" / (pg["slug"].replace("/", "__") + ".json")
        destino.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    (CONTEUDO / "navegacao.json").write_text(json.dumps(nav, ensure_ascii=False, indent=1), encoding="utf-8")

    relatorio = {"substituicoes_de_cor": notebook.SUBSTITUICOES,
                 "substituicoes_de_cor_guia_viz": partes_viz.get("_substituicoes", []), "avisos_guia_viz": partes_viz["_avisos"],
                 "estatisticas": nav["estatisticas"], "figuras_notebook": figs_nb[0], "figuras_guia": figs_viz,
                 "figuras_estudo_de_caso": figs_caso[0]}
    (AQUI / "cache").mkdir(exist_ok=True)
    (AQUI / "cache" / "relatorio.json").write_text(json.dumps(relatorio, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(nav["estatisticas"], ensure_ascii=False), "| figuras notebook:", figs_nb[0], "| guia:", figs_viz)
    if partes_viz["_avisos"]:
        print("avisos do guia:", *partes_viz["_avisos"], sep="\n  ")


if __name__ == "__main__":
    main()
