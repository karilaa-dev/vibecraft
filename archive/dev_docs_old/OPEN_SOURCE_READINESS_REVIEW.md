# VibeCraft – Open Source Readiness Review

Date: 2025-11-05
Reviewer: Automated pass focused on investor-facing polish + FAANG-grade quality bar.

## Summary
Great progress on modularizing the MCP server and trimming unused assets. However, the latest sweep surfaced several blocking defects (broken imports, async misuse, failing tests) plus doc inconsistencies that would stop external contributors and investors. Below are the actionable findings ordered by severity.

## Critical Issues

1. **Invalid safety import breaks `rcon_command`**  
   File: `mcp-server/src/vibecraft/tools/core_tools.py:61`  
   The handler still does `from ..safety import …` even though the module is `sanitizer.py`. Calling `rcon_command` raises `ModuleNotFoundError`, blocking every tool that proxies through this helper. **Fix:** change the import to `from ..sanitizer import …` (or expose a proper safety module) and add a unit test.

2. **Missing `minecraft_items_loader` module**  
   File: `mcp-server/src/vibecraft/tools/helper_utils.py:76`  
   `handle_search_minecraft_item` imports `..minecraft_items_loader`, which no longer exists after the refactor (items now load inside `server.py`). The tool crashes immediately. **Fix:** import the shared list from the new location (e.g., move loader into its own module or expose a getter).

3. **`await` used on synchronous RCON calls**  
   Files: `mcp-server/src/vibecraft/tools/helper_utils.py:159-334`, `mcp-server/src/vibecraft/tools/worldedit_advanced.py:31/102/170/208`  
   `RCONManager.send_command()` is synchronous and returns a string; awaiting it raises `TypeError: object str can't be used in 'await' expression`. Every helper listed (player position, surface detection, vegetation, deform, etc.) currently explodes. **Fix:** remove `await` and call the synchronous method, or convert `RCONManager` to async.

4. **Pytest suite cannot import the package**  
   File: `mcp-server/tests/test_minecraft_item_search.py:9`  
   Tests execute `from vibecraft.server import minecraft_items`, but when running `pytest` inside `mcp-server` the `src/` directory isn’t on `PYTHONPATH`. `python3 -c "import vibecraft"` fails with `ModuleNotFoundError`. CI (see `.github/workflows/tests.yml`) only installs requirements, not the package, so every run will fail. **Fix:** add `pip install -e .` (or `python -m pip install .`) before running tests, or update tests to insert `src` into `sys.path`.

## Major Issues

5. **Helper docs/tools still reference removed APIs**  
   Files: `AGENTS/minecraft-interior-designer.md:189-205`, `AGENTS/minecraft-master-planner.md:142-145`  
   Both specialist prompts require `analyze_placement_area`, but that tool has been removed in favor of `spatial_awareness_scan`. Agents now instruct users to call a non-existent MCP tool. **Fix:** update all agent playbooks to reference the surviving V2 scan workflow.

6. **Agent prompts refer to deleted context file**  
   Files: e.g., `AGENTS/minecraft-facade-architect.md:56`, `AGENTS/minecraft-redstone-engineer.md:23`, `AGENTS/minecraft-shell-engineer.md:208`  
   They tell Claude to read `context/minecraft_items.txt`, but that TOON file was removed during cleanup. The canonical sources are `context/minecraft_items_filtered.json` + `context/README.md`. **Fix:** update every agent reference and regenerate prompts.

7. **CI workflow doesn’t install the project under test**  
   File: `.github/workflows/tests.yml`  
   The workflow installs `requirements.txt` and `requirements-dev.txt` but never `pip install -e .`, so pytest still can’t import `vibecraft`. Even after fixing the local tests, CI will remain red without this step.

8. **`mcp-server/README.md` hardcodes personal paths**  
   File: `mcp-server/README.md:31-119`  
   Setup instructions still reference `/Users/er/Repos/vibecraft/...`, which is confusing for external engineers. Replace with `$VIBECRAFT_ROOT` or relative paths, matching the polish in the root README.

9. **Root README uses placeholder clone URL**  
   File: `README.md:34`  
   Quick start shows `git clone https://github.com/your-org/vibecraft.git`. For public investors, this should be the actual repository URL.

## Minor / Polish

10. **Unused `formatters/` package**  
    Directory: `mcp-server/src/vibecraft/formatters/` (empty `__init__.py`)  
    The refactor created the package but nothing imports or implements formatters yet. Either add real formatter modules or remove the placeholder to avoid confusion.

11. **Documentation purge left gaps**  
    The `docs/` directory now only contains `MINECRAFT_SERVER_SETUP.md`, but previous essentials (`USER_ACTION_GUIDE.md`, `COMPLETE_SETUP_GUIDE.md`, reset procedures) were deleted. README links no longer exist, and there is no dedicated troubleshooting or AI-client configuration doc beyond the main README. Restoring or rewriting these guides would better match the “investor-ready” expectation.

## Recommendations

- Fix the import + async issues first; they currently break core functionality.
- Update CI/test harness to install the package so tests and workflows succeed consistently.
- Align every piece of documentation and agent guidance with the refactored toolset (`spatial_awareness_scan`, JSON item files, etc.).
- Remove or flesh out placeholder modules/directory structures to avoid signaling unfinished work.
- Replace local file paths and placeholder URLs with production-ready values.

With these addressed, the repo will present far more like a polished, high-value open source project.
