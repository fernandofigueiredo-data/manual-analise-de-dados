"""Seção 1: fundamentos de matplotlib e seaborn."""
from kit import code, switcher, nav, k, r, chips_eixos

ANATOMIA = code(r'''
    <<MPL>>

    meses = np.arange(1, 13)
    vendas = np.array([42, 45, 47, 46, 52, 55, 58, 57, 61, 64, 66, 70])

    fig, ax = plt.subplots(figsize=(8, 4.8))
    fig.set_facecolor("#EEF2F7")           # a Figure é a folha inteira
    ax.plot(meses, vendas, color=AZUL, linewidth=2.5, label="Vendas")
    ax.axhline(55, color=CINZA, linestyle="--", label="Meta")
    ax.set_ylim(30, 80)
    ax.set_xticks(meses)
    ax.set_title("Título: ax.set_title()")
    ax.set_xlabel("Rótulo do eixo x: ax.set_xlabel()")
    ax.set_ylabel("Rótulo do eixo y")
    ax.legend(frameon=False, loc="upper left")

    seta = dict(color=LARANJA, fontsize=9.5, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=LARANJA, lw=1.2))
    fig.text(0.62, 0.955, "Figure: todo o fundo azulado", color=LARANJA, fontsize=9.5,
             fontweight="bold", va="center")
    ax.annotate("Axes (área de plotagem)", xy=(10.6, 36), xytext=(7.6, 39), **seta)
    ax.annotate("Line2D: um Artist de dados", xy=(7, 58), xytext=(7.6, 48), **seta)
    ax.annotate("Legend", xy=(2.9, 75.5), xytext=(4.2, 75), va="center", **seta)
    ax.annotate("Spine (borda)", xy=(0, 0.3), xycoords="axes fraction",
                xytext=(0.07, 0.2), textcoords="axes fraction", **seta)
    ax.annotate("Tick e rótulo do tick", xy=(4, 30), xytext=(3.2, 33.5), **seta)
    plt.show()
''')

PYPLOT = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 5, 11)
    y = x ** 2

    # Interface pyplot: cada comando age sobre a figura e os eixos "atuais"
    plt.figure(figsize=(8, 3.5))
    plt.subplot(1, 2, 1)
    plt.plot(x, y, "r--")
    plt.title("plt.subplot(1, 2, 1)")
    plt.subplot(1, 2, 2)
    plt.plot(y, x, "g*-")
    plt.title("plt.subplot(1, 2, 2)")
    plt.tight_layout()
    plt.show()
''')

OO = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 5, 11)
    y = x ** 2

    # Interface orientada a objetos: você guarda a figura e cada Axes
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 3.5))
    axes[0].plot(x, y, color="#1F5FA8")
    axes[0].set_title("axes[0].plot(x, y)")
    axes[1].plot(y, x, color="#A6A6A6")
    axes[1].set_title("axes[1].plot(y, x)")
    for ax in axes:
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.tight_layout()
    plt.show()
''')

INSET = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 5, 11)
    y = x ** 2

    fig = plt.figure(figsize=(6.5, 4))
    eixo_principal = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # esquerda, base, largura, altura (0 a 1)
    eixo_inserido = fig.add_axes([0.2, 0.5, 0.4, 0.3])

    eixo_principal.plot(x, y, color="#1F5FA8")
    eixo_principal.set_xlabel("x")
    eixo_principal.set_ylabel("y")
    eixo_principal.set_title("Eixo principal")

    eixo_inserido.plot(y, x, color="#A6A6A6")
    eixo_inserido.set_title("Eixo inserido", fontsize=9)
    plt.show()
''')

ESTILOS_MPL = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    anos = np.arange(2018, 2026)
    valores = np.array([3.1, 3.4, 2.9, 3.8, 4.2, 4.0, 4.6, 5.1])
    estilos = ["default", "ggplot", "seaborn-v0_8-whitegrid", "bmh"]

    fig = plt.figure(figsize=(9, 5.5))
    for i, estilo in enumerate(estilos, start=1):
        with plt.style.context(estilo):  # o estilo vale só dentro do bloco
            ax = fig.add_subplot(2, 2, i)
            ax.plot(anos, valores, marker="o")
            ax.set_title(f'plt.style.context("{estilo}")', fontsize=10)
    fig.tight_layout()
    plt.show()
''')

ESTILOS_SNS = code(r'''
    import matplotlib.pyplot as plt
    import seaborn as sns

    gorjetas = sns.load_dataset("tips")
    estilos = ["darkgrid", "whitegrid", "white", "ticks"]

    fig = plt.figure(figsize=(9, 5.5))
    for i, estilo in enumerate(estilos, start=1):
        with sns.axes_style(estilo):  # equivalente local de sns.set_style
            ax = fig.add_subplot(2, 2, i)
            sns.countplot(data=gorjetas, x="sex", color="#A6A6A6", ax=ax)
            ax.set_title(f'sns.axes_style("{estilo}")', fontsize=10)
            ax.set(xlabel="", ylabel="")
            if estilo == "ticks":
                sns.despine(ax=ax)  # remove as bordas de cima e da direita
                ax.set_title('"ticks" + sns.despine()', fontsize=10)
    fig.tight_layout()
    plt.show()
''')

CAMADAS = code(r'''
    import matplotlib.pyplot as plt
    import seaborn as sns

    gorjetas = sns.load_dataset("tips")

    # seaborn desenha dentro de Axes do matplotlib...
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    sns.histplot(data=gorjetas, x="total_bill", bins=20, color="#A6A6A6",
                 edgecolor="white", ax=axes[0])
    sns.boxplot(data=gorjetas, x="day", y="total_bill", color="#EDEDED",
                linecolor="#7F7F7F", ax=axes[1])

    # ...e o acabamento continua sendo matplotlib
    axes[0].axvline(gorjetas["total_bill"].median(), color="#1F5FA8", linewidth=2)
    axes[0].set_title("sns.histplot(..., ax=axes[0])", loc="left", fontsize=10.5)
    axes[1].set_title("sns.boxplot(..., ax=axes[1])", loc="left", fontsize=10.5)
    axes[1].set_xticks(range(4), ["Qui", "Sex", "Sáb", "Dom"])
    for ax in axes:
        ax.set(xlabel="", ylabel="")
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    plt.show()
''')

FIGURA = code(r'''
    import matplotlib.pyplot as plt
    import seaborn as sns

    gorjetas = sns.load_dataset("tips")
    gorjetas["periodo"] = gorjetas["time"].map({"Lunch": "Almoço", "Dinner": "Jantar"})

    # Função de figura: cria a própria grade (FacetGrid) e devolve o objeto g
    g = sns.relplot(data=gorjetas, x="total_bill", y="tip", col="periodo",
                    color="#A6A6A6", height=3.4, aspect=1.1, s=18, edgecolor="none")
    g.set_titles("{col_name}")
    g.set_axis_labels("Valor da conta (US$)", "Gorjeta (US$)")
    for ax in g.axes.flat:              # cada faceta é um Axes comum
        ax.axline((0, 0), slope=0.15, color="#1F5FA8", linewidth=1.5)
    g.axes.flat[1].text(20, 9, "linha: gorjeta de 15%", color="#1F5FA8", fontsize=9)
    g.figure.suptitle("Função de figura: sns.relplot(..., col='periodo')", x=0.02,
                      ha="left", y=1.04, fontsize=12)
    plt.show()
''')


def html():
    nav(1, "fundamentos", "Fundamentos")
    nav(2, "f-anatomia", "Anatomia de uma figura")
    nav(2, "f-interfaces", "Duas interfaces")
    nav(2, "f-estilos", "Estilos e rcParams")
    nav(2, "f-seaborn", "Seaborn sobre matplotlib")
    nav(2, "f-escolha", "Quando usar cada um")
    nav(2, "f-api", "Atualizações de API")
    return f'''
<section id="fundamentos" class="secao">
  <p class="sobretitulo">Parte 1</p>
  <h2>Fundamentos</h2>
  <p class="lead">Antes de escolher um gráfico, vale saber do que ele é feito. Todo elemento que aparece na tela é um objeto que pode ser ajustado ou removido. É essa possibilidade de remover que torna o matplotlib uma boa ferramenta para aplicar as ideias de Knaflic.</p>

  <article class="bloco" id="f-anatomia">
    <h3>Anatomia de uma figura</h3>
    <p>O matplotlib organiza tudo em uma hierarquia. A <strong>Figure</strong> é a folha inteira. Dentro dela ficam um ou mais <strong>Axes</strong>, cada um uma área de plotagem com seus eixos x e y, bordas (<em>spines</em>), marcas (<em>ticks</em>), título e legenda. Tudo o que é desenhado (linhas, barras, textos) é um <strong>Artist</strong>.</p>
    <div class="nota-eixo">{chips_eixos(["desordem"])}<span>Cada elemento anotado abaixo é candidato a ser removido ou atenuado. Saber o nome dele é o primeiro passo para eliminar a desordem.</span></div>
    {switcher("anatomia", [dict(label="Anatomia anotada", lib="mpl", code=ANATOMIA)], alt="Anatomia de uma figura do matplotlib")}
  </article>

  <article class="bloco" id="f-interfaces">
    <h3>Duas interfaces: pyplot e orientada a objetos</h3>
    <p>A interface <strong>pyplot</strong> (<code>plt.plot</code>, <code>plt.title</code>) age sobre a figura “atual” e é prática para testes rápidos. A interface <strong>orientada a objetos</strong> (<code>fig, ax = plt.subplots()</code> e depois <code>ax.plot</code>, <code>ax.set_title</code>) deixa explícito em qual Axes cada comando age.</p>
    <p>{r("Use a interface orientada a objetos em tudo que vai para apresentação. Com vários gráficos na mesma figura, com seaborn ou com funções reutilizáveis de estilo, ela evita que um ajuste caia no gráfico errado. Todos os exemplos deste guia seguem esse padrão.")}</p>
    {switcher("interfaces", [
        dict(label="pyplot (estado)", lib="mpl", code=PYPLOT),
        dict(label="Orientada a objetos", lib="mpl", code=OO),
        dict(label="Eixos inseridos (add_axes)", lib="mpl", code=INSET),
    ], alt="Comparação entre interfaces do matplotlib")}
    <p class="base">Base: seções “Comandos básicos”, “Criando multiplots”, “Introdução ao método orientado a objetos” e “subplots()” do seu notebook <em>matplotlib.ipynb</em>, com os mesmos dados <code>x = np.linspace(0, 5, 11)</code> e <code>y = x ** 2</code>.</p>
  </article>

  <article class="bloco" id="f-estilos">
    <h3>Estilos e rcParams</h3>
    <p>A aparência padrão vem de um dicionário de configurações, o <code>plt.rcParams</code>. Um <strong>estilo</strong> é apenas um conjunto pronto de rcParams. Há três maneiras de aplicá-los:</p>
    <ul>
      <li><code>plt.style.use("nome")</code> muda o padrão da sessão inteira;</li>
      <li><code>with plt.style.context("nome"):</code> vale só dentro do bloco;</li>
      <li><code>plt.rcParams.update({{...}})</code> ajusta chaves específicas. É o que o preâmbulo dos exemplos deste guia faz.</li>
    </ul>
    <p>No seaborn, <code>sns.set_theme()</code> aplica estilo, contexto e paleta de uma vez; <code>sns.set_style()</code> controla fundo e grade; <code>sns.set_context()</code> escala fontes e linhas para <code>"paper"</code>, <code>"notebook"</code>, <code>"talk"</code> ou <code>"poster"</code>; <code>sns.despine()</code> remove bordas.</p>
    <div class="nota-eixo">{chips_eixos(["desordem", "designer"])}<span>{r("Nenhum estilo pronto segue à risca os princípios do livro: quase todos mantêm grade e bordas. Parta de <code>white</code> ou <code>ticks</code> e complete com o estilo da <a href='#r-estilo'>referência rápida</a>.")}</span></div>
    {switcher("estilos", [
        dict(label="Estilos do matplotlib", lib="mpl", code=ESTILOS_MPL),
        dict(label="Estilos do seaborn", lib="sns", code=ESTILOS_SNS),
    ], alt="Comparação de estilos")}
    <p class="base">Base: seu notebook <em>5-estilos-e-cores.ipynb</em> (<code>set_style</code>, <code>despine</code>, <code>set_context</code>) e o capítulo “Estilização” da apostila de Seaborn da pasta <em>seaborn</em>.</p>
  </article>

  <article class="bloco" id="f-seaborn">
    <h3>O papel do seaborn sobre o matplotlib</h3>
    <p>O seaborn não substitui o matplotlib: ele desenha <em>com</em> o matplotlib. O que ele acrescenta é uma camada estatística e orientada a DataFrames:</p>
    <ul>
      <li>recebe um DataFrame e nomes de colunas (<code>data=, x=, y=</code>);</li>
      <li>calcula estatísticas sozinho: médias com intervalo de confiança, densidades, regressões, contagens;</li>
      <li>mapeia variáveis para cor, tamanho e estilo (<code>hue</code>, <code>size</code>, <code>style</code>);</li>
      <li>cria grades de pequenos múltiplos com <code>col</code> e <code>row</code>.</li>
    </ul>
    <p>Suas funções se dividem em dois níveis. As <strong>funções de eixo</strong> (<code>histplot</code>, <code>boxplot</code>, <code>scatterplot</code>, <code>regplot</code>, <code>heatmap</code>...) desenham em um Axes e aceitam <code>ax=</code>. As <strong>funções de figura</strong> (<code>relplot</code>, <code>displot</code>, <code>catplot</code>, <code>lmplot</code>, <code>pairplot</code>, <code>jointplot</code>) criam a própria figura e devolvem um objeto de grade, como o <code>FacetGrid</code>. Em ambos os casos, o acabamento (títulos, anotações, cores de destaque) é feito com métodos do matplotlib.</p>
    {switcher("camadas", [
        dict(label="Funções de eixo", lib="sns", code=CAMADAS),
        dict(label="Funções de figura", lib="sns", code=FIGURA),
    ], alt="seaborn desenhando sobre matplotlib")}
    <p class="base">Base: seus notebooks <em>6-pairgrid.ipynb</em> (<code>PairGrid</code>, <code>FacetGrid</code>, <code>JointGrid</code>) e <em>3-plots-de-regressoes.ipynb</em> (<code>lmplot</code> com <code>col</code> e <code>row</code>).</p>
  </article>

  <article class="bloco" id="f-escolha">
    <h3>Quando usar cada um</h3>
    <p>{r("O critério deste guia: use seaborn quando a estatística ou a divisão em grupos for o trabalho pesado; use matplotlib quando o trabalho for de acabamento ou o gráfico não existir pronto. Na prática, gráficos explicativos costumam usar os dois.")}</p>
    <div class="tabela-wrap"><table>
      <thead><tr><th>Situação</th><th>Ferramenta</th><th>Motivo</th></tr></thead>
      <tbody>
        <tr><td>Dados brutos em DataFrame e você quer média, contagem ou intervalo de confiança</td><td>seaborn</td><td><code>barplot</code>, <code>countplot</code> e <code>pointplot</code> agregam sozinhos</td></tr>
        <tr><td>Distribuições, densidades e regressões</td><td>seaborn</td><td><code>histplot</code>, <code>kdeplot</code>, <code>violinplot</code>, <code>regplot</code> já calculam</td></tr>
        <tr><td>Pequenos múltiplos por categoria</td><td>seaborn</td><td><code>col=</code> e <code>row=</code> nas funções de figura</td></tr>
        <tr><td>Exploração de muitas variáveis</td><td>seaborn</td><td><code>pairplot</code>, <code>jointplot</code>, <code>heatmap</code></td></tr>
        <tr><td>Dados já agregados (poucos números prontos)</td><td>matplotlib</td><td>não há nada a calcular; <code>ax.bar</code> e <code>ax.plot</code> bastam</td></tr>
        <tr><td>Gráficos sem função pronta: cascata, inclinação, empilhadas, texto simples</td><td>matplotlib</td><td>montados com primitivas (<code>bar</code> com <code>bottom</code>, <code>plot</code>, <code>text</code>)</td></tr>
        <tr><td>Rótulos diretos, anotações, cor por elemento, layout fino</td><td>matplotlib</td><td>acesso direto a cada Artist</td></tr>
        <tr><td>Gráfico final para apresentação</td><td>os dois</td><td>seaborn desenha, matplotlib dá o acabamento</td></tr>
      </tbody>
    </table></div>
  </article>

  <article class="bloco" id="f-api">
    <h3>Atualizações de API no material das suas pastas</h3>
    <p>Alguns códigos dos seus notebooks e apostilas foram escritos para versões antigas. Este guia foi gerado com {{VERSOES}}. As trocas abaixo já estão aplicadas em todos os exemplos.</p>
    <div class="tabela-wrap"><table>
      <thead><tr><th>Onde aparece</th><th>Código antigo</th><th>Código atual</th></tr></thead>
      <tbody>
        <tr><td><em>1-plots-de-distribuicoes.ipynb</em>, exercícios</td><td><code>sns.distplot(tips['total_bill'])</code></td><td><code>sns.histplot(data=tips, x='total_bill', kde=True)</code>. O <code>distplot</code> foi descontinuado.</td></tr>
        <tr><td><em>2-plots-categoricos.ipynb</em></td><td><code>factorplot</code> (citado no texto)</td><td><code>sns.catplot(..., kind='bar')</code>, como o próprio notebook já usa no código</td></tr>
        <tr><td><em>3-plots-de-regressoes.ipynb</em>, apostila</td><td><code>lmplot(..., size=8)</code></td><td><code>lmplot(..., height=8)</code></td></tr>
        <tr><td>exercícios (titanic)</td><td><code>titanic.corr()</code></td><td><code>titanic.corr(numeric_only=True)</code>. No pandas atual, colunas de texto geram erro.</td></tr>
        <tr><td><em>2-plots-categoricos.ipynb</em></td><td><code>sns.boxplot(x='day', y='total_bill', data=tips, palette='rainbow')</code></td><td><code>palette</code> sem <code>hue</code> gera aviso no seaborn 0.13. Use <code>hue='day', legend=False</code> ou uma cor única com <code>color=</code>.</td></tr>
        <tr><td><em>6-pairgrid.ipynb</em></td><td><code>g.plot(sns.regplot, sns.distplot)</code></td><td><code>g.plot(sns.regplot, sns.histplot)</code></td></tr>
        <tr><td><em>matplotlib.ipynb</em></td><td><code>plt.boxplot(data, vert=True)</code></td><td><code>vert</code> está sendo substituído por <code>orientation='vertical'</code>; para rótulos, use <code>tick_labels=</code></td></tr>
        <tr><td><em>matplotlib.ipynb</em></td><td><code>ax.legend(loc=1)</code></td><td>prefira nomes: <code>loc='upper right'</code>. Melhor ainda, troque a legenda por <a href="#a-rotulos">rótulos diretos</a>.</td></tr>
        <tr><td>vários notebooks</td><td><code>%matplotlib inline</code></td><td>desnecessário no Jupyter atual, onde a exibição inline já é o padrão</td></tr>
      </tbody>
    </table></div>
  </article>
</section>
'''
