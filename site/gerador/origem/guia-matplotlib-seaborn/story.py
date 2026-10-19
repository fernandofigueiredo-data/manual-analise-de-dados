"""Seções de storytelling: eixos, antes e depois, roteiro e erros comuns."""
import kit
from kit import code, switcher, nav, k, r, chips_eixos, CONFIRMAR, EIXOS

REG = []   # (âncora, rótulo, conjunto de eixos)


def registra(ancora, rotulo, codigos):
    eixos = set()
    for c in codigos:
        eixos |= set(kit.mapa_eixos(c))
    REG.append((ancora, rotulo, eixos))


def ba(id_, titulo, tecnica, texto, antes, depois, eixos, rotulos=("Antes", "Depois"), nota=""):
    registra(id_, titulo, [depois])
    return f'''
  <article class="bloco ba-bloco" id="{id_}">
    <h3>{titulo}</h3>
    <p class="tecnica">{tecnica}</p>
    <div class="nota-eixo">{chips_eixos(eixos)}</div>
    {texto}
    {switcher(id_, [dict(label=rotulos[0], lib="mpl", code=antes), dict(label=rotulos[1], lib="mpl", code=depois)], kind="ba", alt=titulo)}
    {nota}
  </article>'''


# ======================================================================= ANTES E DEPOIS
A1_ANTES = code(r'''
    import matplotlib.pyplot as plt

    trimestres = ["1º tri", "2º tri", "3º tri", "4º tri"]
    chamados = [1240, 1180, 1510, 1630]

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.bar(trimestres, chamados)
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.set_title("Chamados abertos por trimestre")
    ax.set_ylabel("Chamados")
    plt.show()
''')

A1_DEPOIS = code(r'''
    import matplotlib.pyplot as plt

    trimestres = ["1º tri", "2º tri", "3º tri", "4º tri"]
    chamados = [1240, 1180, 1510, 1630]

    fig, ax = plt.subplots(figsize=(6.5, 4))
    barras = ax.bar(trimestres, chamados, width=0.6)
    ax.set_title("Chamados abertos por trimestre", loc="left")

    # 1. sem grade e sem as bordas de cima, da direita e da esquerda
    ax.grid(False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#BFBFBF")
    # 2. o eixo y dá lugar a rótulos nas próprias barras
    ax.set_yticks([])
    ax.bar_label(barras, labels=[f"{c:,}".replace(",", ".") for c in chamados],
                 padding=4, color="#595959")
    # 3. marcas de eixo removidas e textos em cinza
    ax.tick_params(bottom=False, colors="#595959")
    plt.show()
''')

A2_ANTES = code(r'''
    <<MPL>>

    regioes = ["Sudeste", "Sul", "Centro-Oeste", "Nordeste", "Norte"]
    prazo = [2.1, 2.4, 3.2, 3.6, 5.8]  # dias médios de entrega (sintético)

    fig, ax = plt.subplots(figsize=(7, 3.8))
    barras = ax.barh(regioes, prazo, color=plt.cm.tab10.colors[:5], height=0.6)
    ax.invert_yaxis()
    ax.bar_label(barras, labels=[f"{p:.1f} dias".replace(".", ",") for p in prazo], padding=4)
    ax.set_title("Prazo médio de entrega por região")
    ax.spines[["left", "bottom"]].set_visible(False)
    ax.tick_params(left=False)
    ax.set_xticks([])
    plt.show()
''')

A2_DEPOIS = code(r'''
    <<MPL>>

    regioes = ["Sudeste", "Sul", "Centro-Oeste", "Nordeste", "Norte"]
    prazo = [2.1, 2.4, 3.2, 3.6, 5.8]  # dias médios de entrega (sintético)
    cores = [AZUL if r == "Norte" else CINZA for r in regioes]

    fig, ax = plt.subplots(figsize=(7, 3.8))
    barras = ax.barh(regioes, prazo, color=cores, height=0.6)
    ax.invert_yaxis()
    ax.bar_label(barras, labels=[f"{p:.1f} dias".replace(".", ",") for p in prazo],
                 padding=4, color="#595959")
    ax.get_yticklabels()[-1].set_color(AZUL)        # o nome também ganha o destaque
    ax.get_yticklabels()[-1].set_fontweight("bold")
    ax.set_title("Prazo médio de entrega por região")
    ax.spines[["left", "bottom"]].set_visible(False)
    ax.tick_params(left=False)
    ax.set_xticks([])
    plt.show()
''')

A3_ANTES = code(r'''
    <<MPL>>

    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    planos = {  # assinantes em milhares (sintético)
        "Básico": [120, 118, 121, 125, 123, 126, 130, 128, 131, 133, 132, 135],
        "Padrão": [210, 215, 222, 230, 236, 241, 249, 255, 262, 270, 276, 284],
        "Premium": [80, 84, 90, 97, 105, 114, 124, 135, 147, 160, 174, 189],
        "Empresarial": [40, 41, 41, 43, 44, 44, 46, 47, 47, 49, 50, 51],
    }

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for nome, valores in planos.items():
        ax.plot(meses, valores, linewidth=2, label=nome)
    ax.legend(title="Plano", loc="upper left")
    ax.set_title("Assinantes por plano em 2025 (milhares)")
    plt.show()
''')

A3_DEPOIS = code(r'''
    <<MPL>>

    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    planos = {  # assinantes em milhares (sintético)
        "Básico": [120, 118, 121, 125, 123, 126, 130, 128, 131, 133, 132, 135],
        "Padrão": [210, 215, 222, 230, 236, 241, 249, 255, 262, 270, 276, 284],
        "Premium": [80, 84, 90, 97, 105, 114, 124, 135, 147, 160, 174, 189],
        "Empresarial": [40, 41, 41, 43, 44, 44, 46, 47, 47, 49, 50, 51],
    }

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for nome, valores in planos.items():
        linha, = ax.plot(meses, valores, linewidth=2)
        # rótulo direto no fim da linha, na mesma cor da série
        ax.annotate(f"{nome} ({valores[-1]})", (11, valores[-1]), xytext=(6, 0),
                    textcoords="offset points", va="center", color=linha.get_color(),
                    fontweight="bold")
    ax.set_xlim(-0.3, 13.5)
    ax.set_title("Assinantes por plano em 2025 (milhares)")
    plt.show()
''')

A4_ANTES = code(r'''
    <<MPL>>

    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    conversao = np.array([1.6, 1.5, 1.7, 1.6, 1.7, 2.9, 3.2, 3.3, 3.1, 3.4, 3.3, 3.5])

    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(meses, conversao, color=AZUL, linewidth=2.5)
    ax.set_ylim(0, 4)
    ax.set_ylabel("%")
    ax.set_title("Taxa de conversão mensal")
    plt.show()
''')

A4_DEPOIS = code(r'''
    <<MPL>>

    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    conversao = np.array([1.6, 1.5, 1.7, 1.6, 1.7, 2.9, 3.2, 3.3, 3.1, 3.4, 3.3, 3.5])

    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(meses, conversao, color=AZUL, linewidth=2.5)
    ax.set_ylim(0, 4)
    ax.set_ylabel("%")
    # o título enuncia a conclusão; o subtítulo diz o que está sendo medido
    ax.set_title("A conversão dobrou após o novo checkout, lançado em junho", pad=26)
    ax.text(0, 1.03, "Taxa de conversão do site, % das visitas, 2025",
            transform=ax.transAxes, color="#7F7F7F", fontsize=10)
    plt.show()
''')

A5_ANTES = code(r'''
    <<MPL>>
    import matplotlib.dates as mdates
    import pandas as pd

    rng = np.random.default_rng(7)
    dias = pd.date_range("2025-04-01", periods=61)
    visitas = 1200 + rng.normal(0, 60, 61)
    visitas[37:43] += [300, 900, 1600, 1100, 500, 200]  # efeito da campanha (sintético)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dias, visitas, color=AZUL, linewidth=2)
    ax.set_ylim(0, 3300)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.set_title("Visitas diárias ao site, abril e maio de 2025")
    plt.show()
''')

A5_DEPOIS = code(r'''
    <<MPL>>
    import matplotlib.dates as mdates
    import pandas as pd

    rng = np.random.default_rng(7)
    dias = pd.date_range("2025-04-01", periods=61)
    visitas = 1200 + rng.normal(0, 60, 61)
    visitas[37:43] += [300, 900, 1600, 1100, 500, 200]  # efeito da campanha (sintético)
    pico = visitas.argmax()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axvspan(dias[37], dias[42], color="#EDEDED", zorder=0)  # período da campanha
    ax.plot(dias, visitas, color=AZUL, linewidth=2)
    ax.set_ylim(0, 3300)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.annotate(f"Campanha de Dia das Mães:\npico de {visitas[pico] / 1000:.1f} mil visitas".replace(".", ","),
                xy=(dias[pico], visitas[pico]), xytext=(dias[pico] + pd.Timedelta(days=5), 2950),
                va="top", color="#404040",
                arrowprops=dict(arrowstyle="-", color="#7F7F7F", lw=1))
    ax.text(dias[2], 1420, "patamar sem campanha: cerca de 1,2 mil por dia", color="#7F7F7F", fontsize=9.5)
    ax.set_title("Visitas diárias ao site, abril e maio de 2025")
    plt.show()
''')


def antes_depois_html():
    nav(1, "antes-depois", "Antes e depois")
    nav(2, "a-bordas", "Bordas e grades")
    nav(2, "a-cor", "Cor como destaque")
    nav(2, "a-rotulos", "Rótulos diretos")
    nav(2, "a-titulo", "Título com a conclusão")
    nav(2, "a-anotacoes", "Anotações")
    blocos = [
        ba("a-bordas", "Remoção de bordas e grades",
           "Técnica: tirar o que não carrega dado.",
           f'<p>{k("Knaflic trata cada elemento sem função como desordem, algo que aumenta a carga cognitiva sem acrescentar informação. Bordas do gráfico, linhas de grade e marcas de eixo estão entre os primeiros candidatos a sair. Quando os valores aparecem direto nas barras, o eixo y também se torna dispensável.")}</p>',
           A1_ANTES, A1_DEPOIS, ["desordem"]),
        ba("a-cor", "Cor como destaque",
           "Técnica: cinza para o contexto, uma cor para a mensagem.",
           f'<p>{k("A cor é um dos atributos pré-atentivos mais fortes: o olho a detecta antes de qualquer leitura consciente. Por isso a autora recomenda usá-la com parcimônia. Se tudo é colorido, nada se destaca. Com o restante em cinza, uma única cor diz onde olhar.")}</p><p>{r("Faça a lista de cores com uma compreensão de lista (<code>[AZUL if ... else CINZA for ...]</code>). Assim, trocar o destaque vira trocar uma condição. Pinte também o rótulo da categoria, para ligar nome e barra.")}</p>',
           A2_ANTES, A2_DEPOIS, ["atencao"]),
        ba("a-rotulos", "Rótulos diretos no lugar da legenda",
           "Técnica: escrever o nome da série junto à própria série.",
           f'<p>{k("A legenda obriga o olho a ir e voltar entre a chave de cores e os dados. Knaflic recomenda rotular as séries diretamente, aproveitando o princípio da proximidade: o que está perto parece pertencer ao mesmo grupo.")}</p><p>{r("<code>ax.annotate</code> com <code>textcoords=\'offset points\'</code> desloca o texto alguns pontos à direita do último valor. A cor vem de <code>linha.get_color()</code>, sem repetir a paleta. Abra espaço à direita com <code>set_xlim</code>.")}</p>',
           A3_ANTES, A3_DEPOIS, ["desordem", "designer"]),
        ba("a-titulo", "Título que enuncia a conclusão",
           "Técnica: trocar a descrição do gráfico pela frase que você quer que o público lembre.",
           f'<p>{k("O texto é parte do design, não um acessório. Nos exemplos do livro, o título carrega a mensagem (o “e daí?”), e o restante do gráfico serve de prova. Um título descritivo, como “Taxa de conversão mensal”, deixa a interpretação por conta do público.")}</p><p>{r("Alinhe título e subtítulo à esquerda (<code>loc=\'left\'</code> ou <code>axes.titlelocation</code>). Use <code>pad</code> para abrir espaço e posicione o subtítulo com <code>ax.text(..., transform=ax.transAxes)</code>.")}</p>',
           A4_ANTES, A4_DEPOIS, ["historia", "designer"]),
        ba("a-anotacoes", "Anotações",
           "Técnica: explicar no próprio gráfico o que causou o padrão.",
           f'<p>{k("Anotações respondem à pergunta que o público faria ao ver o pico ou a queda. Knaflic usa texto no gráfico para explicar eventos e dar contexto, sempre com moderação, para não recriar a desordem que foi removida.")}</p><p>{r("<code>ax.axvspan</code> sombreia um período sem competir com a linha; <code>ax.annotate</code> com uma seta discreta liga o texto ao ponto. Datas ficam legíveis com <code>mdates.DateFormatter(\'%d/%m\')</code>.")}</p>',
           A5_ANTES, A5_DEPOIS, ["historia", "atencao"]),
    ]
    return f'''
<section id="antes-depois" class="secao">
  <p class="sobretitulo">Parte 4</p>
  <h2>Antes e depois</h2>
  <p class="lead">Cada par abaixo isola <em>uma</em> técnica: o “antes” e o “depois” diferem apenas nela, para que fique claro o efeito de cada linha de código. Use o seletor para alternar. O <a href="#roteiro">roteiro de montagem</a> junta todas as técnicas em um único gráfico.</p>
  {"".join(blocos)}
</section>'''


# ======================================================================= ROTEIRO
DADOS_ROTEIRO = '''meses = [f"{m}/{a}" for a in ("24", "25") for m in
         ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]][:18]
taxa = np.array([2.0, 2.1, 1.9, 2.2, 2.0, 2.1, 2.2, 2.0, 2.1, 2.3, 2.1, 2.2,
                 2.1, 2.2, 3.6, 4.0, 4.2, 4.3])  # % de assinantes que cancelaram no mês (sintético)'''

E1 = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    DADOS

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.bar(meses, taxa, label="Taxa de cancelamento")
    ax.legend()
    ax.grid(True)
    ax.set_title("Taxa de cancelamento")
    plt.xticks(rotation=45)
    plt.show()
'''.replace("DADOS", DADOS_ROTEIRO.replace("\n", "\n    ")))

E2 = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    DADOS

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(meses, taxa, marker="o", label="Taxa de cancelamento")  # tendência pede linha
    ax.legend()
    ax.grid(True)
    ax.set_title("Taxa de cancelamento")
    plt.xticks(rotation=45)
    plt.show()
'''.replace("DADOS", DADOS_ROTEIRO.replace("\n", "\n    ")))

E3 = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    DADOS

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(range(18), taxa, color="#7F7F7F", linewidth=2)       # sem marcadores e sem legenda
    ax.spines[["top", "right"]].set_visible(False)              # sem bordas supérfluas
    ax.spines[["left", "bottom"]].set_color("#BFBFBF")
    ax.tick_params(colors="#595959", length=0)
    ax.set_xticks(range(0, 18, 3), meses[::3])                  # rótulos horizontais e espaçados
    ax.set_ylim(0, 5)
    ax.set_ylabel("% de assinantes por mês", color="#595959")
    ax.set_title("Taxa de cancelamento", loc="left", color="#404040")
    plt.show()
'''.replace("DADOS", DADOS_ROTEIRO.replace("\n", "\n    ")))

E4 = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    CINZA, LARANJA = "#A6A6A6", "#D9731A"
    DADOS

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(range(14), taxa[:14], color=CINZA, linewidth=2)           # contexto em cinza
    ax.plot(range(13, 18), taxa[13:], color=LARANJA, linewidth=3)     # o problema em laranja
    ax.scatter(17, taxa[-1], color=LARANJA, zorder=3)
    ax.annotate(f"{taxa[-1]:.1f}%".replace(".", ","), (17, taxa[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", color=LARANJA, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#BFBFBF")
    ax.tick_params(colors="#595959", length=0)
    ax.set_xticks(range(0, 18, 3), meses[::3])
    ax.set_xlim(-0.5, 18.2)
    ax.set_ylim(0, 5)
    ax.set_ylabel("% de assinantes por mês", color="#595959")
    ax.set_title("Taxa de cancelamento", loc="left", color="#404040")
    plt.show()
'''.replace("DADOS", DADOS_ROTEIRO.replace("\n", "\n    ")))

E5 = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    CINZA, AZUL, LARANJA = "#A6A6A6", "#1F5FA8", "#D9731A"
    DADOS
    media_antes = taxa[:14].mean()

    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.plot(range(14), taxa[:14], color=CINZA, linewidth=2)
    ax.plot(range(13, 18), taxa[13:], color=LARANJA, linewidth=3)
    ax.scatter(17, taxa[-1], color=LARANJA, zorder=3)
    ax.annotate(f"{taxa[-1]:.1f}%".replace(".", ","), (17, taxa[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", color=LARANJA, fontweight="bold")
    # contexto: a referência anterior e o evento que explica a mudança
    ax.hlines(media_antes, 0, 13, color=CINZA, linestyle="--", linewidth=1)
    ax.text(0, media_antes + 0.25, f"média antes do reajuste: {media_antes:.1f}%".replace(".", ","),
            color="#7F7F7F", fontsize=9.5)
    ax.axvline(14, color="#BFBFBF", linewidth=1, linestyle=":")
    ax.text(13.8, 4.9, "reajuste de 15%\nem mar/25", ha="right", va="top", color="#595959", fontsize=9.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#BFBFBF")
    ax.tick_params(colors="#595959", length=0)
    ax.set_xticks(range(0, 18, 3), meses[::3])
    ax.set_xlim(-0.5, 18.2)
    ax.set_ylim(0, 5)
    # a grande ideia vira título; o subtítulo explica a medida; o rodapé pede a ação
    ax.set_title("O reajuste de março dobrou a taxa de cancelamento", loc="left",
                 fontsize=14, color="#262626", pad=26)
    ax.text(0, 1.03, "% de assinantes que cancelaram no mês, jan/24 a jun/25",
            transform=ax.transAxes, color="#7F7F7F", fontsize=10)
    ax.text(0, -0.13, "Proposta: aprovar hoje o desconto de fidelidade para quem assina há\n"
            "mais de um ano e medir o efeito em 90 dias.", transform=ax.transAxes, color=AZUL,
            fontweight="bold", fontsize=10, va="top")
    plt.show()
'''.replace("DADOS", DADOS_ROTEIRO.replace("\n", "\n    ")))


def roteiro_html():
    nav(1, "roteiro", "Roteiro de montagem")
    nav(2, "r-contexto", "1. Contexto")
    nav(2, "r-grande-ideia", "2. Grande ideia")
    nav(2, "r-storyboard", "3. Storyboard")
    nav(2, "r-narrativa", "4. Estrutura narrativa")
    nav(2, "r-montagem", "5. Montagem do gráfico")
    registra("r-montagem", "Roteiro: montagem do gráfico", [E5])
    passos = [
        dict(label="1. Padrão", lib="mpl", code=E1, texto="<p><strong>Ponto de partida.</strong> O gráfico que sai “de fábrica”: barras para uma série temporal, legenda para uma única série, grade, rótulos inclinados e um título que só repete o nome da medida.</p>"),
        dict(label="2. Visual", lib="mpl", code=E2, texto=f"<p><strong>Escolher um visual eficaz.</strong> {k('A pergunta é sobre tendência ao longo do tempo, e o livro indica a linha para dados contínuos como o tempo.')} Só a troca de <code>ax.bar</code> por <code>ax.plot</code> já deixa visível o salto.</p>"),
        dict(label="3. Desordem", lib="mpl", code=E3, texto=f"<p><strong>Eliminar a desordem.</strong> Saem legenda, grade, marcadores, bordas de cima e da direita e a inclinação dos rótulos. Os eixos ficam em cinza para não competir com os dados. {r('Mostrar um rótulo a cada três meses mantém a referência temporal sem amontoar texto.')}</p>"),
        dict(label="4. Atenção", lib="mpl", code=E4, texto=f"<p><strong>Focar a atenção.</strong> O período antes do reajuste vira contexto, em cinza. O trecho do problema ganha o laranja, reservado neste guia para alertas, e o último valor é rotulado diretamente. {k('É a aplicação direta dos atributos pré-atentivos: cor e espessura dizem onde olhar.')}</p>"),
        dict(label="5. História", lib="mpl", code=E5, texto=f"<p><strong>Pensar como designer e contar a história.</strong> A grande ideia vira título; o subtítulo explica a medida; uma linha de referência e uma anotação dão o contexto; o rodapé traz a chamada à ação, em azul. {r('Todos os textos ficam alinhados à esquerda, na mesma margem do título.')}</p>"),
    ]
    return f'''
<section id="roteiro" class="secao">
  <p class="sobretitulo">Parte 5</p>
  <h2>Roteiro prático: do contexto ao gráfico explicativo</h2>
  <p class="lead">Um caso único, do começo ao fim. Uma empresa fictícia de cursos por assinatura reajustou o preço em março de 2025, e a área de dados precisa levar o assunto à diretoria. Os quatro primeiros passos acontecem longe do Python; o quinto mostra o código evoluindo.</p>

  <article class="bloco" id="r-contexto">
    <h3>1. Entender o contexto</h3>
    <p>{k("Knaflic começa pela distinção entre análise <strong>exploratória</strong>, em que se procuram as poucas descobertas relevantes no meio de muitas, e <strong>explicativa</strong>, em que se comunica uma delas a um público específico. Para o trabalho explicativo, ela propõe responder três perguntas antes de abrir qualquer ferramenta: <strong>quem</strong> é o público, <strong>o que</strong> você quer que ele saiba ou faça e <strong>como</strong> os dados vão sustentar esse pedido. Ela também diferencia a apresentação ao vivo, em que você conduz, do documento enviado, que precisa se explicar sozinho.")}</p>
    <div class="cartoes3">
      <div class="cartao"><p class="cartao-rot">Quem</p><p>Diretoria comercial: decide preços e campanhas, tem dez minutos na pauta e não acompanha os indicadores mês a mês.</p></div>
      <div class="cartao"><p class="cartao-rot">O quê</p><p>Aprovar, na própria reunião, um desconto de fidelidade para assinantes antigos, em teste por 90 dias.</p></div>
      <div class="cartao"><p class="cartao-rot">Como</p><p>Apresentação ao vivo: um gráfico com a evolução do cancelamento e um slide com a proposta e o custo estimado.</p></div>
    </div>
    <p>{r("Escreva essas três respostas como comentário no topo da célula ou do script que gera o gráfico final. Elas viram critério de revisão: cada linha de código precisa servir ao “o quê”.")}</p>
  </article>

  <article class="bloco" id="r-grande-ideia">
    <h3>2. A grande ideia</h3>
    <p>{k("A grande ideia (<em>Big Idea</em>) é a mensagem inteira condensada em uma frase completa, que expressa o seu ponto de vista e deixa claro o que está em jogo. Knaflic credita o conceito a Nancy Duarte.")} {CONFIRMAR}</p>
    <blockquote class="grande-ideia">O reajuste de março dobrou a taxa de cancelamento; se não aprovarmos hoje um desconto de fidelidade, vamos perder cerca de 1.800 assinantes até dezembro.</blockquote>
    <p>{k("Junto com a grande ideia, a autora sugere preparar a <strong>história de três minutos</strong>: a versão que você conseguiria contar se todo o tempo da reunião desaparecesse e restassem só três minutos. Se você consegue contá-la, entendeu o próprio material.")}</p>
    <p class="checklist-titulo">Teste rápido da sua frase</p>
    <ul class="checklist">
      <li>É uma frase completa, com sujeito e verbo?</li>
      <li>Mostra um ponto de vista, e não apenas um tema (“análise do cancelamento”)?</li>
      <li>Diz o que se ganha ou se perde com a decisão?</li>
    </ul>
  </article>

  <article class="bloco" id="r-storyboard">
    <h3>3. Storyboard</h3>
    <p>{k("Knaflic recomenda montar o storyboard antes de produzir qualquer conteúdo, de preferência com papel e notas autoadesivas: é barato, fácil de reordenar e evita o apego ao que já foi feito no computador. Também é o momento de alinhar a estrutura com quem pediu o trabalho.")}</p>
    <ol class="storyboard">
      <li><span>Cenário</span>A base cresceu 12% em 2024, com cancelamento estável perto de 2% ao mês.</li>
      <li><span>Mudança</span>Em março de 2025 o preço subiu 15%.</li>
      <li><span>Conflito</span>O cancelamento saltou para 4,3% ao mês e não voltou.</li>
      <li><span>Consequência</span>No ritmo atual, são cerca de 1.800 assinantes a menos até dezembro.</li>
      <li><span>Opções</span>Reverter o preço, desconto para todos ou desconto de fidelidade.</li>
      <li><span>Ação</span>Aprovar hoje o desconto de fidelidade, em teste por 90 dias.</li>
    </ol>
  </article>

  <article class="bloco" id="r-narrativa">
    <h3>4. Estrutura narrativa</h3>
    <p>{k("A autora organiza a história em começo, meio e fim. No <strong>começo</strong>, o cenário e o que o público precisa saber para acompanhar. No <strong>meio</strong>, a tensão: o problema, as evidências e as alternativas. No <strong>fim</strong>, a chamada à ação. Ela discute também a ordem: seguir a cronologia ou abrir pela conclusão, o que costuma funcionar melhor com executivos que querem a resposta primeiro.")}</p>
    <div class="tabela-wrap"><table>
      <thead><tr><th>Parte</th><th>Neste caso</th><th>No gráfico</th></tr></thead>
      <tbody>
        <tr><td>Começo</td><td>Base saudável, cancelamento estável</td><td>trecho cinza e a média anterior</td></tr>
        <tr><td>Meio</td><td>Reajuste e salto do cancelamento</td><td>trecho em laranja e anotação do reajuste</td></tr>
        <tr><td>Fim</td><td>Pedido de decisão</td><td>rodapé com a proposta</td></tr>
      </tbody>
    </table></div>
    <p>{k("Para testar a narrativa, Knaflic sugere a <strong>lógica horizontal</strong> (lidos em sequência, só os títulos dos slides contam a história?) e a <strong>lógica vertical</strong> (o conteúdo de cada slide sustenta o seu título?), além do <strong>storyboard reverso</strong> (anotar a ideia central de cada slide pronto e conferir se o roteiro resultante faz sentido) e da <strong>perspectiva de fora</strong> (pedir a alguém que não conhece o tema para explicar o que entendeu).")}</p>
    <p>{k("Ela também valoriza a repetição para fixar a mensagem: dizer o que vai ser dito, dizer e, no fim, retomar o que foi dito.")} {CONFIRMAR}</p>
  </article>

  <article class="bloco" id="r-montagem">
    <h3>5. Montagem do gráfico, passo a passo</h3>
    <p>Cada etapa abaixo traz o código completo que gerou a imagem. Avance com os botões ou com as setas do teclado quando o seletor estiver em foco.</p>
    <div class="nota-eixo">{chips_eixos(["visual", "desordem", "atencao", "designer", "historia"])}</div>
    {switcher("roteiro", passos, kind="steps", alt="Montagem de um gráfico explicativo")}
  </article>
</section>'''


# ======================================================================= ERROS COMUNS
ER1_ERRO = code(r'''
    <<MPL>>

    lojas = ["Centro", "Norte", "Sul", "Leste"]
    satisfacao = [94, 96, 95, 97]  # % (sintético)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(lojas, satisfacao, color=CINZA, width=0.6)
    ax.set_ylim(93, 97.5)  # eixo truncado: diferenças de 1 ponto parecem enormes
    ax.set_title("Satisfação por loja (%)")
    plt.show()
''')

ER1_OK = code(r'''
    <<MPL>>

    lojas = ["Centro", "Norte", "Sul", "Leste"]
    satisfacao = [94, 96, 95, 97]  # % (sintético)

    fig, ax = plt.subplots(figsize=(6, 4))
    barras = ax.bar(lojas, satisfacao, color=CINZA, width=0.6)
    ax.set_ylim(0, 105)  # barras sempre partem do zero
    ax.bar_label(barras, fmt="%d%%", padding=4, color="#595959")
    ax.set_title("As quatro lojas têm satisfação parecida, entre 94% e 97%")
    ax.spines["left"].set_visible(False)
    ax.set_yticks([])
    plt.show()
''')

ER2_ERRO = code(r'''
    import matplotlib.pyplot as plt
    import numpy as np

    produtos = ["A", "B", "C", "D", "E"]
    vendas = [320, 290, 410, 180, 260]  # unidades (sintético)

    fig = plt.figure(figsize=(6.5, 4.8))
    ax = fig.add_subplot(projection="3d")
    ax.bar3d(np.arange(5), np.zeros(5), np.zeros(5), 0.6, 0.6, vendas, shade=True)
    ax.set_xticks(np.arange(5) + 0.3, produtos)
    ax.set_title("Vendas por produto")
    plt.show()
''')

ER2_OK = code(r'''
    <<MPL>>

    produtos = ["Produto A", "Produto B", "Produto C", "Produto D", "Produto E"]
    vendas = np.array([320, 290, 410, 180, 260])  # unidades (sintético)
    ordem = np.argsort(vendas)[::-1]
    nomes, valores = [produtos[i] for i in ordem], vendas[ordem]

    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    barras = ax.barh(nomes, valores, color=[AZUL] + [CINZA] * 4, height=0.6)
    ax.invert_yaxis()
    ax.bar_label(barras, padding=4, color="#595959")
    ax.set_title("O produto C lidera as vendas, com 410 unidades")
    ax.spines[["left", "bottom"]].set_visible(False)
    ax.tick_params(left=False)
    ax.set_xticks([])
    plt.show()
''')

ER3_ERRO = code(r'''
    <<MPL>>

    meses = ["jan", "fev", "mar", "abr", "mai", "jun"]
    receita = [4.2, 4.5, 4.9, 5.4, 5.8, 6.3]  # R$ milhões (sintético)
    margem = [18, 17, 15, 14, 12, 11]         # %

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(meses, receita, color=CINZA, width=0.6)
    ax.set_ylabel("Receita (R$ milhões)")
    ax2 = ax.twinx()                           # segundo eixo y: duas escalas no mesmo espaço
    ax2.plot(meses, margem, color=LARANJA, marker="o", linewidth=2)
    ax2.spines["right"].set_visible(True)
    ax2.set_ylabel("Margem (%)")
    ax.set_title("Receita e margem no 1º semestre")
    plt.show()
''')

ER3_OK = code(r'''
    <<MPL>>

    meses = ["jan", "fev", "mar", "abr", "mai", "jun"]
    receita = [4.2, 4.5, 4.9, 5.4, 5.8, 6.3]  # R$ milhões (sintético)
    margem = [18, 17, 15, 14, 12, 11]         # %

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
    barras = ax1.bar(meses, receita, color=CINZA, width=0.6)
    ax1.bar_label(barras, labels=[f"{v:.1f}".replace(".", ",") for v in receita],
                  padding=3, color="#595959")
    ax1.set_title("Receita (R$ milhões)", fontsize=10.5, color="#595959")

    ax2.plot(meses, margem, color=LARANJA, marker="o", linewidth=2.5)
    for x, y in zip(meses, margem):
        ax2.annotate(f"{y}%", (x, y), xytext=(0, 8), textcoords="offset points",
                     ha="center", color=LARANJA, fontsize=9.5)
    ax2.set_ylim(0, 23)
    ax2.set_title("Margem (%)", fontsize=10.5, color="#595959")

    for ax in (ax1, ax2):
        ax.spines["left"].set_visible(False)
        ax.set_yticks([])
    fig.suptitle("A receita cresceu 50% no semestre, mas a margem caiu 7 pontos",
                 x=0.02, ha="left", fontsize=13)
    fig.tight_layout()
    plt.show()
''')

ER4_ERRO = code(r'''
    <<MPL>>

    rng = np.random.default_rng(6)
    meses = np.arange(1, 13)
    vendas = {f"Loja {i}": 100 + rng.normal(0.5, 2.5, 12).cumsum() for i in range(1, 9)}
    vendas["Loja 5"] = vendas["Loja 5"] - np.linspace(0, 30, 12)  # índice, jan = ~100 (sintético)

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for nome, serie in vendas.items():
        ax.plot(meses, serie, linewidth=2, label=nome)  # oito cores do ciclo padrão
    ax.legend(ncol=2, fontsize=9)
    ax.set_title("Vendas mensais por loja (índice)")
    plt.show()
''')

ER4_OK = code(r'''
    <<MPL>>

    rng = np.random.default_rng(6)
    meses = np.arange(1, 13)
    vendas = {f"Loja {i}": 100 + rng.normal(0.5, 2.5, 12).cumsum() for i in range(1, 9)}
    vendas["Loja 5"] = vendas["Loja 5"] - np.linspace(0, 30, 12)  # índice, jan = ~100 (sintético)
    queda = vendas["Loja 5"][-1] / vendas["Loja 5"][0] - 1

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for nome, serie in vendas.items():
        if nome != "Loja 5":
            ax.plot(meses, serie, color="#C8C8C8", linewidth=1.2)
    ax.plot(meses, vendas["Loja 5"], color=LARANJA, linewidth=3)
    ax.annotate("Loja 5", (12, vendas["Loja 5"][-1]), xytext=(6, 0), textcoords="offset points",
                va="center", color=LARANJA, fontweight="bold")
    ax.text(12.15, 112, "outras 7 lojas", color="#7F7F7F", va="center", fontsize=9.5)
    ax.set_xlim(0.7, 13.8)
    ax.set_xticks([1, 4, 7, 10, 12], ["jan", "abr", "jul", "out", "dez"])
    ax.set_title(f"Só a Loja 5 terminou o ano abaixo do início: queda de {-queda:.0%}")
    plt.show()
''')


def erros_html():
    nav(1, "erros", "Erros comuns")
    nav(2, "e-truncado", "Eixo truncado em barras")
    nav(2, "e-3d", "Gráficos 3D")
    nav(2, "e-secundario", "Eixo secundário")
    nav(2, "e-cores", "Excesso de cores")
    rot = ("Erro", "Correção")
    blocos = [
        ba("e-truncado", "Eixo truncado em gráfico de barras",
           "Problema: o comprimento da barra deixa de ser proporcional ao valor.",
           f'<p>{k("Para Knaflic, gráficos de barras precisam começar no zero, porque o leitor compara comprimentos. Com o eixo começando em 93, uma diferença de 3 pontos parece uma barra quatro vezes maior que a outra.")}</p><p>{r("Se a diferença pequena for justamente a mensagem, não force as barras: mostre as diferenças em pontos percentuais ou use pontos (<code>ax.scatter</code>) com o eixo ajustado e avisado no título.")}</p>',
           ER1_ERRO, ER1_OK, ["visual", "designer"], rotulos=rot),
        ba("e-3d", "Gráficos 3D",
           "Problema: perspectiva e sombra distorcem os valores e acrescentam elementos sem dado.",
           f'<p>{k("A autora recomenda não usar 3D em gráficos de dados: a perspectiva faz barras iguais parecerem diferentes, dificulta ler valores contra o eixo e acrescenta paredes, sombras e ângulos que só ocupam espaço.")}</p><p>{r("O matplotlib só cria 3D quando você pede (<code>projection=\'3d\'</code>). Reserve esse recurso para dados de fato tridimensionais, como superfícies, e nunca para barras ou pizzas.")}</p>',
           ER2_ERRO, ER2_OK, ["visual", "desordem"], rotulos=rot),
        ba("e-secundario", "Eixo secundário",
           "Problema: duas escalas no mesmo espaço deixam o leitor sem saber qual série ler em qual eixo, e o cruzamento das linhas não significa nada.",
           f'<p>{k("Knaflic desaconselha o segundo eixo y. Entre as alternativas que ela propõe estão rotular diretamente os pontos da segunda série, dispensando o eixo, ou separar as séries em dois gráficos que compartilham o eixo x.")}</p><p>{r("<code>plt.subplots(2, 1, sharex=True)</code> faz exatamente isso: duas áreas de plotagem empilhadas, o mesmo eixo x e uma escala para cada medida.")}</p>',
           ER3_ERRO, ER3_OK, ["visual", "designer", "historia"], rotulos=rot),
        ba("e-cores", "Excesso de cores",
           "Problema: oito cores obrigam o leitor a decodificar a legenda e nenhuma série se destaca.",
           f'<p>{k("O livro insiste no uso parcimonioso e intencional da cor: ela deve marcar o que importa, e não decorar. Para gráficos com muitas linhas, a autora mostra como colocar o conjunto em segundo plano e destacar uma série por vez.")}</p><p>{r("Desenhe primeiro as séries de contexto em cinza claro e por último a série destacada, mais grossa. Se o público precisar ver várias lojas, faça pequenos múltiplos (<code>plt.subplots(2, 4, sharey=True)</code>) com um destaque diferente em cada um.")}</p>',
           ER4_ERRO, ER4_OK, ["atencao", "desordem"], rotulos=rot),
    ]
    return f'''
<section id="erros" class="secao">
  <p class="sobretitulo">Parte 6</p>
  <h2>Erros comuns e como corrigir em código</h2>
  <p class="lead">Quatro problemas frequentes, com o código do erro e o da correção. Alterne entre os dois para comparar.</p>
  {"".join(blocos)}
</section>'''


# ======================================================================= OS SEIS EIXOS
EIXO_TXT = {
    "contexto": (
        "Antes de qualquer gráfico, separar a exploração da explicação e responder quem é o público, o que ele deve saber ou fazer e como os dados sustentam isso. A grande ideia e a história de três minutos condensam a mensagem.",
        "Não há função de matplotlib para isso. O contexto aparece no código como a decisão sobre o que entra e o que sai: qual série recebe cor, qual frase vira título.",
        [("#r-contexto", "Roteiro: contexto"), ("#r-grande-ideia", "Roteiro: grande ideia"), ("#g-pairplot", "Pairplot: exploração versus explicação")],
    ),
    "visual": (
        "Um repertório pequeno resolve a maior parte dos casos: texto simples, tabela, mapa de calor, dispersão, linha, inclinação, barras verticais, horizontais e empilhadas, cascata e área. Pizza, rosca, 3D e eixo secundário devem ser evitados.",
        "A chamada principal (<code>ax.plot</code>, <code>ax.barh</code>, <code>sns.histplot</code>...) é a escolha do visual. Comece pela <a href='#r-pergunta'>tabela de perguntas</a>.",
        [],
    ),
    "desordem": (
        "Todo elemento sem função aumenta a carga cognitiva. Os princípios da Gestalt (proximidade, semelhança, delimitação, fechamento, continuidade e conexão) ajudam a decidir o que pode sair. Alinhamento e espaço em branco organizam o que fica.",
        "Bordas (<code>spines</code>), grade (<code>grid</code>), marcas (<code>tick_params</code>), legenda e eixo y substituído por <code>bar_label</code>.",
        [],
    ),
    "atencao": (
        "Atributos pré-atentivos, como cor, intensidade, tamanho, espessura, posição, forma e marcações adicionais, são percebidos antes da leitura consciente. Usados com parcimônia, dizem ao público onde olhar. A autora sugere testar o gráfico perguntando para onde os olhos vão primeiro.",
        "Cinza para o contexto e uma cor de destaque (<code>AZUL</code>, ou <code>LARANJA</code> para alertas), negrito no rótulo-chave e <code>zorder</code> para pôr o destaque por cima.",
        [],
    ),
    "designer": (
        "A forma segue a função. Knaflic usa a ideia de affordances: destacar o importante, eliminar distrações e criar hierarquia visual. Soma a isso acessibilidade (o texto é aliado: títulos, rótulos de eixos e anotações), estética e a aceitação do público.",
        "Rótulos horizontais, texto alinhado à esquerda (<code>axes.titlelocation</code>), números no formato brasileiro, proporções (<code>figsize</code>) e limites (<code>set_xlim</code>) que abrem espaço para rótulos diretos.",
        [],
    ),
    "historia": (
        "Uma história tem começo (cenário), meio (tensão) e fim (chamada à ação). O gráfico explicativo é uma cena dessa história: o título enuncia a conclusão e as anotações explicam o que aconteceu.",
        "<code>ax.set_title</code> com a conclusão, subtítulo com <code>ax.text</code>, <code>ax.annotate</code>, <code>axvspan</code> e <code>axhline</code> para dar referência.",
        [("#r-narrativa", "Roteiro: estrutura narrativa")],
    ),
}


def eixos_html(registro):
    nav(1, "eixos", "Os seis eixos de Knaflic")
    for i, (e, nome) in enumerate(EIXOS.items(), 1):
        nav(2, f"eixo-{e}", f"{i}. {nome}")
    cards = []
    for i, (e, nome) in enumerate(EIXOS.items(), 1):
        proposta, python, extras = EIXO_TXT[e]
        links = [f'<a href="{h}">{t}</a>' for h, t in extras]
        for ancora, rotulo, eixos in registro:
            if e in eixos:
                links.append(f'<a href="#{ancora}" class="mostra-linhas" data-axis="{e}">{rotulo}</a>')
        cards.append(f'''
    <article class="eixo-card" id="eixo-{e}">
      <p class="eixo-num">{i}</p>
      <div>
        <h3>{nome}</h3>
        <p>{k(proposta)}</p>
        <p>{r(python)}</p>
        <details class="onde"><summary>Onde aparece no código ({len(links)})</summary>
          <p class="onde-ajuda">Ao clicar, o guia abre o exemplo e realça as linhas que aplicam este eixo.</p>
          <div class="onde-lista">{"".join(links)}</div></details>
      </div>
    </article>''')
    return f'''
<section id="eixos" class="secao">
  <p class="sobretitulo">Parte 2</p>
  <h2>Os seis eixos de Knaflic, ligados ao código</h2>
  <p class="lead">Em <em>Storytelling com Dados</em>, Cole Nussbaumer Knaflic organiza o processo em seis lições. Este guia usa essas lições como eixos que atravessam todos os exemplos. Em cada cartão de gráfico, os botões de eixo realçam as linhas de código que aplicam aquela lição.</p>
  <div class="legenda-selos">
    <span><span class="selo knaflic">Knaflic</span> ideia da autora, parafraseada</span>
    <span><span class="selo tec">Recomendação técnica</span> sugestão deste guia sobre matplotlib e seaborn</span>
    <span>{CONFIRMAR} detalhe que deve ser conferido no livro</span>
  </div>
  <div class="eixos-grid">{"".join(cards)}</div>
</section>'''
