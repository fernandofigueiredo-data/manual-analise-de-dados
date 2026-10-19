// Dados gerados por gerador/gerar.py (src/conteudo/). Ordem da trilha = ordem de navegacao.json.
import navegacao from '../conteudo/navegacao.json';

const arquivos = import.meta.glob('../conteudo/paginas/*.json', { eager: true, import: 'default' });

export const paginas = {};
for (const dados of Object.values(arquivos)) paginas[dados.slug] = dados;

export const modulos = navegacao.modulos;
export const abertura = navegacao.abertura;
export const indice = navegacao.indice;
export const estatisticas = navegacao.estatisticas;
export const versoesGuia = navegacao.versoes_guia;

export const trilha = modulos.flatMap((m) => m.paginas);

export function url(slug) {
  return `/${slug}/`;
}

export function vizinhos(slug) {
  const i = trilha.indexOf(slug);
  return {
    anterior: i > 0 ? paginas[trilha[i - 1]] : null,
    proxima: i >= 0 && i < trilha.length - 1 ? paginas[trilha[i + 1]] : null,
  };
}

export function modulo(id) {
  return modulos.find((m) => m.id === id);
}
