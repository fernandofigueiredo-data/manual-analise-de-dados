# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Analistas e estudantes de dados. Consultam o site para aprender análise de dados e data science e para copiar padrões de código, de análise e de relatório para os próprios projetos. O uso é de leitura e consulta: chegam por uma dúvida pontual (busca, link direto) ou seguem a trilha de aprendizado do início ao fim.

## Product Purpose

Manual e guia de referência em português do Brasil sobre análise de dados, organizado, didático e estruturado para consulta rápida, aprendizado e aplicação prática. É um produto público e permanente, não um protótipo, e também funciona como portfólio do autor no GitHub. Sucesso: a pessoa encontra rápido o que procura, entende, e consegue reutilizar o código ou o modelo sem retrabalho.

## Positioning

Reúne em uma única trilha quatro materiais do mesmo autor (notebook mestre de análise de dados, guia de matplotlib e seaborn com storytelling, guia do relatório profissional e manual de Machine Learning com skill de decisão e auditoria), com o notebook como espinha dorsal, código executado de verdade com as saídas e gráficos reais, e um diagnóstico de dataset que roda no navegador sem enviar o arquivo a servidor algum.

## Operating Context

- Leitura no desktop durante o trabalho (ao lado do editor ou do notebook) e no celular para estudo.
- Ações típicas: buscar um termo, navegar pela trilha, copiar um bloco de código, consultar uma tabela de decisão, baixar o modelo de relatório (.docx) ou a skill (.md), diagnosticar um dataset no navegador.
- Mantido a partir dos materiais de origem por um gerador (`site/gerador/`); o site é estático e pronto para a Vercel.

## Capabilities and Constraints

- Preservar integralmente o conteúdo dos materiais de origem, sem perda, omissão ou alteração de informação.
- Consolidar conteúdos, exemplos e códigos repetidos quando necessário, evitando redundância sem eliminar conhecimento relevante. (Diretriz confirmada em 02/10/2026; ainda não aplicada ao conteúdo. As duplicações conhecidas estão em `docs/OBSERVACOES.md`, itens D1 a D9.)
- Organizar o conteúdo de forma lógica e consistente, facilitando a navegação, a localização de informações e a reutilização de códigos e modelos.
- Português do Brasil em todo o site.
- Stack existente: Astro (estático), Pagefind (busca), gerador Python e Node; detalhes em `docs/DECISOES.md`.

## Brand Commitments

- Design system obrigatório: *Design System — Developer / Data Science / AI* (v1.0, Fernando Figueiredo), em `site/design-system/design-system-visual.md`, aplicado conforme `docs/DESIGN-SYSTEM.md`. Linguagem visual alinhada aos universos de desenvolvimento, data science e IA; escuro por padrão.
- Autoria: os quatro materiais são de Fernando Figueiredo.

## Evidence on Hand

- Materiais de origem em `site/gerador/origem/` (notebook, dois guias, pacote de ML).
- Saídas e 98 gráficos gerados pela execução real do código; 289 blocos de código.
- Auditoria técnica do manual de ML (`auditoria_ml.md`) com os resultados declarados pelo autor; os scripts não foram reexecutados na montagem do site.
- Não existem depoimentos, métricas de uso, clientes ou números de audiência: não inventar.

## Product Principles

1. Conteúdo primeiro: nada dos materiais se perde; a interface serve à leitura e à reutilização.
2. Achar rápido: busca, trilha, índice da página e links diretos levam ao ponto exato.
3. Copiar e usar: todo código e todo modelo pode ser copiado ou baixado sem atrito.
4. Honestidade técnica: código executado de verdade, limites e pendências declarados.
5. Consistência do sistema: um único design system, sem exceções silenciosas.

## Accessibility & Inclusion

WCAG 2.2 nível AA. Lighthouse com no mínimo 90 em desempenho, acessibilidade, boas práticas e SEO.
