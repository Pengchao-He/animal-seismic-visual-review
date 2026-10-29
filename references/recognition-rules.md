# Recognition rules v1.0.0

Derived solely from Pengchao's reviewed workbench revision 173. These are empirical rules to test. The camera evidence is reported by the user, not independently rechecked. User prose and structured evidence fields occasionally differ; preserve both, do not upgrade certainty.

## Vehicle — V1–V3

- **V1:** A coherent approach–pass–recede event: waveform amplitude builds then decays; the spectrogram's energetic bandwidth widens near the middle then narrows, creating a roughly triangular plume, often with curved boundaries. The teaching examples have minute-scale events. Duration is a tendency, not a hard threshold.
- **V2:** Narrowband tracks that bend, slope, drift, or vary in frequency, sometimes forming harmonic families, support a mechanical/vehicle interpretation. They can be discontinuous and weak. Examples show these both above 75 Hz and at lower frequencies; no fixed frequency threshold is universal.
- **V3:** Multiple peaks, asymmetry, and long tails do not exclude a vehicle. A double peak alone cannot distinguish two vehicles from one vehicle interacting with road features. Plume plus approach/recede envelope is useful even when tracks are weak, but compare the sheep case before raising confidence.

Reference images: `ppt-s10-i1`, `ppt-s10-i2`, `ppt-s11-i1`, `ppt-s12-i1` event 1, `ppt-s13-i1`, `ppt-s17-i1`, `ppt-s23-i1`. Their originals are linked in `teaching-cases.md` and mapped to filenames in `teaching_records.json`.

## Gerbil — G1–G3

- **G1:** Irregular intermittent sharp waveform impulses and broadband vertical spectrogram stripes, sometimes spanning the displayed 0–200 Hz range. There can be activity–pause–activity sequences.
- **G2:** Recurrent enhanced frequency bands, patches or bright nodes at similar frequencies across several impulses, sometimes forming horizontal texture connecting them, support gerbil over hare. Check that the texture is local to the activity, rather than a persistent background line or vehicle track. Frequency bands vary across examples (roughly 50–100 Hz in one, 125–200 Hz in another); do not hard-code them.
- **G3:** Horizontal connections need not be obvious: `ppt-s14-i2` event 1 is a user camera-confirmed gerbil example with weak connections. Recurring frequency patches can be supporting evidence, but low visibility alone cannot resolve species.

Reference images: `ppt-s12-i1` event 2; `ppt-s14-i1` event 1; `ppt-s14-i2` event 1; `ppt-s15-i1` event 2 and the alternate views `ppt-s15-i2/i3/i4`.

## Tarim hare — H1–H2

- **H1:** Separated broadband impulse stripes with sharp waveform pulses. Compared with gerbil examples, enhanced bands are scattered, inconsistent, or absent and the stripes remain relatively isolated without persistent horizontal links.
- **H2:** This is a comparative interpretation, not proof from absence. Weak, clipped, or saturated spectrograms can hide gerbil bands. Isolated impulses also have non-animal causes. Use `animal_unspecified` or a low-confidence best guess when visibility or the activity pattern is inadequate.

Reference images: `ppt-s14-i1` event 2; `ppt-s15-i1` event 1 and its alternate views. The four slide-15 images include the same event pair in different views; they are not four independent confirmations.

## Sheep flock — S1–S3

- **S1:** A long, broad rise-and-fall envelope with many dense, irregular vertical impact stripes embedded in it, rather than one smooth compact pass. The two teaching windows have activity over a large part of about 20 minutes.
- **S2:** Dense impacts and lack of a clear family of changing mechanical frequency tracks support sheep over vehicle. Duration and triangular outline alone are insufficient. Short snippets may not show the full envelope; nearby repeated vehicle passes can mimic a prolonged event.
- **S3:** A longer signal is not automatically sheep; if impacts are unresolved or mechanical tracks are ambiguous, report the competing vehicle interpretation. Do not impose an exact 20-minute requirement.

Reference images: `ppt-s16-i1`, `ppt-s16-i2`. Only two reviewed sheep images exist in this snapshot; avoid claiming broad validation.

## Earthquake-like and other events — E1, U1

- **E1:** The single earthquake teaching example has sudden low-frequency onset, mainly below about 25 Hz, then a continuous decay/coda with narrowing bandwidth. It contrasts with gradually approaching vehicles and separated broadband animal impulses. Report `earthquake_like` as a visual hypothesis; do not certify an earthquake or identify P/S phases from this one pattern.
- **U1:** Persistent narrowband backgrounds, wind-like/noisy fluctuations, saturation, very weak events, or patterns not represented in the reviewed teaching set belong in `other_or_uncertain` or `no_clear_event`, unless a supported source can be separated. Do not inherit unreviewed PPT guesses such as pumps or rivers as validated classes.

Reference for E1: `ppt-s14-i2` event 2. No reviewed training evidence here establishes all environmental or mechanical background classes.

## Display and evidence limits — C1–C3

- **C1:** Teaching images use different per-image color scales; the supplied blind collection is described by the user as fixed-scale. Read visible axes and colorbars, compare within-image event-to-background structure, and do not convert a red area into a physical amplitude claim. Raw waveform units are not assumed calibrated.
- **C2:** Saturation or low contrast may erase texture. Absence of a visible horizontal connection or engine track is weaker evidence under these conditions. Magnification can resolve pixels but cannot recover clipped information.
- **C3:** Rules interpret morphology, not location, station identity, time-of-day, original class text, or camera labels. A source inference and an explanation of its physical mechanism are distinct claims. Preserve this distinction in evidence records.
