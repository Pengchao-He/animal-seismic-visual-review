# Teaching data provenance and publication scope

The maintainer explicitly authorized publication of the reviewed teaching cases on
2026-10-29. This package exports the 15 reviewed images and 26 regions used to build
the original rules, from teaching-workbench revision 173. The source presentation
is `Wild animal spectrugram labels 10272026.pptx`; slide/image positions are retained
in each case's `source` field. The original PPTX and workbench database are not
distributed.

- [teaching-cases.md](teaching-cases.md): original expert descriptions with image links.
- [teaching_records.json](teaching_records.json): structured reviewed labels,
  confidence, evidence fields, descriptions, and normalized image regions.
- [provenance.json](provenance.json): snapshot version, selected IDs, category counts,
  source/export hashes, and transformation record.
- `images/`: original PNG bytes; each record includes the SHA-256 digest.

Absolute local `source_path` fields were removed from exported metadata. Image
bytes and expert descriptions were not changed. The published case document
retains original on-image/PPT labels as unverified context. Reviewed region labels
take precedence; these are teaching judgments, not newly verified ground truth.
Regions use `x`, `y`, `w`, `h` normalized to the whole original image. They can span
both waveform and spectrogram and are not equivalent to calibrated time windows.

Slide 15 includes alternate views of the same event pair. Counts are not
independent observations. Camera confirmation is reported by the maintainer and
has not been independently checked. Statements about mechanism, animal numbers,
or vehicle size in original notes remain explanatory hypotheses.

Blind-test images, predictions, answers, raw waveforms, and camera files are not
part of this publication. Tests verify hashes and metadata consistency, not source
identity or classification accuracy.

## Reuse terms pending

The maintainer authorized public posting. A separate reuse license and rights-holder
confirmation have been requested and are pending. Public availability does not
itself establish permission to redistribute or adapt the images/notes. No blanket
third-party ownership or license-compatibility claim is made. The synthetic SVG in
`examples/` was created for this repository; it is demonstration material, not an
observational teaching image.
