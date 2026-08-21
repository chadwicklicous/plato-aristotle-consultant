#!/usr/bin/env python3
"""Extract the Oxford Grammar of Classical Greek PDF into citation-tagged segments.

The grammar is a clean-text PDF (292 pages) with real Greek. We split it into
per-page segments, each tagged with the page number, preserving Greek diacritics.

Output: text/greek_grammar.tsv  (CITATION\tTEXT)
"""
import fitz, os, re

PDF = r"C:\Users\philo\deep-research\.hermes\desktop-attachments\11 The Oxford Grammar of Classical Greek.pdf"
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'text', 'greek_grammar.tsv')

doc = fitz.open(PDF)
os.makedirs(os.path.dirname(OUT), exist_ok=True)

with open(OUT, 'w', encoding='utf-8') as f:
    for i in range(doc.page_count):
        text = doc[i].get_text()
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) < 30:
            continue
        cit = f"Oxford Greek Grammar | page {i+1}"
        f.write(f"{cit}\t{text}\n")

print(f"Wrote {os.path.getsize(OUT)} bytes to {OUT}")
