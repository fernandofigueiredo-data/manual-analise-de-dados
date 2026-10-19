# Decisões de implementação

Registro atualizado em 01/10/2026, depois de duas mudanças pedidas pelo autor: a inclusão do **manual e guia de data science** (`data-science-htlm.zip`) e a troca completa do design system pelo **Design System — Developer / Data Science / AI** (`design-system-visual.md`).

## 1. Stack

| Camada | Escolha | Motivo |
|---|---|---|
| Site | **Astro 7** em modo estático (`build.format: directory`, CSS embutido no HTML) | gera HTML puro, sem framework de interface no navegador; rotas a partir de dados; empacota só o JavaScript de cada página; detectado automaticamente pela Vercel |
| Busca | **Pagefind 1.5** sobre `dist/` | índice estático gerado no build, carregado sob demanda, com radical da língua portuguesa, sub-resultados por âncora e destaque do termo na página de destino |
| Conteúdo | **gerador Python** (`site/gerador/`) que grava JSON em `src/conteudo/` | os materiais são Python, Jupyter ou HTML; o guia de visualização tem um motor próprio (`kit.py`) reaproveitado; o notebook precisa ser executado |
| Dados do manual de ML | **Node** (`gerador/extrair_ml.mjs`) | os 43 modelos e a matriz estão no JavaScript do manual; o próprio script do autor é executado num contexto isolado para extrair os dados, sem reescrevê-los |
| Interface | componentes Astro, CSS próprio e JavaScript sem dependências | controle total sobre os tokens: nenhum CSS de terceiros |
| Verificação | Playwright, axe-core e Lighthouse como dependências de desenvolvimento | auditorias reprodutíveis por `npm run` |

Alternativas descartadas: **Starlight** e **Docusaurus** trazem CSS próprio que violaria o critério “nenhum valor fora dos tokens”; **gerar HTML direto em Python** perderia o empacotamento de scripts por página e o caminho padrão de deploy na Vercel.

**Build reprodutível.** O conteúdo gerado (JSON, imagens e os scripts copiados do manual de ML) fica no repositório, então `npm run build` não depende de Python nem de rede. O build roda `verificar-tokens.mjs`, `astro build` e `pagefind`. Node travado em `package-lock.json` (versões exatas); Python em `gerador/requirements.lock`.

## 2. Design system

- **Fonte única:** `design-system-visual.md`, copiado para `site/design-system/`. A aplicação ao site, os tokens derivados e os desvios estão em `docs/DESIGN-SYSTEM.md`. O sistema anterior (skill ui-ux-pro-max) foi substituído integralmente e arquivado em `docs/historico/`.
- **Dark-first:** o site abre no escuro mesmo que o sistema operacional esteja no claro. O modo claro é um sistema derivado, com valores próprios, escolhido no botão do cabeçalho (a seção 9 do sistema veta a inversão automática de tokens).
- **Sem sombras:** elevação só por camada tonal (Navy, Grafite, Grafite secundário); um único glow, no botão principal da página inicial.
- **Semântica de cor aplicada componente a componente:** Ciano só no que é clicável; Verde em código e sucesso; Roxo em dado e modelo (etiquetas e cartões de ML, indicadores); Âmbar em atenção. Callouts de nota, alternativa e complemento ficaram neutros, porque nenhuma das quatro perguntas do sistema se aplica a eles.
- **Fontes:** Inter (interface e prosa) e JetBrains Mono (código, saídas, tabelas de dados, números), servidas pelo site.
- **Ajustes para AA**, todos documentados: anel de foco a 60%, borda de campo a 60%, versão de texto do Roxo, vermelho de erro adotado conforme a seção 7, tons de badge a 8% no claro.

## 3. Conteúdo

- **Fidelidade.** Texto e código vêm sempre das cópias em `site/gerador/origem/`. `gerador/verificar_conteudo.py` compara **10.292 trechos** (2.432 do notebook, 1.019 do guia de visualização, 552 do guia de relatório, 6.289 do pacote de ML: HTML estático, os 20 campos dos 43 modelos, a matriz, a skill, a auditoria, o README e os 7 scripts) com o site gerado. Resultado em `docs/verificacao-conteudo.json`: nenhum ausente.
- **Divisão em páginas** segue os títulos de origem (`docs/ARQUITETURA.md`). A seção 12 do notebook foi dividida em quatro páginas e a seção 2 em duas. O manual de ML virou 20 páginas (uma por seção, com “Início” e “Como usar” juntos e o diagnóstico à parte), mais a skill e a auditoria.
- **Títulos.** O título da seção vira o `h1` da página e os demais níveis foram ajustados para não pular nível. No manual de ML, os títulos que não tinham âncora ganharam uma a partir do texto, para o índice da página e a busca.
- **Marcadores do notebook** (⚠️ 🔹 ➕ 📘) viraram callouts, selos ou ícones SVG, porque o design system proíbe emoji como ícone.
- **Fórmulas** do notebook em MathML (`latex2mathml`), sem JavaScript.
- **Referências cruzadas.** “Seção 4.2” e afins viram links; links internos dos guias e do manual de ML (`#r-estilo`, `#s8-4`, `#m-xgboost`, `skill_decisao_ml.md`) apontam para a página certa.
- **Saídas do notebook.** O original não tinha saídas; elas vêm da execução do notebook inteiro (Python 3.14.7, pandas 3.0.5, NumPy 2.5.2, matplotlib 3.11.1, seaborn 0.13.2, SciPy, statsmodels, pingouin, scikit-posthocs), sem erros.
- **Guia de visualização.** Módulos de conteúdo e funções de `build.py` executados sem alteração; só a renderização do `kit.py` foi trocada (`gerador/guia_viz.py`). Com as versões fixadas iguais às do guia, 60 das 62 imagens saíam idênticas pixel a pixel às originais; depois, por sua escolha, foram regeneradas no tema do design system (ver 4.2).
- **Guia de relatório.** HTML original convertido para os componentes do site; script de interação portado.
- **Manual de ML.**
  - Os **43 cartões** e a **matriz dos sete critérios** são renderizados no build a partir dos dados do próprio manual, na mesma ordem e com o mesmo conteúdo das funções `cardHtml()` e `renderMatriz()`. Ficam no HTML (indexados pela busca e legíveis sem JavaScript), dentro de `details` recolhíveis.
  - A **legenda de categorias** filtra o índice dos 43 modelos na página de apresentação (os cartões agora estão em várias páginas) e, como no original, os filtros são combináveis.
  - **Expandir/Recolher**, abrir o cartão por link (`#m-xgboost`) e cartões expandidos na impressão foram portados. A busca do manual (destacar termos e abrir cartões) foi substituída pela busca global com destaque do Pagefind, que também abre os cartões que contêm o termo.
  - **Diagnóstico do dataset:** o script original (113 KB) roda sem nenhuma alteração, copiado pelo gerador para `src/scripts/gerado/`, junto com a função de realce de que ele depende. Só a marcação ao redor foi adaptada (contêiner `#diagnostico`, bloco do código inicial no componente do site). O arquivo continua sendo lido apenas no navegador.
  - **Skill e auditoria** em Markdown viraram páginas; o cabeçalho YAML da skill aparece como tabela “Metadados da skill”; os scripts da auditoria aparecem recolhíveis no fim da página. A skill e a auditoria também podem ser baixadas.
- **READMEs dos pacotes** (e o `.gitignore` do pacote de ML) estão na página `/sobre/`. Downloads sem alteração: modelo `.docx`, notebook `.ipynb`, `skill_decisao_ml.md`, `auditoria_ml.md`.

## 4. Gráficos

### 4.1 Notebook: tema do design system aplicado na execução

Uma célula oculta, inserida depois da 1.2, registra JetBrains Mono, os mapas `ds_seq`, `ds_div` e `ds_escura` e aplica `sns.set_theme` com fundo Grafite, texto do sistema e a ordem categórica Ciano → Verde → Roxo → Âmbar (`gerador/tema.py`). As cores fixadas no código e as barras de erro são trocadas **só no código executado**; o código exibido é sempre o original, e a página Sobre avisa o leitor.

| Células | No código | Na execução |
|---|---|---|
| 40, 117, 185, 194 | `'steelblue'`, `'#2a9d8f'` | Ciano |
| 111 | `'#453698'` (quartis) | texto secundário |
| 111, 192, 250 | `'red'` | Âmbar |
| 114 | `'green'` | Verde |
| 246 | `'#efab02'` | Âmbar |
| 110, 260 | `'black'` | texto primário (preto some no fundo escuro) |
| 194 | `'gray'` | texto secundário |
| 148 | `'lightgray'` | Grafite secundário |
| 162 | `linecolor='white'` | Grafite |
| 131, 153, 162, 171, 188 | `viridis`, `Blues`, `magma`, `YlGnBu` | `ds_seq` (luminâncias do Roxo) |
| 135 | `RdBu_r` | `ds_div` (Âmbar ↔ Ciano) |
| 149, 260 | `palette='viridis'` | `ds_escura` (Roxo escurecido, para o rótulo branco) |
| 149, 260 | `capsize=0.1,` | acrescenta `err_kws={'color': texto secundário}`: o seaborn desenha as barras de erro em cinza escuro, invisível no fundo escuro |

Registro completo em `gerador/cache/relatorio.json`. Dados, cálculos, tipos de gráfico e textos não mudam.

### 4.2 Guia de visualização e guia de relatório

- As 62 figuras do guia de visualização foram regeneradas no tema escuro, por sua escolha (V1, opção b). Como no notebook, as cores são trocadas só no código executado, por `gerador/guia_viz.py`: um prelúdio aplica o tema (fundo Grafite, texto, grade, JetBrains Mono, ordem categórica) e reaplica-o depois de `sns.set_theme`/`set_style`; as cores literais do guia viram cores do sistema (azul → Ciano, laranja → Âmbar, cinzas → cinzas do tema, `"white"` → Grafite, exceto nomes de estilo e a cor de texto escolhida por célula no mapa de calor). As figuras que demonstram os estilos prontos e o mapa `Blues` ficam como estão, porque o texto as descreve. 305 trocas em 56 figuras, registradas em `gerador/cache/relatorio.json`. As amostras de cor do guia no site passaram a mostrar as cores usadas.
- Os 3 gráficos SVG do guia de relatório usam tokens: acompanham os dois temas e destacam em Ciano (`OBSERVACOES.md`, V3).

### 4.3 Formato e acessibilidade

WebP sem perdas com `width`/`height` declarados e `loading="lazy"` (98 figuras, cerca de 2,4 MB); figuras ampliáveis em diálogo; texto alternativo escrito para cada figura do notebook (`gerador/alt_notebook.py`) e o do próprio guia nas demais.

## 5. Interface

- **Tokens:** `src/styles/tokens.css` é o único arquivo com valores literais; `scripts/verificar-tokens.mjs` falha o build se encontrar cor, fonte, tamanho, espaçamento, raio, sombra ou duração literal em outro CSS, atributo `style` em componentes ou conteúdo gerado, ou cor literal em SVG do conteúdo. Exceções pontuais exigem o comentário `token-exceção` (6 linhas: texto só para leitor de tela, opacidade de 40% do estado desabilitado, ícone de ampliar em duas regras, altura do código no guia, duração do indicador de carregamento). Fora do CSS: cor da `<meta name="theme-color">` e do `favicon.svg`.
- **Navegação:** barra lateral com sete módulos recolhíveis; no módulo Machine Learning, as páginas ficam agrupadas pelas partes do manual. Índice da página sempre presente (ignora títulos dentro de painéis ocultos); abaixo de 1200 px vira “Nesta página”; abaixo de 768 px a navegação vira gaveta.
- **Busca global** em diálogo (`/` ou `Ctrl/⌘ K`), com navegação por setas e destaque do termo na página de destino.
- **Guia de visualização:** busca e filtros do catálogo no topo da lista; links “onde aparece no código” atravessam páginas (`?eixo=`).
- **Guia de relatório:** progresso por lista (o “progresso geral” deixou de fazer sentido com o guia dividido em páginas); marcações não gravadas, como no original.

## 5.1 Refinamento com a skill impeccable

- **Instalação:** skill `impeccable` v4.5.0, usada localmente (`.claude/` e `.impeccable/`, fora deste repositório), com ganchos que rodam o detector a cada edição. Contexto do produto em `docs/PRODUCT.md`.
- **Escopo:** só interface, por sua escolha; o conteúdo dos materiais não mudou (`npm run verificar:conteudo` segue em 10.292 de 10.292).
- **Detector:** de 675 achados para 0 primários (7 avisos de travessão no texto dos materiais). O que mudou:
  - página inicial sem sobretítulo e sem bloco de indicadores; linha de fatos em JetBrains Mono; trilha como lista ordenada, materiais e páginas de módulo como listas, no lugar de grades de cartões;
  - sobretítulos acima do h1 viraram linha de metadados abaixo do título, em todas as páginas;
  - faixas laterais de 2 a 4 px em callouts, cartões de modelo, caixas e destaques trocadas por borda de 1 px em volta; o bloco de código mantém a borda Verde do sistema e ganhou cantos retos;
  - caixa alta retirada de rótulos longos; indicadores da navegação e do índice com 1 px;
  - medida de leitura de 72ch para 60ch (cerca de 76 caracteres);
  - títulos sem pular nível (o gerador ajusta h2 a h5);
  - barra de progresso animada por `transform`; imagem vazia do diálogo de figura criada só ao abrir; barra de código com mais respiro e alvo de 36 px;
  - barras de rolagem e cursor de texto no tema; glow do CTA restrito à página inicial.
- **Exceções do detector**, por regra do design system: fonte Inter, paleta Navy/Ciano/Verde/Roxo e glow do CTA. Na varredura por URL no celular restam dois falsos positivos: a gaveta de navegação fechada e os links do “Nesta página” recolhido.

## 5.2 Notebooks modelo de Machine Learning (06/10/2026)

- **Origem:** 10 notebooks de estudo (exercícios da *Machine Learning Specialization*). Todos tinham problemas (dependências ausentes, avaliação no treino, erros pontuais como o `-1` da árvore de decisão, a softmax instável, o vazamento de dados do recomendador e a API descontinuada do `gym`); a lista completa está em `docs/NOTEBOOKS-MODELO.md`. Os originais não foram alterados e, por serem material do curso, não estão neste repositório.
- **Correspondência:** cada notebook foi associado a um cartão já existente; nenhum modelo novo. Dois casos pedem decisão: a detecção de anomalias gaussiana ficou no cartão *GMM* (é um GMM de 1 componente com covariância diagonal; o cartão *Z-score* é univariado e exclui anomalias multivariadas) e o *Advice for Applying ML* ficou no cartão *Regressão Polinomial* (o modelo central do notebook, com a escolha de grau e λ que o cartão lista).
- **Formato dos templates:** uma única célula de configuração; dados sintéticos quando o caminho é `None`; pré-processamento ajustado só no treino; verificações automáticas no lugar dos testes do curso; métricas do cartão; comparação com a implementação de referência. Português do Brasil.
- **No site:** `NOTEBOOKS_MODELO` em `gerador/guia_ml.py` é a fonte única do mapeamento; ele gera o bloco de download no cartão, o selo “notebook modelo” no índice dos modelos, a cópia para `public/downloads/` e a lista da página Sobre. O bloco usa os componentes existentes (botão secundário pequeno, ícone de download) e só tokens.
- **Validação:** 30 execuções completas, mais 3 treinos completos do DQN (sementes 0, 1 e 2), em ambiente com TensorFlow 2.21, Keras 3.15, Gymnasium 1.4 e scikit-learn 1.9.1, com dados sintéticos, os dados originais quando disponíveis e datasets de outro formato. Resultados em `modelos/REVISAO_NOTEBOOKS.md`, seção 5.

## 6. Verificação

| Critério | Evidência |
|---|---|
| Build sem erros e site local | `npm run build` (tokens + Astro + Pagefind): 68 páginas geradas, 67 indexadas |
| Conteúdo completo | `docs/qualidade/verificacao-conteudo.json` (10.292 de 10.292 trechos) e tabela origem → página em `docs/ARQUITETURA.md` |
| Navegação, índice, busca, temas, copiar | em todas as páginas de conteúdo; botão Copiar em todos os 289 blocos de código |
| Responsivo 375 / 768 / 1440 | `docs/capturas/` (60 imagens: início, código, gráficos, catálogo, relatório-modelo, apresentação do manual de ML, cartão de modelo e diagnóstico executado, nos dois temas; menu móvel e busca) |
| WCAG AA, teclado, texto alternativo | `docs/qualidade/acessibilidade-axe.json`: axe-core (WCAG 2.0/2.1/2.2 A e AA) sem violações em 67 páginas × 2 temas; 21 de 21 passos de teclado, inclusive filtro de categoria, cartão de modelo e diagnóstico |
| Lighthouse ≥ 90 | `docs/qualidade/lighthouse/RESUMO.md`: 9 páginas, perfis móvel e desktop: desempenho 98 a 99, acessibilidade, boas práticas e SEO 100 |
| Tokens | `npm run verificar` |

O Lighthouse foi medido contra o build de produção servido localmente (`astro preview`), com a limitação de rede e CPU simulada do próprio Lighthouse; os números na Vercel só podem ser confirmados depois do deploy.

## 7. O que não foi feito

- Nenhum deploy, publicação ou repositório remoto; o projeto também não foi colocado sob controle de versão (`git init`), porque isso não foi pedido. O `.gitignore` está pronto.
- `SITE_URL` não definida: sem ela, o site não emite `<link rel="canonical">` nem sitemap.
- Os scripts da auditoria do manual de ML não foram executados (exigem ambientes próprios com TensorFlow, PyTorch e boosting); ver `OBSERVACOES.md`, M5.
