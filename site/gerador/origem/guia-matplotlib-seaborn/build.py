"""Monta o arquivo guia_matplotlib_seaborn.html.

Uso: python build.py (o HTML é gravado na mesma pasta deste script).
"""
import html as H
import platform
import sys
import unicodedata
from pathlib import Path

import matplotlib
import numpy
import pandas
import seaborn

import kit
import catalogo
import fundamentos
import story
import referencia

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "guia_matplotlib_seaborn.html"

VERSOES = (f"Python {platform.python_version()}, matplotlib {matplotlib.__version__}, "
           f"seaborn {seaborn.__version__}, pandas {pandas.__version__} e NumPy {numpy.__version__}")


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn").lower()


def coleta_nav(fn, *a):
    inicio = len(kit.NAV)
    conteudo = fn(*a)
    itens = kit.NAV[inicio:]
    del kit.NAV[inicio:]
    return conteudo, itens


# ------------------------------------------------------------------ catálogo
def card_html(c):
    libs = sorted({v["lib"] for v in c["variantes"]})
    eixos = set()
    for v in c["variantes"]:
        eixos |= set(kit.mapa_eixos(v["code"]))
    ordem = [e for e in kit.EIXOS if e in eixos]
    story.REG.append((c["id"], c["titulo"], eixos))
    sit = "".join(f'<span class="tag">{catalogo.SIT[s]}</span>' for s in c["sit"])
    lib = "".join(f'<span class="tag lib">{kit.LIBNOME[l]}</span>' for l in libs)
    escolha = "".join(f"<li>{x}</li>" for x in c["escolha"])
    evite = "".join(f"<li>{x}</li>" for x in c["evite"])
    notas = "".join(f'<p>{kit.k(t) if tipo == "k" else kit.r(t)}</p>' for tipo, t in c["nota"])
    base = f'<p class="base">Base: {c["base"]}</p>' if c.get("base") else ""
    busca = sem_acento(" ".join([c["titulo"], c["objetivo"], " ".join(c["escolha"]),
                                 " ".join(catalogo.SIT[s] for s in c["sit"]), " ".join(kit.LIBNOME[l] for l in libs)]))
    kit.nav(2, c["id"], c["titulo"], sit=" ".join(c["sit"]), lib=" ".join(libs))
    return f'''
  <article class="card" id="{c["id"]}" data-sit="{" ".join(c["sit"])}" data-lib="{" ".join(libs)}" data-busca="{H.escape(busca)}">
    <header class="card-head"><h3>{c["titulo"]}</h3><div class="tags">{sit}{lib}</div></header>
    <p class="objetivo"><span class="rot">Objetivo</span>{c["objetivo"]}</p>
    <div class="uso">
      <div class="uso-sim"><p class="rot">Quando escolher</p><ul>{escolha}</ul></div>
      <div class="uso-nao"><p class="rot">Quando evitar</p><ul>{evite}</ul></div>
    </div>
    <div class="nota-eixo"><span class="rot">Realçar no código</span>{kit.chips_eixos(ordem)}</div>
    {kit.switcher(c["id"], c["variantes"], alt=c["titulo"])}
    <div class="notas">{notas}</div>
    {base}
  </article>'''


def catalogo_html():
    kit.nav(1, "catalogo", "Catálogo de gráficos")
    cards = "".join(card_html(c) for c in catalogo.CARDS)
    sits = "".join(f'<li><strong>{n}</strong>: {d}</li>' for n, d in [
        ("Comparação", "qual é maior, menor, melhor ou pior"),
        ("Tendência", "como algo muda ao longo do tempo"),
        ("Distribuição", "como os valores se espalham"),
        ("Relação", "se duas medidas variam juntas"),
        ("Composição", "como um todo se divide em partes")])
    return f'''
<section id="catalogo" class="secao">
  <p class="sobretitulo">Parte 3</p>
  <h2>Catálogo de gráficos</h2>
  <p class="lead">Dezesseis gráficos, cada um com objetivo, critérios de escolha, código completo e a imagem gerada por esse código. Todos já aplicam os princípios do livro; os botões “Realçar no código” mostram quais linhas fazem cada trabalho. Use os filtros da barra lateral para ver só uma situação ou uma biblioteca.</p>
  <ul class="situacoes">{sits}</ul>
  <p class="vazio" hidden>Nenhum gráfico corresponde aos filtros. Limpe a busca ou escolha “Todas”.</p>
  {cards}
</section>'''


def inicio_html():
    kit.nav(1, "inicio", "Como usar este guia")
    return f'''
<section id="inicio" class="secao">
  <p class="sobretitulo">Guia interativo</p>
  <h1>Matplotlib e seaborn, do gráfico padrão ao gráfico que conta uma história</h1>
  <p class="lead">Um manual de código para as duas bibliotecas de visualização mais usadas em Python e, ao mesmo tempo, um manual prático das ideias de Cole Nussbaumer Knaflic em <em>Storytelling com Dados</em>. Cada exemplo mostra o código completo e a imagem que ele gerou.</p>
  <div class="cartoes3">
    <div class="cartao"><p class="cartao-rot">Para aprender a biblioteca</p><p>Comece pelos <a href="#fundamentos">fundamentos</a> e siga para o <a href="#catalogo">catálogo</a>. Os filtros da barra lateral separam os gráficos por situação e por biblioteca.</p></div>
    <div class="cartao"><p class="cartao-rot">Para melhorar um gráfico</p><p>Veja os <a href="#antes-depois">pares antes e depois</a>, os <a href="#erros">erros comuns</a> e o <a href="#r-estilo">estilo reutilizável</a>.</p></div>
    <div class="cartao"><p class="cartao-rot">Para preparar uma apresentação</p><p>Siga o <a href="#roteiro">roteiro de montagem</a>, da grande ideia ao gráfico final, e confira o <a href="#r-checklist">checklist</a>.</p></div>
  </div>
  <h3 class="h3-solto">Convenções</h3>
  <ul>
    <li><strong>Cores com função.</strong> <span class="amostra" style="background:#A6A6A6"></span> cinza para contexto, <span class="amostra" style="background:#1F5FA8"></span> azul para destaque e <span class="amostra" style="background:#D9731A"></span> laranja só para alertas e contrastes. O próprio guia segue a mesma regra.</li>
    <li><strong>Código completo.</strong> Cada bloco roda sozinho em um notebook ou script: tem os imports, os dados e o <code>plt.show()</code>. A maior parte começa com um preâmbulo de estilo de oito linhas, explicado em <a href="#f-estilos">Estilos e rcParams</a>.</li>
    <li><strong>Dados.</strong> São sintéticos (e marcados como tal) ou vêm dos conjuntos embutidos no seaborn (<code>tips</code>, <code>flights</code>, <code>iris</code>). Na primeira execução, <code>sns.load_dataset</code> baixa os arquivos da internet.</li>
    <li><strong>Quem disse o quê.</strong> <span class="selo knaflic">Knaflic</span> marca ideias da autora, sempre parafraseadas. <span class="selo tec">Recomendação técnica</span> marca sugestões deste guia sobre matplotlib e seaborn. <span class="selo confirmar">a confirmar no livro</span> marca detalhes que devem ser conferidos na fonte.</li>
  </ul>
</section>'''


# ------------------------------------------------------------------ montagem
partes = {}
partes["inicio"] = coleta_nav(inicio_html)
partes["fund"] = coleta_nav(fundamentos.html)
partes["cat"] = coleta_nav(catalogo_html)
partes["ad"] = coleta_nav(story.antes_depois_html)
partes["rot"] = coleta_nav(story.roteiro_html)
partes["err"] = coleta_nav(story.erros_html)
partes["ref"] = coleta_nav(referencia.html, VERSOES)
# a ordem do registro define a ordem dos links nos eixos: catálogo primeiro
registro = [x for x in story.REG if x[0].startswith("g-")] + [x for x in story.REG if not x[0].startswith("g-")]
partes["eixos"] = coleta_nav(story.eixos_html, registro)

ordem = ["inicio", "fund", "eixos", "cat", "ad", "rot", "err", "ref"]
corpo = "".join(partes[p][0] for p in ordem).replace("{VERSOES}", VERSOES)

nav_itens = []
for p in ordem:
    for nivel, id_, rotulo, attrs in partes[p][1]:
        extra = "".join(f' data-{a}="{v}"' for a, v in attrs.items())
        busca = H.escape(sem_acento(rotulo))
        nav_itens.append(f'<li class="n{nivel}"{extra} data-busca="{busca}"><a href="#{id_}">{rotulo}</a></li>')
NAV_HTML = "".join(nav_itens)

FILTROS_SIT = "".join(f'<button type="button" class="filtro" data-grupo="sit" data-valor="{k_}" aria-pressed="false">{v}</button>'
                      for k_, v in catalogo.SIT.items())

CSS = (AQUI / "estilo.css").read_text(encoding="utf-8")
JS = (AQUI / "app.js").read_text(encoding="utf-8")

pagina = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guia matplotlib e seaborn</title>
<meta name="description" content="Manual interativo de matplotlib e seaborn com os princípios de storytelling com dados de Cole Nussbaumer Knaflic.">
<style>{CSS}</style>
</head>
<body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="barra-movel">
  <button type="button" class="abre-menu" aria-expanded="false" aria-controls="lateral">Menu</button>
  <span>Guia matplotlib e seaborn</span>
</header>
<aside id="lateral" class="lateral" aria-label="Navegação do guia">
  <div class="lateral-topo">
    <p class="marca">Guia matplotlib<br>e seaborn</p>
    <p class="marca-sub">com storytelling de dados</p>
    <label class="busca"><span class="sr">Buscar no guia</span>
      <input type="search" id="busca" placeholder="Buscar gráfico ou seção" autocomplete="off"></label>
    <div class="filtros" role="group" aria-label="Filtrar catálogo por situação">
      <p class="filtros-rot">Situação</p>
      <button type="button" class="filtro" data-grupo="sit" data-valor="todas" aria-pressed="true">Todas</button>{FILTROS_SIT}
    </div>
    <div class="filtros" role="group" aria-label="Filtrar catálogo por biblioteca">
      <p class="filtros-rot">Biblioteca</p>
      <button type="button" class="filtro" data-grupo="lib" data-valor="todas" aria-pressed="true">Todas</button><button type="button" class="filtro" data-grupo="lib" data-valor="mpl" aria-pressed="false">matplotlib</button><button type="button" class="filtro" data-grupo="lib" data-valor="sns" aria-pressed="false">seaborn</button>
    </div>
    <p class="contagem" aria-live="polite"></p>
  </div>
  <nav><ul class="nav">{NAV_HTML}</ul></nav>
</aside>
<div class="veu" hidden></div>
<main id="conteudo">
{corpo}
<footer class="rodape"><p>Guia gerado em Python; cada imagem foi produzida pelo código exibido ao lado dela. Ideias de storytelling: Cole Nussbaumer Knaflic, <em>Storytelling com Dados</em>.</p></footer>
</main>
<script>{JS}</script>
</body>
</html>
'''

with open(SAIDA, "w", encoding="utf-8") as f:
    f.write(pagina)

print("imagens:", kit.STATS["imagens"], "| PNG total:", round(kit.STATS["bytes"] / 1e6, 2), "MB")
print("arquivo:", round(len(pagina.encode()) / 1e6, 2), "MB")
print("avisos:", *kit.WARN_LOG, sep="\n  ")
