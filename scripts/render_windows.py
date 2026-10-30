"""Draw time-window overlays in HTML while leaving source images untouched.

Standard library only. Run: python3 render_windows.py annotations.json output.html
The manifest format is documented in references/output-schema.md.
"""
import argparse
import html
import json
import math
import os
from pathlib import Path
from urllib.parse import quote

# Map source-class strings to display colors; unknown keys use a neutral fallback.
COLORS = {'vehicle': '#e97700', 'gerbil': '#8054e8', 'tarim_hare': '#008d96',
          'sheep_flock': '#d63c91', 'earthquake_like': '#2164d9'}

def mmss(seconds):
    """Format numeric seconds as rounded mm:ss text; return the display string."""
    seconds = round(seconds)
    return f'{seconds // 60:02d}:{seconds % 60:02d}'

def validate_sample(sample):
    """Check a sample mapping's geometry and windows; return None or raise ValueError."""
    width, height = sample['image_width'], sample['image_height']
    x0, y0, x1, y1 = sample['spectrogram_bounds_px']
    t0, t1 = sample['time_axis_seconds']
    values = [width, height, x0, y0, x1, y1, t0, t1]
    if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in values):
        raise ValueError('Geometry and time-axis values must be finite numbers')
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height and t0 < t1):
        raise ValueError('Invalid plot geometry or time axis')
    for window in sample['windows']:
        a, b = window['start_seconds'], window['end_seconds']
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            raise ValueError('Window boundaries must be numeric')
        if not (math.isfinite(a) and math.isfinite(b) and t0 <= a < b <= t1):
            raise ValueError('Window lies outside the visible time axis or is reversed')
        if window['confidence'] not in ('high', 'medium', 'low'):
            raise ValueError('Unknown confidence')
        if window.get('timing_basis') != 'visual_estimate':
            raise ValueError('This renderer requires explicitly marked visual estimates')

def window_geometry(sample, window):
    """Map a sample and event window to an (x, y, width, height) pixel tuple."""
    x0, y0, x1, y1 = sample['spectrogram_bounds_px']
    t0, t1 = sample['time_axis_seconds']
    left = x0 + (window['start_seconds'] - t0) / (t1 - t0) * (x1 - x0)
    right = x0 + (window['end_seconds'] - t0) / (t1 - t0) * (x1 - x0)
    return left, y0, right - left, y1 - y0

def overlay_markup(sample):
    """Validate one sample mapping; return escaped SVG overlay and HTML legend strings."""
    validate_sample(sample)
    e = html.escape
    groups, legend = [], []
    for index, window in enumerate(sample['windows'], 1):
        x, y, w, h = window_geometry(sample, window)
        color = COLORS.get(window['label'], '#52636d')
        label = window.get('display_label', window['label'])
        interval = f"{mmss(window['start_seconds'])}–{mmss(window['end_seconds'])}"
        boundary = ' · window edge' if window['start_seconds'] == sample['time_axis_seconds'][0] or window['end_seconds'] == sample['time_axis_seconds'][1] else ''
        description = f'W{index} · {label} · ≈ {interval} · {window["confidence"]}{boundary}'
        # The full-height rectangle denotes time only, not energy at every frequency.
        groups.append(f'<g><title>{e(description)}</title><rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{color}" fill-opacity="0.07" stroke="white" stroke-width="6"/><rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="none" stroke="{color}" stroke-width="3" stroke-dasharray="12 6"/><rect x="{x:.3f}" y="{y+9:.3f}" width="60" height="33" rx="5" fill="white"/><text x="{x+8:.3f}" y="{y+33:.3f}" font-size="24" font-family="sans-serif" font-weight="bold" fill="#172d35">W{index}</text></g>')
        legend.append(f'<span class="window-chip" style="border-color:{color}">{e(description)}</span>')
    svg = f'<svg class="time-window-overlay" viewBox="0 0 {sample["image_width"]} {sample["image_height"]}" role="img" aria-label="Estimated event time windows for {e(sample["sample_id"], quote=True)}">{"".join(groups)}</svg>'
    return svg, '<div class="window-legend">' + ''.join(legend) + '</div>'

STYLE = '''.annotated-plot{position:relative}.annotated-plot img{display:block;width:100%;height:auto}.time-window-overlay{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.window-legend{display:flex;flex-wrap:wrap;gap:8px;padding:12px 20px}.window-chip{border-left:5px solid;padding:4px 9px;background:#f0f4f4;font-size:13px}.hide-windows .time-window-overlay,.hide-windows .window-legend{display:none}'''

def render(manifest_path, output_path):
    """Read a JSON manifest path and write an HTML output path; return None, retain images."""
    manifest_path, output_path = Path(manifest_path).resolve(), Path(output_path).resolve()
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('schema_version') != '1.1':
        raise ValueError('Expected schema_version 1.1')
    cards = []
    ids = set()
    for sample in manifest['samples']:
        if sample['sample_id'] in ids:
            raise ValueError('Duplicate sample ID')
        ids.add(sample['sample_id'])
        image = (manifest_path.parent / sample['image_path']).resolve()
        if not image.is_file():
            raise FileNotFoundError(image)
        src = quote(os.path.relpath(image, output_path.parent).replace(os.sep, '/'), safe='/')
        svg, legend = overlay_markup(sample)
        cards.append(f'<article><h2>{html.escape(sample["sample_id"])}</h2><div class="annotated-plot"><img width="{sample["image_width"]}" height="{sample["image_height"]}" src="{src}" alt="{html.escape(sample["sample_id"],quote=True)} source plot">{svg}</div>{legend}</article>')
    output_path.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Estimated event windows</title><style>body{font:16px/1.5 system-ui;max-width:1400px;margin:32px auto;padding:0 20px;color:#20353b;background:#f3f5f5}article{background:white;padding:12px;margin:24px 0}'+STYLE+'</style><h1>Estimated event windows</h1><p>Time is relative to each displayed plot. Full-height boxes indicate time intervals only, not frequency extent. Boundaries are visual estimates, not exact detections.</p><label><input type="checkbox" checked onchange="document.body.classList.toggle(\'hide-windows\',!this.checked)"> Show windows</label>'+''.join(cards)+'</html>')

if __name__ == '__main__':
    # Accept manifest/output CLI paths, write the annotated HTML, and return no value.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest')
    parser.add_argument('output')
    args = parser.parse_args()
    render(args.manifest, args.output)
