/* legacy-shim.js - lets the app run on old iPads / iPhones (Safari 9 to 13) as well as on new browsers.
 * Plain ES5 on purpose. It is bundled first, before the app (see compat/build.mjs).
 *  1. Pointer Events (Safari 13+) -> built from touch / mouse events
 *  2. Element.append (Safari 10+)
 *  3. App size: 100dvw / 100dvh (Safari 15.4+) -> window.innerWidth / innerHeight
 *  4. Container query units cqw / cqh (Safari 16+) -> --cqw / --cqh custom properties (used by style.compat.css)
 *  5. aspect-ratio (Safari 15+) -> square shapes get their height from JS
 *  6. Flexbox gap (Safari 14.1+) -> class "no-flex-gap" on <html> (style.compat.css adds margins)
 */
(function () {
  "use strict";
  var doc = document, win = window, root = doc.documentElement;
  var FORCE = !!win.__compatForce;                   // tests only: behave like an old browser
  var supports = function (p, v) { if (FORCE) return false; try { return !!(win.CSS && CSS.supports && CSS.supports(p, v)); } catch (e) { return false; } };

  /* 1. Pointer Events */
  if (!win.PointerEvent || FORCE) {
    var MAP = { pointerdown: ["touchstart", "mousedown"], pointerup: ["touchend", "mouseup"], pointercancel: ["touchcancel"] };
    var lastTouch = 0;
    var proto = (win.EventTarget && EventTarget.prototype.addEventListener) ? EventTarget.prototype : Node.prototype;
    var add = proto.addEventListener, remove = proto.removeEventListener;
    var wrapKey = "__ptr" + Math.random().toString(36).slice(2);
    var fake = function (type, e, t) {
      return {
        type: type, target: (t && t.target) || e.target, currentTarget: e.currentTarget,
        clientX: t ? t.clientX : e.clientX, clientY: t ? t.clientY : e.clientY,
        pointerId: t ? t.identifier : 1, pointerType: t ? "touch" : "mouse", isPrimary: true, button: 0,
        preventDefault: function () { e.preventDefault(); }, stopPropagation: function () { e.stopPropagation(); },
        stopImmediatePropagation: function () { if (e.stopImmediatePropagation) e.stopImmediatePropagation(); },
        originalEvent: e
      };
    };
    var wrapped = function (type, fn) {
      if (!fn[wrapKey]) fn[wrapKey] = {};
      if (!fn[wrapKey][type]) {
        fn[wrapKey][type] = function (e) {
          var call = typeof fn === "function" ? fn : fn.handleEvent && function (x) { fn.handleEvent(x); };
          if (!call) return;
          if (e.changedTouches) {
            lastTouch = Date.now();
            for (var i = 0; i < e.changedTouches.length; i++) call.call(this, fake(type, e, e.changedTouches[i]));
          } else {
            if (Date.now() - lastTouch < 900) return;        // mouse events iOS makes up after a touch
            call.call(this, fake(type, e, null));
          }
        };
      }
      return fn[wrapKey][type];
    };
    proto.addEventListener = function (type, fn, opt) {
      if (MAP[type] && fn) {
        var capture = typeof opt === "object" ? !!opt.capture : !!opt, self = this;
        MAP[type].forEach(function (real) {
          var o = real.indexOf("touch") === 0 ? { capture: capture, passive: false } : capture;
          try { add.call(self, real, wrapped(type, fn), o); } catch (e) { add.call(self, real, wrapped(type, fn), capture); }
        });
        return;
      }
      if (type === "pointerleave" || type === "pointermove") return;   // not needed by the app on touch screens
      return add.call(this, type, fn, opt);
    };
    proto.removeEventListener = function (type, fn, opt) {
      if (MAP[type] && fn && fn[wrapKey]) {
        var self = this, capture = typeof opt === "object" ? !!opt.capture : !!opt;
        MAP[type].forEach(function (real) { remove.call(self, real, fn[wrapKey][type], capture); });
        return;
      }
      return remove.call(this, type, fn, opt);
    };
  }

  /* 2. Element.append / prepend */
  [Element.prototype, Document.prototype, DocumentFragment.prototype].forEach(function (p) {
    if (!p.append) p.append = function () {
      for (var i = 0; i < arguments.length; i++) {
        var n = arguments[i];
        this.appendChild(n instanceof Node ? n : doc.createTextNode(String(n)));
      }
    };
  });
  if (!Element.prototype.remove) Element.prototype.remove = function () { if (this.parentNode) this.parentNode.removeChild(this); };
  if (win.NodeList && !NodeList.prototype.forEach) NodeList.prototype.forEach = Array.prototype.forEach;

  /* 6. Flexbox gap */
  var flexGap = (function () {
    var d = doc.createElement("div");
    d.style.cssText = "display:flex;flex-direction:column;row-gap:1px;position:absolute;visibility:hidden";
    d.appendChild(doc.createElement("div")); d.appendChild(doc.createElement("div"));
    root.appendChild(d); var ok = d.scrollHeight === 1; root.removeChild(d); return ok;
  })();
  if (!flexGap || FORCE) root.className += " no-flex-gap";

  var DVH = supports("height", "100dvh"), CQ = supports("width", "1cqw"), AR = supports("aspect-ratio", "1");
  if (!CQ) root.className += " no-cq";

  function layout() {
    var app = doc.getElementById("app");
    if (!app) return;
    /* 3. app size (only when dvh is missing: the CSS fallback 100vh is too tall on iPad Safari) */
    if (!DVH) {
      var w = win.innerWidth, h = win.innerHeight;
      var rotate = win.matchMedia && matchMedia("(orientation: portrait) and (pointer: coarse)").matches;
      app.style.width = (rotate ? h : w) + "px";
      app.style.height = (rotate ? w : h) + "px";
      app.style.left = (rotate ? w : 0) + "px";
    }
    /* 4. 1cqw / 1cqh of #app (its content box) */
    var cs = win.getComputedStyle(app);
    var cw = app.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    var ch = app.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
    app.style.setProperty("--cqw", cw / 100 + "px");
    app.style.setProperty("--cqh", ch / 100 + "px");
    squares();
  }
  /* 5. square shapes without aspect-ratio */
  var SQUARE = ".key .shape, .mini-key .shape, .fly .shape";
  function squares() {
    if (AR) return;
    var els = doc.querySelectorAll(SQUARE);
    for (var i = 0; i < els.length; i++) { var el = els[i]; el.style.height = el.offsetWidth + "px"; }
  }
  var queued = false;
  function soon() {
    if (queued) return; queued = true;
    (win.requestAnimationFrame || setTimeout)(function () { queued = false; layout(); });
  }
  win.addEventListener("resize", soon);
  win.addEventListener("orientationchange", function () { setTimeout(layout, 250); });
  doc.addEventListener("DOMContentLoaded", function () {
    layout();
    if (!AR && win.MutationObserver) {
      new MutationObserver(function () { (win.requestAnimationFrame || setTimeout)(squares); })
        .observe(doc.getElementById("app") || doc.body, { childList: true, subtree: true });
    }
  });
  win.addEventListener("load", layout);
  layout();                                          // #app already exists: the scripts are at the end of <body>
  win.__compatLayout = layout;
})();
