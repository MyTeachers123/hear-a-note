"""
compat_css.py - static/style.css -> static/style.compat.css with fallbacks for old Safari (iOS 9 to 15).

For every declaration that old browsers cannot read, an older-style copy is written in front of it.
Old browsers ignore the part they do not understand and keep the fallback; new browsers use the original.

  1cqw / 1cqh (Safari 16+)     -> calc(1 * var(--cqw)) ; --cqw / --cqh are set by compat/legacy-shim.js
  clamp(a, b, c) (Safari 13.4) -> b  and  max(a, min(b, c))  (Safari 11.1+)
  100dvh / 100dvw (Safari 15.4)-> 100vh / 100vw (legacy-shim.js then sets exact pixel sizes)
  inset (Safari 14.1)          -> top / right / bottom / left
  place-items (Safari 11)      -> align-items + justify-items
  backdrop-filter              -> + -webkit-backdrop-filter
  flex gap (Safari 14.1)       -> .no-flex-gap ... > * + * { margin }   (class set by legacy-shim.js)
  custom properties with cq / clamp -> .no-cq ... { --x: fallback }     (class set by legacy-shim.js)

Run: python compat/compat_css.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "static"
CQ = re.compile(r"(-?\d*\.?\d+)cq(w|h)\b")
DV = re.compile(r"(\d*\.?\d+)(?:d|s|l)v(h|w)\b")


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def split_top(s, sep):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur); cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def parse(css):
    """-> list of ("rule", prelude, body) or ("at", prelude, children) or ("raw", text)."""
    nodes, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        k = css.find("}", i)
        semi = css.find(";", i)
        if j == -1 or (k != -1 and k < j):
            break
        prelude = css[i:j].strip()
        if prelude.startswith("@") and semi != -1 and semi < j:     # @import / @charset ...;
            nodes.append(("raw", css[i:semi + 1].strip())); i = semi + 1; continue
        # find matching brace
        depth, p = 1, j + 1
        while depth and p < n:
            if css[p] == "{": depth += 1
            elif css[p] == "}": depth -= 1
            p += 1
        body = css[j + 1:p - 1]
        if prelude.startswith("@") and not prelude.startswith(("@font-face", "@page")):
            nodes.append(("at", prelude, parse(body)))
        else:
            nodes.append(("rule", prelude, body))
        i = p
    return nodes


def clamp_to(value, mode):
    """mode 'mid' -> middle value; 'maxmin' -> max(a, min(b, c))."""
    while "clamp(" in value:
        s = value.index("clamp(")
        depth, p = 0, s + 5
        while True:
            if value[p] == "(": depth += 1
            elif value[p] == ")":
                depth -= 1
                if depth == 0: break
            p += 1
        a, b, c = [x.strip() for x in split_top(value[s + 6:p], ",")]
        rep = b if mode == "mid" else f"max({a}, min({b}, {c}))"
        value = value[:s] + rep + value[p + 1:]
    return value


def conv(value, mode):
    v = clamp_to(value, mode)
    v = CQ.sub(lambda m: f"calc({m.group(1)} * var(--cq{m.group(2)}, 1v{m.group(2)}))", v)
    v = DV.sub(lambda m: f"{m.group(1)}v{m.group(2)}", v)
    return v


def prefix(selectors, cls):
    out = []
    for sel in split_top(selectors, ","):
        sel = sel.strip()
        if sel.startswith("html"):
            out.append("html." + cls + sel[4:])
        elif sel.startswith(":root"):
            out.append(":root." + cls + sel[5:])
        else:
            out.append(f".{cls} {sel}")
    return ", ".join(out)


def words(s):
    """split on spaces that are not inside parentheses"""
    return [w for w in split_top(" ".join(s.split()), " ") if w]


def decls(body):
    out = []
    for d in split_top(body, ";"):
        if ":" not in d or not d.strip():
            continue
        prop, val = d.split(":", 1)
        out.append((prop.strip(), val.strip()))
    return out


STATS = {"fallbacks": 0, "cq_vars": 0, "flex_gap": 0}


def rule(prelude, body, in_keyframes=False):
    ds = decls(body)
    lines, extra = [], []
    display = next((v for p, v in ds if p == "display"), "")
    column = any(p == "flex-direction" and v.startswith("column") for p, v in ds)
    cq_over = []
    for prop, val in ds:
        needs = bool(CQ.search(val) or DV.search(val) or "clamp(" in val)
        if prop.startswith("--"):
            lines.append(f"{prop}: {val}")
            if needs:
                cq_over.append(f"{prop}: {conv(val, 'maxmin')}"); STATS["cq_vars"] += 1
            continue
        if needs:
            lines.append(f"{prop}: {conv(val, 'mid')}")
            if "clamp(" in val:
                lines.append(f"{prop}: {conv(val, 'maxmin')}")
            STATS["fallbacks"] += 1
        if prop == "inset":
            parts = words(val.replace("!important", ""))
            vals = {1: lambda p: [p[0]] * 4, 2: lambda p: [p[0], p[1], p[0], p[1]],
                    3: lambda p: [p[0], p[1], p[2], p[1]], 4: lambda p: p}[len(parts)](parts)
            for side, v in zip(("top", "right", "bottom", "left"), vals):
                lines.append(f"{side}: {conv(v, 'mid')}")
            STATS["fallbacks"] += 1
        if prop == "place-items":
            parts = val.split()
            lines.append(f"align-items: {parts[0]}")
            lines.append(f"justify-items: {parts[-1]}")
        if prop == "backdrop-filter":
            lines.append(f"-webkit-backdrop-filter: {val}")
        lines.append(f"{prop}: {val}")
        if prop in ("gap", "column-gap") and "flex" in display and not in_keyframes:
            g = words(val)[-1] if prop == "gap" else val
            side = "margin-top" if column else "margin-left"
            if prop == "gap" and column:
                g = words(val)[0]
            sels = ", ".join(f"{s.strip()} > * + *" for s in split_top(prelude, ","))
            extra.append(f"{prefix(sels, 'no-flex-gap')} {{ {side}: {conv(g, 'maxmin')} }}")
            STATS["flex_gap"] += 1
    out = f"{prelude} {{ " + "; ".join(lines) + " }"
    if cq_over and not in_keyframes:
        out += f"\n{prefix(prelude, 'no-cq')} {{ " + "; ".join(cq_over) + " }"
    for e in extra:
        out += "\n" + e
    return out


def emit(nodes, in_keyframes=False):
    out = []
    for node in nodes:
        if node[0] == "raw":
            out.append(node[1])
        elif node[0] == "rule":
            out.append(rule(node[1], node[2], in_keyframes))
        else:
            kf = "keyframes" in node[1]
            out.append(f"{node[1]} {{\n" + emit(node[2], kf) + "\n}")
    return "\n".join(out)


def main():
    src = (ROOT / "style.css").read_text(encoding="utf-8")
    css = emit(parse(strip_comments(src)))
    head = "/* GENERATED by compat/compat_css.py from style.css - do not edit; edit style.css and run it again */\n"
    (ROOT / "style.compat.css").write_text(head + css + "\n", encoding="utf-8")
    print("style.compat.css:", STATS)


if __name__ == "__main__":
    main()
