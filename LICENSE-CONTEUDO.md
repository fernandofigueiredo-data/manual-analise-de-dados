# Licenças deste repositório

Este repositório tem duas licenças, uma para o código e outra para o conteúdo.

## Código: MIT

Arquivo [`LICENSE`](LICENSE). Vale para:

- o código do site (`site/src/`, `site/scripts/`, `site/astro.config.mjs`);
- o gerador (`site/gerador/*.py` e os scripts em `site/gerador/origem/`);
- **todo bloco de código** dos materiais, inclusive as células de código dos notebooks (`.ipynb`) e os exemplos mostrados no site.

Copiar um trecho de código para o seu projeto não exige citação além do aviso da licença MIT.

## Conteúdo: Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)

Vale para o texto, as explicações, as tabelas de decisão, os gráficos e imagens, os guias em HTML, o modelo de relatório (`.docx`), a skill de decisão (`.md`), as células de texto dos notebooks e a documentação em `docs/`.

Você pode copiar, redistribuir, adaptar e usar inclusive comercialmente, desde que **atribua a autoria**, indique o link da licença e diga se fez alterações. Sugestão de atribuição:

> *Manual de Análise de Dados*, de Fernando Figueiredo, licenciado sob CC BY 4.0. https://github.com/fernandofigueiredo-data/manual-analise-de-dados

Resumo da licença: https://creativecommons.org/licenses/by/4.0/deed.pt-br
Texto legal completo: https://creativecommons.org/licenses/by/4.0/legalcode.pt

## Exceções (material de terceiros)

- **Fontes Inter e JetBrains Mono** (`site/public/fonts/`, `site/gerador/fontes/`): SIL Open Font License 1.1, dos respectivos autores. As licenças acompanham as fontes (`OFL-*.txt`).
- **Notebooks modelo de Machine Learning** (`site/gerador/origem/modelos-ml/`): reescritos a partir de exercícios da *Machine Learning Specialization* (DeepLearning.AI e Stanford Online), com a origem indicada no cabeçalho de cada um. O curso e os exercícios originais pertencem aos seus autores; os originais não estão neste repositório.
- **Conjuntos de dados de exemplo** (`tips`, `flights`, `iris`, baixados pelo seaborn durante a geração): seguem as licenças das suas fontes e não estão neste repositório.
- **Dados da ANAC no estudo de caso** (`site/gerador/estudo-de-caso/`): Voo Regular Ativo (VRA), Dados Estatísticos do Transporte Aéreo e reclamações do consumidor.gov.br, publicados pela Agência Nacional de Aviação Civil em https://sistemas.anac.gov.br/dadosabertos/. A página de dados abertos não declara uma licença própria (o rodapé do portal gov.br cita a CC BY-ND 3.0); como dados abertos do Poder Executivo federal, o uso é livre, com crédito à fonte (Decreto 8.777/2016, art. 2º, III). Os arquivos brutos **não** estão neste repositório: são baixados por `baixar_dados.py`. Só os agregados derivados (`agregados/`), os gráficos e as tabelas do estudo estão aqui, sempre com o crédito "Fonte: ANAC (dados abertos)". A análise e o texto do estudo seguem a CC BY 4.0; os dados continuam sendo da ANAC.
