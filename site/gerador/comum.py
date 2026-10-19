"""Peças compartilhadas pelos geradores: realce de código, componentes HTML, imagens e ícones.

Nenhuma cor ou medida é escrita aqui: o HTML só leva classes, e o estilo vem dos tokens
do design system em src/styles/.
"""
from __future__ import annotations

import html
import io
import re
import unicodedata
from pathlib import Path

from PIL import Image
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.token import Token

RAIZ = Path(__file__).resolve().parent.parent          # site/
PUBLICO = RAIZ / "public"
CONTEUDO = RAIZ / "src" / "conteudo"


# ------------------------------------------------------------------ texto
def slug(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t


def esc(texto: str) -> str:
    return html.escape(texto, quote=True)


# ------------------------------------------------------------------ ícones (traço no estilo Lucide)
_SVG = ('<svg class="icone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{}</svg>')
ICONES = {
    "atencao": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "alternativa": '<path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
    "complemento": '<circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/>',
    "nota": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "sucesso": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "erro": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    "livro": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
    "download": '<path d="M12 15V3"/><path d="m7 10 5 5 5-5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>',
    "imprimir": '<path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v8H6z"/>',
    "ampliar": '<path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="m21 3-7 7"/><path d="m3 21 7-7"/>',
}


def icone(nome: str) -> str:
    return _SVG.format(ICONES[nome])


# ------------------------------------------------------------------ realce de sintaxe
_CLASSES = [
    (Token.Comment, "tk-com"),
    (Token.Literal.String.Affix, "tk-kw"),
    (Token.Literal.String, "tk-str"),
    (Token.Literal.Number, "tk-num"),
    (Token.Operator.Word, "tk-kw"),
    (Token.Keyword, "tk-kw"),
    (Token.Name.Builtin.Pseudo, "tk-kw"),
    (Token.Name.Builtin, "tk-bi"),
    (Token.Name.Function, "tk-fn"),
    (Token.Name.Class, "tk-fn"),
    (Token.Name.Decorator, "tk-dec"),
]


def _classe(ttype) -> str:
    for base, cls in _CLASSES:
        if ttype in base:
            return cls
    return ""


def _lexer(linguagem: str):
    if linguagem == "python":
        try:
            return get_lexer_by_name("ipython3")
        except Exception:  # pragma: no cover
            return PythonLexer()
    if linguagem in ("sql",):
        return get_lexer_by_name("sql")
    return None


def realcar(codigo: str, linguagem: str = "python") -> list[str]:
    """Devolve uma lista de linhas em HTML, com classes tk-* nos tokens."""
    lexer = _lexer(linguagem)
    if lexer is None:
        return [esc(l) for l in codigo.split("\n")]
    toks = list(lexer.get_tokens(codigo))
    linhas: list[list[str]] = [[]]
    for i, (ttype, valor) in enumerate(toks):
        cls = _classe(ttype)
        if not cls and ttype in Token.Name:
            # chamada de função: nome seguido de "("
            prox = next((v for _, v in toks[i + 1:i + 4] if v.strip()), "")
            if prox.startswith("("):
                cls = "tk-fn"
        partes = valor.split("\n")
        for j, parte in enumerate(partes):
            if j > 0:
                linhas.append([])
            if parte:
                linhas[-1].append(f'<span class="{cls}">{esc(parte)}</span>' if cls else esc(parte))
    if linhas and not linhas[-1]:
        linhas.pop()          # o lexer acrescenta uma quebra final
    return ["".join(l) for l in linhas]


def bloco_codigo(codigo: str, linguagem: str = "python", rotulo: str | None = None,
                 extra_attrs: str = "", classe_extra: str = "") -> str:
    """Bloco de código com barra, botão Copiar e linhas numeradas (span.ln)."""
    codigo = codigo.rstrip("\n")
    linhas = realcar(codigo, linguagem)
    corpo = "\n".join(f'<span class="ln" data-n="{i}">{l}</span>' for i, l in enumerate(linhas, 1))
    rot = rotulo or linguagem
    cls = f"codigo {classe_extra}".strip()
    return (f'<div class="{cls}" data-lang="{esc(linguagem)}"{extra_attrs}>'
            f'<div class="codigo__barra" data-pagefind-ignore><span class="codigo__lang">{esc(rot)}</span>'
            f'<button type="button" class="codigo__copiar" data-copiar>Copiar</button></div>'
            f'<pre class="codigo__pre" tabindex="0" aria-label="Código {esc(rot)}"><code>{corpo}</code></pre></div>')


def tabela(html_tabela: str, rotulo: str = "Tabela") -> str:
    return (f'<div class="tabela" role="region" tabindex="0" aria-label="{esc(rotulo)}">'
            f'{html_tabela}</div>')


# ------------------------------------------------------------------ imagens
def salvar_imagem(png: bytes | Image.Image, destino: Path) -> tuple[int, int]:
    """Converte para WebP sem perdas e devolve (largura, altura)."""
    img = png if isinstance(png, Image.Image) else Image.open(io.BytesIO(png))
    img = img.convert("RGB")
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino, format="WEBP", lossless=True, method=6, quality=100)
    return img.size


def figura(src: str, largura: int, altura: int, alt: str, legenda: str = "") -> str:
    leg = f"<figcaption>{legenda}</figcaption>" if legenda else ""
    return (f'<figure class="figura">'
            f'<button type="button" class="figura__ampliar" data-ampliar aria-label="Ampliar imagem: {esc(alt)}">'
            f'<img src="{src}" width="{largura}" height="{altura}" alt="{esc(alt)}" loading="lazy" decoding="async">'
            f'<span class="figura__icone">{icone("ampliar")}</span></button>{leg}</figure>')


def callout(tipo: str, corpo: str, titulo: str | None = None) -> str:
    rotulos = {"atencao": "Atenção", "alternativa": "Alternativa", "complemento": "Complemento", "nota": "Nota",
               "sucesso": "Boa prática", "erro": "Erro ou mito"}
    if titulo:
        cab = f'<p class="callout__titulo">{icone(tipo)}<span>{titulo}</span></p>'
    else:
        cab = f'<p class="callout__titulo callout__titulo--so-icone">{icone(tipo)}<span class="sr-only">{rotulos[tipo]}</span></p>'
    return f'<aside class="callout callout--{tipo}">{cab}<div class="callout__corpo">{corpo}</div></aside>'


def selo(tipo: str, texto: str, titulo: str = "") -> str:
    t = f' title="{esc(titulo)}"' if titulo else ""
    return f'<span class="selo selo--{tipo}"{t} data-pagefind-ignore>{texto}</span>'
