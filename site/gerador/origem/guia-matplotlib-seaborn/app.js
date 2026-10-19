(function () {
  "use strict";

  /* ------------------------------------------------ realce de sintaxe Python */
  var KW = new Set("False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield".split(" "));
  var BI = new Set("print len range dict list tuple set zip enumerate sorted min max sum abs round int float str bool isinstance open map filter any all reversed super".split(" "));
  var RX = /(#[^\n]*)|((?:[rRbBuUfF]{1,2})?(?:"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'))|(\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b)|(@[A-Za-z_][\w.]*)|([A-Za-z_À-ɏ][\wÀ-ɏ]*)|([\s\S])/g;

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function realca(el) {
    var src = el.textContent.replace(/\n$/, "");
    el._bruto = src;
    var toks = [], m, prev = "";
    RX.lastIndex = 0;
    while ((m = RX.exec(src))) {
      var cls = "";
      if (m[1]) cls = "t-com";
      else if (m[2]) cls = "t-str";
      else if (m[3]) cls = "t-num";
      else if (m[4]) cls = "t-dec";
      else if (m[5]) {
        var w = m[5];
        if (KW.has(w)) cls = "t-kw";
        else if (prev === "def" || prev === "class") cls = "t-fn";
        else if (BI.has(w)) cls = "t-bi";
        else if (/^\s*\(/.test(src.slice(RX.lastIndex, RX.lastIndex + 40))) cls = "t-fn";
        prev = w;
      }
      toks.push([cls, m[0]]);
    }
    var linhas = [[]];
    toks.forEach(function (t) {
      t[1].split("\n").forEach(function (parte, i) {
        if (i > 0) linhas.push([]);
        if (parte) linhas[linhas.length - 1].push(t[0] ? '<span class="' + t[0] + '">' + esc(parte) + "</span>" : esc(parte));
      });
    });
    el.innerHTML = linhas.map(function (l, i) {
      return '<span class="ln" data-n="' + (i + 1) + '">' + l.join("") + "</span>";
    }).join("");
  }
  document.querySelectorAll("code.py").forEach(realca);

  /* ------------------------------------------------ copiar */
  function copiaTexto(texto) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(texto).then(function () { return true; }, function () { return copiaAntigo(texto); });
    }
    return Promise.resolve(copiaAntigo(texto));
  }
  function copiaAntigo(texto) {
    var ta = document.createElement("textarea");
    ta.value = texto;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    ta.remove();
    return ok;
  }
  document.querySelectorAll(".copy").forEach(function (bt) {
    bt.addEventListener("click", function () {
      var code = bt.closest(".codeblock").querySelector("code");
      copiaTexto(code._bruto + "\n").then(function (ok) {
        bt.textContent = ok ? "Copiado" : "Selecione e copie";
        bt.classList.toggle("ok", ok);
        setTimeout(function () { bt.textContent = "Copiar"; bt.classList.remove("ok"); }, 1800);
      });
    });
  });

  /* ------------------------------------------------ realce de linhas por eixo */
  function recipiente(el) { return el.closest(".card, .bloco"); }

  function aplicaEixo(cont, eixo) {
    if (!cont) return;
    cont.querySelectorAll(".ln.hl").forEach(function (l) { l.classList.remove("hl"); });
    cont.dataset.eixo = eixo || "";
    cont.querySelectorAll(".chip.eixo").forEach(function (c) {
      c.setAttribute("aria-pressed", String(!!eixo && c.dataset.axis === eixo));
    });
    if (!eixo) return 0;
    var total = 0;
    cont.querySelectorAll(".pane:not([hidden]) .codeblock").forEach(function (cb) {
      var mapa = JSON.parse(cb.dataset.axes || "{}");
      var linhas = mapa[eixo] || [];
      var primeira = null;
      linhas.forEach(function (n) {
        var ln = cb.querySelector('.ln[data-n="' + n + '"]');
        if (ln) { ln.classList.add("hl"); primeira = primeira || ln; total++; }
      });
      if (primeira) {
        var pre = cb.querySelector("pre");
        pre.scrollTop += primeira.getBoundingClientRect().top - pre.getBoundingClientRect().top - 40;
      }
    });
    return total;
  }

  document.querySelectorAll(".chip.eixo").forEach(function (chip) {
    chip.setAttribute("aria-pressed", "false");
    chip.title = "Realçar as linhas de código que aplicam este eixo";
    chip.addEventListener("click", function () {
      var cont = recipiente(chip);
      var ativo = cont.dataset.eixo === chip.dataset.axis;
      aplicaEixo(cont, ativo ? "" : chip.dataset.axis);
    });
  });

  /* ------------------------------------------------ alternadores (abas, antes e depois, passos) */
  document.querySelectorAll(".switch").forEach(function (sw) {
    var abas = Array.prototype.slice.call(sw.querySelectorAll(":scope > .seg > button"));
    var paineis = Array.prototype.slice.call(sw.querySelectorAll(":scope > .pane"));
    var anterior = sw.querySelector(".prev"), proximo = sw.querySelector(".next");
    var atual = 0;
    function seleciona(i, foco) {
      atual = i;
      abas.forEach(function (a, j) {
        a.setAttribute("aria-selected", String(j === i));
        a.tabIndex = j === i ? 0 : -1;
      });
      paineis.forEach(function (p, j) { p.hidden = j !== i; });
      if (foco) abas[i].focus();
      if (anterior) { anterior.disabled = i === 0; proximo.disabled = i === abas.length - 1; }
      var cont = recipiente(sw);
      if (cont && cont.dataset.eixo) aplicaEixo(cont, cont.dataset.eixo);
    }
    sw._seleciona = seleciona;
    sw._atual = function () { return atual; };
    sw._abas = abas;
    abas.forEach(function (a, i) {
      a.addEventListener("click", function () { seleciona(i); });
      a.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight" || e.key === "ArrowDown") { e.preventDefault(); seleciona((i + 1) % abas.length, true); }
        if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); seleciona((i - 1 + abas.length) % abas.length, true); }
      });
    });
    if (anterior) {
      anterior.addEventListener("click", function () { if (atual > 0) seleciona(atual - 1); });
      proximo.addEventListener("click", function () { if (atual < abas.length - 1) seleciona(atual + 1); });
    }
    seleciona(0);
  });

  /* ------------------------------------------------ filtros e busca */
  var estado = { sit: "todas", lib: "todas", q: "" };
  var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));
  var itensNav = Array.prototype.slice.call(document.querySelectorAll(".nav li"));
  var contagem = document.querySelector(".contagem");
  var vazio = document.querySelector("#catalogo .vazio");
  var busca = document.getElementById("busca");

  function normaliza(s) {
    return (s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
  }
  function passaFiltro(el) {
    var sits = (el.dataset.sit || "").split(" ");
    var libs = (el.dataset.lib || "").split(" ");
    return (estado.sit === "todas" || sits.indexOf(estado.sit) >= 0) &&
           (estado.lib === "todas" || libs.indexOf(estado.lib) >= 0);
  }
  function aplicaFiltros() {
    var q = normaliza(estado.q);
    var n = 0;
    cards.forEach(function (c) {
      var ok = passaFiltro(c) && (!q || c.dataset.busca.indexOf(q) >= 0);
      c.hidden = !ok;
      if (ok) n++;
      if (ok && estado.lib !== "todas") {
        var sw = c.querySelector(".switch");
        if (sw && sw._abas[sw._atual()].dataset.lib !== estado.lib) {
          var idx = sw._abas.findIndex(function (a) { return a.dataset.lib === estado.lib; });
          if (idx >= 0) sw._seleciona(idx);
        }
      }
    });
    itensNav.forEach(function (li) {
      if (li.classList.contains("n1")) { li.hidden = false; return; }
      var ok = li.dataset.sit === undefined ? true : passaFiltro(li);
      if (q) ok = ok && li.dataset.busca.indexOf(q) >= 0;
      li.hidden = !ok;
    });
    var filtrando = estado.sit !== "todas" || estado.lib !== "todas" || q;
    contagem.textContent = filtrando ? n + " de " + cards.length + " gráficos no catálogo" : "";
    vazio.hidden = n > 0;
  }
  document.querySelectorAll(".filtro").forEach(function (bt) {
    bt.addEventListener("click", function () {
      var grupo = bt.dataset.grupo;
      estado[grupo] = bt.dataset.valor;
      document.querySelectorAll('.filtro[data-grupo="' + grupo + '"]').forEach(function (b) {
        b.setAttribute("aria-pressed", String(b === bt));
      });
      aplicaFiltros();
    });
  });
  busca.addEventListener("input", function () { estado.q = busca.value; aplicaFiltros(); });
  busca.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      var alvo = itensNav.filter(function (li) { return !li.hidden && li.classList.contains("n2"); })[0];
      if (alvo) { alvo.querySelector("a").click(); }
    }
    if (e.key === "Escape") { busca.value = ""; estado.q = ""; aplicaFiltros(); }
  });
  function limpaFiltros() {
    estado.sit = "todas"; estado.lib = "todas"; estado.q = ""; busca.value = "";
    document.querySelectorAll(".filtro").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.valor === "todas")); });
    aplicaFiltros();
  }

  /* ------------------------------------------------ links "onde aparece" dos eixos */
  document.querySelectorAll(".mostra-linhas").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var id = a.getAttribute("href").slice(1);
      var alvo = document.getElementById(id);
      if (!alvo) return;
      if (alvo.hidden) limpaFiltros();
      var eixo = a.dataset.axis;
      var sw = alvo.querySelector(".switch");
      if (sw) {
        var visivel = sw.querySelector(".pane:not([hidden]) .codeblock");
        var tem = visivel && (JSON.parse(visivel.dataset.axes || "{}")[eixo] || []).length;
        if (!tem) {
          var paineis = Array.prototype.slice.call(sw.querySelectorAll(":scope > .pane"));
          var idx = paineis.findIndex(function (p) {
            var cb = p.querySelector(".codeblock");
            return cb && (JSON.parse(cb.dataset.axes || "{}")[eixo] || []).length;
          });
          if (idx >= 0) sw._seleciona(idx);
        }
      }
      history.pushState(null, "", "#" + id);
      alvo.scrollIntoView({ behavior: "smooth", block: "start" });
      aplicaEixo(alvo, eixo);
    });
  });

  /* ------------------------------------------------ menu no celular */
  var lateral = document.getElementById("lateral");
  var veu = document.querySelector(".veu");
  var abreMenu = document.querySelector(".abre-menu");
  function menu(abrir) {
    lateral.classList.toggle("aberta", abrir);
    veu.hidden = !abrir;
    abreMenu.setAttribute("aria-expanded", String(abrir));
  }
  abreMenu.addEventListener("click", function () { menu(!lateral.classList.contains("aberta")); });
  veu.addEventListener("click", function () { menu(false); });
  lateral.querySelectorAll(".nav a").forEach(function (a) {
    a.addEventListener("click", function () { if (window.innerWidth <= 960) menu(false); });
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") menu(false); });

  /* ------------------------------------------------ seção ativa na navegação */
  var links = {};
  lateral.querySelectorAll(".nav a").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
  var navCaixa = lateral.querySelector("nav");
  var ultimo = null;
  if ("IntersectionObserver" in window) {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        var a = links[en.target.id];
        if (!a || a === ultimo) return;
        if (ultimo) ultimo.classList.remove("ativo");
        a.classList.add("ativo");
        ultimo = a;
        var topo = a.getBoundingClientRect().top - navCaixa.getBoundingClientRect().top + navCaixa.scrollTop;
        var alto = navCaixa.clientHeight;
        if (topo < navCaixa.scrollTop + 40 || topo > navCaixa.scrollTop + alto - 60) {
          navCaixa.scrollTop = topo - alto / 3;
        }
      });
    }, { rootMargin: "-8% 0px -82% 0px" });
    Object.keys(links).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) obs.observe(el);
    });
  }

  aplicaFiltros();
})();
