"""Manual e guia de data science (pacote data-science-htlm) -> páginas do site.

- manual_machine_learning.html: as seções estáticas são lidas do HTML; os 43 cartões de modelo e a
  matriz dos sete critérios, que o manual monta em JavaScript, são renderizados no build a partir dos
  dados do próprio script (MODELS, MATRIZ, CATS, BLOCKS), extraídos por extrair_ml.mjs.
- O diagnóstico do dataset continua rodando no navegador com o script original do manual, sem
  alterações (copiado para src/scripts/gerado/).
- skill_decisao_ml.md e auditoria_ml.md viram páginas; os scripts da auditoria aparecem na página
  da auditoria. O texto não é alterado.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin

from comum import CONTEUDO, PUBLICO, RAIZ, bloco_codigo, callout, esc, icone, slug, tabela

AQUI = Path(__file__).resolve().parent
ORIGEM = AQUI / "origem" / "data-science-htlm"
MANUAL = ORIGEM / "manual_machine_learning.html"
SCRIPTS_GERADOS = RAIZ / "src" / "scripts" / "gerado"
ORIGEM_NOTEBOOKS = AQUI / "origem" / "modelos-ml"

URL_SKILL = "/modelar/skill-de-decisao/"
URL_MANUAL = "/modelar/manual-de-machine-learning/"

# Notebooks modelo (templates genéricos) derivados de notebooks de estudo (fora do repositório) e associados ao cartão
# do modelo correspondente: id do modelo -> [(arquivo, título, descrição, notebook de origem)].
# Os arquivos ficam em origem/modelos-ml/ e são copiados sem alteração para /downloads/.
NOTEBOOKS_MODELO = {
    "linear-regression": [(
        "modelo_ml_regressao_linear.ipynb", "Regressão linear com gradiente descendente",
        "custo, gradiente e gradiente descendente implementados do zero para n features, com treino/teste, "
        "MAE, RMSE, R², resíduos e validação contra a forma fechada.", "C1_W2_Linear_Regression.ipynb")],
    "logistic": [(
        "modelo_ml_regressao_logistica.ipynb", "Regressão logística com e sem regularização",
        "sigmoide, log loss e gradiente do zero, expansão polinomial opcional e L2, ROC-AUC, PR-AUC, escolha do "
        "limiar e comparação com LogisticRegression.", "C1_W3_Logistic_Regression.ipynb")],
    "mlp": [(
        "modelo_ml_rede_neural_binaria.ipynb", "Rede neural para classificação binária",
        "MLP em Keras 3 com treino/validação/teste e early stopping, e a propagação direta reimplementada em "
        "NumPy e conferida com o Keras.", "C2_W1_Assignment.ipynb"), (
        "modelo_ml_rede_neural_multiclasse.ipynb", "Rede neural multiclasse com softmax",
        "ReLU, saída linear com from_logits=True, softmax estável em NumPy, métricas por classe e análise "
        "dos erros.", "C2_W2_Assignment.ipynb")],
    "polynomial": [(
        "modelo_ml_regressao_polinomial_vies_variancia.ipynb", "Regressão polinomial e viés × variância",
        "treino/validação/teste, escolha do grau e de λ, curva de aprendizado e, opcionalmente, redes "
        "simples, complexas e regularizadas.", "C2_W3_Assignment.ipynb")],
    "decision-tree": [(
        "modelo_ml_arvore_de_decisao.ipynb", "Árvore de decisão do zero",
        "entropia ou Gini, ganho de informação, limiares para features numéricas, construção recursiva, "
        "previsão, regras legíveis e comparação com DecisionTreeClassifier.", "C2_W4_Decision_Tree_with_Markdown.ipynb")],
    "kmeans": [(
        "modelo_ml_kmeans.ipynb", "K-Means do zero",
        "atribuição e atualização vetorizadas, k-means++, várias inicializações, cotovelo e silhouette, perfil "
        "dos grupos e compressão de imagem opcional.", "C3_W1_KMeans_Assignment.ipynb")],
    "gmm": [(
        "modelo_ml_deteccao_anomalias_gaussiana.ipynb", "Detecção de anomalias por densidade gaussiana",
        "densidade gaussiana em escala log (GMM de 1 componente), limiar ε pelo F1 na validação, teste "
        "separado e extensão para K componentes pelo BIC.", "C3_W1_Anomaly_Detection.ipynb")],
    "content-based": [(
        "modelo_ml_recomendacao_conteudo_rede_neural.ipynb", "Recomendação por conteúdo com rede de duas torres",
        "vetores de usuário e de item treinados juntos, RMSE contra baseline, precision@k e NDCG@k, novos "
        "usuários e itens semelhantes.", "C3_W2_RecSysNN_Assignment.ipynb")],
    "dqn": [(
        "modelo_ml_dqn.ipynb", "Deep Q-Network com replay e rede-alvo",
        "qualquer ambiente Gymnasium de ações discretas, atualização suave da rede-alvo, ε-gulosa e "
        "avaliação gulosa separada do treino.", "C3_W3_A1_Assignment.ipynb")],
}


# ------------------------------------------------------------------ dados do script do manual
def dados() -> dict:
    saida = subprocess.run(["node", str(AQUI / "extrair_ml.mjs"), str(MANUAL)],
                           check=True, capture_output=True, text=True).stdout
    return json.loads(saida)


def _tag(t: str, cats: dict) -> str:
    return f'<span class="selo tag-cat" data-tag="{t}">{esc(cats[t])}</span>'


def cartao(m: dict, d: dict) -> str:
    """Mesmo conteúdo e ordem de cardHtml() do manual, com os componentes do site."""
    blocos = []
    for i, (chave, rotulo) in enumerate(d["BLOCKS"], 1):
        if chave == "cod":
            corpo = bloco_codigo(m[chave], "python")
            classe = " bloco-ml--largo"
        else:
            corpo = f'<div class="bloco-ml__c">{m[chave]}</div>'
            classe = ""
        blocos.append(f'<section class="bloco-ml{classe}"><h4 class="bloco-ml__h">'
                      f'<span class="bloco-ml__n">{i:02d}</span>{rotulo}</h4>{corpo}</section>')
    pres = (f'<p class="modelo__pres"><b>Pressupostos:</b> {d["MATRIZ"][m["id"]]["pres"]}</p>'
            if m["id"] in d["MATRIZ"] else "")
    tags = "".join(_tag(t, d["CATS"]) for t in m["tags"])
    return (f'<details class="modelo" id="m-{m["id"]}" data-tags="{" ".join(m["tags"])}">'
            f'<summary><h3 class="modelo__nome" id="m-{m["id"]}-titulo">{m["nome"]}</h3>'
            f'<span class="modelo__tags">{tags}</span>'
            f'<span class="modelo__resumo">{m["resumo"]}</span></summary>'
            f'<div class="modelo__corpo">{pres}{bloco_notebooks(m["id"])}'
            f'<div class="modelo__blocos">{"".join(blocos)}</div></div></details>')


def bloco_notebooks(model_id: str) -> str:
    """Downloads dos notebooks modelo associados ao cartão (vazio se não houver)."""
    itens = NOTEBOOKS_MODELO.get(model_id)
    if not itens:
        return ""
    lis = "".join(
        f'<li><a class="botao botao--secundario botao--pequeno" href="/downloads/{arq}" download>'
        f'{icone("download")}Baixar {esc(arq)}</a>'
        f'<span class="modelo__notebooks-desc"><b>{esc(titulo)}:</b> {esc(desc)} '
        f'Derivado de <code>{esc(origem)}</code>.</span></li>'
        for arq, titulo, desc, origem in itens)
    rotulo = "Notebook modelo" if len(itens) == 1 else "Notebooks modelo"
    return (f'<div class="modelo__notebooks"><p class="modelo__notebooks-titulo">{rotulo} '
            f'(template genérico para o seu dataset)</p><ul class="modelo__notebooks-lista">{lis}</ul></div>')


def lista_notebooks(d: dict, pagina_do_grupo: dict) -> list[dict]:
    """Notebooks modelo para a página Sobre, na ordem dos cartões do manual."""
    saida = []
    for m in d["MODELS"]:
        for arq, titulo, desc, origem in NOTEBOOKS_MODELO.get(m["id"], []):
            saida.append({"arquivo": arq, "titulo": titulo, "descricao": desc, "origem": origem,
                          "modelo": m["nome"], "url": f'/{pagina_do_grupo[m["grupo"]]}/#m-{m["id"]}'})
    return saida


def _nivel(v: str, inverte: bool = False) -> str:
    bom = v == "Baixo" if inverte else v == "Alta"
    ruim = v == "Alto" if inverte else v == "Baixa"
    return f'<span class="nivel {"nv-bom" if bom else "nv-ruim" if ruim else "nv-medio"}">{v}</span>'


def linhas_matriz(d: dict) -> str:
    """Mesmo conteúdo de renderMatriz() do manual."""
    linhas = []
    for m in d["MODELS"]:
        x = d["MATRIZ"].get(m["id"])
        if not x:
            continue
        linhas.append(f'<tr data-mid="{m["id"]}" data-tags="{" ".join(m["tags"])}">'
                      f'<td><a href="#m-{m["id"]}">{m["nome"].split(" (")[0]}</a></td>'
                      f'<td>{x["pres"]}</td><td>{x["forte"]}</td><td>{x["fraco"]}</td><td>{x["dados"]}</td>'
                      f'<td>{_nivel(x["i"])}</td><td>{_nivel(x["c"], True)}</td><td>{x["met"]}</td></tr>')
    return "".join(linhas)


# ------------------------------------------------------------------ seções do HTML
TIPO_CALLOUT = {"warn": "atencao", "ok": "sucesso", "bad": "erro"}


def _converter(sec, d: dict, promover: bool = True) -> None:
    # cartões de modelo e matriz (gerados em JavaScript no original)
    for host in sec.select("[data-models]"):
        grupo = host["data-models"]
        host.clear()
        host.append(BeautifulSoup("".join(cartao(m, d) for m in d["MODELS"] if m["grupo"] == grupo), "html.parser"))
        host["class"] = (host.get("class") or []) + ["modelos"]
        del host["data-models"]
    corpo = sec.select_one("#matriz7 tbody")
    if corpo is not None:
        corpo.clear()
        corpo.append(BeautifulSoup(linhas_matriz(d), "html.parser"))
    # blocos de código estáticos
    for pre in sec.select("pre.code"):
        code = pre.find("code")
        if code is not None and code.get("id") == "dxCodigo":
            continue
        shell = (pre.get("data-lang") == "shell") or (code is not None and code.get("data-lang") == "shell")
        novo = bloco_codigo(pre.get_text(), "text" if shell else "python", rotulo="shell" if shell else None)
        alvo = pre.parent if "code-wrap" in (pre.parent.get("class") or []) else pre
        alvo.replace_with(BeautifulSoup(novo, "html.parser"))
    # callouts
    for c in sec.select("div.callout"):
        if c.get("id"):                       # caixa de erro do diagnóstico: preenchida pelo script
            continue
        classes = c.get("class") or []
        tipo = next((TIPO_CALLOUT[k] for k in TIPO_CALLOUT if k in classes), "nota")
        t = c.find("b", class_="ctitle")
        titulo = t.decode_contents() if t else None
        if t:
            t.decompose()
        c.replace_with(BeautifulSoup(callout(tipo, c.decode_contents().strip(), titulo), "html.parser"))
    # etiquetas de categoria e pílulas
    for t in sec.select("span.tag"):
        cat = next((x[2:] for x in t.get("class", []) if x.startswith("t-")), "")
        texto = t.get_text(strip=True)
        t.replace_with(BeautifulSoup(f'<span class="selo tag-cat" data-tag="{cat}">{esc(texto)}</span>', "html.parser"))
    for p in sec.select("span.pill"):
        p["class"] = ["selo"] + (["pill-estado"] if p.get("id") else [])
    # tabelas
    for w in sec.select("div.table-wrap"):
        w["class"] = ["tabela"]
        w["role"] = "region"
        w["tabindex"] = "0"
        ant = w.find_previous(["h2", "h3", "h4", "p"])
        w["aria-label"] = (ant.get_text(" ", strip=True) if ant else "Tabela")[:120]
        t = w.find("table")
        if t is not None and not t.get("id"):
            t["class"] = (t.get("class") or [])
        for th in w.select("thead th"):
            th["scope"] = "col"
    # botões
    for b in sec.select(".btn"):
        b["class"] = ["botao", "botao--secundario", "botao--pequeno"]
        b["type"] = b.get("type", "button")
    # estilos inline: só espaçamentos/larguras (descartados) e um tom de texto secundário
    for el in sec.find_all(style=True):
        if "color:" in el["style"]:
            el["class"] = (el.get("class") or []) + ["muted", "small"]
        del el["style"]
    # links para os outros arquivos do pacote
    for a in sec.find_all("a", href=True):
        h = a["href"]
        if h.startswith("skill_decisao_ml.md"):
            a["href"] = URL_SKILL
        elif h.startswith("manual_machine_learning.html"):
            a["href"] = h.split(".html", 1)[1] or URL_MANUAL
    # hierarquia: o h2 da seção vira o h1 da página
    if promover:
        for h in sec.find_all(["h3", "h4", "h5"]):
            if "modelo__nome" in (h.get("class") or []) or "bloco-ml__h" in (h.get("class") or []):
                continue
            h.name = {"h3": "h2", "h4": "h3", "h5": "h4"}[h.name]
    # âncoras para os títulos que não tinham id (índice da página e busca)
    usados = {t["id"] for t in sec.find_all(id=True)}
    for h in sec.find_all(["h2", "h3"]):
        if h.get("id") or h.find_parent("details", class_="modelo"):
            continue
        base = slug(h.get_text(" ", strip=True)) or "secao"
        ident, n = base, 2
        while ident in usados:
            ident, n = f"{base}-{n}", n + 1
        usados.add(ident)
        h["id"] = ident


def secoes(d: dict) -> dict:
    sopa = BeautifulSoup(MANUAL.read_text(encoding="utf-8"), "html.parser")
    saida = {}
    for sec in sopa.select("main section.sec"):
        ident = sec["id"]
        tags = []
        cab = sec.find("div", class_="sec-head")
        if cab is not None:
            sobre = cab.find(class_="sec-num").get_text(" ", strip=True)
            h2 = cab.find("h2")
            for t in h2.select("span.tag"):
                tags.append(next((x[2:] for x in t.get("class", []) if x.startswith("t-")), ""))
                t.decompose()
            titulo = h2.get_text(" ", strip=True)
            cab.decompose()
        else:                                    # início: título no herói
            h1 = sec.find("h1")
            titulo, sobre = h1.get_text(" ", strip=True), ""
            h1.decompose()
        _converter(sec, d, promover=ident != "comousar")
        saida[ident] = {"titulo": titulo, "sobretitulo": sobre, "tags": tags, "html": sec.decode_contents()}
    return saida


def legenda_e_indice(d: dict) -> str:
    """Legenda clicável (filtros por categoria) e índice dos 43 modelos, que o filtro afeta.
    No original, a legenda filtrava os cartões da página única; aqui eles estão em várias páginas."""
    botoes = "".join(
        f'<button type="button" class="filtro filtro-cat" data-tag="{k}" aria-pressed="false">{esc(v)}</button>'
        for k, v in d["CATS"].items())
    return botoes


def indice_modelos(d: dict, pagina_do_grupo: dict) -> str:
    itens = []
    for m in d["MODELS"]:
        url = f'/{pagina_do_grupo[m["grupo"]]}/#m-{m["id"]}'
        tags = "".join(_tag(t, d["CATS"]) for t in m["tags"])
        if m["id"] in NOTEBOOKS_MODELO:
            tags += '<span class="selo">notebook modelo</span>'
        itens.append(f'<li class="indice-modelos__item" data-tags="{" ".join(m["tags"])}">'
                     f'<a href="{url}">{m["nome"]}</a><span class="modelo__tags">{tags}</span>'
                     f'<span class="indice-modelos__resumo">{m["resumo"]}</span></li>')
    return ('<h2 id="indice-dos-modelos">Índice dos modelos</h2>'
            '<p class="contagem" id="contagemModelos" aria-live="polite"></p>'
            f'<ul class="indice-modelos" id="indiceModelos">{"".join(itens)}</ul>')


# ------------------------------------------------------------------ Markdown (skill e auditoria)
def _fence(self, tokens, idx, options, env):
    tok = tokens[idx]
    lang = (tok.info or "").strip().split()[0] if tok.info else ""
    if lang == "python":
        return bloco_codigo(tok.content, "python")
    return bloco_codigo(tok.content, "text", rotulo=lang or "texto")


MD = MarkdownIt("commonmark", {"html": False}).enable("table").use(tasklists_plugin, enabled=True, label=True)
MD.add_render_rule("fence", _fence)
MD.add_render_rule("code_block", _fence)


def markdown(fonte: str) -> tuple[str, str]:
    """Devolve (título do # inicial, HTML do resto) com títulos ajustados e tabelas no componente do site."""
    m = re.search(r"^# (.+)$", fonte, re.M)
    titulo = m.group(1).strip() if m else ""
    if m:
        fonte = fonte[:m.start()] + fonte[m.end():]
    sopa = BeautifulSoup(MD.render(fonte), "html.parser")
    usados: set[str] = set()
    for h in sopa.find_all(["h2", "h3", "h4"]):
        base = slug(h.get_text(" ", strip=True)) or "secao"
        ident, n = base, 2
        while ident in usados:
            ident, n = f"{base}-{n}", n + 1
        usados.add(ident)
        h["id"] = ident
    for t in sopa.find_all("table"):
        ant = t.find_previous(["h2", "h3", "h4"])
        t.wrap(BeautifulSoup(tabela("", ant.get_text(" ", strip=True) if ant else "Tabela"), "html.parser").div)
    for a in sopa.find_all("a", href=True):
        if a["href"].startswith("skill_decisao_ml.md"):
            a["href"] = URL_SKILL
    for code in sopa.find_all("code"):
        if code.find_parent("pre"):
            continue
        txt = code.get_text()
        if txt.startswith("manual_machine_learning.html#"):
            ancora = txt.split("#", 1)[1]
            code.wrap(sopa.new_tag("a", href=f"#{ancora}"))
    return titulo, str(sopa)


def pagina_skill() -> dict:
    fonte = (ORIGEM / "skill_decisao_ml.md").read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---\n", fonte, re.S)
    meta = ""
    if fm:
        linhas = []
        for ln in fm.group(1).splitlines():
            chave, _, valor = ln.partition(":")
            linhas.append(f"<tr><th scope=\"row\"><code>{esc(chave.strip())}</code></th><td>{esc(valor.strip())}</td></tr>")
        meta = ('<h2 id="metadados-da-skill">Metadados da skill</h2>'
                '<p class="muted small">Cabeçalho YAML do arquivo, lido pelo agente para decidir quando usar a skill.</p>'
                + tabela(f'<table class="tabela-dados"><tbody>{"".join(linhas)}</tbody></table>', "Metadados da skill"))
        fonte = fonte[fm.end():]
    titulo, html = markdown(fonte)
    acoes = ('<div class="ferramentas-guia" data-pagefind-ignore>'
             '<a class="botao botao--secundario botao--pequeno" href="/downloads/skill_decisao_ml.md" download>Baixar skill_decisao_ml.md</a></div>')
    return {"titulo": titulo, "html": acoes + meta + html}


def pagina_auditoria() -> dict:
    titulo, html = markdown((ORIGEM / "auditoria_ml.md").read_text(encoding="utf-8"))
    scripts = []
    for f in sorted((ORIGEM / "auditoria").iterdir()):
        if f.suffix not in (".py", ".sh"):
            continue
        lang = "python" if f.suffix == ".py" else "text"
        scripts.append(f'<details class="fold"><summary><code>auditoria/{f.name}</code></summary><div class="fold-body">'
                       f'{bloco_codigo(f.read_text(encoding="utf-8"), lang, rotulo=None if lang == "python" else "bash")}</div></details>')
    extra = ('<h2 id="scripts-da-auditoria">Scripts da auditoria (pasta <code>auditoria/</code>)</h2>'
             '<p>Os seis scripts que reproduzem a auditoria, como foram entregues no pacote.</p>' + "".join(scripts))
    acoes = ('<div class="ferramentas-guia" data-pagefind-ignore>'
             '<a class="botao botao--secundario botao--pequeno" href="/downloads/auditoria_ml.md" download>Baixar auditoria_ml.md</a></div>')
    return {"titulo": titulo, "html": acoes + html + extra}


def readme_html() -> str:
    sopa = BeautifulSoup(MD.render((ORIGEM / "README.md").read_text(encoding="utf-8")), "html.parser")
    for h in sopa.find_all(["h1", "h2", "h3"]):
        h.name = {"h1": "h3", "h2": "h4", "h3": "h5"}[h.name]
    for t in sopa.find_all("table"):
        t["class"] = ["tabela-dados"]
        t.wrap(BeautifulSoup(tabela("", "Arquivos do pacote"), "html.parser").div)
    gi = (ORIGEM / ".gitignore")
    if gi.exists():
        sopa.append(BeautifulSoup('<p class="muted small">Arquivo <code>.gitignore</code> do pacote:</p>'
                                  + bloco_codigo(gi.read_text(encoding="utf-8"), "text", rotulo=".gitignore"), "html.parser"))
    return str(sopa)


# ------------------------------------------------------------------ scripts do diagnóstico e downloads
def gerar_scripts() -> None:
    """Copia, sem alterações, o script do diagnóstico e a função de realce que ele usa."""
    html = MANUAL.read_text(encoding="utf-8")
    scripts = [m.group(1) for m in re.finditer(r"<script[^>]*>(.*?)</script>", html, re.S)]
    principal, diagnostico = scripts[0], scripts[1]
    ini = principal.index("// realce de sintaxe Python")
    fim = principal.index("/* ===================== renderização dos cards")
    realce = principal[ini:fim]
    esc_fn = re.search(r"const esc = .*?;\n", principal).group(0)
    SCRIPTS_GERADOS.mkdir(parents=True, exist_ok=True)
    (SCRIPTS_GERADOS / "realce-py.js").write_text(
        "// Gerado por gerador/guia_ml.py a partir de manual_machine_learning.html (não editar).\n"
        "// Função de realce usada pelo diagnóstico para o código inicial.\n"
        + esc_fn + realce + "\nglobalThis.highlightPy = highlightPy;\n", encoding="utf-8")
    (SCRIPTS_GERADOS / "diagnostico-ml.js").write_text(
        "// Gerado por gerador/guia_ml.py: script do diagnóstico copiado sem alterações de\n"
        "// manual_machine_learning.html (pacote data-science-htlm).\n" + diagnostico, encoding="utf-8")


def copiar_downloads() -> None:
    destino = PUBLICO / "downloads"
    destino.mkdir(parents=True, exist_ok=True)
    for nome in ("skill_decisao_ml.md", "auditoria_ml.md"):
        shutil.copy2(ORIGEM / nome, destino / nome)
    for itens in NOTEBOOKS_MODELO.values():
        for arq, *_ in itens:
            if not (ORIGEM_NOTEBOOKS / arq).exists():
                raise FileNotFoundError(f"notebook modelo ausente: {ORIGEM_NOTEBOOKS / arq}")
            shutil.copy2(ORIGEM_NOTEBOOKS / arq, destino / arq)


def diagnostico_ajustes(html: str) -> str:
    """Bloco do código inicial no componente do site, mantendo o id que o script preenche."""
    sopa = BeautifulSoup(html, "html.parser")
    code = sopa.find("code", id="dxCodigo")
    if code is not None:
        alvo = code.find_parent("div", class_="code-wrap") or code.find_parent("pre")
        alvo.replace_with(BeautifulSoup(
            '<div class="codigo" data-lang="python"><div class="codigo__barra" data-pagefind-ignore>'
            '<span class="codigo__lang">python</span><button type="button" class="codigo__copiar" data-copiar>Copiar</button></div>'
            '<pre class="codigo__pre" tabindex="0" aria-label="Código inicial gerado"><code id="dxCodigo"></code></pre></div>',
            "html.parser"))
    drop = sopa.find(id="dxDrop")
    if drop is not None:
        drop["class"] = ["dx-drop"]
    return str(sopa)
