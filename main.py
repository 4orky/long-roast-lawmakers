"""One-line roast for the make.fun bounty "The Long Roast: Lawmakers and
the File They Cannot Convert" (u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7).

The script drafts a slate of single-sentence roasts, grades every draft on
five craft dimensions, keeps the strongest draft, and stores it as the
entry in /output/entry.txt. Grading is fully deterministic, so repeated
runs produce byte-identical output.
"""

from hashlib import sha256
from pathlib import Path
import sys

ENTRY_PATH = Path("/output/entry.txt")
CHAR_CEILING = 320

WEIGHTS = {"subject": 3, "reversal": 3, "targeting": 2, "readability": 2, "surprise": 2}

DRAFTS = [
    {
        "text": "They write the laws for AI, crypto and the internet, then print the email, sign the printout, scan it back in and call IT because the PDF they just made is somehow a photograph of their desk.",
        "grades": {"subject": 10, "reversal": 10, "targeting": 9, "readability": 9, "surprise": 10},
    },
    {
        "text": "They can outlaw an algorithm before lunch, yet the button that turns a document into a PDF has outwitted them for ten years, so their aides still print every attachment and file it under miscellaneous.",
        "grades": {"subject": 10, "reversal": 9, "targeting": 10, "readability": 9, "surprise": 9},
    },
    {
        "text": "The committee that writes the rules for artificial intelligence just asked its intern how to save a file, because the future they keep legislating arrives in their inbox as a scanned photograph of a printed email.",
        "grades": {"subject": 9, "reversal": 9, "targeting": 9, "readability": 10, "surprise": 9},
    },
    {
        "text": "They govern the cloud, the blockchain and every chatbot on earth, but the office printer remains their most trusted colleague, converting each urgent memo into a warm stack of paper nobody can search.",
        "grades": {"subject": 9, "reversal": 9, "targeting": 9, "readability": 9, "surprise": 9},
    },
    {
        "text": "He can explain how a neural network should be regulated for an hour, yet his own laptop holds a folder called FINAL_final_v2 that nobody, including him, dares to open.",
        "grades": {"subject": 9, "reversal": 8, "targeting": 9, "readability": 9, "surprise": 9},
    },
    {
        "text": "Lawmakers will happily debate the sentience of machines until midnight, then spend the morning asking IT why the document they photographed is still not a PDF.",
        "grades": {"subject": 9, "reversal": 8, "targeting": 9, "readability": 8, "surprise": 9},
    },
    {
        "text": "They wrote three hundred pages of law about data portability and then emailed the bill to each other as a photograph of a screen, because the export menu was obviously far too powerful to touch.",
        "grades": {"subject": 8, "reversal": 9, "targeting": 9, "readability": 9, "surprise": 8},
    },
    {
        "text": "The senator who wants every algorithm audited keeps his passwords on a sticky note, his drafts in a drawer, and his faith in a grandson who visits on Sundays to fix the Wi-Fi.",
        "grades": {"subject": 9, "reversal": 8, "targeting": 8, "readability": 9, "surprise": 8},
    },
    {
        "text": "Their plan to govern the internet fits on one page, mostly because the second page jammed in the printer, and the third page was scanned upside down and saved as a photograph of the carpet.",
        "grades": {"subject": 8, "reversal": 8, "targeting": 9, "readability": 9, "surprise": 8},
    },
    {
        "text": "She chairs the subcommittee on emerging technology and still believes the cloud is a filing cabinet somewhere in Virginia that a very polite man empties every Friday.",
        "grades": {"subject": 8, "reversal": 8, "targeting": 8, "readability": 9, "surprise": 8},
    },
    {
        "text": "They demand a backdoor into every encrypted message on the planet, yet the only door they have ever successfully opened is the one to the supply closet where the toner lives.",
        "grades": {"subject": 8, "reversal": 7, "targeting": 8, "readability": 9, "surprise": 8},
    }]


def _weighted_total(grades):
    tally = 0
    for dimension, weight in WEIGHTS.items():
        # A missing grade counts as zero instead of crashing the run.
        tally += grades.get(dimension, 0) * weight
    return tally


def _check_line(text):
    stripped = text.strip()
    if not stripped:
        raise ValueError("draft is empty")
    if len(stripped) > CHAR_CEILING:
        raise ValueError(f"draft runs {len(stripped)} characters, over the {CHAR_CEILING} ceiling")
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("draft must stay on one line")
    if "  " in stripped:
        raise ValueError("draft contains a double space")
    if stripped.count(".") != 1 or not stripped.endswith("."):
        raise ValueError(f"draft must be exactly one sentence: {stripped!r}")


def _choose(drafts):
    if not drafts:
        raise ValueError("no drafts to grade")
    front_runner = None
    front_score = None
    for draft in drafts:
        _check_line(draft["text"])
        tally = _weighted_total(draft["grades"])
        ranking = (tally, -len(draft["text"]))
        if front_score is None or ranking > front_score:
            front_score = ranking
            front_runner = draft["text"]
    return front_runner


def _emit(line):
    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENTRY_PATH.write_text(line, encoding="utf-8")
    reread = ENTRY_PATH.read_text(encoding="utf-8")
    if reread != line:
        raise ValueError("entry file does not match the chosen line")
    if reread != reread.strip():
        raise ValueError("entry file has leading or trailing whitespace")
    digest = sha256(reread.encode("utf-8")).hexdigest()
    if digest != sha256(line.encode("utf-8")).hexdigest():
        raise ValueError("entry file hash does not match the chosen line")
    if len(reread.strip()) > CHAR_CEILING:
        raise ValueError("entry file over the character ceiling")
    sys.stdout.write(line + "\n")


def _launch():
    chosen = _choose(DRAFTS)
    _emit(chosen)


_RUN_AS_SCRIPT = __name__ == "__main__"
if _RUN_AS_SCRIPT:
    _launch()
