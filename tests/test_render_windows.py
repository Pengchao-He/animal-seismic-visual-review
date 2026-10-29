import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('renderer', ROOT/'scripts/render_windows.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

class WindowTests(unittest.TestCase):
    def setUp(self):
        self.sample = {'sample_id':'EXAMPLE', 'image_width':1000,'image_height':500,
            'spectrogram_bounds_px':[80,200,920,440], 'time_axis_seconds':[0,1200],
            'windows':[{'start_seconds':300,'end_seconds':600,'label':'vehicle',
            'confidence':'medium','timing_basis':'visual_estimate'}]}

    def test_time_mapping_stays_inside_spectrogram(self):
        self.assertEqual(renderer.window_geometry(self.sample,self.sample['windows'][0]), (290,200,210,240))
        shifted=copy.deepcopy(self.sample)
        shifted['time_axis_seconds']=[100,1300]
        shifted['windows'][0].update(start_seconds=400,end_seconds=700)
        self.assertEqual(renderer.window_geometry(shifted,shifted['windows'][0]), (290,200,210,240))

    def test_rejects_invalid_geometry_and_ranges(self):
        for start,end in [(-1,50),(500,400),(0,1201),(float('nan'),500)]:
            bad=copy.deepcopy(self.sample)
            bad['windows'][0].update(start_seconds=start,end_seconds=end)
            with self.assertRaises(ValueError):renderer.overlay_markup(bad)
        self.sample['spectrogram_bounds_px']=[80,200,1001,440]
        with self.assertRaises(ValueError):renderer.overlay_markup(self.sample)

    def test_escapes_labels_and_preserves_source(self):
        self.sample['windows'][0]['display_label']='<script>bad()</script>'
        svg,legend=renderer.overlay_markup(self.sample)
        self.assertNotIn('<script>',svg+legend)
        self.assertIn('&lt;script&gt;',legend)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);source=p/'source.svg';source.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
            before=source.read_bytes();self.sample['image_path']='source.svg'
            (p/'annotations.json').write_text(json.dumps({'schema_version':'1.1','samples':[self.sample]}))
            renderer.render(p/'annotations.json',p/'report.html')
            self.assertEqual(source.read_bytes(),before)
            result=(p/'report.html').read_text()
            self.assertIn('05:00–10:00',result)
            self.assertIn('src="source.svg"',result)

if __name__=='__main__':unittest.main()
