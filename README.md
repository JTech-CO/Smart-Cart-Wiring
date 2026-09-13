# Smart Cart Module Wiring Studio B1

[한국어](README-KR.md) | [English](README.md)

A module-level wiring viewer for the user-following smart cart. This is NOT a PCB layout or a cart-control application. The project contains original textured vector illustrations, an accurate reference breadboard contact map, terminal data, and editable electrical schematic exports.

## Use
Open `index.html`. All assets are local, with no build step, CDN, login, backend, or device-control API. Alternatively, run `python -m http.server 8000` in this folder. For GitHub Pages, copy the entire folder contents to a chosen deployment directory. To preserve the existing Smart-Cart viewer, add this package under a separate `wiring/` directory instead of overwriting its root files.

## Files
- `assets/drawings/`: four editable SVG drawing sheets.
- `downloads/Smart-Cart-Wiring-B1.pdf`: A3 landscape drawing and assembly-reference set.
- `eda/easyeda/SmartCart-B1-Modules.json`: self-contained EasyEDA Standard schematic; import into Pro using Import EasyEDA(Standard).
- `eda/kicad/`: KiCad 5.1-compatible legacy schematic/library source, not a modern PCB project.
- `data/`: module BOM, terminal netlist and breadboard contacts.
- `tools/`: reproducible model/export/render generators.
- `tests/`: static and browser checks and reports.

## Scope
The reference uses 44 wired module symbols, 194 schematic terminals and 63 net names. A 400-tie breadboard uses 300 strip contacts and 100 rail contacts. Rails are numbered separately from the numbered strip columns, from left to right, 1 to 25.

The first three drawings use named functional terminals and cable bundles; their pictorial geometry is not a mechanical drawing or exact purchased-board pin placement. Follow physical terminal names and the contact tables, not illustrative silkscreen positions. Components with unknown specifications and fuse ratings marked * are conditional. This is a bench prototype reference, not a release-approved vehicle harness.

EasyEDA Standard JSON uses real symbols, pins, wires and net labels, not an imported picture. Native EasyEDA Pro conversion and native KiCad ERC have NOT been executed. Check the import against the supplied 194-terminal CSV before any hardware work. No Gerber, PCB, pick-and-place or footprint package is supplied.

See `docs/ASSEMBLY-KR.md`, `docs/EASYEDA-IMPORT-KR.md`, `docs/SOURCES.md` and `tests/design-report.json`.
