# The Long Roast: Lawmakers and the File They Cannot Convert — make.fun bounty
# u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7
#
# The program writes one satirical sentence (1-320 characters) to
# /output/entry.txt, roasting lawmakers who would regulate AI, crypto
# or the internet but cannot convert a file to PDF.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a one-sentence roast on the subject: lawmakers, the rules they
#      write, and the file they cannot convert
#   2. a real turn: the sentence sets up the lawmaker's authority and
#      then undercuts it with the file
#   3. aim stays on lawmakers and power/competence, not random abuse
#   4. reads clean in one pass, quotable, punch on the last few words
#   5. a specific, unexpected detail over a worn tech-illiteracy cliche
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: subject 10, turn 10, aim 9, clean 9, fresh 10 = 48
    ("They write the laws for AI, crypto and the internet, then print "
     "the email, sign the printout, scan it back in and call IT because "
     "the PDF they just made is somehow a photograph of their desk.",
     48),
    # score: subject 10, turn 9, aim 10, clean 9, fresh 9 = 47
    ("They can ban an algorithm before breakfast, yet the PDF button "
     "has defeated them for a decade — the only file they have ever "
     "successfully converted is a campaign promise into a press release.",
     47),
    # score: subject 9, turn 9, aim 9, clean 9, fresh 9 = 45
    ("He chairs the committee on artificial intelligence, regulates "
     "crypto before lunch and the internet by dinner, yet his staff "
     "still converts his files to PDF for him — the only thing in his "
     "office that ever gets converted is a campaign promise into a "
     "press release.",
     45),
    # score: subject 9, turn 8, aim 9, clean 9, fresh 8 = 43
    ("Congress can draft a 900-page bill to govern artificial "
     "intelligence, but ask them to turn a Word file into a PDF and "
     "suddenly the future of technology is a three-week IT ticket.",
     43),
    # score: subject 9, turn 8, aim 8, clean 9, fresh 8 = 42
    ("They will legislate the algorithm, the blockchain and the whole "
     "internet, then email you a scanned photo of a printed Word "
     "document and ask why the PDF button doesn't work.",
     42),
    # score: subject 9, turn 8, aim 9, clean 8, fresh 8 = 42
    ("They regulate artificial intelligence, crypto and the entire "
     "internet, yet the one file format that has ever truly stumped "
     "them is the PDF — so their staff prints the bill, and the future "
     "of technology arrives by fax.",
     42),
]

# The gate requires 1-320 characters of non-whitespace UTF-8 text,
# one sentence, standing alone.
MAX_CHARS = 320


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        # One sentence: exactly one sentence-ending full stop, at the end.
        assert text.count(".") == 1 and text.endswith("."), \
            f"candidate is not one sentence: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    roast = pick(CANDIDATES)
    import hashlib
    import os
    expected_sha256 = hashlib.sha256(roast.encode("utf-8")).hexdigest()
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(roast)
    # Verify what was actually written: the gate reads this file, not stdout.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == roast, "entry.txt differs from the chosen line"
    assert hashlib.sha256(written.encode("utf-8")).hexdigest() == \
        expected_sha256, "entry.txt sha256 mismatch"
    assert 1 <= len(written.strip()) <= MAX_CHARS, \
        "entry.txt outside the gate"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    assert written.count(".") == 1 and written.endswith("."), \
        "entry.txt must be exactly one sentence"
    print(roast)


if __name__ == "__main__":
    main()
