/* legacy.js - very old tablets (first iPad on iOS 5, old Android tablets).
 * Their browsers have no CSS variables, no modern flexbox and no vw / vh / calc, so the normal layout
 * cannot work. Here the page gets the class "legacy" plus legacy.css, and the app is laid out with plain
 * pixel positions. Only the on-screen keys ("No piano") are offered there (no microphone access).
 * Plain old JavaScript on purpose; loaded in <head> before the app. Test on a new browser: /?legacy=1
 */
(function () {
  var d = document, root = d.documentElement, w = window, modern = false;
  try { modern = !!(w.CSS && CSS.supports && CSS.supports("--a", "0")); } catch (e) {}
  if (/[?&]legacy=1/.test(location.search)) modern = false;
  if (modern) return;
  root.className += " legacy";
  d.write('<link rel="stylesheet" href="legacy.css">');

  function q(sel) { return d.querySelector(sel); }
  function place(el, box) {
    if (!el) return;
    for (var k in box) if (box.hasOwnProperty(k)) el.style[k] = Math.round(box[k]) + "px";
  }
  function layout() {
    var app = d.getElementById("app"), keys = d.getElementById("keys");
    if (!app || !keys) return;
    var vw = w.innerWidth, vh = w.innerHeight, turn = vh > vw;       // portrait: turn the app into landscape
    var W = turn ? vh : vw, H = turn ? vw : vh;
    place(app, { left: 0, top: 0, width: W, height: H });
    var t = turn ? "translate(" + vw + "px,0) rotate(90deg)" : "none";
    app.style.webkitTransformOrigin = "0 0"; app.style.transformOrigin = "0 0";
    app.style.webkitTransform = t; app.style.transform = t;

    var pad = Math.max(6, Math.round(Math.min(W, H) * 0.015));
    var topH = Math.round(H * 0.36);
    place(q(".top"), { left: 0, top: 0, width: W, height: topH });
    var nh = topH - 2 * pad, nw = Math.min(W * 0.52, nh * 2.05);
    place(q("#now"), { left: pad, top: pad, width: nw, height: nh });
    var inner = nh - 6, s = inner - 2 * pad;                          // 3 px card border
    place(q(".now-staff"), { left: pad, top: pad, width: s, height: s });
    place(q(".now-key-wrap"), { left: nw - 6 - pad - s, top: pad, width: s, height: s });
    var gapX = nw - 6 - 2 * pad - 2 * s;
    place(q(".now-arrow"), { left: pad + s + gapX / 2 - 12, top: pad + s / 2 - 12, width: 24, height: 24 });
    place(q(".bar"), { right: pad, top: pad, width: W - nw - 3 * pad });

    var kw = W - 2 * pad, kh = H - topH - pad - 8;
    place(keys, { left: pad, top: topH, width: kw, height: kh });
    var whites = keys.querySelectorAll(".key:not(.black)");
    var n = whites.length, gap = Math.max(4, Math.round(kw * 0.008)), ww = (kw - gap * (n - 1)) / n;
    for (var i = 0; i < n; i++) {
      place(whites[i], { left: i * (ww + gap), top: 0, width: ww, height: kh });
      var z = Math.min(ww * 0.62, kh * 0.3);
      place(whites[i].querySelector(".shape"), { width: z, height: z, left: (ww - 6 - z) / 2, top: kh - 6 - z - kh * 0.08 });
    }
  }
  w.__legacyLayout = layout;                          // app.js calls it before placing the black keys
  w.addEventListener("resize", function () { setTimeout(layout, 60); }, false);
  w.addEventListener("orientationchange", function () { setTimeout(layout, 250); }, false);
  d.addEventListener("DOMContentLoaded", layout, false);
})();
