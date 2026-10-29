# Prediction and annotation output · v1.1

For each sample, retain the original image and provide an annotated HTML view with
time-window rectangles on the spectrogram, a machine-readable annotation manifest,
and a summary table. Keep evidence and uncertainty per event, not only per image.

Time windows use numeric `start_seconds` and `end_seconds` relative to the displayed
time axis, with matching `mm:ss` labels. For image-only inference, set
`timing_basis: visual_estimate`; formatting seconds does not establish second-level
accuracy. Mark contact with either image boundary and do not equate a right-edge
cutoff to the true end of an event. Do not invent a numerical timing uncertainty.

Separate source events with different labels. A stronger classification in one
window does not validate another window. Preserve peak/strongest-subinterval notes
as notes; they are not additional source events. For legacy prose, convert only
unambiguous interval ranges and review the conversion. Do not box an isolated peak
time as a zero-width event or silently convert “weaker to…” to a complete interval.

## Manifest

```json
{
  "schema_version": "1.1",
  "samples": [{
    "sample_id": "DEMO001",
    "image_path": "synthetic.svg",
    "image_width": 1000,
    "image_height": 500,
    "spectrogram_bounds_px": [80, 200, 920, 440],
    "time_axis_seconds": [0, 1200],
    "windows": [{
      "start_seconds": 210,
      "end_seconds": 438,
      "label": "vehicle",
      "confidence": "medium",
      "timing_basis": "visual_estimate"
    }]
  }]
}
```

Image dimensions and plot bounds refer to the original image pixel coordinates.
Bounds are `[left, top, right, bottom]` of the spectrogram axes, excluding labels,
colorbar, and waveform panel. Calibrate each layout; never reuse pixel bounds for
another layout without checking them. `time_axis_seconds` need not start at zero.

Map time to x using `x = left + (t - t_min)/(t_max - t_min)*(right - left)`.
Full-height boxes select a time window only. They do not assert that the source
occupies all plotted frequencies. Use measured frequency bounds only when actually
supported, with a separate documented mapping; the bundled renderer does not infer
frequency bounds. Show numbered boxes and a matching class/time/confidence legend
without hiding axes or changing source colors. Support hiding the overlay and
opening the untouched source image.

Use `scripts/render_windows.py annotations.json report.html` for a portable HTML
view. It needs Python 3.9+ and only the standard library. Images remain linked by
relative path; keep the HTML and image directory structure together when sharing.

## Reproducibility

Keep the full prediction fields specified in SKILL.md. Record skill version, source
image hashes, annotation geometry, and timing basis. Freeze predictions before any
answer-key access. A later display/annotation update must retain the original
prediction file and checksum and document which version supplied each artifact.
Do not silently replace classification results when adding windows.
