// Guia matplotlib e seaborn: abas, antes/depois, passos, realce de linhas por eixo e filtros do catálogo.
// Portado de app.js do guia original, adaptado para várias páginas.

function recipiente(el) { return el.closest('.card, .bloco, .ba-bloco'); }

function aplicaEixo(cont, eixo) {
  if (!cont) return 0;
  cont.querySelectorAll('.ln.hl').forEach((l) => l.classList.remove('hl'));
  cont.dataset.eixo = eixo || '';
  cont.querySelectorAll('.chip.eixo').forEach((c) => {
    c.setAttribute('aria-pressed', String(!!eixo && c.dataset.axis === eixo));
  });
  if (!eixo) return 0;
  let total = 0;
  cont.querySelectorAll('.pane:not([hidden]) .codeblock').forEach((cb) => {
    const linhas = JSON.parse(cb.dataset.axes || '{}')[eixo] || [];
    let primeira = null;
    linhas.forEach((n) => {
      const ln = cb.querySelector(`.ln[data-n="${n}"]`);
      if (ln) { ln.classList.add('hl'); primeira = primeira || ln; total++; }
    });
    if (primeira) {
      const pre = cb.querySelector('pre');
      pre.scrollTop += primeira.getBoundingClientRect().top - pre.getBoundingClientRect().top - 40;
    }
  });
  return total;
}

document.querySelectorAll('.chip.eixo').forEach((chip) => {
  chip.setAttribute('aria-pressed', 'false');
  chip.title = 'Realçar as linhas de código que aplicam este eixo';
  chip.addEventListener('click', () => {
    const cont = recipiente(chip);
    if (!cont) return;
    const ativo = cont.dataset.eixo === chip.dataset.axis;
    aplicaEixo(cont, ativo ? '' : chip.dataset.axis);
  });
});

/* ------------------------------------------------ alternadores (abas, antes e depois, passos) */
document.querySelectorAll('.switch').forEach((sw) => {
  const abas = [...sw.querySelectorAll(':scope > .seg > button')];
  const paineis = [...sw.querySelectorAll(':scope > .pane')];
  const anterior = sw.querySelector('.prev');
  const proximo = sw.querySelector('.next');
  let atual = 0;
  function seleciona(i, foco) {
    atual = i;
    abas.forEach((a, j) => {
      a.setAttribute('aria-selected', String(j === i));
      a.tabIndex = j === i ? 0 : -1;
    });
    paineis.forEach((p, j) => { p.hidden = j !== i; });
    if (foco) abas[i].focus();
    if (anterior) { anterior.disabled = i === 0; proximo.disabled = i === abas.length - 1; }
    const cont = recipiente(sw);
    if (cont && cont.dataset.eixo) aplicaEixo(cont, cont.dataset.eixo);
  }
  sw._seleciona = seleciona;
  sw._atual = () => atual;
  sw._abas = abas;
  abas.forEach((a, i) => {
    a.addEventListener('click', () => seleciona(i));
    a.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); seleciona((i + 1) % abas.length, true); }
      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); seleciona((i - 1 + abas.length) % abas.length, true); }
      if (e.key === 'Home') { e.preventDefault(); seleciona(0, true); }
      if (e.key === 'End') { e.preventDefault(); seleciona(abas.length - 1, true); }
    });
  });
  anterior?.addEventListener('click', () => { if (atual > 0) seleciona(atual - 1); });
  proximo?.addEventListener('click', () => { if (atual < abas.length - 1) seleciona(atual + 1); });
  seleciona(0);
});

/* ------------------------------------------------ filtros e busca do catálogo */
const busca = document.getElementById('busca-catalogo');
const cards = [...document.querySelectorAll('article.card')];
const estado = { sit: 'todas', lib: 'todas', q: '' };
const contagem = document.querySelector('.filtros-catalogo .contagem');
const vazio = document.querySelector('.vazio');

function normaliza(s) {
  return (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
}
function passaFiltro(el) {
  const sits = (el.dataset.sit || '').split(' ');
  const libs = (el.dataset.lib || '').split(' ');
  return (estado.sit === 'todas' || sits.includes(estado.sit)) && (estado.lib === 'todas' || libs.includes(estado.lib));
}
function aplicaFiltros() {
  if (!busca) return;
  const q = normaliza(estado.q);
  let n = 0;
  cards.forEach((c) => {
    const ok = passaFiltro(c) && (!q || (c.dataset.busca || '').includes(q));
    c.hidden = !ok;
    if (ok) n++;
    if (ok && estado.lib !== 'todas') {
      const sw = c.querySelector('.switch');
      if (sw && sw._abas[sw._atual()].dataset.lib !== estado.lib) {
        const idx = sw._abas.findIndex((a) => a.dataset.lib === estado.lib);
        if (idx >= 0) sw._seleciona(idx);
      }
    }
  });
  const filtrando = estado.sit !== 'todas' || estado.lib !== 'todas' || q;
  contagem.textContent = filtrando ? `${n} de ${cards.length} gráficos no catálogo` : '';
  if (vazio) vazio.hidden = n > 0;
  document.querySelectorAll('.toc a[data-toc], .toc-movel a').forEach((a) => {
    const alvo = document.getElementById(a.getAttribute('href').slice(1));
    if (alvo && alvo.matches('article.card')) a.parentElement.hidden = alvo.hidden;
  });
}
function limpaFiltros() {
  estado.sit = 'todas'; estado.lib = 'todas'; estado.q = '';
  if (busca) busca.value = '';
  document.querySelectorAll('.filtro').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.valor === 'todas')));
  aplicaFiltros();
}
if (busca) {
  document.querySelectorAll('.filtro').forEach((bt) => {
    bt.addEventListener('click', () => {
      const grupo = bt.dataset.grupo;
      estado[grupo] = bt.dataset.valor;
      document.querySelectorAll(`.filtro[data-grupo="${grupo}"]`).forEach((b) => b.setAttribute('aria-pressed', String(b === bt)));
      aplicaFiltros();
    });
  });
  busca.addEventListener('input', () => { estado.q = busca.value; aplicaFiltros(); });
  busca.addEventListener('keydown', (e) => { if (e.key === 'Escape') { busca.value = ''; estado.q = ''; aplicaFiltros(); } });
  aplicaFiltros();
}

/* ------------------------------------------------ "onde aparece no código": abre o exemplo e realça as linhas */
function mostraLinhas(id, eixo, rolar) {
  const alvo = document.getElementById(id);
  if (!alvo) return;
  if (alvo.hidden) limpaFiltros();
  const sw = alvo.querySelector('.switch');
  if (sw && sw._abas) {
    const visivel = sw.querySelector('.pane:not([hidden]) .codeblock');
    const tem = visivel && (JSON.parse(visivel.dataset.axes || '{}')[eixo] || []).length;
    if (!tem) {
      const paineis = [...sw.querySelectorAll(':scope > .pane')];
      const idx = paineis.findIndex((p) => {
        const cb = p.querySelector('.codeblock');
        return cb && (JSON.parse(cb.dataset.axes || '{}')[eixo] || []).length;
      });
      if (idx >= 0) sw._seleciona(idx);
    }
  }
  if (rolar) alvo.scrollIntoView({ block: 'start' });
  aplicaEixo(alvo, eixo);
}

document.querySelectorAll('.mostra-linhas').forEach((a) => {
  const destino = new URL(a.getAttribute('href'), location.href);
  destino.searchParams.set('eixo', a.dataset.axis);
  a.href = destino.pathname + destino.search + destino.hash;
  a.addEventListener('click', (e) => {
    if (destino.pathname !== location.pathname) return;   // outra página: navegação normal
    e.preventDefault();
    history.pushState(null, '', destino.search + destino.hash);
    mostraLinhas(destino.hash.slice(1), a.dataset.axis, true);
  });
});

const params = new URLSearchParams(location.search);
if (params.get('eixo') && location.hash) {
  const id = decodeURIComponent(location.hash.slice(1));
  mostraLinhas(id, params.get('eixo'), true);
  window.addEventListener('load', () => document.getElementById(id)?.scrollIntoView({ block: 'start' }), { once: true });
}
