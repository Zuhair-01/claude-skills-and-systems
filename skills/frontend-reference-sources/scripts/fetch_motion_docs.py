#!/usr/bin/env python3
"""Fetch motion.dev docs — token-cheap, no deps.

  python fetch_motion_docs.py                 -> prints the llms.txt index (all doc URLs + blurbs)
  python fetch_motion_docs.py <substr>        -> prints index lines matching <substr> (e.g. "scroll", "gesture")
  python fetch_motion_docs.py <full-doc-url>  -> prints that doc page as text

motion.dev serves a stable text/plain llms.txt index; feed a page URL back in to read it.
ponytail: dumb urllib fetch, upgrade to caching if it's hit a lot.
"""
import sys, re, urllib.request

INDEX = "https://motion.dev/llms.txt"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg and arg.startswith("http"):
        html = get(arg)
        text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", "", html)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        print(text)
        return
    idx = get(INDEX)
    if arg:
        for line in idx.splitlines():
            if arg.lower() in line.lower():
                print(line)
    else:
        print(idx)


if __name__ == "__main__":
    main()
