/* ============================================================
   DDIA — قارئ الكتب الإلكترونية
   ============================================================ */
(function () {
  "use strict";

  var MD = (window.__BOOK__ || "");
  var contentEl = document.getElementById("content");
  var tocEl = document.getElementById("toc");
  var drawer = document.getElementById("sidebar");
  var scrim = document.getElementById("scrim");
  var STORE = "ddia.reader.v1";

  /* =====================================================
     1. أدوات تنسيق النص
     ===================================================== */
  var AMP = "\uE000", LT = "\uE001", GT = "\uE002";

  function esc(s) {
    return s.replace(/&/g, AMP).replace(/</g, LT).replace(/>/g, GT);
  }
  function unesc(s) {
    return s.split(AMP).join("&amp;").split(LT).join("&lt;").split(GT).join("&gt;");
  }
  function htm(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // مقطع لاتيني: كلمات وحروف فقط — بلا مسافة لاحقة وبلا أقواس أو علامات ترقيم،
  // حتى لا تختلّ ثنائية الاتجاه (bidi) عند حدود النص العربي.
  var LATIN = /[A-Za-z0-9](?:[A-Za-z0-9_+#\-]|\.(?=[A-Za-z0-9]))*(?:[ \t]+[A-Za-z0-9](?:[A-Za-z0-9_+#\-]|\.(?=[A-Za-z0-9]))*)*/g;

  function wrapLatin(text) {
    return text.replace(LATIN, function (m) {
      if (!/[A-Za-z]{2,}/.test(m)) return m;
      return '<span class="lat">' + m + "</span>";
    });
  }

  var REFMARK = /\[(\d+(?:\s*,\s*\d+)*)\]/g;
  var ARRUN = /[\u0600-\u06FF][\u0600-\u06FF\u00A0-\u00FF\u2010-\u206F]*/g;

  function wrapArabic(text) {
    return text.replace(ARRUN, function (m) {
      if (!/[\u0600-\u06FF]/.test(m)) return m;
      return '<span class="ar">' + m + "</span>";
    });
  }

  function inline(src, ltr) {
    var stash = [];
    function keep(html) {
      stash.push(html);
      return "\u0001" + (stash.length - 1) + "\u0001";
    }

    var out = src.replace(/`([^`]+)`/g, function (_, c) {
      return keep("<code>" + esc(c) + "</code>");
    });
    out = out.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (_, t, u) {
      return keep('<a href="' + u + '" target="_blank" rel="noopener">' + esc(t) + "</a>");
    });
    out = out.replace(/(^|[\s(])(https?:\/\/[^\s<>()]+)/g, function (_, pre, u) {
      return pre + keep('<a href="' + u + '" target="_blank" rel="noopener">' + esc(u) + "</a>");
    });
    out = out.replace(/\*\*([^*]+)\*\*/g, function (_, t) {
      return keep("<strong>" + esc(t) + "</strong>");
    });
    out = out.replace(/(^|[\s(])\*([^*\n]+)\*(?=[\s).,،:؛؟!]|$)/g, function (_, pre, t) {
      return pre + keep("<em>" + esc(t) + "</em>");
    });

    out = esc(out);
    out = wrapLatin(out);
    if (ltr) out = wrapArabic(out);
    // العلامات المرجعية [12] / [3, 4] → أرقام مرجعية مرتفعة
    out = out.replace(REFMARK, function (m, nums) {
      return '<sup class="refmark">' + nums.replace(/\s+/g, "") + "</sup>";
    });
    out = out.replace(/\u0001(\d+)\u0001/g, function (_, i) { return stash[+i]; });
    return unesc(out);
  }

  /* =====================================================
     2. كشف الشيفرة ولغتها
     ===================================================== */
  var LANG_RULES = [
    ["sql", /^\s*(SELECT|INSERT\s+INTO|UPDATE\b|DELETE\s+FROM|CREATE\s+(TABLE|INDEX|VIEW)|ALTER\s+TABLE|DROP\s+TABLE|WITH\b|BEGIN\s+TRANSACTION|COMMIT\b|ROLLBACK\b|EXPLAIN\b)/i],
    ["cypher", /^\s*(MATCH\s*\(|RETURN\s|OPTIONAL\s+MATCH|CREATE\s*\()|\)\s*-\[:/i],
    ["sparql", /^\s*(PREFIX\b|BASE\b|SELECT\s+\??\w+\s+WHERE|ASK\s*\{)/i],
    ["turtle", /^\s*(@prefix|@base|_:\w+\s|a\s+:\w+)/i],
    ["datalog", /(^|\s):-/],
    ["prolog", /:-/],
    ["python", /^\s*(def\s+\w+\s*\(|import\s+\w+|from\s+\w+\s+import|print\()/i],
    ["ruby", /^\s*(def\s+\w+|end\b|\w+\.each\s+do\s*\||puts\s|require\s)/i],
    ["javascript", /^\s*(function\s*\w*\s*\(|var\s+\w+|let\s+\w+|const\s+\w+|=>|\w+\s*=\s*function)/i],
    ["avro", /^\s*(\{\s*"type"\s*:\s*"record"|record\s+\w+\s*\{)/i],
    ["thrift", /^\s*(struct\s+\w+\s*\{|message\s+\w+\s*\{)/i],
    ["json", /^\s*[{[]/],
    ["shell", /^\s*(\$\s|#\s*!|!\/bin\/|\w+\s+-\w+\s|\|\s*\w+)/],
    ["html", /^\s*<\/?[a-zA-Z!]/],
    ["css", /\{[^}]*:[^}]*;?\s*\}\s*$/],
  ];

  function detectLang(code) {
    var head = code.split("\n").slice(0, 6).join("\n");
    for (var i = 0; i < LANG_RULES.length; i++) {
      if (LANG_RULES[i][1].test(head)) return LANG_RULES[i][0];
    }
    if (/\bfunction\b|=>|\bvar\b|\blet\b|\bconst\b/.test(head)) return "javascript";
    if (/\bdef\b|\bself\b|puts\b/.test(head)) return "ruby";
    if (/\bSELECT\b|\bFROM\b|\bWHERE\b/i.test(head)) return "sql";
    if (/\bfunction\b|\bclass\b|\bpublic\b|\bvoid\b/.test(head)) return "java";
    return "text";
  }

  var KEYWORDS = {
    sql: "select|from|where|insert|into|values|update|set|delete|create|table|index|primary|key|foreign|references|not|null|and|or|order|by|group|having|join|left|right|inner|outer|on|as|distinct|case|when|then|else|end|union|all|count|sum|avg|min|max|begin|commit|rollback|transaction|isolation|level|serializable|repeatable|read|committed|uncommitted|explain|alter|drop|add|column|default|cast|coalesce|exists|any|some|asc|desc|limit|offset|using|returning|check|constraint|with|recursive|over|partition|wINDOW",
    javascript: "function|var|let|const|return|if|else|for|while|do|break|continue|new|class|extends|super|this|typeof|instanceof|async|await|try|catch|finally|throw|switch|case|default|delete|in|of|null|undefined|true|false|import|export|from|as",
    python: "def|class|return|if|elif|else|for|while|import|from|as|try|except|finally|raise|with|lambda|yield|pass|break|continue|global|nonlocal|assert|del|in|is|not|and|or|None|True|False|self",
    ruby: "def|class|module|end|do|if|elsif|else|unless|while|until|for|in|return|yield|begin|rescue|ensure|raise|require|require_relative|attr_accessor|attr_reader|attr_writer|nil|true|false|self|super|then|next|break|redo|retry|case|when|puts|print|lambda|proc|each|map|select|reject|reduce",
    shell: "if|then|else|elif|fi|for|while|do|done|case|esac|function|return|export|local|echo|cd|ls|grep|sed|awk|cat|curl|git|make|npm|docker|kubectl|set|unset|source|exit",
    cypher: "match|optional|where|return|with|unwind|create|merge|set|delete|remove|order|by|skip|limit|distinct|as|and|or|not|in|is|null|true|false|starts|ends|contains|call|yield|foreach|begin|commit|rollback",
    sparql: "prefix|base|select|distinct|reduced|where|graph|filter|optional|union|minus|bind|values|order|by|limit|offset|group|having|construct|ask|describe",
    java: "public|private|protected|class|interface|extends|implements|static|final|void|int|long|double|boolean|char|new|return|if|else|for|while|do|switch|case|default|break|continue|try|catch|finally|throw|throws|import|package|this|super|null|true|false|abstract|synchronized|volatile|transient|instanceof",
    json: "true|false|null",
    turtle: "a|@prefix|@base|true|false",
    datalog: "name|type|within|edge|relation|true|false",
    prolog: "name|type|edge|within|true|false",
    avro: "record|enum|array|map|union|required|optional|namespace|type|fields|name|default",
    thrift: "struct|union|exception|service|enum|typedef|required|optional|list|map|set|bool|i8|i16|i32|i64|double|string|binary",
    css: "background|color|display|font|margin|padding|border|width|height|list-style|content|position|top|left|right|bottom",
  };

  var COMMENTS = {
    sql: { line: "--", block: null },
    python: { line: "#", block: null },
    ruby: { line: "#", block: null },
    shell: { line: "#", block: null },
    javascript: { line: "//", block: ["/*", "*/"] },
    java: { line: "//", block: ["/*", "*/"] },
    cypher: { line: "//", block: ["/*", "*/"] },
    sparql: { line: "#", block: null },
    css: { line: null, block: ["/*", "*/"] },
    html: { line: null, block: ["<!--", "-->"] },
    json: { line: null, block: null },
    turtle: { line: "#", block: null },
    datalog: { line: "%", block: null },
    prolog: { line: "%", block: null },
    avro: { line: null, block: null },
    thrift: { line: null, block: null },
    css: { line: null, block: ["/*", "*/"] },
    text: { line: null, block: null },
  };

  var KW_RE = {};
  function kwRe(lang) {
    if (KW_RE[lang]) return KW_RE[lang];
    var kws = (KEYWORDS[lang] || "").split("|").filter(Boolean);
    KW_RE[lang] = kws.length
      ? new RegExp("\\b(" + kws.join("|") + ")\\b", "gi")
      : /(?!)()\B/g;
    return KW_RE[lang];
  }

  /** تلوين شيفرة مبسّط: تعليقات / نصوص / أرقام / كلمات مفتاحية */
  function highlight(code, lang) {
    var cm = COMMENTS[lang] || COMMENTS.text;
    var parts = [];
    var re = /[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|`(?:\\.|[^`\\])*`/g;
    var i = 0, m;

    function flush(txt) { if (txt) parts.push(htm(txt)); }

    while ((m = re.exec(code)) !== null) {
      var tok = m[0];
      var start = m.index;
      // هل الكود قبل هذا الرمز تعليق؟
      var chunk = code.slice(i, start);
      if (cm.line) {
        var li = chunk.lastIndexOf(cm.line);
        if (li !== -1 && chunk.indexOf("\n", li) === -1) {
          flush(chunk.slice(0, li));
          parts.push('<span class="c">' + htm(chunk.slice(li)) + "</span>");
          chunk = "";
        }
      }
      flush(chunk);

      if (cm.block && code.slice(Math.max(0, start - 2), start) === cm.block[0].slice(-2)) {
        // داخل كتلة تعليق
        var end = code.indexOf(cm.block[1], start);
        if (end === -1) end = code.length;
        parts.push('<span class="c">' + htm(code.slice(start, end + cm.block[1].length)) + "</span>");
        re.lastIndex = end + cm.block[1].length;
        i = re.lastIndex;
        continue;
      }
      if (cm.line && code.slice(Math.max(0, start - cm.line.length), start) === cm.line) {
        var eol = code.indexOf("\n", start);
        if (eol === -1) eol = code.length;
        parts.push('<span class="c">' + htm(code.slice(start, eol)) + "</span>");
        re.lastIndex = eol;
        i = eol;
        continue;
      }
      if (/^['"`]/.test(tok)) {
        parts.push('<span class="s">' + htm(tok) + "</span>");
      } else if (/^\d/.test(tok)) {
        parts.push('<span class="n">' + htm(tok) + "</span>");
      } else {
        var kw = kwRe(lang);
        kw.lastIndex = 0;
        parts.push(kw.test(tok) ? '<span class="k">' + htm(tok) + "</span>" : htm(tok));
      }
      i = start + tok.length;
    }
    flush(code.slice(i));
    return parts.join("");
  }

  var CODE_KW = /\b(SELECT|INSERT\s+INTO|UPDATE|DELETE\s+FROM|CREATE|ALTER|DROP|WITH|BEGIN|COMMIT|ROLLBACK|EXPLAIN|MATCH|RETURN|PREFIX|DEFINE|CLASS|FUNCTION|VAR|LET|CONST|DEF|END|RETURN|IF|ELSE|FOR|WHILE|IMPORT|REQUIRE|PACKAGE|PUBLIC|PRIVATE|VOID|INT|NEW|TRY|CATCH|THROW|PRINT|ECHO)\b/gi;
  var CODE_SYM = /[{}()\[\];=<>|&]/g;

  function isCode(s) {
    if (!s) return false;
    if (/[\u0600-\u06FF]/.test(s)) return false;      // فيه عربي ⇒ ليس شيفرة
    if (/^\s*—/.test(s)) return false;                 // نسب الاقتباس
    if (/^!/.test(s)) return true;                      // shebang
    if (/<[a-zA-Z!]/.test(s)) return true;              // HTML / XML
    if (/^\s*(--|\/\/|\*\s|#\s)/.test(s)) return true;   // تعليق
    var sym = (s.match(CODE_SYM) || []).length;
    var kw = (s.match(CODE_KW) || []).length;
    if (sym < 2 && kw === 0) return false;
    if (s.length < 12 && !/[=;{}]/.test(s)) return false;
    var ascii = 0;
    for (var i = 0; i < s.length; i++) if (s.charCodeAt(i) < 128) ascii++;
    return ascii / s.length > 0.8;
  }

  /* =====================================================
     3. المحوّل من Markdown إلى HTML
     ===================================================== */
  var headingId = 0;

  function render(md) {
    var lines = md.split("\n");
    var html = [];
    var i = 0, n = lines.length;
    var codeBuf = [];
    var inChapter = false, inPart = false, partNo = 0, coverParts = [];

    function flushCode() {
      if (!codeBuf.length) return;
      var code = codeBuf.join("\n");
      codeBuf = [];
      var lang = detectLang(code);
      html.push(
        '<figure class="codeblock" data-lang="' + lang + '">' +
          '<figcaption class="code-head"><span class="code-lang">' + lang + "</span>" +
          '<button class="code-copy" type="button" aria-label="نسخ الشيفرة">' +
          '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>' +
          "<span>نسخ</span></button></figcaption>" +
          '<pre dir="ltr"><code>' + highlight(code, lang) + "</code></pre>" +
        "</figure>"
      );
    }

    function flushPara(buf) {
      if (!buf.length) return;
      var t = buf.join(" ");
      var isRef = /^\[\d+\]/.test(t.trim());
      html.push(isRef
        ? '<p class="ref" dir="ltr">' + inline(t, true) + "</p>"
        : "<p>" + inline(t) + "</p>");
    }

    while (i < n) {
      var s = lines[i].trim();

      if (!s) { i++; continue; }

      var pm = s.match(/^<!--\s*page\s+(\d+)\s*-->$/);
      if (pm) {
        flushCode();
        html.push('<div class="pagenum" data-page="' + pm[1] + '">' + pm[1] + "</div>");
        i++;
        continue;
      }

      if (s.indexOf("<table>") === 0) {
        flushCode();
        var tbl = [];
        while (i < n) {
          tbl.push(lines[i]);
          if (lines[i].trim().slice(-8) === "</table>") { i++; break; }
          i++;
        }
        html.push('<div class="figure">' + tbl.join("\n") + "</div>");
        continue;
      }

      if (/^#+$/.test(s)) { i++; continue; }

      var kind = "", chapNum = 0;
      var mk = s.match(/^(CHAPTER|PART)([0-9]*)\|(.*)$/);
      if (mk) { kind = mk[1]; chapNum = parseInt(mk[2], 10) || 0; s = mk[3].trim(); }
      var hm = s.match(/^(#{1,6})\s+(.*)$/);
      if (hm) {
        flushCode();
        var lvl = Math.min(hm[1].length, 4);
        var txt = hm[2].trim();
        if (isCode(txt)) {
          codeBuf.push(txt);
        } else {
          var cls = kind ? ' class="' + kind.toLowerCase() + '"' : "";
          if (kind === "CHAPTER") {
            if (inChapter) html.push("</section>");
            html.push('<section class="chapter" data-ch="' + chapNum + '">');
            inChapter = true;
            html.push('<div class="chapter-eyebrow"><span>الفصل ' + chapNum + "</span></div>");
          } else if (kind === "PART") {
            if (inChapter) { html.push("</section>"); inChapter = false; }
            html.push('<section class="partband" data-part="' + (partNo++) + '">');
            inPart = true;
          }
          var hid = "h" + (headingId++);
          var pg = "";
          var pj = i + 1;
          while (pj < n && !lines[pj].trim()) pj++;
          if (pj < n && lines[pj].trim().indexOf("PAGENO|") === 0) {
            pg = lines[pj].trim().slice(7).trim();
            i = pj;
          }
          html.push("<h" + lvl + cls + ' id="' + hid + '"' +
                    (pg ? ' data-page="' + pg + '"' : "") + ">" + inline(txt) + "</h" + lvl + ">");
          if (inPart && lvl > 1) { html.push("</section>"); inPart = false; }
        }
        i++;
        continue;
      }

      if (s.indexOf("FIGIMG|") === 0) {
        flushCode();
        var ffile = s.slice(7).trim();
        var cap = "";
        var j = i + 1;
        while (j < n && !lines[j].trim()) j++;
        if (j < n && lines[j].trim().indexOf("FIGCAP|") === 0) {
          cap = lines[j].trim().slice(7).trim();
          i = j;
        }
        var alt = cap.replace(/^الشكل\s*[\d–\-]+\.?\s*/, "");
        html.push('<figure class="fig">' +
          '<a class="fig-zoom" href="assets/figures/' + ffile + '" target="_blank" rel="noopener" title="اضغط للتكبير">' +
          '<img src="assets/figures/' + ffile + '" alt="' + htm(alt) + '" loading="lazy" decoding="async"></a>' +
          (cap ? "<figcaption>" + inline(cap) + "</figcaption>" : "") +
          "</figure>");
        i++;
        continue;
      }

      if (s.indexOf("TOCPAGE|") === 0) {
        flushCode();
        html.push('<section class="tocpage" id="tocpage"></section>');
        i++;
        continue;
      }

      if (s.indexOf("COVER|") === 0) {
        flushCode();
        var cv = s.slice(6).trim();
        coverParts.push(cv);
        if (coverParts.length === 1) {
          html.push('<section class="coverpage">');
          html.push('<h2 class="cover-t">' + inline(cv) + "</h2>");
        } else if (coverParts.length === 2) {
          html.push('<p class="cover-s">' + inline(cv) + "</p>");
        } else {
          html.push('<p class="cover-a">' + inline(cv) + "</p>");
          html.push("</section>");
        }
        i++;
        continue;
      }

      if (s.indexOf("LBL4|") === 0) {
        var lblTxt = s.slice(5);
        if (isCode(lblTxt)) {
          codeBuf.push(lblTxt);
        } else {
          flushCode();
          html.push('<p class="label4">' + inline(lblTxt) + "</p>");
        }
        i++;
        continue;
      }

      if (s.indexOf("FIGTXT|") === 0) {
        flushCode();
        html.push('<div class="figtxt">' + inline(s.slice(7)) + "</div>");
        i++;
        continue;
      }

      if (s.indexOf("RUNFOOT|") === 0) {
        flushCode();
        html.push('<div class="runfoot">' + inline(s.slice(8)) + "</div>");
        i++;
        continue;
      }

      if (s.indexOf("FIGCAP|") === 0) {
        flushCode();
        html.push('<div class="figcap">' + inline(s.slice(7)) + "</div>");
        i++;
        continue;
      }

      if (s.indexOf("EPIATTR|") === 0) {
        flushCode();
        var attr = inline(s.slice(8));
        var prev = html.pop();
        if (prev && prev.charAt(0) === "<" && prev.indexOf("<p>") === 0 && prev.slice(-4) === "</p>") {
          html.push('<blockquote class="epigraph">' + prev + "<footer>" + attr + "</footer></blockquote>");
        } else {
          if (prev) html.push(prev);
          html.push('<div class="epigraph-attrib">' + attr + "</div>");
        }
        i++;
        continue;
      }

      if (s.charAt(0) === "•") {
        flushCode();
        var ul = [];
        while (i < n && lines[i].trim().charAt(0) === "•") {
          ul.push("<li>" + inline(lines[i].trim().slice(1).trim()) + "</li>");
          i++;
        }
        html.push("<ul>" + ul.join("") + "</ul>");
        continue;
      }

      if (/^\d+\.\s/.test(s)) {
        flushCode();
        var ol = [];
        while (i < n && /^\d+\.\s/.test(lines[i].trim())) {
          ol.push("<li>" + inline(lines[i].trim().replace(/^\d+\.\s*/, "")) + "</li>");
          i++;
        }
        html.push("<ol>" + ol.join("") + "</ol>");
        continue;
      }

      var para = [];
      while (i < n) {
        var t = lines[i].trim();
        if (!t || t.charAt(0) === "•" || /^#{1,6}\s/.test(t) ||
            /^\d+\.\s/.test(t) || t.indexOf("<table>") === 0 ||
            /^(FIGTXT|RUNFOOT|FIGCAP|FIGIMG|LBL4|EPIATTR)\|/.test(t) ||
            /^<!--\s*page\s+\d+\s*-->$/.test(t)) break;
        para.push(t);
        i++;
      }
      if (para.length && isCode(para[0])) {
        for (var q = 0; q < para.length; q++) codeBuf.push(para[q]);
      } else {
        flushCode();
        flushPara(para);
      }
    }
    flushCode();
    if (inChapter) html.push("</section>");
    else if (inPart) html.push("</section>");
    return html.join("\n");
  }

  /* =====================================================
     4. الإعدادات
     ===================================================== */
  var settings = {
    theme: "light", font: "naskh", scale: 100,
    numbers: true, justify: false, lh: 1.95, width: 40
  };
  try {
    var raw = localStorage.getItem(STORE);
    if (raw) Object.assign(settings, JSON.parse(raw));
  } catch (e) {}

  function save() { try { localStorage.setItem(STORE, JSON.stringify(settings)); } catch (e) {} }

  var FONTS = {
    naskh: "'Noto Naskh Arabic', 'Amiri', Georgia, serif",
    cairo: "'Cairo', 'Noto Naskh Arabic', system-ui, sans-serif",
    amiri: "'Amiri', 'Noto Naskh Arabic', Georgia, serif"
  };

  function applySettings() {
    var r = document.documentElement;
    r.setAttribute("data-theme", settings.theme);
    r.style.setProperty("--font-body", FONTS[settings.font] || FONTS.naskh);
    r.style.setProperty("--fs", (19 * settings.scale / 100).toFixed(2) + "px");
    r.style.setProperty("--lh", String(settings.lh));
    r.style.setProperty("--measure", settings.width + "rem");
    document.body.classList.toggle("no-numbers", !settings.numbers);
    document.body.classList.toggle("justify", settings.justify);
    var lbl = document.getElementById("fsLabel");
    if (lbl) lbl.textContent = settings.scale + "%";
    var lhLbl = document.getElementById("lhLabel");
    if (lhLbl) lhLbl.textContent = settings.lh.toFixed(2);
    var wLbl = document.getElementById("wLabel");
    if (wLbl) wLbl.textContent = settings.width + "rem";
    save();
  }

  (function readQuery() {
    var q = new URLSearchParams(location.search);
    var t = q.get("theme");
    if (t && ["light", "mid", "cream", "dark"].indexOf(t) !== -1) settings.theme = t;
    var f = q.get("font");
    if (f && FONTS[f]) settings.font = f;
    var s = parseInt(q.get("scale"), 10);
    if (s >= 70 && s <= 150) settings.scale = s;
    if (q.get("numbers") === "0") settings.numbers = false;
    if (q.get("justify") === "1") settings.justify = true;
  })();

  /* =====================================================
     5. الفهرس الجانبي
     ===================================================== */
  var headings = [];
  var chapters = [];

  function buildToc() {
    var html = [], inChapter = false;
    headings = []; chapters = [];
    var nodes = contentEl.querySelectorAll("h1, h2, h3");
    for (var k = 0; k < nodes.length; k++) {
      var h = nodes[k];
      var lvl = parseInt(h.tagName[1], 10);
      var text = h.textContent.trim();
      headings.push({ el: h, level: lvl, text: text });
      if (lvl === 1) {
        if (h.classList.contains("chapter")) chapters.push({ el: h, text: text });
        if (h.classList.contains("part")) {
          html.push('<li class="toc-part"><span>' + text + "</span></li>");
          continue;
        }
        var ch = h.closest(".chapter");
        var chAttr = ch ? ' data-ch="' + ch.getAttribute("data-ch") + '"' : "";
        html.push('<li class="toc-chapter">');
        html.push('<a class="lvl-1"' + chAttr + ' href="#' + h.id + '" data-t="' + h.id + '">' + text + "</a>");
        html.push('<ul class="toc-sub">');
        inChapter = true;
        continue;
      }
      if (lvl === 2) {
        html.push('<li><a class="lvl-2" href="#' + h.id + '" data-t="' + h.id + '">' + text + "</a></li>");
      } else if (lvl === 3) {
        html.push('<li><a class="lvl-3" href="#' + h.id + '" data-t="' + h.id + '">' + text + "</a></li>");
      }
    }
    if (inChapter) html.push("</ul></li>");
    tocEl.innerHTML = html.join("");
  }

  /* =====================================================
     5b. صفحة الفهرس التفاعلية داخل المتن
     ===================================================== */
  function buildTocPage() {
    var host = document.getElementById("tocpage");
    if (!host) return;
    var html = [];
    var open = false;
    var nodes = contentEl.querySelectorAll("h1, h2");
    for (var i = 0; i < nodes.length; i++) {
      var h = nodes[i];
      var lvl = parseInt(h.tagName[1], 10);
      var txt = h.textContent.trim();
      var pg = h.getAttribute("data-page");
      if (pg && parseInt(pg, 10) <= 0) pg = "";
      if (lvl === 1) {
        if (open) { html.push("</div>"); open = false; }
        if (h.classList.contains("part")) {
          html.push('<div class="tp-part">' + txt + "</div>");
          continue;
        }
        if (!h.classList.contains("chapter")) continue;   // العناوين الجبهية فقط
        var ch = h.closest(".chapter");
        var acc = ch ? ch.getAttribute("data-ch") : "";
        html.push('<a class="tp-ch" data-ch="' + (acc || "") + '" href="#' + h.id + '">' +
                  '<span class="tp-ch-t">' + txt + "</span>" +
                  (pg ? '<span class="tp-pg">' + pg + "</span>" : "") + "</a>");
        html.push('<div class="tp-sec">');
        open = true;
        continue;
      }
      if (!open) { html.push('<div class="tp-sec">'); open = true; }
      html.push('<a class="tp-s" href="#' + h.id + '">' + txt +
                (pg ? '<span class="tp-pg">' + pg + "</span>" : "") + "</a>");
    }
    if (open) html.push("</div>");
    host.innerHTML = html.join("");
  }

  /* =====================================================
     6. الدرج (فهرس المحتويات)
     ===================================================== */
  var navToggle = document.getElementById("navToggle");

  function openDrawer() {
    drawer.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    navToggle.setAttribute("aria-expanded", "true");
    scrim.hidden = false;
    requestAnimationFrame(function () { scrim.classList.add("show"); });
  }
  function closeDrawer() {
    drawer.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    navToggle.setAttribute("aria-expanded", "false");
    scrim.classList.remove("show");
    setTimeout(function () { scrim.hidden = true; }, 260);
  }
  function toggleDrawer() {
    if (drawer.classList.contains("open")) closeDrawer(); else openDrawer();
  }

  navToggle.addEventListener("click", toggleDrawer);
  scrim.addEventListener("click", closeDrawer);
  document.getElementById("drawerClose").addEventListener("click", closeDrawer);

  tocEl.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[data-t]") : null;
    if (!a) return;
    var target = document.getElementById(a.getAttribute("data-t"));
    if (!target) return;
    e.preventDefault();
    var top = target.getBoundingClientRect().top + window.scrollY - 80;
    window.scrollTo({ top: top, behavior: "smooth" });
    history.replaceState(null, "", "#" + a.getAttribute("data-t"));
    a.classList.add("active");
    if (window.innerWidth < 960) closeDrawer();
  });

  document.getElementById("tocFilter").addEventListener("input", function (e) {
    var v = e.target.value.trim().toLowerCase();
    Array.prototype.forEach.call(tocEl.querySelectorAll("a"), function (a) {
      var hit = !v || a.textContent.toLowerCase().indexOf(v) !== -1;
      a.style.display = hit ? "" : "none";
      var li = a.parentElement;
      if (li && li.tagName === "LI" && !li.classList.contains("toc-chapter")) {
        li.style.display = hit ? "" : "none";
      }
    });
  });

  /* =====================================================
     7. التمرير النشط + الموضع
     ===================================================== */
  var posLabel = document.getElementById("posLabel");
  var pctLabel = document.getElementById("pctLabel");
  var timeLabel = document.getElementById("timeLabel");
  var prevBtn = document.getElementById("prevChapter");
  var nextBtn = document.getElementById("nextChapter");
  var tocLinks = [];
  var prog = document.querySelector("#progress > i");

  function topOf(el) {
    return el.getBoundingClientRect().top + window.scrollY;
  }

  function currentChapterIndex() {
    var idx = 0;
    var y = window.scrollY + 230;
    for (var c = 0; c < chapters.length; c++) {
      if (topOf(chapters[c].el) <= y) idx = c; else break;
    }
    return idx;
  }

  function initSpy() {
    tocLinks = Array.prototype.slice.call(tocEl.querySelectorAll("a[data-t]"));
    var ticking = false;
    function update() {
      var y = window.scrollY + 150, cur = null;
      for (var i = 0; i < headings.length; i++) {
        if (topOf(headings[i].el) <= y) cur = headings[i]; else break;
      }
      tocLinks.forEach(function (a) { a.classList.remove("active"); });
      if (cur) {
        var link = tocEl.querySelector('a[data-t="' + cur.el.id + '"]');
        if (link) {
          link.classList.add("active");
          if (drawer.classList.contains("open")) {
            var lr = link.getBoundingClientRect(), sr = drawer.getBoundingClientRect();
            if (lr.top < sr.top + 60 || lr.bottom > sr.bottom - 20) {
              tocEl.scrollTop += (lr.top - sr.top) - tocEl.clientHeight / 3;
            }
          }
        }
      }
      var idx = currentChapterIndex();
      if (posLabel) posLabel.textContent = chapters[idx] ? chapters[idx].text : (chapters[0] && chapters[0].text) || "";
      // اجعل لون الواجهة يتبع لون الفصل الحالي
      var chap = chapters[idx] && chapters[idx].el.closest(".chapter");
      if (chap) {
        var cs = getComputedStyle(chap);
        var root = document.documentElement.style;
        if (root.getPropertyValue("--chc") !== cs.getPropertyValue("--chc").trim()) {
          root.setProperty("--chc", cs.getPropertyValue("--chc").trim());
          root.setProperty("--chcs", cs.getPropertyValue("--chcs").trim());
          root.setProperty("--chct", cs.getPropertyValue("--chct").trim());
        }
      }
      prevBtn.disabled = idx <= 0;
      nextBtn.disabled = idx >= chapters.length - 1;

      var h = document.documentElement.scrollHeight - window.innerHeight;
      var pct = h > 0 ? Math.min(100, Math.round((window.scrollY / h) * 100)) : 0;
      if (pctLabel) pctLabel.textContent = pct + "%";
      prog.style.width = pct + "%";
      toTop.classList.toggle("show", window.scrollY > 700);
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  prevBtn.addEventListener("click", function () { goChapter(currentChapterIndex() - 1); });
  nextBtn.addEventListener("click", function () { goChapter(currentChapterIndex() + 1); });
  function goChapter(i) {
    var t = chapters[i];
    if (!t) return;
    window.scrollTo({ top: t.el.getBoundingClientRect().top + window.scrollY - 120, behavior: "smooth" });
  }

  document.getElementById("homeLink").addEventListener("click", function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  var startBtn = document.getElementById("startReading");
  if (startBtn) {
    startBtn.addEventListener("click", function () {
      var first = contentEl.querySelector("h1");
      var t = (first ? first.getBoundingClientRect().top : contentEl.getBoundingClientRect().top)
              + window.scrollY - 90;
      window.scrollTo({ top: t, behavior: "smooth" });
    });
  }

  /* =====================================================
     8. البحث
     ===================================================== */
  var marks = [], markIdx = -1;
  var searchBar = document.getElementById("searchBar");
  var searchInput = document.getElementById("searchInput");
  var searchTimer = null;

  function clearMarks() {
    marks.forEach(function (m) {
      var p = m.parentNode;
      if (!p) return;
      while (m.firstChild) p.insertBefore(m.firstChild, m);
      p.removeChild(m);
      p.normalize();
    });
    marks = []; markIdx = -1;
  }

  function doSearch(q) {
    clearMarks();
    if (!q || q.length < 2) {
      document.getElementById("searchCount").textContent = "—";
      return;
    }
    var needle = q.toLowerCase();
    var walker = document.createTreeWalker(contentEl, NodeFilter.SHOW_TEXT, null);
    var nodes = [], node;
    while ((node = walker.nextNode())) {
      var p = node.parentNode.nodeName;
      if (p === "SCRIPT" || p === "STYLE" || p === "MARK") continue;
      if (node.nodeValue.toLowerCase().indexOf(needle) !== -1) nodes.push(node);
    }
    nodes.forEach(function (n) {
      var text = n.nodeValue, low = text.toLowerCase();
      var frag = document.createDocumentFragment();
      var pos = 0, idx;
      while ((idx = low.indexOf(needle, pos)) !== -1) {
        if (idx > pos) frag.appendChild(document.createTextNode(text.slice(pos, idx)));
        var mk = document.createElement("mark");
        mk.textContent = text.slice(idx, idx + q.length);
        frag.appendChild(mk);
        marks.push(mk);
        pos = idx + q.length;
      }
      if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
      n.parentNode.replaceChild(frag, n);
    });
    markIdx = -1;
    document.getElementById("searchCount").textContent = marks.length
      ? ("0 / " + marks.length) : "لا نتائج";
    if (marks.length) gotoMark(0);
  }

  function gotoMark(i) {
    if (!marks.length) return;
    marks.forEach(function (m) { m.classList.remove("current"); });
    markIdx = (i + marks.length) % marks.length;
    var m = marks[markIdx];
    m.classList.add("current");
    var rect = m.getBoundingClientRect();
    if (rect.top < 90 || rect.bottom > window.innerHeight - 60) {
      window.scrollTo({ top: window.scrollY + rect.top - window.innerHeight / 2.5, behavior: "smooth" });
    }
    document.getElementById("searchCount").textContent = (markIdx + 1) + " / " + marks.length;
  }

  function openSearch() {
    searchBar.classList.add("open");
    searchInput.focus(); searchInput.select();
  }
  function closeSearch() {
    searchBar.classList.remove("open");
    clearMarks();
    document.getElementById("searchCount").textContent = "—";
  }
  document.getElementById("searchBtn").addEventListener("click", function () {
    if (searchBar.classList.contains("open")) closeSearch(); else openSearch();
  });
  document.getElementById("searchClose").addEventListener("click", closeSearch);
  document.getElementById("searchNext").addEventListener("click", function () { gotoMark(markIdx + 1); });
  document.getElementById("searchPrev").addEventListener("click", function () { gotoMark(markIdx - 1); });
  searchInput.addEventListener("input", function () {
    clearTimeout(searchTimer);
    var v = searchInput.value;
    searchTimer = setTimeout(function () { doSearch(v); }, 220);
  });
  searchInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") { e.preventDefault(); gotoMark(markIdx + (e.shiftKey ? -1 : 1)); }
    if (e.key === "Escape") { e.preventDefault(); closeSearch(); searchInput.blur(); }
  });

  /* =====================================================
     9. قائمة الإعدادات
     ===================================================== */
  var settingsBtn = document.getElementById("settingsBtn");
  var settingsMenu = document.getElementById("settingsMenu");
  function closeMenu() { settingsMenu.classList.remove("open"); settingsBtn.setAttribute("aria-expanded", "false"); }
  settingsBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    var open = settingsMenu.classList.toggle("open");
    settingsBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  document.addEventListener("click", function (e) {
    if (!settingsMenu.contains(e.target) && e.target !== settingsBtn) closeMenu();
  });

  Array.prototype.forEach.call(settingsMenu.querySelectorAll("[data-theme-opt]"), function (b) {
    b.addEventListener("click", function () {
      settings.theme = b.getAttribute("data-theme-opt");
      applySettings(); syncChecks(); closeMenu();
    });
  });
  Array.prototype.forEach.call(settingsMenu.querySelectorAll("[data-font-opt]"), function (b) {
    b.addEventListener("click", function () {
      settings.font = b.getAttribute("data-font-opt");
      applySettings(); syncChecks(); closeMenu();
    });
  });
  document.getElementById("fsUp").addEventListener("click", function () {
    settings.scale = Math.min(150, settings.scale + 10); applySettings();
  });
  document.getElementById("fsDown").addEventListener("click", function () {
    settings.scale = Math.max(70, settings.scale - 10); applySettings();
  });
  document.getElementById("lhUp").addEventListener("click", function () {
    settings.lh = Math.min(2.4, Math.round((settings.lh + 0.1) * 100) / 100); applySettings();
  });
  document.getElementById("lhDown").addEventListener("click", function () {
    settings.lh = Math.max(1.4, Math.round((settings.lh - 0.1) * 100) / 100); applySettings();
  });
  document.getElementById("wUp").addEventListener("click", function () {
    settings.width = Math.min(58, settings.width + 2); applySettings();
  });
  document.getElementById("wDown").addEventListener("click", function () {
    settings.width = Math.max(30, settings.width - 2); applySettings();
  });
  document.getElementById("toggleNumbers").addEventListener("click", function () {
    settings.numbers = !settings.numbers; applySettings(); syncChecks(); closeMenu();
  });
  document.getElementById("toggleJustify").addEventListener("click", function () {
    settings.justify = !settings.justify; applySettings(); syncChecks(); closeMenu();
  });
  document.getElementById("printBtn").addEventListener("click", function () {
    closeMenu(); window.print();
  });

  function syncChecks() {
    Array.prototype.forEach.call(settingsMenu.querySelectorAll("[data-theme-opt]"), function (b) {
      b.setAttribute("aria-checked", b.getAttribute("data-theme-opt") === settings.theme ? "true" : "false");
    });
    Array.prototype.forEach.call(settingsMenu.querySelectorAll("[data-font-opt]"), function (b) {
      b.setAttribute("aria-checked", b.getAttribute("data-font-opt") === settings.font ? "true" : "false");
    });
    document.getElementById("toggleNumbers").setAttribute("aria-checked", settings.numbers ? "true" : "false");
    document.getElementById("toggleJustify").setAttribute("aria-checked", settings.justify ? "true" : "false");
  }

  /* =====================================================
     10. نسخ الشيفرة
     ===================================================== */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest(".code-copy") : null;
    if (!btn) return;
    var block = btn.closest(".codeblock");
    var code = block ? block.querySelector("pre").textContent : "";
    var done = function () {
      btn.classList.add("ok");
      var lbl = btn.querySelector("span");
      var old = lbl.textContent;
      lbl.textContent = "تم النسخ";
      setTimeout(function () { lbl.textContent = old; btn.classList.remove("ok"); }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(code).then(done, function () { fallbackCopy(code, done); });
    } else {
      fallbackCopy(code, done);
    }
  });

  function fallbackCopy(text, cb) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); cb(); } catch (e) {}
    document.body.removeChild(ta);
  }

  /* =====================================================
     11. تكبير الأشكال
     ===================================================== */
  var lightbox = document.getElementById("lightbox");
  var lightboxImg = document.getElementById("lightboxImg");
  var lightboxCap = document.getElementById("lightboxCap");

  function openLightbox(src, cap) {
    lightboxImg.src = src;
    lightboxImg.alt = cap || "";
    lightboxCap.textContent = cap || "";
    lightbox.hidden = false;
    requestAnimationFrame(function () { lightbox.classList.add("show"); });
    document.body.style.overflow = "hidden";
  }
  function closeLightbox() {
    lightbox.classList.remove("show");
    document.body.style.overflow = "";
    setTimeout(function () { lightbox.hidden = true; lightboxImg.src = ""; }, 240);
  }
  document.addEventListener("click", function (e) {
    var link = e.target.closest ? e.target.closest(".fig-zoom") : null;
    if (link) {
      e.preventDefault();
      var fig = link.closest("figure.fig");
      var cap = fig && fig.querySelector("figcaption") ? fig.querySelector("figcaption").textContent : "";
      openLightbox(link.getAttribute("href"), cap);
    }
  });
  lightbox.addEventListener("click", function (e) {
    if (e.target === lightbox || e.target.closest("#lightboxClose")) closeLightbox();
  });

  /* =====================================================
     12. اختصارات لوحة المفاتيح + المساعدة
     ===================================================== */
  var toTop = document.getElementById("toTop");
  toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

  var help = document.getElementById("help");
  function toggleHelp(force) {
    var on = force !== undefined ? force : help.hidden;
    help.hidden = !on;
    if (on) help.classList.add("show");
  }
  document.getElementById("helpBtn").addEventListener("click", function () { toggleHelp(); });

  document.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    var typing = tag === "input" || tag === "textarea" || e.target.isContentEditable;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "f") { e.preventDefault(); openSearch(); return; }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b") { e.preventDefault(); toggleDrawer(); return; }
    if (typing) return;
    if (e.key === "/") { e.preventDefault(); openSearch(); }
    else if (e.key === "?") { e.preventDefault(); toggleHelp(); }
    else if (e.key === "Escape") { closeSearch(); closeMenu(); toggleHelp(false); closeLightbox(); }
    else if (e.key === "t" || e.key === "ط") {
      var order = ["light", "mid", "cream", "dark"];
      settings.theme = order[(order.indexOf(settings.theme) + 1) % order.length];
      applySettings(); syncChecks();
    }
    else if (e.key === "+" || e.key === "=") { settings.scale = Math.min(150, settings.scale + 10); applySettings(); }
    else if (e.key === "-") { settings.scale = Math.max(70, settings.scale - 10); applySettings(); }
    else if (e.key === "[" || e.key === "]") {
      var i = currentChapterIndex();
      goChapter(e.key === "[" ? i - 1 : i + 1);
    }
  });

  /* =====================================================
     13. استئناف القراءة + وقت القراءة
     ===================================================== */
  var LASTPOS = "ddia.lastpos";
  var restore = true;

  function savePos() {
    try { localStorage.setItem(LASTPOS, String(Math.round(window.scrollY))); } catch (e) {}
  }
  var posTimer = null;
  window.addEventListener("scroll", function () {
    if (posTimer) return;
    posTimer = setTimeout(function () { savePos(); posTimer = null; }, 900);
  }, { passive: true });

  function restorePos() {
    var y = 0;
    try { y = parseInt(localStorage.getItem(LASTPOS) || "0", 10) || 0; } catch (e) {}
    if (y > 400) {
      window.scrollTo(0, y);
      toast("استُؤنف القراءة من موضعك المحفوظ");
    }
  }

  var toastEl = document.getElementById("toast");
  var toastTimer = null;
  function toast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 2600);
  }

  function readingTime() {
    var words = contentEl.textContent.trim().split(/\s+/).length;
    var mins = Math.round(words / 180);
    if (!timeLabel) return;
    if (mins >= 60) {
      var h = Math.floor(mins / 60), m = mins % 60;
      timeLabel.textContent = "≈ " + h + " س" + (m ? " " + m + " د" : "");
    } else {
      timeLabel.textContent = "≈ " + mins + " د";
    }
  }

  /* =====================================================
     14. الإقلاع
     ===================================================== */
  function boot() {
    if (!MD) {
      contentEl.innerHTML = '<p style="text-align:center;color:#b00">تعذّر تحميل محتوى الكتاب.</p>';
      return;
    }
    var t0 = performance.now();
    contentEl.innerHTML = render(MD);
    buildToc();
    buildTocPage();
    buildTocPage();
    initSpy();
    applySettings();
    syncChecks();
    readingTime();
    restorePos();
    console.log("DDIA reader: rendered in", Math.round(performance.now() - t0), "ms,",
                headings.length, "headings,", chapters.length, "chapters,",
                contentEl.querySelectorAll("figure.fig").length, "figures,",
                contentEl.querySelectorAll(".codeblock").length, "code blocks");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
