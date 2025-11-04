"""Helper utilities for managing WorldEdit schematics."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import nbtlib

SCHEM_SOURCE_DIR = Path(__file__).parent.parent.parent.parent / "schemas"
SCHEM_DEST_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "minecraft-server"
    / "plugins"
    / "WorldEdit"
    / "schematics"
)


@dataclass
class SchematicMetadata:
    name: str
    path: Path
    width: Optional[int] = None
    height: Optional[int] = None
    length: Optional[int] = None
    block_count: Optional[int] = None
    offset: Optional[List[int]] = None
    exists_on_server: bool = False


def list_schematics() -> List[SchematicMetadata]:
    SCHEM_DEST_DIR.mkdir(parents=True, exist_ok=True)
    schematics: List[SchematicMetadata] = []

    if not SCHEM_SOURCE_DIR.exists():
        return schematics

    for file in sorted(SCHEM_SOURCE_DIR.glob("*.schem")):
        meta = read_metadata(file)
        if meta:
            meta.exists_on_server = (SCHEM_DEST_DIR / file.name).exists()
            schematics.append(meta)

    return schematics


def read_metadata(path: Path) -> Optional[SchematicMetadata]:
    try:
        nbt_file = nbtlib.load(path)
    except FileNotFoundError:
        return None
    except Exception as exc:
        return SchematicMetadata(name=path.stem, path=path)

    # nbtlib 2.0+ API: File object acts as the root compound directly
    # Access the root compound tag (usually empty string key for schematics)
    try:
        # Try to get root compound - schematics typically have root at top level
        if hasattr(nbt_file, 'root'):
            # Older API compatibility
            root = nbt_file.root
        elif isinstance(nbt_file, dict):
            # nbtlib 2.0+: File acts like a dict
            # For .schem files, data is typically at root level or under empty string key
            root = nbt_file.get('', nbt_file)
        else:
            # Direct access if it's the compound itself
            root = nbt_file
    except Exception:
        return SchematicMetadata(name=path.stem, path=path)

    width = _safe_get(root, "Width")
    height = _safe_get(root, "Height")
    length = _safe_get(root, "Length")

    block_data = root.get("BlockData")
    block_count = len(block_data) if block_data is not None else None
    offset = root.get("Offset")
    if offset is not None:
        offset = list(offset)

    return SchematicMetadata(
        name=path.stem,
        path=path,
        width=width,
        height=height,
        length=length,
        block_count=block_count,
        offset=offset,
    )


def copy_to_server(source_name: str, target_name: Optional[str] = None) -> Path:
    if not source_name.endswith(".schem"):
        source_name = f"{source_name}.schem"

    source_path = SCHEM_SOURCE_DIR / source_name
    if not source_path.exists():
        raise FileNotFoundError(f"Schematic '{source_name}' not found in {SCHEM_SOURCE_DIR}")

    SCHEM_DEST_DIR.mkdir(parents=True, exist_ok=True)

    target_filename = target_name or source_path.stem
    if not target_filename.endswith(".schem"):
        target_filename = f"{target_filename}.schem"

    destination = SCHEM_DEST_DIR / target_filename
    shutil.copy2(source_path, destination)
    return destination


def _safe_get(root: Dict[str, object], key: str) -> Optional[int]:
    value = root.get(key)
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
