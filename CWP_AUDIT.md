# CWP preparation audit — 2026-10-29

Scope: **full preparation**, requested by the maintainer. This audit applies the
maintainer-supplied CWP working checklist; it does not assert institutional approval.
The repository is **not yet fully CWP-ready**. Author metadata, complete credits,
and reuse licensing remain unresolved.

| Requirement | Status | Evidence | Next action |
|---|---|---|---|
| Human-readable entry point | PASS | Root `README.md` | None |
| Opening description | PASS | README opening explains visual interpretation and annotation | None |
| Specific CWP report number/year | FAIL | README explicitly marks this pending | Author supplies report identity |
| Durable developer email | FAIL | README has GitHub contact but no confirmed public email | Author supplies email and confirms longevity through report year |
| Dependencies and versions | PASS | README Dependencies; `requirements.txt`: CPython >=3.9, tested 3.14.7, stdlib only; browser and agent requirements separated | Record a model/build for future prediction runs |
| Complete authors/contributors/method credits | UNVERIFIED | README credits Pengchao He, initial labels attributed to 宇潭, and Codex assistance; rules cite reviewed snapshot | Author confirms full report author/co-developer list and preferred contributor names |
| Minimum source documentation | PASS | All Python modules/functions/classes have purpose/input/output docstrings; CLI blocks and constant mapping documented; record/schema fields described in reference docs | Keep documentation current |
| Press-play execution | PASS | README venv/setup/render/test commands; isolated execution produced expected HTML | None |
| Small example | PASS | Included synthetic SVG and manifest; two rendered intervals verified | Reuse grant remains pending under License below |
| Versioned environment specification | PASS | `requirements.txt` states runtime version range and exact tested runtime; no third-party packages needed | None |
| Tested system | PASS | macOS 27.0, arm64, CPython 3.14.7; CPU only; README distinguishes untested support | None |
| Full applicable root license | FAIL | No license chosen; README and data provenance explicitly state pending terms | Rights holder authorizes code/skill and teaching-data licenses; then add full texts |

## Executed checks

The repository's documented workflow was run from the repository root, using an
isolated environment at an external temporary location to avoid distributing it:

```bash
python3 -m venv /tmp/animal-seismic-cwp-venv-20261029
/tmp/animal-seismic-cwp-venv-20261029/bin/python -m pip install --no-index -r requirements.txt
/tmp/animal-seismic-cwp-venv-20261029/bin/python scripts/render_windows.py examples/annotations.json examples/report.html
/tmp/animal-seismic-cwp-venv-20261029/bin/python -m unittest discover -s tests -v
```

Observed result: dependency setup needed no external packages; renderer completed;
**4 tests passed**. The generated HTML contained two SVG window groups, the expected
03:30–07:18 and 17:00–20:00 labels, and a relative link to the supplied synthetic SVG.
Tests additionally checked time mapping with a nonzero origin, rejected invalid
ranges, escaped labels, and preserved source bytes.

The teaching-pack integrity test verified 15 PNG hashes, 26 valid normalized
regions, per-category counts, all case IDs, the exported-record hash, and verbatim
descriptions in the illustrated case document. An AST check found docstrings for
every authored Python module, function, and class. Public prose/metadata were
checked for local absolute paths and common credential markers. These are bounded
checks, not proof that every possible secret or third-party right has been audited.

The existing prediction report's overlay alignment and toggle were visually checked
in Codex's in-app browser on macOS. Classification accuracy is **not** established
by any of these software or packaging checks. No blind answers were opened.

## Mandatory unresolved items

Report number/year; public developer email and longevity; complete credits; and
rights-holder license selection. Do not replace missing facts with invented values,
and do not describe this release as fully CWP-ready until the table is all PASS.

## Sponsor-integration concerns

- No third-party Python package, copied external library, GPL integration, Madagascar,
  or Spectrum component is bundled or required by the renderer. No conclusion is
  made about unspecified downstream integrations or a future inference provider.
- Reviewed teaching images and descriptions are now publicly posted at the
  maintainer's explicit request. Public-posting authorization is recorded separately
  from permission for downstream reuse; see `references/DATA_PROVENANCE.md`.
- Python rendering is reproducible; species prediction still depends on a visual
  agent and subjective empirical interpretation. No trained model is distributed.

## Optional recommendations

After resolving mandatory items: add CI on selected Python/platform versions,
record the exact inference model/build for new runs, add citation metadata once a
report exists, and independently evaluate event-level accuracy with overlap controls.
These recommendations do not add submission blockers beyond the table above.
