#!/usr/bin/env python3
"""
Validate furniture layouts against the JSON schema.
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("❌ jsonschema library not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema", "--quiet"])
    import jsonschema
    from jsonschema import validate, ValidationError


def main():
    # Load schema
    schema_path = Path(__file__).parent.parent / 'context' / 'furniture_layout_schema.json'
    with open(schema_path, 'r') as f:
        schema = json.load(f)

    print(f"✅ Loaded schema from {schema_path}")

    # Load layouts
    layouts_path = Path(__file__).parent.parent / 'context' / 'minecraft_furniture_layouts.json'
    with open(layouts_path, 'r') as f:
        layouts = json.load(f)

    print(f"✅ Loaded {len(layouts)} furniture layouts from {layouts_path}\n")

    # Validate each layout
    errors = []
    warnings = []

    for i, layout in enumerate(layouts):
        layout_name = layout.get('name', f'Layout {i+1}')
        layout_id = layout.get('id', 'unknown')

        print(f"Validating: {layout_name} ({layout_id})...")

        try:
            # Validate against schema
            validate(instance=layout, schema=schema)

            # Additional checks beyond schema
            bounds = layout.get('bounds', {})
            placements = layout.get('placements', [])

            # Check if placements fit within bounds
            for j, placement in enumerate(placements):
                if placement.get('type') == 'block':
                    pos = placement.get('pos', {})
                    x, y, z = pos.get('x', 0), pos.get('y', 0), pos.get('z', 0)

                    # Check bounds
                    if x < 0 or x >= bounds.get('width', 0):
                        warnings.append(f"  ⚠️  {layout_name}: Placement {j+1} X={x} outside width bounds (0-{bounds.get('width', 0)-1})")
                    if y < 0 or y >= bounds.get('height', 0):
                        warnings.append(f"  ⚠️  {layout_name}: Placement {j+1} Y={y} outside height bounds (0-{bounds.get('height', 0)-1})")
                    if z < 0 or z >= bounds.get('depth', 0):
                        warnings.append(f"  ⚠️  {layout_name}: Placement {j+1} Z={z} outside depth bounds (0-{bounds.get('depth', 0)-1})")

                elif placement.get('type') == 'fill':
                    from_pos = placement.get('from', {})
                    to_pos = placement.get('to', {})

                    for pos, label in [(from_pos, 'from'), (to_pos, 'to')]:
                        x, y, z = pos.get('x', 0), pos.get('y', 0), pos.get('z', 0)

                        if x < 0 or x >= bounds.get('width', 0):
                            warnings.append(f"  ⚠️  {layout_name}: Fill {label} X={x} outside width bounds")
                        if y < 0 or y >= bounds.get('height', 0):
                            warnings.append(f"  ⚠️  {layout_name}: Fill {label} Y={y} outside height bounds")
                        if z < 0 or z >= bounds.get('depth', 0):
                            warnings.append(f"  ⚠️  {layout_name}: Fill {label} Z={z} outside depth bounds")

            # Check if materials count is reasonable
            materials = layout.get('materials', {})
            placement_count = len(placements)
            material_count = sum(materials.values())

            if material_count == 0:
                warnings.append(f"  ⚠️  {layout_name}: No materials specified")

            print(f"  ✅ Valid! ({len(placements)} placements, {material_count} total materials)")

        except ValidationError as e:
            errors.append(f"  ❌ {layout_name}: {e.message}")
            print(f"  ❌ FAILED: {e.message}")

    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print('='*60)
    print(f"Total layouts: {len(layouts)}")
    print(f"Valid: {len(layouts) - len(errors)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print(f"\n{'='*60}")
        print("ERRORS:")
        print('='*60)
        for error in errors:
            print(error)

    if warnings:
        print(f"\n{'='*60}")
        print("WARNINGS:")
        print('='*60)
        for warning in warnings:
            print(warning)

    if not errors and not warnings:
        print(f"\n🎉 All layouts are valid with no warnings!")
        return 0
    elif not errors:
        print(f"\n✅ All layouts are valid (with {len(warnings)} warnings)")
        return 0
    else:
        print(f"\n❌ Validation failed with {len(errors)} errors")
        return 1


if __name__ == '__main__':
    sys.exit(main())
