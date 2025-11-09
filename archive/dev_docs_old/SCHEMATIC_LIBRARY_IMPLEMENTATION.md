# Schematic Library Implementation

## Summary
- Added `schematic_library` MCP tool to list, inspect, stage, and load `.schem` files directly from the repository `schemas/` directory.
- Introduced `schematic_manager` helper for reading NBT metadata and copying files into the server’s WorldEdit schematics folder.
- Updated documentation (CLAUDE.md, README.md, context/README.md) describing new workflow and usage guidance.

## Key Components
- `mcp-server/src/vibecraft/server.py`
  - Registers the new tool and routes actions (`list`, `info`, `prepare`, `load`).
  - Integrates workflow state logging already used by structure, lighting, and symmetry validators.
- `mcp-server/src/vibecraft/schematic_manager.py`
  - Resolves source/destination paths, reads .schem metadata via `nbtlib`, copies files, and surfaces structured metadata objects.
- Dependencies updated to include `nbtlib` (`requirements.txt`, `pyproject.toml`).

## Usage Flow
1. `schematic_library(action="list")` – discover available schematics under `schemas/`.
2. `schematic_library(action="info", name="modern_villa_1")` – view size, block count, offset, and whether it already exists on the server.
3. `schematic_library(action="prepare", name="modern_villa_1")` – copy the file into `plugins/WorldEdit/schematics/` without loading.
4. `schematic_library(action="load", name="modern_villa_1")` – ensure the file is copied and run `//schem load schem modern_villa_1`.
5. Paste in-world using `worldedit_clipboard(command="paste -a -o")` (or other desired flags).

## Notes & Safeguards
- Destination names are validated to avoid spaces (WorldEdit cannot load filenames containing spaces).
- Metadata parsing is best-effort: if NBT fields are missing, the tool still lists the schematic but marks unknown values.
- The helper auto-creates the target schematics directory to avoid runtime failures on fresh setups.

## Next Opportunities
- Surface schematic thumbnails or block counts grouped by material once richer analytics are needed.
- Add optional bounding-box previews (rendered textually) or automated staging commands for setting paste positions.
- Extend support to `.schematic` legacy format if required.
