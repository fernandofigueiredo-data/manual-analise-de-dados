// Comportamentos presentes em todas as páginas.

/* ------------------------------------------------ tema claro/escuro */
const raiz = document.documentElement;
const botaoTema = document.querySelector('[data-tema]');
function rotuloTema() {
  const escuro = raiz.getAttribute('data-theme') === 'dark';
  botaoTema?.setAttribute('aria-label', escuro ? 'Ativar tema claro' : 'Ativar tema escuro');
}
rotuloTema();
botaoTema?.addEventListener('click', () => {
  const novo = raiz.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  raiz.setAttribute('data-theme', novo);
  try { localStorage.setItem('tema', novo); } catch (e) { /* armazenamento indisponível */ }
  rotuloTema();
});

/* ------------------------------------------------ gaveta de navegação (celular) */
const lateral = document.getElementById('lateral');
const veu = document.querySelector('.veu');
const abreMenu = document.querySelector('.abre-menu');
const movel = matchMedia('(max-width: 767px)');
function menu(abrir) {
  if (!lateral) return;
  lateral.classList.toggle('aberta', abrir);
  if (veu) veu.hidden = !abrir;
  abreMenu?.setAttribute('aria-expanded', String(abrir));
  abreMenu?.setAttribute('aria-label', abrir ? 'Fechar menu de navegação' : 'Abrir menu de navegação');
  if (abrir) lateral.querySelector('[aria-current="page"], summary')?.focus();
  else if (movel.matches) abreMenu?.focus();
}
abreMenu?.addEventListener('click', () => menu(!lateral.classList.contains('aberta')));
veu?.addEventListener('click', () => menu(false));
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && lateral?.classList.contains('aberta')) menu(false);
});
movel.addEventListener('change', () => menu(false));
{
  // centraliza o item atual sem mover o ponto de partida do foco (scrollIntoView moveria)
  const atualNav = lateral?.querySelector('[aria-current="page"]');
  if (atualNav) lateral.scrollTop = atualNav.offsetTop - lateral.clientHeight / 2;
}

/* ------------------------------------------------ índice da página: seção visível */
const linksToc = [...document.querySelectorAll('.toc a[data-toc]')];
if (linksToc.length && 'IntersectionObserver' in window) {
  const porId = new Map(linksToc.map((a) => [a.dataset.toc, a]));
  let atual = null;
  const obs = new IntersectionObserver((entradas) => {
    for (const en of entradas) {
      if (!en.isIntersecting) continue;
      const a = porId.get(en.target.id || en.target.dataset.ancora);
      if (!a || a === atual) continue;
      atual?.removeAttribute('aria-current');
      a.setAttribute('aria-current', 'true');
      atual = a;
    }
  }, { rootMargin: '-10% 0px -80% 0px' });
  for (const id of porId.keys()) {
    const alvo = document.getElementById(id);
    if (alvo) obs.observe(alvo);
  }
}

/* ------------------------------------------------ copiar */
export async function copiarTexto(texto) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(texto);
      return true;
    }
  } catch (e) { /* cai no método antigo */ }
  const ta = document.createElement('textarea');
  ta.value = texto;
  ta.setAttribute('readonly', '');
  ta.className = 'sr-only';
  document.body.appendChild(ta);
  ta.select();
  let ok = false;
  try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
  ta.remove();
  return ok;
}

const aviso = document.createElement('p');
aviso.className = 'sr-only';
aviso.setAttribute('aria-live', 'polite');
document.body.appendChild(aviso);
export function anunciar(msg) {
  aviso.textContent = '';
  setTimeout(() => { aviso.textContent = msg; }, 50);
}

export function feedbackCopia(botao, ok, rotuloOriginal) {
  botao.textContent = ok ? 'Copiado' : 'Selecione e copie';
  botao.dataset.estado = ok ? 'ok' : 'erro';
  anunciar(ok ? 'Copiado para a área de transferência' : 'Não foi possível copiar');
  setTimeout(() => { botao.textContent = rotuloOriginal; delete botao.dataset.estado; }, 1800);
}

document.addEventListener('click', async (e) => {
  const botao = e.target.closest('[data-copiar]');
  if (!botao) return;
  const code = botao.closest('.codigo')?.querySelector('code');
  if (!code) return;
  const linhas = [...code.querySelectorAll('.ln')];
  const texto = linhas.length ? linhas.map((l) => l.textContent).join('\n') : code.textContent;
  feedbackCopia(botao, await copiarTexto(texto + '\n'), 'Copiar');
});

/* ------------------------------------------------ ampliar figura */
const dialogoFig = document.getElementById('dialogo-figura');
let imgFig = null;
let origemFoco = null;
document.addEventListener('click', (e) => {
  const bt = e.target.closest('[data-ampliar]');
  if (!bt || !dialogoFig) return;
  const img = bt.querySelector('img');
  if (!imgFig) {
    imgFig = document.createElement('img');
    dialogoFig.appendChild(imgFig);
  }
  imgFig.src = img.currentSrc || img.src;
  imgFig.alt = img.alt;
  origemFoco = bt;
  dialogoFig.showModal();
});
dialogoFig?.querySelector('[data-fecha-figura]')?.addEventListener('click', () => dialogoFig.close());
dialogoFig?.addEventListener('click', (e) => { if (e.target === dialogoFig) dialogoFig.close(); });
dialogoFig?.addEventListener('close', () => origemFoco?.focus());

/* ------------------------------------------------ imprimir (guia de relatório) */
document.addEventListener('click', (e) => {
  if (e.target.closest('[data-imprimir]')) window.print();
});

/* ------------------------------------------------ busca (Pagefind) */
const dialogo = document.getElementById('dialogo-busca');
const entrada = document.getElementById('busca-entrada');
const lista = document.getElementById('busca-resultados');
const estado = document.getElementById('busca-estado');
let carga = null;
let consulta = 0;
let selecionado = -1;
let espera = null;

function carregarPagefind() {
  if (!carga) {
    const caminho = '/pagefind/pagefind.js';
    carga = import(/* @vite-ignore */ caminho).then(async (pf) => {
      await pf.options({ excerptLength: 22, highlightParam: 'destaque' });
      await pf.init();
      return pf;
    });
    carga.catch(() => { carga = null; });
  }
  return carga;
}

function abrirBusca() {
  if (!dialogo || dialogo.open) return;
  dialogo.showModal();
  entrada.focus();
  entrada.select();
  carregarPagefind().catch(() => {
    estado.textContent = 'A busca fica disponível depois do build (npm run build e npm run preview).';
  });
}
document.querySelectorAll('[data-abre-busca]').forEach((b) => b.addEventListener('click', abrirBusca));
dialogo?.querySelector('[data-fecha-busca]')?.addEventListener('click', () => dialogo.close());
dialogo?.addEventListener('click', (e) => { if (e.target === dialogo) dialogo.close(); });
document.addEventListener('keydown', (e) => {
  const tag = (e.target.tagName || '').toLowerCase();
  const digitando = tag === 'input' || tag === 'textarea' || tag === 'select' || e.target.isContentEditable;
  if ((e.key === '/' && !digitando) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) {
    e.preventDefault();
    abrirBusca();
  }
});

function escapar(s) {
  return s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

function marcar(i) {
  const itens = [...lista.querySelectorAll('a')];
  itens.forEach((a, j) => { if (j === i) a.dataset.ativo = ''; else delete a.dataset.ativo; });
  selecionado = i;
  itens[i]?.scrollIntoView({ block: 'nearest' });
}

function agendarBusca() {
  clearTimeout(espera);
  espera = setTimeout(buscar, 150);
}

async function buscar() {
  const q = entrada.value.trim();
  const minha = ++consulta;
  selecionado = -1;
  if (q.length < 2) {
    lista.innerHTML = '';
    estado.textContent = 'Digite pelo menos duas letras.';
    return;
  }
  estado.innerHTML = '<span class="carregando" aria-hidden="true"></span> Buscando…';
  let pf;
  try { pf = await carregarPagefind(); } catch (e) { return; }
  const res = await pf.search(q);
  if (!res || minha !== consulta) return;
  const dados = await Promise.all(res.results.slice(0, 10).map((r) => r.data()));
  if (minha !== consulta) return;
  lista.innerHTML = dados.map((d, i) => {
    const sub = (d.sub_results || []).find((s) => s.url !== d.url) || null;
    const destino = sub ? sub.url : d.url;
    const secao = sub ? `<span class="busca__secao">${escapar(sub.title)}</span>` : '';
    return `<li><a href="${destino}" id="res-${i}">` +
      `<span class="busca__titulo">${escapar(d.meta.title || d.url)}</span>${secao}` +
      `<span class="busca__trecho">${(sub || d).excerpt}</span></a></li>`;
  }).join('');
  estado.textContent = dados.length
    ? `${res.results.length} ${res.results.length === 1 ? 'página encontrada' : 'páginas encontradas'}. Use as setas para navegar.`
    : 'Nenhum resultado. Tente outro termo.';
}
entrada?.addEventListener('input', agendarBusca);
entrada?.addEventListener('keydown', (e) => {
  const itens = lista.querySelectorAll('a');
  if (e.key === 'ArrowDown' && itens.length) { e.preventDefault(); marcar(Math.min(selecionado + 1, itens.length - 1)); }
  else if (e.key === 'ArrowUp' && itens.length) { e.preventDefault(); marcar(Math.max(selecionado - 1, 0)); }
  else if (e.key === 'Enter' && itens.length) { e.preventDefault(); (itens[selecionado] || itens[0]).click(); }
});
lista?.addEventListener('click', (e) => { if (e.target.closest('a')) dialogo.close(); });

/* ------------------------------------------------ destaque dos termos buscados (?destaque=…) */
const termoBuscado = new URLSearchParams(location.search).get('destaque');
if (termoBuscado) {
  const caminho = '/pagefind/pagefind-highlight.js';
  import(/* @vite-ignore */ caminho).then(() => {
    // eslint-disable-next-line no-undef
    new PagefindHighlight({ highlightParam: 'destaque', markContext: '[data-pagefind-body]' });
    setTimeout(() => {
      const marcas = document.querySelectorAll('mark.pagefind-highlight');
      marcas.forEach((m) => { let d = m.closest('details'); while (d) { d.open = true; d = d.parentElement?.closest('details'); } });
      if (!location.hash && marcas[0]) marcas[0].scrollIntoView({ block: 'center' });
    }, 120);
  }).catch(() => { /* destaque indisponível fora do build */ });
}
