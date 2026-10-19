// Auditoria automática de acessibilidade (axe-core, regras WCAG 2.0/2.1/2.2 A e AA)
// em todas as páginas do site, nos temas claro e escuro, mais um teste de teclado.
// Uso: com o preview rodando (npm run preview), node scripts/auditar-a11y.mjs [url-base]
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import { readdirSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const BASE = process.argv[2] || 'http://localhost:4321';
const RAIZ = fileURLToPath(new URL('..', import.meta.url));
const DIST = join(RAIZ, 'dist');

function paginasHtml(dir) {
  const out = [];
  for (const nome of readdirSync(dir)) {
    const p = join(dir, nome);
    if (statSync(p).isDirectory()) { if (nome !== 'pagefind' && nome !== '_astro') out.push(...paginasHtml(p)); }
    else if (nome === 'index.html') out.push('/' + relative(DIST, dir).replaceAll('\\', '/') + (relative(DIST, dir) ? '/' : ''));
  }
  return out.map((u) => u.replace('//', '/'));
}

const urls = paginasHtml(DIST).sort();
const navegador = await chromium.launch();
const resultado = { data: new Date().toISOString(), base: BASE, paginas: urls.length, violacoes: [], teclado: [] };

for (const tema of ['light', 'dark']) {
  const ctx = await navegador.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.addInitScript((t) => { try { localStorage.setItem('tema', t); } catch (e) {} }, tema);
  const pagina = await ctx.newPage();
  for (const u of urls) {
    await pagina.goto(BASE + u, { waitUntil: 'load' });
    const r = await new AxeBuilder({ page: pagina })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    for (const v of r.violations) {
      resultado.violacoes.push({ tema, url: u, regra: v.id, impacto: v.impact, alvos: v.nodes.slice(0, 5).map((n) => n.target.join(' ')), n: v.nodes.length, resumo: v.nodes[0]?.failureSummary });
    }
  }
  await ctx.close();
}

// Teclado: pular para o conteúdo, abrir a busca com "/", fechar com Esc, abrir menu no celular, abas com setas
{
  const ctx = await navegador.newContext({ viewport: { width: 1440, height: 900 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const p = await ctx.newPage();
  const passo = (nome, ok, det = '') => resultado.teclado.push({ nome, ok, det });
  await p.goto(BASE + '/explorar/analise-univariada/');
  await p.keyboard.press('Tab');
  passo('1º Tab foca "Pular para o conteúdo"', await p.evaluate(() => document.activeElement?.classList.contains('pular')));
  await p.keyboard.press('Enter');
  passo('Enter no link leva o foco ao conteúdo', await p.evaluate(() => document.activeElement?.id === 'conteudo' || location.hash === '#conteudo'));
  await p.keyboard.press('/');
  passo('"/" abre a busca com foco no campo', await p.evaluate(() => document.getElementById('dialogo-busca').open && document.activeElement?.id === 'busca-entrada'));
  await p.keyboard.type('qui-quadrado');
  await p.waitForSelector('#busca-resultados a', { timeout: 8000 }).catch(() => {});
  const n = await p.locator('#busca-resultados a').count();
  passo('Busca retorna resultados para "qui-quadrado"', n > 0, `${n} resultados`);
  await p.keyboard.press('ArrowDown');
  await p.keyboard.press('Enter');
  await p.waitForLoadState('load');
  passo('Setas + Enter abrem um resultado', !p.url().endsWith('/explorar/analise-univariada/'), p.url());
  await p.goto(BASE + '/explorar/analise-univariada/');
  await p.keyboard.press('Control+k');
  await p.keyboard.press('Escape');
  passo('Esc fecha a busca', await p.evaluate(() => !document.getElementById('dialogo-busca').open));
  const copiar = p.locator('[data-copiar]').first();
  await copiar.focus();
  await p.keyboard.press('Enter');
  await p.waitForTimeout(300);
  passo('Enter em "Copiar" dá retorno', (await copiar.textContent()).trim() !== 'Copiar', await copiar.textContent());
  const fig = p.locator('[data-ampliar]').first();
  await fig.focus();
  await p.keyboard.press('Enter');
  passo('Enter em uma figura abre a ampliação', await p.evaluate(() => document.getElementById('dialogo-figura').open));
  await p.keyboard.press('Escape');
  passo('Esc fecha a figura e devolve o foco', await p.evaluate(() => !document.getElementById('dialogo-figura').open && document.activeElement?.hasAttribute('data-ampliar')));

  await p.goto(BASE + '/visualizar/catalogo-de-graficos/');
  const aba = p.locator('#g-linha [role="tab"]').first();
  await aba.focus();
  await p.keyboard.press('ArrowRight');
  passo('Setas trocam a aba (matplotlib → seaborn)', await p.evaluate(() => document.activeElement?.getAttribute('aria-selected') === 'true' && document.activeElement?.dataset.lib === 'sns'));
  const chip = p.locator('#g-linha .chip.eixo').first();
  await chip.focus();
  await p.keyboard.press('Enter');
  passo('Enter em um eixo realça linhas do código', (await p.locator('#g-linha .ln.hl').count()) > 0);

  await p.goto(BASE + '/comecar/entender-a-demanda/');
  await p.locator('#b-demandante').focus();
  await p.keyboard.type('Fulana, Operações');
  passo('Briefing atualiza o resumo pelo teclado', (await p.locator('#briefing-saida').textContent()).includes('Fulana, Operações'));
  const caixa = p.locator('.check input').first();
  await caixa.focus();
  await p.keyboard.press('Space');
  passo('Espaço marca item da lista de verificação', (await p.locator('.check .check-count').first().textContent()).startsWith('1 de'));

  await p.goto(BASE + '/modelar/manual-de-machine-learning/');
  const filtro = p.locator('#legend .filtro-cat[data-tag="boo"]');
  await filtro.focus();
  await p.keyboard.press('Enter');
  passo('ML: Enter na etiqueta "Boosting" filtra o índice dos modelos', (await p.locator('#indiceModelos .indice-modelos__item:not([hidden])').count()) === 4,
    `${await p.locator('#indiceModelos .indice-modelos__item:not([hidden])').count()} visíveis`);
  await p.goto(BASE + '/modelar/aprendizado-supervisionado/');
  const resumo = p.locator('#m-xgboost > summary');
  await resumo.focus();
  await p.keyboard.press('Enter');
  passo('ML: Enter abre o cartão do modelo', await p.evaluate(() => document.getElementById('m-xgboost').open));
  await p.goto(BASE + '/modelar/aprendizado-supervisionado/#m-lightgbm');
  passo('ML: link direto #m-lightgbm abre o cartão', await p.evaluate(() => document.getElementById('m-lightgbm').open));
  await p.goto(BASE + '/modelar/diagnostico-do-dataset/');
  await p.locator('#dxExemplo').focus();
  await p.keyboard.press('Enter');
  await p.waitForFunction(() => !document.getElementById('dxPainel').hidden, null, { timeout: 15000 }).catch(() => {});
  passo('ML: diagnóstico do exemplo pelo teclado gera os 16 itens', (await p.locator('#dxSaida .dx-item').count()) === 16,
    `${await p.locator('#dxSaida .dx-item').count()} itens`);
  const objetivo = p.locator('#dxObjetivo');
  await objetivo.focus();
  passo('ML: campos do diagnóstico alcançáveis pelo teclado', await p.evaluate(() => document.activeElement?.id === 'dxObjetivo'));

  const movel = await navegador.newContext({ viewport: { width: 375, height: 812 } });
  const m = await movel.newPage();
  await m.goto(BASE + '/explorar/outliers/');
  await m.locator('.abre-menu').focus();
  await m.keyboard.press('Enter');
  passo('Celular: Enter abre o menu', await m.evaluate(() => document.getElementById('lateral').classList.contains('aberta')));
  await m.keyboard.press('Escape');
  passo('Celular: Esc fecha o menu', await m.evaluate(() => !document.getElementById('lateral').classList.contains('aberta')));
  const largura = await m.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
  passo('Celular: sem rolagem horizontal da página (375 px)', largura);
  await movel.close();
  await ctx.close();
}

await navegador.close();
mkdirSync(join(RAIZ, '..', 'docs', 'qualidade'), { recursive: true });
writeFileSync(join(RAIZ, '..', 'docs', 'qualidade', 'acessibilidade-axe.json'), JSON.stringify(resultado, null, 1));
const falhasTeclado = resultado.teclado.filter((t) => !t.ok);
console.log(`axe: ${resultado.violacoes.length} violação(ões) em ${urls.length} páginas × 2 temas`);
for (const v of resultado.violacoes) console.log(`  [${v.tema}] ${v.url} ${v.regra} (${v.impacto}, ${v.n}) ${v.alvos[0]}`);
console.log(`teclado: ${resultado.teclado.length - falhasTeclado.length}/${resultado.teclado.length} passos ok`);
for (const t of resultado.teclado) console.log(`  ${t.ok ? 'ok ' : 'FALHA'} ${t.nome} ${t.det}`);
process.exit(resultado.violacoes.length || falhasTeclado.length ? 1 : 0);
