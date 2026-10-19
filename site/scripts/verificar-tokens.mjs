// Verifica que nenhum valor de cor, fonte, tamanho de fonte, espaçamento, raio, sombra ou duração
// aparece fora dos tokens do design system (src/styles/tokens.css).
// Roda antes de todo build (npm run build). Sai com código 1 se encontrar violações.
//
// Exceções pontuais são aceitas quando a linha traz o comentário /* token-exceção: motivo */.
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = fileURLToPath(new URL('..', import.meta.url));
const violacoes = [];

function arquivos(dir, filtro) {
  const saida = [];
  for (const nome of readdirSync(dir)) {
    const p = join(dir, nome);
    if (statSync(p).isDirectory()) saida.push(...arquivos(p, filtro));
    else if (filtro(p)) saida.push(p);
  }
  return saida;
}

const CORES_NOMEADAS = /\b(white|black|red|green|blue|gray|grey|orange|yellow|purple|pink|brown|navy|teal|silver|maroon|olive|lime|aqua|fuchsia|steelblue|lightgray|darkgray)\b/i;
const COR_LITERAL = /#[0-9a-f]{3,8}\b|\brgba?\(|\bhsla?\(|\boklch\(|\blab\(/i;
const ESPACO = /^(margin|padding|gap|row-gap|column-gap|top|right|bottom|left|inset)(-[a-z-]+)?$/;
const SO_TOKENS = /^(font-size|border-radius|box-shadow|line-height|letter-spacing)$/;

function valorSoComTokens(valor) {
  // aceita var(), calc() com var(), 0, auto, palavras-chave e porcentagens de 100%
  const limpo = valor
    .replace(/!important/g, '')
    .replace(/calc\([^;]*\)/g, (m) => (m.includes('var(') ? 'TOKEN' : m))
    .replace(/var\([^)]*\)\)?/g, 'TOKEN')
    .trim();
  return limpo.split(/[\s,/]+/).every((parte) =>
    parte === '' || parte === 'TOKEN' || parte === '0' || parte === '-0' ||
    /^(auto|none|inherit|initial|unset|normal|transparent|currentColor|100%|-100%|50%|0%)$/i.test(parte));
}

function verificarCss(caminho, texto) {
  const rel = relative(RAIZ, caminho);
  let emFontFace = false;
  texto.split('\n').forEach((linha, i) => {
    if (linha.includes('token-exceção')) return;
    if (/@font-face/.test(linha)) emFontFace = true;
    const semComentario = linha.replace(/\/\*.*?\*\//g, '');
    for (const m of semComentario.matchAll(/([a-z-]+)\s*:\s*([^;{}]+)/g)) {
      const [, prop, valor] = m;
      if (prop.startsWith('--')) continue;
      if (/^(content|grid-template|grid-column|counter)/.test(prop)) continue;
      const onde = `${rel}:${i + 1}`;
      if (COR_LITERAL.test(valor) || (CORES_NOMEADAS.test(valor) && !/url\(/.test(valor))) {
        violacoes.push(`${onde}  cor literal em "${prop}: ${valor.trim()}"`);
      }
      if (prop === 'font-family' && !emFontFace && !/^\s*(var\(|inherit)/.test(valor)) {
        violacoes.push(`${onde}  fonte fora dos tokens: ${valor.trim()}`);
      }
      if ((ESPACO.test(prop) || SO_TOKENS.test(prop)) && !valorSoComTokens(valor)) {
        violacoes.push(`${onde}  valor literal em "${prop}: ${valor.trim()}"`);
      }
      if (/^(transition|animation)/.test(prop) && /\d+m?s\b/.test(valor) && !valor.includes('var(')) {
        violacoes.push(`${onde}  duração literal em "${prop}: ${valor.trim()}"`);
      }
    }
    if (emFontFace && linha.includes('}')) emFontFace = false;
  });
}

// 1. folhas de estilo (exceto tokens.css, que é a fonte dos valores)
for (const css of arquivos(join(RAIZ, 'src/styles'), (p) => p.endsWith('.css') && !p.endsWith('tokens.css'))) {
  verificarCss(css, readFileSync(css, 'utf8'));
}

// 2. componentes e páginas: sem atributo style e sem <style> com literais
for (const astro of arquivos(join(RAIZ, 'src'), (p) => p.endsWith('.astro'))) {
  const texto = readFileSync(astro, 'utf8');
  const rel = relative(RAIZ, astro);
  if (/\sstyle=/.test(texto)) violacoes.push(`${rel}  atributo style= em componente`);
  for (const m of texto.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)) verificarCss(astro, m[1]);
}

// 3. conteúdo gerado: sem style=, sem fill/stroke com cor literal
for (const json of arquivos(join(RAIZ, 'src/conteudo'), (p) => p.endsWith('.json'))) {
  const texto = readFileSync(json, 'utf8');
  const rel = relative(RAIZ, json);
  if (/\sstyle=\\?"/.test(texto)) violacoes.push(`${rel}  atributo style= no conteúdo gerado`);
  if (/(fill|stroke)=\\?"#/i.test(texto)) violacoes.push(`${rel}  cor literal em SVG do conteúdo gerado`);
}

if (violacoes.length) {
  console.error(`verificar-tokens: ${violacoes.length} violação(ões)\n  ` + violacoes.join('\n  '));
  process.exit(1);
}
console.log('verificar-tokens: nenhum valor fora dos tokens do design system.');
