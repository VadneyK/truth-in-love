#!/usr/bin/env python3
"""List phrases in a draft that deserve a second look before it is sent in your name.

Three groups, each tied to a principle in principles.md:
  stock    phrases that read as written by a model or a template, not by you (principle 3)
  promise  offers of your time or outcomes you may not have made (principle 10), and lines that
           position your own motives (principle 12)
  heart    first-person feelings, prayers and memories: fine when true, to confirm each time (principle 11)

Usage: heart_check.py DRAFT.txt [--extra my_phrases.txt]
Exit 1 when a stock or promise phrase is found. Heart claims are printed and never change the exit code:
only you know whether they are true. A phrase list cannot read a heart; this is a prompt to reread, no more.
"""
import argparse
import re
import sys

STOCK = [
    r"i hope this (finds|helps)", r"i wanted to reach out", r"just wanted to", r"great question",
    r"circle back", r"\bdelve", r"\bleverage", r"\bseamless", r"\brobust\b", r"\bcomprehensive\b",
    r"\badditionally\b", r"it'?s worth noting", r"in summary", r"to be clear", r"rest assured",
    r"not (just|only) [^.]{1,40}, but", r"feel free to", r"don'?t hesitate", r"\butilize\b",
    r"game.?changer", r"\bthrilled\b", r"excited to share", r"\bunlock", r"\bsupercharge", r"\bempower",
    r"\btapestry", r"at its core", r"let that sink in", r"important to note",
]
PROMISE = [
    r"i'll make sure", r"anytime you need", r"happy to help", r"i'?d love to",
    r"hoping to (come|make it|join|be there)", r"if you want help",
    r"if you (ever )?(want|need|would like)\b[^.\n]{0,70}\bi(?:'|’)?m happy to\b",
    r"i'?d rather [^.]{0,60}\bthan\b", r"i don'?t want to (build|duplicate|step on|reinvent)",
    r"i'?ve been thinking about how (i can|to) (help|serve)",
]
HEART = [
    r"\bi'?m (so |really |very |truly )?(excited|passionate|honou?red|blessed|humbled|moved|touched)\b",
    r"\bi'?ve been (reflecting|praying|thinking a lot)\b", r"\bpraying for (you|your)\b",
    r"\bi'?ll (be )?pray(ing)?\b", r"(means|meant) (so much|a lot|the world) to me",
    r"\bi (still )?remember (when|how|that)\b", r"\bfrom the bottom of my heart\b",
    r"\bdeeply (grateful|moved|touched|care)\b", r"\bi truly\b", r"\bmy heart (is|goes|was)\b",
    r"\b(really )?resonate[sd]? with me\b", r"\bi'?ve always (wanted|loved|been drawn)\b",
]


def compile_group(patterns):
    return re.compile("|".join(patterns), re.I)


def find(text, extra=()):
    """Return a list of (group, phrase, context)."""
    groups = [("stock", compile_group(STOCK + list(extra))), ("promise", compile_group(PROMISE)),
              ("heart", compile_group(HEART))]
    out = []
    for name, rx in groups:
        for m in rx.finditer(text):
            a = max(0, m.start() - 40)
            out.append((name, m.group(0), text[a:m.end() + 40].replace("\n", " ")))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--extra", help="a file of your own stock phrases, one regular expression per line")
    a = ap.parse_args()
    extra = []
    if a.extra:
        extra = [ln.strip() for ln in open(a.extra, encoding="utf-8") if ln.strip() and not ln.startswith("#")]
    hits = find(open(a.path, encoding="utf-8", errors="replace").read(), extra)
    for group, phrase, ctx in hits:
        print(f"{group}: \"{phrase}\" in ...{ctx}...")
    hard = [h for h in hits if h[0] != "heart"]
    heart = [h for h in hits if h[0] == "heart"]
    if heart:
        print(f"{len(heart)} heart claim(s): keep each only if it is true of you")
    print("ok" if not hard else f"{len(hard)} phrase(s) to reread")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
