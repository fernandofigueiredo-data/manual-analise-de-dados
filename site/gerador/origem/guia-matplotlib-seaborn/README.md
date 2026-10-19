# Guia matplotlib e seaborn com storytelling de dados

Guia interativo em um único arquivo HTML que funciona como manual de matplotlib e seaborn e, ao mesmo tempo, como manual prático das ideias de Cole Nussbaumer Knaflic em *Storytelling com Dados*.

Abra `guia_matplotlib_seaborn.html` em qualquer navegador. Não há dependências externas: CSS, JavaScript e imagens estão embutidos no arquivo.

## Conteúdo do guia

1. **Fundamentos**: anatomia de uma figura, interfaces pyplot e orientada a objetos, estilos e rcParams, o papel do seaborn e quando usar cada biblioteca.
2. **Os seis eixos de Knaflic**, ligados às linhas de código que os aplicam.
3. **Catálogo** com 16 gráficos, cada um com objetivo, critérios de escolha, código completo e a imagem gerada.
4. **Antes e depois**: bordas e grades, cor como destaque, rótulos diretos, título com a conclusão e anotações.
5. **Roteiro de montagem**: contexto, grande ideia, storyboard, estrutura narrativa e o gráfico em cinco etapas.
6. **Erros comuns**: eixo truncado, 3D, eixo secundário e excesso de cores.
7. **Referência rápida**: tabela pergunta → gráfico, funções de estilo reutilizáveis e checklist.

## Estrutura do repositório

| Arquivo | Função |
|---|---|
| `guia_matplotlib_seaborn.html` | Guia pronto (resultado do build) |
| `build.py` | Monta o HTML: executa cada exemplo, captura a figura e grava o arquivo final |
| `kit.py` | Motor: preâmbulos de estilo, execução dos códigos, compressão das imagens, mapa de eixos por linha |
| `fundamentos.py` | Parte 1: fundamentos |
| `catalogo.py` | Parte 3: catálogo de gráficos |
| `story.py` | Partes 2, 4, 5 e 6: eixos, antes e depois, roteiro e erros comuns |
| `referencia.py` | Parte 7: referência rápida e créditos |
| `estilo.css` | Estilos da página |
| `app.js` | Interatividade: realce de sintaxe, busca, filtros, abas, antes e depois, copiar código |

## Como gerar o HTML de novo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py
```

Na primeira execução, `sns.load_dataset` baixa os conjuntos `tips`, `flights` e `iris` da internet. O build leva poucos segundos e informa no terminal o número de imagens, o tamanho do arquivo e os avisos emitidos pelas bibliotecas.

Cada imagem do guia é produzida executando exatamente o código exibido ao lado dela. Para alterar um exemplo, edite o código no módulo correspondente e rode o build.

## Versões usadas

Python 3.14, matplotlib 3.11.1, seaborn 0.13.2, pandas 3.0.5, NumPy 2.5.2 e Pillow 12.3.0.

## Créditos

- Ideias de storytelling: Cole Nussbaumer Knaflic, *Storytelling with Data* (Wiley, 2015), publicado no Brasil como *Storytelling com Dados*. Todas parafraseadas; itens incertos estão marcados no guia como "a confirmar no livro".
- Exemplos-base adaptados de notebooks e apostilas de estudo do autor do projeto, incluindo material da Pierian Data e da Asimov Academy, cuja autoria permanece com quem os produziu.
- Dados: sintéticos ou conjuntos embutidos no seaborn.
