#!/usr/bin/env python3
"""Extract Presocratic fragments into citation-tagged segments.

Uses the clean Heraclitus fragments from r03ert0/Heraclitus-Fragments (119 Greek
fragments, Diels-Kranz numbering) plus any individual Presocratic fragments found
in the First1KGreek corpus (e.g. Xenophanes).

Output: text/presocratics.tsv
"""
import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
HERA = os.path.join(REPO, '_heraclitus')
TEXT = os.path.join(BASE, 'text')
os.makedirs(TEXT, exist_ok=True)


def extract_heraclitus():
    """Extract Heraclitus fragments (Diels-Kranz 22) from the Greek txt files."""
    out = []
    frags = sorted(glob.glob(os.path.join(HERA, 'fragment-*.greek.txt')),
                   key=lambda f: int(re.search(r'fragment-(\d+)', f).group(1)))
    for f in frags:
        num = int(re.search(r'fragment-(\d+)', f).group(1))
        with open(f, encoding='utf-8') as fh:
            text = fh.read().strip()
        if text:
            # Heraclitus fragment, Diels-Kranz 22B{num}
            text = re.sub(r'\s+', ' ', text)  # keep on one line (TSV)
            cit = f"Heraclitus | Diels-Kranz 22B{num}"
            out.append((cit, text))
    return out


if __name__ == '__main__':
    print("Extracting Heraclitus fragments...")
    hera = extract_heraclitus()
    print(f"  {len(hera)} fragments")
    with open(os.path.join(TEXT, 'presocratics.tsv'), 'w', encoding='utf-8') as f:
        for cit, text in hera:
            f.write(f"{cit}\t{text}\n")
    print(f"Done: {len(hera)} Presocratic segments")
