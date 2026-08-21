# Plato, Aristotle & Presocratics Consultant

A citation-grounded research consultant for **Plato, Aristotle, and the Presocratic
philosophers**, answering **from the original Greek** with exact scholarly citations
(Stephanus page numbers for Plato, Bekker numbers for Aristotle, Diels-Kranz for
Heraclitus) — not from a translation or a model's recollection.

## What it does

1. Downloads the clean original-Greek texts from the Perseus Digital Library and
   the Open Greek and Latin project:
   - **Plato** (all 36 canonical works) — the Perseus canonical Greek text, Stephanus pagination
   - **Aristotle** (40 works) — the First1KGreek corpus, Bekker pagination
   - **Heraclitus** — 119 Diels-Kranz fragments (22B)
2. Extracts 13,706 citation-tagged segments, each `CITATION\tTEXT`.
3. Builds a ChromaDB vector index (bge-m3, 1024-dim, multilingual) for semantic search.
4. Answers questions by retrieving the relevant Greek passages with exact citations.

## Coverage

| Author | Works | Segments | Citation format |
|--------|-------|----------|-----------------|
| **Plato** | All 36 canonical works (Euthyphro, Apology, Crito, Republic, Symposium, etc.) | 9,771 | `Plato \| Ἀπολογία Σωκράτους \| 17` (Stephanus) |
| **Aristotle** | 40 works (Categories, Analytics, Metaphysics, Ethics, De anima, etc.) | 3,816 | `Aristotle \| Analytica priora \| priora` (Bekker) |
| **Heraclitus** | 119 fragments | 119 | `Heraclitus \| Diels-Kranz 22B1` |

### Not yet included (deferred)

The full **Diels-Kranz Presocratic corpus** (Anaximander, Parmenides, Empedocles,
Democritus, and the other fragmentary Presocratics) is **not included**, because no
clean, machine-readable original-Greek source is freely available. The only complete
collection is the Thesaurus Linguae Graecae (TLG), which is subscription-gated. If a
clean edition is sourced (including via TLG), the fragmentary Presocratics can be added
following the same pattern. Heraclitus is included via the public-domain Diels-Kranz
text; the rest are flagged as deferred.

## Supplemental translation tools

Beyond the corpus itself, the consultant works with the standard reference works for
translating the original Greek (and, for the wider Latin tradition, the Latin dictionaries).
These are **not bundled** in the repo (they are large, and the OLD is copyrighted); the
user downloads them for local use and they are indexed as translation aids.

| Tool | What it is | Source (download for local use) |
|------|-----------|--------------------------------|
| **Liddell-Scott Greek-English Lexicon (LSJ)** | The standard Greek-English lexicon; 111,506 headwords, machine-readable | `https://github.com/ciscoriordan/lsj9` (CC-BY 4.0, clean JSON/TSV) |
| **Oxford Grammar of Classical Greek** | Reference grammar of Classical Greek | `https://archive.org/details/oxfordgrammarofc0000jame` (or your own copy of the OUP grammar) |
| **Oxford Latin Dictionary (Glare)** | The standard Latin-English dictionary | `https://archive.org/details/oxford-latin-dictionary-p.-g.-w.-glare` (DJVU/EPUB; copyrighted — for personal research use) |

- **LSJ (Greek)** is indexed by the bundled `pa_lexicon.py` tool — after cloning
  `ciscoriordan/lsj9` into the repo's `_lsj/` folder, run:
  ```bash
  python pa_lexicon.py --lookup "τίθημι"   # Greek word -> English definition
  python pa_lexicon.py --search "love"      # English -> matching Greek headwords
  ```
- The **Oxford Grammar of Greek** is extracted by `pa_extract_grammar.py` into the corpus
  as a grammar reference.
- The **Oxford Latin Dictionary** is copyrighted (Oxford UP); it is intended for **personal research use only** and is kept local, not redistributed. It can be indexed into the Thomistic/Patristic consultants as a Latin lexicon if you have a legitimate copy.

> **Note on sources:** These are supplementary reference works a researcher would legitimately possess or obtain from the public archive links above. The Liddell-Scott (LSJ) is CC-BY; the Oxford Grammar is widely available; the Oxford Latin Dictionary is the standard lexicographical text (copyrighted — use under your own judgment, per license/fair-use for personal research).

## Requirements

- **Python 3.9+** (stdlib only for the pipeline; `chromadb` for the index)
- **ChromaDB** — `pip install "chromadb==1.5.9"` (in `requirements.txt`). Runs embedded.
- **Ollama** — the embedding provider (free, local, no API key). Pull `bge-m3` with `ollama pull bge-m3` (multilingual — required for Greek).

## Quick start

```bash
# 1. Install dependencies
pip install "chromadb==1.5.9"

# 2. Pull the embedding model
ollama pull bge-m3

# 3. Build the corpus (downloads the Greek XML from Perseus/OGL)
cd scripts
# (the repos are cloned and extracted by the scripts)

# 4. Extract citation-tagged segments
python pa_extract.py            # Plato + Aristotle
python pa_extract_presoc.py     # Heraclitus fragments

# 5. Build the vector index
python pa_index.py

# 6. Query — in Greek (original)
python pa_index.py --query "τὸ ἀγαθὸν" --k 5
# or in English (bge-m3 is multilingual)
python pa_index.py --query "the form of the good" --k 5
```

## The scripts

| Script | Purpose |
|--------|---------|
| `pa_extract.py` | Splits Plato + Aristotle Greek XML into citation-tagged segments |
| `pa_extract_presoc.py` | Extracts Heraclitus fragments (Diels-Kranz) |
| `pa_index.py` | Builds/updates the ChromaDB vector index; runs `--query` |

## Citation format

| Form | Meaning |
|------|---------|
| `Plato \| Απολογία Σοκράτους \| 17` | Plato, Apology, Stephanus page 17 |
| `Plato \| Εὐθύφρων \| 2a` | Plato, Euthyphro, Stephanus 2a |
| `Aristotle \| Analytica priora` | Aristotle, Prior Analytics |
| `Heraclitus \| Diels-Kranz 22B1` | Heraclitus, fragment 1 |

## License

MIT. The Greek texts are from the Perseus Digital Library (Tufts) and the Open Greek
and Latin project (CC-BY), both public/open; this repository does not distribute the
large corpus — the scripts build it from the public sources.

---

*The Plato & Aristotle Consultant is a research aid. It retrieves and cites the texts;
the interpretation and judgment remain with the reader.*
