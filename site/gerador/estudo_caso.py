"""Estudo de caso com dados reais (ANAC) -> páginas do site.

O notebook (gerador/estudo-de-caso/Estudo_de_Caso_Aviacao_ANAC.ipynb) é versionado já executado,
com as saídas, porque os dados brutos não estão no repositório. Com --reexecutar, o gerador baixa
o que faltar (o próprio notebook chama baixar_dados.py), executa o notebook e grava as saídas nele.

Cada página reúne seções inteiras do notebook ("## N. Título"). Metadados de célula usados:
  alt              lista com o texto alternativo de cada figura da célula (obrigatório)
  site.so_saida    true: mostra só a saída (ex.: texto do relatório montado a partir dos números)
"""
from __future__ import annotations

import base64
import os
import re
import shutil
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import notebook
from comum import PUBLICO, bloco_codigo, esc, figura, salvar_imagem

AQUI = Path(__file__).resolve().parent
PASTA = AQUI / "estudo-de-caso"
ORIGEM = PASTA / "Estudo_de_Caso_Aviacao_ANAC.ipynb"
IMG = PUBLICO / "img" / "estudo-de-caso"


def executar(forcar: bool = False) -> nbformat.NotebookNode:
    nb = nbformat.read(ORIGEM, as_version=4)
    if not forcar:
        sem_saida = [i for i, c in enumerate(nb.cells) if c.cell_type == "code" and c.source.strip()
                     and c.get("execution_count") is None]
        if sem_saida:
            raise RuntimeError(f"Notebook do estudo de caso sem saídas (células {sem_saida[:5]}…): "
                               "rode npm run gerar:tudo para executá-lo.")
        return nb
    env_kernel = AQUI / ".venv" / "share" / "jupyter"
    os.environ["JUPYTER_PATH"] = str(env_kernel) + os.pathsep + os.environ.get("JUPYTER_PATH", "")
    cliente = NotebookClient(nb, timeout=1800, kernel_name="analise-de-dados", allow_errors=False,
                             resources={"metadata": {"path": str(PASTA)}})
    cliente.execute()
    for c in nb.cells:                       # metadados voláteis da execução não vão para o git
        c.metadata.pop("execution", None)
    nbformat.write(nb, ORIGEM)
    return nb


def secao_da_celula(nb) -> list[str | None]:
    """Número da seção ("0", "1", …) de cada célula, pelo último título "## N." visto."""
    atual, secoes = None, []
    for c in nb.cells:
        if c.cell_type == "markdown":
            m = re.search(r"^## (\d+)\.", c.source, re.M)
            if m:
                atual = m.group(1)
        secoes.append(atual)
    return secoes


def _saidas(i: int, celula, contador: list[int], usados: set[str]) -> str:
    partes, n_fig = [], 0
    alts = celula.metadata.get("alt", [])
    for o in celula.get("outputs", []):
        if o.output_type == "stream":
            if o.name == "stderr":
                raise RuntimeError(f"Estudo de caso, célula {i} escreveu em stderr: {o.text[:300]}")
            partes.append(f'<pre class="saida__texto" tabindex="0">{esc(o.text.rstrip())}</pre>')
        elif o.output_type in ("execute_result", "display_data"):
            dados = o.get("data", {})
            if "image/png" in dados:
                if n_fig >= len(alts):
                    raise KeyError(f"Estudo de caso: falta texto alternativo para a figura {n_fig} da célula {i}")
                nome = f"celula-{i:03d}" + (f"-{n_fig + 1}" if n_fig else "") + ".webp"
                w, h = salvar_imagem(base64.b64decode(dados["image/png"]), IMG / nome)
                partes.append(figura(f"/img/estudo-de-caso/{nome}", w, h, alts[n_fig],
                                     "Fonte: ANAC (dados abertos). Elaboração própria."))
                n_fig += 1
                contador[0] += 1
            elif "text/markdown" in dados:
                partes.append(notebook.markdown_para_html(dados["text/markdown"], usados))
            elif "text/html" in dados:
                partes.append(notebook._tabela_dataframe(dados["text/html"], "Saída em tabela"))
            elif "text/plain" in dados:
                partes.append(f'<pre class="saida__texto" tabindex="0">{esc(dados["text/plain"])}</pre>')
        elif o.output_type == "error":
            raise RuntimeError(f"Estudo de caso, erro na célula {i}: {o.ename}: {o.evalue}")
    if not partes:
        return ""
    return ('<div class="saida" data-pagefind-ignore><p class="saida__rotulo">Saída</p>'
            + "".join(partes) + "</div>")


def renderizar_pagina(nb, pagina: dict, contador: list[int]) -> str:
    secoes = secao_da_celula(nb)
    usados: set[str] = set()
    partes = []
    for i, c in enumerate(nb.cells):
        if secoes[i] not in pagina["secoes"]:
            continue
        if c.cell_type == "markdown":
            fonte = re.sub(r"^---\s*$", "", c.source, flags=re.M)
            partes.append(notebook.markdown_para_html(fonte, usados))
        elif c.source.strip():
            if c.metadata.get("site", {}).get("so_saida"):
                partes.append(_saidas(i, c, contador, usados).replace(
                    '<div class="saida" data-pagefind-ignore><p class="saida__rotulo">Saída</p>', '<div>', 1))
            else:
                partes.append(bloco_codigo(c.source, "python"))
                partes.append(_saidas(i, c, contador, usados))
    return "\n".join(p for p in partes if p)


def limpar_imagens() -> None:
    if IMG.exists():
        shutil.rmtree(IMG)
    IMG.mkdir(parents=True)


def copiar_downloads() -> None:
    destino = PUBLICO / "downloads"
    destino.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ORIGEM, destino / ORIGEM.name)
