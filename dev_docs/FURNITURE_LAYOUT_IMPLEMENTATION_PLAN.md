# Implementation Plan: Structured Furniture Layouts

This plan defines how to convert the Minecraft furniture catalog into machine-actionable blueprints that AI agents can execute with WorldEdit.

## 1. Define the Placement Schema
- Finalize a JSON layout format with fields for:
  - `name`, `category`, `origin` (reference point + default facing)
  - `bounds` (`width`, `height`, `depth`)
  - `placements` (array of `block`, `fill`, optional `line`/`layer` instructions)
  - `materials`, `notes`, and optional `variants`
- Document conventions: `(0,0,0)` = front-left-bottom corner; `facing` indicates forward.
- Specify supported placement operations and block state/NBT encoding.

## 2. Curate Furniture Inventory
- Use `context/minecraft_furniture_catalog.json` as the master list.
- Extract the unique furniture entries (ignore pure category headings except “Closets” which has content).
- Build a quick reference table (name, hierarchy, raw description) for layout authoring.

## 3. Author Layout Data
- For each furniture item:
  - Derive bounding box coordinates and orientation from the tutorial text.
  - Enumerate block placements with precise coordinates and block states.
  - Capture necessary supporting blocks (e.g., banners, armor stands, water).
  - Summarize material counts and add design notes/variants.
- Save all layouts in `context/minecraft_furniture_layouts.json` as an array following the schema.

## 4. Quality Assurance
- Run a validation script to ensure every layout object passes schema checks.
- Spot-check orientations and coordinates for symmetry/accuracy.
- Verify each entry has a non-empty `placements` list and valid bounds.

## 5. Build Retrieval Tool
- Implement an MCP tool (e.g., `furniture_lookup`) with two actions:
  - `search`: substring match on `name`, `category`, `tags`.
  - `get`: fetch a single layout object by canonical name/ID.
- Ensure responses are concise and return only the requested furniture layout.

## 6. Placement Helper
- Create a helper module/MCP tool that:
  - Accepts a layout + target origin (world coordinates) and optional facing override.
  - Transforms relative coordinates into absolute coordinates.
  - Emits a list of executable WorldEdit commands (`//set`, `//fill`, etc.) or directly invokes the appropriate MCP tools.

## 7. Update Agent Guidance
- Extend `CLAUDE.md` with instructions on:
  - Searching for a furniture layout.
  - Applying the placement helper with a target origin.
  - Noting bounding boxes and undo recommendations.
- Add examples illustrating the workflow end-to-end.

## 8. Testing
- Unit-test the placement helper with sample layouts (assert generated commands align with expected coordinates/states).
- In a test world, build a handful of furniture pieces to validate orientations and block states.
- Confirm material lists match the generated builds.

## 9. Documentation & Launch
- Document the schema in `context/README.md` (field definitions, orientation rules).
- Provide onboarding notes on how to add new furniture layouts or update existing ones.
- Announce availability in changelog/README so the team can adopt the new pipeline.

## 10. Future Enhancements
- Add automatic rotation support (generate placements for all four cardinal facings).
- Introduce tagging (style, size, materials) to improve search.
- Generate optional ASCII or rendered previews for quick visual reference.
