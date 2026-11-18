---
name: truth-in-love
description: Check any draft the owner will send or post, and any money step, against the owner's written, scripture-grounded principles. Returns at most a short note with the principle and verse, a suggested rewrite in the owner's voice, and one thing to learn, or nothing when nothing needs changing. Use before showing the owner any draft and before preparing any purchase, subscription, giving change, loan or investment step.
---

# Truth in love

A Claude skill wrapper around the prompts in this repo. Copy this folder to `~/.claude/skills/truth-in-love/`
and copy `principles.md`, `prompts/check-draft.md` and `prompts/money-pause.md` beside this file.

1. Read `principles.md` once per session before the first check.
2. For a draft, follow `check-draft.md` exactly.
3. For a money step, follow `money-pause.md` exactly.

It guides and never blocks. The owner decides. It adds to Claude's built-in safety rules and never replaces
them.

Optional scripts (plain Python 3, no packages): `scripts/heart_check.py <draft.txt>` lists stock phrases and
first-person heart claims to confirm; `scripts/reader_check.py <draft.txt>` checks that an email is plain
enough for a non-technical reader.
