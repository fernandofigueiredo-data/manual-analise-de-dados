"""Baixa os dados abertos da ANAC usados no estudo de caso e registra tamanho e hash de cada arquivo.

Uso (a partir de site/):
    gerador/.venv/bin/python gerador/estudo-de-caso/baixar_dados.py --inicio 2023-01 --fim 2026-08

Os arquivos ficam em gerador/estudo-de-caso/dados/ (fora do git, ver .gitignore). O registro
(URL, tamanho em bytes, SHA-256 e data do download) vai para manifesto_download.json, que é
versionado: quem rodar de novo sabe se recebeu os mesmos arquivos.

Fontes (Fonte: ANAC, dados abertos):
  1. VRA, Voo Regular Ativo: um CSV por mês.
  2. Dados Estatísticos do Transporte Aéreo: um CSV único, de 2000 até hoje (o filtro de anos é feito na leitura).
  3. Reclamações do consumidor.gov.br contra companhias aéreas: um CSV por ano.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / "dados"
MANIFESTO = AQUI / "manifesto_download.json"
BASE = "https://sistemas.anac.gov.br/dadosabertos/Voos e operações aéreas/"

MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
ANOS_RECLAMACOES = range(2017, 2026)        # anos publicados em 19/10/2026


def url(caminho: str) -> str:
    return urllib.parse.quote(BASE + caminho, safe=":/")


def arquivos(inicio: str, fim: str) -> list[tuple[str, str]]:
    """(URL, caminho local relativo a dados/) de cada arquivo do período AAAA-MM a AAAA-MM."""
    a0, m0 = map(int, inicio.split("-"))
    a1, m1 = map(int, fim.split("-"))
    lista = []
    a, m = a0, m0
    while (a, m) <= (a1, m1):
        lista.append((url(f"Voo Regular Ativo (VRA)/{a}/{m:02d} - {MESES[m - 1]}/VRA_{a}{m}.csv"),
                      f"vra/VRA_{a}{m:02d}.csv"))
        a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    lista.append((url("Dados Estatísticos do Transporte Aéreo/Dados_Estatisticos.csv"),
                  "estatisticas/Dados_Estatisticos.csv"))
    for ano in range(a0, a1 + 1):
        if ano in ANOS_RECLAMACOES:
            lista.append((url(f"Dados do consumidor.gov/dadosconsumidor{ano}.csv"),
                          f"reclamacoes/dadosconsumidor{ano}.csv"))
    return lista


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def baixar(endereco: str, destino: Path, tentativas: int = 3) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporario = destino.with_suffix(destino.suffix + ".parcial")
    for n in range(1, tentativas + 1):
        try:
            req = urllib.request.Request(endereco, headers={"User-Agent": "manual-analise-de-dados/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r, temporario.open("wb") as f:
                while bloco := r.read(1 << 20):
                    f.write(bloco)
            temporario.replace(destino)
            return
        except OSError as erro:
            if n == tentativas:
                raise
            print(f"  falhou ({erro}); nova tentativa em {5 * n} s", file=sys.stderr)
            time.sleep(5 * n)


def main(inicio: str, fim: str, forcar: bool = False) -> dict:
    """Baixa o que falta (ou tudo, com forcar) e devolve o manifesto."""
    anterior = json.loads(MANIFESTO.read_text(encoding="utf-8")) if MANIFESTO.exists() else {}
    registros = {r["arquivo"]: r for r in anterior.get("arquivos", [])}
    novos = []
    for endereco, relativo in arquivos(inicio, fim):
        destino = DADOS / relativo
        if forcar or not destino.exists():
            print(f"baixando {relativo}…")
            baixar(endereco, destino)
            registro = {"arquivo": relativo, "url": endereco, "bytes": destino.stat().st_size,
                        "sha256": sha256(destino),
                        "baixado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        else:
            registro = registros.get(relativo) or {"arquivo": relativo, "url": endereco}
            if registro.get("bytes") != destino.stat().st_size or "sha256" not in registro:
                registro.update(bytes=destino.stat().st_size, sha256=sha256(destino),
                                baixado_em=registro.get("baixado_em", "desconhecido"))
        novos.append(registro)
    manifesto = {"fonte": "ANAC (dados abertos), https://sistemas.anac.gov.br/dadosabertos/",
                 "periodo": {"inicio": inicio, "fim": fim},
                 "total_bytes": sum(r["bytes"] for r in novos),
                 "arquivos": novos}
    MANIFESTO.write_text(json.dumps(manifesto, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(novos)} arquivos, {manifesto['total_bytes'] / 1e6:,.0f} MB em {DADOS.relative_to(AQUI.parent)}/")
    return manifesto


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--inicio", default="2023-01", help="primeiro mês do VRA, AAAA-MM")
    p.add_argument("--fim", default="2026-08", help="último mês do VRA, AAAA-MM")
    p.add_argument("--forcar", action="store_true", help="baixa de novo mesmo os arquivos que já existem")
    a = p.parse_args()
    main(a.inicio, a.fim, a.forcar)
