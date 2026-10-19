# Observações e pendências

Erros, lacunas, duplicações e pontos que pedem decisão, encontrados ao montar o site (atualizado com o pacote de data science e o novo design system). Pela regra do projeto, **nada disso foi corrigido no conteúdo**: o site reproduz os materiais como estão. Cada item traz uma sugestão de tratamento.

Prioridade: **Alta** = afeta a leitura ou a coerência visual do site; **Média** = afeta a precisão de um trecho; **Baixa** = acabamento.

## Decisões pendentes

| # | Prioridade | Onde | Situação | Sugestão |
|---|---|---|---|---|
| V1 | Média | Guia de visualização: texto e código | **Figuras resolvidas:** as 62 figuras foram regeneradas no tema escuro, com as cores trocadas só na execução (azul → Ciano, laranja → Âmbar, cinza → cinza do tema, fundo branco → Grafite); a página Sobre explica isso ao leitor. **Fica pendente o texto:** o guia ainda diz “azul para destaque”, o código exibido define `AZUL = "#1F5FA8"` e `fig.set_facecolor("#EEF2F7")`, e o `.docx` diz “Destaque em azul”, enquanto a figura mostra Ciano. | Revisar o texto para “cor de destaque” ou “ciano”, numa futura passada de conteúdo; ou aceitar a diferença, já explicada na página Sobre. |
| C1 | Média | Todos os materiais | Diretriz nova do `PRODUCT.md`: consolidar conteúdos, exemplos e códigos repetidos quando necessário, sem eliminar conhecimento. **Ainda não aplicada:** esta rodada foi só de interface, por decisão de projeto. As duplicações candidatas estão na seção “Duplicações e divergências entre os materiais” (D1 a D9). | Fazer uma passada de conteúdo dedicada, decidindo item a item o que consolidar. |
| V3 | Média | Guia de relatório, Figuras 1 e 2 (SVG) e regras da etapa 5 | O texto diz “só o dado que importa está em azul”. No site, os gráficos SVG seguem o design system e o destaque é Ciano (a primeira cor categórica e o mais próximo de azul na paleta). | Trocar “em azul” por “em cor de destaque”, ou aceitar a leitura de ciano como azul. |
| V4 | Média | Manual de ML, “Convenções” e legenda | O manual descreve “16 categorias com código de cor”, “etiquetas coloridas”, “a borda esquerda do card usa a categoria mais específica” e destaques “azul contexto · amarelo cuidado · verde boa prática · vermelho erro”. O design system proíbe cores fora das quatro de acento e reserva o roxo para dado/modelo; por isso todas as etiquetas de categoria e as bordas dos cartões são roxas (a categoria é lida pelo rótulo), e o callout de contexto é neutro. Âmbar, verde e vermelho seguem como no texto. | Atualizar o texto das convenções (“etiquetas de categoria”, “destaque de contexto neutro”) ou decidir manter as 16 cores como exceção ao design system. |
| V2 | Média | Guia de visualização, 5 trechos marcados “a confirmar no livro” | Detalhes atribuídos a Knaflic que o próprio guia marca como não conferidos. | Conferir no livro e retirar o selo, ou remover o trecho. |

## Manual e guia de data science

| # | Prioridade | Onde | Observação | Sugestão |
|---|---|---|---|---|
| M1 | Média | Manual, “Como usar”, callout “Modo consulta em 5 segundos” | “A busca varre os **520 blocos** dos cards”: com 43 modelos de 20 blocos, são **860** blocos. O número parece ser da época em que o manual tinha 26 cartões (a auditoria §1 também cita “26/26 cards”). | Atualizar para 860, ou deixar sem número. |
| M2 | Média | Manual, início e “Atalhos da interface” | O texto descreve a interface do arquivo único: “Busca client-side”, “um único arquivo HTML, sem backend”, busca que “filtra cards e seções” na própria página, botão “Tema” que “fica salvo”, “Passe o mouse sobre o bloco e clique em copiar”, legenda que filtra “os cards do manual”. No site, o manual está dividido em 22 páginas: a busca é global (Pagefind), destaca os termos e abre os cartões na página de destino, mas não esconde seções; a legenda filtra o índice dos 43 modelos (e a matriz, quando na mesma página); o botão Copiar fica sempre visível. | Revisar os atalhos para a versão em site, ou manter o texto como descrição do arquivo `.html` original. |
| M3 | Baixa | `auditoria/rodar_tudo.sh` e `auditoria_ml.md` §10 | Os comentários e caminhos usam a pasta `htlm/` (`bash htlm/auditoria/rodar_tudo.sh`), e o próprio pacote se chama `data-science-htlm`: provável troca de letras em “html”. | Padronizar o nome da pasta. |
| M4 | Baixa | Manual, títulos das seções 6, 7, 8, 10, 16, 17 e 18 | O título traz uma etiqueta de categoria colada ao texto (“Regularização Regularização”, “Avaliação e validação Métricas”). No site, a etiqueta vira um selo ao lado do título. | Nenhuma; registrado porque a leitura do HTML original sem estilo repete a palavra. |
| M5 | Média | Auditoria | Os scripts da auditoria **não foram executados** na montagem do site: exigem dois ambientes Python próprios (3.14 com scikit-learn, boosting, PyTorch, Gymnasium; 3.12 com TensorFlow) e `libomp`. Os números da auditoria (69/69 trechos, 43/43 fórmulas etc.) são os do relatório entregue. | Rodar `bash auditoria/rodar_tudo.sh` antes de publicar e, se quiser, incorporar a execução ao processo de geração do site. |
| M6 | Baixa | Manual, “Diagnóstico do seu dataset” | O diagnóstico também roda no site, inteiro no navegador. Foi testado com o CSV de exemplo (2.412 linhas, 14 colunas → 16 itens e código inicial), não com arquivos XLSX ou JSON reais. | Testar com alguns arquivos reais antes de divulgar a ferramenta. |

## Notebook mestre

| # | Prioridade | Célula / seção | Observação | Sugestão |
|---|---|---|---|---|
| N1 | Alta | arquivo | O notebook foi entregue **sem saídas** (nenhuma tabela, texto impresso ou gráfico gravado). Para o site, ele foi executado do início ao fim; rodou sem erros com pingouin, scikit-posthocs e openpyxl instalados. | Nenhuma ação necessária; vale manter uma versão executada no repositório, se a ideia for ler o notebook no GitHub. |
| N2 | Baixa | célula 2 (seção 0) | A seção 0 usa título de nível 2 (`## 0. Roteiro rápido`), enquanto as seções 1 a 15 usam nível 1 (`# 1. …`). | Usar `#` também na seção 0. |
| N3 | Média | célula 203 (12.1), linha “α” | “padrão **0,05** (zona de "maioria" C = 95%)”: a expressão “zona de maioria C” não é explicada em nenhum outro ponto. | Trocar por “nível de confiança 1 − α = 95%”, se for esse o sentido. |
| N4 | Baixa | célula 40 (3.3) | O gráfico de nulos mostra o rótulo **“None”** no eixo x, porque o índice de `pct` não tem nome e o seaborn usa o nome do índice como rótulo. | Acrescentar `ax.set_xlabel('')`. |
| N5 | Baixa | células com `sns.boxplot` (6.3, 7.1, 8.3, 11.3) | Com matplotlib 3.11, o seaborn 0.13.2 usa internamente o parâmetro `vert`, já descontinuado (removido no matplotlib 3.13). No notebook o aviso fica oculto, porque o Jupyter só mostra avisos de descontinuação disparados no código do próprio usuário; na geração do guia ele apareceu (item G4). Quando o matplotlib 3.13 sair, esses gráficos podem quebrar se o seaborn não for atualizado. | Acompanhar a próxima versão do seaborn; nenhuma mudança no código do notebook resolve. |
| N6 | Baixa | célula 0 e seção 11.4 | O notebook sugere destacar com `palette=['#acacac', '#34ba34']` (cinza + verde), enquanto os guias usam cinza + azul. | Unificar a cor de destaque sugerida nos três materiais (ver V1 e V3). |
| N7 | Baixa | célula 105 (6.1) | O callout “O que observar” termina em “Confirme com:” e o código que completa a frase é a célula seguinte. No site isso funciona, mas o callout fica visualmente separado do código. | Mover a frase para fora do bloco “O que observar”, ou incluir o código no próprio Markdown. |

## Guia matplotlib e seaborn

| # | Prioridade | Onde | Observação | Sugestão |
|---|---|---|---|---|
| G1 | Média | Parte 3 (introdução) e “Como usar” (cartão “Para aprender a biblioteca”) | O texto manda usar “os filtros da barra lateral”. No site, a busca e os filtros do catálogo ficam no topo da lista de cartões. | Trocar por “os filtros no topo do catálogo”. |
| G2 | Média | Parte 1, “Atualizações de API no material das suas pastas”; parágrafos “Base: seu notebook …” | O texto fala diretamente com o autor (“suas pastas”, “seu notebook *matplotlib.ipynb*”), o que soa estranho para o público do site. | Reescrever em terceira pessoa (“nos materiais de estudo que deram origem ao guia”). |
| G3 | Baixa | Parte 3, Regressão (seaborn e lmplot) | As duas figuras mudam levemente a cada geração, porque o intervalo de confiança do `regplot`/`lmplot` usa reamostragem sem semente. As outras 60 figuras são idênticas às originais. | Passar `seed=0` (ou `n_boot` fixo com semente) nessas chamadas. |
| G4 | Baixa | Fundamentos (“Funções de eixo”) e Parte 3 (Boxplot, seaborn) | Aviso `MatplotlibDeprecationWarning: vert` durante a geração (ver N5). | Nenhuma ação no código do guia; acompanhar o seaborn. |
| G5 | Baixa | `README.md` do guia (na página Sobre) | As instruções (“Abra `guia_matplotlib_seaborn.html`…”, “rode `build.py`”) se referem ao pacote original, não ao site. | Manter para histórico ou trocar por um README do site. |

## Guia do relatório profissional

| # | Prioridade | Onde | Observação | Sugestão |
|---|---|---|---|---|
| R1 | Média | Início, “Como usar” | “O contador mostra o progresso por etapa e no total”: no site, como as etapas estão em páginas separadas, cada lista mostra o próprio progresso, e não há total. | Trocar por “O contador mostra o progresso de cada lista”, ou pedir a volta do total (gravando as marcações na sessão). |
| R2 | Baixa | Início, “Como usar” | “Navegue pelo menu lateral ou busque um termo”: continua válido, mas a busca do site é global (os três materiais), não só do guia. | Nenhuma, ou mencionar a busca global. |
| R3 | Baixa | `README.md` do guia | “Mantenha os dois arquivos na mesma pasta: o guia aponta para o modelo por um link relativo” não se aplica ao site, onde o modelo está em `/downloads/`. | Idem G5. |

Os números do relatório-modelo fictício foram conferidos e são internamente consistentes (por exemplo, 33,0% × 1.120 ≈ 370 atrasos da transportadora B, 370 / 640 = 57,8%; 3.297 − 12 − 85 = 3.200 pedidos; recompra total de 31%).

## Duplicações e divergências entre os materiais

O site mantém as três versões quando há repetição (regra de preservar o conteúdo) e as aproxima pela navegação. Onde as versões divergem:

| # | Tema | Divergência | Sugestão |
|---|---|---|---|
| D1 | Função `descritivas()` | Notebook 5.5: inclui `IQR` e fixa a ordem das colunas. Guia de relatório, etapa 3: versão reduzida, sem `IQR` nem seleção de colunas. | Usar a versão do notebook nos dois lugares, ou dizer no guia que é uma versão resumida da seção 5.5. |
| D2 | Modelos de frase para reportar resultados | Notebook 14.2: 6 linhas, com “Correlação”. Guia de relatório, etapa 5: 5 linhas, sem “Correlação”. | Incluir a linha de correlação no guia. |
| D3 | “Qual teste usar” | Notebook 12.2: inclui um grupo contra referência, proporções/A/B e pós-testes. Guia de relatório, etapa 3: tabela reduzida. | Manter a reduzida no guia com um link para a 12.2 (o site já liga as páginas pela trilha). |
| D4 | Parâmetros de leitura de arquivo | Notebook 2.1: 7 situações. Guia de relatório, etapa 2: 5 situações. | Idem D3. |
| D5 | Estratégias para nulos | Notebook 4.3 e guia de relatório, etapa 2: mesma tabela; o notebook tem a coluna “Código”. | Nenhuma; a repetição é intencional. |
| D6 | Funções desatualizadas | Notebook 11.5 e guia de visualização, “Atualizações de API”: listas que se sobrepõem em parte (`distplot`, `factorplot`, `size=`, `corr()`), cada uma com itens que a outra não tem. | Unificar numa única tabela e citá-la nos dois lugares. |
| D7 | “Qual gráfico usar” | Três tabelas com recortes diferentes: notebook 11.1, guia de visualização (pergunta → gráfico) e guia de relatório (etapa 5). | Manter as três (públicos diferentes) e citar o catálogo como referência principal. |
| D9 | Pré-processamento, validação, pipeline e checklist | Notebook 4, 12, 14.5 e 15 e manual de ML 8, 10, 11 e 15 tratam os mesmos temas com focos diferentes (análise × modelagem). Não há contradição, mas o leitor encontra quatro checklists. | Citar, no checklist do notebook, o checklist profissional do manual para projetos de modelagem. |
| D8 | Do resultado ao insight; estrutura do relatório | Notebook 14.1 e 14.4 e guia de relatório, etapas 3 e 4: mesmo conteúdo; o guia expande o notebook. | Nenhuma; no site, a página 14 do notebook vem logo antes das etapas 4 a 6. |
