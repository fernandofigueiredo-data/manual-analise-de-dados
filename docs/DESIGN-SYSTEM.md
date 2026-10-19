# Design system do site

**Fonte única de verdade:** *Design System — Developer / Data Science / AI*, v1.0, de Fernando Figueiredo (24/09/2026), entregue em `design-system-visual.md` e copiado para `site/design-system/design-system-visual.md`. Ele substituiu integralmente o design system anterior, gerado pela skill ui-ux-pro-max (verde e âmbar, Exo e Roboto Mono). O anterior está guardado em `docs/historico/` só para rastreabilidade.

Implementação: `site/src/styles/tokens.css`. Nenhum outro arquivo de estilo declara cor, fonte, tamanho de fonte, espaçamento, raio ou duração fora de `var(--…)`; o build falha se encontrar um (`site/scripts/verificar-tokens.mjs`).

Princípio do sistema, aplicado em todo o site: **escuridão como padrão, cor como sinal, nunca como decoração.** Cada acento responde a uma única pergunta:

| Acento | Token | Pergunta | Onde aparece no site |
|---|---|---|---|
| Ciano `#00E5FF` | `--color-accent-primary` | onde eu clico? | links, botões, filtros ativos, aba selecionada, item atual da navegação, anel de foco, “+” dos cartões |
| Verde `#39FF88` | `--color-accent-success` | isso funcionou? | borda dos blocos de código, strings no código, “Copiado”, “versão forte”, barra de progresso das listas, callout de boa prática |
| Roxo `#A970FF` | `--color-accent-data` | isso é dado ou modelo? | etiquetas de categoria de ML, borda dos cartões de modelo, indicadores da página inicial, números dos blocos do cartão, ícone da marca |
| Âmbar `#FFB84D` | `--color-accent-warning` | precisa da minha atenção? | callouts “O que observar”/“Atenção”, linhas de código realçadas, selo “a confirmar no livro”, nível “ruim” da matriz |

## 1. Tokens de cor

### 1.1 Paleta do sistema (sem alteração)

| Token | Valor | Papel |
|---|---|---|
| `--color-bg-base` | `#101522` | Navy: fundo da página (camada 1) |
| `--color-bg-surface` | `#151C2B` | Grafite: cartões, painéis, navegação lateral, tabelas, cabeçalho (camada 2) |
| `--color-bg-surface-raised` | `#202938` | Grafite secundário: blocos de código, diálogos, hover de cartão, cabeçalho de tabela (camada 3) |
| `--color-accent-primary` | `#00E5FF` | Ciano |
| `--color-accent-success` | `#39FF88` | Verde |
| `--color-accent-data` | `#A970FF` | Roxo |
| `--color-accent-warning` | `#FFB84D` | Âmbar |
| `--color-text-primary` | `#F2F7FF` | texto |
| `--color-text-secondary` | `#AAB8CC` | metadados, legendas, rótulos |

### 1.2 Adotado da seção 7 do sistema

| Token | Valor | Motivo |
|---|---|---|
| `--color-accent-error` | `#FF5C5C` | O sistema não define vermelho, mas sugere este “vermelho de baixa saturação” quando o projeto precisar distinguir erro de atenção, depois de validar o contraste. O manual de ML tem callouts de “erro ou mito a desfazer” e os guias têm a “versão fraca”; o contraste foi validado: 6,02 / 5,63 / 4,83:1 nas três superfícies. |

### 1.3 Derivados (só misturas de cores da paleta)

| Token | Definição | Uso |
|---|---|---|
| `--color-on-accent` | = Navy | texto do botão primário (seção 6: “Ciano/Navy invertido”) |
| `--color-accent-data-text` | Roxo 85% + texto primário (`#B484FF`, 5,35:1 sobre o Grafite secundário) | roxo em **texto pequeno**; a seção 2 do sistema veta Roxo puro em texto pequeno sobre o Grafite secundário (4,49:1) |
| `--color-border` | = Grafite secundário | borda de cartão (seção 6) |
| `--color-border-strong` | = texto secundário | borda do botão secundário e dos filtros (seção 6) |
| `--color-border-input` | texto secundário 60% sobre o Grafite | contorno de campo |
| `--color-focus-ring` | Ciano a 60% | anel de foco |
| `--tint-*`, `--line-*` | acento a 15% e a 30% sobre o Grafite | fundo e borda de badge (seção 6) |
| `--hover-accent`, `--active-accent` | Ciano clareado 8% / escurecido 15% | estados do botão primário (seção 7) |
| `--glow-cta` | brilho Ciano | único glow permitido: o botão “Começar pela trilha” da página inicial (seção 8), declarado só na própria página |
| `--chart-guia-cinza`, `--chart-guia-azul`, `--chart-guia-laranja` | texto secundário 50% sobre o Grafite · Ciano · Âmbar | amostras de cor do guia de visualização: mostram as cores que aparecem nas figuras temáticas |

### 1.4 Contraste verificado (WCAG 2.1, luminância relativa)

| Par | Navy | Grafite | Grafite secundário |
|---|---|---|---|
| texto primário | 16,94 | 15,84 | 13,60 |
| texto secundário | 9,06 | 8,47 | 7,27 |
| Ciano | 11,85 | 11,07 | 9,51 |
| Verde | 13,74 | 12,84 | 11,03 |
| Roxo (só gráfico e texto grande) | 5,60 | 5,23 | 4,49 |
| Roxo para texto (`--color-accent-data-text`) | – | – | 5,35 |
| Âmbar | 10,60 | 9,91 | 8,51 |
| Vermelho de erro | 6,02 | 5,63 | 4,83 |
| Navy sobre Ciano (botão) | 11,85 | | |
| anel de foco (Ciano 60%) | 4,93 | 4,60 | |

A auditoria axe (WCAG 2.0, 2.1 e 2.2 A/AA) das 67 páginas indexadas, nos dois temas, não encontrou violações (`docs/qualidade/acessibilidade-axe.json`).

## 2. Tipografia (seção 3)

| Token | Valor | Uso |
|---|---|---|
| `--font-family-ui` | Inter (400, 500, 600; 700 só no título da página inicial) | interface e prosa |
| `--font-family-mono` | JetBrains Mono (400, 500) | código, saídas, tabelas de dados, números dos indicadores, selos de estado, gráficos do notebook |

Escala do sistema: `--font-size-xs` 0,8rem · `sm` 0,875rem · `base` 1rem · `lg` 1,25rem · `xl` 1,563rem (h2) · `2xl` 1,953rem (h1) · `3xl` 2,441rem (título da página inicial). Pesos: 400 corpo, 500 rótulos e botões, 600 títulos; 700 só no título da página inicial (“nunca 700+ fora de headlines”).

Medida de leitura: `--measure` 60ch (cerca de 76 caracteres de Inter) em parágrafos, listas e citações da prosa; tabelas ficam livres. Rótulos e títulos em caixa normal (sem caixa alta), com exceção de siglas.

As fontes são servidas pelo site (pacotes `@fontsource/inter` e `@fontsource/jetbrains-mono`, subconjunto latino, `font-display: swap`, Inter 400 e 600 pré-carregadas). Os gráficos do notebook usam JetBrains Mono, carregada no matplotlib a partir de TTF local.

## 3. Espaçamento, raio, movimento e elevação

- Grid de 8 px (seção 4): `--space-1` 4 · `2` 8 · `3` 12 · `4` 16 · `6` 24 · `8` 32 · `12` 48 · `16` 64 · `24` 96 px.
- Raio: `--radius-base` 12 px (seção 10) para cartões e painéis; `--radius-sm` 8 px (derivado do grid) para botões, campos e código; `--radius-full` para pílulas.
- Transição: `--transition-base` 150 ms (seção 10); zero com `prefers-reduced-motion`. Só cor, fundo, opacidade e `transform` são animados (a barra de progresso usa `scaleX`, não `width`).
- Alvo compacto: `--target-compact` 2,25rem (36 px) para o botão “Copiar” da barra de código, acima do mínimo de 24 px da WCAG 2.2 (2.5.8).
- **Elevação sem sombra** (seção 5): Navy → Grafite → Grafite secundário. Cartões e painéis no Grafite; código, diálogos e hover de cartão no Grafite secundário. Não há `box-shadow` no site, exceto o glow único da seção 8. Destaque além da camada 3 vem de **borda de 1 px na cor do acento a 30%** (`--line-*`) contornando o componente inteiro: cartões de modelo, callouts e caixas de diagnóstico. Não há faixas laterais grossas em cartões arredondados; a única borda lateral do site é a do bloco de código (2 px Verde), e por isso o bloco tem cantos retos.

## 4. Componentes

| Componente | Regra aplicada |
|---|---|
| Botão primário | Ciano com texto Navy; hover clareia 8%, pressionado escurece 15% |
| Botão secundário | transparente, borda 1 px texto secundário, texto primário; hover: borda Ciano |
| Badge/selo | acento a 15% no fundo, texto no acento (roxo em versão de texto), borda a 30%. Roxo = categoria de ML e “dados fictícios”; Âmbar = “a confirmar no livro”; demais selos neutros |
| Bloco de código | Grafite secundário, cantos retos, JetBrains Mono, borda esquerda 2 px Verde; saída encostada logo abaixo; realce restrito à paleta: strings Verde, palavras-chave Roxo (versão de texto), funções Ciano, comentários texto secundário, demais tokens texto primário; botão “Copiar” |
| Saída de código | Grafite, abaixo do bloco; texto em JetBrains Mono sobre Navy |
| Cartão | Grafite, borda 1 px Grafite secundário, raio 12, padding 24; hover: fundo sobe para o Grafite secundário em 150 ms |
| Campo | Grafite, borda texto secundário a 60%, texto primário; foco: borda Ciano sólida, sem glow |
| Callout | Grafite, raio 12, borda 1 px em volta: âmbar (atenção), verde (boa prática), vermelho (erro ou mito) a 30%; neutra para nota, alternativa, complemento e contexto; ícone SVG e título textual, a cor nunca é o único sinal |
| Tabela | Grafite, cabeçalho no Grafite secundário, hover da linha sobe uma camada; tabelas de dados e números em JetBrains Mono |
| Cartão de modelo (ML) | Grafite, borda 1 px Roxo a 30% em volta (seção 12: “output de modelo marcado com indicador Roxo”), etiquetas roxas, 20 blocos numerados |
| Abas, filtros | aba selecionada com fundo Navy, texto Ciano e peso 600 (sem sublinhado); filtro ativo em Ciano com texto Navy |
| Navegação | barra lateral no Grafite, item atual com fio Ciano de 1 px e fundo Grafite secundário, grupos (“Parte I — Base”) em texto secundário e caixa normal; barras de rolagem finas e cursor de texto Ciano |
| Cabeçalho de página | o título (h1) vem primeiro; módulo, selos e etiquetas ficam numa linha de metadados logo abaixo, em texto secundário (sem sobretítulo acima do título) |
| Página inicial | título, subtítulo, citação, ações e uma linha de fatos em JetBrains Mono; a trilha é uma lista ordenada (número, título, resumo, páginas), não grade de cartões nem bloco de indicadores |
| Figura | moldura no Grafite com borda; clique amplia em diálogo |

Ícones: SVG de traço único no estilo Lucide com `currentColor`. Nenhum emoji como ícone.

## 5. Modo escuro (padrão) e modo claro (derivado)

- O site abre **sempre no escuro**, independentemente da preferência do sistema operacional (“escuridão como padrão”).
- O botão do cabeçalho troca para o **sistema claro derivado**, gravado em `localStorage`. A seção 9 do sistema permite o claro só “como sistema derivado à parte, não uma inversão automática de tokens”; por isso ele foi desenhado com valores próprios em `:root[data-theme="light"]`:
  - fundos: `#F2F7FF` (o texto primário do escuro), `#E8EEF8` e `#DEE5F1` (misturas com o texto secundário), mantendo as três camadas;
  - texto: Navy e texto secundário escurecido (`#5D6677`);
  - acentos escurecidos com Navy até 4,5:1 sobre as três superfícies: Ciano `#0A687A`, Verde `#20734B`, Roxo `#6C4CA7`, Âmbar `#7C5E35`, Vermelho `#9F4045`;
  - badges com fundo a 8% (e não 15%), para o texto do acento manter 4,5:1;
  - sem glow.

## 6. Gráficos

**Notebook (36 figuras), regeneradas no tema do sistema** (`site/gerador/tema.py`):

| Elemento | Valor |
|---|---|
| Fundo da figura e dos eixos | Grafite `#151C2B` |
| Texto, títulos, rótulos | texto primário; marcas dos eixos em texto secundário |
| Grade | Grafite secundário |
| Ordem categórica | Ciano → Verde → Roxo → Âmbar; da 5ª série em diante, as mesmas quatro escurecidas com Navy (seção 6: “nunca uma cor nova”) |
| Sequencial `ds_seq` | variações de luminância do Roxo (dado), do Grafite ao Roxo claro |
| Divergente `ds_div` | Âmbar ← Grafite secundário → Ciano |
| Fonte | JetBrains Mono (gráfico é dado) |

**Guia de relatório (3 gráficos SVG):** desenhados com tokens e acompanham os dois temas. O destaque usa Ciano, a primeira cor categórica; o contexto usa o texto secundário atenuado.

**Guia de visualização (62 figuras), regeneradas no tema do sistema** (`site/gerador/guia_viz.py`). Como no notebook, as cores são trocadas **só na execução**; o código exibido continua o original:

| Cor do guia | Na figura |
|---|---|
| Cinza de contexto `#A6A6A6` | texto secundário 50% sobre o Grafite |
| Azul de destaque `#1F5FA8` | Ciano |
| Laranja `#D9731A` | Âmbar |
| Cinzas de texto (`#262626`, `#404040`, `#595959`, `#7F7F7F`) | texto primário ou secundário |
| Fundos claros (`#EEF2F7`, `#EDEDED`) e `"white"` | Grafite secundário / Grafite |

Exceções intencionais: as figuras que demonstram os estilos prontos do seaborn e do matplotlib (mostram cada estilo como ele é) e o mapa de calor com o colormap `Blues`, nomeado no texto. O registro de cada troca (305 trocas em 56 figuras) fica em `gerador/cache/relatorio.json`. O texto do guia ainda diz “azul”; ver `docs/OBSERVACOES.md`, V1.

## 7. Desvios em relação ao texto do sistema

| Regra do sistema | O que foi feito | Motivo |
|---|---|---|
| Foco: anel de 2 px a 40% de opacidade (seção 7) | 60% | a 40%, o anel tem 2,84:1 sobre o Navy, abaixo de 3:1 (WCAG 1.4.11) |
| Campo: borda texto secundário a 30% (seção 6) | 60% | idem: contorno de controle precisa de 3:1 |
| Palavras-chave do código em Roxo sobre o Grafite secundário (seção 6) | Roxo 85% + texto primário | o próprio sistema veta Roxo puro em texto pequeno nessa superfície (seção 2) |
| Sem vermelho (seção 1) | `#FF5C5C` adotado | previsto na seção 7, com contraste validado |
| Claro “se necessário” (seção 9) | sistema claro derivado, opcional | o projeto exige modo claro e escuro |
| Badge “não deveria repetir o texto que a cor já diz” (seção 6) | selos mantêm o rótulo | o rótulo é conteúdo dos materiais (por exemplo “Complemento”) e a cor sozinha não é acessível |
| Glow só no CTA (seção 8) | mantido, mas declarado na página inicial e não no CSS global | o glow fica restrito ao único ponto previsto |

## 8. Verificação automática do acabamento (impeccable)

A skill [impeccable](https://github.com/pbakaus/impeccable) v4.5.0 foi usada localmente (`.claude/skills/impeccable/` e `.impeccable/config.json`, fora deste repositório), com o contexto do produto em `docs/PRODUCT.md`. O detector (`impeccable detect site/dist`) roda sem achados primários; restam 7 avisos de excesso de travessão, que estão no texto dos materiais e não são alterados. Exceções registradas, todas por decisão deste design system:

| Regra do detector | Motivo da exceção |
|---|---|
| `overused-font` (Inter) | seção 3: Inter é a fonte de interface |
| `ai-color-palette` | seções 1 e 6: Navy, Ciano, Verde e Roxo são a paleta do sistema |
| `dark-glow` em `dist/index.html` | seção 8: o glow único do botão principal |

