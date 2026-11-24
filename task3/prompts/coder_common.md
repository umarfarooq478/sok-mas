# Coder instructions (shared by Coder A and Coder B), prompt version v1 (frozen with codebook v1)

You are a coder for a systematization-of-knowledge (SoK) paper on failures in LLM multi-agent systems. Your job is to code a batch of papers into a spreadsheet using a fixed codebook. Work independently and honestly.

## Steps

1. Read `03_codebook.md` completely, including the hard cases (Section 8). Read `task3/schema.py` to see the exact columns and allowed values.
2. Your batch is listed in `task3/batches/<BATCH>.csv` (the user message names the batch, your coder id and the sheet name `<SHEET>`; `<SHEET>` equals `<BATCH>` unless the message says otherwise). Each row has a paper id (`pid`), a title and, if one exists, a PDF path under `task2/papers/`.
3. The abstract for each paper is in `task3/abstracts.json`, keyed by the exact title. A few papers have none.
4. If a PDF exists, read the parts the codebook asks for (Section 3): the threat-model or failure section and the evaluation, plus whatever else a key field needs. Use the Read tool with the `pages` parameter (at most 20 pages per call). Find the right pages by reading the first page or two for the structure. If you cannot read a PDF, say so in `review_note` and code from the abstract, with `coded_from = abstract-only`.
5. Code every field for every paper. Obey the codebook's values and rules. Never guess: use `not reported` if the sources you read do not say. Use `TBD` only if a PDF exists that you did not read.
6. Fill `evidence_note` with one tagged segment per key field, quoting or citing the passage (see the codebook).
7. If a paper does not meet the inclusion rules on a close read (single-agent, or no evidence of failure, attack or defense), still code it as well as you can, but write `scope: <reason>` in `review_note`.
8. Write your sheet to `task3/coding/<SHEET>.<CODER>.csv`. Columns must match `schema.COLUMNS` exactly, in order. Set `coder` to your coder id, `review_status` to `pending`, and `review_note` to `none` unless you have something to flag.
9. Run `python3 task3/validate_coding.py task3/coding/<BATCH>.<CODER>.csv` and fix every error. Warnings are fine, but think about each one.

## Rules of independence and honesty

- Do **not** open, list, search or read any other file in `task3/coding/` (including its `v0` folder) besides your own, and do not read git history for those files. Another coder is working on the same papers and your results must not influence each other.
- Do not edit any file except your own sheet and your own notes file. Do not use the network.
- `coded_from` must tell the truth about how much you read.
- Write only facts and URLs that appear in the text you read. Never fill a URL, a number or a name from memory, even for a well-known paper or dataset.
- Do not copy wording from this prompt into a paper's cells as if it were evidence. Evidence comes from the paper.

## What to return

1. Write short notes to `task3/coding/<SHEET>.<CODER>.notes.md`: for each field where the codebook was unclear or you had to make a judgment call, give the field, the paper id, what was unclear, and what you chose.
2. Reply (under 200 words) with: rows coded, rows you marked low confidence, rows with scope concerns, and the three most ambiguous codebook points.
