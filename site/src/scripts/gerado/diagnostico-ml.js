// Gerado por gerador/guia_ml.py: script do diagnóstico copiado sem alterações de
// manual_machine_learning.html (pacote data-science-htlm).

/* ============================================================
   Diagnóstico de dataset — regras determinísticas, 100% no navegador.
   O arquivo é lido com a File API e analisado aqui; nada é enviado
   pela rede nem gravado em armazenamento. Fonte das regras: skill_decisao_ml.md.
   ============================================================ */
(function(){
"use strict";

const MAX_BYTES = 100 * 1024 * 1024;   // acima disso o navegador sofre; peça uma amostra
const MAX_LINHAS = 500000;             // linhas analisadas (as demais são ignoradas, com aviso)
const AMOSTRA = 50000;                 // linhas usadas nas estatísticas mais caras

/* ===================== utilitários ===================== */
const escH = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const fmtInt = x => Number(x).toLocaleString("pt-BR");
const fmtPct = (x, d) => (100 * x).toLocaleString("pt-BR", {maximumFractionDigits: d == null ? 1 : d}) + "%";
const fmtNum = x => !isFinite(x) ? "—"
  : (Math.abs(x) >= 1e7 || (Math.abs(x) < 1e-3 && x !== 0)) ? x.toExponential(2).replace(".", ",")
  : x.toLocaleString("pt-BR", {maximumFractionDigits: 3});
const pl = (n, um, varios) => fmtInt(n) + " " + (n === 1 ? um : varios);
const cn = s => "`" + String(s).replace(/`/g, "'") + "`";
const lista = (arr, max) => {
  const m = max || 6, a = arr.slice(0, m).map(cn).join(", ");
  return arr.length > m ? a + " e mais " + (arr.length - m) : a;
};
const py = s => JSON.stringify(String(s));
const normNome = s => String(s).normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();

const ROTULO_TIPO = {numerico: "numérico", binario: "binário", categorico: "categórico", texto: "texto livre", data: "data", id: "identificador",
                     constante: "constante", vazia: "vazia", aninhado: "aninhado", imagem: "imagem", audio: "áudio"};
const NA = new Set(["", "na", "n/a", "nan", "null", "none", "nil", "?", "#n/a", "#n/d", "#na", "-", "--", "undefined", "nat"]);

const RE_ID_NOME  = /^(id|uuid|guid|cpf|cnpj|rg|matricula|codigo|cod|key|chave|index|indice|unnamed.*)$|^(id|cod|codigo|num|numero|nr)[_ .-]|[_ .-](id|cod|codigo|uuid|key)$/;
const RE_ENT_NOME = /(cliente|customer|client|user|usuario|paciente|patient|loja|store|conta|account|device|dispositivo|maquina|machine|sensor|empresa|company|aluno|student|fornecedor|vendedor|seller|sessao|session)/;
const RE_TEMPO_NOME = /(^|[_ .-])(data|date|dt|time|timestamp|hora|ano|year|mes|month|periodo|period|semana|week|safra|competencia)([_ .-]|$)|^(data|date|dt|ano|mes)/;
const RE_NASC     = /(nasc|birth)/;
const RE_VAZ_NOME = /(estorno|chargeback|cancelad|cancelamento|motivo|resultado|desfecho|outcome|apos|after|depois|^pos_|_pos$|futur|fechamento|encerr|recuperad|cobranca|quitad|pago_em|data_pag|resolvid|diagnostico_final)/;
const RE_PII_NOME = /(cpf|cnpj|^rg$|e-?mail|telefone|celular|phone|^nome|^name$|nome_|endereco|address|^cep$|logradouro)/;
const RE_USER = /(user|usuario|cliente|customer|client|leitor|comprador|buyer)/;
const RE_ITEM = /(item|produto|product|filme|movie|sku|artigo|musica|song|livro|book|anuncio|conteudo)/;
const RE_TRANS = /(transac|pedido|order|cesta|basket|ticket|cupom|nota_fiscal|venda|compra)/;
const ALVO_NOMES = [
  /^(target|alvo|label|rotulo|y|class|classe|outcome|resposta|desfecho)$/,
  /^(churn|fraude|fraud|default|inadimplente|inadimplencia|cancelou|evadiu|survived|converteu|comprou|is_fraud|is_churn|aprovado)$/,
  /(target|alvo|label|rotulo|churn|fraud|default|inadimpl|cancelou|survived|convert)/
];
const POSITIVOS = new Set(["1", "sim", "s", "yes", "y", "true", "verdadeiro", "t", "v", "positivo", "pos"]);

function quantil(ordenado, q){
  if (!ordenado.length) return NaN;
  const pos = (ordenado.length - 1) * q, b = Math.floor(pos), r = pos - b;
  return ordenado[b + 1] !== undefined ? ordenado[b] + r * (ordenado[b + 1] - ordenado[b]) : ordenado[b];
}

/* ===================== leitura de arquivos ===================== */
async function lerArquivo(file){
  if (file.size > MAX_BYTES)
    throw new Error("O arquivo tem " + (file.size / 1048576).toFixed(0) + " MB e o limite desta página é 100 MB. Envie uma amostra (por exemplo, as primeiras 200 mil linhas).");
  const ext = ((file.name || "").match(/\.([a-z0-9]+)$/i) || [, ""])[1].toLowerCase();
  const buf = await file.arrayBuffer();
  const u8 = new Uint8Array(buf);
  if (!u8.length) throw new Error("O arquivo está vazio.");
  const zip = u8[0] === 0x50 && u8[1] === 0x4b;
  if (ext === "parquet" || (u8[0] === 0x50 && u8[1] === 0x41 && u8[2] === 0x52 && u8[3] === 0x31))
    throw new Error("Parquet não é aceito nesta versão. Exporte como CSV — em pandas: df.to_csv(\"arquivo.csv\", index=False).");
  if (ext === "xls") throw new Error("O formato .xls (Excel 97–2003) não é aceito. Salve a planilha como .xlsx ou .csv.");
  if (ext === "xlsx" || ext === "xlsm" || zip) {
    if (!zip) throw new Error("O arquivo tem extensão .xlsx mas não é uma planilha válida.");
    return lerXlsx(buf);
  }
  const {texto, encoding} = decodificar(u8);
  if (["json", "jsonl", "ndjson"].includes(ext) || /^\s*[\[{]/.test(texto.slice(0, 200)))
    return lerJson(texto, ext, encoding);
  return lerDelimitado(texto, ext, encoding);
}

function decodificar(u8){
  if (u8[0] === 0xff && u8[1] === 0xfe) return {texto: new TextDecoder("utf-16le").decode(u8.subarray(2)), encoding: "utf-16"};
  if (u8[0] === 0xfe && u8[1] === 0xff) return {texto: new TextDecoder("utf-16be").decode(u8.subarray(2)), encoding: "utf-16"};
  try { return {texto: new TextDecoder("utf-8", {fatal: true}).decode(u8).replace(/^\uFEFF/, ""), encoding: "utf-8"}; }
  catch (e) { return {texto: new TextDecoder("windows-1252").decode(u8), encoding: "cp1252"}; }
}

function contarForaDeAspas(linha, sep){
  let c = 0, aspas = false;
  for (let i = 0; i < linha.length; i++) {
    const ch = linha[i];
    if (ch === '"') aspas = !aspas;
    else if (ch === sep && !aspas) c++;
  }
  return c;
}

function detectarSep(texto, ext){
  if (ext === "tsv" || ext === "tab") return "\t";
  const linhas = texto.slice(0, 65536).split(/\r\n|\n|\r/).filter(l => l.trim()).slice(0, 30);
  let melhor = ",", melhorScore = -1;
  for (const sep of [",", ";", "\t", "|"]) {
    const cont = linhas.map(l => contarForaDeAspas(l, sep));
    const freq = new Map(); cont.forEach(c => freq.set(c, (freq.get(c) || 0) + 1));
    let moda = 0, vezes = 0;
    freq.forEach((v, k) => { if (v > vezes || (v === vezes && k > moda)) { moda = k; vezes = v; } });
    if (moda === 0) continue;
    const score = (vezes / cont.length) * 1000 + moda;
    if (score > melhorScore) { melhorScore = score; melhor = sep; }
  }
  return melhor;
}

// CSV no padrão RFC 4180: aspas duplas, "" como escape, quebras de linha dentro de aspas
function parseCsv(t, sep, limite){
  const linhas = []; let linha = [], i = 0, truncado = false;
  const n = t.length;
  while (i < n) {
    let campo;
    if (t.charCodeAt(i) === 34) {
      let j = i + 1, partes = "";
      for (;;) {
        const q = t.indexOf('"', j);
        if (q === -1) { partes += t.slice(j); j = n; break; }
        partes += t.slice(j, q);
        if (t.charCodeAt(q + 1) === 34) { partes += '"'; j = q + 2; continue; }
        j = q + 1; break;
      }
      campo = partes; i = j;
      while (i < n && t[i] !== sep && t[i] !== "\n" && t[i] !== "\r") { campo += t[i]; i++; }
    } else {
      let j = i;
      while (j < n) { const c = t[j]; if (c === sep || c === "\n" || c === "\r") break; j++; }
      campo = t.slice(i, j); i = j;
    }
    linha.push(campo);
    if (i >= n) { linhas.push(linha); break; }
    if (t[i] === sep) { i++; if (i >= n) { linha.push(""); linhas.push(linha); } continue; }
    if (t[i] === "\r" && t[i + 1] === "\n") i += 2; else i++;
    linhas.push(linha); linha = [];
    if (linhas.length > limite) { truncado = i < n; break; }
  }
  return {linhas, truncado};
}

function nomesUnicos(brutos){
  const vistos = new Map();
  return brutos.map((b, k) => {
    let nome = String(b == null ? "" : b).trim() || "coluna_" + (k + 1);
    if (vistos.has(nome)) { const c = vistos.get(nome) + 1; vistos.set(nome, c); nome = nome + "_" + c; }
    else vistos.set(nome, 1);
    return nome;
  });
}

function montar(nomes, cols, meta){
  const n = cols.length ? cols[0].length : 0;
  return {nomes, cols, n, meta};
}

function lerDelimitado(texto, ext, encoding){
  const sep = detectarSep(texto, ext);
  const {linhas, truncado} = parseCsv(texto, sep, MAX_LINHAS + 1);
  const uteis = linhas.filter(l => !(l.length === 1 && l[0].trim() === ""));
  if (uteis.length < 2) throw new Error("Não encontrei linhas de dados: o arquivo precisa de um cabeçalho e ao menos uma linha.");
  const nomes = nomesUnicos(uteis[0]);
  const p = nomes.length, corpo = uteis.slice(1);
  if (p < 2) throw new Error("Só encontrei uma coluna. Confira se o separador é vírgula, ponto e vírgula, tabulação ou barra vertical.");
  const cols = nomes.map(() => new Array(corpo.length));
  let irregulares = 0;
  for (let i = 0; i < corpo.length; i++) {
    const l = corpo[i];
    if (l.length !== p) irregulares++;
    for (let k = 0; k < p; k++) cols[k][i] = k < l.length ? l[k] : "";
  }
  return montar(nomes, cols, {formato: ext === "tsv" ? "TSV" : "CSV", sep, encoding, truncado, irregulares});
}

function valorJson(v, aninhada, nome){
  if (v === null || v === undefined) return "";
  if (typeof v === "object") { aninhada.add(nome); return JSON.stringify(v); }
  return String(v);
}

function lerJson(texto, ext, encoding){
  let dados, linhasJson = false, chave = null, orient = null;
  try { dados = JSON.parse(texto); }
  catch (e) {
    const ls = texto.split(/\r?\n/).filter(l => l.trim());
    try { dados = ls.map(l => JSON.parse(l)); linhasJson = true; }
    catch (e2) { throw new Error("JSON inválido: " + e.message); }
  }
  const aninhadas = new Set();
  const ehObj = x => x && typeof x === "object" && !Array.isArray(x);
  if (ehObj(dados)) {
    const vals = Object.values(dados);
    if (Array.isArray(dados.columns) && Array.isArray(dados.data)) {
      orient = "split";
      const nomes = nomesUnicos(dados.columns);
      const cols = nomes.map((nm, k) => dados.data.slice(0, MAX_LINHAS).map(r => valorJson(r[k], aninhadas, nm)));
      return montar(nomes, cols, {formato: "JSON", encoding, orient, aninhadas, truncado: dados.data.length > MAX_LINHAS});
    }
    if (vals.length > 1 && vals.every(Array.isArray) && new Set(vals.map(v => v.length)).size === 1) {
      orient = "columns-list";
      const nomes = Object.keys(dados);
      const cols = nomes.map(nm => dados[nm].slice(0, MAX_LINHAS).map(x => valorJson(x, aninhadas, nm)));
      return montar(nomes, cols, {formato: "JSON", encoding, orient, aninhadas, truncado: vals[0].length > MAX_LINHAS});
    }
    if (vals.length > 1 && vals.every(ehObj) && !Object.keys(dados).some(k => Array.isArray(dados[k]))) {
      orient = "columns";
      const nomes = Object.keys(dados);
      const idx = []; const vistos = new Set();
      vals.forEach(o => Object.keys(o).forEach(k => { if (!vistos.has(k)) { vistos.add(k); idx.push(k); } }));
      const cols = nomes.map(nm => idx.slice(0, MAX_LINHAS).map(r => valorJson(dados[nm][r], aninhadas, nm)));
      return montar(nomes, cols, {formato: "JSON", encoding, orient, aninhadas, truncado: idx.length > MAX_LINHAS});
    }
    const achado = Object.entries(dados).find(([, v]) => Array.isArray(v) && v.length && v.every(ehObj));
    if (!achado) throw new Error("Não encontrei uma tabela no JSON. Formatos aceitos: lista de objetos, JSON Lines, {coluna: [valores]} ou um objeto com uma lista de registros.");
    chave = achado[0]; dados = achado[1];
  }
  if (!Array.isArray(dados) || !dados.length) throw new Error("O JSON não contém registros.");
  const truncado = dados.length > MAX_LINHAS;
  const regs = dados.slice(0, MAX_LINHAS);
  if (regs.every(Array.isArray)) {
    const nomes = nomesUnicos(regs[0]);
    const cols = nomes.map((nm, k) => regs.slice(1).map(r => valorJson(r[k], aninhadas, nm)));
    return montar(nomes, cols, {formato: "JSON", encoding, orient: "values", aninhadas, truncado});
  }
  const nomes = []; const vistos = new Set();
  for (const o of regs) {
    if (!ehObj(o)) throw new Error("O JSON mistura registros que não são objetos.");
    for (const k of Object.keys(o)) if (!vistos.has(k)) { vistos.add(k); nomes.push(k); }
  }
  const cols = nomes.map(nm => regs.map(o => valorJson(o[nm], aninhadas, nm)));
  return montar(nomes, cols, {formato: linhasJson ? "JSON Lines" : "JSON", encoding, orient: linhasJson ? "lines" : "records", chave, aninhadas, truncado});
}

/* ---------- XLSX: ZIP + XML, com a descompressão nativa do navegador ---------- */
function decodXml(s){
  return s.replace(/&(lt|gt|amp|quot|apos|#x[0-9a-f]+|#\d+);/gi, (m, e) => {
    const l = e.toLowerCase();
    if (l === "lt") return "<"; if (l === "gt") return ">"; if (l === "amp") return "&";
    if (l === "quot") return '"'; if (l === "apos") return "'";
    return String.fromCodePoint(l[1] === "x" ? parseInt(l.slice(2), 16) : parseInt(l.slice(1), 10));
  });
}

async function lerXlsx(buf){
  if (typeof DecompressionStream === "undefined")
    throw new Error("Este navegador não descompacta planilhas nativamente. Atualize o navegador ou exporte a planilha como CSV.");
  const u8 = new Uint8Array(buf), dv = new DataView(buf), td = new TextDecoder();
  let fim = -1;
  for (let i = u8.length - 22; i >= Math.max(0, u8.length - 65557); i--)
    if (dv.getUint32(i, true) === 0x06054b50) { fim = i; break; }
  if (fim < 0) throw new Error("Planilha XLSX inválida (o arquivo não é um ZIP íntegro).");
  const total = dv.getUint16(fim + 10, true);
  let p = dv.getUint32(fim + 16, true);
  const ent = {};
  for (let k = 0; k < total; k++) {
    if (dv.getUint32(p, true) !== 0x02014b50) break;
    const metodo = dv.getUint16(p + 10, true), tam = dv.getUint32(p + 20, true);
    const ln = dv.getUint16(p + 28, true), lx = dv.getUint16(p + 30, true), lc = dv.getUint16(p + 32, true);
    const off = dv.getUint32(p + 42, true);
    ent[td.decode(u8.subarray(p + 46, p + 46 + ln))] = {metodo, tam, off};
    p += 46 + ln + lx + lc;
  }
  async function ler(nome){
    const e = ent[nome]; if (!e) return null;
    const ini = e.off + 30 + dv.getUint16(e.off + 26, true) + dv.getUint16(e.off + 28, true);
    const dados = u8.subarray(ini, ini + e.tam);
    if (e.metodo === 0) return td.decode(dados);
    if (e.metodo !== 8) throw new Error("A planilha usa um método de compressão não suportado.");
    const fluxo = new Blob([dados]).stream().pipeThrough(new DecompressionStream("deflate-raw"));
    return await new Response(fluxo).text();
  }
  const wb = await ler("xl/workbook.xml");
  if (!wb) throw new Error("O arquivo ZIP não contém uma planilha do Excel.");
  const abas = [...wb.matchAll(/<sheet\b[^>]*?name="([^"]*)"[^>]*?r:id="([^"]*)"/g)].map(m => ({nome: decodXml(m[1]), rid: m[2]}));
  let alvo = "xl/worksheets/sheet1.xml";
  const rels = await ler("xl/_rels/workbook.xml.rels");
  if (rels && abas.length) {
    const re = new RegExp('<Relationship\\b[^>]*?Id="' + abas[0].rid + '"[^>]*?Target="([^"]*)"|<Relationship\\b[^>]*?Target="([^"]*)"[^>]*?Id="' + abas[0].rid + '"');
    const m = rels.match(re);
    if (m) { const t = m[1] || m[2]; alvo = t.startsWith("/") ? t.slice(1) : "xl/" + t.replace(/^\.\//, ""); }
  }
  const sst = await ler("xl/sharedStrings.xml");
  const compart = sst ? [...sst.replace(/<rPh\b[\s\S]*?<\/rPh>/g, "").matchAll(/<si>([\s\S]*?)<\/si>/g)]
    .map(m => decodXml([...m[1].matchAll(/<t\b[^>]*>([\s\S]*?)<\/t>/g)].map(x => x[1]).join(""))) : [];
  // estilos: identifica células com formato de data
  const estilos = await ler("xl/styles.xml");
  const ehData = [];
  if (estilos) {
    const custom = {};
    for (const m of estilos.matchAll(/<numFmt\b[^>]*numFmtId="(\d+)"[^>]*formatCode="([^"]*)"/g)) custom[m[1]] = decodXml(m[2]);
    const xfs = (estilos.match(/<cellXfs\b[\s\S]*?<\/cellXfs>/) || [""])[0];
    for (const m of xfs.matchAll(/<xf\b([^>]*)/g)) {
      const id = +((m[1].match(/numFmtId="(\d+)"/) || [, 0])[1]);
      let d = (id >= 14 && id <= 22) || (id >= 45 && id <= 47);
      if (!d && custom[id]) d = /[dmy]/i.test(custom[id].replace(/"[^"]*"|\[[^\]]*\]|\\./g, ""));
      ehData.push(d);
    }
  }
  const xml = await ler(alvo);
  if (!xml) throw new Error("Não encontrei a primeira aba da planilha.");
  const linhas = [];
  let truncado = false;
  const colIdx = ref => { let c = 0; for (const ch of ref) { const k = ch.charCodeAt(0); if (k < 65 || k > 90) break; c = c * 26 + (k - 64); } return c - 1; };
  for (const mr of xml.matchAll(/<row\b[^>]*>([\s\S]*?)<\/row>/g)) {
    if (linhas.length > MAX_LINHAS) { truncado = true; break; }
    const linha = [];
    let auto = 0;
    for (const mc of mr[1].matchAll(/<c\b([^>]*?)(?:\/>|>([\s\S]*?)<\/c>)/g)) {
      const at = mc[1], corpo = mc[2] || "";
      const ref = (at.match(/\br="([A-Z]+)\d+"/) || [])[1];
      const k = ref ? colIdx(ref) : auto;
      auto = k + 1;
      const t = (at.match(/\bt="(\w+)"/) || [])[1];
      const s = +((at.match(/\bs="(\d+)"/) || [, -1])[1]);
      const v = (corpo.match(/<v>([\s\S]*?)<\/v>/) || [])[1];
      let val = "";
      if (t === "s") val = v != null ? (compart[+v] || "") : "";
      else if (t === "inlineStr") val = decodXml([...corpo.matchAll(/<t\b[^>]*>([\s\S]*?)<\/t>/g)].map(x => x[1]).join(""));
      else if (t === "b") val = v === "1" ? "TRUE" : "FALSE";
      else if (t === "e") val = "";
      else if (v != null) {
        val = decodXml(v);
        if (t !== "str" && s >= 0 && ehData[s] && isFinite(+val)) {
          const ms = Date.UTC(1899, 11, 30) + Math.round(+val * 86400000);
          const iso = new Date(ms).toISOString();
          val = +val % 1 === 0 ? iso.slice(0, 10) : iso.slice(0, 19).replace("T", " ");
        }
      }
      linha[k] = val;
    }
    linhas.push(linha);
  }
  while (linhas.length && !linhas[linhas.length - 1].some(x => x != null && x !== "")) linhas.pop();
  if (linhas.length < 2) throw new Error("A primeira aba da planilha não tem cabeçalho e dados.");
  const largura = Math.max(...linhas.map(l => l.length));
  const nomes = nomesUnicos(Array.from({length: largura}, (_, k) => linhas[0][k]));
  const corpo = linhas.slice(1);
  const cols = nomes.map((_, k) => corpo.map(l => l[k] == null ? "" : l[k]));
  return montar(nomes, cols, {formato: "XLSX", encoding: "utf-8", truncado, abas: abas.map(a => a.nome)});
}

/* ===================== perfil das colunas ===================== */
const RE_US = /^[-+]?(?:\d{1,3}(?:,\d{3})+|\d*)(?:\.\d+)?(?:e[-+]?\d+)?$/i;
const RE_BR = /^[-+]?(?:\d{1,3}(?:\.\d{3})+|\d*)(?:,\d+)?(?:e[-+]?\d+)?$/i;
const limpaNum = s => s.replace(/^(?:R\$|US\$|\$|€)\s*/i, "").replace(/\s*%$/, "").replace(/\s/g, "");

function detectarNumero(freq, nn){
  let us = 0, br = 0;
  freq.forEach((c, s) => {
    const t = limpaNum(s);
    if (!/\d/.test(t)) return;
    if (RE_US.test(t)) us += c;
    if (RE_BR.test(t)) br += c;
  });
  const fmt = br > us ? "br" : "us", re = fmt === "br" ? RE_BR : RE_US;
  const mapa = new Map(); let ok = 0, milhar = false; const ruins = [];
  freq.forEach((c, s) => {
    const t = limpaNum(s);
    let x = NaN;
    if (/\d/.test(t) && re.test(t)) {
      if (fmt === "br") { if (t.indexOf(".") >= 0) milhar = true; x = parseFloat(t.replace(/\./g, "").replace(",", ".")); }
      else { if (t.indexOf(",") >= 0) milhar = true; x = parseFloat(t.replace(/,/g, "")); }
    }
    if (isFinite(x)) { mapa.set(s, x); ok += c; } else if (ruins.length < 4) ruins.push(s);
  });
  const frac = nn ? ok / nn : 0;
  return {ok: frac >= 0.95, parcial: frac >= 0.5 && frac < 0.95, frac, fmt, mapa, ruins, milhar};
}

const RE_ISO = /^(\d{4})-(\d{1,2})-(\d{1,2})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?(?:Z|[+-]\d{2}:?\d{2})?)?$/;
const RE_DMY = /^(\d{1,2})[\/.-](\d{1,2})[\/.-](\d{4}|\d{2})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2}))?)?$/;
const RE_YMS = /^(\d{4})\/(\d{1,2})\/(\d{1,2})/;
const RE_YM  = /^(\d{4})-(\d{2})$/;

function detectarData(freq, nn){
  let ok = 0, dmy = 0, primeiroMaior = false, segundoMaior = false;
  freq.forEach((c, s) => {
    let m;
    if (RE_ISO.test(s) || RE_YMS.test(s) || RE_YM.test(s)) ok += c;
    else if ((m = s.match(RE_DMY))) { ok += c; dmy += c; if (+m[1] > 12) primeiroMaior = true; if (+m[2] > 12) segundoMaior = true; }
  });
  const dayfirst = primeiroMaior || !segundoMaior;
  return {ok: nn > 0 && ok / nn >= 0.9, dmy: dmy > ok / 2, dayfirst};
}

function paraTs(s, dayfirst){
  let m;
  if ((m = s.match(RE_ISO))) return Date.UTC(+m[1], +m[2] - 1, +m[3], +(m[4] || 0), +(m[5] || 0), +(m[6] || 0));
  if ((m = s.match(RE_YMS))) return Date.UTC(+m[1], +m[2] - 1, +m[3]);
  if ((m = s.match(RE_YM))) return Date.UTC(+m[1], +m[2] - 1, 1);
  if ((m = s.match(RE_DMY))) {
    let a = +m[3]; if (a < 100) a += a < 70 ? 2000 : 1900;
    const d = dayfirst ? +m[1] : +m[2], me = dayfirst ? +m[2] : +m[1];
    return Date.UTC(a, me - 1, d, +(m[4] || 0), +(m[5] || 0), +(m[6] || 0));
  }
  return NaN;
}

function topK(freq, k){
  const top = [];
  freq.forEach((c, s) => {
    if (top.length < k) { top.push([s, c]); top.sort((a, b) => b[1] - a[1]); }
    else if (c > top[k - 1][1]) { top[k - 1] = [s, c]; top.sort((a, b) => b[1] - a[1]); }
  });
  return top;
}

function estatisticas(p, idx){
  const num = p.num;
  let cnt = 0, media = 0, m2 = 0, min = Infinity, max = -Infinity, inteiro = true, neg = false, zeros = 0;
  for (let i = 0; i < num.length; i++) {
    const x = num[i]; if (x !== x) continue;
    cnt++; const d = x - media; media += d / cnt; m2 += d * (x - media);
    if (x < min) min = x; if (x > max) max = x;
    if (inteiro && !Number.isInteger(x)) inteiro = false;
    if (x < 0) neg = true; if (x === 0) zeros++;
  }
  const dp = cnt > 1 ? Math.sqrt(m2 / cnt) : 0;
  const am = [];
  for (const i of idx) { const x = num[i]; if (x === x) am.push(x); }
  am.sort((a, b) => a - b);
  const med = quantil(am, 0.5);
  const desv = am.map(x => Math.abs(x - med)).sort((a, b) => a - b);
  const mad = quantil(desv, 0.5);
  let out = 0, m3 = 0;
  for (const x of am) { if (mad > 0 && Math.abs(0.6745 * (x - med) / mad) > 3.5) out++; m3 += Math.pow(x - media, 3); }
  Object.assign(p, {cnt, media, dp, min, max, inteiro, naoNeg: !neg, zeros: cnt ? zeros / cnt : 0, med, mad,
    outl: am.length ? out / am.length : 0, assim: dp > 0 && am.length ? (m3 / am.length) / Math.pow(dp, 3) : 0});
}

function perfilColuna(nome, bruto, aninhada, idx){
  const n = bruto.length, nomeN = normNome(nome);
  const v = new Array(n), freq = new Map();
  let nMiss = 0, somaLen = 0, comEspaco = 0;
  for (let i = 0; i < n; i++) {
    const s = bruto[i] == null ? "" : String(bruto[i]).trim();
    if (NA.has(s.toLowerCase())) { v[i] = null; nMiss++; continue; }
    v[i] = s; freq.set(s, (freq.get(s) || 0) + 1);
    somaLen += s.length; if (s.indexOf(" ") > 0) comEspaco++;
  }
  const nn = n - nMiss, distinct = freq.size;
  const p = {nome, nomeN, n, nn, nMiss, pMiss: n ? nMiss / n : 0, distinct, v, freq, top: topK(freq, 3),
             avgLen: nn ? somaLen / nn : 0, tipo: "categorico", alta: false, entidade: false};
  if (nn === 0) { p.tipo = "vazia"; return p; }
  const det = detectarNumero(freq, nn);
  if (det.ok) {
    p.fmt = det.fmt; p.milhar = det.milhar; p.ruins = det.ruins; p.fracNum = det.frac;
    const num = new Float64Array(n);
    for (let i = 0; i < n; i++) { const x = v[i] === null ? undefined : det.mapa.get(v[i]); num[i] = x === undefined ? NaN : x; }
    p.num = num;
  } else if (det.parcial) { p.sujeira = det; }
  if (distinct === 1) { p.tipo = "constante"; return p; }
  if (aninhada) { p.tipo = "aninhado"; return p; }
  if (RE_PII_NOME.test(nomeN)) p.pii = true;
  const pareceId = RE_ID_NOME.test(nomeN) || /[a-z]Id$|^id[A-Z]/.test(nome);
  if (distinct === 2) { p.tipo = "binario"; if (p.num) estatisticas(p, idx); return p; }
  if (p.num) {
    estatisticas(p, idx);
    const unico = distinct === nn;
    if (pareceId && distinct >= 0.5 * nn) { p.tipo = "id"; return p; }
    if (unico && p.inteiro && nn > 20 && p.max - p.min + 1 === nn) { p.tipo = "id"; p.sequencial = true; return p; }
    if (pareceId) { p.tipo = "categorico"; p.codigo = true; p.alta = distinct > 50; p.entidade = true; delete p.num; return p; }
    p.tipo = "numerico";
    if (/^(lat|latitude)$/.test(nomeN) && p.min >= -90 && p.max <= 90) p.geo = "lat";
    if (/^(lon|lng|long|longitude)$/.test(nomeN) && p.min >= -180 && p.max <= 180) p.geo = "lon";
    return p;
  }
  const dt = detectarData(freq, nn);
  if (dt.ok) {
    p.tipo = "data"; p.dayfirst = dt.dayfirst; p.dmy = dt.dmy;
    const ts = new Float64Array(n); let ant = NaN, pares = 0, cresc = 0, tmin = Infinity, tmax = -Infinity;
    for (let i = 0; i < n; i++) {
      const t = v[i] === null ? NaN : paraTs(v[i], dt.dayfirst); ts[i] = t;
      if (t === t) { if (ant === ant) { pares++; if (t >= ant) cresc++; } ant = t; if (t < tmin) tmin = t; if (t > tmax) tmax = t; }
    }
    p.ts = ts; p.tmin = tmin; p.tmax = tmax; p.ordenada = pares > 10 && cresc / pares > 0.99;
    return p;
  }
  let img = 0, aud = 0, email = 0, cpf = 0;
  freq.forEach((c, s) => {
    if (/\.(jpe?g|png|gif|bmp|tiff?|webp)$/i.test(s)) img += c;
    if (/\.(wav|mp3|flac|ogg|m4a)$/i.test(s)) aud += c;
    if (/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(s)) email += c;
    if (/^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$/.test(s)) cpf += c;
  });
  if (email / nn > 0.5 || cpf / nn > 0.5) p.pii = true;
  if (img / nn > 0.9) { p.tipo = "imagem"; return p; }
  if (aud / nn > 0.9) { p.tipo = "audio"; return p; }
  const razao = distinct / nn;
  if (p.avgLen >= 25 && comEspaco / nn >= 0.5 && razao >= 0.3) { p.tipo = "texto"; return p; }
  if ((distinct === nn && nn > 20 && p.avgLen < 40) || (pareceId && razao > 0.9)) { p.tipo = "id"; return p; }
  p.tipo = "categorico"; p.alta = distinct > 50;
  if ((pareceId || RE_ENT_NOME.test(nomeN)) && distinct <= 0.9 * nn) p.entidade = true;
  return p;
}

function perfilar(ds){
  const n = ds.n;
  const passo = Math.max(1, Math.floor(n / AMOSTRA));
  const idx = []; for (let i = 0; i < n; i += passo) idx.push(i);
  const aninhadas = ds.meta.aninhadas || new Set();
  const cols = ds.nomes.map((nome, k) => perfilColuna(nome, ds.cols[k], aninhadas.has(nome), idx));
  // duplicatas exatas
  let dup = 0; const vistos = new Set();
  for (let i = 0; i < n; i++) {
    let ch = ""; for (let k = 0; k < cols.length; k++) ch += (cols[k].v[i] === null ? "\u0000" : cols[k].v[i]) + "\u0001";
    if (vistos.has(ch)) dup++; else vistos.add(ch);
  }
  // pares numéricos muito correlacionados (amostra)
  const nums = cols.filter(c => c.num && (c.tipo === "numerico" || c.tipo === "binario")).slice(0, 40);
  const pares = [];
  for (let a = 0; a < nums.length; a++) for (let b = a + 1; b < nums.length; b++) {
    const r = pearson(nums[a].num, nums[b].num, idx);
    if (Math.abs(r) >= 0.9) pares.push([nums[a].nome, nums[b].nome, r]);
  }
  return {ds, cols, n, p: cols.length, idx, dup, pares, meta: ds.meta};
}

function pearson(A, B, idx){
  let m = 0, sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0;
  for (const i of idx) { const x = A[i], y = B[i]; if (x !== x || y !== y) continue; m++; sx += x; sy += y; sxx += x * x; syy += y * y; sxy += x * y; }
  if (m < 30) return 0;
  const d = Math.sqrt((m * sxx - sx * sx) * (m * syy - sy * sy));
  return d > 0 ? (m * sxy - sx * sy) / d : 0;
}

/* ===================== sugestões de contexto ===================== */
const PODE_SER_ALVO = c => ["binario", "categorico", "numerico"].includes(c.tipo);

function sugerirAlvo(P){
  for (const re of ALVO_NOMES) {
    const c = P.cols.find(c => PODE_SER_ALVO(c) && re.test(c.nomeN));
    if (c) return {nome: c.nome, motivo: "nome"};
  }
  const ult = [...P.cols].reverse().find(PODE_SER_ALVO);
  return ult ? {nome: ult.nome, motivo: "ultima"} : null;
}
const opcoesTempo = P => P.cols.filter(c => c.tipo === "data" ||
  (c.tipo === "numerico" && c.inteiro && /^(ano|year|mes|month|periodo|period|safra|semana|week|competencia)/.test(c.nomeN)));
function sugerirTempo(P){
  const c = opcoesTempo(P).find(c => c.tipo === "data" && !RE_NASC.test(c.nomeN));
  return c ? c.nome : "";
}
const opcoesEntidade = P => P.cols.filter(c => c.entidade);
function detectarFormato(P){
  const rep = c => c.distinct >= 2 && c.distinct < c.nn;
  const user = P.cols.find(c => rep(c) && RE_USER.test(c.nomeN) && ["categorico", "id"].includes(c.tipo));
  const item = P.cols.find(c => rep(c) && RE_ITEM.test(c.nomeN) && ["categorico", "id"].includes(c.tipo) && c !== user);
  const trans = P.cols.find(c => rep(c) && RE_TRANS.test(c.nomeN) && ["categorico", "id"].includes(c.tipo));
  const binarias = P.cols.filter(c => c.tipo === "binario" && c.num && c.min === 0 && c.max === 1).length;
  return {interacoes: !!(user && item), user: user && user.nome, item: item && item.nome,
          transacional: !!(trans && item) || binarias >= 5 && binarias >= 0.8 * P.p, trans: trans && trans.nome};
}

/* ===================== análise do alvo ===================== */
function analisarAlvo(P, a){
  const r = {col: a, invalido: null, avisos: []};
  const rot = a.nn;
  if (a.tipo === "vazia" || a.tipo === "constante") { r.invalido = "a coluna " + cn(a.nome) + " tem um único valor — não há o que prever"; return r; }
  if (a.tipo === "id") { r.invalido = cn(a.nome) + " parece um identificador (um valor por linha), não um alvo"; return r; }
  if (["texto", "imagem", "audio", "aninhado"].includes(a.tipo)) { r.invalido = cn(a.nome) + " é " + a.tipo + " livre; esta ferramenta trata alvos de classificação e regressão"; return r; }
  if (a.tipo === "data") { r.invalido = cn(a.nome) + " é uma data; para prever “quando”, defina um alvo de tempo até o evento (análise de sobrevivência) ou um alvo binário com janela"; return r; }
  if (a.tipo === "binario") r.tipo = "binaria";
  else if (a.tipo === "categorico") {
    if (a.distinct > 0.5 * rot) { r.invalido = cn(a.nome) + " tem " + fmtInt(a.distinct) + " valores distintos em " + fmtInt(rot) + " linhas — parece texto ou identificador, não classe"; return r; }
    r.tipo = "multiclasse";
    if (a.distinct > 50) r.avisos.push("[[medio]] " + fmtInt(a.distinct) + " classes: considere agrupar classes raras ou rever se o problema não é de ranking/recomendação");
  } else if (a.tipo === "numerico") {
    if (a.inteiro && a.distinct <= 10 && a.min >= 0) {
      r.tipo = "multiclasse"; r.ordinal = true;
      r.avisos.push("[[info]] alvo inteiro com " + a.distinct + " valores: tratado como multiclasse; se houver ordem (nota 1–5) ou for contagem, avalie regressão ordinal ou de contagem");
    } else if (a.inteiro && a.naoNeg && (a.zeros >= 0.1 || a.assim > 1)) r.tipo = "contagem";
    else r.tipo = "regressao";
  }
  r.clf = r.tipo === "binaria" || r.tipo === "multiclasse";
  if (r.clf) {
    r.classes = [...a.freq.entries()].sort((x, y) => y[1] - x[1]);
    const total = rot;
    r.k = r.classes.length;
    r.min = r.classes[r.k - 1][1] / total; r.max = r.classes[0][1] / total;
    if (r.tipo === "binaria") {
      const [c1, c2] = r.classes;
      const sem = r.classes.find(([s]) => POSITIVOS.has(s.toLowerCase()));
      r.pos = r.min >= 0.4 && sem ? sem[0] : c2[0];
      r.taxaPos = a.freq.get(r.pos) / total;
      r.desb = r.min < 0.01 ? "extremo" : r.min <= 0.10 ? "moderado" : "leve";
      r.nPos = Math.round(r.min * total);
    } else {
      r.desigual = r.max / r.min > 1.5;
      r.desb = r.min < 0.01 ? "extremo" : r.min <= 0.10 ? "moderado" : "leve";
    }
  } else {
    const ys = []; for (let i = 0; i < a.num.length; i++) if (a.num[i] === a.num[i]) ys.push(a.num[i]);
    ys.sort((x, y) => x - y);
    r.ys = ys;
  }
  if (a.pMiss > 0) {
    if (a.pMiss > 0.5 && rot >= 30 && r.clf) {
      r.semi = true;
      r.avisos.push("[[medio]] " + fmtPct(a.pMiss) + " das linhas não têm rótulo: há espaço para aprendizagem semissupervisionada (§3.12 da skill), sempre contra o baseline treinado só com os " + fmtInt(rot) + " rotulados");
    } else r.avisos.push("[[medio]] " + fmtInt(a.nMiss) + " linhas (" + fmtPct(a.pMiss) + ") sem valor no alvo: ficam fora do treino e da avaliação");
  }
  vazamentos(P, r);
  return r;
}

function aucSeparacao(x, y, idx){
  const pares = [];
  for (const i of idx) { const xi = x[i], yi = y[i]; if (xi === xi && yi >= 0) pares.push([xi, yi]); }
  let nP = 0; for (const p of pares) nP += p[1];
  const nN = pares.length - nP;
  if (nP < 10 || nN < 10) return null;
  pares.sort((a, b) => a[0] - b[0]);
  let somaRank = 0;
  for (let i = 0; i < pares.length;) {
    let j = i; while (j + 1 < pares.length && pares[j + 1][0] === pares[i][0]) j++;
    const rk = (i + j) / 2 + 1;
    for (let k = i; k <= j; k++) if (pares[k][1] === 1) somaRank += rk;
    i = j + 1;
  }
  const auc = (somaRank - nP * (nP + 1) / 2) / (nP * nN);
  return Math.max(auc, 1 - auc);
}

function vazamentos(P, r){
  const a = r.col, idx = P.idx;
  r.vaz = []; r.suspeitosNome = []; r.ausInfo = [];
  const tokensAlvo = a.nomeN.split(/[^a-z0-9]+/).filter(t => t.length >= 4);
  let y = null;
  if (r.tipo === "binaria") { y = new Int8Array(a.n).fill(-1); for (let i = 0; i < a.n; i++) if (a.v[i] !== null) y[i] = a.v[i] === r.pos ? 1 : 0; }
  for (const c of P.cols) {
    if (c === a || ["vazia", "constante"].includes(c.tipo)) continue;
    if (RE_VAZ_NOME.test(c.nomeN) || tokensAlvo.some(t => c.nomeN.includes(t))) r.suspeitosNome.push(c.nome);
    if (r.tipo === "binaria") {
      // valor numérico que separa o alvo sozinho
      if (c.num && (c.tipo === "numerico" || c.tipo === "binario")) {
        const auc = aucSeparacao(c.num, y, idx);
        if (auc !== null && auc >= 0.98) { r.vaz.push({col: c.nome, motivo: "sozinha separa as classes (AUC " + fmtNum(auc) + ")"}); continue; }
      }
      // presença/ausência do valor que coincide com o alvo
      if (c.nMiss >= 10 && c.pMiss < 0.99) {
        let mP = 0, mN = 0, oP = 0, oN = 0;
        for (let i = 0; i < a.n; i++) { if (y[i] < 0) continue; if (c.v[i] === null) { if (y[i]) mP++; else mN++; } else { if (y[i]) oP++; else oN++; } }
        const nPos = mP + oP, nNeg = mN + oN;
        const presPos = nPos ? oP / nPos : 0, presNeg = nNeg ? oN / nNeg : 0;
        if (nPos >= 10 && nNeg >= 10 && Math.abs(presPos - presNeg) >= 0.97) {
          r.vaz.push({col: c.nome, motivo: "o valor só está preenchido em uma das classes (preenchido em " + fmtPct(presPos) + " dos positivos e " + fmtPct(presNeg) + " dos negativos)"}); continue;
        }
        const tm = (mP + mN) ? mP / (mP + mN) : 0, to = (oP + oN) ? oP / (oP + oN) : 0;
        if (mP + mN >= 30 && c.pMiss >= 0.01 && Math.abs(tm - to) >= 0.05 && (tm >= 2 * to || to >= 2 * tm))
          r.ausInfo.push({col: c.nome, tm, to});
      }
      // categoria que determina o alvo
      if (["categorico", "binario"].includes(c.tipo) && !c.num && c.distinct <= 0.5 * c.nn) {
        if (purezaCat(c, a, idx) >= 0.99 && r.min >= 0.01) r.vaz.push({col: c.nome, motivo: "cada categoria corresponde a uma única classe em ≥ 99% das linhas"});
      }
    } else if (r.tipo === "multiclasse") {
      if (["categorico", "binario"].includes(c.tipo) && !c.num && c.distinct <= 0.5 * c.nn) {
        const pz = purezaCat(c, a, idx);
        if (pz >= 0.99 && pz - r.max >= 0.05) r.vaz.push({col: c.nome, motivo: "cada categoria corresponde a uma única classe em ≥ 99% das linhas"});
      }
    } else if (c.num && c.tipo === "numerico") {
      const cor = pearson(c.num, a.num, idx);
      if (Math.abs(cor) >= 0.98) r.vaz.push({col: c.nome, motivo: "correlação de " + fmtNum(cor) + " com o alvo"});
    }
  }
  const nomesVaz = new Set(r.vaz.map(x => x.col));
  r.suspeitosNome = r.suspeitosNome.filter(n => !nomesVaz.has(n));
}

function purezaCat(c, a, idx){
  const tab = new Map(); let m = 0;
  for (const i of idx) {
    if (a.v[i] === null) continue;
    const k = c.v[i] === null ? "\u0000" : c.v[i];
    let t = tab.get(k); if (!t) { t = new Map(); tab.set(k, t); }
    t.set(a.v[i], (t.get(a.v[i]) || 0) + 1); m++;
  }
  if (tab.size < 2 || m < 30) return 0;
  let soma = 0; tab.forEach(t => { let mx = 0; t.forEach(v => { if (v > mx) mx = v; }); soma += mx; });
  return soma / m;
}

function conflitosRotulo(P, a){
  let conf = 0; const mapa = new Map();
  for (let i = 0; i < P.n; i++) {
    if (a.v[i] === null) continue;
    let ch = ""; for (const c of P.cols) if (c !== a) ch += (c.v[i] === null ? "\u0000" : c.v[i]) + "\u0001";
    const ant = mapa.get(ch);
    if (ant === undefined) mapa.set(ch, a.v[i]); else if (ant !== a.v[i]) conf++;
  }
  return conf;
}

/* ===================== catálogo de modelos ===================== */
const CAT = {
  logC:   {nome: "LogisticRegression", nivel: 1, fw: "scikit-learn", card: "logistic",
           vant: "interpretável (coeficientes em log-odds), barata, latência mínima", lim: "fronteira linear; interações só com features explícitas",
           hp: "`C` em escala log (1e-3 a 1e2); `l1_ratio` de 0 a 1 para L1/Elastic Net (`penalty` está depreciado desde a 1.8); `class_weight`"},
  ridge:  {nome: "Ridge", nivel: 1, fw: "scikit-learn", card: "ridge",
           vant: "estável sob multicolinearidade; coeficientes interpretáveis", lim: "relação linear; sensível a outliers no alvo", hp: "`alpha` em escala log (1e-3 a 1e3)"},
  enet:   {nome: "Elastic Net (ElasticNet ou LogisticRegression com `l1_ratio`)", nivel: 1, fw: "scikit-learn", card: "elasticnet",
           vant: "seleciona variáveis com estabilidade quando há muitas features", lim: "linear; exige escala", hp: "`alpha`/`C` em grade explícita (`n_alphas` foi removido na 1.9) e `l1_ratio` de 0,1 a 0,9"},
  poisson:{nome: "PoissonRegressor", nivel: 1, fw: "scikit-learn", card: null,
           vant: "perda de Poisson para contagens; previsões sempre positivas", lim: "supõe média ≈ variância; com superdispersão use `TweedieRegressor`", hp: "`alpha` (L2) e `max_iter`"},
  sgd:    {nome: "SGDClassifier / SGDRegressor", nivel: 1, fw: "scikit-learn", card: null,
           vant: "treina em milhões de linhas com memória constante (`partial_fit`)", lim: "sensível à escala e à taxa de aprendizado", hp: "`alpha` em escala log, `loss=\"log_loss\"` para probabilidades, `learning_rate`"},
  nb:     {nome: "ComplementNB sobre TF-IDF", nivel: 1, fw: "scikit-learn", card: "naive-bayes",
           vant: "muito rápido; baseline clássico de texto", lim: "independência condicional; probabilidades mal calibradas", hp: "`alpha` de 0,01 a 1"},
  logTxt: {nome: "TF-IDF + modelo linear (LogisticRegression ou Ridge)", nivel: 1, fw: "scikit-learn", card: "logistic",
           vant: "interpretável por termo; forte em texto esparso", lim: "ignora a ordem das palavras além dos n-gramas", hp: "`C`/`alpha` em escala log; `TfidfVectorizer(ngram_range=(1, 2), min_df=2 a 5)`"},
  linsvc: {nome: "LinearSVC sobre TF-IDF", nivel: 3, fw: "scikit-learn", card: "svm",
           vant: "forte em texto de alta dimensão", lim: "sem probabilidade nativa (use `CalibratedClassifierCV`)", hp: "`C` de 0,01 a 10 (log)"},
  tree:   {nome: "DecisionTree rasa (profundidade ≤ 4)", nivel: 2, fw: "scikit-learn", card: "decision-tree",
           vant: "regras legíveis por quem decide", lim: "instável; perde para ensembles", hp: "`max_depth` 2–4, `min_samples_leaf` 20–200, `ccp_alpha`"},
  rf:     {nome: "RandomForest", nivel: 2, fw: "scikit-learn", card: "random-forest",
           vant: "não linearidade e interações com pouco tuning; OOB score", lim: "não é imune a overfitting; modelo pesado; no scikit-learn exige encoding e imputação", hp: "`n_estimators` 300–800, `max_depth` None ou 8–30, `min_samples_leaf` 1–20, `max_features` `sqrt` ou 0,3–0,8"},
  hgb:    {nome: "HistGradientBoosting", nivel: 3, fw: "scikit-learn", card: "histgb",
           vant: "NaN e categóricas nativos; rápido; sem dependência extra", lim: "categóricas nativas até 255 níveis; exige early stopping e tuning", hp: "`learning_rate` 0,02–0,2 (log), `max_leaf_nodes` 15–127, `min_samples_leaf` 20–200, `l2_regularization` 0–10, `max_iter` até 1.000 com `early_stopping=True`"},
  lgbm:   {nome: "LightGBM", nivel: 3, fw: "LightGBM", card: "lightgbm",
           vant: "o mais rápido da categoria; categóricas e NaN nativos; escala para milhões de linhas", lim: "overfitta com `num_leaves` alto em bases pequenas; exige early stopping", hp: "`num_leaves` 31–127, `min_child_samples` 20–500, `learning_rate` 0,02–0,1 (log), `feature_fraction` 0,6–1,0, `lambda_l2` 0–10, `n_estimators` até 5.000 com `callbacks=[lgb.early_stopping(50)]`"},
  xgb:    {nome: "XGBoost", nivel: 3, fw: "XGBoost", card: "xgboost",
           vant: "referência em tabular; regularização explícita; `enable_categorical=True`", lim: "mais hiperparâmetros; mais lento que LightGBM em bases grandes", hp: "`max_depth` 3–10, `learning_rate` 0,02–0,1, `subsample` e `colsample_bytree` 0,6–1,0, `reg_lambda` 0–10, `early_stopping_rounds=50` no construtor"},
  cat:    {nome: "CatBoost", nivel: 3, fw: "CatBoost", card: "catboost",
           vant: "codificação ordenada de categóricas de alta cardinalidade (menos vazamento no encoding); bons defaults", lim: "treino mais lento; modelo maior", hp: "`depth` 4–10, `learning_rate` 0,02–0,1, `l2_leaf_reg` 1–10, `iterations` até 3.000 com `early_stopping_rounds=50` e `eval_set` como tupla"},
  cnn:    {nome: "CNN com transfer learning", nivel: 4, fw: "Keras/TensorFlow ou PyTorch", card: "mlp",
           vant: "o sinal está nos pixels; modelos pré-treinados encurtam o caminho", lim: "exige GPU, augmentation e mais manutenção", hp: "taxa de aprendizado da cabeça e do ajuste fino, camadas descongeladas, augmentation"},
  kmeans: {nome: "K-Means", fw: "scikit-learn", card: "kmeans", vant: "simples, rápido, centróides interpretáveis", lim: "supõe grupos esféricos; exige escolher k e escalar", hp: "`n_clusters` 2–10 (silhouette), `n_init=10`"},
  gmm:    {nome: "Gaussian Mixture", fw: "scikit-learn", card: "gmm", vant: "fronteiras suaves e probabilidade de pertencimento", lim: "supõe gaussianas; sensível à inicialização", hp: "`n_components` por BIC, `covariance_type`"},
  hdbscan:{nome: "HDBSCAN / DBSCAN", fw: "scikit-learn", card: "dbscan", vant: "forma arbitrária e rótulo de ruído", lim: "sensível a escala e densidade variável (DBSCAN)", hp: "`min_cluster_size` (HDBSCAN), `eps` e `min_samples` (DBSCAN)"},
  hier:   {nome: "Clustering hierárquico", fw: "scikit-learn", card: "hierarchical", vant: "dendrograma mostra a estrutura em vários níveis", lim: "memória O(n²): só bases pequenas", hp: "`linkage` (ward, average), `n_clusters` ou `distance_threshold`"},
  pca:    {nome: "PCA", fw: "scikit-learn", card: "pca", vant: "compressão linear com variância explicada mensurável", lim: "só relações lineares; componentes pouco interpretáveis", hp: "`n_components` pela variância acumulada (ex.: 0,95)"},
  tsvd:   {nome: "TruncatedSVD", fw: "scikit-learn", card: "pca", vant: "funciona em matriz esparsa (texto, one-hot)", lim: "não centraliza os dados", hp: "`n_components` 50–300"},
  iforest:{nome: "IsolationForest", fw: "scikit-learn", card: "isolation-forest", vant: "rápido, sem escala, bom em alta dimensão", lim: "anomalias locais escapam", hp: "`n_estimators` 200–500, `contamination` (\"auto\" ou taxa esperada), `max_samples`"},
  lof:    {nome: "Local Outlier Factor", fw: "scikit-learn", card: "lof", vant: "pega anomalias locais (densidade relativa)", lim: "custo alto em bases grandes; exige escala", hp: "`n_neighbors` 10–50, `novelty=True` para pontuar dados novos"},
  zscore: {nome: "Z-score robusto (MAD) por variável", fw: "NumPy/pandas", card: "zscore", vant: "transparente; serve de baseline", lim: "olha uma variável por vez", hp: "limiar 3,5"},
  popular:{nome: "Popularidade recente", fw: "pandas", card: null, vant: "baseline obrigatório de recomendação", lim: "não personaliza", hp: "janela de recência"},
  cfknn:  {nome: "Filtragem colaborativa por vizinhança (item-based)", fw: "scikit-learn / NumPy", card: "cf-knn", vant: "explicável (“quem viu X viu Y”)", lim: "cold start; esparsidade", hp: "número de vizinhos, similaridade (cosseno)"},
  mf:     {nome: "Fatoração de matrizes (ALS implícito)", fw: "implicit ou TensorFlow (§16.6)", card: "mf", vant: "captura gosto latente; escala bem", lim: "cold start; pouco interpretável", hp: "fatores 32–256, regularização, peso de confiança"},
  content:{nome: "Baseada em conteúdo / híbrida", fw: "scikit-learn", card: "content-based", vant: "resolve itens e usuários novos", lim: "depende de bons atributos de item", hp: "representação dos itens, peso do híbrido"},
  contag: {nome: "Contagem dos pares mais frequentes", fw: "pandas", card: null, vant: "baseline transparente", lim: "não mede associação além do acaso", hp: "—"},
  fpg:    {nome: "FP-Growth (Apriori em bases pequenas)", fw: "mlxtend", card: "fpgrowth", vant: "mesmo resultado do Apriori, muito mais rápido", lim: "lift não é causalidade", hp: "`min_support`, filtro por lift > 1"},
  self:   {nome: "Self-Training", fw: "scikit-learn", card: "self-training", vant: "aproveita não rotulados com pouco código", lim: "propaga erros se o classificador for ruim", hp: "`threshold` alto (ex.: 0,9)"},
  spread: {nome: "Label Spreading", fw: "scikit-learn", card: "label-spreading", vant: "usa a vizinhança dos dados", lim: "grafo RBF usa memória O(n²)", hp: "`kernel` (rbf ou knn), `alpha`"}
};

/* ===================== motor de regras ===================== */
const OBJETIVOS = {
  prever: "Prever uma coluna (supervisionado)",
  agrupar: "Agrupar linhas parecidas (clustering)",
  anomalias: "Encontrar registros raros (anomalias)",
  comprimir: "Comprimir ou visualizar (redução de dimensão)",
  recomendar: "Recomendar itens a usuários",
  associar: "Itens que ocorrem juntos (associação)"
};

function contexto(P, ctx){
  const C = {P, ctx};
  C.n = P.n;
  C.tam = P.n < 1000 ? "pequeno" : P.n < 100000 ? "médio" : P.n < 1000000 ? "grande" : "muito grande";
  C.alvo = ctx.objetivo === "prever" ? P.cols.find(c => c.nome === ctx.alvo) : null;
  C.tempo = ctx.tempo ? P.cols.find(c => c.nome === ctx.tempo) : null;
  C.ent = ctx.entidade ? P.cols.find(c => c.nome === ctx.entidade) : null;
  C.A = C.alvo ? analisarAlvo(P, C.alvo) : null;
  const vazSet = new Set(C.A && C.A.vaz ? C.A.vaz.map(v => v.col) : []);
  C.excluir = {};
  const feats = [];
  for (const c of P.cols) {
    if (c === C.alvo) continue;
    let motivo = null;
    if (c.tipo === "vazia" || c.tipo === "constante") motivo = "constante ou vazia";
    else if (c.tipo === "id") motivo = "identificador";
    else if (c === C.ent) motivo = "entidade (usada para agrupar a validação)";
    else if (c.tipo === "data") motivo = "data (derive componentes antes de usar)";
    else if (vazSet.has(c.nome)) motivo = "suspeita de vazamento";
    else if (c.tipo === "aninhado") motivo = "estrutura aninhada (achate antes)";
    else if (c.tipo === "imagem" || c.tipo === "audio") motivo = "caminho de arquivo (" + c.tipo + ")";
    else if (c.pMiss > 0.95) motivo = "mais de 95% ausente";
    if (motivo) { C.excluir[c.nome] = motivo; continue; }
    feats.push(c);
  }
  C.feats = feats;
  C.num = feats.filter(c => c.tipo === "numerico" || (c.tipo === "binario" && c.num));
  C.catBaixa = feats.filter(c => (c.tipo === "categorico" && !c.alta) || (c.tipo === "binario" && !c.num));
  C.catAlta = feats.filter(c => c.tipo === "categorico" && c.alta);
  C.texto = feats.filter(c => c.tipo === "texto");
  C.imagem = P.cols.filter(c => c.tipo === "imagem" || c.tipo === "audio");
  C.textoPrincipal = C.texto.length > 0 && (C.num.length + C.catBaixa.length + C.catAlta.length) <= 2;
  C.pEnc = C.num.length + C.catBaixa.reduce((s, c) => s + Math.max(1, Math.min(c.distinct, 50) - 1), 0) + C.catAlta.length;
  C.pnAlto = C.pEnc / Math.max(1, P.n) > 0.1 || C.pEnc > 1000;
  C.pn = C.pEnc / Math.max(1, P.n);
  C.outl = C.num.filter(c => c.outl > 0.01);
  C.multicol = P.pares.filter(([a, b]) => !(C.alvo && (a === C.alvo.nome || b === C.alvo.nome)) && !C.excluir[a] && !C.excluir[b]);
  C.regulado = ctx.interp === "obrigatoria";
  C.tempoReal = ctx.latencia === "real";
  C.fmt = detectarFormato(P);
  return C;
}

function alertas(C){
  const P = C.P, A = C.A, L = [];
  const add = (sev, txt) => L.push("[[" + sev + "]] " + txt);
  const m = P.meta;
  if (m.truncado) add("medio", "o arquivo passa de " + fmtInt(MAX_LINHAS) + " linhas: só as primeiras foram analisadas. Se o arquivo estiver ordenado (por data, por classe), o perfil pode não representar o todo");
  if (m.irregulares) add("medio", pl(m.irregulares, "linha", "linhas") + " com número de campos diferente do cabeçalho — confira aspas e separador (" + (m.sep === "\t" ? "tabulação" : "“" + m.sep + "”") + ")");
  if (m.abas && m.abas.length > 1) add("info", "a planilha tem " + m.abas.length + " abas; foi analisada só a primeira (“" + m.abas[0] + "”)");
  if (m.encoding === "cp1252") add("info", "o arquivo não está em UTF-8; foi lido como Windows-1252 (comum em exportações do Excel no Brasil)");
  if (A && A.vaz) A.vaz.forEach(v => add("alto", "**possível vazamento** em " + cn(v.col) + ": " + v.motivo + ". Desempenho assim é presunção de leakage até prova em contrário (§3.6) — confirme se a coluna existe no momento da previsão; ela foi retirada do código abaixo"));
  if (A && A.suspeitosNome.length) add("medio", "verifique se estas colunas existem **antes** do evento que se quer prever (o nome sugere informação posterior ou ligada ao alvo): " + lista(A.suspeitosNome));
  if (A) A.avisos.forEach(x => L.push(x));
  if (A && A.clf && A.desb === "extremo") add("alto", "classe minoritária com " + fmtPct(A.min, 2) + " das linhas: desbalanceamento **extremo** — accuracy é proibida como métrica principal (§3.4)");
  else if (A && A.clf && A.desb === "moderado") add("medio", "classe minoritária com " + fmtPct(A.min) + " das linhas: desbalanceamento **moderado** (§3.4)");
  if (A && A.tipo === "binaria" && A.nPos < 50) add("alto", "só " + fmtInt(A.nPos) + " exemplos da classe minoritária: cada fold de validação terá cerca de " + fmtInt(Math.round(A.nPos / 5)) + " — a métrica vai oscilar muito entre folds");
  const sup = C.ctx.objetivo === "prever";
  if (P.dup) add("medio", pl(P.dup, "linha duplicada", "linhas duplicadas") + (sup ? ": deduplique **antes** do split, senão a mesma linha cai em treino e teste (§3.4)"
    : " — repetições pesam em dobro em distâncias, contagens e scores; deduplique, salvo se forem eventos legítimos repetidos"));
  if (A && C.conflitos) add("medio", pl(C.conflitos, "linha repete", "linhas repetem") + " todas as features com alvo diferente: rótulo ruidoso ou falta uma feature que explique a diferença");
  const ids = P.cols.filter(c => c.tipo === "id");
  if (ids.length) add("info", "identificadores fora das features: " + lista(ids.map(c => c.nome)) + " (um valor por linha não generaliza)");
  const const_ = P.cols.filter(c => c.tipo === "constante" || c.tipo === "vazia");
  if (const_.length) add("info", "colunas constantes ou vazias, sem informação: " + lista(const_.map(c => c.nome)));
  const quase = P.cols.filter(c => !["constante", "vazia", "id"].includes(c.tipo) && c.top.length && c.top[0][1] / Math.max(1, c.nn) >= 0.99 && c.nn > 100);
  if (quase.length) add("info", "colunas quase constantes (≥ 99% com o mesmo valor): " + lista(quase.map(c => c.nome)));
  const severos = P.cols.filter(c => c.pMiss > 0.4 && c.tipo !== "vazia" && c !== C.alvo);
  if (severos.length) add("medio", "ausência severa (> 40%) em " + lista(severos.map(c => c.nome + " " + fmtPct(c.pMiss, 0))) + ": considere descartar ou usar modelo com NaN nativo e documentar (§3.4)");
  if (A && A.ausInfo.length) add("medio", "ausência provavelmente **informativa** (a taxa da classe positiva muda quando o valor falta): " + lista(A.ausInfo.map(x => x.col + " (" + fmtPct(x.tm, 0) + " × " + fmtPct(x.to, 0) + ")")) + " — crie indicador de ausência em vez de imputar cegamente");
  if (C.catAlta.length) add("info", "categóricas de alta cardinalidade (> 50 níveis): " + lista(C.catAlta.map(c => c.nome + " " + fmtInt(c.distinct))) + " — nunca One-Hot puro (§3.3)");
  if (C.multicol.length) add("info", "pares numéricos com |r| ≥ 0,9 (multicolinearidade): " + C.multicol.slice(0, 5).map(([a, b, r]) => cn(a) + "–" + cn(b) + " " + fmtNum(r)).join("; ") + (sup ? " — não interprete coeficientes de OLS nessas variáveis" : " — variáveis redundantes pesam em dobro nas distâncias; considere PCA ou manter uma de cada par"));
  if (C.outl.length) add("info", "outliers relevantes (> 1% dos valores com |z robusto| > 3,5) em " + lista(C.outl.map(c => c.nome)) + " — investigue a origem antes de remover");
  const sujas = P.cols.filter(c => c.sujeira);
  if (sujas.length) add("medio", "colunas quase numéricas com valores de texto no meio: " + sujas.map(c => cn(c.nome) + " (ex.: " + c.sujeira.ruins.slice(0, 3).map(x => "“" + x + "”").join(", ") + ")").join("; ") + " — limpe ou converta com `pd.to_numeric(errors=\"coerce\")`");
  const ruins = P.cols.filter(c => c.num && c.ruins && c.ruins.length && c.fracNum < 1);
  if (ruins.length) add("info", "valores não numéricos tratados como ausentes em " + ruins.map(c => cn(c.nome) + " (ex.: " + c.ruins.slice(0, 2).map(x => "“" + x + "”").join(", ") + ")").join("; "));
  const pii = P.cols.filter(c => c.pii);
  if (pii.length) add("medio", "possíveis **dados pessoais**: " + lista(pii.map(c => c.nome)) + " — não os use como feature e avalie anonimização e base legal antes de compartilhar o dataset");
  const datas = P.cols.filter(c => c.tipo === "data");
  if (datas.length && !C.tempo && C.ctx.objetivo === "prever") add("medio", "há coluna de data (" + lista(datas.map(c => c.nome)) + ") mas nenhuma foi marcada como ordem temporal: se a previsão é sobre o futuro, K-Fold embaralhado usa o futuro para prever o passado (§3.7)");
  if (C.tempo && C.tempo.ordenada) add("info", "as linhas já estão em ordem de " + cn(C.tempo.nome) + ": embaralhar no split misturaria passado e futuro");
  if (C.texto.length) add("info", "texto livre em " + lista(C.texto.map(c => c.nome)) + ": vira TF-IDF dentro do pipeline; Transformers só com volume e infraestrutura (§3.3)");
  if (C.imagem.length) add("info", "a tabela aponta para arquivos (" + lista(C.imagem.map(c => c.nome)) + "): o sinal está nos arquivos, que não foram enviados — CNN com transfer learning (§3.1)");
  if (P.cols.some(c => c.geo)) add("info", "latitude/longitude detectadas: use distâncias como features; clustering geográfico com DBSCAN e métrica haversine (§3.3)");
  if (C.fmt.interacoes && C.ctx.objetivo !== "recomendar") add("info", "o arquivo tem formato de interações usuário–item (" + cn(C.fmt.user) + " × " + cn(C.fmt.item) + "): se o objetivo é ordenar itens por usuário, escolha “Recomendar itens” no objetivo (§3.10)");
  if (C.fmt.transacional && C.ctx.objetivo !== "associar") add("info", "o arquivo parece transacional (cestas de itens): se o objetivo é descobrir itens comprados juntos, escolha “Itens que ocorrem juntos” (§3.13)");
  if (C.tam === "pequeno" && sup) add("medio", "só " + fmtInt(P.n) + " linhas: Deep Learning proibido sem justificativa escrita; use validação repetida (§3.2)");
  if (C.pnAlto && sup) add("medio", "alta dimensionalidade: cerca de " + fmtInt(C.pEnc) + " colunas após o encoding para " + fmtInt(P.n) + " linhas (p/n ≈ " + fmtNum(C.pn) + ") — regularização forte, KNN e distâncias degradam (§3.2)");
  return L;
}

function escolherCandidatos(C){
  const A = C.A, L = [];
  const add = (k, porque) => { if (!L.some(x => x.k === k)) L.push({k, porque}); };
  const clf = A.clf, cont = A.tipo === "contagem";
  const lin = clf ? "logC" : cont ? "poisson" : "ridge";
  if (C.imagem.length && (C.num.length + C.catBaixa.length + C.catAlta.length) <= 2) {
    add("cnn", "o sinal está em imagem/áudio (§3.1); Deep Learning autorizado pela condição 1 da §4.3");
    add(lin, "modelo linear sobre embeddings de um pré-treinado congelado — baseline obrigatório (§3.1)");
    return L;
  }
  if (C.textoPrincipal) {
    add("logTxt", "texto livre é a entrada principal → TF-IDF + modelo linear (§3.1, §3.3)");
    if (clf) { add("linsvc", "texto esparso de alta dimensão → linear forte (§3.2)"); add("nb", "baseline clássico de texto (§3.1)"); }
    return L;
  }
  const boostCont = cont ? " com perda de Poisson (`loss=\"poisson\"` / `objective=\"poisson\"`)" : "";
  if (C.regulado) {
    add(clf ? "logC" : lin, "explicação exigida por regulação → Nível 1 como modelo final (§3.5)");
    add("tree", "árvore rasa como alternativa legível (§3.5)");
    add(C.catAlta.length ? "cat" : "hgb", "só como desafiante, com SHAP, documentação e aprovação (§3.5)" + boostCont);
    return L;
  }
  if (C.pnAlto) {
    add("enet", "alta dimensionalidade (p/n > 0,1 ou p > 1.000) → linear regularizado L1/Elastic Net (§3.2)");
    if (clf && C.tam === "pequeno") add("nb", "n < 1.000 com p > n/10 → Naive Bayes como alternativa (§3.2)");
    add(lin, "piso de Nível 1 com L2 (§2, passo 7)");
    if (C.tam !== "pequeno") add("hgb", "desafiante de Nível 3; só sobe se superar a regra de promoção (§4.2)" + boostCont);
    return L;
  }
  if (C.tam === "pequeno") {
    add(lin, "n < 1.000 → Nível 1 com regularização forte (§3.2)");
    if (!C.tempoReal) add("rf", "Nível 2 com capacidade controlada (`min_samples_leaf` alto) para testar não linearidade");
    add("hgb", "desafiante de Nível 3; em base pequena só é adotado se vencer pela regra de promoção (§4.2)" + boostCont);
    return L;
  }
  if (C.tam === "muito grande") {
    add("lgbm", "n ≥ 1.000.000 tabular → LightGBM primeiro (§3.2)" + boostCont);
    add("hgb", "alternativa sem dependência extra, com NaN e categóricas nativos" + boostCont);
    add("sgd", "linear com `SGDClassifier`/`SGDRegressor` como candidato de nível inferior (§3.2)");
    return L;
  }
  if (C.tam === "grande") {
    add("lgbm", "100 mil ≤ n < 1 milhão → LightGBM/HistGB; amostre para prototipar (§3.2)" + boostCont);
    add(C.catAlta.length ? "cat" : "hgb", C.catAlta.length ? "categóricas de alta cardinalidade → codificação ordenada (§3.3)" : "alternativa do próprio scikit-learn (§3.2)" + boostCont);
    add(lin, "candidato de nível inferior obrigatório (§2, passo 8)");
    return L;
  }
  // médio
  if (C.catAlta.length) {
    add("cat", "categóricas de alta cardinalidade (" + lista(C.catAlta.map(c => c.nome), 3) + ") → CatBoost (§3.3)" + boostCont);
    add("lgbm", "categóricas nativas e NaN nativo; mais rápido (§3.3)" + boostCont);
  } else if (C.catBaixa.length) {
    add("hgb", "mistura de numéricas e categóricas → HistGradientBoosting (§3.3)" + boostCont);
    add("cat", "mistura de numéricas e categóricas com pouco pré-processamento (§3.3)" + boostCont);
  } else {
    add("lgbm", "tabular numérico de porte médio → boosting é o candidato natural (§3.2)" + boostCont);
    add("xgb", "alternativa de boosting com regularização explícita (§3.1)" + boostCont);
  }
  if (!C.tempoReal && !C.catAlta.length) add("rf", "Nível 2: não linearidade com pouco tuning, para provar que o boosting se paga (§2, passo 8)");
  add(C.multicol.length && !clf ? "ridge" : lin, "candidato de Nível 1 obrigatório — o piso que justifica a complexidade (§2, passo 8)");
  return L;
}

function metricas(C){
  const A = C.A, k = C.ctx.custo;
  if (A.clf) {
    if (A.tipo === "multiclasse") {
      const prob = k === "prob";
      return {
        principal: prob ? "**Log Loss**" : A.desigual ? "**F1 macro**" : "**F1 macro** (accuracy aceitável: classes equilibradas)",
        porque: prob ? "a probabilidade entra na decisão (§3.8)" : A.desigual ? "multiclasse com classes desiguais (maior/menor = " + fmtNum(A.max / A.min) + "×) (§3.8)" : "classes equilibradas e custos simétricos (§3.8)",
        sec: ["F1 por classe — mostra quais classes o modelo sacrifica", "matriz de confusão — onde estão as trocas", "accuracy — só como referência, nunca isolada"],
        sk: prob ? {log_loss: "neg_log_loss", f1_macro: "f1_macro"} : {f1_macro: "f1_macro", acuracia: "accuracy"}
      };
    }
    if (k === "prob") return {principal: "**Log Loss** (ou Brier)", porque: "a probabilidade entra em preço, limite ou corte financeiro (§3.8) — calibre com `CalibratedClassifierCV` (§3.5)",
      sec: ["curva de confiabilidade — calibração", "PR-AUC — ordenação da classe positiva"], sk: {log_loss: "neg_log_loss", brier: "neg_brier_score", pr_auc: "average_precision"}};
    if (A.min < 0.10) {
      const extra = k === "fn" ? "; opere o threshold pelo recall com precision mínima contratada" : k === "fp" ? "; opere o threshold pela precision com recall mínimo contratado" : "";
      return {principal: "**PR-AUC** (`average_precision`)", porque: "classe positiva rara (" + fmtPct(A.min, 2) + ") — o custo está em achar positivos sem inundar de falsos alarmes (§3.8)" + extra,
        sec: ["precision@k (k = capacidade de análise) — o que a operação realmente vê", "recall no threshold operacional", "ROC-AUC — só como referência comparativa", "matriz de confusão no threshold escolhido"],
        sk: {pr_auc: "average_precision", roc_auc: "roc_auc", recall: "recall", precision: "precision"}};
    }
    if (k === "fn") return {principal: "**Recall** com precision mínima contratada", porque: "deixar passar um positivo custa muito mais (§3.8)", sec: ["PR-AUC", "F1"], sk: {recall: "recall", precision: "precision", pr_auc: "average_precision"}};
    if (k === "fp") return {principal: "**Precision** com recall mínimo contratado", porque: "alarme falso custa muito mais (§3.8)", sec: ["PR-AUC", "F1"], sk: {precision: "precision", recall: "recall", pr_auc: "average_precision"}};
    return {principal: "**F1**" + (A.min >= 0.4 ? " (accuracy aceitável: classes equilibradas)" : ""),
      porque: (k === "simetrico" ? "custos simétricos" : "custo do erro não informado — F1 é o padrão para custos simétricos; defina o custo acima") + " (§3.8)",
      sec: ["ROC-AUC — ordenação independente do threshold", "Log Loss — qualidade das probabilidades", "matriz de confusão"], sk: {f1: "f1", roc_auc: "roc_auc", log_loss: "neg_log_loss"}};
  }
  const skReg = {rmse: "neg_root_mean_squared_error", mae: "neg_mean_absolute_error", r2: "r2"};
  if (A.tipo === "contagem") skReg.deviance_poisson = "neg_mean_poisson_deviance";
  const secReg = ["R² — fração explicada, nunca como número único (§3.8)", "resíduos por faixa do alvo — onde o modelo erra"];
  if (A.tipo === "contagem") secReg.unshift("deviance de Poisson — adequação ao modelo de contagem");
  if (k === "grandes") return {principal: "**RMSE**", porque: "erros grandes custam desproporcionalmente mais (§3.8)", sec: ["MAE"].concat(secReg), sk: skReg};
  if (k === "linear") return {principal: "**MAE**", porque: "custo proporcional ao erro (§3.8)", sec: ["RMSE", "MAPE se o alvo nunca for zero"].concat(secReg), sk: skReg};
  if (k === "escala") return {principal: "**WAPE** (ou MAPE)", porque: "séries com escalas heterogêneas (§3.8); MAPE explode com alvo perto de zero", sec: ["MAE por série"].concat(secReg), sk: skReg};
  return {principal: "**RMSE ou MAE** — defina o custo do erro acima", porque: "RMSE se erros grandes custam desproporcionalmente mais; MAE se o custo é linear (§3.8). A escolha não sai do arquivo",
    sec: ["a outra das duas", "MAPE/WAPE se houver séries de escalas diferentes"].concat(secReg), sk: skReg};
}

function validacao(C){
  const A = C.A, clf = A && A.clf;
  if (C.tempo) return {txt: "`TimeSeriesSplit(n_splits=5)` com as linhas ordenadas por " + cn(C.tempo.nome) + "; acrescente `gap` se o rótulo demora a amadurecer",
    porque: "há ordem temporal relevante (§3.7): o teste precisa estar depois do treino", cod: "TimeSeriesSplit(n_splits=5)", imp: "TimeSeriesSplit"};
  if (C.ent) return {txt: (clf ? "`StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)`" : "`GroupKFold(n_splits=5)`") + " com grupos = " + cn(C.ent.nome),
    porque: "a mesma entidade aparece em várias linhas (" + fmtInt(C.ent.distinct) + " entidades para " + fmtInt(C.ent.nn) + " linhas) — sem grupo, o modelo é avaliado em entidades que já viu (§3.7)",
    cod: clf ? "StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)" : "GroupKFold(n_splits=5)", imp: clf ? "StratifiedGroupKFold" : "GroupKFold", grupos: true};
  if (clf && C.n < 1000) return {txt: "`RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)`", porque: "classificação com n < 1.000: repetir reduz a variância da estimativa (§3.7)",
    cod: "RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)", imp: "RepeatedStratifiedKFold"};
  if (clf) return {txt: "`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`", porque: "sem tempo nem entidade repetida; estratificar preserva a proporção das classes em cada fold (§3.7)",
    cod: "StratifiedKFold(n_splits=5, shuffle=True, random_state=42)", imp: "StratifiedKFold"};
  return {txt: "`KFold(n_splits=5, shuffle=True, random_state=42)`", porque: "regressão sem tempo nem entidade repetida (§3.7)",
    cod: "KFold(n_splits=5, shuffle=True, random_state=42)", imp: "KFold"};
}

function baselineValores(A){
  if (A.clf) {
    if (A.tipo === "binaria") {
      const p = A.min;
      const ll = -(p * Math.log(p) + (1 - p) * Math.log(1 - p));
      return "`DummyClassifier(strategy=\"prior\")` neste arquivo: PR-AUC ≈ " + fmtNum(p) + " (a taxa da classe minoritária), ROC-AUC = 0,5, accuracy = " + fmtNum(1 - p) +
        ", F1 = 0, Log Loss ≈ " + fmtNum(ll) + ", Brier ≈ " + fmtNum(p * (1 - p));
    }
    const m = A.max;
    return "`DummyClassifier(strategy=\"prior\")` neste arquivo: accuracy = " + fmtNum(m) + " (sempre a classe mais frequente), F1 macro ≈ " + fmtNum((2 * m / (1 + m)) / A.k);
  }
  const ys = A.ys, med = quantil(ys, 0.5);
  let mae = 0, mse = 0, media = 0, sst = 0;
  for (const y of ys) { mae += Math.abs(y - med); mse += (y - med) ** 2; media += y; }
  media /= ys.length; for (const y of ys) sst += (y - media) ** 2;
  const nome = A.tipo === "contagem" ? "DummyRegressor(strategy=\"mean\")" : "DummyRegressor(strategy=\"median\")";
  if (A.tipo === "contagem") return "`" + nome + "` neste arquivo: RMSE ≈ " + fmtNum(Math.sqrt(sst / ys.length)) + ", R² = 0 (a mediana pode ser zero, e a deviance de Poisson exige previsão positiva)";
  return "`" + nome + "` neste arquivo: MAE ≈ " + fmtNum(mae / ys.length) + ", RMSE ≈ " + fmtNum(Math.sqrt(mse / ys.length)) + ", R² ≈ " + fmtNum(1 - mse / sst);
}

function preprocessamento(C, cands){
  const fams = new Set(cands.map(c => c.k));
  const temLinear = ["logC", "ridge", "enet", "poisson", "sgd"].some(k => fams.has(k));
  const temArvoreSk = fams.has("rf") || fams.has("tree");
  const temBoost = ["hgb", "lgbm", "xgb", "cat"].some(k => fams.has(k));
  const L = [];
  const sc = C.outl.length ? "`RobustScaler`" : "`StandardScaler`";
  if (C.num.length) {
    const comAus = C.num.filter(c => c.nMiss > 0);
    if (temLinear) L.push("- **Numéricas** (" + C.num.length + ") para os lineares: `SimpleImputer(strategy=\"median\"" + (comAus.length ? ", add_indicator=True" : "") + ")` + " + sc + (C.outl.length ? " (há outliers relevantes)" : "") + " — a penalização depende da escala (§3.9)");
    if (temBoost) L.push("- **Numéricas** para o boosting: nada — escala é desnecessária e o NaN é tratado nativamente; imputar por hábito pode piorar (§3.4, §3.9)");
    if (temArvoreSk) L.push("- **Numéricas** para RandomForest/árvore: imputação obrigatória (não aceitam NaN no scikit-learn); escala desnecessária (§3.9)");
  }
  if (C.catBaixa.length) L.push("- **Categóricas de baixa cardinalidade** (" + lista(C.catBaixa.map(c => c.nome), 5) + "): `OneHotEncoder(handle_unknown=\"infrequent_if_exist\")` nos lineares; categóricas nativas no boosting (`OrdinalEncoder` + `categorical_features` no HistGB, `category` no LightGBM, `cat_features` no CatBoost) (§3.3)");
  if (C.catAlta.length) L.push("- **Categóricas de alta cardinalidade** (" + lista(C.catAlta.map(c => c.nome), 5) + "): `TargetEncoder` **dentro do pipeline** (faz cross-fitting interno) ou categóricas nativas do CatBoost/LightGBM; nunca One-Hot puro (§3.3)");
  if (C.texto.length) L.push("- **Texto livre** (" + lista(C.texto.map(c => c.nome)) + "): `TfidfVectorizer(ngram_range=(1, 2), min_df=2)` dentro do pipeline (§3.3)");
  const datas = C.P.cols.filter(c => c.tipo === "data");
  if (datas.length) L.push("- **Datas** (" + lista(datas.map(c => c.nome)) + "): derive ano, mês, dia da semana, tempo desde o evento e codificação cíclica; " + (C.tempo ? "lags e janelas móveis usando **só o passado** de cada linha (§3.3)" : "a data bruta não entra como número") );
  const ex = Object.entries(C.excluir).filter(([, m]) => m !== "data (derive componentes antes de usar)");
  if (ex.length) L.push("- **Fora das features**: " + ex.slice(0, 8).map(([n, m]) => cn(n) + " (" + m + ")").join("; ") + (ex.length > 8 ? " e mais " + (ex.length - 8) : ""));
  if (C.P.dup) L.push("- **Deduplicar** " + pl(C.P.dup, "linha repetida", "linhas repetidas") + " antes do split (§3.4)");
  const A = C.A;
  if (A && A.clf && A.desb !== "leve") L.push("- **Desbalanceamento**: `class_weight=\"balanced\"` (ou `scale_pos_weight` no XGBoost/LightGBM) e ajuste de threshold; SMOTE só **dentro** do fold de treino e sempre comparado com `class_weight` (§3.4)");
  if (A && A.tipo === "regressao" && A.col.naoNeg && A.col.assim > 1) L.push("- **Alvo assimétrico** (assimetria " + fmtNum(A.col.assim) + "): teste `TransformedTargetRegressor(func=np.log1p, inverse_func=np.expm1)` contra o alvo bruto");
  L.push("- Tudo dentro de um `Pipeline`/`ColumnTransformer` ajustado só no treino de cada fold (§3.6, item 3)");
  return L;
}

function diagnosticar(P, ctx){
  const C = contexto(P, ctx);
  const obj = ctx.objetivo;
  if (obj !== "prever") return diagnosticarNaoSup(C);
  const A = C.A;
  if (!A) return {erro: "Escolha a coluna-alvo para receber o diagnóstico."};
  if (A.invalido) return {erro: "A coluna-alvo escolhida não serve: " + A.invalido + ". Escolha outra coluna ou outro objetivo."};
  if (P.n <= 200000) C.conflitos = conflitosRotulo(P, C.alvo);
  const cands = escolherCandidatos(C);
  const M = metricas(C), V = validacao(C), al = alertas(C);
  const it = [];
  const tipoTxt = {binaria: "classificação binária", multiclasse: "classificação multiclasse", regressao: "regressão", contagem: "regressão de contagem (Poisson/Tweedie)"}[A.tipo];
  const porqueTipo = {binaria: "o alvo tem 2 valores", multiclasse: "o alvo tem " + A.k + " classes mutuamente exclusivas", regressao: "o alvo é numérico contínuo", contagem: "o alvo é inteiro não negativo e assimétrico/com muitos zeros — não use regressão linear comum (§2, passo 3)"}[A.tipo];
  it.push({t: "Tipo de problema", c: ["**" + (A.semi ? "semissupervisionado" : "supervisionado") + " · " + tipoTxt + "** — " + porqueTipo + "."]});

  const alvoL = ["Coluna " + cn(A.col.nome) + (ctx.motivoAlvo === "nome" ? " (sugerida pelo nome — confirme)" : ctx.motivoAlvo === "ultima" ? " (a última coluna, sugerida por convenção — confirme)" : "")];
  if (A.clf) alvoL.push("- Distribuição: " + A.classes.slice(0, 8).map(([s, c]) => "“" + s + "” " + fmtInt(c) + " (" + fmtPct(c / A.col.nn) + ")").join(" · ") + (A.k > 8 ? " · …" : "") + (A.tipo === "binaria" ? " — classe positiva considerada: “" + A.pos + "”" : ""));
  else alvoL.push("- Distribuição: mín " + fmtNum(A.col.min) + " · mediana " + fmtNum(A.col.med) + " · média " + fmtNum(A.col.media) + " · máx " + fmtNum(A.col.max) + " · assimetria " + fmtNum(A.col.assim));
  alvoL.push("- Janela de observação e de previsão: **INDETERMINADO — falta: a definição do evento e das janelas**, que o arquivo não informa (§2, passo 2)");
  if (C.tempo && C.tempo.tipo === "data") alvoL.push("- Corte temporal: os dados vão de " + new Date(C.tempo.tmin).toISOString().slice(0, 10) + " a " + new Date(C.tempo.tmax).toISOString().slice(0, 10) + " — reserve o período mais recente como teste final");
  it.push({t: "Target", c: alvoL});

  const tiposCont = {};
  P.cols.forEach(c => { tiposCont[c.tipo] = (tiposCont[c.tipo] || 0) + 1; });
  const ausTop = P.cols.filter(c => c.pMiss > 0).sort((a, b) => b.pMiss - a.pMiss).slice(0, 4);
  it.push({t: "Características dos dados", c: [
    "- Tamanho: n = " + fmtInt(P.n) + ", p = " + P.p + " colunas (~" + fmtInt(C.pEnc) + " após encoding) → **" + C.tam + "**",
    "- Tipos: " + Object.entries(tiposCont).map(([k, v]) => v + " " + ROTULO_TIPO[k]).join(" · ") + (C.catAlta.length ? "; alta cardinalidade: " + lista(C.catAlta.map(c => c.nome)) : ""),
    "- Ausentes: " + (ausTop.length ? ausTop.map(c => cn(c.nome) + " " + fmtPct(c.pMiss)).join(" · ") : "nenhum"),
    "- Outliers: " + (C.outl.length ? "relevantes em " + lista(C.outl.map(c => c.nome)) : "irrelevantes nas numéricas"),
    A.clf ? "- Desbalanceamento: menor classe com " + fmtPct(A.min, 2) + " → **" + A.desb + "**" : "- Desbalanceamento: não se aplica (regressão)",
    "- Multicolinearidade: " + (C.multicol.length ? "alta em " + C.multicol.length + " par(es)" : "baixa") + " · p/n ≈ " + fmtNum(C.pn),
    "- Estrutura: " + [C.tempo ? "temporal (" + cn(C.tempo.nome) + ")" : "sem ordem temporal marcada", C.ent ? "entidade repetida (" + cn(C.ent.nome) + ")" : "sem entidade repetida marcada"].join(" · "),
    "- Não linearidade: **NÃO INSPECIONADO** — só aparece comparando o linear com o boosting na validação"
  ]});

  it.push({t: "Riscos identificados", c: al.length ? al.map(x => "- " + x) : ["Nenhum alerta automático. Os riscos que o arquivo não revela continuam valendo — veja o item 15."]});
  it.push({t: "Pré-processamento recomendado", c: preprocessamento(C, cands)});
  it.push({t: "Baseline", c: [
    "**" + (A.clf ? "`DummyClassifier(strategy=\"prior\")`" : A.tipo === "contagem" ? "`DummyRegressor(strategy=\"mean\")`" : "`DummyRegressor(strategy=\"median\")`") + " + " + CAT[A.clf ? "logC" : A.tipo === "contagem" ? "poisson" : "ridge"].nome + "** (§2, passo 7)",
    "- Valor de referência: " + baselineValores(A) + ". Calculado no arquivo inteiro, sem split: é o piso que qualquer candidato precisa superar."
  ]});

  it.push({t: "Modelos recomendados", c: cands.map((x, i) => {
    const m = CAT[x.k];
    return (i + 1) + ". **" + m.nome + "** · Nível " + m.nivel + " · " + m.fw + (m.card ? " · [card](#m-" + m.card + ")" : "") +
      " — **por quê:** " + x.porque + ". **Vantagens:** " + m.vant + ". **Limitações:** " + m.lim + ".";
  }).concat(cands.every(x => CAT[x.k].nivel < 4) ? ["Deep Learning não é recomendado aqui: em dados tabulares de porte pequeno ou médio, modelos baseados em árvores permanecem competitivos ou superiores (Grinsztajn, Oyallon & Varoquaux, 2022) — §4.3."] : [])});

  const fws = [...new Set(cands.map(x => CAT[x.k].fw))];
  const pip = {"scikit-learn": "scikit-learn", "LightGBM": "lightgbm", "XGBoost": "xgboost", "CatBoost": "catboost", "Keras/TensorFlow ou PyTorch": "tensorflow ou torch"};
  const itM = it[it.length - 1];
  itM.c.push("**Frameworks:** " + fws.map(f => f + (pip[f] ? " (`pip install " + pip[f] + "`)" : "")).join(" · ") +
    ". O código abaixo usa só scikit-learn 1.9; os demais entram quando o candidato for medido — a API atual está no card de cada modelo.");

  it.push({t: "Estratégia de validação", c: [V.txt + " — **por quê:** " + V.porque + ".",
    "- Separe antes um conjunto de teste final" + (C.tempo ? " (o período mais recente)" : "") + " e toque nele uma única vez, no fim.",
    "- Reporte média **e** desvio-padrão entre folds; com tuning intensivo, use nested CV."]
    .concat(A.tipo === "binaria" && A.nPos < 100 ? ["- Com " + fmtInt(A.nPos) + " positivos, confira se todo fold tem positivos suficientes."] : [])
    .concat(C.tempo && A.clf ? ["- Folds temporais iniciais podem ter uma classe só; se der erro em ROC-AUC/PR-AUC, aumente o treino inicial."] : [])});
  it.push({t: "Métrica principal", c: [M.principal + " — **por quê:** " + M.porque + "."]});
  it.push({t: "Métricas secundárias", c: M.sec.map(s => "- " + s)});
  it.push({t: "Hiperparâmetros a explorar", c: cands.map(x => "- **" + CAT[x.k].nome + "**: " + CAT[x.k].hp).concat(["- Busca: `RandomizedSearchCV` (30–60 amostras) sobre o **pipeline completo**, com a mesma validação do item 8."])});

  const ajustes = [];
  if (C.regulado) ajustes.push("interpretabilidade de 0,15 para **0,25–0,30**, retirando de desempenho (contexto regulado)");
  if (C.tempoReal) ajustes.push("custo/latência de 0,10 para **0,20** (tempo real)");
  if (C.tempo) ajustes.push("se houver drift entre períodos, estabilidade de 0,20 para **0,30**");
  it.push({t: "Critério de escolha", c: ["Model Fit Score (§5): `MFS = 0,30·D + 0,20·G + 0,15·I + 0,10·C + 0,10·A + 0,10·M + 0,05·N`.",
    "- Ajustes de peso: " + (ajustes.length ? ajustes.join("; ") : "nenhum — pesos padrão"),
    "- Regra de promoção (§4.2): só suba de nível se o ganho na métrica principal superar `max(1% do score atual, desvio entre folds)`; empate (MFS < 0,02) fica com o modelo mais simples."]});
  it.push({t: "Modelo final proposto", c: ["**INDETERMINADO — falta: medir os candidatos.** Este módulo não treina modelos; o vencedor sai da validação do item 8 pelo critério do item 12. Reavalie quando o volume, a distribuição do alvo ou a disponibilidade das features mudar."]});

  const ov = [];
  if (C.tam === "pequeno") ov.push("- **Alto**: poucas linhas — regularização forte, CV repetida, nada de ensembles grandes ou redes");
  if (C.pnAlto) ov.push("- **Alto**: muitas colunas por linha — L1/Elastic Net ou redução de dimensão");
  if (A.clf && A.desb !== "leve") ov.push("- Boosting com classe rara memoriza poucos positivos — `min_child_samples`/`min_samples_leaf` alto e early stopping pela métrica principal");
  if (C.catAlta.length) ov.push("- Encoding de alta cardinalidade fora do pipeline vaza o alvo — o `TargetEncoder` faz cross-fitting interno no `fit_transform`");
  ov.push("- Controles: early stopping no boosting, `max_depth`/`min_samples_leaf` nas árvores, regularização nos lineares");
  ov.push("- Sinal de alerta: diferença grande entre treino e validação, ou desvio entre folds da ordem da diferença entre modelos");
  it.push({t: "Riscos de overfitting", c: ov});

  it.push({t: "Riscos de leakage", c: [
    "- Feature disponível no momento da previsão: **não verificável pelo arquivo** — confira coluna a coluna" + (A.suspeitosNome.length ? ", começando por " + lista(A.suspeitosNome, 4) : ""),
    "- Feature consequência do alvo: " + (A.vaz.length ? "**" + A.vaz.length + " suspeita(s) forte(s)** — " + lista(A.vaz.map(v => v.col)) + " (retiradas do código)" : "nenhum sinal estatístico forte"),
    "- Pré-processamento dentro do pipeline: garantido no código gerado",
    "- Split respeita o tempo: " + (C.tempo ? "sim (" + cn(C.tempo.nome) + ")" : P.cols.some(c => c.tipo === "data") ? "**atenção** — há data, mas nenhuma marcada como ordem temporal" : "sem coluna temporal no arquivo"),
    "- Split respeita grupos: " + (C.ent ? "sim (" + cn(C.ent.nome) + ")" : "nenhuma entidade marcada" + (opcoesEntidade(P).length ? " — candidatas: " + lista(opcoesEntidade(P).map(c => c.nome), 3) : "")),
    "- Duplicatas cruzando treino e teste: " + (P.dup ? pl(P.dup, "linha repetida", "linhas repetidas") + " — deduplique antes" : "nenhuma duplicata exata"),
    "- Agregações e janelas só com o passado; teste nunca usado para escolher nada: dependem da execução"]});

  const exps = [];
  exps.push("1. Baseline (Dummy + " + CAT[A.clf ? "logC" : A.tipo === "contagem" ? "poisson" : "ridge"].nome + ") com o código abaixo — custo mínimo; registre média e desvio da métrica principal.");
  const fortes = cands.filter(x => CAT[x.k].nivel >= 2);
  fortes.forEach((x, i) => exps.push((i + 2) + ". " + CAT[x.k].nome + " — hipótese: supera o nível anterior acima do ruído (regra §4.2)."));
  let k = fortes.length + 2;
  if (A.vaz.length) exps.push(k++ + ". Reincluir " + lista(A.vaz.map(v => v.col), 2) + " só depois de confirmar que existe no momento da previsão; se o score saltar, é vazamento.");
  if (A.tipo === "binaria") exps.push(k++ + ". Ajuste de threshold pelo custo do erro, na validação — nunca no teste.");
  if (A.semi) exps.push(k++ + ". Self-Training/Label Spreading contra o baseline só com rotulados, em ≥ 5 sementes (§3.12).");
  exps.push(k + ". Interpretação do vencedor: `permutation_importance`, SHAP e dependência parcial; validar com quem usa a decisão.");
  it.push({t: "Próximos experimentos", c: exps});

  return {C, itens: it, resumo: [tipoTxt, M.principal.replace(/[*`]/g, ""), V.txt.replace(/`/g, ""), cands.map(x => CAT[x.k].nome).join(", ")], codigo: codigoSup(C, cands, M, V)};
}

function diagnosticarNaoSup(C){
  const P = C.P, obj = C.ctx.objetivo, al = alertas(C), it = [];
  let cands = [], metrica, porqueM, valid, tipo;
  const temTexto = C.texto.length > 0;
  if (obj === "agrupar") {
    tipo = "não supervisionado · clustering";
    cands = [{k: "kmeans", porque: "objetivo agrupar, grupos compactos (§3.1)"}, {k: "gmm", porque: "fronteiras suaves e probabilidade de pertencimento (§3.1)"}, {k: "hdbscan", porque: "ruído e forma irregular (§3.1)"}];
    if (P.n <= 10000) cands.push({k: "hier", porque: "base pequena: o dendrograma ajuda a escolher o número de grupos"});
    metrica = "**Silhouette**"; porqueM = "coesão × separação sem rótulo (§3.8); secundárias Davies-Bouldin (menor melhor), Calinski-Harabasz (maior melhor) e validação de negócio";
    valid = "estabilidade dos grupos entre sementes e subamostras (ex.: ARI entre execuções) + leitura de negócio dos perfis de cada grupo";
  } else if (obj === "anomalias") {
    tipo = "não supervisionado · detecção de anomalias";
    cands = [{k: "zscore", porque: "baseline transparente por variável (§3.1)"}, {k: "iforest", porque: "anomalia global, sem escala (§3.1)"}];
    if (P.n <= 100000) cands.push({k: "lof", porque: "anomalia local, por densidade relativa (§3.1)"});
    const rot = P.cols.find(c => c.tipo === "binario" && c.top.length === 2 && c.top[1][1] / c.nn < 0.1);
    metrica = rot ? "**PR-AUC** usando " + cn(rot.nome) + " como rótulo parcial" : "**taxa de alerta + revisão amostrada**";
    porqueM = rot ? "há uma coluna binária rara que pode servir de rótulo para avaliar (§3.8)" : "sem rótulo, a avaliação é operacional: quantos alertas e quantos se confirmam (§3.8)";
    valid = "separe um período ou amostra para revisão humana; acompanhe a estabilidade do score no tempo";
  } else if (obj === "comprimir") {
    tipo = "não supervisionado · redução de dimensionalidade";
    cands = [{k: "pca", porque: "compressão linear (§3.1)"}];
    if (temTexto || C.catBaixa.length + C.catAlta.length > C.num.length) cands.push({k: "tsvd", porque: "dados esparsos (texto, one-hot) (§3.1)"});
    metrica = "**variância explicada acumulada**"; porqueM = "quanto da informação sobra com k componentes; se a compressão alimenta um modelo, a métrica dele decide";
    valid = "ajuste o PCA só no treino quando ele fizer parte de um pipeline supervisionado";
  } else if (obj === "recomendar") {
    tipo = "recomendação · ranking de itens por usuário";
    cands = [{k: "popular", porque: "baseline obrigatório, calculado só com interações anteriores ao corte (§3.10)"}, {k: "cfknn", porque: "histórico de interações (§3.1)"}, {k: "mf", porque: "histórico de interações, catálogo grande (§3.1)"}, {k: "content", porque: "itens ou usuários novos — cold start (§3.1)"}];
    metrica = "**NDCG@k**"; porqueM = "o usuário vê uma lista ordenada, não uma nota (§3.8); secundárias recall@k, MAP@k, cobertura de catálogo e diversidade";
    valid = C.tempo ? "split temporal global por " + cn(C.tempo.nome) + ": treino até a data de corte, teste depois; split aleatório de interações é proibido (§3.10)" : "**falta coluna de tempo**: o split temporal global é o padrão (§3.10); sem ela, leave-last-out por usuário só vale para recomendação sequencial";
  } else {
    tipo = "não supervisionado · regras de associação";
    cands = [{k: "contag", porque: "baseline (§4.4)"}, {k: "fpg", porque: "base transacional; mesmo resultado do Apriori, mais rápido (§3.13)"}];
    metrica = "**Lift > 1** com suporte mínimo"; porqueM = "mede associação além do acaso (§3.8); secundárias confiança, leverage e conviction";
    valid = "estabilidade das regras no período seguinte; regra que vira ação passa por teste A/B — lift não é causalidade (§3.13)";
  }
  it.push({t: "Tipo de problema", c: ["**" + tipo + "**."]});
  it.push({t: "Target", c: ["Não há target: o objetivo substituto é “" + OBJETIVOS[obj].toLowerCase() + "”."]});
  it.push({t: "Características dos dados", c: ["- Tamanho: n = " + fmtInt(P.n) + ", p = " + P.p + " → **" + C.tam + "**",
    "- Numéricas: " + C.num.length + " · categóricas: " + (C.catBaixa.length + C.catAlta.length) + " · texto: " + C.texto.length]});
  it.push({t: "Riscos identificados", c: al.length ? al.map(x => "- " + x) : ["Nenhum alerta automático."]});
  const pre = [];
  if (["agrupar", "anomalias", "comprimir"].includes(obj)) {
    pre.push("- **Escala obrigatória** para métodos de distância (K-Means, GMM, DBSCAN, LOF, PCA): " + (C.outl.length ? "`RobustScaler` (há outliers)" : "`StandardScaler`") + " (§3.9)");
    if (C.catBaixa.length) pre.push("- Categóricas de baixa cardinalidade: One-Hot com cuidado — distâncias entre dummies dominam facilmente (§3.9)");
    if (C.catAlta.length) pre.push("- Alta cardinalidade (" + lista(C.catAlta.map(c => c.nome), 3) + "): sem alvo, `TargetEncoder` não se aplica — agrupe níveis raros ou deixe de fora");
    pre.push("- Ausentes: imputar (`SimpleImputer`) — métodos de distância não aceitam NaN (§3.9); IsolationForest também exige imputação");
  } else if (obj === "recomendar") {
    pre.push("- Monte a matriz usuário × item esparsa; feedback implícito: ausência é “não observado”, não negativo (§3.10)");
    pre.push("- Exclua itens já consumidos das recomendações, salvo domínios de recompra (§3.10)");
  } else {
    pre.push("- Converta para formato de cesta (uma linha por transação, uma coluna booleana por item); remova itens onipresentes antes de minerar (§3.13)");
  }
  it.push({t: "Pré-processamento recomendado", c: pre});
  it.push({t: "Modelos recomendados", c: cands.map((x, i) => { const m = CAT[x.k]; return (i + 1) + ". **" + m.nome + "** · " + m.fw + (m.card ? " · [card](#m-" + m.card + ")" : "") + " — **por quê:** " + x.porque + ". **Vantagens:** " + m.vant + ". **Limitações:** " + m.lim + "."; })});
  it[it.length - 1].c.push("**Frameworks:** " + [...new Set(cands.map(x => CAT[x.k].fw))].join(" · ") + ".");
  it.push({t: "Estratégia de validação", c: [valid + "."]});
  it.push({t: "Métrica principal", c: [metrica + " — **por quê:** " + porqueM + "."]});
  it.push({t: "Hiperparâmetros a explorar", c: cands.map(x => "- **" + CAT[x.k].nome + "**: " + CAT[x.k].hp)});
  it.push({t: "Modelo final proposto", c: ["**INDETERMINADO — falta: medir os candidatos.** Este módulo não treina modelos."]});
  return {C, itens: it, resumo: [tipo, metrica.replace(/\*\*/g, ""), valid.replace(/[`*]/g, ""), cands.map(x => CAT[x.k].nome).join(", ")], codigo: codigoNaoSup(C)};
}

/* ===================== código Python inicial ===================== */
function leituraPy(P){
  const m = P.meta, nome = m.nomeArquivo || "seu_arquivo";
  if (m.formato === "XLSX") return "df = pd.read_excel(" + py(nome) + ", sheet_name=0)   # requer openpyxl";
  if (m.formato === "JSON Lines") return "df = pd.read_json(" + py(nome) + ", lines=True)";
  if (m.formato === "JSON") {
    if (m.chave) return "import json\nwith open(" + py(nome) + ", encoding=\"utf-8\") as f:\n    df = pd.DataFrame(json.load(f)[" + py(m.chave) + "])";
    if (m.orient === "split") return "df = pd.read_json(" + py(nome) + ", orient=\"split\")";
    if (m.orient === "columns-list") return "import json\nwith open(" + py(nome) + ", encoding=\"utf-8\") as f:\n    df = pd.DataFrame(json.load(f))";
    if (m.orient === "columns") return "df = pd.read_json(" + py(nome) + ", orient=\"columns\")";
    return "df = pd.read_json(" + py(nome) + ")";
  }
  const args = [py(nome), "sep=" + py(m.sep)];
  const br = P.cols.some(c => c.num && c.fmt === "br" && [...c.freq.keys()].some(k => k.indexOf(",") >= 0));
  if (br) { args.push("decimal=\",\""); if (P.cols.some(c => c.num && c.fmt === "br" && c.milhar)) args.push("thousands=\".\""); }
  if (m.encoding === "cp1252") args.push("encoding=\"cp1252\"");
  if (m.encoding === "utf-16") args.push("encoding=\"utf-16\"");
  args.push("na_values=[\"?\", \"-\", \"NA\", \"N/A\", \"null\", \"#N/D\"]");
  return "df = pd.read_csv(" + args.join(", ") + ")";
}

const pyLista = cols => "[" + cols.map(c => py(c.nome)).join(", ") + "]";

function codigoSup(C, cands, M, V){
  const P = C.P, A = C.A, clf = A.clf, cont = A.tipo === "contagem";
  if (C.imagem.length && cands[0].k === "cnn") return "# O sinal está nos arquivos de imagem/áudio, que não fazem parte da tabela.\n# Comece por um modelo pré-treinado congelado + cabeça linear: veja a seção 5.1 (TensorFlow na prática) do manual.";
  const imp = new Set(["import numpy as np", "import pandas as pd", "from sklearn.compose import ColumnTransformer", "from sklearn.pipeline import Pipeline", "from sklearn.model_selection import cross_validate, " + V.imp]);
  const L = [];
  L.push("# Código inicial gerado pelo diagnóstico — confira antes de executar (scikit-learn 1.9).");
  L.push("# Mede o baseline e os candidatos com a validação recomendada; não escolhe o modelo final por você.");
  L.push("");
  L.push(leituraPy(P));
  if (P.dup) L.push("df = df.drop_duplicates()   # " + pl(P.dup, "linha repetida", "linhas repetidas") + ": deduplicar antes do split");
  if (C.tempo) {
    if (C.tempo.tipo === "data") L.push("df[" + py(C.tempo.nome) + "] = pd.to_datetime(df[" + py(C.tempo.nome) + "]" + (C.tempo.dmy ? ", dayfirst=" + (C.tempo.dayfirst ? "True" : "False") : "") + ", errors=\"coerce\")");
    L.push("df = df.sort_values(" + py(C.tempo.nome) + ").reset_index(drop=True)   # validação temporal exige ordem");
  }
  L.push("");
  L.push("alvo = " + py(A.col.nome));
  L.push("df = df[df[alvo].notna()].copy()");
  if (A.tipo === "binaria") {
    if (A.col.num) L.push("y = (df[alvo] == " + A.col.num[A.col.v.indexOf(A.pos)] + ").astype(int)   # classe positiva: " + A.pos);
    else L.push("y = (df[alvo].astype(str).str.strip() == " + py(A.pos) + ").astype(int)   # classe positiva: " + py(A.pos));
  } else if (A.tipo === "multiclasse") L.push("y = df[alvo].astype(str).str.strip()");
  else L.push("y = df[alvo]");
  L.push("");
  const textoMain = C.textoPrincipal;
  const vazias = Object.entries(C.excluir);
  if (vazias.length) {
    L.push("# fora das features:");
    vazias.slice(0, 12).forEach(([n, m]) => L.push("#   " + n + " — " + m));
    if (vazias.length > 12) L.push("#   … e mais " + (vazias.length - 12));
  }
  const modelos = [];
  let scoring = M.sk;
  if (clf) { imp.add("from sklearn.dummy import DummyClassifier"); modelos.push(["baseline_dummy", "DummyClassifier(strategy=\"prior\")"]); }
  else { imp.add("from sklearn.dummy import DummyRegressor"); modelos.push(["baseline_dummy", "DummyRegressor(strategy=\"" + (cont ? "mean" : "median") + "\")"]); }
  const bal = clf && A.desb !== "leve" ? ", class_weight=\"balanced\"" : "";
  if (textoMain) {
    const tc = C.texto[0].nome;
    imp.add("from sklearn.feature_extraction.text import TfidfVectorizer");
    L.push("texto = " + py(tc));
    L.push("X = df[texto].fillna(\"\")");
    L.push("");
    if (clf) {
      imp.add("from sklearn.linear_model import LogisticRegression"); imp.add("from sklearn.naive_bayes import ComplementNB");
      modelos.push(["nivel1_tfidf_logistica", "Pipeline([(\"tfidf\", TfidfVectorizer(ngram_range=(1, 2), min_df=2)),\n                                     (\"mod\", LogisticRegression(max_iter=1000" + bal + "))])"]);
      modelos.push(["nivel1_tfidf_nb", "Pipeline([(\"tfidf\", TfidfVectorizer(ngram_range=(1, 2), min_df=2)),\n                              (\"mod\", ComplementNB())])"]);
    } else {
      imp.add("from sklearn.linear_model import Ridge");
      modelos.push(["nivel1_tfidf_ridge", "Pipeline([(\"tfidf\", TfidfVectorizer(ngram_range=(1, 2), min_df=2)),\n                                  (\"mod\", Ridge())])"]);
    }
  } else {
    L.push("num_cols = " + pyLista(C.num));
    L.push("cat_cols = " + pyLista(C.catBaixa) + "   # até 50 níveis");
    L.push("alta_card = " + pyLista(C.catAlta) + "   # mais de 50 níveis");
    L.push("X = df[num_cols + cat_cols + alta_card].copy()");
    if (C.num.length) L.push("X[num_cols] = X[num_cols].apply(pd.to_numeric, errors=\"coerce\")   # sobras de texto viram NaN");
    if (C.ent) L.push("grupos = df[" + py(C.ent.nome) + "]");
    L.push("");
    const esc = C.outl.length ? "RobustScaler" : "StandardScaler";
    imp.add("from sklearn.impute import SimpleImputer");
    imp.add("from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, TargetEncoder, " + esc);
    L.push("# lineares: imputação + escala + One-Hot; alta cardinalidade com TargetEncoder (cross-fitting interno)");
    L.push("pre_linear = ColumnTransformer([");
    L.push("    (\"num\", Pipeline([(\"imp\", SimpleImputer(strategy=\"median\", add_indicator=True)), (\"esc\", " + esc + "())]), num_cols),");
    L.push("    (\"cat\", Pipeline([(\"imp\", SimpleImputer(strategy=\"most_frequent\")),");
    L.push("                      (\"ohe\", OneHotEncoder(handle_unknown=\"infrequent_if_exist\"))]), cat_cols),");
    L.push("    (\"alta\", TargetEncoder(random_state=42), alta_card),");
    L.push("])");
    L.push("# boosting: categóricas nativas e NaN nativo, sem escala");
    L.push("pre_arvore = ColumnTransformer([");
    L.push("    (\"cat\", OrdinalEncoder(handle_unknown=\"use_encoded_value\", unknown_value=np.nan), cat_cols),");
    L.push("    (\"alta\", TargetEncoder(random_state=42), alta_card),");
    L.push("], remainder=\"passthrough\")   # numéricas passam direto, com NaN");
    L.push("");
    const catIdx = C.catBaixa.length ? "list(range(len(cat_cols)))" : "None";
    if (clf) {
      imp.add("from sklearn.linear_model import LogisticRegression"); imp.add("from sklearn.ensemble import HistGradientBoostingClassifier");
      modelos.push(["nivel1_logistica", "Pipeline([(\"pre\", pre_linear), (\"mod\", LogisticRegression(max_iter=1000" + bal + "))])"]);
      modelos.push(["nivel3_histgb", "Pipeline([(\"pre\", pre_arvore), (\"mod\", HistGradientBoostingClassifier(\n        categorical_features=" + catIdx + ", early_stopping=True, random_state=42" + bal + "))])"]);
    } else {
      imp.add("from sklearn.ensemble import HistGradientBoostingRegressor");
      if (cont) { imp.add("from sklearn.linear_model import PoissonRegressor"); modelos.push(["nivel1_poisson", "Pipeline([(\"pre\", pre_linear), (\"mod\", PoissonRegressor(max_iter=1000))])"]); }
      else { imp.add("from sklearn.linear_model import Ridge"); modelos.push(["nivel1_ridge", "Pipeline([(\"pre\", pre_linear), (\"mod\", Ridge())])"]); }
      modelos.push(["nivel3_histgb", "Pipeline([(\"pre\", pre_arvore), (\"mod\", HistGradientBoostingRegressor(\n        " + (cont ? "loss=\"poisson\", " : "") + "categorical_features=" + catIdx + ", early_stopping=True, random_state=42))])"]);
    }
  }
  L.push("modelos = {");
  modelos.forEach(([n, m]) => L.push("    " + py(n) + ": " + m + ","));
  L.push("}");
  if (cands.some(x => ["lgbm", "xgb", "cat", "rf"].includes(x.k)))
    L.push("# Os demais candidatos (" + cands.filter(x => ["lgbm", "xgb", "cat", "rf"].includes(x.k)).map(x => CAT[x.k].nome).join(", ") + ") entram no mesmo laço — API no card de cada modelo no manual.");
  L.push("");
  L.push("cv = " + V.cod);
  L.push("metricas = {" + Object.entries(scoring).map(([k, v]) => py(k) + ": " + py(v)).join(", ") + "}");
  if (!clf) L.push("# métricas neg_* são negativas por convenção do scikit-learn: quanto mais perto de zero, melhor");
  L.push("for nome, modelo in modelos.items():");
  L.push("    res = cross_validate(modelo, X, y, cv=cv, scoring=metricas" + (V.grupos && !textoMain ? ", groups=grupos" : "") + ", n_jobs=-1)");
  L.push("    resumo = {m: f\"{res['test_' + m].mean():.4f} ± {res['test_' + m].std():.4f}\" for m in metricas}");
  L.push("    print(nome, resumo)");
  return [...imp].sort((a, b) => (a.startsWith("import") ? 0 : 1) - (b.startsWith("import") ? 0 : 1) || a.localeCompare(b)).join("\n") + "\n\n" + L.join("\n");
}

function codigoNaoSup(C){
  const P = C.P, obj = C.ctx.objetivo;
  if (obj === "recomendar") return "# Recomendação: veja a seção 16 do manual (16.4 validação temporal, 16.6 fatoração em TensorFlow).\n# Comece pelo baseline de popularidade calculado só com interações anteriores ao corte.";
  if (obj === "associar") return "# Regras de associação: veja a seção 3.5 do manual (FP-Growth com mlxtend).\n# Transforme em cesta: uma linha por transação, uma coluna booleana por item.";
  const esc = C.outl.length ? "RobustScaler" : "StandardScaler";
  const L = ["import numpy as np", "import pandas as pd", "from sklearn.compose import ColumnTransformer", "from sklearn.impute import SimpleImputer",
    "from sklearn.pipeline import Pipeline", "from sklearn.preprocessing import OneHotEncoder, " + esc];
  if (obj === "agrupar") L.push("from sklearn.cluster import KMeans", "from sklearn.metrics import silhouette_score");
  if (obj === "anomalias") L.push("from sklearn.ensemble import IsolationForest");
  if (obj === "comprimir") L.push("from sklearn.decomposition import PCA");
  L.push("", "# Código inicial gerado pelo diagnóstico — confira antes de executar (scikit-learn 1.9).", "", leituraPy(P));
  if (P.dup && obj !== "anomalias") L.push("df = df.drop_duplicates()");
  L.push("num_cols = " + pyLista(C.num), "cat_cols = " + pyLista(C.catBaixa) + "   # alta cardinalidade e texto ficam de fora",
    "X = df[num_cols + cat_cols].copy()");
  if (C.num.length) L.push("X[num_cols] = X[num_cols].apply(pd.to_numeric, errors=\"coerce\")");
  L.push("pre = ColumnTransformer([",
    "    (\"num\", Pipeline([(\"imp\", SimpleImputer(strategy=\"median\")), (\"esc\", " + esc + "())]), num_cols),",
    "    (\"cat\", Pipeline([(\"imp\", SimpleImputer(strategy=\"most_frequent\")),",
    "                      (\"ohe\", OneHotEncoder(handle_unknown=\"ignore\", sparse_output=False))]), cat_cols),",
    "])", "");
  if (obj === "agrupar") L.push("Xt = pre.fit_transform(X)", "for k in range(2, 11):",
    "    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xt)",
    "    s = silhouette_score(Xt, km.labels_, sample_size=min(10000, Xt.shape[0]), random_state=42)",
    "    print(k, round(s, 4))   # escolha k pela silhouette E pela leitura de negócio dos grupos");
  if (obj === "anomalias") L.push("iso = Pipeline([(\"pre\", pre), (\"mod\", IsolationForest(n_estimators=300, random_state=42))])",
    "iso.fit(X)", "df[\"score_anomalia\"] = -iso.score_samples(X)   # maior = mais anômalo",
    "print(df.sort_values(\"score_anomalia\", ascending=False).head(20))   # revise uma amostra com quem conhece o processo");
  if (obj === "comprimir") L.push("Xt = pre.fit_transform(X)", "pca = PCA().fit(Xt)", "acum = np.cumsum(pca.explained_variance_ratio_)",
    "print(\"componentes para 95% da variância:\", int(np.searchsorted(acum, 0.95)) + 1)");
  return L.join("\n");
}

/* ===================== saída: HTML e Markdown ===================== */
function inline(s){
  let h = escH(s);
  h = h.replace(/\[\[(alto|medio|info)\]\]\s*/g, (m, k) => '<span class="dx-sev ' + k + '">' + ({alto: "alto", medio: "médio", info: "info"})[k] + "</span>");
  h = h.replace(/`([^`]+)`/g, "<code>$1</code>");
  h = h.replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
  h = h.replace(/\[([^\]]+)\]\((#[a-z0-9-]+)\)/g, '<a href="$2">$1</a>');
  return h;
}

function corpoHtml(linhas){
  let h = "", ul = null, ol = null;
  const fecha = () => { if (ul) { h += "<ul>" + ul + "</ul>"; ul = null; } if (ol) { h += "<ol>" + ol + "</ol>"; ol = null; } };
  for (const l of linhas) {
    if (l.startsWith("- ")) { if (ol) fecha(); ul = (ul || "") + "<li>" + inline(l.slice(2)) + "</li>"; }
    else if (/^\d+\. /.test(l)) { if (ul) fecha(); ol = (ol || "") + "<li>" + inline(l.replace(/^\d+\. /, "")) + "</li>"; }
    else { fecha(); h += "<p>" + inline(l) + "</p>"; }
  }
  fecha();
  return h;
}

function paraMarkdown(D, P){
  const md = [];
  md.push("# Diagnóstico do Dataset — " + (P.meta.nomeArquivo || "dataset"), "");
  md.push("> Gerado por regras determinísticas (skill de decisão do Manual de Machine Learning), no navegador, sem treinar modelos. " +
          fmtInt(P.n) + " linhas · " + P.p + " colunas · " + new Date().toISOString().slice(0, 10), "");
  D.itens.forEach((x, i) => {
    md.push("**" + (i + 1) + ". " + x.t + "**", "");
    x.c.forEach(l => md.push(l.replace(/\[\[(alto|medio|info)\]\]/g, (m, k) => "**[" + k.toUpperCase().replace("MEDIO", "MÉDIO") + "]**").replace(/ · \[card\]\((#[a-z0-9-]+)\)/g, " · card `$1` no manual").replace(/\[([^\]]+)\]\(#[a-z0-9-]+\)/g, "$1")));
    md.push("");
  });
  md.push("## Código inicial", "", "```python", D.codigo, "```", "");
  return md.join("\n");
}

/* ===================== dataset de exemplo (sintético) ===================== */
function exemploCsv(){
  let s = 20260901;
  const rnd = () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const um = (a) => a[Math.floor(rnd() * a.length)];
  const UFS = ["SP", "SP", "SP", "RJ", "RJ", "MG", "MG", "RS", "PR", "SC", "BA", "PE", "CE", "GO", "DF", "ES", "PA", "AM", "MT", "MS", "PB", "RN", "AL", "PI", "MA", "SE", "TO"];
  const FEED = ["app trava ao abrir a fatura", "atendimento resolveu rápido", "preço subiu demais neste ano", "gosto do plano mas a internet cai à noite", "demorou para instalar o equipamento", "sem reclamações, serviço estável", "cobrança duplicada no último mês"];
  const linhas = ["id_cliente;data_cadastro;uf;bairro;plano;canal_aquisicao;mensalidade;meses_contrato;chamados_suporte_90d;nps;usa_app;ultimo_feedback;motivo_cancelamento;cancelou"];
  const regs = [];
  for (let i = 0; i < 2400; i++) {
    const plano = um(["básico", "básico", "padrão", "padrão", "premium"]);
    const base = plano === "básico" ? 79.9 : plano === "padrão" ? 119.9 : 189.9;
    const meses = 1 + Math.floor(rnd() * 48);
    const cham = Math.floor(-Math.log(1 - rnd()) * 1.2);
    const usaApp = rnd() < 0.6;
    const z = -2.4 + 0.55 * cham - 0.04 * meses + (usaApp ? -0.5 : 0.3) + (plano === "básico" ? 0.4 : 0) + (rnd() - 0.5);
    const cancelou = rnd() < 1 / (1 + Math.exp(-z));
    const nps = rnd() < (cancelou ? 0.35 : 0.12) ? "" : String(Math.max(0, Math.min(10, Math.round((cancelou ? 5 : 8) + (rnd() - 0.5) * 5))));
    const d = new Date(Date.UTC(2022, 0, 1) + Math.floor(rnd() * 1460) * 86400000);
    const data = String(d.getUTCDate()).padStart(2, "0") + "/" + String(d.getUTCMonth() + 1).padStart(2, "0") + "/" + d.getUTCFullYear();
    const mens = (base + Math.round((rnd() - 0.5) * 20 * 100) / 100).toFixed(2).replace(".", ",");
    regs.push(["C" + String(10001 + i), data, um(UFS), "bairro_" + String(1 + Math.floor(Math.pow(rnd(), 1.6) * 180)).padStart(3, "0"), plano,
      um(["site", "app", "loja", "indicação"]), mens, meses, cham, nps, usaApp ? "sim" : "não",
      rnd() < 0.55 ? "" : "\"" + um(FEED) + ", " + um(FEED) + " (protocolo " + (10000 + Math.floor(rnd() * 89999)) + ")\"", cancelou ? um(["preço", "concorrência", "atendimento", "mudança de endereço"]) : "", cancelou ? "sim" : "não"]);
  }
  for (let k = 0; k < 12; k++) regs.push(regs[Math.floor(rnd() * regs.length)].slice());
  regs.forEach(r => linhas.push(r.join(";")));
  return linhas.join("\n") + "\n";
}

/* ===================== exportação para testes (Node) ===================== */
const API = {lerArquivo, lerDelimitado, lerJson, lerXlsx, perfilar, sugerirAlvo, sugerirTempo, opcoesEntidade, diagnosticar, paraMarkdown, exemploCsv, corpoHtml};
if (typeof document === "undefined") { globalThis.__dx = API; return; }

/* ===================== interface ===================== */
const el = id => document.getElementById(id);
const raiz = el("diagnostico");
if (!raiz) return;
const zona = el("dxDrop"), entrada = el("dxFile"), status = el("dxStatus"), erroBox = el("dxErro"), painel = el("dxPainel");
const sel = {objetivo: el("dxObjetivo"), alvo: el("dxAlvo"), tempo: el("dxTempo"), entidade: el("dxEntidade"), custo: el("dxCusto"), interp: el("dxInterp"), latencia: el("dxLatencia")};
let P = null, D = null, motivoAlvo = null;

function setStatus(txt){ status.textContent = txt; }
function mostrarErro(msg){ erroBox.innerHTML = msg ? '<b class="ctitle">Não foi possível analisar</b>' + escH(msg) : ""; erroBox.hidden = !msg; }

async function processar(file, nomeExibido){
  mostrarErro(""); setStatus("lendo " + (nomeExibido || file.name) + "…");
  await new Promise(r => setTimeout(r, 30));
  try {
    const ds = await lerArquivo(file);
    ds.meta.nomeArquivo = nomeExibido || file.name;
    if (!ds.n) throw new Error("O arquivo não tem linhas de dados.");
    setStatus("analisando " + fmtInt(ds.n) + " linhas…");
    await new Promise(r => setTimeout(r, 30));
    P = perfilar(ds);
    prepararFormulario();
    renderPerfil();
    painel.hidden = false;
    atualizar();
    setStatus((nomeExibido || file.name) + " · " + fmtInt(P.n) + " linhas · " + P.p + " colunas · analisado no seu navegador");
    el("dxPerfil").scrollIntoView({behavior: "smooth", block: "start"});
  } catch (e) {
    P = null; painel.hidden = true;
    setStatus("nenhum arquivo analisado");
    mostrarErro(e && e.message ? e.message : String(e));
  }
}

function opcoes(select, itens, valor){
  select.innerHTML = itens.map(([v, t]) => '<option value="' + escH(v) + '"' + (v === valor ? " selected" : "") + ">" + escH(t) + "</option>").join("");
}

function prepararFormulario(){
  const sug = sugerirAlvo(P);
  motivoAlvo = sug ? sug.motivo : null;
  const fmt = detectarFormato(P);
  opcoes(sel.objetivo, Object.entries(OBJETIVOS), "prever");
  opcoes(sel.alvo, [["", "— escolha —"]].concat(P.cols.filter(PODE_SER_ALVO).map(c => [c.nome, c.nome + " (" + c.tipo + ")"])), sug ? sug.nome : "");
  opcoes(sel.tempo, [["", "nenhuma"]].concat(opcoesTempo(P).map(c => [c.nome, c.nome])), sugerirTempo(P));
  const ents = opcoesEntidade(P);
  opcoes(sel.entidade, [["", "nenhuma"]].concat(ents.map(c => [c.nome, c.nome + " (" + fmtInt(c.distinct) + " valores)"])), ents.length && !fmt.interacoes ? ents[0].nome : "");
  sel.interp.value = "desejavel"; sel.latencia.value = "lote";
  opcoesCusto();
}

function opcoesCusto(){
  const a = P && P.cols.find(c => c.nome === sel.alvo.value);
  const reg = a && a.tipo === "numerico" && !(a.inteiro && a.distinct <= 10 && a.min >= 0);
  const atual = sel.custo.value;
  const itens = reg
    ? [["nd", "não definido"], ["grandes", "erros grandes custam muito mais"], ["linear", "custo proporcional ao erro"], ["escala", "várias séries com escalas diferentes"]]
    : [["nd", "não definido"], ["simetrico", "os dois erros custam parecido"], ["fn", "deixar passar um positivo é pior (FN)"], ["fp", "alarme falso é pior (FP)"], ["prob", "a probabilidade vira preço ou limite"]];
  opcoes(sel.custo, itens, itens.some(([v]) => v === atual) ? atual : "nd");
  raiz.querySelectorAll(".dx-sup").forEach(e => e.hidden = sel.objetivo.value !== "prever");
}


function renderPerfil(){
  const m = P.meta;
  const sepTxt = m.sep ? (m.sep === "\t" ? "tabulação" : "“" + m.sep + "”") : null;
  el("dxResumo").innerHTML = [
    "<b>" + fmtInt(P.n) + "</b> linhas", "<b>" + P.p + "</b> colunas", "formato <b>" + escH(m.formato) + "</b>",
    sepTxt ? "separador <b>" + escH(sepTxt) + "</b>" : null, "<b>" + fmtInt(P.dup) + "</b> duplicadas",
    "codificação <b>" + escH(m.encoding) + "</b>"
  ].filter(Boolean).map(x => '<span class="kpi">' + x + "</span>").join("");
  const linhas = P.cols.slice(0, 300).map(c => {
    let ex;
    if (c.num && (c.tipo === "numerico" || c.tipo === "binario")) ex = "mín " + fmtNum(c.min) + " · mediana " + fmtNum(c.med) + " · máx " + fmtNum(c.max);
    else if (c.tipo === "data") ex = new Date(c.tmin).toISOString().slice(0, 10) + " → " + new Date(c.tmax).toISOString().slice(0, 10);
    else ex = c.top.map(([s, k]) => (s.length > 28 ? s.slice(0, 27) + "…" : s) + " (" + fmtInt(k) + ")").join(" · ");
    const obs = [];
    if (c.alta) obs.push("alta cardinalidade");
    if (c.entidade) obs.push("entidade?");
    if (c.pii) obs.push("dado pessoal?");
    if (c.outl > 0.01) obs.push("outliers");
    if (c.sujeira) obs.push("quase numérica");
    if (c.pMiss > 0.4) obs.push("ausência severa");
    return "<tr><td><b>" + escH(c.nome) + "</b></td><td><span class=\"dx-tipo\">" + (ROTULO_TIPO[c.tipo] || c.tipo) + (c.inteiro && c.tipo === "numerico" ? " inteiro" : "") + "</span></td><td>" +
      (c.nMiss ? fmtPct(c.pMiss) : "0") + "</td><td>" + fmtInt(c.distinct) + "</td><td>" + escH(ex) + "</td><td>" + escH(obs.join(", ")) + "</td></tr>";
  }).join("");
  el("dxColunas").querySelector("tbody").innerHTML = linhas + (P.p > 300 ? '<tr><td colspan="6">… e mais ' + (P.p - 300) + " colunas</td></tr>" : "");
}

function atualizar(){
  if (!P) return;
  const ctx = {objetivo: sel.objetivo.value, alvo: sel.alvo.value, tempo: sel.tempo.value, entidade: sel.entidade.value,
               custo: sel.custo.value, interp: sel.interp.value, latencia: sel.latencia.value,
               motivoAlvo: sel.alvo.value && P.cols.find(c => c.nome === sel.alvo.value) && sugerirAlvo(P) && sugerirAlvo(P).nome === sel.alvo.value ? motivoAlvo : null};
  try { D = diagnosticar(P, ctx); }
  catch (e) { D = {erro: "Falha inesperada nas regras: " + (e && e.message)}; }
  const saida = el("dxSaida"), cod = el("dxCodigo");
  if (D.erro) {
    saida.innerHTML = '<div class="callout warn"><b class="ctitle">Falta uma escolha</b>' + escH(D.erro) + "</div>";
    cod.textContent = ""; el("dxCodigoBox").hidden = true; el("dxAcoes").hidden = true;
    return;
  }
  const rs = D.resumo;
  saida.innerHTML = '<div class="callout ok"><b class="ctitle">Resumo</b>' +
    "<b>" + escH(rs[0]) + "</b> · métrica principal: <b>" + escH(rs[1]) + "</b><br>validação: " + escH(rs[2]) + "<br>candidatos: " + escH(rs[3]) + "</div>" +
    D.itens.map((x, i) => '<div class="dx-item' + (x.t === "Riscos identificados" && x.c.some(l => l.includes("[[alto]]")) ? " dx-alto" : "") + '"><h4><i>' + String(i + 1).padStart(2, "0") + "</i>" + escH(x.t) + "</h4>" + corpoHtml(x.c) + "</div>").join("");
  cod.innerHTML = typeof highlightPy === "function" ? highlightPy(escH(D.codigo).replace(/&quot;/g, '"')) : escH(D.codigo);
  el("dxCodigoBox").hidden = false; el("dxAcoes").hidden = false;
}

function baixar(nome, conteudo, tipo){
  const url = URL.createObjectURL(new Blob([conteudo], {type: tipo}));
  const a = document.createElement("a"); a.href = url; a.download = nome;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

zona.addEventListener("click", () => entrada.click());
zona.addEventListener("dragover", e => { e.preventDefault(); zona.classList.add("over"); });
zona.addEventListener("dragleave", () => zona.classList.remove("over"));
zona.addEventListener("drop", e => { e.preventDefault(); zona.classList.remove("over"); const f = e.dataTransfer.files[0]; if (f) processar(f); });
entrada.addEventListener("change", () => { const f = entrada.files[0]; if (f) processar(f); entrada.value = ""; });
el("dxExemplo").addEventListener("click", () => {
  const f = new File([exemploCsv()], "exemplo_churn_sintetico.csv", {type: "text/csv"});
  processar(f, "exemplo_churn_sintetico.csv");
});
el("dxBaixarExemplo").addEventListener("click", () => baixar("exemplo_churn_sintetico.csv", exemploCsv(), "text/csv;charset=utf-8"));
sel.objetivo.addEventListener("change", () => { opcoesCusto(); atualizar(); });
sel.alvo.addEventListener("change", () => { opcoesCusto(); atualizar(); });
[sel.tempo, sel.entidade, sel.custo, sel.interp, sel.latencia].forEach(s => s.addEventListener("change", atualizar));
el("dxBaixarMd").addEventListener("click", () => {
  if (!D || D.erro) return;
  const base = (P.meta.nomeArquivo || "dataset").replace(/\.[^.]+$/, "");
  baixar("diagnostico_" + base + ".md", paraMarkdown(D, P), "text/markdown;charset=utf-8");
});
el("dxCopiarMd").addEventListener("click", ev => {
  if (!D || D.erro) return;
  const b = ev.currentTarget;
  navigator.clipboard.writeText(paraMarkdown(D, P)).then(() => { b.textContent = "Copiado"; setTimeout(() => b.textContent = "Copiar diagnóstico", 1400); })
    .catch(() => { b.textContent = "Falhou"; });
});
el("dxLimpar").addEventListener("click", () => {
  P = null; D = null; painel.hidden = true; mostrarErro(""); setStatus("nenhum arquivo analisado");
  el("dxSaida").innerHTML = ""; el("dxCodigo").textContent = "";
  el("dxColunas").querySelector("tbody").innerHTML = "";
});
})();
