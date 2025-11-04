# Implementation Plan: Terrain Planning Tool

Goal: deliver a terrain-analysis helper that can scan a user-specified region, summarize topography/biome data, and surface build considerations. The tool must be exposed through the MCP server and documented for Claude agents.

## 1. Core Capabilities
- Accept a 3D region (two corners or origin + dimensions).
- Collect elevation statistics (min/max Y, average, standard deviation, slope heatmap).
- Report block composition (top blocks, liquids, tree density, air cavities).
- Detect biome distribution and climate notes.
- Flag hazards (lava, water, caves) and opportunities (flat areas, cliffs, coastlines).
- Output JSON with machine-readable fields and a short natural-language summary.

## 2. Data Acquisition Strategy
- Preferred: query the server via WorldEdit `//chunkinfo`, `//distr`, `//biomeinfo`, or custom scanning commands if available.
- Fallback: iterate with `/execute positioned` commands to sample blocks (may be slower; consider rate limits).
- Cache results per region to avoid re-scanning large areas.

## 3. MCP Tool Design
- **Tool name**: `terrain_analyzer`.
- **Input schema**: coordinates (`x1,y1,z1`, `x2,y2,z2`), optional sampling resolution, flags for biome/block reports.
- **Output schema**: structured JSON containing stats, hazard/opportunity lists, biome summary, and plain-text recap for Claude to present.
- Handle validation (selection size limits) and error reporting (server offline, invalid region).

## 4. Server-Side Implementation Steps
1. Create a new module under `mcp-server/src/vibecraft/` (e.g., `terrain.py`) encapsulating scan logic.
2. Add utility functions for:
   - Sampling blocks via RCON commands.
   - Aggregating statistics (heights, block counts).
   - Generating hazard/opportunity heuristics.
3. Integrate with `server.py`:
   - Add import and instantiate the analyzer helper.
   - Register the `terrain_analyzer` tool in `list_tools()` with description + schema.
   - Implement call handler in `call_tool()` delegating to the analyzer module.
4. Ensure sanitization/bounds checks reuse existing safety mechanisms (coordinate validation).

## 5. Performance Considerations
- Provide an adjustable sampling resolution (e.g., analyze every block, every 2 blocks, etc.) to balance accuracy and speed.
- Limit maximum region size; return informative error if exceeded.
- Optionally support asynchronous chunk loading if the server exposes it.

## 6. Testing Plan
- Unit tests for the analyzer module (mock sampling results to verify stats and hazard detection).
- Integration test hitting the MCP tool with a known test world region.
- Manual validation in-game: compare reported summaries with actual terrain features.

## 7. Documentation & Agent Guidance
- Update `CLAUDE.md` with:
  - Tool overview.
  - Input examples and recommended workflow (e.g., analyze before planning a mega build).
  - Explanation of output fields (what “slope index” or “hazards” mean).
- Add entry to `context/README.md` if sample outputs or additional context files are created (e.g., saved terrain profiles).
- Mention the tool in repository README or changelog for visibility.

## 8. Future Enhancements
- Heatmap visualization exports (2D ASCII or image).
- Pathfinding suggestions (ideal road/bridge placements).
- Integration with furniture/structure planners to suggest optimal placement spots.
