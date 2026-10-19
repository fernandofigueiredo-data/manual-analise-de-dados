// Capturas de tela para verificação do layout responsivo (375, 768 e 1440 px) e dos dois temas.
// Uso: com o preview rodando (npm run preview), node scripts/capturas.mjs [url-base]
// Saída: ../docs/capturas/<pagina>-<largura>-<tema>[-<trecho>].png
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const BASE = process.argv[2] || 'http://localhost:4321';
const SAIDA = join(fileURLToPath(new URL('..', import.meta.url)), '..', 'docs', 'capturas');
mkdirSync(SAIDA, { recursive: true });

const PAGINAS = [
  { nome: 'inicio', url: '/' },
  { nome: 'codigo-consultas-sql', url: '/preparar/consultas-sql/', trecho: '.codigo' },
  { nome: 'graficos-analise-univariada', url: '/explorar/analise-univariada/', trecho: '.figura' },
  { nome: 'catalogo-de-graficos', url: '/visualizar/catalogo-de-graficos/', trecho: '#g-barras-v' },
  { nome: 'relatorio-modelo', url: '/comunicar/estruturar-o-relatorio/', trecho: '#relatorio-ficticio' },
  { nome: 'ml-manual', url: '/modelar/manual-de-machine-learning/', trecho: '#legend' },
  { nome: 'ml-cartao-de-modelo', url: '/modelar/aprendizado-supervisionado/#m-xgboost' },
  { nome: 'ml-diagnostico', url: '/modelar/diagnostico-do-dataset/', acao: '#dxExemplo', trecho: '#dxSaida' },
];
const LARGURAS = [[375, 812], [768, 1024], [1440, 900]];

const b = await chromium.launch();
for (const tema of ['light', 'dark']) {
  for (const [w, h] of LARGURAS) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await ctx.addInitScript((t) => { try { localStorage.setItem('tema', t); } catch (e) {} }, tema);
    const p = await ctx.newPage();
    for (const pg of PAGINAS) {
      if (tema === 'light' && w !== 1440 && pg.nome !== 'inicio') continue;   // claro: sistema derivado, conferido em 1440
      await p.goto(BASE + pg.url, { waitUntil: 'networkidle' });
      const base = `${pg.nome}-${w}-${tema === 'light' ? 'claro' : 'escuro'}`;
      if (pg.acao) { await p.click(pg.acao); await p.waitForFunction(() => !document.getElementById('dxPainel').hidden, null, { timeout: 15000 }); }
      await p.waitForTimeout(250);
      await p.screenshot({ path: join(SAIDA, `${base}.png`) });
      if (pg.trecho) {
        await p.evaluate((sel) => {
          const el = document.querySelector(sel);
          document.documentElement.style.scrollBehavior = 'auto';
          window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 70);
        }, pg.trecho);
        await p.waitForTimeout(250);
        await p.screenshot({ path: join(SAIDA, `${base}-trecho.png`) });
      }
    }
    await ctx.close();
  }
}
// menu de navegação aberto no celular
const ctx = await b.newContext({ viewport: { width: 375, height: 812 } });
await ctx.addInitScript(() => { try { localStorage.setItem('tema', 'dark'); } catch (e) {} });
const p = await ctx.newPage();
await p.goto(BASE + '/explorar/outliers/');
await p.click('.abre-menu');
await p.waitForTimeout(300);
await p.screenshot({ path: join(SAIDA, 'menu-aberto-375-escuro.png') });
await p.keyboard.press('Escape');
await p.keyboard.press('/');
await p.keyboard.type('qui-quadrado');
await p.waitForSelector('#busca-resultados a', { timeout: 8000 });
await p.screenshot({ path: join(SAIDA, 'busca-375-escuro.png') });
await b.close();
console.log('capturas em', SAIDA);
