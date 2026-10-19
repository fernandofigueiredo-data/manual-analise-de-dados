// Extrai os dados do manual de ML (CATS, BLOCKS, MODELS, MATRIZ) executando a parte de dados do
// próprio script do manual em um contexto isolado do Node. Saída: JSON no stdout.
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const html = readFileSync(process.argv[2], 'utf8');
const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
const fonte = scripts[0];
const corte = fonte.indexOf('const esc =');
if (corte < 0) throw new Error('marcador "const esc =" não encontrado no script do manual');
const codigo = fonte.slice(0, corte) + '\n;globalThis.__dados = { CATS, BLOCKS, MODELS, MATRIZ };';
const ctx = vm.createContext({});
vm.runInContext(codigo, ctx);
process.stdout.write(JSON.stringify(ctx.__dados));
