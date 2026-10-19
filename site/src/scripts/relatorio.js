// Guia do relatório profissional: copiar modelos, versão fraca/forte, listas de verificação,
// briefing com resumo automático, abrir/fechar modelos e impressão. Portado do script original.
// Como no original, marcações e campos ficam só em memória: voltam ao início ao recarregar.
import { copiarTexto, feedbackCopia } from './base.js';

/* ---------- copiar modelos e resumo ---------- */
document.addEventListener('click', async (ev) => {
  const b = ev.target.closest('[data-copy]');
  if (!b) return;
  const alvo = document.querySelector(b.getAttribute('data-copy'));
  if (alvo) feedbackCopia(b, await copiarTexto(alvo.textContent.trim()), b.textContent);
});

/* ---------- versão fraca / forte ---------- */
document.querySelectorAll('[data-compare]').forEach((c) => {
  const botoes = c.querySelectorAll('.seg button');
  botoes.forEach((b) => {
    b.addEventListener('click', () => {
      const v = b.getAttribute('data-v');
      botoes.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      c.querySelector('.v-fraca').hidden = v !== 'fraca';
      c.querySelector('.v-forte').hidden = v !== 'forte';
    });
  });
});

/* ---------- listas de verificação ---------- */
document.querySelectorAll('.check[data-etapa]').forEach((box) => {
  const caixas = box.querySelectorAll('input[type=checkbox]');
  const barra = box.querySelector('.bar');
  barra?.setAttribute('role', 'progressbar');
  barra?.setAttribute('aria-label', box.querySelector('h3')?.textContent || 'Progresso');
  barra?.setAttribute('aria-valuemin', '0');
  barra?.setAttribute('aria-valuemax', String(caixas.length));
  function atualizar() {
    const feitos = [...caixas].filter((cx) => cx.checked).length;
    box.querySelector('.check-count').textContent = `${feitos} de ${caixas.length}`;
    box.querySelector('.bar > span').style.transform = `scaleX(${caixas.length ? feitos / caixas.length : 0})`;
    barra?.setAttribute('aria-valuenow', String(feitos));
  }
  box.addEventListener('change', atualizar);
  atualizar();
});

/* ---------- briefing ---------- */
const form = document.getElementById('formBriefing');
const saida = document.getElementById('briefing-saida');
if (form && saida) {
  saida.setAttribute('aria-live', 'polite');
  saida.setAttribute('tabindex', '0');
  const briefing = {};
  const v = (rotulo) => (briefing[rotulo] || '').trim() || '[a definir]';
  const f = (rotulo) => v(rotulo).replace(/[.;:!?\s]+$/, '');
  function gerarResumo() {
    form.querySelectorAll('[data-b]').forEach((el) => { briefing[el.getAttribute('data-b')] = el.value; });
    const linhas = [
      'BRIEFING DA DEMANDA',
      '',
      'Demandante: ' + v('Demandante'),
      'Quem decide: ' + v('Quem decide'),
      'Prazo: ' + v('Prazo'),
      'Formato de entrega: ' + v('Formato'),
      '',
      'Pergunta de negócio: ' + v('Pergunta de negócio'),
      'Decisão que o relatório apoia: ' + v('Decisão que o relatório apoia'),
      'Critério de sucesso: ' + v('Critério de sucesso'),
      '',
      'Escopo: ' + v('Escopo'),
      'Fora do escopo: ' + v('Fora do escopo'),
      'Fontes de dados: ' + v('Fontes de dados'),
      'Hipóteses do demandante: ' + v('Hipóteses do demandante'),
      'Outros leitores: ' + v('Outros leitores'),
      'Restrições: ' + v('Restrições'),
      '',
      'Declaração do problema:',
      f('Quem decide') + ' precisa decidir ' + f('Decisão que o relatório apoia') + ' até ' + f('Prazo') +
        '. Para isso, precisa saber: ' + f('Pergunta de negócio') + '. Escopo: ' + f('Escopo') +
        '. O relatório terá cumprido seu papel se: ' + f('Critério de sucesso') + '.',
      '',
      'Por favor, confirme se este resumo reflete o pedido ou indique o que ajustar.',
    ];
    saida.textContent = linhas.join('\n');
  }
  form.addEventListener('input', gerarResumo);
  form.addEventListener('change', gerarResumo);
  document.getElementById('limparBriefing')?.addEventListener('click', () => { form.reset(); gerarResumo(); });
  gerarResumo();
}

/* ---------- seções recolhíveis ---------- */
const dobras = document.querySelectorAll('#modelo-secoes details.fold');
document.getElementById('abrirTodas')?.addEventListener('click', () => dobras.forEach((d) => { d.open = true; }));
document.getElementById('fecharTodas')?.addEventListener('click', () => dobras.forEach((d) => { d.open = false; }));

/* ---------- impressão: abre tudo antes e restaura depois ---------- */
let abertosAntes = [];
window.addEventListener('beforeprint', () => {
  abertosAntes = [];
  document.querySelectorAll('details').forEach((d) => { abertosAntes.push(d.open); d.open = true; });
});
window.addEventListener('afterprint', () => {
  document.querySelectorAll('details').forEach((d, i) => { d.open = abertosAntes[i]; });
});
