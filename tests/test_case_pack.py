"""Validate the published case pack from repository files; emit unittest results."""
import hashlib
import json
from pathlib import Path
import unittest

# Resolve the repository reference directory from this test file, independent of cwd.
REFERENCES = Path(__file__).resolve().parents[1] / 'references'


class CasePackTests(unittest.TestCase):
    """Read exported records and images; report integrity and region failures as assertions."""

    def test_images_records_and_regions_match_provenance(self):
        """Take no extra inputs; check hashes, counts, labels, and normalized boxes, return None."""
        raw = (REFERENCES / 'teaching_records.json').read_bytes()
        records = json.loads(raw)
        provenance = json.loads((REFERENCES / 'provenance.json').read_text())
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         provenance['public_export']['exported_records_sha256'])
        self.assertEqual([case['id'] for case in records], provenance['selected_case_ids'])
        self.assertEqual(len(records), 15)
        self.assertEqual(sum(len(case['events']) for case in records), 26)
        guide = (REFERENCES / 'teaching-cases.md').read_text()
        counts = {}
        for case in records:
            self.assertNotIn('source_path', case)
            data = (REFERENCES / 'images' / case['image']).read_bytes()
            self.assertTrue(data.startswith(b'\x89PNG\r\n\x1a\n'))
            self.assertEqual(hashlib.sha256(data).hexdigest(), case['sha256'])
            self.assertIn(f"images/{case['image']}", guide)
            for event in case['events']:
                region = event['region']
                self.assertTrue(0 <= region['x'] < region['x'] + region['w'] <= 1)
                self.assertTrue(0 <= region['y'] < region['y'] + region['h'] <= 1)
                self.assertIn(event['description'].strip(), guide)
                counts[event['category']] = counts.get(event['category'], 0) + 1
        self.assertEqual(counts, provenance['annotation_counts'])


if __name__ == '__main__':
    # Accept standard unittest CLI arguments; print results and exit with test status.
    unittest.main()
