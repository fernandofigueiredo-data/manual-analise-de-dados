"""Referência rápida."""
from kit import code, switcher, nav, k, r

FUNCOES = r'''
    import matplotlib.pyplot as plt

    CINZA_ESCURO, CINZA, CINZA_CLARO = "#404040", "#A6A6A6", "#D9D9D9"
    AZUL, LARANJA = "#1F5FA8", "#D9731A"


    def estilo_explicativo(fonte=10.5):
        """Estilo enxuto, alinhado aos princípios de design de Knaflic."""
        plt.rcParams.update({
            "figure.facecolor": "white", "axes.facecolor": "white",
            "axes.spines.top": False, "axes.spines.right": False,
            "axes.edgecolor": "#BFBFBF", "axes.grid": False,
            "axes.titlelocation": "left", "axes.titlesize": fonte * 1.25,
            "axes.titlecolor": "#262626", "axes.titlepad": 10,
            "axes.labelcolor": "#595959", "axes.labelsize": fonte,
            "axes.prop_cycle": plt.cycler(color=[CINZA]),
            "xtick.color": "#595959", "ytick.color": "#595959",
            "xtick.major.size": 0, "ytick.major.size": 0,
            "legend.frameon": False, "font.size": fonte,
            "lines.linewidth": 2, "savefig.dpi": 200, "savefig.bbox": "tight",
        })


    def titulo(ax, texto, subtitulo=None):
        """Título com a conclusão e subtítulo opcional em cinza."""
        ax.set_title(texto, pad=26 if subtitulo else 10)
        if subtitulo:
            ax.text(0, 1.03, subtitulo, transform=ax.transAxes, color="#7F7F7F",
                    fontsize=plt.rcParams["font.size"] - 0.5)


    def destacar(barras, indices, cor=AZUL):
        """Pinta só as barras indicadas; as demais ficam em cinza."""
        for i, barra in enumerate(barras):
            barra.set_color(cor if i in indices else CINZA)


    def rotular_fim(ax, x, y, texto, cor=CINZA_ESCURO, negrito=False):
        """Rótulo direto ao fim de uma linha, no lugar da legenda."""
        ax.annotate(texto, (x[-1], y[-1]), xytext=(6, 0), textcoords="offset points",
                    va="center", color=cor, fontweight="bold" if negrito else "normal")


    def sem_eixo(ax, eixo="y"):
        """Remove um eixo quando os valores já estão escritos no gráfico."""
        if eixo == "y":
            ax.spines["left"].set_visible(False)
            ax.set_yticks([])
        else:
            ax.spines["bottom"].set_visible(False)
            ax.set_xticks([])


    def numero_br(valor, casas=0):
        """Formata número no padrão brasileiro: 1.234,5"""
        texto = f"{valor:,.{casas}f}"
        return texto.replace(",", "X").replace(".", ",").replace("X", ".")
'''

DEMO_MPL = code(FUNCOES + r'''

    # ---------------------------------------------------------------- uso
    import numpy as np

    estilo_explicativo()
    meses = np.arange(1, 13)
    equipes = {  # tempo médio de resposta, em horas (sintético)
        "Suporte N1": [9.8, 9.5, 9.9, 9.6, 9.4, 9.7, 9.5, 9.3, 9.6, 9.4, 9.5, 9.3],
        "Financeiro": [14.2, 14.5, 13.9, 14.1, 14.4, 14.0, 13.8, 14.2, 14.1, 13.9, 14.0, 13.7],
        "Comercial": [4.1, 4.3, 4.0, 4.4, 4.2, 4.5, 4.3, 4.1, 4.4, 4.2, 4.0, 3.9],
        "Suporte N2": [21.5, 21.0, 20.8, 19.4, 16.2, 12.9, 10.4, 8.8, 7.9, 7.1, 6.8, 6.5],
    }

    fig, ax = plt.subplots(figsize=(8, 4.4))
    for nome, valores in equipes.items():
        destaque = nome == "Suporte N2"
        ax.plot(meses, valores, color=AZUL if destaque else CINZA_CLARO, linewidth=3 if destaque else 2)
        rotular_fim(ax, meses, valores, f"{nome}: {numero_br(valores[-1], 1)} h",
                    cor=AZUL if destaque else "#7F7F7F", negrito=destaque)
    ax.annotate("novo fluxo de triagem\nem abril", xy=(4, 19.4), xytext=(5.5, 19), va="center",
                color="#595959", fontsize=9.5, arrowprops=dict(arrowstyle="-", color="#7F7F7F"))
    ax.set_xticks([1, 4, 7, 10, 12], ["jan", "abr", "jul", "out", "dez"])
    ax.set_xlim(0.7, 15.2)
    ax.set_ylabel("horas")
    titulo(ax, "O Suporte N2 reduziu o tempo de resposta de 21 para 6,5 horas",
           "Tempo médio até a primeira resposta, por equipe, 2025")
    plt.show()
''')

DEMO_SNS = code(r'''
    import matplotlib.pyplot as plt
    import seaborn as sns

    CINZA, AZUL = "#A6A6A6", "#1F5FA8"

    # o mesmo estilo, aplicado pelo seaborn
    sns.set_theme(style="white", font_scale=0.95, rc={
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#BFBFBF", "axes.titlelocation": "left",
        "axes.titlesize": 13, "axes.titlecolor": "#262626",
        "axes.labelcolor": "#595959", "xtick.color": "#595959", "ytick.color": "#595959",
        "legend.frameon": False,
    })

    gorjetas = sns.load_dataset("tips")
    media = gorjetas.groupby("size")["tip"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(7, 3.8))
    sns.barplot(data=media, x="size", y="tip", color=CINZA, width=0.65, ax=ax)
    ax.patches[-1].set_facecolor(AZUL)  # destaque: mesas de 6 pessoas
    ax.bar_label(ax.containers[0], labels=[f"{v:.2f}".replace(".", ",") for v in media["tip"]],
                 padding=4, color="#595959")
    ax.set_title("Mesas de 6 pessoas deixam a maior gorjeta média: US$ 5,22")
    ax.set(xlabel="pessoas na mesa", ylabel="", yticks=[])
    sns.despine(left=True)
    plt.show()
''')

PERGUNTAS = [
    ("Qual é o valor deste indicador?", "Texto simples (número em destaque)", "g-texto"),
    ("Como estas categorias se comparam?", "Barras horizontais (nomes longos, ranking) ou verticais (poucas categorias)", "g-barras-h"),
    ("Qual categoria é a maior ou a menor?", "Barras ordenadas com uma cor de destaque", "g-barras-v"),
    ("Como esta medida evoluiu ao longo do tempo?", "Linha", "g-linha"),
    ("O que mudou entre dois momentos?", "Gráfico de inclinação", "g-inclinacao"),
    ("Como o todo se divide em partes?", "Barras empilhadas 100% (pizza só com duas ou três fatias)", "g-empilhadas"),
    ("Como saio do valor inicial e chego ao final?", "Cascata", "g-cascata"),
    ("Como os valores se distribuem?", "Histograma", "g-histograma"),
    ("As distribuições diferem entre grupos?", "Boxplot ou violino", "g-boxplot"),
    ("Duas medidas numéricas variam juntas?", "Dispersão, com destaque para o grupo de interesse", "g-dispersao"),
    ("Quanto Y muda quando X aumenta?", "Regressão", "g-regressao"),
    ("Qual é a relação e onde estão concentrados os casos?", "Distribuição conjunta", "g-conjunta"),
    ("Por onde começar a explorar várias variáveis?", "Pairplot (só na exploração)", "g-pairplot"),
    ("Onde estão os picos em uma tabela de duas dimensões?", "Mapa de calor", "g-heatmap"),
    ("Duas medidas com escalas diferentes?", "Dois gráficos empilhados com o mesmo eixo x, nunca eixo secundário", "e-secundario"),
]


def html(versoes):
    nav(1, "referencia", "Referência rápida")
    nav(2, "r-pergunta", "Pergunta → gráfico")
    nav(2, "r-estilo", "Estilo reutilizável")
    nav(2, "r-checklist", "Checklist final")
    nav(2, "creditos", "Fontes e créditos")
    linhas = "".join(f'<tr><td>{p}</td><td><a href="#{a}">{g}</a></td></tr>' for p, g, a in PERGUNTAS)
    return f'''
<section id="referencia" class="secao">
  <p class="sobretitulo">Parte 7</p>
  <h2>Referência rápida</h2>

  <article class="bloco" id="r-pergunta">
    <h3>Pergunta que quero responder → gráfico recomendado</h3>
    <p>{r("Tabela de consulta deste guia, construída a partir do repertório de visuais que Knaflic apresenta, somado aos gráficos estatísticos do seaborn. Clique no gráfico para ir ao exemplo.")}</p>
    <div class="tabela-wrap"><table class="perguntas">
      <thead><tr><th>Pergunta</th><th>Gráfico recomendado</th></tr></thead>
      <tbody>{linhas}</tbody>
    </table></div>
  </article>

  <article class="bloco" id="r-estilo">
    <h3>Trecho reutilizável de estilo</h3>
    <p>{r("As funções abaixo aplicam, em poucas chamadas, os princípios de design do livro: sem bordas e grade, títulos alinhados à esquerda e com espaço para subtítulo, cinza como cor padrão (o destaque precisa ser pedido), rótulos diretos e números no formato brasileiro. Copie o bloco das funções para um arquivo <code>estilo.py</code> e use <code>from estilo import *</code> nos seus notebooks.")}</p>
    <p>O exemplo em matplotlib traz as funções completas e o uso; o exemplo em seaborn mostra o mesmo estilo aplicado com <code>sns.set_theme</code>.</p>
    {switcher("estilo", [dict(label="Funções + uso (matplotlib)", lib="mpl", code=DEMO_MPL), dict(label="Mesmo estilo no seaborn", lib="sns", code=DEMO_SNS)], alt="Exemplo do estilo reutilizável")}
  </article>

  <article class="bloco" id="r-checklist">
    <h3>Checklist antes de apresentar</h3>
    <ul class="checklist">
      <li>Consigo dizer a grande ideia em uma frase? Ela está no título?</li>
      <li>O tipo de gráfico responde à pergunta da <a href="#r-pergunta">tabela acima</a>?</li>
      <li>Barras começam no zero? Há só um eixo y?</li>
      <li>Retirei bordas, grade, marcadores e legenda que não fazem falta?</li>
      <li>Existe uma única cor de destaque, e ela está no ponto da mensagem?</li>
      <li>Ao olhar o gráfico pela primeira vez, para onde vão os olhos? É para lá que eu queria?</li>
      <li>Os textos estão na horizontal, alinhados à esquerda e com números no formato brasileiro?</li>
      <li>Alguém que não conhece o tema entende o gráfico sem minha explicação?</li>
      <li>A chamada à ação está explícita (no rodapé, no slide ou na fala)?</li>
    </ul>
  </article>

  <article class="bloco" id="creditos">
    <h3>Fontes e créditos</h3>
    <p><strong>Livro.</strong> As ideias marcadas com o selo <span class="selo knaflic">Knaflic</span> vêm de Cole Nussbaumer Knaflic, <em>Storytelling with Data: A Data Visualization Guide for Business Professionals</em> (Wiley, 2015), publicado no Brasil como <em>Storytelling com Dados</em>. Todas foram parafraseadas; nenhum trecho foi reproduzido. Os exemplos, dados e cenários deste guia são próprios e sintéticos, exceto os conjuntos embutidos no seaborn. Itens marcados com <span class="selo confirmar">a confirmar no livro</span> são detalhes que não pude verificar com segurança.</p>
    <p><strong>Seu material.</strong> Serviram de base: o notebook <em>matplotlib/matplotlib.ipynb</em> (interfaces pyplot e orientada a objetos, <code>subplots</code>, <code>add_axes</code>, <code>figsize</code>, legendas, cores, estilos de linha e os primeiros <code>scatter</code>, <code>hist</code> e <code>boxplot</code>); os notebooks de <em>seaborn/notebooks</em> (distribuições, categóricos, regressões, matrizes, estilos e grades, além do caderno de exercícios); a apostila <em>Visualização de Dados Avançada com Seaborn</em> (Asimov Academy) e o PDF <em>Visualizndo Dados com Matplotlib</em>, que reúne a impressão dos mesmos notebooks de seaborn. Cada cartão indica de onde veio o exemplo original. O caderno de exercícios traz o cabeçalho da Pierian Data, e a apostila é da Asimov Academy: a autoria desses materiais permanece com quem os produziu.</p>
    <p><strong>Ambiente.</strong> Imagens geradas com {versoes}, executando exatamente o código exibido ao lado de cada uma.</p>
  </article>
</section>'''
