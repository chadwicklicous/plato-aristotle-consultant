#!/usr/bin/env python3
"""Extract Plato & Aristotle Greek TEI XML into citation-tagged segments.

Parses PerseusDL canonical-greekLit (Plato) and First1KGreek (Aristotle)
TEI/CTS XML files. Each segment becomes a CITATION\tTEXT row.

For Plato: citations use Stephanus page+letter (e.g. "Crito 43a").
For Aristotle: citations use work + section. Aristotle drawn from BOTH
First1KGreek and PerseusDL so the major works (Metaphysics, Ethics, Politics,
Rhetoric, Poetics) are covered.

Output: text/plato.tsv, text/aristotle.tsv
"""
import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
PG = os.path.join(REPO, '_pg', 'data')
F1K = os.path.join(REPO, '_f1k', 'data')
TEXT = os.path.join(BASE, 'text')
os.makedirs(TEXT, exist_ok=True)


def strip_tags(xml):
    xml = re.sub(r'<[^>]+>', '', xml)
    xml = xml.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    xml = xml.replace('&quot;', '"').replace('&apos;', "'")
    xml = re.sub(r'&#x([0-9a-fA-F]+);', lambda m: chr(int(m.group(1), 16)), xml)
    xml = re.sub(r'&#([0-9]+);', lambda m: chr(int(m.group(1))), xml)
    xml = re.sub(r'[<>]', ' ', xml)
    xml = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', xml)
    xml = re.sub(r'^\s*\d+\s+', '', xml)
    xml = re.sub(r'\s+', ' ', xml)
    return xml


def get_work_title(xml):
    m = re.search(r'<title xml:lang="grc">([^<]*)</title>', xml)
    if m and m.group(1).strip():
        return strip_tags(m.group(1)).strip()
    m = re.search(r'<title xml:lang="lat">([^<]*)</title>', xml)
    if m and m.group(1).strip():
        return strip_tags(m.group(1)).strip()
    m = re.search(r'<title[^>]*>([^<]*)</title>', xml)
    if m and m.group(1).strip():
        return strip_tags(m.group(1)).strip()
    return None


def get_author(xml):
    m = re.search(r'<author>([^<]*)</author>', xml)
    return m.group(1).strip() if m else None


def extract_plato():
    """Extract Plato (Stephanus citations)."""
    out = []
    files = sorted(glob.glob(os.path.join(PG, 'tlg0059', 'tlg*', 'tlg0059.tlg*.perseus-grc*.xml')))
    for f in files:
        with open(f, encoding='utf-8') as fh:
            xml = fh.read()
        title = get_work_title(xml) or os.path.basename(f)
        author = get_author(xml) or 'Plato'
        body = xml[xml.find('<body>'):]
        current = None
        for pm in re.finditer(r'<p\b[^>]*>(.*?)</p>', body, re.S):
            p_raw = pm.group(1)
            p_text = strip_tags(p_raw).strip()
            ms = re.search(r'milestone\b[^>]*\bn="([0-9]+[a-e]?)"[^>]*\bunit="section"[^>]*\bresp="Stephanus"', p_raw)
            if not ms:
                ms = re.search(r'milestone\b[^>]*\bunit="section"[^>]*\bresp="Stephanus"[^>]*\bn="([0-9]+[a-e]?)"', p_raw)
            if ms:
                current = ms.group(1)
            if len(p_text) < 20:
                continue
            out.append((f"{author} | {title} | {current or ''}", p_text))
    return out


def extract_aristotle():
    """Extract Aristotle from First1K + PerseusDL (handle nested divs, <p> attrs)."""
    out = []
    seen = set()
    f1k_files = sorted(glob.glob(os.path.join(F1K, 'tlg0086', 'tlg*', 'tlg0086.tlg*.1st1K-grc*.xml')))
    pg_files = sorted(glob.glob(os.path.join(PG, 'tlg0086', 'tlg*', 'tlg0086.tlg*.perseus-grc*.xml')))

    for f in f1k_files + pg_files:
        with open(f, encoding='utf-8') as fh:
            xml = fh.read()
        title = get_work_title(xml) or os.path.basename(f)
        author = get_author(xml) or 'Aristotle'
        if title in seen:
            continue
        seen.add(title)
        body = xml[xml.find('<body>'):]
        # walk: track current section from textpart div n=, extract each <p> (with attrs)
        current = ''
        for m in re.finditer(r'(<div type="textpart"[^>]*>)|(<p\b[^>]*>.*?</p>)', body, re.S):
            if m.group(1):
                dm = re.search(r'n="([^"]*)"', m.group(1))
                if dm:
                    current = dm.group(1)
            elif m.group(2):
                pt = strip_tags(m.group(2)).strip()
                if len(pt) >= 20:
                    out.append((f"{author} | {title} | {current}", pt))
    return out


if __name__ == '__main__':
    print("Extracting Plato...")
    plato = extract_plato()
    print(f"  {len(plato)} segments")
    with open(os.path.join(TEXT, 'plato.tsv'), 'w', encoding='utf-8') as f:
        for cit, text in plato:
            f.write(f"{cit}\t{text}\n")

    print("Extracting Aristotle...")
    aristotle = extract_aristotle()
    print(f"  {len(aristotle)} segments")
    with open(os.path.join(TEXT, 'aristotle.tsv'), 'w', encoding='utf-8') as f:
        for cit, text in aristotle:
            f.write(f"{cit}\t{text}\n")

    print(f"Done: {len(plato)} Plato + {len(aristotle)} Aristotle segments")
