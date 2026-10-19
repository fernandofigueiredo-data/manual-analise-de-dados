---
title: Design System — Developer / Data Science / AI
version: 1.0
author: Fernando Figueiredo
data: 2026-09-24
escopo: identidade visual reutilizável para dashboards, produtos de dados, landing pages e apresentações técnicas
---

# Design System — Developer / Data Science / AI

Sistema derivado da identidade visual aplicada ao macOS (Navy/Ciano/Verde/Roxo), generalizado para qualquer superfície de software: web, dashboards, CLIs, apresentações. Princípio único: escuridão como padrão, cor como sinal, nunca como decoração. Cada cor de acento tem exatamente uma função semântica e não circula livremente pela interface.

## 1. Paleta

| Token | Hex | RGB | Papel semântico |
|---|---|---|---|
| `--color-bg-base` | `#101522` | 16, 21, 34 | Navy. Fundo primário, a camada mais profunda. |
| `--color-bg-surface` | `#151C2B` | 21, 28, 43 | Grafite. Cards, painéis, sidebars — um nível acima do fundo. |
| `--color-bg-surface-raised` | `#202938` | 32, 41, 56 | Grafite secundário. Elementos elevados: modais, dropdowns, hover de card. |
| `--color-accent-primary` | `#00E5FF` | 0, 229, 255 | Ciano. Interação: links, foco, CTAs primários, cursor/prompt de terminal. |
| `--color-accent-success` | `#39FF88` | 57, 255, 136 | Verde. Sucesso, execução, código, estados "ok" e "rodando". |
| `--color-accent-data` | `#A970FF` | 169, 112, 255 | Roxo. IA, machine learning, dados, o domínio analítico — nunca interação. |
| `--color-accent-warning` | `#FFB84D` | 255, 184, 77 | Âmbar. Atenção, alerta, estados intermediários — nunca erro crítico. |
| `--color-text-primary` | `#F2F7FF` | 242, 247, 255 | Texto de leitura primária, títulos, corpo. |
| `--color-text-secondary` | `#AAB8CC` | 170, 184, 204 | Metadados, legendas, texto de apoio, placeholders. |

Regra de uso das quatro cores de acento: cada uma responde a uma pergunta diferente. Ciano responde "onde eu clico". Verde responde "isso funcionou". Roxo responde "isso é dado ou modelo". Âmbar responde "isso precisa da minha atenção". Se duas cores respondem à mesma pergunta em uma mesma tela, uma das duas está sobrando.

## 2. Matriz de contraste (WCAG 2.1)

Medido por luminância relativa, não por inspeção visual. Toda combinação abaixo é segura para produção; a única ressalva está marcada.

| Primeiro plano | Sobre Navy | Sobre Grafite | Sobre Grafite secundário |
|---|---|---|---|
| Texto primário | 16.94:1 (AAA) | 15.84:1 (AAA) | 13.60:1 (AAA) |
| Texto secundário | 9.06:1 (AAA) | 8.47:1 (AAA) | 7.27:1 (AAA) |
| Ciano | 11.85:1 (AAA) | 11.07:1 (AAA) | 9.51:1 (AAA) |
| Verde | 13.74:1 (AAA) | 12.84:1 (AAA) | 11.03:1 (AAA) |
| Roxo | 5.60:1 (AA) | 5.23:1 (AA) | **4.49:1 (AA-large)** |
| Âmbar | 10.60:1 (AAA) | 9.91:1 (AAA) | 8.51:1 (AAA) |

**Ressalva sobre Roxo em Grafite secundário**: 4.49:1 fica um centésimo abaixo do piso de 4.5:1 para texto normal. Use Roxo nessa superfície apenas em texto grande (≥18pt, ou ≥14pt em negrito), ícones, bordas ou preenchimentos — nunca em corpo de texto pequeno. Nas outras duas superfícies, Roxo é seguro em qualquer tamanho.

## 3. Tipografia

Duas famílias, papéis fixos.

- **Interface e prosa**: `Inter`, fallback `-apple-system, "SF Pro Text", system-ui, sans-serif`. Geométrica o suficiente para ler como técnica, sem ser fria.
- **Código, dados, terminal**: `"JetBrains Mono"`, fallback `"SF Mono", "Fira Code", ui-monospace, monospace`. Qualquer valor numérico em um dashboard, qualquer trecho de código, qualquer output de CLI usa mono — é o que sinaliza "isto é dado bruto, não prosa".

Escala (base 16px, razão 1.25):

| Token | Tamanho | Uso |
|---|---|---|
| `--font-size-xs` | 12.8px | legendas, metadados, timestamps |
| `--font-size-sm` | 14px | texto secundário, labels |
| `--font-size-base` | 16px | corpo |
| `--font-size-lg` | 20px | subtítulos, destaques |
| `--font-size-xl` | 25px | títulos de seção |
| `--font-size-2xl` | 31px | títulos de página |
| `--font-size-3xl` | 39px | hero, headline |

Peso: 400 para corpo, 500 para labels e botões, 600 para títulos. Nunca 700+ fora de headlines — negrito pesado em fundo escuro satura visualmente antes do necessário.

## 4. Espaçamento

Grid de 8px, sem exceções ad hoc.

`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96` (px)

Padding interno de componentes em múltiplos de 8; gaps entre componentes em múltiplos de 16; margens de seção em múltiplos de 32 ou 48.

## 5. Modelo de elevação

Três camadas, sem sombras — a profundidade vem da progressão tonal, não de drop-shadow, que em fundo escuro fica suja.

1. `--color-bg-base` (Navy): o chão. Body, fundo de página, fundo de dashboard.
2. `--color-bg-surface` (Grafite): a primeira elevação. Cards, painéis, sidebar, tabelas.
3. `--color-bg-surface-raised` (Grafite secundário): a segunda elevação. Modais, dropdowns abertos, tooltips, estado de hover de um card da camada 2.

Nunca pular uma camada (Navy direto para Grafite secundário) e nunca inventar uma quarta — se algo precisa de mais destaque que a camada 3, o destaque vem de cor de acento na borda, não de mais uma camada de cinza.

## 6. Componentes

**Botão primário**: fundo `--color-accent-primary`, texto Navy (não texto claro — Ciano é claro demais para texto branco em cima, o par correto é Ciano/Navy invertido). Hover: escurece 8%. Focus: anel de 2px em Ciano com 40% de opacidade.

**Botão secundário**: fundo transparente, borda 1px `--color-text-secondary`, texto `--color-text-primary`. Hover: borda vira Ciano.

**Badge/tag**: fundo da cor de acento a 15% de opacidade sobre a superfície, texto na cor de acento sólida, borda 1px na mesma cor a 30%. Um badge Roxo lê "dado/IA", um badge Verde lê "ativo/sucesso", um badge Âmbar lê "pendente/atenção" — a cor already carrega o significado, o texto do badge não deveria precisar repetir "sucesso" se a cor já é Verde.

**Bloco de código**: fundo `--color-bg-surface-raised`, fonte mono, borda-esquerda 2px Verde. Syntax highlight restrito à paleta: strings em Verde, keywords em Roxo, funções em Ciano, comentários em texto secundário. Não introduzir cores fora da paleta para highlight — se o tema de sintaxe do editor não couber nessas quatro cores, ele não é deste sistema.

**Card**: fundo `--color-bg-surface`, borda 1px `--color-bg-surface-raised`, raio 12px, padding 24px. Hover: fundo sobe para `--color-bg-surface-raised`, transição 150ms.

**Input**: fundo `--color-bg-surface`, borda 1px `--color-text-secondary` a 30% de opacidade, texto `--color-text-primary`. Focus: borda Ciano sólida, sem glow — glow é reservado para os casos descritos na seção 8.

**Gráficos e dashboards**: ver a diretriz de cores categóricas do skill `dataviz` para a lógica de atribuição de cor por série; dentro deste sistema, a ordem categórica é Ciano → Verde → Roxo → Âmbar, e uma quinta série em diante usa variações de luminância das mesmas quatro, nunca uma cor nova.

## 7. Estados de interação

| Estado | Regra |
|---|---|
| Hover | escurecer 8% (superfícies) ou clarear 8% (acentos), nunca trocar de cor |
| Active/pressed | escurecer 15% |
| Focus | anel de 2px na cor de acento relevante ao contexto, opacidade 40% |
| Disabled | opacidade 40% no elemento inteiro, sem alteração de cor |
| Erro | usar `--color-accent-warning`; este sistema não define um vermelho — se um projeto precisar de estado de erro distinto de atenção, adicionar um vermelho de baixa saturação (`#FF5C5C` sugerido, validar contraste antes de adotar) em vez de usar Âmbar para as duas coisas |

## 8. Onde o glow é permitido

Regra restritiva: brilho/glow (`box-shadow` ou `filter: blur` colorido) é permitido em no máximo um elemento por tela — o ponto de maior importância hierárquica (ex.: o CTA principal, o nó ativo de um grafo, o cursor piscando em uma demo de terminal). Fora desse único ponto, zero glow. É a diferença entre "sofisticado" e "gamer RGB": um sistema onde tudo brilha não comunica hierarquia, comunica ruído.

## 9. O que este sistema proíbe

- Gradientes saturados cobrindo áreas grandes (>10% da tela)
- Mais de um elemento com glow simultâneo na mesma tela
- Vermelho e verde saturados lado a lado (a leitura fica infantil/semáforo)
- Preenchimento de fundo em branco ou cinza claro — este sistema é dark-first; um modo claro, se necessário, é um sistema derivado à parte, não uma inversão automática de tokens
- Uso de Roxo para qualquer ação clicável — Roxo é território de dados, Ciano é território de interação, a troca quebra a semântica do sistema inteiro
- Sombra cinza tradicional (`box-shadow: 0 4px 6px rgba(0,0,0,.1)`) — usar elevação por camada tonal (seção 5)

## 10. Tokens — CSS

```css
:root {
  --color-bg-base: #101522;
  --color-bg-surface: #151C2B;
  --color-bg-surface-raised: #202938;

  --color-accent-primary: #00E5FF;
  --color-accent-success: #39FF88;
  --color-accent-data: #A970FF;
  --color-accent-warning: #FFB84D;

  --color-text-primary: #F2F7FF;
  --color-text-secondary: #AAB8CC;

  --font-family-ui: 'Inter', -apple-system, 'SF Pro Text', system-ui, sans-serif;
  --font-family-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', ui-monospace, monospace;

  --font-size-xs: 0.8rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.563rem;
  --font-size-2xl: 1.953rem;
  --font-size-3xl: 2.441rem;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  --radius-base: 12px;
  --transition-base: 150ms ease;
}
```

## 11. Tokens — Tailwind (`tailwind.config`)

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        base: '#101522',
        surface: '#151C2B',
        'surface-raised': '#202938',
        primary: '#00E5FF',
        success: '#39FF88',
        data: '#A970FF',
        warning: '#FFB84D',
        'text-primary': '#F2F7FF',
        'text-secondary': '#AAB8CC',
      },
      fontFamily: {
        ui: ['Inter', '-apple-system', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"SF Mono"', '"Fira Code"', 'ui-monospace', 'monospace'],
      },
    },
  },
}
```

## 12. Aplicação por tipo de projeto

- **Dashboards de dados** (InstaAnalyser, sistema de dados automatizado): Navy de fundo, cards em Grafite, KPIs em texto primário grande, deltas positivos em Verde, deltas negativos em Âmbar (nunca vermelho saturado), séries de gráfico na ordem Ciano→Verde→Roxo→Âmbar.
- **Ferramentas com IA embutida** (Roteirista.IA, NarrativeOS): qualquer output gerado por modelo é marcado com um indicador Roxo discreto (borda, ícone ou badge), distinguindo visualmente "isto o modelo escreveu" de "isto você escreveu".
- **Landing pages e material de captação**: Navy dominante, um único CTA em Ciano por dobra de tela, Roxo reservado para badges de "powered by AI" ou seções que falam de dados/modelo.
- **Apresentações e decks técnicos**: fundo Navy, títulos em texto primário, um destaque de cor por slide no máximo — a mesma regra de glow da seção 8 se aplica a ênfase cromática em slides.

## 13. Checklist antes de aplicar a um novo projeto

- [ ] Fundo é uma das três superfícies, nunca branco ou cinza neutro
- [ ] Cada cor de acento aparece por uma única razão semântica na tela
- [ ] Nenhum texto pequeno em Roxo sobre Grafite secundário
- [ ] No máximo um elemento com glow por tela
- [ ] Código e valores numéricos estão em fonte mono, prosa está em Inter
- [ ] Gráficos seguem a ordem categórica Ciano→Verde→Roxo→Âmbar
