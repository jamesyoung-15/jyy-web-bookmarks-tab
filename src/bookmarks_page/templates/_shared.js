/* Shared behavior: data access, search, header, theme, keyboard navigation.
   Each layout calls BM.init({ layout, render }) where render(query) draws the
   page and returns the ranked link ids for a non-empty query (or null). */
(function () {
  const data = window.BOOKMARKS;
  const links = Object.values(data.links);
  const LAYOUTS = ["cards", "tiles", "launcher"];

  function esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function hue(s) {
    let h = 0;
    for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 360;
    return h;
  }

  function icon(link, size) {
    const el = document.createElement("span");
    el.className = "ico";
    if (size) { el.style.width = el.style.height = size + "px"; el.style.fontSize = Math.round(size * 0.5) + "px"; }
    if (link.icon) {
      const img = document.createElement("img");
      img.src = link.icon;
      img.alt = "";
      el.appendChild(img);
    } else {
      el.classList.add("letter");
      el.style.setProperty("--hue", hue(link.host || link.title));
      el.textContent = (link.title.match(/[A-Za-z0-9]/) || ["?"])[0].toUpperCase();
    }
    return el;
  }

  /* Search: every token must match somewhere; score favors title hits. */
  function fields(link) {
    return {
      title: link.title.toLowerCase(),
      alias: link.alias.toLowerCase(),
      tags: link.tags.join(" ").toLowerCase(),
      host: link.host.toLowerCase(),
      desc: link.desc.toLowerCase(),
      groups: link.groups.join(" ").toLowerCase(),
    };
  }
  const index = links.map((l) => ({ link: l, f: fields(l) }));

  function tokenScore(f, t) {
    let s = 0;
    if (f.title.startsWith(t)) s = Math.max(s, 100);
    else if (new RegExp("(^|[^a-z0-9])" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(f.title)) s = Math.max(s, 70);
    else if (f.title.includes(t)) s = Math.max(s, 45);
    if (f.alias.includes(t) || f.tags.includes(t)) s = Math.max(s, 60);
    if (f.host.includes(t)) s = Math.max(s, 30);
    if (f.groups.includes(t)) s = Math.max(s, 25);
    if (f.desc.includes(t)) s = Math.max(s, 15);
    return s;
  }

  function search(q) {
    const tokens = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!tokens.length) return [];
    const out = [];
    for (const { link, f } of index) {
      let total = 0;
      for (const t of tokens) {
        const s = tokenScore(f, t);
        if (!s) { total = 0; break; }
        total += s;
      }
      if (total) out.push({ link, score: total });
    }
    out.sort((a, b) => b.score - a.score || a.link.title.localeCompare(b.link.title));
    return out;
  }

  function highlight(text, q) {
    const tokens = q.toLowerCase().split(/\s+/).filter(Boolean);
    let html = esc(text);
    if (!tokens.length) return html;
    const re = new RegExp("(" + tokens.map((t) => esc(t).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|") + ")", "gi");
    return html.replace(re, "<mark>$1</mark>");
  }

  /* Theme: auto (OS) -> light -> dark, remembered per browser. */
  const THEME_KEY = "bm-theme";
  function getTheme() { try { return localStorage.getItem(THEME_KEY) || "auto"; } catch (e) { return "auto"; } }
  function applyTheme(t) {
    if (t === "auto") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", t);
    const btn = document.getElementById("theme-btn");
    if (btn) btn.textContent = "Theme: " + t;
  }
  function cycleTheme() {
    const order = ["auto", "light", "dark"];
    const next = order[(order.indexOf(getTheme()) + 1) % order.length];
    try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
    applyTheme(next);
  }

  function startClock() {
    const t = document.getElementById("clock-time");
    const d = document.getElementById("clock-date");
    const tick = () => {
      const now = new Date();
      t.textContent = now.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
      d.textContent = now.toLocaleDateString([], { weekday: "long", month: "long", day: "numeric" });
    };
    tick();
    setInterval(tick, 10000);
  }

  function header(layout) {
    const top = document.getElementById("top");
    top.className = "top";
    top.innerHTML =
      '<div class="clock"><span class="clock-time" id="clock-time"></span><span class="clock-date" id="clock-date"></span></div>' +
      '<label class="search"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input id="q" type="search" placeholder="Search links, descriptions, tags" autocomplete="off" spellcheck="false" aria-label="Search bookmarks">' +
      '<span class="kbd">/</span></label>' +
      '<button class="icon-btn" id="theme-btn" type="button"></button>';
    document.getElementById("theme-btn").addEventListener("click", cycleTheme);

    const foot = document.getElementById("foot");
    foot.className = "foot";
    foot.innerHTML =
      "<span>Layout: " +
      LAYOUTS.map((l) => '<a href="' + l + '.html"' + (l === layout ? ' aria-current="page"' : "") + ">" + l + "</a>").join(" ") +
      "</span><span>" + links.length + " links, built " + esc(data.generated.replace("T", " ")) + " from " + esc(data.source) + "</span>" +
      "<span>Keys: / search, Enter open top match, arrows move, Esc clear</span>";
  }

  /* Arrow keys move to the nearest visible link in that direction. */
  function visibleLinks() {
    return [...document.querySelectorAll(".bm-link")].filter((el) => el.offsetParent !== null);
  }
  function moveFocus(from, dir) {
    const els = visibleLinks();
    if (!els.length) return;
    if (!from || !els.includes(from)) { els[0].focus(); return; }
    const a = from.getBoundingClientRect();
    const ax = a.left + a.width / 2, ay = a.top + a.height / 2;
    let best = null, bestScore = Infinity;
    for (const el of els) {
      if (el === from) continue;
      const b = el.getBoundingClientRect();
      const dx = b.left + b.width / 2 - ax, dy = b.top + b.height / 2 - ay;
      const along = dir === "ArrowRight" ? dx : dir === "ArrowLeft" ? -dx : dir === "ArrowDown" ? dy : -dy;
      const across = dir === "ArrowRight" || dir === "ArrowLeft" ? Math.abs(dy) : Math.abs(dx);
      if (along <= 1) continue;
      const score = along + across * 3;
      if (score < bestScore) { bestScore = score; best = el; }
    }
    if (best) best.focus();
  }

  function open(url, newTab) {
    if (newTab) window.open(url, "_blank", "noopener");
    else window.location.href = url;
  }

  function init({ layout, render }) {
    header(layout);
    applyTheme(getTheme());
    startClock();
    const input = document.getElementById("q");
    let ranked = null;

    function update() {
      const q = input.value.trim();
      ranked = render(q);
      document.querySelectorAll(".bm-link.is-top").forEach((el) => el.classList.remove("is-top"));
      if (ranked && ranked.length) {
        const el = visibleLinks().find((e) => e.dataset.id === ranked[0]);
        if (el) el.classList.add("is-top");
      }
    }
    input.addEventListener("input", update);

    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && ranked && ranked.length) {
        e.preventDefault();
        open(data.links[ranked[0]].url, e.ctrlKey || e.metaKey);
      } else if (e.key === "Escape") {
        input.value = "";
        update();
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        const top = document.querySelector(".bm-link.is-top") || visibleLinks()[0];
        if (top) top.focus();
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.target === input || e.altKey || e.ctrlKey || e.metaKey) return;
      if (e.key === "/") { e.preventDefault(); input.focus(); input.select(); return; }
      if (e.key === "Escape") { input.value = ""; update(); input.focus(); return; }
      if (e.key.startsWith("Arrow") && document.activeElement.classList.contains("bm-link")) {
        e.preventDefault();
        moveFocus(document.activeElement, e.key);
        return;
      }
      // Typing anywhere goes to the search box.
      if (e.key.length === 1 && /\S/.test(e.key)) { input.focus(); }
    });

    // ?q=term prefills the search, so the page can double as a Chrome site search.
    const preset = new URLSearchParams(location.search).get("q");
    if (preset) input.value = preset;
    update();
    input.focus();
  }

  window.BM = { data, links, esc, icon, search, highlight, init };
})();
