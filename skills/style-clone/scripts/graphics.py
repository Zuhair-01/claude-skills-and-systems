#!/usr/bin/env python3
"""Render a typographic card (hook headline, lock-in stat, CTA) to a PNG, for slots in
an EDL whose `kind` is "graphic" rather than sourced footage.

This is deliberately narrow: static title/subtitle/accent-word cards only — the
bold-sans-headline-with-one-italic-accent-word pattern that shows up across most creators'
DNAs (see `_CRAFT_LAYER.md`). It does NOT attempt animated diagrams (a line chart filling
in as narrated, a bar chart building bar-by-bar) — those are a confirmed, separate pipeline
gap; approximating them here would be exactly the kind of fake signature-move Phase 6b
exists to prevent. Build those properly (learn the real motion frame-by-frame, verify in
isolation) and give them their own script once one exists.

Engine: gstack's `browse` headless Chromium (already on this box, already the shared
renderer other skills use) — `load-html` the card, `screenshot --selector` the frame.
No network dependency: fonts default to system-safe stacks so a render never silently
waits on a font that didn't load in time.

Usage:
  python graphics.py --title "Every *style* is a formula" \
                     --subtitle "measured, not eyeballed" \
                     --out hook.png [--size 1080x1920] [--bg '#0E1013'] [--fg '#F3F1EC'] \
                     [--accent '#E3A857'] [--accent-font "Georgia,'Times New Roman',serif"] \
                     [--font "Arial,Helvetica,sans-serif"] [--align top|center] \
                     [--google-font 'family=Fraunces:ital,wght@0,600;1,500']

`*word*` in --title or --subtitle renders that word in the accent colour and accent font
(italic), matching the "one emphasised word" pattern. Escape a literal asterisk as `\\*`.

Second mode — `--layout badge`: a small icon+label chip meant to be composited (via
render.py's badge overlay, see below) on top of continuous real footage rather than shown
full-frame — the "app icon pops up under the chin while a presenter talks" move (`mavgpt`
DNA, confirmed on his corpus 2026-09-22; closes a `_CRAFT_LAYER.md` pipeline gap). Usage:
  python graphics.py --layout badge --title "ChatGPT" --out badge.png \
                     --badge-size 640x220 [--icon-image path/to/icon.png] \
                     [--accent '#FFD84D'] [--chroma-key '#00FF00']

The underlying `browse` headless-screenshot renderer does NOT preserve alpha (confirmed by
a real test render 2026-09-22 — a `background:transparent` page still screenshots as opaque
RGB, flattened to white). So this renders on a solid **chroma-key** background instead
(pure green by default) — render.py's badge overlay keys that colour out with ffmpeg's
`colorkey` filter before compositing, the same reliable technique real chroma-key footage
uses. Pick `--chroma-key` to a colour that doesn't appear in the icon or label (the default
pure green fails if you ever badge something actually green — override it then).
`--icon-image` is optional — a local PNG (e.g. a real product icon sourced from that
product's own brand/press page for a nominative fair-use reference, never fabricated or
mislabeled) is drawn above the label; without it, only the label text renders. Icons are
inlined as base64 data URIs, not `file://` links — `browse`'s headless Chromium refuses
`file://` image loads outright (confirmed 2026-09-23: "Not allowed to load local resource",
a real error, not a timing race the old `--wait` pattern could paper over).

Third mode — `--layout flow`: two icon badges with a connecting arrow and a short verb
label between them — "X connects to Y" / "X sends data to Y" (`visual-per-clause.md` case
2, the one confirmed pipeline gap as of 2026-09-22, closed here). Full-frame, opaque
background like `card` (this is nick_saraev's straight-cut full-frame style, not a
compositing overlay — no chroma-key needed). Usage:
  python graphics.py --layout flow --icon-image ga.png --icon-image-2 claude.png \
                     --left-label "Analytics" --right-label "Claude" \
                     --flow-verb "sends data to" --out flow.png
Both icons are required (a flow needs two named things — if you only have one, it's case 1,
use `--layout badge` or the default card instead). `--flow-verb` renders as a small label
centered on the arrow between them; omit it for a bare arrow.

`--rtl` (any layout): right-align text, flip the card's accent-bar and the flow layout's
arrow to the right, and drop the default negative letter-spacing (it breaks Arabic's
cursive glyph joining). CSS flexbox `row` is direction-aware, so `--layout flow --rtl`
auto-mirrors the icon order too — pass `--font`/`--accent-font` that actually covers the
script you're rendering; `--rtl` only fixes direction/alignment, not font coverage.
"""
import argparse, base64, html as htmllib, mimetypes, os, re, shutil, subprocess, sys, tempfile

BROWSE = shutil.which("browse") or os.path.expanduser(
    "~/.claude/skills/gstack/browse/dist/browse")
if not os.path.exists(BROWSE):
    BROWSE = os.path.expanduser("~/.claude/skills/gstack/browse/dist/browse.exe")


def data_uri(path):
    """browse's headless Chromium refuses `file://` image loads outright ("Not allowed
    to load local resource" — confirmed by a real render test 2026-09-22, not a timing
    race). Inline the bytes as a data: URI instead — sidesteps the restriction entirely,
    same trusted-origin path as the load-html call itself."""
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def markup_to_html(text, accent_font):
    """`*word*` -> <em>word</em>; `\\*` -> literal *. Rest is HTML-escaped."""
    text = text.replace("\\*", "\x00ESC\x00")
    parts = re.split(r"\*(.+?)\*", text)
    out = []
    for i, p in enumerate(parts):
        esc = htmllib.escape(p).replace("\x00ESC\x00", "*")
        out.append(f"<em>{esc}</em>" if i % 2 else esc)
    return "".join(out)


CARD_HTML = """<!doctype html><html dir="{dir}"><head><meta charset="utf-8">
{google_font_link}
<style>
  html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:{bg}}}
  .wrap{{
    width:100%;height:100%;box-sizing:border-box;
    display:flex;flex-direction:column;justify-content:{justify};
    padding:{pad}px;font-family:{font};color:{fg};direction:{dir};text-align:{text_align};
  }}
  h1{{
    margin:0;font-size:{title_size}px;line-height:1.14;font-weight:800;
    letter-spacing:{letter_spacing};
  }}
  h1 em{{font-family:{accent_font};font-style:italic;font-weight:500;color:{accent}}}
  .accent-bar{{
    width:64px;height:8px;background:{accent};margin:0 0 28px 0;border-radius:2px;
    margin-left:{bar_margin_left};margin-right:{bar_margin_right};
  }}
  p.sub{{
    margin:26px 0 0;font-size:{sub_size}px;line-height:1.35;font-weight:600;
    font-family:{accent_font};font-style:italic;color:{accent};
  }}
</style></head>
<body><div class="wrap">
  <div class="accent-bar"></div>
  <h1>{title}</h1>
  {sub_html}
</div></body></html>"""


BADGE_HTML = """<!doctype html><html dir="{dir}"><head><meta charset="utf-8">
<style>
  html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:{chroma}}}
  .wrap{{
    width:100%;height:100%;box-sizing:border-box;display:flex;flex-direction:column;
    align-items:center;justify-content:center;gap:{gap}px;font-family:{font};
  }}
  img{{width:{icon_size}px;height:{icon_size}px;border-radius:{icon_radius}px;
      box-shadow:0 4px 18px rgba(0,0,0,.45);object-fit:cover}}
  .label{{
    font-size:{label_size}px;font-weight:800;color:{accent};
    text-shadow:0 2px 10px rgba(0,0,0,.55);letter-spacing:{letter_spacing};
    text-align:center;
  }}
</style></head>
<body><div class="wrap">
  {icon_html}
  <div class="label">{label}</div>
</div></body></html>"""


FLOW_HTML = """<!doctype html><html dir="{dir}"><head><meta charset="utf-8">
<style>
  html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:{bg}}}
  .wrap{{
    width:100%;height:100%;box-sizing:border-box;display:flex;flex-direction:column;
    align-items:center;justify-content:center;font-family:{font};color:{fg};
  }}
  .row{{display:flex;flex-direction:row;align-items:center;justify-content:center;
       gap:{icon_gap}px}}
  .node{{display:flex;flex-direction:column;align-items:center;gap:{node_gap}px}}
  img{{width:{icon_size}px;height:{icon_size}px;border-radius:{icon_radius}px;
      box-shadow:0 4px 18px rgba(0,0,0,.35);object-fit:cover}}
  .node-label{{font-size:{node_label_size}px;font-weight:800;letter-spacing:{letter_spacing};
              text-align:center}}
  .arrow{{
    display:flex;flex-direction:column;align-items:center;gap:{verb_gap}px;
    width:{arrow_w}px;flex-shrink:0;
  }}
  .arrow-line{{
    width:100%;height:{line_h}px;background:{accent};position:relative;border-radius:2px;
  }}
  .arrow-line::after{{
    content:"";position:absolute;{arrow_tip_side}:-2px;top:50%;transform:translateY(-50%);
    width:0;height:0;border-top:{tri}px solid transparent;
    border-bottom:{tri}px solid transparent;{arrow_tip_border}:{tri2}px solid {accent};
  }}
  .verb{{font-size:{verb_size}px;font-weight:700;color:{accent};text-align:center}}
</style></head>
<body><div class="wrap"><div class="row">
  <div class="node"><img src="{icon1}">{left_label_html}</div>
  <div class="arrow">{verb_html}<div class="arrow-line"></div></div>
  <div class="node"><img src="{icon2}">{right_label_html}</div>
</div></div></body></html>"""


def build_html(a):
    rtl = getattr(a, "rtl", False)
    dir_ = "rtl" if rtl else "ltr"
    letter_spacing = "normal" if rtl else "-.01em"  # negative letter-spacing breaks
                                                     # Arabic's cursive glyph joining
    if getattr(a, "layout", "card") == "flow":
        w, h = (int(x) for x in a.size.split("x"))
        icon_size = int(w * 0.16)
        node_label_size = int(w * 0.032)
        left_label_html = (f'<div class="node-label">{htmllib.escape(a.left_label)}</div>'
                           if a.left_label else "")
        right_label_html = (f'<div class="node-label">{htmllib.escape(a.right_label)}</div>'
                            if a.right_label else "")
        verb_html = (f'<div class="verb">{htmllib.escape(a.flow_verb)}</div>'
                    if a.flow_verb else "")
        return FLOW_HTML.format(
            dir=dir_, w=w, h=h, bg=a.bg, fg=a.fg, font=a.font, accent=a.accent,
            icon_gap=int(w * 0.05), node_gap=int(icon_size * 0.14),
            icon_size=icon_size, icon_radius=int(icon_size * 0.2),
            node_label_size=node_label_size, letter_spacing=letter_spacing,
            arrow_w=int(w * 0.22),
            verb_gap=int(w * 0.02), line_h=max(4, int(w * 0.006)),
            tri=int(w * 0.014), tri2=int(w * 0.022), verb_size=int(w * 0.026),
            # dir=rtl reverses flexbox `row` order automatically (source ends up on the
            # physical right), so the arrow tip has to flip sides too, or it'll point the
            # wrong way relative to the now-mirrored icons
            arrow_tip_side=("left" if rtl else "right"),
            arrow_tip_border=("border-right" if rtl else "border-left"),
            icon1=data_uri(a.icon_image), icon2=data_uri(a.icon_image_2),
            left_label_html=left_label_html, right_label_html=right_label_html,
            verb_html=verb_html,
        )
    if getattr(a, "layout", "card") == "badge":
        w, h = (int(x) for x in a.badge_size.split("x"))
        icon_size = int(h * 0.55)
        icon_html = (f'<img src="{data_uri(a.icon_image)}">'
                    if getattr(a, "icon_image", None) else "")
        return BADGE_HTML.format(
            dir=dir_, w=w, h=h, gap=int(h * 0.06), font=a.font, icon_size=icon_size,
            icon_radius=int(icon_size * 0.22), label_size=int(h * 0.19),
            letter_spacing=letter_spacing,
            accent=a.accent, icon_html=icon_html, chroma=a.chroma_key,
            label=htmllib.escape(a.title),
        )
    google_link = ""
    if a.google_font:
        google_link = (f'<link rel="preconnect" href="https://fonts.googleapis.com">'
                       f'<link href="https://fonts.googleapis.com/css2?{a.google_font}'
                       f'&display=swap" rel="stylesheet">')
    title_html = markup_to_html(a.title, a.accent_font)
    sub_html = (f'<p class="sub">{markup_to_html(a.subtitle, a.accent_font)}</p>'
               if a.subtitle else "")
    w, h = (int(x) for x in a.size.split("x"))
    return CARD_HTML.format(
        google_font_link=google_link, dir=dir_, w=w, h=h, bg=a.bg, fg=a.fg,
        justify="center" if a.align == "center" else "flex-start",
        text_align=("right" if rtl else "left"), letter_spacing=letter_spacing,
        bar_margin_left=("auto" if rtl else "0"), bar_margin_right=("0" if rtl else "auto"),
        pad=int(w * 0.072), font=a.font, title_size=int(w * 0.082),
        sub_size=int(w * 0.036), accent=a.accent, accent_font=a.accent_font,
        title=title_html, sub_html=sub_html,
    )


def render(a):
    if not os.path.exists(BROWSE):
        sys.exit(f"browse binary not found at {BROWSE} — run its setup first "
                 "(see the `browse` skill).")
    html_content = build_html(a)
    tmp_html = tempfile.NamedTemporaryFile(
        suffix=".html", delete=False, dir=os.path.dirname(os.path.abspath(a.out)) or ".")
    tmp_html.write(html_content.encode("utf-8"))
    tmp_html.close()

    w, h = (a.badge_size if getattr(a, "layout", "card") == "badge" else a.size).split("x")
    out_abs = os.path.abspath(a.out)
    os.makedirs(os.path.dirname(out_abs) or ".", exist_ok=True)

    # browse's daemon state dir (.gstack/) is created relative to the caller's cwd —
    # pin it to $HOME so repeated runs reuse the one shared daemon other skills already
    # use there, instead of scattering a fresh .gstack/ into whatever directory this
    # happened to be invoked from (the skill's own script folder, a project dir, ...).
    home = os.path.expanduser("~")

    def run(cmd):
        r = subprocess.run([BROWSE] + cmd, text=True, capture_output=True,
                           encoding="utf-8", errors="replace", timeout=60, cwd=home)
        if r.returncode != 0:
            sys.exit(f"browse {cmd[0]} failed:\n{r.stdout}\n{r.stderr}")
        return r.stdout

    run(["viewport", f"{w}x{h}"])
    run(["load-html", tmp_html.name])
    # a Google Font needs a beat to actually apply before the screenshot fires
    if a.google_font:
        run(["wait", "body", "--timeout", "1500"])
    run(["screenshot", out_abs])
    os.unlink(tmp_html.name)
    print(f"-> {out_abs}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default=None,
                    help="required for --layout card/badge; unused for --layout flow")
    ap.add_argument("--subtitle", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--bg", default="#0E1013")
    ap.add_argument("--fg", default="#F3F1EC")
    ap.add_argument("--accent", default="#E3A857")
    ap.add_argument("--font", default="Arial,Helvetica,sans-serif")
    ap.add_argument("--accent-font", default="Georgia,'Times New Roman',serif")
    ap.add_argument("--align", default="top", choices=["top", "center"])
    ap.add_argument("--rtl", action="store_true",
                    help="Arabic/Hebrew/etc: right-align text, flip the accent-bar and "
                         "flow-arrow to the right, and drop the default negative "
                         "letter-spacing (it breaks Arabic's cursive glyph joining). "
                         "The font stack still needs to actually cover the script — "
                         "pick a --font/--accent-font that does, this flag alone won't "
                         "fix missing glyphs.")
    ap.add_argument("--google-font", default=None,
                    help="the querystring part only, e.g. "
                         "\"family=Fraunces:ital,wght@0,600;1,500\" — "
                         "omit to stay offline-safe on system fonts")
    ap.add_argument("--layout", default="card", choices=["card", "badge", "flow"],
                    help="'card' (default): full-frame opaque title/subtitle card. "
                         "'badge': small transparent icon+label chip for compositing "
                         "onto real footage. 'flow': full-frame two-icon "
                         "relationship/arrow card (see module docstring)")
    ap.add_argument("--badge-size", default="640x220",
                    help="--layout badge only: WxH of the small transparent PNG")
    ap.add_argument("--icon-image", default=None,
                    help="--layout badge/flow: local PNG drawn above the label "
                         "(flow: the left/source icon, required)")
    ap.add_argument("--icon-image-2", default=None,
                    help="--layout flow only: the right/destination icon PNG, required")
    ap.add_argument("--left-label", default=None,
                    help="--layout flow only: name under the left icon, e.g. 'Analytics'")
    ap.add_argument("--right-label", default=None,
                    help="--layout flow only: name under the right icon, e.g. 'Claude'")
    ap.add_argument("--flow-verb", default=None,
                    help="--layout flow only: short verb label on the arrow, "
                         "e.g. 'sends data to' — omit for a bare arrow")
    ap.add_argument("--chroma-key", default="#00FF00",
                    help="--layout badge only: solid background colour render.py keys "
                         "out during compositing (browse's screenshot has no real alpha "
                         "support — see module docstring). Pick a colour absent from the "
                         "icon/label.")
    a = ap.parse_args()
    if a.layout == "flow" and not (a.icon_image and a.icon_image_2):
        sys.exit("--layout flow requires both --icon-image and --icon-image-2 "
                 "(a flow needs two named things — one icon alone is case 1, "
                 "use --layout badge or the default card instead)")
    if a.layout != "flow" and not a.title:
        sys.exit(f"--title is required for --layout {a.layout}")
    render(a)


def _selfcheck():
    class A: pass
    a = A()
    a.title, a.accent_font = "Every *style* is a formula", "Georgia,serif"
    got = markup_to_html(a.title, a.accent_font)
    assert got == "Every <em>style</em> is a formula", got
    assert markup_to_html(r"escaped \*star\*", "x") == "escaped *star*"
    assert markup_to_html("no markup here", "x") == "no markup here"
    a2 = argparse.Namespace(title="Plain *word*", subtitle=None, size="1080x1920",
                            bg="#000", fg="#fff", accent="#E3A857",
                            justify="top", font="Arial", accent_font="Georgia",
                            align="top", google_font=None)
    html_out = build_html(a2)
    assert "<em>word</em>" in html_out
    assert "1080px" in html_out and "1920px" in html_out

    # 1x1 PNG bytes — real files on disk so data_uri()'s open() call is a genuine
    # exercise of that path, not a mock.
    px = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108020000009077"
                       "53de0000000c4944415478da6360606060000000050001a5f645400000000049454e44ae426082")
    tmpdir = tempfile.mkdtemp()
    p1, p2 = os.path.join(tmpdir, "a.png"), os.path.join(tmpdir, "b.png")
    open(p1, "wb").write(px); open(p2, "wb").write(px)
    assert data_uri(p1).startswith("data:image/png;base64,")

    a3 = argparse.Namespace(layout="flow", size="1080x1920", bg="#000", fg="#fff",
                            accent="#E3A857", font="Arial", icon_image=p1,
                            icon_image_2=p2, left_label="Analytics",
                            right_label="Claude", flow_verb="sends data to")
    flow_out = build_html(a3)
    assert flow_out.count("data:image/png;base64,") == 2, flow_out
    assert "file://" not in flow_out
    assert "Analytics" in flow_out and "Claude" in flow_out
    assert "sends data to" in flow_out
    assert "arrow-line" in flow_out
    assert 'dir="ltr"' in flow_out and "border-left" in flow_out  # default, arrow -> right

    a4 = argparse.Namespace(title="Plain *word*", subtitle=None, size="1080x1920",
                            bg="#000", fg="#fff", accent="#E3A857",
                            justify="top", font="Arial", accent_font="Georgia",
                            align="top", google_font=None, rtl=True)
    rtl_out = build_html(a4)
    assert 'dir="rtl"' in rtl_out, rtl_out
    assert "text-align:right" in rtl_out
    assert "letter-spacing:normal" in rtl_out  # negative spacing breaks Arabic joining
    assert "margin-left:auto" in rtl_out       # accent-bar flipped to the right

    a5 = argparse.Namespace(layout="flow", size="1080x1920", bg="#000", fg="#fff",
                            accent="#E3A857", font="Arial", icon_image=p1,
                            icon_image_2=p2, left_label="Analytics", right_label="Claude",
                            flow_verb="sends data to", rtl=True)
    flow_rtl_out = build_html(a5)
    assert 'dir="rtl"' in flow_rtl_out
    assert "border-right" in flow_rtl_out  # arrow tip flips when the row visually mirrors
    shutil.rmtree(tmpdir)
    print("selfcheck ok")


if __name__ == "__main__":
    if "--selfcheck" in sys.argv:
        _selfcheck()
    else:
        main()
