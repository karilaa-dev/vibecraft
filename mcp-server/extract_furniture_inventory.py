#!/usr/bin/env python3
"""
Extract furniture inventory from minecraft_furniture_catalog.json

Filters out pure category headings and extracts actual furniture items
with build instructions. Creates a reference table for layout authoring.
"""

import json
import sys
from pathlib import Path


def has_build_instructions(entry):
    """
    Determine if an entry contains actual furniture build instructions.

    Pure category headings have:
    - Only overview paragraphs
    - No detailed lists or tables
    - heading_level typically 2 (main sections)

    Actual furniture has:
    - Lists of materials
    - Detailed paragraphs with dimensions
    - Often heading_level 3 or 4 (subsections)
    """
    content_blocks = entry.get('content_blocks', [])

    if not content_blocks:
        return False

    # Check for lists (material lists, build instructions)
    has_lists = any(block.get('type') == 'list' for block in content_blocks)

    # Check for tables (dimension tables, variant tables)
    has_tables = any(block.get('type') == 'table' for block in content_blocks)

    # Check for multiple paragraphs (detailed instructions)
    paragraph_count = sum(1 for block in content_blocks if block.get('type') == 'paragraph')
    has_detailed_paragraphs = paragraph_count >= 2

    # Special case: Closets has heading_level 3 but contains build instructions
    # Generally, heading_level 3+ are furniture items, not categories
    is_subsection = entry.get('heading_level', 2) >= 3

    # Entry is likely furniture if it has:
    # 1. Lists or tables (build instructions), OR
    # 2. Is a subsection (level 3+) with content
    return (has_lists or has_tables or is_subsection) and (has_lists or has_detailed_paragraphs or content_blocks)


def extract_first_sentence(content_blocks):
    """Extract the first sentence from content blocks for description."""
    for block in content_blocks:
        if block.get('type') == 'paragraph':
            text = block.get('text', '')
            # Get first sentence (up to first period)
            first_sentence = text.split('.')[0] + '.'
            if len(first_sentence) > 200:
                first_sentence = first_sentence[:197] + '...'
            return first_sentence
    return ""


def main():
    # Load the furniture catalog
    catalog_path = Path(__file__).parent.parent / 'context' / 'minecraft_furniture_catalog.json'

    if not catalog_path.exists():
        print(f"❌ Catalog not found at {catalog_path}")
        sys.exit(1)

    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    print(f"📚 Loaded {len(catalog)} entries from furniture catalog")

    # Filter to actual furniture items
    furniture_items = []
    category_headings = []

    for entry in catalog:
        if has_build_instructions(entry):
            furniture_items.append(entry)
        else:
            category_headings.append(entry)

    print(f"\n✅ Found {len(furniture_items)} furniture items")
    print(f"📂 Found {len(category_headings)} category headings\n")

    # Create reference table
    reference_table = []

    for item in furniture_items:
        reference_table.append({
            'name': item['name'],
            'id': item['id'],
            'hierarchy': ' > '.join(item['hierarchy']),
            'category': item['category'],
            'heading_level': item['heading_level'],
            'description': extract_first_sentence(item['content_blocks']),
            'has_lists': any(block.get('type') == 'list' for block in item['content_blocks']),
            'has_tables': any(block.get('type') == 'table' for block in item['content_blocks']),
            'block_count': len(item['content_blocks'])
        })

    # Save reference table
    output_path = Path(__file__).parent.parent / 'dev_docs' / 'furniture_inventory_reference.json'
    with open(output_path, 'w') as f:
        json.dump(reference_table, f, indent=2)

    print(f"💾 Saved reference table to {output_path}")

    # Print summary by category
    print("\n📊 Furniture items by category:")
    category_counts = {}
    for item in reference_table:
        cat = item['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1

    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count} items")

    # Print first 10 items as preview
    print("\n📋 Preview of first 10 furniture items:")
    for i, item in enumerate(reference_table[:10], 1):
        print(f"\n{i}. {item['name']}")
        print(f"   ID: {item['id']}")
        print(f"   Category: {item['category']}")
        print(f"   Hierarchy: {item['hierarchy']}")
        print(f"   Has lists: {item['has_lists']}, Has tables: {item['has_tables']}")
        print(f"   Description: {item['description'][:80]}...")

    print(f"\n✅ Extraction complete! {len(furniture_items)} furniture items identified.")
    print(f"📝 Reference table saved for layout authoring.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
