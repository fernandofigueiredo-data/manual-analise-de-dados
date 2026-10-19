"""Catálogo de gráficos."""
from kit import code

SIT = {
    "comparacao": "Comparação",
    "tendencia": "Tendência",
    "distribuicao": "Distribuição",
    "relacao": "Relação",
    "composicao": "Composição",
}

CARDS = []


def card(**kw):
    CARDS.append(kw)


# ------------------------------------------------------------------ linha
card(
    id="g-linha", titulo="Linha", sit=["tendencia"],
    objetivo="Mostrar como uma medida contínua evolui ao longo do tempo.",
    escolha=["Séries temporais com intervalos regulares (dias, meses, anos).",
             "Quando o formato da trajetória (alta, queda, sazonalidade) é a mensagem.",
             "Até três ou quatro séries; acima disso, destaque uma e deixe as outras em cinza."],
    evite=["Categorias sem ordem natural: a linha sugere continuidade que não existe.",
           "Poucos pontos isolados no tempo (dois momentos pedem gráfico de inclinação).",
           "Muitas séries com cores diferentes, o famoso gráfico espaguete."],
    nota=[("k", "Knaflic recomenda a linha para dados contínuos, em especial o tempo, e lembra que, ao contrário das barras, ela não exige eixo começando no zero, desde que a escala não distorça a leitura."),
          ("r", "Use uma única cor para a série principal e rotule o último valor diretamente; isso dispensa legenda e grade.")],
    base="Dados do conjunto <code>flights</code>, o mesmo do seu notebook <em>4-plots-matriciais.ipynb</em> e da apostila de Seaborn da pasta <em>seaborn</em>.",
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>
            import seaborn as sns  # apenas para carregar o conjunto de dados

            voos = sns.load_dataset("flights")
            anual = voos.groupby("year")["passengers"].sum()
            crescimento = anual.iloc[-1] / anual.iloc[0]

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(anual.index, anual.values, color=AZUL, linewidth=2.5)
            ax.scatter(anual.index[-1], anual.iloc[-1], color=AZUL, zorder=3)
            ax.annotate(f"{anual.iloc[-1]:,.0f} mil".replace(",", "."),
                        (anual.index[-1], anual.iloc[-1]), xytext=(-8, 8),
                        textcoords="offset points", ha="right", color=AZUL, fontweight="bold")
            ax.set_title(f"Passageiros anuais cresceram {crescimento:.1f} vezes de 1949 a 1960".replace(".", ","))
            ax.set_ylabel("Passageiros por ano (milhares)")
            ax.set_ylim(0, anual.max() * 1.15)
            ax.set_xticks(anual.index[::2])
            plt.show()
        ''')),
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>

            voos = sns.load_dataset("flights")
            anual = voos.groupby("year", as_index=False)["passengers"].sum()
            crescimento = anual["passengers"].iloc[-1] / anual["passengers"].iloc[0]
            ultimo = anual.iloc[-1]

            fig, ax = plt.subplots(figsize=(7, 4))
            sns.lineplot(data=anual, x="year", y="passengers", color=AZUL, linewidth=2.5, ax=ax)
            ax.scatter(ultimo["year"], ultimo["passengers"], color=AZUL, zorder=3)
            ax.annotate(f"{ultimo['passengers']:,.0f} mil".replace(",", "."),
                        (ultimo["year"], ultimo["passengers"]), xytext=(-8, 8),
                        textcoords="offset points", ha="right", color=AZUL, fontweight="bold")
            ax.set_title(f"Passageiros anuais cresceram {crescimento:.1f} vezes de 1949 a 1960".replace(".", ","))
            ax.set(xlabel="", ylabel="Passageiros por ano (milhares)",
                   ylim=(0, anual["passengers"].max() * 1.15))
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ barras verticais
card(
    id="g-barras-v", titulo="Barras verticais", sit=["comparacao"],
    objetivo="Comparar a grandeza de poucas categorias, de preferência com ordem natural.",
    escolha=["Até cerca de sete categorias com nomes curtos.",
             "Categorias ordinais (dias, faixas etárias, trimestres).",
             "Quando a comparação de tamanhos é a mensagem principal."],
    evite=["Nomes longos de categoria (prefira barras horizontais).",
           "Eixo y que não começa no zero: o comprimento da barra deixa de ser proporcional ao valor.",
           "Dezenas de categorias: agrupe, filtre ou ordene em barras horizontais."],
    nota=[("k", "Para Knaflic, gráficos de barras precisam de linha de base em zero, porque o olho compara o comprimento das barras."),
          ("r", "Com <code>ax.bar_label</code> os valores vão para o topo das barras e o eixo y pode sair; a cor marca só a categoria que interessa."),
          ("r", "No seaborn 0.13, para colorir cada barra use <code>hue</code> igual ao eixo x com <code>legend=False</code>. O <code>dodge=False</code> evita que as barras fiquem estreitas e deslocadas, efeito observado ao gerar este guia com pandas 3.")],
    base="Adaptado de <code>sns.barplot(x='sex', y='total_bill', data=tips)</code>, do seu notebook <em>2-plots-categoricos.ipynb</em>.",
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>
            import seaborn as sns  # apenas para carregar o conjunto de dados

            gorjetas = sns.load_dataset("tips")
            media = gorjetas.groupby("day", observed=True)["total_bill"].mean()
            cores = [AZUL if dia == media.idxmax() else CINZA for dia in media.index]

            fig, ax = plt.subplots(figsize=(6, 4))
            barras = ax.bar(["Qui", "Sex", "Sáb", "Dom"], media.values, color=cores, width=0.65)
            ax.bar_label(barras, labels=[f"US$ {v:.2f}".replace(".", ",") for v in media.values],
                         padding=4, color="#595959")
            ax.set_title("Domingo tem a conta média mais alta da semana")
            ax.spines["left"].set_visible(False)
            ax.set_yticks([])
            plt.show()
        ''')),
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>

            gorjetas = sns.load_dataset("tips")
            cores = {"Thur": CINZA, "Fri": CINZA, "Sat": CINZA, "Sun": AZUL}

            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(data=gorjetas, x="day", y="total_bill", hue="day", palette=cores,
                        errorbar=None, width=0.65, legend=False, dodge=False, ax=ax)
            for barras in ax.containers:
                valor = barras.datavalues[0]
                ax.bar_label(barras, labels=[f"US$ {valor:.2f}".replace(".", ",")],
                             padding=4, color="#595959")
            ax.set_xticks(range(4), ["Qui", "Sex", "Sáb", "Dom"])
            ax.set(xlabel="", ylabel="")
            ax.set_yticks([])
            ax.set_title("Domingo tem a conta média mais alta da semana")
            sns.despine(left=True)
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ barras horizontais
card(
    id="g-barras-h", titulo="Barras horizontais", sit=["comparacao"],
    objetivo="Comparar e ordenar categorias, sobretudo quando os nomes são longos.",
    escolha=["Rankings: ordene do maior para o menor (ou ao contrário, se o foco for o pior).",
             "Nomes de categoria longos, que ficariam inclinados no eixo x.",
             "Muitas categorias (até umas quinze, com folga vertical)."],
    evite=["Séries temporais: o tempo se lê da esquerda para a direita.",
           "Ordem alfabética quando a mensagem é o ranking.",
           "Cores diferentes para cada barra sem motivo."],
    nota=[("k", "Knaflic aponta as barras horizontais como uma das formas mais versáteis para dados categóricos: a leitura começa pelo nome da categoria e segue até o valor."),
          ("r", "Em matplotlib, <code>barh</code> desenha de baixo para cima; <code>ax.invert_yaxis()</code> coloca o primeiro item da lista no topo.")],
    base=None,
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>

            canais = ["Aplicativo", "Site", "Chat", "E-mail", "Loja física", "Redes sociais", "Telefone"]
            satisfacao = [86, 78, 74, 69, 67, 61, 52]  # % de clientes satisfeitos (sintético)
            cores = [AZUL if c == "Aplicativo" else CINZA for c in canais]

            fig, ax = plt.subplots(figsize=(7, 4))
            barras = ax.barh(canais, satisfacao, color=cores, height=0.65)
            ax.invert_yaxis()  # maior valor no topo
            ax.bar_label(barras, fmt="%d%%", padding=4, color="#595959")
            ax.set_title("O aplicativo lidera a satisfação, 34 pontos acima do telefone")
            ax.spines[["left", "bottom"]].set_visible(False)
            ax.tick_params(left=False)
            ax.set_xticks([])
            plt.show()
        ''')),
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>
            import pandas as pd

            dados = pd.DataFrame({
                "canal": ["Aplicativo", "Site", "Chat", "E-mail", "Loja física", "Redes sociais", "Telefone"],
                "satisfacao": [86, 78, 74, 69, 67, 61, 52],  # % de clientes satisfeitos (sintético)
            })
            cores = {c: (AZUL if c == "Aplicativo" else CINZA) for c in dados["canal"]}

            fig, ax = plt.subplots(figsize=(7, 4))
            sns.barplot(data=dados, x="satisfacao", y="canal", hue="canal", palette=cores,
                        legend=False, dodge=False, width=0.65, ax=ax)
            for barras in ax.containers:
                ax.bar_label(barras, fmt="%d%%", padding=4, color="#595959")
            ax.set_title("O aplicativo lidera a satisfação, 34 pontos acima do telefone")
            ax.set(xlabel="", ylabel="")
            ax.set_xticks([])
            sns.despine(left=True, bottom=True)
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ barras empilhadas
card(
    id="g-empilhadas", titulo="Barras empilhadas (100%)", sit=["composicao", "comparacao"],
    objetivo="Mostrar como um todo se divide em partes e comparar essa divisão entre grupos.",
    escolha=["Pesquisas com escala (negativo, neutro, positivo).",
             "Poucos segmentos (dois a quatro) e ordem lógica entre eles.",
             "Quando a comparação importante é a do primeiro ou do último segmento."],
    evite=["Muitos segmentos: os do meio não têm linha de base comum e ficam difíceis de comparar.",
           "Quando o total absoluto importa mais que a proporção (use barras simples ou empilhadas absolutas)."],
    nota=[("k", "Knaflic observa que barras empilhadas facilitam comparar o total e a série que encosta na base, mas dificultam comparar os segmentos internos, que flutuam sem referência comum."),
          ("r", "Rotule os segmentos uma única vez, sobre a primeira barra, e dispense a legenda. Bordas brancas (<code>edgecolor='white'</code>) separam os blocos sem acrescentar tinta.")],
    base=None,
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>

            itens = ["Facilidade de uso", "Velocidade", "Clareza das faturas", "Suporte técnico"]
            negativo = np.array([12, 18, 25, 38])  # % de respostas (sintético)
            neutro = np.array([20, 24, 30, 27])
            positivo = 100 - negativo - neutro
            camadas = [("Negativo", negativo, "#7F7F7F", "white"),
                       ("Neutro", neutro, "#D9D9D9", "#404040"),
                       ("Positivo", positivo, AZUL, "white")]

            fig, ax = plt.subplots(figsize=(7.5, 3.8))
            esquerda = np.zeros(len(itens))
            for nome, valores, cor, cor_texto in camadas:
                barras = ax.barh(itens, valores, left=esquerda, color=cor, height=0.6,
                                 edgecolor="white", linewidth=1.5)
                ax.bar_label(barras, labels=[f"{v}%" for v in valores], label_type="center",
                             color=cor_texto, fontsize=9.5)
                # rótulo direto da camada, acima da primeira barra
                ax.text(esquerda[0] + valores[0] / 2, -0.45, nome, ha="center", va="bottom",
                        color="#595959" if cor != AZUL else AZUL, fontweight="bold", fontsize=9.5)
                esquerda += valores
            ax.set_ylim(len(itens) - 0.5, -0.9)  # primeiro item no topo
            ax.set_xlim(0, 100)
            ax.set_title("Suporte técnico é o único item com mais críticas do que elogios")
            ax.spines[["left", "bottom"]].set_visible(False)
            ax.tick_params(left=False)
            ax.set_xticks([])
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ dispersão
card(
    id="g-dispersao", titulo="Dispersão", sit=["relacao"],
    objetivo="Mostrar a relação entre duas variáveis numéricas e revelar grupos ou exceções.",
    escolha=["Investigar se duas medidas variam juntas.",
             "Destacar um subconjunto de pontos (clientes, lojas, mesas) que atende a um critério.",
             "Encontrar valores atípicos."],
    evite=["Milhares de pontos sobrepostos sem transparência (use <code>alpha</code>, hexágonos ou densidade).",
           "Quando uma das variáveis é categórica (prefira boxplot ou pontos agrupados)."],
    nota=[("k", "No livro, a dispersão aparece como o gráfico para relação entre duas variáveis, e a cor é usada para separar o grupo que merece atenção do restante."),
          ("r", "Desenhe primeiro os pontos de contexto em cinza e depois os destacados, para que fiquem por cima.")],
    base="Expande o <code>plt.scatter(x, y)</code> da seção de gráficos especiais do seu <em>matplotlib.ipynb</em>.",
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>
            import seaborn as sns  # apenas para carregar o conjunto de dados

            gorjetas = sns.load_dataset("tips")
            generosa = gorjetas["tip"] / gorjetas["total_bill"] >= 0.20
            contexto, destaque = gorjetas[~generosa], gorjetas[generosa]

            fig, ax = plt.subplots(figsize=(7, 4.2))
            ax.scatter(contexto["total_bill"], contexto["tip"], s=22, color=CINZA, alpha=0.6)
            ax.scatter(destaque["total_bill"], destaque["tip"], s=26, color=AZUL)
            ax.text(4, 8.6, f"Em azul, as {generosa.mean():.0%} de mesas que deixaram\n20% ou mais de gorjeta",
                    color=AZUL, va="top")
            ax.set_title("A gorjeta cresce com a conta, mas poucas mesas chegam a 20%")
            ax.set_xlabel("Valor da conta (US$)")
            ax.set_ylabel("Gorjeta (US$)")
            plt.show()
        ''')),
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>

            gorjetas = sns.load_dataset("tips")
            gorjetas["generosa"] = gorjetas["tip"] / gorjetas["total_bill"] >= 0.20
            gorjetas = gorjetas.sort_values("generosa")  # destacados desenhados por último

            fig, ax = plt.subplots(figsize=(7, 4.2))
            sns.scatterplot(data=gorjetas, x="total_bill", y="tip", hue="generosa",
                            palette={False: CINZA, True: AZUL}, s=26, edgecolor="none",
                            legend=False, ax=ax)
            ax.text(4, 8.6, f"Em azul, as {gorjetas['generosa'].mean():.0%} de mesas que deixaram\n20% ou mais de gorjeta",
                    color=AZUL, va="top")
            ax.set_title("A gorjeta cresce com a conta, mas poucas mesas chegam a 20%")
            ax.set(xlabel="Valor da conta (US$)", ylabel="Gorjeta (US$)")
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ histograma
card(
    id="g-histograma", titulo="Histograma", sit=["distribuicao"],
    objetivo="Mostrar como os valores de uma variável numérica se distribuem em faixas.",
    escolha=["Entender forma, centro, dispersão e assimetria de uma variável.",
             "Checar dados antes de calcular médias (a média engana em distribuições assimétricas).",
             "Comunicar onde está a maior parte dos casos."],
    evite=["Comparar muitos grupos sobrepostos (prefira boxplot, violino ou pequenos múltiplos).",
           "Poucas observações: o desenho depende demais do número de faixas (<code>bins</code>)."],
    nota=[("r", "Teste diferentes valores de <code>bins</code> na exploração; na explicação, escolha um e marque a referência que sustenta a mensagem, como a mediana."),
          ("k", "A distinção de Knaflic entre análise exploratória e explicativa se aplica bem aqui: o histograma costuma nascer exploratório e só vai para a apresentação se carregar uma conclusão.")],
    base="Adaptado de <code>sns.distplot(tips['total_bill'])</code>, do seu <em>1-plots-de-distribuicoes.ipynb</em>. A função <code>distplot</code> foi descontinuada; o substituto é <code>histplot</code>, como já mostra a apostila de Seaborn da sua pasta.",
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>
            import seaborn as sns  # apenas para carregar o conjunto de dados

            contas = sns.load_dataset("tips")["total_bill"]
            mediana = contas.median()

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(contas, bins=20, color=CINZA, edgecolor="white")
            ax.axvline(mediana, color=AZUL, linewidth=2)
            ax.text(mediana + 0.8, ax.get_ylim()[1] * 0.93,
                    f"Mediana: US$ {mediana:.2f}".replace(".", ","), color=AZUL, fontweight="bold")
            ax.set_title("Metade das contas fica abaixo de US$ 17,80")
            ax.set_xlabel("Valor da conta (US$)")
            ax.set_ylabel("Número de mesas")
            plt.show()
        ''')),
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>

            gorjetas = sns.load_dataset("tips")
            mediana = gorjetas["total_bill"].median()

            fig, ax = plt.subplots(figsize=(7, 4))
            sns.histplot(data=gorjetas, x="total_bill", bins=20, color=CINZA,
                         edgecolor="white", alpha=1, ax=ax)
            ax.axvline(mediana, color=AZUL, linewidth=2)
            ax.text(mediana + 0.8, ax.get_ylim()[1] * 0.93,
                    f"Mediana: US$ {mediana:.2f}".replace(".", ","), color=AZUL, fontweight="bold")
            ax.set_title("Metade das contas fica abaixo de US$ 17,80")
            ax.set(xlabel="Valor da conta (US$)", ylabel="Número de mesas")
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ boxplot
card(
    id="g-boxplot", titulo="Boxplot", sit=["distribuicao", "comparacao"],
    objetivo="Comparar distribuições entre grupos por meio de mediana, quartis e valores atípicos.",
    escolha=["Comparar a mesma medida em vários grupos de forma compacta.",
             "Público que conhece a leitura de quartis.",
             "Detectar valores atípicos por grupo."],
    evite=["Plateias leigas sem explicação de como ler a caixa.",
           "Distribuições bimodais: a caixa esconde os dois picos (use violino ou pontos)."],
    nota=[("r", "Ao apresentar, explique a leitura uma vez (a linha é a mediana; a caixa reúne a metade central dos dados) e use cor só na mediana, que costuma ser o ponto da conversa."),
          ("k", "Vale o princípio de Knaflic de pensar no público: se a plateia não conhece o formato, o custo de leitura precisa ser pago com texto explicativo.")],
    base="Adaptado de <code>sns.boxplot(x='day', y='total_bill', data=tips, palette='rainbow')</code>, do seu <em>2-plots-categoricos.ipynb</em>. A paleta arco-íris deu lugar a cinza com destaque na mediana.",
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>
            import seaborn as sns  # apenas para carregar o conjunto de dados

            gorjetas = sns.load_dataset("tips")
            grupos = [gorjetas.loc[gorjetas["day"] == d, "total_bill"] for d in ["Thur", "Fri", "Sat", "Sun"]]

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.boxplot(grupos, tick_labels=["Qui", "Sex", "Sáb", "Dom"], widths=0.5, patch_artist=True,
                       medianprops={"color": AZUL, "linewidth": 2.5},
                       boxprops={"facecolor": "#EDEDED", "edgecolor": CINZA},
                       whiskerprops={"color": CINZA}, capprops={"color": CINZA},
                       flierprops={"marker": "o", "markersize": 4, "markerfacecolor": CINZA,
                                   "markeredgecolor": "none"})
            ax.text(4.32, grupos[3].median(), "mediana", color=AZUL, va="center", fontsize=9.5)
            ax.set_title("No fim de semana, as contas são mais altas e mais dispersas")
            ax.set_ylabel("Valor da conta (US$)")
            plt.show()
        ''')),
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>

            gorjetas = sns.load_dataset("tips")

            fig, ax = plt.subplots(figsize=(7, 4))
            sns.boxplot(data=gorjetas, x="day", y="total_bill", color="#EDEDED", linecolor=CINZA,
                        width=0.5, medianprops={"color": AZUL, "linewidth": 2.5},
                        flierprops={"marker": "o", "markersize": 4, "markerfacecolor": CINZA,
                                    "markeredgecolor": "none"}, ax=ax)
            ax.text(3.32, gorjetas.loc[gorjetas["day"] == "Sun", "total_bill"].median(), "mediana",
                    color=AZUL, va="center", fontsize=9.5)
            ax.set_xticks(range(4), ["Qui", "Sex", "Sáb", "Dom"])
            ax.set_title("No fim de semana, as contas são mais altas e mais dispersas")
            ax.set(xlabel="", ylabel="Valor da conta (US$)")
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ violino
card(
    id="g-violino", titulo="Violino", sit=["distribuicao", "comparacao"],
    objetivo="Comparar a forma completa das distribuições entre grupos.",
    escolha=["Quando a forma importa: dois picos, cauda longa, concentração.",
             "Poucos grupos (dois a cinco) com bastante dado em cada um."],
    evite=["Amostras pequenas: a estimativa de densidade inventa curvas suaves onde há poucos pontos.",
           "Plateias leigas sem explicação (a largura representa densidade, não quantidade absoluta)."],
    nota=[("r", "Uma linha de referência (aqui, US$ 30) transforma a comparação de formas em uma pergunta objetiva: qual grupo tem mais casos acima do limite?")],
    base="Adaptado de <code>sns.violinplot(x='day', y='total_bill', data=tips, ...)</code>, do seu <em>2-plots-categoricos.ipynb</em>.",
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>
            import seaborn as sns  # apenas para carregar o conjunto de dados

            gorjetas = sns.load_dataset("tips")
            almoco = gorjetas.loc[gorjetas["time"] == "Lunch", "total_bill"]
            jantar = gorjetas.loc[gorjetas["time"] == "Dinner", "total_bill"]

            fig, ax = plt.subplots(figsize=(6.5, 4.2))
            partes = ax.violinplot([almoco, jantar], showmedians=True, widths=0.7)
            for corpo, cor in zip(partes["bodies"], [CINZA, AZUL]):
                corpo.set_facecolor(cor)
                corpo.set_edgecolor("none")
                corpo.set_alpha(0.6)
            for chave in ["cmins", "cmaxes", "cbars", "cmedians"]:
                partes[chave].set_color("#595959")
            ax.axhline(30, color="#7F7F7F", linewidth=1, linestyle="--")
            ax.text(2.42, 30, "US$ 30", color="#595959", va="center")
            ax.set_xticks([1, 2], ["Almoço", "Jantar"])
            ax.set_title(f"Contas acima de US$ 30: {(jantar > 30).mean():.0%} no jantar, "
                         f"{(almoco > 30).mean():.0%} no almoço")
            ax.set_ylabel("Valor da conta (US$)")
            plt.show()
        ''')),
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>

            gorjetas = sns.load_dataset("tips")
            acima = (gorjetas["total_bill"] > 30).groupby(gorjetas["time"], observed=True).mean()

            fig, ax = plt.subplots(figsize=(6.5, 4.2))
            sns.violinplot(data=gorjetas, x="time", y="total_bill", order=["Lunch", "Dinner"],
                           color=CINZA, inner="quart", linewidth=1, linecolor="#595959", ax=ax)
            ax.collections[1].set_facecolor(AZUL)  # destaca o jantar (segundo violino)
            for corpo in ax.collections[:2]:
                corpo.set_alpha(0.6)
            ax.axhline(30, color="#7F7F7F", linewidth=1, linestyle="--")
            ax.text(1.42, 30, "US$ 30", color="#595959", va="center")
            ax.set_xticks([0, 1], ["Almoço", "Jantar"])
            ax.set_title(f"Contas acima de US$ 30: {acima['Dinner']:.0%} no jantar, "
                         f"{acima['Lunch']:.0%} no almoço")
            ax.set(xlabel="", ylabel="Valor da conta (US$)")
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ heatmap
card(
    id="g-heatmap", titulo="Mapa de calor", sit=["comparacao", "tendencia", "relacao"],
    objetivo="Revelar padrões em uma tabela de duas dimensões usando a intensidade da cor.",
    escolha=["Tabelas mês × ano, dia × hora, produto × região.",
             "Matrizes de correlação na fase exploratória.",
             "Quando a plateia precisa dos números, mas também do padrão."],
    evite=["Escalas arco-íris ou divergentes para dados que só crescem (use um único matiz, do claro ao escuro).",
           "Quando a comparação exata entre células é a mensagem: a cor é imprecisa para isso."],
    nota=[("k", "Knaflic apresenta o mapa de calor como meio-termo entre tabela e gráfico: mantém os números e usa a saturação da cor para guiar o olho até os valores altos e baixos."),
          ("r", "Use <code>cmap='Blues'</code> (sequencial, um só matiz) e <code>cbar=False</code> quando os números já estão escritos nas células.")],
    base="Adaptado de <code>pvflights = flights.pivot_table(...)</code> e <code>sns.heatmap(pvflights, cmap='magma', ...)</code>, do seu <em>4-plots-matriciais.ipynb</em> e da apostila de Seaborn.",
    variantes=[
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>

            voos = sns.load_dataset("flights")
            tabela = voos.pivot_table(index="month", columns="year", values="passengers", observed=False)
            tabela.index = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(tabela, cmap="Blues", annot=True, fmt=".0f", annot_kws={"fontsize": 7.5},
                        linewidths=1, linecolor="white", cbar=False, ax=ax)
            ax.set_title("Julho e agosto são o pico de passageiros em todos os anos")
            ax.set(xlabel="", ylabel="")
            ax.tick_params(left=False, bottom=False)
            ax.tick_params(axis="y", labelrotation=0)
            plt.show()
        ''')),
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>
            import seaborn as sns  # apenas para carregar o conjunto de dados

            voos = sns.load_dataset("flights")
            tabela = voos.pivot_table(index="month", columns="year", values="passengers", observed=False)
            meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
            limiar = tabela.values.min() + 0.6 * (tabela.values.max() - tabela.values.min())

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.imshow(tabela.values, cmap="Blues", aspect="auto")
            for i in range(tabela.shape[0]):
                for j in range(tabela.shape[1]):
                    valor = tabela.values[i, j]
                    ax.text(j, i, f"{valor:.0f}", ha="center", va="center", fontsize=7.5,
                            color="white" if valor > limiar else "#262626")
            ax.set_xticks(range(tabela.shape[1]), tabela.columns)
            ax.set_yticks(range(12), meses)
            ax.spines[:].set_visible(False)
            ax.tick_params(left=False, bottom=False)
            ax.set_title("Julho e agosto são o pico de passageiros em todos os anos")
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ slopegraph
card(
    id="g-inclinacao", titulo="Gráfico de inclinação (slopegraph)", sit=["comparacao", "tendencia"],
    objetivo="Mostrar a mudança de várias categorias entre dois momentos.",
    escolha=["Antes e depois, dois anos, duas pesquisas.",
             "Quando a direção e a intensidade da mudança são a mensagem.",
             "Até uns dez itens, com destaque em poucos."],
    evite=["Mais de dois momentos (use linhas).",
           "Valores muito próximos, que sobrepõem os rótulos (ajuste manualmente ou use barras)."],
    nota=[("k", "Knaflic recomenda o gráfico de inclinação para comparar dois períodos ou pontos, porque a inclinação de cada linha comunica de uma vez o aumento ou a queda."),
          ("r", "Aqui o laranja aparece porque a mensagem é um alerta (a única queda). Os demais itens ficam em cinza e continuam legíveis como contexto.")],
    base=None,
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>

            regioes = ["Sudeste", "Sul", "Centro-Oeste", "Nordeste", "Norte"]
            em_2024 = [72, 70, 66, 61, 68]  # % de satisfação (sintético)
            em_2025 = [78, 75, 71, 69, 59]

            fig, ax = plt.subplots(figsize=(6.2, 5))
            for nome, antes, depois in zip(regioes, em_2024, em_2025):
                caiu = depois < antes
                cor = LARANJA if caiu else CINZA
                ax.plot([0, 1], [antes, depois], color=cor, linewidth=2.5 if caiu else 1.5, marker="o")
                ax.text(-0.05, antes, f"{nome}  {antes}%", ha="right", va="center", color=cor)
                ax.text(1.05, depois, f"{depois}%  {nome}", ha="left", va="center", color=cor,
                        fontweight="bold" if caiu else "normal")
            ax.set_xlim(-0.8, 1.8)
            ax.set_xticks([0, 1], ["2024", "2025"])
            ax.set_yticks([])
            ax.spines[["left", "bottom"]].set_visible(False)
            ax.tick_params(bottom=False)
            ax.set_title("Só o Norte piorou de 2024 para 2025")
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ cascata
card(
    id="g-cascata", titulo="Cascata (waterfall)", sit=["composicao"],
    objetivo="Decompor como se chega de um valor inicial a um valor final, passo a passo.",
    escolha=["Da receita ao lucro, do orçamento ao realizado, do quadro inicial ao final de pessoas.",
             "Quando cada etapa intermediária precisa aparecer com seu peso."],
    evite=["Muitas etapas pequenas (agrupe em \"outros\").",
           "Quando só o resultado final importa (um número em destaque basta)."],
    nota=[("k", "O livro apresenta a cascata como uma forma de separar as partes de uma mudança entre um ponto de partida e um ponto de chegada."),
          ("r", "Matplotlib não tem função própria: a cascata é um <code>ax.bar</code> com o argumento <code>bottom</code> calculado a partir do acumulado.")],
    base=None,
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>

            etapas = ["Receita\nbruta", "Impostos", "Custo dos\nprodutos", "Despesas\ncomerciais",
                      "Despesas\nadministrativas", "Lucro\nlíquido"]
            inicio = 1000                      # R$ mil (sintético)
            variacoes = [-180, -390, -150, -120]
            niveis = [inicio] + list(inicio + np.cumsum(variacoes))
            fim = niveis[-1]

            bases = [0] + niveis[1:] + [0]
            alturas = [inicio] + [-v for v in variacoes] + [fim]
            cores = ["#7F7F7F"] + [CINZA] * len(variacoes) + [AZUL]

            fig, ax = plt.subplots(figsize=(8, 4.2))
            barras = ax.bar(etapas, alturas, bottom=bases, color=cores, width=0.6)
            rotulos = [f"{inicio}"] + [f"-{-v}" for v in variacoes] + [f"{fim}"]
            cores_texto = ["white"] + ["#262626"] * len(variacoes) + ["white"]
            for barra, rotulo, cor in zip(barras, rotulos, cores_texto):
                ax.text(barra.get_x() + barra.get_width() / 2, barra.get_y() + barra.get_height() / 2,
                        rotulo, ha="center", va="center", color=cor, fontweight="bold")
            for i, nivel in enumerate(niveis):  # conectores entre as barras
                ax.plot([i + 0.3, i + 0.7], [nivel, nivel], color=CINZA, linewidth=1)
            ax.set_title(f"De cada R$ 1.000 faturados, só {fim / inicio:.0%} viram lucro")
            ax.set_ylabel("R$ mil")
            ax.spines["left"].set_visible(False)
            ax.set_yticks([])
            ax.tick_params(bottom=False)
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ pizza e rosca
card(
    id="g-pizza", titulo="Pizza e rosca", sit=["composicao"],
    objetivo="Mostrar a participação de cada parte em um todo.",
    escolha=["Duas ou três partes, com uma delas claramente dominante.",
             "Quando a ideia de \"parte de um todo\" precisa ser imediata para uma plateia leiga."],
    evite=["Mais de três ou quatro fatias, ou fatias de tamanho parecido.",
           "Comparar pizzas lado a lado (ninguém compara ângulos com precisão).",
           "3D, fatias explodidas e legendas distantes das fatias."],
    nota=[("k", "Knaflic é explicitamente crítica a pizzas e roscas: nossos olhos comparam mal ângulos e áreas, e a rosca piora a tarefa ao pedir que se comparem comprimentos de arco. Ela sugere barras horizontais como alternativa."),
          ("r", "Se o gráfico de pizza for exigência do público, limite a poucas fatias, ordene da maior para a menor a partir das 12 horas e destaque só a fatia da mensagem. A aba \"Alternativa\" mostra a mesma informação em barras.")],
    base=None,
    variantes=[
        dict(label="Pizza", lib="mpl", code=code(r'''
            <<MPL>>

            canais = ["Loja online", "Lojas físicas", "Marketplaces", "Revendedores"]
            participacao = [42, 27, 18, 13]  # % das vendas (sintético)
            cores = [AZUL, "#BFBFBF", "#D4D4D4", "#E6E6E6"]

            fig, ax = plt.subplots(figsize=(5.5, 4.5))
            _, _, percentuais = ax.pie(participacao, labels=canais, colors=cores, autopct="%d%%",
                                       startangle=90, counterclock=False,
                                       wedgeprops={"edgecolor": "white", "linewidth": 2},
                                       textprops={"color": "#404040"})
            percentuais[0].set_color("white")
            ax.set_title("A loja online responde por 42% das vendas")
            plt.show()
        ''')),
        dict(label="Rosca", lib="mpl", code=code(r'''
            <<MPL>>

            canais = ["Loja online", "Lojas físicas", "Marketplaces", "Revendedores"]
            participacao = [42, 27, 18, 13]  # % das vendas (sintético)
            cores = [AZUL, "#BFBFBF", "#D4D4D4", "#E6E6E6"]

            fig, ax = plt.subplots(figsize=(5.5, 4.5))
            ax.pie(participacao, labels=canais, colors=cores, startangle=90, counterclock=False,
                   wedgeprops={"width": 0.35, "edgecolor": "white", "linewidth": 2},
                   textprops={"color": "#404040"})
            ax.text(0, 0, "42%\nonline", ha="center", va="center", fontsize=16,
                    fontweight="bold", color=AZUL)
            ax.set_title("A loja online responde por 42% das vendas")
            plt.show()
        ''')),
        dict(label="Alternativa: barras", lib="mpl", code=code(r'''
            <<MPL>>

            canais = ["Loja online", "Lojas físicas", "Marketplaces", "Revendedores"]
            participacao = [42, 27, 18, 13]  # % das vendas (sintético)
            cores = [AZUL] + [CINZA] * 3

            fig, ax = plt.subplots(figsize=(6.5, 3))
            barras = ax.barh(canais, participacao, color=cores, height=0.6)
            ax.invert_yaxis()
            ax.bar_label(barras, fmt="%d%%", padding=4, color="#595959")
            ax.set_title("A loja online responde por 42% das vendas")
            ax.spines[["left", "bottom"]].set_visible(False)
            ax.tick_params(left=False)
            ax.set_xticks([])
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ pairplot
card(
    id="g-pairplot", titulo="Pairplot", sit=["relacao", "distribuicao"],
    objetivo="Explorar de uma vez as relações entre todos os pares de variáveis numéricas.",
    escolha=["Início da análise exploratória, para decidir onde olhar.",
             "Poucas variáveis numéricas (até umas seis) e uma categoria para colorir."],
    evite=["Apresentações para decisão: é um gráfico para quem analisa, não para quem decide.",
           "Muitas variáveis: a grade vira um mosaico ilegível."],
    nota=[("k", "Knaflic separa a análise exploratória (procurar o que é interessante) da explicativa (comunicar o que foi encontrado). O pairplot é a ferramenta típica da primeira etapa: depois dele, escolha um par e construa um gráfico explicativo."),
          ("r", "<code>corner=True</code> remove a metade espelhada da grade e corta a redundância pela metade.")],
    base="Adaptado de <code>sns.pairplot(iris, hue='species', palette='rainbow')</code>, do seu <em>6-pairgrid.ipynb</em>, e de <code>sns.pairplot(tips, hue='sex')</code>, do <em>1-plots-de-distribuicoes.ipynb</em>.",
    variantes=[
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>

            iris = sns.load_dataset("iris").rename(columns={
                "sepal_length": "Sépala, comprimento", "sepal_width": "Sépala, largura",
                "petal_length": "Pétala, comprimento", "petal_width": "Pétala, largura",
                "species": "Espécie"})
            cores = {"setosa": "#BFBFBF", "versicolor": "#7F7F7F", "virginica": AZUL}

            g = sns.pairplot(iris, hue="Espécie", palette=cores, corner=True, height=1.9,
                             diag_kind="kde", plot_kws={"s": 14, "alpha": 0.8, "edgecolor": "none"})
            sns.move_legend(g, "upper right", bbox_to_anchor=(0.92, 0.92), frameon=False)
            g.figure.suptitle("As pétalas separam bem as espécies; as sépalas, nem tanto",
                              x=0.02, ha="left", y=1.02, fontsize=13)
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ regressão
card(
    id="g-regressao", titulo="Regressão", sit=["relacao"],
    objetivo="Mostrar a tendência média da relação entre duas variáveis numéricas.",
    escolha=["Quando a pergunta é \"quanto Y muda quando X aumenta\".",
             "Comparar a mesma relação entre grupos (facetas com <code>col</code> ou <code>row</code>)."],
    evite=["Relações claramente não lineares sem ajuste adequado (<code>order</code>, <code>lowess</code>).",
           "Sugerir causalidade: a reta descreve associação."],
    nota=[("r", "Traduza a inclinação em linguagem de negócio no título (\"cada 10 dólares a mais rendem cerca de 1 dólar de gorjeta\"); isso transforma estatística em mensagem."),
          ("r", "<code>regplot</code> é de eixo (aceita <code>ax=</code>); <code>lmplot</code> é de figura e cria uma grade de facetas.")],
    base="Adaptado de <code>sns.lmplot(x='total_bill', y='tip', data=tips, col='time', ...)</code>, do seu <em>3-plots-de-regressoes.ipynb</em> e do capítulo de regressão da apostila.",
    variantes=[
        dict(label="seaborn", lib="sns", code=code(r'''
            <<SNS>>
            import numpy as np

            gorjetas = sns.load_dataset("tips")
            inclinacao, _ = np.polyfit(gorjetas["total_bill"], gorjetas["tip"], 1)

            fig, ax = plt.subplots(figsize=(7, 4.2))
            sns.regplot(data=gorjetas, x="total_bill", y="tip", ax=ax,
                        scatter_kws={"s": 20, "color": CINZA, "alpha": 0.7},
                        line_kws={"color": AZUL, "linewidth": 2.5})
            ax.set_title(f"Cada 10 dólares a mais na conta rendem cerca de US$ {10 * inclinacao:.2f} "
                         "de gorjeta".replace(".", ","))
            ax.set(xlabel="Valor da conta (US$)", ylabel="Gorjeta (US$)")
            plt.show()
        ''')),
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>
            import seaborn as sns  # apenas para carregar o conjunto de dados

            gorjetas = sns.load_dataset("tips")
            inclinacao, intercepto = np.polyfit(gorjetas["total_bill"], gorjetas["tip"], 1)
            x = np.linspace(gorjetas["total_bill"].min(), gorjetas["total_bill"].max(), 100)

            fig, ax = plt.subplots(figsize=(7, 4.2))
            ax.scatter(gorjetas["total_bill"], gorjetas["tip"], s=20, color=CINZA, alpha=0.7)
            ax.plot(x, intercepto + inclinacao * x, color=AZUL, linewidth=2.5)
            ax.set_title(f"Cada 10 dólares a mais na conta rendem cerca de US$ {10 * inclinacao:.2f} "
                         "de gorjeta".replace(".", ","))
            ax.set_xlabel("Valor da conta (US$)")
            ax.set_ylabel("Gorjeta (US$)")
            plt.show()
        ''')),
        dict(label="seaborn lmplot (facetas)", lib="sns", code=code(r'''
            <<SNS>>

            gorjetas = sns.load_dataset("tips")
            gorjetas["periodo"] = gorjetas["time"].map({"Lunch": "Almoço", "Dinner": "Jantar"})

            g = sns.lmplot(data=gorjetas, x="total_bill", y="tip", col="periodo", height=3.6,
                           aspect=1, scatter_kws={"s": 18, "color": CINZA, "alpha": 0.7},
                           line_kws={"color": AZUL, "linewidth": 2.5})
            g.set_titles("{col_name}", loc="left")
            g.set_axis_labels("Valor da conta (US$)", "Gorjeta (US$)")
            g.figure.suptitle("A relação entre conta e gorjeta é parecida no almoço e no jantar",
                              x=0.02, ha="left", y=1.04, fontsize=13)
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ jointplot
card(
    id="g-conjunta", titulo="Distribuição conjunta", sit=["relacao", "distribuicao"],
    objetivo="Ver ao mesmo tempo a relação entre duas variáveis e a distribuição de cada uma.",
    escolha=["Exploração de um par de variáveis que parece promissor.",
             "Quando a concentração dos dados (onde estão a maioria dos casos) importa tanto quanto a tendência."],
    evite=["Apresentações para plateia não técnica: três gráficos em um exigem esforço de leitura.",
           "Quando só a relação importa (uma dispersão simples basta)."],
    nota=[("r", "Com muitos pontos, troque <code>kind='scatter'</code> por <code>kind='hex'</code> (aba ao lado): cada hexágono conta quantos pontos caem nele e a sobreposição deixa de esconder dados.")],
    base="Adaptado de <code>sns.jointplot(x='total_bill', y='tip', data=tips, kind='scatter')</code> e <code>kind='hex'</code>, do seu <em>1-plots-de-distribuicoes.ipynb</em>.",
    variantes=[
        dict(label="seaborn (pontos)", lib="sns", code=code(r'''
            <<SNS>>

            gorjetas = sns.load_dataset("tips")
            faixa = gorjetas["total_bill"].between(10, 20).mean()

            g = sns.jointplot(data=gorjetas, x="total_bill", y="tip", kind="scatter", color=AZUL,
                              height=5.2, joint_kws={"s": 18, "alpha": 0.6, "edgecolor": "none"},
                              marginal_kws={"bins": 25, "color": CINZA, "edgecolor": "white"})
            g.ax_joint.axvspan(10, 20, color="#EDEDED", zorder=0)
            g.set_axis_labels("Valor da conta (US$)", "Gorjeta (US$)")
            g.figure.suptitle(f"{faixa:.0%} das contas ficam entre 10 e 20 dólares (faixa cinza)",
                              x=0.02, ha="left", y=1.02, fontsize=13)
            plt.show()
        ''')),
        dict(label="seaborn (hexágonos)", lib="sns", code=code(r'''
            <<SNS>>

            gorjetas = sns.load_dataset("tips")
            faixa = gorjetas["total_bill"].between(10, 20).mean()

            g = sns.jointplot(data=gorjetas, x="total_bill", y="tip", kind="hex", color=AZUL,
                              height=5.2, joint_kws={"gridsize": 18},
                              marginal_kws={"bins": 25, "edgecolor": "white"})
            g.set_axis_labels("Valor da conta (US$)", "Gorjeta (US$)")
            g.figure.suptitle(f"{faixa:.0%} das contas ficam entre 10 e 20 dólares",
                              x=0.02, ha="left", y=1.02, fontsize=13)
            plt.show()
        ''')),
    ],
)

# ------------------------------------------------------------------ texto simples
card(
    id="g-texto", titulo="Texto simples (número em destaque)", sit=["comparacao"],
    objetivo="Comunicar um ou dois números importantes sem a mediação de um gráfico.",
    escolha=["Quando há um único indicador ou uma comparação de dois valores.",
             "Painéis e slides em que o número é a mensagem."],
    evite=["Séries com muitos pontos: aí o gráfico mostra o padrão que o número esconde."],
    nota=[("k", "Knaflic sugere que, quando se tem só um ou dois números para comunicar, o texto simples em destaque costuma funcionar melhor que um gráfico, que gastaria espaço para dizer pouco."),
          ("r", "Em matplotlib, <code>fig.text</code> posiciona texto em coordenadas da figura (de 0 a 1), sem precisar de eixos.")],
    base=None,
    variantes=[
        dict(label="matplotlib", lib="mpl", code=code(r'''
            <<MPL>>

            fig = plt.figure(figsize=(6.5, 2.4))
            fig.text(0.03, 0.62, "73%", fontsize=54, fontweight="bold", color=AZUL, va="center")
            fig.text(0.37, 0.62, "dos clientes que usaram o novo autoatendimento\n"
                                 "resolveram o problema sem falar com um atendente",
                     fontsize=12.5, color="#404040", va="center")
            fig.text(0.03, 0.12, "Antes da mudança, eram 41%. Fonte: pesquisa interna (dados sintéticos).",
                     fontsize=9.5, color="#7F7F7F")
            plt.show()
        ''')),
    ],
)
