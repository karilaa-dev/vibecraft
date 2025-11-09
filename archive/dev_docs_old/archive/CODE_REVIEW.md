# VibeCraft Code & Documentation Review

This review captures structural, correctness, and documentation issues discovered while reading the current tree. Findings are grouped by severity. Line numbers refer to the checked-in revision paths (1-based).

## Critical

- **Monolithic MCP server implementation** – `mcp-server/src/vibecraft/server.py:1` weighs in at ~5,900 lines, bundling transport setup, tool definitions, resource loading, formatting, workflow orchestration, and logging. The lack of modular boundaries makes it extremely difficult to reason about side effects, reuse logic across tools, or add tests. Refactor by splitting into focused modules (e.g., tool handlers, resource providers, logging/bootstrap) and composing them in a thin entrypoint.

## Major

- **Duplicate spatial-analysis stacks** – Two divergent analyzers live side-by-side (`mcp-server/src/vibecraft/spatial_analyzer.py:1` and `mcp-server/src/vibecraft/spatial_analyzer_v2.py:1`). The server imports both (`mcp-server/src/vibecraft/server.py:4859`, `:4967`), with large swaths of overlapping responsibilities. Consolidate into a single implementation (or clearly mark V1 as deprecated and remove its call sites) to avoid bit rot and dual maintenance.
- **Manual “tests” bypass pytest** – Files such as `mcp-server/test_furniture_placement_fix.py:1`, `mcp-server/test_search.py:1`, and `mcp-server/test_sse_tools.py:1` are executable scripts, not pytest cases, so `pytest` (configured in `pyproject.toml`) ignores them. Either convert them into real tests under `mcp-server/tests/` or relocate them to a `scripts/` directory to avoid a false sense of coverage.
- **Out-of-date setup instructions** – The comprehensive guide still instructs users to run `./setup.sh` (`docs/COMPLETE_SETUP_GUIDE.md:48`), but the supported path is the root-level `./setup-all.sh`. Update this document (and any cross references) to spotlight the single-command bootstrap, keeping manual steps in a clearly-labelled fallback section.
- **Mismatch between setup script messaging and compose config** – `setup-all.sh:214` promises “WorldEdit 7.3.10”, yet `docker-compose.yml:25` installs 7.3.17. Align the script output (and any documentation references) with the actual version to prevent confusion when verifying installs.

## Minor

- **Password generation dependency** – `setup-all.sh:98` relies on `openssl` to generate the RCON password but never checks that the binary exists. Add a prerequisite check (and a fallback using `python -c 'import secrets'`) so the script fails gracefully on systems without OpenSSL in PATH.
- **Global logger initialisation side effects** – `mcp-server/src/vibecraft/server.py:28-54` configures logging (creating log directories, attaching handlers) at import time. This makes unit testing and reuse as a library awkward. Move logging/bootstrap into the `if __name__ == "__main__"` block or an explicit `main()` routine invoked from the entry script.
- **Hard-coded absolute paths in documentation** – Several docs still reference `/Users/er/Repos/vibecraft/…` (e.g., `docs/COMPLETE_SETUP_GUIDE.md:45`, `docs/USER_ACTION_GUIDE.md:48`). Replace with placeholders or relative paths so new users aren’t misled into copy-pasting local machine paths.
- **Large static resources in source tree** – Massive reference archives (`reference-worldedit/`, `reference-rcon-mcp/`, `minecraft-data/`) live at the root. Consider documenting their purpose and, if appropriate, converting them into optional Git LFS assets or download-on-demand artifacts to keep the default clone leaner.

## Documentation Gaps & Opportunities

- `docs/README.md:5-14` should explicitly point first-time users to `./setup-all.sh`, mirroring the emphasis already present in the root README and user action guide.
- The README now highlights the quick-start script, but there’s no guidance on how to recover or rerun only parts of the setup (e.g., re-seeding the Minecraft container). A short “Reset/repair” section would reduce repeated questions.
- Several Markdown guides include very long command transcripts. Converting them into collapsible sections or linking out to dedicated troubleshooting docs would make the core path easier to scan.

## Suggested Next Steps

1. Carve `server.py` into composable modules (tool registry, resource loaders, analyzers, workflow coordination) and cover them with unit tests.
2. Decide which spatial analyzer to keep, migrate all call sites, and delete the redundant implementation.
3. Promote `./setup-all.sh` as the canonical setup path across *all* docs, keeping manual steps in a supplementary annex.
4. Modernise the ad-hoc test scripts into pytest cases so automated checks exercise the critical placement logic.
5. Harden `setup-all.sh` by checking for `openssl`, exporting the detected WorldEdit version, and collapsing duplicate log messaging.

Have fun, and thanks for the hard work bringing VibeCraft toward open-source polish!
