---
name: plato-aristotle-consultant
description: "Answer questions about Plato, Aristotle, and the Presocratics from the original Greek."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [plato, aristotle, presocratics, greek, philosophy, vector-search]
    category: research
---

# Plato & Aristotle Consultant

Answer questions about **Plato, Aristotle, and the Presocratics** — from the **original Greek** with exact scholarly citations (Stephanus pages for Plato, Bekker references for Aristotle, Diels-Kranz for Heraclitus) — not from a translation or the model's recollection.

## When to Use

- User asks about a Platonic dialogue, an Aristotelian doctrine, or a Presocratic fragment
- User wants a passage located, a Greek term examined, or a citation verified
- User is studying ancient Greek philosophy, the history of philosophy, or classical philology

## The Corpus (already built)

- **Text corpus:** `C:\Users\philo\plato-aristotle-consultant\scripts\text\` — 3 TSV files, 13,706 entries, each `CITATION\tTEXT`
- **Vector index:** `C:\Users\philo\plato-aristotle-consultant\scripts\chroma\` — ChromaDB collection `greek_philosophy_corpus`, bge-m3 (1024-dim, multilingual)
- **Raw sources:** `scripts/raw/` — the clean Greek TEI XML from PerseusDL + First1KGreek

The corpus covers:

| Author | Works | Segments |
|--------|-------|----------|
| **Plato** | All 36 canonical works (Euthyphro, Apology, Crito, Republic, Symposium, etc.) | 9,771 |
| **Aristotle** | 40 works (Categories, Analytics, Metaphysics, Ethics, De anima, etc.) | 3,816 |
| **Heraclitus** | 119 Diels-Kranz fragments | 119 |

Each entry carries the author + work + section in its citation, e.g.
`Plato | Ἀπολογία Σωκράτους | 17` (Stephanus) or `Aristotle | Analytica priora | priora`.

### Not yet included (deferred)

The full **Diels-Kranz Presocratic corpus** (Anaximander, Parmenides, Empedocles,
Democritus, etc.) is **not** included because no clean machine-readable Greek source is
publicly available; the only complete collection is the subscription-gated **Thesaurus
Linguae Graecae (TLG)**. If a clean edition is sourced (including via a TLG copy), the
fragmentary Presocratics can be added following the same pattern. Heraclitus is included
via the public-domain Diels-Kranz text.

## Query Workflow

### 1. Semantic retrieval

```bash
cd /c/Users/philo/plato-aristotle-consultant/scripts
python pa_index.py --query "<question, in Greek or English>" --k 5
```

bge-m3 is multilingual, so English queries match Greek text. Returns the top-k entries
with exact citations. For a broader sweep, use `--k 10`.

### 2. Read the actual text

The query returns the passage text. Read it carefully. If you need the full text, grep
the TSV:

```bash
grep -F "Plato | Ἀπολογία Σ οκράτους | 17" /c/Users/philo/plato-aristotle-consultant/scripts/text/plato.tsv
```

### 3. Answer from the source

- Quote the **original Greek** passage.
- Give the **exact citation** (e.g. `Plato | Φαῖδρος | 244a`, `Aristotle | Categoriae`).
- Explain the passage in the user's language, but anchor every claim in the quoted text.
- Note the original Greek term where relevant (e.g. *εἶδος* "form", *οὐσία* "substance",
  *ψυχή* "soul").

### Epistemic standards (READ BEFORE ANSWERING)

Classical-philosophy material — especially secondhand commentaries, doxographies,
and modern summaries — is full of distortions, retrojected readings, and
fabricated or misattributed fragments. The user explicitly wants accuracy and
awareness of limits over confidence. Apply these rules to every answer:

1. **Separate exactly three registers, and label each:**
   - **Text** — something I retrieved verbatim from a corpus file (Plato,
     Aristotle, Heraclitus) with a citation.
   - **Sourced tradition** — a claim an ancient source or the later tradition says
     an author held (e.g. a doxographer attributing a doctrine to a Presocratic;
     Aristotle reporting Plato's unwritten doctrines). Still cite the source that
     reports it.
   - **Hypothesis / general knowledge** — my inference or what I know from outside
     the corpus. ALWAYS label it as such ("my hypothesis is…", "this is general
     knowledge, not from the corpus"). Never deliver it in the voice of the text.

2. **Never counter a claim with an equally-unsourced counter-claim.** If I doubt a
   report, I may say "I cannot find it in the sources I have" (a statement of
   absence, backed by the search I actually ran) — but I must NOT substitute my
   own made-up reading as if it were the tradition. A hypothesis is welcome and
   can generate leads, but it must be flagged as a hypothesis, not asserted as
   fact.

3. **Absence ≠ non-existence.** "Not in my corpus" means exactly that. State which
   sources I checked. Do not upgrade a searching-failure into "this is fake
   everywhere." If the report is attributed to a source or fragment I don't hold,
   say so explicitly and offer to go get that source (e.g. a fragment from the
   subscription-gated TLG, or another dialogue).

4. **Do not paraphrase a polemical or revisionist secondhand summary as the story
   itself.** If the user brings me a claim (from a video, a blog, or a secondhand
   summary), separate (a) what I can verify in primary texts from (b) what I can
   only see in the retelling. Do not inherit the retelling's specifics unless I
   find them in a primary text.

5. **A counter-reading is only legitimate if I have a text for it.** To say "the
   tradition reads X as Y," I need a source that says so. If I only *think* that's
   how it's read, label it a hypothesis.

6. **When genuinely uncertain, say "I don't know," then state the smallest true
   claim I can defend** and what would settle it. Confidence must scale with
   competence — never fill an evidential gap with assertive prose.

## Citation format

| Form | Meaning |
|------|---------|
| `Plato \| Ἀπολογία Σωκράτους \| 17` | Plato, Apology, Stephanus page 17 |
| `Plato \| ἘᾶΦύθρων \| 2a` | Plato, Euthyphro, Stephanus 2a |
| `Aristotle \| Analytica priora` | Aristotle, Prior Analytics |
| `Heraclitus \| Diels-Kranz 22B1` | Heraclitus, fragment 1 |

## Pitfalls

- **Don't answer from memory or from a translation.** Always retrieve and quote the original Greek.
- **The index build is resumable.** If `pa_index.py` dies partway, re-run it.
- **Ollama must be running** for embeddings (`ollama serve`). Model: `bge-m3` (multilingual — required for Greek).
- **Long entries** are truncated to 5000 chars before embedding (bge-m3 context).
- **The Presocratics are incomplete** — only Heraclitus is in the corpus. Do not answer about Parmenides/Empedocles/Democritus as if from the source; say they are not yet covered.

## Verification

1. Run a query and confirm it returns entries with valid citations.
2. Grep the TSV to confirm the full text matches the citation.
3. Answer a test question and confirm every claim is anchored in a quoted Greek passage.
