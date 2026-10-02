---
name: live-generative-cards
description: Build real, in-browser generative visual components instead of static/recolored mockups — canvas-based image-to-ASCII art (luminance or Sobel edge-detect, for dark-on-dark subjects) from any real photo/logo, per-character wave reveals, animated conic-gradient glow borders, animated counting stat tiles, and terminal-chrome windows — plus how to actually ship one of these onto a real GitHub README (SVG+SMIL, and the trap where GitHub strips the animation and leaves a blank image unless the base state is already correct). Use whenever a request asks for a "live", "animated", "generated", or "dynamic" visual identity/profile/dashboard card, or to put a generated visual on an actual GitHub profile. Triggers on a gitskins-style profile card, an animated hero/identity card, a live stat panel, "make it actually move/generate, not a screenshot," or "put this on my GitHub."
---

# Live Generative Cards

Built while reverse-engineering gitskins.com's README-generator preview (hero identity card, ASCII wordmark, ASCII portrait, animated "Profile Signal" stat grid, floating chip). The lesson that triggered this skill: a first pass that just re-skinned a static mockup in different hex colors was rejected outright — the ask was for the real mechanism, not a repaint. This skill is the reusable mechanism, decoupled from GitHub.

## When to use

Any time a deliverable wants to *feel alive* — a personal/product identity card, a profile page hero, a dashboard stat panel, an about-page portrait, a README, a pitch-deck opener. Works in any HTML/CSS/JS surface (Artifacts, a real site, a component library) — nothing here is GitHub-specific.

## Core technique 1 — image → ASCII art (canvas, no libraries)

Sample the image into a small grid via an offscreen canvas, compute luminance per cell, map to a character ramp. Real algorithm, real input image (embed as a data URI if the runtime blocks remote image loads — e.g. Claude Artifacts' CSP blocks remote `<img>`/fetch, so download the source image ahead of time and inline it as base64).

```js
function imageToAscii(img, cols, rows, callback, opts){
  opts = opts || {};
  var RAMP = " .:-=+*#%@";
  var invert = !!opts.invert;
  var canvas = document.createElement('canvas');
  canvas.width = cols; canvas.height = rows;
  var ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0, cols, rows);
  var data = ctx.getImageData(0,0,cols,rows).data;

  // contrast-stretch: real photos are rarely full 0..1 range, especially
  // dark subjects on dark backgrounds — without this the output is either
  // a near-empty page (raw luminance, dark subject → mostly blank) or a
  // uniform block (no tonal separation). Stretch to the image's own min/max.
  var n = cols*rows, lums = new Float32Array(n), lo = 1, hi = 0;
  for (var p = 0; p < n; p++) {
    var i = p*4;
    var lum = (0.299*data[i] + 0.587*data[i+1] + 0.114*data[i+2]) / 255;
    lums[p] = lum;
    if (lum < lo) lo = lum;
    if (lum > hi) hi = lum;
  }
  var range = Math.max(0.02, hi - lo);

  var out = '';
  for (var y = 0; y < rows; y++) {
    var line = '';
    for (var x = 0; x < cols; x++) {
      var norm = (lums[y*cols+x] - lo) / range;
      if (invert) norm = 1 - norm;
      var idx = Math.min(RAMP.length-1, Math.max(0, Math.floor(norm * RAMP.length)));
      line += RAMP[idx];
    }
    out += line + '\n';
  }
  callback(out);
}
```

**Direct mapping** (bright = dense `@`, dark = blank space) — use for text/logos rendered white-on-black to canvas (a wordmark), or any subject where the *bright* areas are what should read as ink.

**`invert:true`** (dark = dense, bright = blank) — sparse and unreliable for a dark subject on a dark background: real photos rarely separate cleanly by raw luminance alone (a dark hoodie and a near-black background can sit within a few luminance values of each other), so this mode either renders almost nothing or, once contrast-stretched, a muddy uniform block with no legible edges. **Prefer edge-detection (technique 1b) for any dark-subject/dark-background photo** — this mode is only worth reaching for on a subject with real luminance separation from its background (a pale face on a dark background, etc).

Try candidates on the actual source image and keep whichever produces a recognizable silhouette — don't assume; check the rendered output (screenshot the artifact) before shipping either choice.

## Core technique 1b — image → ASCII art via edge detection (Sobel)

For a dark subject on a dark background (a hoodie on a near-black backdrop, most "moody" avatar photography), luminance mapping — direct or inverted, contrast-stretched or not — cannot cleanly separate subject from background because both sit in a similar tonal range. Percentile/tone-banding hacks (pick a luminance window and call anything inside it "subject") are fragile too: they surface an isolated bright fold or reflection as a random unrelated blob with no connection to the actual silhouette.

Edge detection sidesteps the whole problem: a real photo has structure (fabric folds, a jawline, a dot-matrix pattern on a mask) that produces local *gradient* even when two adjacent regions are both objectively dark. A smooth background — even a bright one — produces almost no gradient. This naturally yields a clean, recognizable outline/contour rendering with no per-image threshold tuning.

```js
function imageToAsciiEdge(source, cols, rows, callback, opts){
  opts = opts || {};
  var RAMP = " .:-=+*#%@";
  var scale = opts.scale || 3;               // supersample so fine detail (a dot-matrix face) survives
  var hiW = cols*scale, hiH = rows*scale;
  var canvas = document.createElement('canvas');
  canvas.width = hiW; canvas.height = hiH;
  var ctx = canvas.getContext('2d');
  ctx.drawImage(source, 0, 0, hiW, hiH);
  var data = ctx.getImageData(0,0,hiW,hiH).data;

  var n = hiW*hiH, lum = new Float32Array(n);
  for (var p = 0; p < n; p++) {
    var i = p*4;
    lum[p] = (0.299*data[i] + 0.587*data[i+1] + 0.114*data[i+2]) / 255;
  }
  function L(x,y){
    if (x<0) x=0; else if (x>=hiW) x=hiW-1;
    if (y<0) y=0; else if (y>=hiH) y=hiH-1;
    return lum[y*hiW+x];
  }
  var mag = new Float32Array(n);
  for (var y = 0; y < hiH; y++) for (var x = 0; x < hiW; x++) {
    var gx = -L(x-1,y-1)-2*L(x-1,y)-L(x-1,y+1) + L(x+1,y-1)+2*L(x+1,y)+L(x+1,y+1);
    var gy = -L(x-1,y-1)-2*L(x,y-1)-L(x+1,y-1) + L(x-1,y+1)+2*L(x,y+1)+L(x+1,y+1);
    mag[y*hiW+x] = Math.sqrt(gx*gx+gy*gy);
  }

  // max-pool the hi-res gradient down to the character grid — averaging would
  // blur out exactly the fine detail (the dot pattern) that makes this worth doing.
  var cellW = hiW/cols, cellH = hiH/rows;
  var grid = new Float32Array(cols*rows);
  for (var ry = 0; ry < rows; ry++) {
    var y0 = Math.floor(ry*cellH), y1 = Math.floor((ry+1)*cellH);
    for (var rx = 0; rx < cols; rx++) {
      var x0 = Math.floor(rx*cellW), x1 = Math.floor((rx+1)*cellW), best = 0;
      for (var yy = y0; yy < y1; yy++) for (var xx = x0; xx < x1; xx++) {
        var v = mag[yy*hiW+xx]; if (v > best) best = v;
      }
      grid[ry*cols+rx] = best;
    }
  }

  // normalize against a high percentile (not the true max) so one outlier
  // hot pixel can't wash out the whole normalization
  var sorted = Array.prototype.slice.call(grid).sort(function(a,b){return a-b;});
  var whitePoint = sorted[Math.floor(sorted.length*0.93)] || 1;
  if (whitePoint < 0.02) whitePoint = 0.02;
  var thresh = opts.threshold !== undefined ? opts.threshold : 0.08; // raise if background noise leaks through

  var out = '';
  for (var gy = 0; gy < rows; gy++) {
    var line = '';
    for (var gx2 = 0; gx2 < cols; gx2++) {
      var v2 = grid[gy*cols+gx2] / whitePoint;
      if (v2 < thresh) { line += RAMP[0]; continue; }
      var idx = Math.min(RAMP.length-1, Math.max(1, Math.floor(v2 * RAMP.length)));
      line += RAMP[idx];
    }
    out += line + '\n';
  }
  callback(out);
}
```

Tune `threshold` by looking at the output, not by guessing: too low and background grain/JPEG noise reads as scattered flecks everywhere; too high and fine detail (the dot-matrix face, in this project's case) disappears. `0.08`–`0.28` covered every case hit so far — noisier/lower-contrast sources need the higher end.

## Procedural background (when there's no source file for it)

A user may describe a background they want (a nebula, a starfield, a gradient wash) without actually having the file, or the pasted reference image isn't retrievable as a real file on disk (chat-pasted images aren't always saved anywhere you can `curl`/read — check `OneDrive/Pictures/Screenshots`, `Downloads`, and recent-file search before assuming you can't get it, but be ready to generate a stand-in). Composite a canvas-drawn approximation behind the subject instead of blocking on the exact asset:

```js
function makeNebulaCanvas(size){
  var c = document.createElement('canvas');
  c.width = size; c.height = size;
  var ctx = c.getContext('2d');
  ctx.fillStyle = '#020208'; ctx.fillRect(0,0,size,size);
  function bloom(x,y,r,rgb,alpha){
    var g = ctx.createRadialGradient(x,y,0,x,y,r);
    g.addColorStop(0, 'rgba('+rgb+','+alpha+')');
    g.addColorStop(1, 'rgba('+rgb+',0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill();
  }
  bloom(size*0.22, size*0.18, size*0.6, '124,58,237', 0.5);   // violet
  bloom(size*0.88, size*0.15, size*0.5, '56,189,248', 0.38);  // cyan
  bloom(size*0.72, size*0.88, size*0.55, '167,139,250', 0.32);
  var starCount = Math.floor(size*size/850);
  for (var i = 0; i < starCount; i++) {
    var sx = Math.random()*size, sy = Math.random()*size;
    var r = Math.random() < 0.9 ? Math.random()*0.6+0.25 : Math.random()*1.3+0.7;
    ctx.fillStyle = 'rgba(255,255,255,'+(Math.random()*0.6+0.3)+')';
    ctx.beginPath(); ctx.arc(sx,sy,r,0,Math.PI*2); ctx.fill();
  }
  return c;
}
```
Feeding this composite through the *same* edge-detect function keeps foreground/background naturally separated for free: smooth gradient blooms produce near-zero gradient (stay blank/sparse), while the subject's real structure dominates — no manual masking needed to keep the background from competing with the character.

## Per-character wave reveal (left-to-right, one-time vs looping)

A per-line typed reveal (top-to-bottom) reads as a terminal boot log; a per-*column* reveal reads as a scanning wave sweeping across the subject — closer to what "make it feel alive" usually means for a portrait/wordmark. Wrap each non-space character in its own `<span>`, stagger by column index via `animation-delay`, and let CSS (not a JS loop) drive it:

```js
function waveReveal(el, text, opts){
  opts = opts || {};
  var loop = !!opts.loop, sweepMs = opts.sweepMs || 900;
  var lines = text.replace(/\n$/,'').split('\n');
  var cols = 0;
  for (var li = 0; li < lines.length; li++) if (lines[li].length > cols) cols = lines[li].length;
  el.textContent = '';
  el.classList.add(loop ? 'wave-loop' : 'wave-once');
  var frag = document.createDocumentFragment();
  for (var y = 0; y < lines.length; y++) {
    var line = lines[y];
    for (var x = 0; x < cols; x++) {
      var span = document.createElement('span');
      span.textContent = line[x] || ' ';
      span.style.animationDelay = Math.round((x/cols) * sweepMs) + 'ms';
      frag.appendChild(span);
    }
    frag.appendChild(document.createTextNode('\n'));
  }
  el.appendChild(frag);
}
```
```css
.wave-once span, .wave-loop span{ display:inline-block; }
.wave-once span{ opacity:0; animation:waveOnce 600ms ease-out forwards; }
@keyframes waveOnce{ from{opacity:0;} to{opacity:1;} }
.wave-loop span{ animation:waveLoop 2.4s ease-in-out infinite; }
@keyframes waveLoop{ 0%{opacity:.32;} 14%{opacity:1;} 38%{opacity:.32;} 100%{opacity:.32;} }
```
Because `animation-iteration-count: infinite` on the loop variant restarts each span's own cycle independently once its `animation-delay` elapses, staggered delays alone (no JS timer, no rAF) produce a continuous traveling wave — the phase offset persists across iterations. Use `loop:false` for a one-time "generation" moment (a portrait rendering in), `loop:true` for something that should always look alive (a wordmark/logo). A few thousand spans (a 100×55 character grid is ~5,500) is fine performance-wise in a real browser; skip characters that are just spaces to cut the count substantially (a real portrait is usually 5–15% ink).

**Wordmark from typed text**: draw the text to an offscreen canvas first (`ctx.font`, `fillText`, white on black), then run it through the same `imageToAscii` — one function serves both photos and generated typography.

**Cols/rows**: character cells are taller than wide, so pick rows ≈ cols × (image aspect) × 0.5–0.55 to avoid a squashed result. font-size on the `<pre>` needs to be small (5–7px) with `line-height` near 1.0–1.1 for the density to read as an image rather than text.

## Core technique 2 — animated glow border

A rotating conic-gradient on an oversized pseudo-element, clipped by `overflow:hidden` on the parent — cheap, GPU-friendly, and reads as "alive" immediately.

```css
.card{ position:relative; border-radius:20px; padding:2px; overflow:hidden; }
.card::before{
  content:""; position:absolute; inset:-60%;
  background:conic-gradient(var(--c1), var(--c2), var(--c3), var(--c1));
  animation: rot 7s linear infinite;
}
@keyframes rot{ to{ transform:rotate(360deg); } }
@media (prefers-reduced-motion: reduce){ .card::before{ animation:none; } }
.card-inner{ position:relative; border-radius:18px; background:var(--bg); }
```
Avoid animating a custom `@property` angle for this (`--ang` interpolation) — it's the more "correct" way to animate a conic-gradient's rotation directly, but is unreliable in automated/headless verification contexts (see gotcha below). The rotating pseudo-element + `transform: rotate()` gives the same visual result and is a plain CSS animation, not a custom-property interpolation.

## Core technique 3 — animated counting stat tiles

Count up from 0 to a real number on load, with a fill bar. Use `setInterval` in fixed steps, not `requestAnimationFrame` scaled by timestamp delta (see gotcha).

```js
document.querySelectorAll('.stat-tile').forEach(function(tile){
  var vEl = tile.querySelector('.v'), barEl = tile.querySelector('.bar i');
  var target = parseInt(vEl.dataset.target, 10);
  setTimeout(function(){
    barEl.style.width = barEl.dataset.fill + '%';
    var steps = 24, cur = 0;
    var iv = setInterval(function(){
      cur++;
      vEl.textContent = cur >= steps ? target : Math.floor((cur/steps)*target);
      if (cur >= steps) clearInterval(iv);
    }, 900/steps);
  }, 300);
});
```

## Core technique 4 — terminal-chrome window

A reusable shell for any "generated output" panel (ASCII art, logs, code): traffic-light dots, a centered command-line label, monospace body.

```html
<div class="term-win">
  <div class="term-bar">
    <div class="term-dots"><span></span><span></span><span></span></div>
    <div class="term-cmd">user@host: ~$ ./script.sh</div>
  </div>
  <div class="term-body"><pre class="ascii" id="out"></pre></div>
</div>
```
```css
.term-dots span{width:10px;height:10px;border-radius:50%;}
.term-dots span:nth-child(1){background:#ff5f57;}
.term-dots span:nth-child(2){background:#febc2e;}
.term-dots span:nth-child(3){background:#28c840;}
```

## Reveal animation (typing / line-by-line)

```js
function revealInto(el, text){
  var lines = text.split('\n'), i = 0;
  el.textContent = '';
  (function step(){
    if (i >= lines.length) return;
    el.textContent += lines[i] + '\n';
    i++;
    setTimeout(step, 16); // NOT requestAnimationFrame — see gotcha
  })();
}
```

## Gotcha: requestAnimationFrame stalls in automated/backgrounded tabs

`requestAnimationFrame` is throttled or effectively paused by Chromium when a tab is not the OS-focused, foreground tab — which is exactly the state of a browser driven by automation tools (Claude in Chrome, Playwright, etc.) even while you're actively screenshotting it. Symptom: a reveal or count-up animation renders its *first* frame then appears frozen forever, with zero console errors, because the loop is technically still scheduled — it's just never firing. Plain CSS `animation`/`transition` keep running fine in this state (they're not `rAF`-gated the same way); it's specifically JS-driven `rAF` loops that stall.

Fix: for anything you need to actually verify by screenshotting an automated tab, drive JS animation with `setTimeout`/`setInterval` instead of `requestAnimationFrame`. If the target runtime is guaranteed to be a real, focused user tab (not something you'll verify via automation), `rAF` is fine and smoother — but default to timers when you can't be sure, and *always* when you're about to verify the result yourself via browser automation.

## Target: an actual GitHub README (profile or repo)

**A README is not a runtime.** GitHub strips `<script>` and inline `style=` attributes entirely from rendered Markdown/HTML — none of the JS techniques above (canvas generation, `waveReveal`, count-up `setInterval`, the CSS `@keyframes` blocks) can run there. If a request explicitly wants something "put on my GitHub profile," that's a materially different deliverable from an Artifact, and worth saying so before building — the two most common real options:

1. **A live third-party badge/SVG service** — `capsule-render` (animated header banners), `readme-typing-svg` (typing text), `github-readme-stats` / `github-readme-streak-stats` (real live data, refetched every view). These work because GitHub's `<img>` tag can point at any external URL, and the animation/data-freshness lives entirely on that external service's response — GitHub itself runs nothing.
2. **A hand-built animated SVG, generated ahead of time and committed to the repo.** SVG's native `<animate>`/SMIL tags run in the *browser's* SVG renderer when the image displays — not GitHub's Markdown pipeline — so real animation is possible without any external service. This is the way to get a *custom* generated visual (this project's ASCII portrait/wordmark) animated on a profile.

### The SMIL-on-GitHub trap: base state must be correct **without** the animation

GitHub serves repo-relative images (`<img src="portrait.svg">` pointing at a file in the same repo) through `raw.githubusercontent.com`, which — unlike a general-purpose external SVG host — strips or refuses to execute SMIL `<animate>` for files it serves as user content. Symptom actually hit: a wordmark SVG whose *base* opacity attribute was `0.3` (with an `<animate>` meant to pulse it up to `1`) rendered dim-but-visible on the profile; a portrait SVG whose base opacity was `0` (relying entirely on the animate to reach `1`) rendered **completely blank** — same technique, opposite outcome, because one had a viewable fallback and the other didn't.

**Rule: every `<animate>`'d element's static/base attributes must already be the fully-correct final appearance.** Write the animation as a *bonus* transition into a state the element is already sitting in by default, not as the only path to visibility:

```xml
<!-- WRONG: invisible forever if SMIL is stripped -->
<text opacity="0">A<animate attributeName="opacity" from="0" to="1" begin="0.3s" fill="freeze"/></text>

<!-- RIGHT: fully visible even with zero animation support -->
<text opacity="1">A<animate attributeName="opacity" from="0.15" to="1" begin="0.3s" fill="freeze"/></text>
```
Verify by actually loading the raw file through GitHub's serving path before calling it done — a direct render of the same SVG through a CDN/proxy that preserves SMIL (e.g. `cdn.jsdelivr.net/gh/<user>/<repo>@<branch>/<file>`) can look perfect while the exact same file is blank when embedded via `raw.githubusercontent.com` in the actual README. Check both.

### Generating the ASCII grid outside a browser (Python/Pillow port)

Browser automation for verification is often unavailable or unreliable mid-task (tab state resets, scroll gets stuck, `file://` navigation is blocked for extensions). The same edge-detect algorithm ports directly to Python + Pillow for headless, reliable generation — useful both for producing the character grid to embed in a hand-built SVG, and as a fallback when browser-side canvas access isn't practical:

```python
from PIL import Image
import math

RAMP = " .:-=+*#%@"

def sobel_grid(avatar_path, cols, rows, scale=3, threshold=0.10):
    hiW, hiH = cols*scale, rows*scale
    img = Image.open(avatar_path).convert("RGB").resize((hiW, hiH), Image.LANCZOS)
    px = img.load()
    lum = [[(0.299*px[x,y][0]+0.587*px[x,y][1]+0.114*px[x,y][2])/255
            for x in range(hiW)] for y in range(hiH)]
    def L(x,y):
        x = max(0, min(hiW-1, x)); y = max(0, min(hiH-1, y))
        return lum[y][x]
    mag = [[0.0]*hiW for _ in range(hiH)]
    for y in range(hiH):
        for x in range(hiW):
            gx = -L(x-1,y-1)-2*L(x-1,y)-L(x-1,y+1) + L(x+1,y-1)+2*L(x+1,y)+L(x+1,y+1)
            gy = -L(x-1,y-1)-2*L(x,y-1)-L(x+1,y-1) + L(x-1,y+1)+2*L(x,y+1)+L(x+1,y+1)
            mag[y][x] = math.sqrt(gx*gx+gy*gy)
    cellW, cellH = hiW/cols, hiH/rows
    grid = [[max(mag[yy][xx] for yy in range(int(ry*cellH),int((ry+1)*cellH))
                             for xx in range(int(rx*cellW),int((rx+1)*cellW)))
             for rx in range(cols)] for ry in range(rows)]
    flat = sorted(v for row in grid for v in row)
    wp = max(0.02, flat[int(len(flat)*0.93)] or 1.0)
    return [["".join(RAMP[min(len(RAMP)-1, max(1, int((v/wp)*len(RAMP))))] if v/wp >= threshold else RAMP[0]
                      for v in row)] for row in grid]  # simplified; see project script for the working version
```
(This is trimmed for the skill doc — regenerate the exact tested version rather than trusting the excerpt blind if `threshold` behavior matters.) Once you have the character grid as plain rows of text, generate an SVG directly: one `<text>` (or `<tspan>`) per non-space character, positioned by `x = col*cellW`, `y = row*cellH`, colored via `fill`, with the animate-as-bonus pattern above. Skipping space characters keeps element count low (a real portrait is mostly blank).

## Constraints when the target is a Claude Artifact

- No remote `<img src>`, no `fetch`/XHR to external hosts — the CSP blocks it. Any real source photo/logo must be downloaded ahead of time (`curl`/`WebFetch`) and inlined as a `data:` URI.
- Canvas `getImageData` on a same-origin/data-URI image is fine (not tainted) — only cross-origin remote images would throw, and those can't load anyway under the CSP.
- Keep the whole page under the 16MB artifact cap — a single avatar-sized PNG (a few hundred KB) as base64 is negligible; don't inline multiple large images without checking total size.

## Gotcha: simulated keystroke typing corrupts large/emoji-heavy text in web code editors

Typing a long Markdown/code string (thousands of characters, several emoji) into a browser-based editor (GitHub's CodeMirror 6 file editor, and likely others) via simulated individual keystrokes can silently corrupt the result — observed failure: emoji characters got mangled into unrelated stray emoji at the very start of the document. Simulated `Ctrl+V` paste is also unreliable headlessly (`navigator.clipboard.writeText` can hang indefinitely waiting on a permission grant that never resolves in an automated context).

**Fix: focus the editor's contenteditable element and use `document.execCommand('insertText', false, content)` via JS injection**, after a `document.execCommand('selectAll')` to clear existing content first:
```js
const editable = document.querySelector('.cm-content'); // GitHub's CodeMirror 6 mount point
editable.focus();
document.execCommand('selectAll', false, null);
document.execCommand('insertText', false, fullMarkdownString);
```
This inserts the exact string as a single DOM operation the editor's input-event listener picks up correctly, sidestepping both the keystroke-corruption and the clipboard-permission hang. Verify by screenshotting the result before committing — don't trust the insert silently succeeded just because no error was thrown.

## Do not

- Don't ship a "live/animated" request as a static screenshot or a recolored copy of an existing static mockup — that is the exact failure this skill exists to prevent. If the ask is for a generative/animated mechanism, build the mechanism.
- Don't skip verifying in-browser. CSS/JS visual bugs (empty canvases, stalled animations, wrong contrast) are invisible from reading the code — screenshot the published result before calling it done.
