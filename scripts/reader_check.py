#!/usr/bin/env python3
"""Check that an email draft is plain enough for the person who will read it (principle 17).

Usage: reader_check.py DRAFT.txt|DRAFT.html [--reader nontech|tech]
  nontech: readers who do not write code (the default)
  tech:    engineers (only the readability checks run)
Exit 1 when a draft fails. The plain-language checks follow the US Plain Writing Act guidance as packaged in
surendranb/writing-skills (MIT): front-load the point, short sentences, common words, Flesch reading ease 60+.
English only.
"""
import argparse
import html
import re
import sys

# Words and shapes a non-technical reader should not have to decode. Say what they will see or do instead.
NONTECH = [
    r"\b[A-Z]{1,3}-[A-Z0-9]{6,}\b",          # tracking and measurement ids
    r"\b\d{6,}\b",                            # property, stream, account, project ids
    r"\b(data )?streams?\b", r"measurement id", r"\bproperty id\b", r"\bconfig(uration)?\b",
    r"\bAPI\b", r"\bSDK\b", r"\brepo(sitory)?\b", r"\bPR\b", r"pull request", r"\bmerge[ds]?\b",
    r"\bdeploy(ed|ment|s)?\b", r"\bstaging\b", r"\bprod(uction)?\b", r"\bbackend\b", r"\bfrontend\b",
    r"\bDNS\b", r"\bendpoint\b", r"\bschema\b", r"\bmigration\b",
    r"\bfeature flag\b", r"\bterraform\b", r"\bgithub\b", r"\bCI\b", r"\bJSON\b", r"\bOAuth\b",
    r"exactly matches", r"\bhosting\b", r"\bdashboard id\b",
]
NONTECH_RX = re.compile("|".join(NONTECH), re.I)
JARGON = re.compile(r"\b(utilize|leverage|facilitate|commence|pursuant to|aforementioned|henceforth|"
                    r"in the event that|with regard to|per our|as per)\b", re.I)
URL = re.compile(r"https?://\S+")


def to_text(raw):
    """Strip HTML to visible text; href targets are not read by the reader, so they are dropped."""
    if "<" in raw and ">" in raw:
        raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
        raw = re.sub(r"(?i)<br\s*/?>|</(p|li|h\d|div|tr)>", "\n", raw)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = html.unescape(raw)
    return raw


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def sentences(text):
    text = URL.sub(" ", text)
    out = []
    for line in text.split("\n"):
        line = line.strip(" -*\t")
        if not line or len(line.split()) < 3:   # greetings, sign-offs, headings
            continue
        out += [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if len(s.split()) >= 3]
    return out


def flesch(sents):
    words = [w for s in sents for w in re.findall(r"[A-Za-z']+", s)]
    if not words or not sents:
        return 100.0
    syl = sum(syllables(w) for w in words)
    return 206.835 - 1.015 * (len(words) / len(sents)) - 84.6 * (syl / len(words))


def check(raw, reader="nontech"):
    text = to_text(raw)
    sents = sentences(text)
    problems = []
    score = flesch(sents)
    floor = 60 if reader == "nontech" else 45
    if score < floor:
        problems.append(f"reading ease {score:.0f}, want {floor}+: shorter sentences, shorter words")
    for s in sents:
        if len(s.split()) > 25:
            problems.append(f"long sentence ({len(s.split())} words): {s[:70]}...")
    for m in JARGON.finditer(text):
        problems.append(f"jargon: {m.group(0)}")
    if reader == "nontech":
        # On-screen labels the reader must click (<b class="ui">Stream name</b>) are allowed: they match the screen.
        labels = re.sub(r'(?is)<b class="ui">.*?</b>', " ", raw)
        visible = URL.sub(" ", to_text(labels))
        for m in NONTECH_RX.finditer(visible):
            a = max(0, m.start() - 30)
            problems.append(f"technical for this reader: \"{m.group(0)}\" in ...{visible[a:m.end() + 30]!r}")
        if len(URL.findall(text)) > 0 and "<a " not in raw.lower():
            problems.append("bare link: put it behind words (<a href>) in the HTML version")
    return score, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--reader", choices=["nontech", "tech"], default="nontech")
    a = ap.parse_args()
    score, problems = check(open(a.path, errors="replace").read(), a.reader)
    for p in problems:
        print(p)
    print(f"reader ok (reading ease {score:.0f})" if not problems else f"{len(problems)} reader problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
