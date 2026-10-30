---
name: animal-seismic-visual-review
description: Classify desert nodal-geophone waveform and spectrogram images using Pengchao's reviewed visual cases. Use for vehicle, sheep-flock, Tarim-hare, gerbil, and earthquake-like signal prediction, evidence recording, or blind evaluation. Applies to plotted seismic signals, not animal photographs; permits mixed and uncertain results.
metadata:
  version: 1.2.0
---

# Animal seismic visual review

Apply the user's empirical waveform/spectrogram distinctions, version 1.2.0. This is a visual interpretation procedure, not a fitted classifier or a calibrated species-identification model. Version 1.2 makes each event the classification unit; the recognition rules retain their v1.0 provenance.

## Before prediction

1. Read [the rules](references/recognition-rules.md) and [reviewed teaching cases](references/teaching-cases.md). This distribution includes 15 original teaching images, verbatim expert descriptions, and 26 reviewed regions in [teaching_records.json](references/teaching_records.json). Open the relevant reference images and descriptions before prediction; inspect their annotations and [provenance](references/provenance.json). Prefer the reviewed region labels over original image text. If an installation lacks these files, disclose that predictions use written rules only; do not claim to have compared unavailable cases.
2. Treat the reviewed category within its drawn region as the user's teaching label. Image text, original labels, and PPT headings may conflict with it. Blank time fields are valid: use the drawn region. Do not invent exact timestamps from boxes. A shared description can discuss several regions; apply the correct subsection to each region's reviewed category.
3. For a blind run, open only the designated prediction images. Do not search source catalogs, original labels, prior reviews, camera logs, answer files, or hidden mappings to infer their identities. Inspect folder names without opening answer-bearing contents. Use provided image IDs and visible axes. If an image visibly leaks a true label, flag it and withhold that case from a strict blind score.
4. Freeze the skill and teaching snapshot before seeing test results. Record hashes of the skill files and input images. Any change after viewing answers belongs to a later version. Exact or suspected teaching/test overlaps must be reported separately; identical-image hash comparison does not rule out replotting of the same event.

## Read each image

- Read time/frequency axes and colorbar. Evaluate duration in axis units, never by equal pixel width across plots. Do not infer signal strength from color alone across unequal scales.
- Inspect the whole waveform and spectrogram, identify candidate event groups, then inspect localized details where needed. Retain original plots and use magnification/crops only as inspection aids; do not rescale colors, denoise, or synthesize features for the primary blind run.
- Apply the joint feature rules. Consider event-local horizontal textures separately from narrowband background that persists before and after the event. Distinguish bent/drifting mechanical tracks from near-stationary frequency patches in irregular impulses.
- Decide independently for multiple sources. Do not force an entire plot to one source if there is clear evidence of distinct event types. The 20-minute image is a container, not one event. Segment candidate activity intervals first, then assign each interval its own label, evidence, alternatives, and confidence. Allow overlapping intervals for simultaneous sources. Split separated episodes even when they share a class; do not split every impulse into an animal or count individuals. Unresolved mixtures within one interval remain uncertain.
- Do not identify vehicle size, exact animal count, gait, earthquake phases, or physical mechanisms solely from these pictures. User descriptions suggesting these are explanatory hypotheses, not required output facts.

## Prediction record

For every image, save `sample_id`, `image_path`, and an `events` array. Each event must have its own stable `event_id`, numeric `start_seconds` and `end_seconds`, `label`, `confidence` (high/medium/low, subjective), `supporting_visual_evidence`, `conflicting_or_missing_evidence`, `alternative_labels`, `rule_ids`, `teaching_case_ids`, `review_required`, and `review_status`. Reassess the whole image for missed events, not only previously drawn boxes. Do not copy image-level confidence or evidence into each interval as an independent assessment.

Legacy imports must retain their original judgment in separate `legacy_*` fields. Until an interval is independently reviewed, set its current `label` and `confidence` to null and `review_status` to `legacy_pending`. Format conversion is not new recognition. An actually reviewed but unresolved event uses `other_or_uncertain` (or `animal_unspecified` when appropriate) with explicit alternatives. Silence is not an unknown event; uncertain coverage should be documented without boxing the entire background.
Use stable label codes: `vehicle`, `sheep_flock`, `tarim_hare`, `gerbil`, `earthquake_like`, `animal_unspecified`, `other_or_uncertain`, `no_clear_event`. Derive `labels_present` from reviewed event labels. An optional image summary may say “multiple event types”; it must never replace the individual labels or be copied back to events. Map them to Chinese for the user. A tentative best guess may be recorded with low confidence; never equate self-reported confidence with an accuracy percentage. A secondary candidate is not an asserted co-occurring source.

Save one CSV/JSONL row per event as the primary deliverable, plus an optional image summary. The report heading identifies the image and number of candidate intervals; each box maps to an event row. Category/confidence/review filters must match fields from the same event, not an image-level label or different events. Do not claim precise start/end times from compressed plots. Record source regions as normalized coordinates only if actually measured. Mark all visual timing estimates approximate.

Every prediction delivery must also include numbered time-window boxes drawn over the spectrogram and a matching legend with class, relative `mm:ss` interval, and confidence. Retain the untouched image and support hiding the overlay. Read [output-schema.md](references/output-schema.md) for the numeric start/end fields, pixel calibration, boundary flags, and rendering requirements. Use [render_windows.py](scripts/render_windows.py) or an equivalent verified overlay implementation. Full-height boxes mark time intervals, not the source's frequency extent. Keep uncertain windows visibly tentative and assess separate intervals independently.

## Evaluation

Save and hash predictions before requesting or reading answers. Score only after explicit access to the answer key for evaluation. For event-level scoring, agree temporal matching/tolerance and class handling before opening answers; report missed and extra events as well as classification errors. Keep unreviewed legacy rows out of newly reviewed counts. Align image-level versus event-level labels, mixed events, unknowns, and any class aliases before computing accuracy, per-class precision/recall, confusion matrices, and abstention coverage. Report class support and possible source overlap. Corrections after scoring must not overwrite the original predictions. Never report accuracy without a ground-truth comparison.
