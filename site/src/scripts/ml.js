// Manual de Machine Learning: legenda/filtros por categoria, expandir/recolher cartões,
// abrir o cartão de destino ao chegar por link e na impressão. Portado do script do manual.

const CATS = {};
document.querySelectorAll('#legend .filtro-cat').forEach((b) => { CATS[b.dataset.tag] = b.textContent; });

/* ---------------- filtros por categoria (combinados: o item precisa ter todas as etiquetas) ---------------- */
const ativos = new Set();
const legenda = document.getElementById('legend');
const estado = document.getElementById('filterState');
const contagem = document.getElementById('contagemModelos');
const itens = [...document.querySelectorAll('#indiceModelos .indice-modelos__item')];

function aplicarFiltros() {
  const tags = [...ativos];
  const passa = (el) => !tags.length || tags.every((t) => (el.dataset.tags || '').split(' ').includes(t));
  let n = 0;
  itens.forEach((li) => { const ok = passa(li); li.hidden = !ok; if (ok) n++; });
  document.querySelectorAll('details.modelo').forEach((c) => { c.hidden = !passa(c); });
  document.querySelectorAll('#matriz7 tbody tr').forEach((tr) => { tr.hidden = !passa(tr); });
  if (estado) estado.textContent = tags.length ? 'filtros: ' + tags.map((t) => CATS[t]).join(' + ') : 'nenhum filtro ativo';
  if (contagem) contagem.textContent = tags.length ? `${n} de ${itens.length} modelos` : `${itens.length} modelos`;
}
legenda?.addEventListener('click', (e) => {
  const b = e.target.closest('.filtro-cat');
  if (!b) return;
  const t = b.dataset.tag;
  if (ativos.has(t)) { ativos.delete(t); b.setAttribute('aria-pressed', 'false'); }
  else { ativos.add(t); b.setAttribute('aria-pressed', 'true'); }
  aplicarFiltros();
});
document.getElementById('clearFilters')?.addEventListener('click', () => {
  ativos.clear();
  legenda?.querySelectorAll('.filtro-cat').forEach((b) => b.setAttribute('aria-pressed', 'false'));
  aplicarFiltros();
});
if (legenda) aplicarFiltros();

/* ---------------- expandir / recolher ---------------- */
const cartoes = () => [...document.querySelectorAll('details.modelo')];
document.querySelector('[data-expandir]')?.addEventListener('click', () => cartoes().forEach((c) => { if (!c.hidden) c.open = true; }));
document.querySelector('[data-recolher]')?.addEventListener('click', () => cartoes().forEach((c) => { c.open = false; }));

/* ---------------- abrir o cartão ao chegar por link (#m-xgboost) ou ao clicar num link interno ---------------- */
function abrirAlvo(hash) {
  if (!hash || hash.length < 2) return;
  const alvo = document.getElementById(decodeURIComponent(hash.slice(1)));
  if (!alvo) return;
  let d = alvo.closest('details');
  while (d) { d.open = true; d = d.parentElement?.closest('details'); }
  if (alvo.tagName === 'DETAILS') alvo.open = true;
  alvo.scrollIntoView({ block: 'start' });
}
abrirAlvo(location.hash);
window.addEventListener('hashchange', () => abrirAlvo(location.hash));

/* ---------------- impressão: cartões saem expandidos ---------------- */
let abertos = [];
window.addEventListener('beforeprint', () => { abertos = cartoes().map((c) => c.open); cartoes().forEach((c) => { c.open = true; }); });
window.addEventListener('afterprint', () => cartoes().forEach((c, i) => { c.open = abertos[i]; }));
