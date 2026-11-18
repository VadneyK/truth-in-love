# truth-in-love

A small set of written principles, prompts and two scripts that make an AI assistant check what you are
about to send, and what you are about to spend, against Scripture as you read it. It suggests. You decide.

> Speaking the truth in love (Ephesians 4:15).

It was written by one Christian software engineer for his own daily use. It has had one user. It is offered
as a starting point for others to change, not as a finished product or a standard.

## What it does

- **Before a message goes out:** the assistant reads your draft against 26 short principles (truthful words,
  no flattery, no promises you did not make, no invented feelings, gentleness, humility, care for the
  reader). If something matters, you get at most three lines: a note naming the principle and verse, a
  suggested rewrite in your own voice, and one thing to learn. If nothing matters, you get nothing.
- **Before a money step:** the assistant pauses and asks before a new subscription, a change in giving, new
  debt, an investment move or a large purchase. It never moves money itself.
- **Two small scripts:** one lists stock phrases, empty promises and first-person "heart claims" for you to
  confirm; one checks that an email is plain enough for a reader who does not write code.
- **Two drafts, less tested:** six weekly review questions with no scores and no streaks, and a prompt that
  returns at most five keyword bullets before a conversation.

## What it is not

- **Not accountability software.** It does not watch a screen, filter the web, block anything or report to
  another person. No human accountability partner is part of it. It only looks at text you hand it.
- **Not a pastor and not a judge.** Questions of calling, sin, church and doctrine belong with the people God
  has placed over you. The prompts tell the assistant to say so.
- **Not a doctrine statement.** The principles are one believer's reading, written from an evangelical
  Protestant conviction that Scripture is the final authority. The verse chosen for each principle is his
  choice. Read the passages and change the list.
- **Not a check on truth of Bible quotations.** It cites references only. For checking that a reference
  exists and a quotation matches the text, see the separate project
  [chapter-and-verse](https://github.com/VadneyK/chapter-and-verse).
- **Not proven.** There is no study showing it makes anyone more truthful or more loving. A phrase list
  cannot read a heart, and a model can miss things or be wrong.

## If you are a pastor or ministry leader

You do not need to install anything to judge whether this is sound. Read two files:

1. [principles.md](principles.md): the 26 principles and the passages they rest on.
2. [prompts/check-draft.md](prompts/check-draft.md): the exact instructions the assistant follows.

Things worth your judgment: whether each verse is used in keeping with its context, whether anything
important is missing, and whether a tool like this helps a person grow or lets them hand off what should be
their own heart work. The author would be glad to be corrected on any of it.

## If you are a developer

Works with any assistant that takes a system prompt. Nothing here calls a network or needs a package.

1. Put `prompts/check-draft.md` followed by `principles.md` in the system prompt or project instructions.
   Add `prompts/money-pause.md` if you want the money pause, and set your own amounts.
2. For Claude Code or the Claude apps, copy `skill/truth-in-love/` to `~/.claude/skills/` and place the
   three files beside `SKILL.md` as it says.
3. Scripts (Python 3.9 or newer):

   ```bash
   python3 scripts/heart_check.py draft.txt
   python3 scripts/reader_check.py draft.txt --reader nontech
   python3 scripts/test_checks.py
   ```

To adapt it: edit `principles.md` first. The prompts refer to principles by number, so update the numbers in
"What to look for" when you add or remove one. Keep the rules that matter most: say nothing when nothing
needs changing, one issue per draft, never change the meaning, never preach, the owner decides.

## What stays personal

The author's own setup has more in it than this repo: his own facts file, rules about specific people and
groups, his voice profile, his amounts, and the plumbing that shows drafts on a board. None of that is here,
on purpose. Your convictions and your people are yours to write down.

The plumbing (leases, a send gate, a board of asks) is a separate kit:
[steward-hub](https://github.com/VadneyK/steward-hub).

## Privacy

Your drafts go to whichever AI provider you use, under that provider's terms. The scripts run on your own
computer and send nothing anywhere. This repo collects nothing.

## Feedback

Please [open an issue](https://github.com/VadneyK/truth-in-love/issues): a verse used out of context, a
principle that is missing or wrong, a check that misfired, or a question. Corrections from pastors are
especially welcome. Nothing here collects data, so issues are the only way the author hears what helps.

## Licence

MIT. Scripture references link to the Berean Standard Bible (public domain). No Bible text is included.
