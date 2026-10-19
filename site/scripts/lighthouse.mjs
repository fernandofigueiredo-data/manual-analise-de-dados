// Roda o Lighthouse (perfil móvel padrão e desktop) em páginas representativas e salva os
// relatórios HTML e JSON em ../docs/qualidade/lighthouse/ (fora do git), mais um resumo em ../docs/qualidade/lighthouse/RESUMO.md.
// Uso: com o preview rodando (npm run preview), node scripts/lighthouse.mjs [url-base]
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const BASE = process.argv[2] || 'http://localhost:4321';
const SAIDA = join(fileURLToPath(new URL('..', import.meta.url)), '..', 'docs', 'qualidade', 'lighthouse');
mkdirSync(SAIDA, { recursive: true });

const PAGINAS = [
  ['inicio', '/'],
  ['codigo-consultas-sql', '/preparar/consultas-sql/'],
  ['graficos-analise-univariada', '/explorar/analise-univariada/'],
  ['graficos-bivariada', '/explorar/analise-bivariada-e-multivariada/'],
  ['catalogo-de-graficos', '/visualizar/catalogo-de-graficos/'],
  ['relatorio-estruturar', '/comunicar/estruturar-o-relatorio/'],
  ['ml-manual', '/modelar/manual-de-machine-learning/'],
  ['ml-supervisionado-15-modelos', '/modelar/aprendizado-supervisionado/'],
  ['ml-diagnostico', '/modelar/diagnostico-do-dataset/'],
];
const CATEGORIAS = ['performance', 'accessibility', 'best-practices', 'seo'];

const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless=new', '--no-sandbox'] });
const linhas = [];
for (const perfil of ['mobile', 'desktop']) {
  for (const [nome, caminho] of PAGINAS) {
    const config = perfil === 'desktop'
      ? { extends: 'lighthouse:default', settings: { preset: 'desktop' } }
      : { extends: 'lighthouse:default' };
    const r = await lighthouse(BASE + caminho, { port: chrome.port, output: ['html', 'json'], onlyCategories: CATEGORIAS, logLevel: 'error' }, config);
    const [html, json] = r.report;
    writeFileSync(join(SAIDA, `${perfil}-${nome}.html`), html);
    writeFileSync(join(SAIDA, `${perfil}-${nome}.json`), json);
    const c = r.lhr.categories;
    const nota = (k) => Math.round(c[k].score * 100);
    linhas.push(`| ${perfil} | \`${caminho}\` | ${nota('performance')} | ${nota('accessibility')} | ${nota('best-practices')} | ${nota('seo')} |`);
    console.log(perfil, caminho, CATEGORIAS.map((k) => `${k}=${nota(k)}`).join(' '));
  }
}
await chrome.kill();

const resumo = `# Lighthouse: resumo\n\nGerado em ${new Date().toISOString()} contra \`${BASE}\` (build de produção servido por \`astro preview\`), Lighthouse 13 (tema escuro, o padrão do site).\nPerfil móvel = padrão do Lighthouse (Moto G Power, 4G lento simulado); desktop = preset desktop.\n\n| Perfil | Página | Desempenho | Acessibilidade | Boas práticas | SEO |\n|---|---|---|---|---|---|\n${linhas.join('\n')}\n\nRelatórios completos: arquivos \`<perfil>-<página>.html\` (abrir no navegador) e \`.json\` nesta pasta.\n`;
writeFileSync(join(SAIDA, 'RESUMO.md'), resumo);
