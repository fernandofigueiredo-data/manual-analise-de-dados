# Análise de Dados · Manual de referência

Site de referência em análise de dados e data science, em português do Brasil, que reúne em uma única trilha de aprendizado quatro materiais do mesmo autor:

- **Notebook mestre de análise de dados**: a espinha dorsal, da importação ao checklist final, com código, saídas e gráficos;
- **Guia matplotlib e seaborn com storytelling de dados**: fundamentos, catálogo de 16 gráficos, antes e depois, roteiro e erros comuns;
- **Guia do relatório profissional em dados**: do pedido à entrega, com briefing, listas de verificação, modelos de texto e relatório-modelo;
- **Manual de Machine Learning**: 43 modelos em cartões de 20 blocos, decisão, validação, diagnóstico de dataset no navegador, skill de decisão e auditoria técnica.

Stack: [Astro](https://astro.build) (site estático), [Pagefind](https://pagefind.app) (busca), Python e Node (gerador de conteúdo). Design system: *Developer / Data Science / AI* (`design-system/design-system-visual.md`), escuro por padrão, Inter e JetBrains Mono.

## Rodar localmente

Requisitos: Node 20 ou mais recente (testado com 24).

```bash
npm install
npm run build
npm run preview
```

O site abre em `http://localhost:4321`. A busca só existe depois do build (o índice é criado pelo Pagefind sobre `dist/`). Para desenvolvimento com recarga automática, `npm run dev` (sem busca).

O conteúdo gerado (`src/conteudo/` e `public/img/`) já está no repositório, então o build não precisa de Python.

## Regenerar o conteúdo a partir dos materiais de origem

As cópias dos materiais ficam em `gerador/origem/`. Para regenerar páginas e figuras:

```bash
uv venv --python 3.14 gerador/.venv
uv pip install --python gerador/.venv/bin/python -r gerador/requirements.lock
gerador/.venv/bin/python -m ipykernel install --prefix gerador/.venv --name analise-de-dados
npm run gerar:tudo
```

O estudo de caso com dados da ANAC (`gerador/estudo-de-caso/`) fica de fora dessas execuções: o notebook é versionado já executado, e o gerador só lê as saídas dele. Para baixar os dados (cerca de 1 GB, fora do git) e executá-lo de novo, `npm run gerar:caso`; detalhes em `gerador/estudo-de-caso/LEIAME.md`.

O gerador também usa o Node (já instalado para o site) para extrair os dados do manual de ML. `gerar:tudo` executa o notebook e os exemplos do guia de visualização (cerca de 3 minutos); `npm run gerar` reaproveita o notebook já executado em `gerador/cache/`. Na primeira execução, o seaborn baixa os conjuntos `tips`, `flights` e `iris`.

## Verificações

| Comando | O que verifica |
|---|---|
| `npm run verificar` | nenhum valor de cor, fonte ou espaçamento fora dos tokens (roda em todo build) |
| `npm run verificar:conteudo` | todo trecho de texto e código dos quatro materiais está no site (depois do build) |
| `npm run auditar:a11y` | axe-core (WCAG 2.2 AA) em todas as páginas, nos dois temas, e teste de teclado (com o preview rodando) |
| `npm run auditar:lighthouse` | Lighthouse móvel e desktop em páginas representativas (com o preview rodando) |
| `npm run capturas` | capturas em 375, 768 e 1440 px, claro e escuro (com o preview rodando) |

Os resultados ficam em `../docs/qualidade/` (do Lighthouse, só o `RESUMO.md` vai para o repositório) e as capturas em `../docs/capturas/`.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `gerador/` | gerador: `gerar.py` (orquestra), `notebook.py`, `guia_viz.py`, `guia_relatorio.py`, `guia_ml.py` e `extrair_ml.mjs` (manual de ML), `estudo_caso.py` (estudo de caso), `estrutura.py` (arquitetura da informação), `tema.py` (tema dos gráficos), `alt_notebook.py` (textos alternativos) |
| `gerador/estudo-de-caso/` | estudo de caso com dados da ANAC: notebook executado, download com hash, SQL do modelo estrela e agregados; os dados brutos ficam em `dados/`, fora do git |
| `src/scripts/gerado/` | script do diagnóstico de dataset e função de realce, copiados sem alteração do manual de ML |
| `gerador/origem/` | cópias dos materiais de origem, sem alterações |
| `src/conteudo/` | páginas geradas (JSON) e navegação |
| `src/styles/tokens.css` | tokens do design system: único arquivo com valores literais |
| `src/layouts/`, `src/pages/`, `src/components/`, `src/scripts/` | layout, rotas, componentes e comportamentos |
| `public/` | imagens geradas, fontes e downloads |
| `scripts/` | verificação de tokens, auditorias e capturas |

## Deploy

Pronto para a Vercel (`vercel.json`: framework Astro, `npm run build`, saída `dist/`). Defina a variável `SITE_URL` com a URL pública para gerar as URLs canônicas.
