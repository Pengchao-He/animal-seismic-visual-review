# Animal seismic visual review

A Codex skill for interpreting desert nodal-geophone waveform and spectrogram images using an expert's reviewed visual distinctions. It records candidate source classes, evidence, uncertainty, and estimated event windows, then draws numbered windows directly over the spectrogram.

**中文：** 将人工复核的波形与时频谱经验整理为视觉判断流程，输出类别、依据、置信度和估计时间窗，并在时频谱上显示对应矩形框。原图不变，标框可以隐藏。

Version **1.1.0** adds time-window annotations. The recognition rules retain their v1.0 provenance. This is an empirical interpretation workflow, not a trained neural-network classifier. No accuracy has been established by this public package.

## What it recognizes

| Code | Candidate source |
|---|---|
| `vehicle` | Vehicle / 汽车 |
| `sheep_flock` | Sheep flock / 羊群 |
| `tarim_hare` | Tarim hare / 塔里木兔 |
| `gerbil` | Gerbil / 沙鼠 |
| `earthquake_like` | Earthquake-like morphology, without seismic confirmation |
| `animal_unspecified`, `other_or_uncertain`, `no_clear_event` | Insufficient or different evidence |
| `mixed` | Distinct source types in separate or overlapping event intervals |

The written rules were derived from 15 reviewed teaching images with 26 annotated regions. Those counts are not independent event counts. Original images, detailed expert case records, workbench snapshots, raw data, blind-test images, predictions, and answers are **not included** in this public distribution. The full local case pack contains stronger evidence than this rules-only public distribution.

## Use the skill

Use the repository as a skill folder named `animal-seismic-visual-review`, or copy `SKILL.md`, `references/`, and `scripts/` into that folder under your Codex skills directory. Preserve any existing local teaching case pack when updating. The entry point is [SKILL.md](SKILL.md).

Example request:

> Use $animal-seismic-visual-review to classify these waveform/spectrogram images. Use my reviewed teaching cases, keep the answers closed, and return per-event evidence, uncertainty, numeric time intervals, and numbered time-window boxes over each spectrogram.

Without a reviewed case pack, the skill must disclose that it is relying on written rules alone. Do not treat a prediction as a verified animal observation.

## Run the annotation example

The renderer uses only the Python standard library, Python **3.9 or later**. It does not call a model or classify images; it renders supplied windows.

```bash
python3 scripts/render_windows.py examples/annotations.json examples/report.html
python3 -m unittest discover -s tests -v
```

Open `examples/report.html` in a browser. The supplied graphic is synthetic, solely for demonstrating annotation geometry; it is not a geophone observation, teaching example, or classification benchmark. Keep the relative image paths intact when moving the generated HTML.

![Synthetic annotation layout](examples/synthetic.svg)

## Output contract

- Preserve the source image and record its dimensions, time-axis limits, and spectrogram bounds.
- Return a summary row per image and evidence, alternatives, and confidence per event.
- Record `start_seconds` and `end_seconds` and display matching `mm:ss` windows relative to the plot's time origin.
- Draw numbered boxes and a matching class/time/confidence legend. A full-height box identifies time only, not occupied bandwidth.
- Mark image-derived boundaries as estimates. A value such as `07:18` is a notation conversion, not proof of second-level accuracy. A window ending at the image edge may be truncated.
- Preserve frozen classifications and checksums when adding annotations or comparing answers later.

See the [output schema](references/output-schema.md) and [recognition rules](references/recognition-rules.md). Plot calibration must be checked for each layout; there are no universal pixel coordinates or frequency thresholds.

## Validation and limits

The included tests cover time-to-pixel mapping, nonzero time origins, rejected invalid windows, safe text rendering, and end-to-end HTML output. The example was run with Python 3.14 on macOS. These checks validate the renderer, not species classification accuracy. Color saturation, unequal colorbars, persistent background lines, and incomplete event windows can all affect visual interpretation.

## Maintainer and publication scope

Maintained by [Pengchao He](https://github.com/Pengchao-He). The empirical distinctions originate from the maintainer's reviewed annotations; implementation and packaging were assisted by Codex.

This repository is public for inspection. No open-source license grant has been selected for this release; public visibility alone does not grant a reuse license. The synthetic example is original demonstration material. No CWP compliance claim is made.
