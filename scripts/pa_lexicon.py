#!/usr/bin/env python3
"""Greek-English lexicon lookup (LSJ, 9th ed.) for the Plato/Aristotle consultant.

Wraps the clean LSJ data (ciscoriordan/lsj9, CC-BY) so the consultant can look up
the definition of any Greek word found in the corpus. Used to aid translation:
given a Greek term, returns its headword, grammar, etymology, and English gloss.

Data files (from _lsj/):
  - lsj9_headwords.json   -> [{id, headword, grammar, etymology}]
  - lsj9_glosses.jsonl    -> [{headword, text, gloss_id}]  (full definitions)
  - lsj9_short_defs.json  -> {headword: short_definition}

Usage:
  python pa_lexicon.py --lookup "τίθημι"          # exact Greek headword
  python pa_lexicon.py --search "love"            # English -> Greek headwords
  python pa_lexicon.py --forms "τίθημι"           # show inflected forms
"""
import os, sys, json

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
LSJ = os.path.join(REPO, '_lsj')

# Load headwords (lazy)
_HEADWORDS = None
_GLOSSES = None
_SHORT = None

def _load():
    global _HEADWORDS, _GLOSSES, _SHORT
    if _HEADWORDS is None:
        with open(os.path.join(LSJ, 'lsj9_headwords.json'), encoding='utf-8') as f:
            _HEADWORDS = json.load(f)
    if _SHORT is None:
        with open(os.path.join(LSJ, 'lsj9_short_defs.json'), encoding='utf-8') as f:
            _SHORT = json.load(f)
    if _GLOSSES is None:
        _GLOSSES = {}
        with open(os.path.join(LSJ, 'lsj9_glosses.jsonl'), encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                _GLOSSES[rec.get('headword','')] = rec.get('text','')

def lookup_exact(term):
    """Return the LSJ entry for an exact Greek headword."""
    _load()
    term = term.strip()
    # exact headword match
    for rec in _HEADWORDS:
        if rec.get('headword') == term:
            gloss = _GLOSSES.get(term) or _SHORT.get(term) or '(no gloss)'
            return {
                'headword': term,
                'grammar': rec.get('grammar',''),
                'etymology': rec.get('etymology',''),
                'definition': gloss,
            }
    # try stripping breathing marks / accents? For now, substring match on headword
    matches = [r for r in _HEADWORDS if term in r.get('headword','')]
    if matches:
        m = matches[0]
        gloss = _GLOSSES.get(m.get('headword','')) or _SHORT.get(m.get('headword','')) or '(no gloss)'
        return {
            'headword': m.get('headword',''),
            'grammar': m.get('grammar',''),
            'etymology': m.get('etymology',''),
            'definition': gloss,
            'note': f'closest headword ({len(matches)} partial matches)',
        }
    return None

def search_english(term):
    """Search glosses for an English word, return matching Greek headwords."""
    _load()
    term = term.lower()
    hits = []
    for hw, defn in _SHORT.items():
        if term in defn.lower():
            hits.append(hw)
    return hits[:20]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(0)
    mode, term = sys.argv[1], sys.argv[2]
    if mode == '--lookup':
        r = lookup_exact(term)
        if r:
            print(f"Greek: {r['headword']} ({r.get('grammar','')})")
            if r.get('etymology'): print(f"Etym: {r['etymology']}")
            print(f"Def: {r['definition']}")
        else:
            print(f"No LSJ entry for {term!r}")
    elif mode == '--search':
        hits = search_english(term)
        print(f"Greek headwords matching English {term!r}:")
        for h in hits:
            print(f"  {h}: {_SHORT.get(h,'')[:60]}")
