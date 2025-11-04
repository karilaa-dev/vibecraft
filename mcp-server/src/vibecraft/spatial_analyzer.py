"""
Spatial Analysis Helper

Analyzes blocks in a local area to provide spatial context for precise placement.
Used for furniture placement (finding floors/ceilings) and roof construction (detecting stair patterns).
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from collections import Counter

logger = logging.getLogger(__name__)


class SpatialAnalyzer:
    """
    Analyzes spatial context around a point in Minecraft world.

    Provides:
    - Surface detection (floor Y, ceiling Y, walls)
    - Roof context (existing stairs, next layer offset)
    - Block grid mapping
    - Placement recommendations
    """

    def __init__(self, rcon_manager):
        """Initialize with RCON manager for block queries."""
        self.rcon = rcon_manager

    def analyze_area(
        self,
        center_x: int,
        center_y: int,
        center_z: int,
        radius: int = 5,
        analysis_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Analyze area around center point.

        Args:
            center_x, center_y, center_z: Center coordinates
            radius: Scan radius (default 5 blocks)
            analysis_type: "general", "surfaces", "roof_context", "furniture_placement"

        Returns:
            Dictionary with analysis results including surfaces, blocks, and recommendations
        """
        logger.info(f"Analyzing placement area at ({center_x},{center_y},{center_z}) radius={radius} type={analysis_type}")

        # Scan blocks in area
        blocks = self._scan_blocks(center_x, center_y, center_z, radius)

        result = {
            "center": [center_x, center_y, center_z],
            "radius": radius,
            "analysis_type": analysis_type
        }

        # Always detect surfaces
        surfaces = self._detect_surfaces(center_x, center_y, center_z, blocks)
        result["surfaces"] = surfaces

        # Type-specific analysis
        if analysis_type in ["furniture_placement", "general"]:
            result["furniture_placement"] = self._analyze_furniture_placement(
                center_x, center_y, center_z, surfaces, blocks
            )

        if analysis_type in ["roof_context", "general"]:
            result["roof_context"] = self._analyze_roof_context(
                center_x, center_y, center_z, blocks, radius
            )

        # Include block grid if requested
        if analysis_type == "general":
            result["blocks"] = self._format_block_grid(center_x, center_y, center_z, blocks)

        return result

    def _scan_blocks(
        self,
        center_x: int,
        center_y: int,
        center_z: int,
        radius: int
    ) -> Dict[Tuple[int, int, int], str]:
        """
        Scan all blocks in radius around center.

        Returns:
            Dict mapping (x,y,z) to block type
        """
        blocks = {}

        # Limit scan size for performance
        max_blocks = 500
        blocks_scanned = 0

        # Scan in 3D cube
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    if blocks_scanned >= max_blocks:
                        logger.warning(f"Hit max blocks limit ({max_blocks}), stopping scan")
                        return blocks

                    x = center_x + dx
                    y = center_y + dy
                    z = center_z + dz

                    # Get block at position
                    block_type = self._get_block_at(x, y, z)
                    if block_type:
                        blocks[(x, y, z)] = block_type
                        blocks_scanned += 1

        logger.info(f"Scanned {blocks_scanned} blocks")
        return blocks

    def _get_block_at(self, x: int, y: int, z: int) -> Optional[str]:
        """
        Get block type at coordinates using WorldEdit.
        Same as terrain analyzer approach.
        """
        try:
            # Set WorldEdit selection to single block
            self.rcon.send_command(f"//pos1 {x},{y},{z}")
            self.rcon.send_command(f"//pos2 {x},{y},{z}")

            # Get block distribution
            result = self.rcon.send_command("//distr")

            if result is None:
                return None

            result = str(result)

            # Parse WorldEdit distribution output
            import re
            match = re.search(r'[\d.]+%\s+([a-z_:]+)', result, re.IGNORECASE)
            if match:
                block_name = match.group(1)
                # Remove minecraft: prefix if present
                if ':' in block_name:
                    block_name = block_name.split(':', 1)[1]
                return block_name

            return None
        except Exception as e:
            # Silently handle errors
            return None

    def _detect_surfaces(
        self,
        center_x: int,
        center_y: int,
        center_z: int,
        blocks: Dict[Tuple[int, int, int], str]
    ) -> Dict[str, Any]:
        """
        Detect floor, ceiling, and wall surfaces around center point.

        Returns:
            {
                "floor_y": Y coordinate of floor surface (top of solid block),
                "ceiling_y": Y coordinate of ceiling surface (bottom of solid block),
                "walls": List of directions with walls (["north", "south", "east", "west"])
            }
        """
        # Find floor: scan downward from center until hitting solid block
        floor_y = None
        for dy in range(0, -10, -1):  # Scan down up to 10 blocks
            check_y = center_y + dy
            block = blocks.get((center_x, check_y, center_z))
            if block and block != "air" and self._is_solid_block(block):
                floor_y = check_y  # This is the floor BLOCK Y
                break

        # Find ceiling: scan upward from center until hitting solid block
        ceiling_y = None
        for dy in range(0, 10):  # Scan up up to 10 blocks
            check_y = center_y + dy
            block = blocks.get((center_x, check_y, center_z))
            if block and block != "air" and self._is_solid_block(block):
                ceiling_y = check_y  # This is the ceiling BLOCK Y
                break

        # Detect walls in cardinal directions
        walls = []
        wall_checks = {
            "north": (center_x, center_y, center_z - 1),
            "south": (center_x, center_y, center_z + 1),
            "east": (center_x + 1, center_y, center_z),
            "west": (center_x - 1, center_y, center_z)
        }

        for direction, pos in wall_checks.items():
            block = blocks.get(pos)
            if block and block != "air" and self._is_solid_block(block):
                walls.append(direction)

        return {
            "floor_y": floor_y,
            "ceiling_y": ceiling_y,
            "walls": walls
        }

    def _is_solid_block(self, block_name: str) -> bool:
        """Check if block is solid (not air, not transparent)."""
        # List of non-solid blocks
        non_solid = {
            "air", "water", "lava", "flowing_water", "flowing_lava",
            "torch", "wall_torch", "redstone_torch", "soul_torch",
            "ladder", "vine", "snow", "tall_grass", "grass", "fern",
            "dead_bush", "flower", "rose", "dandelion", "poppy",
            "sign", "wall_sign", "banner", "wall_banner"
        }

        # Check if block is in non-solid list
        for non_solid_name in non_solid:
            if non_solid_name in block_name.lower():
                return False

        # Default to solid
        return True

    def _analyze_furniture_placement(
        self,
        center_x: int,
        center_y: int,
        center_z: int,
        surfaces: Dict[str, Any],
        blocks: Dict[Tuple[int, int, int], str]
    ) -> Dict[str, Any]:
        """
        Provide furniture placement recommendations.

        Returns:
            {
                "recommended_floor_y": Y to place floor furniture (on top of floor),
                "recommended_ceiling_y": Y to place ceiling furniture (at ceiling bottom),
                "placement_type": "floor" or "ceiling" or "wall",
                "clear_space": True if there's room
            }
        """
        floor_y = surfaces.get("floor_y")
        ceiling_y = surfaces.get("ceiling_y")

        # Floor placement: ON TOP of floor block (floor_y + 1)
        recommended_floor_y = floor_y + 1 if floor_y is not None else center_y

        # Ceiling placement: AT ceiling block (same Y as ceiling block for hanging)
        recommended_ceiling_y = ceiling_y if ceiling_y is not None else center_y

        # Determine placement type based on context
        # If we're close to floor, it's floor placement
        # If we're close to ceiling, it's ceiling placement
        if floor_y and ceiling_y:
            dist_to_floor = abs(center_y - floor_y)
            dist_to_ceiling = abs(center_y - ceiling_y)
            placement_type = "floor" if dist_to_floor < dist_to_ceiling else "ceiling"
        elif floor_y:
            placement_type = "floor"
        elif ceiling_y:
            placement_type = "ceiling"
        else:
            placement_type = "floor"  # Default

        # Check if there's clear space at placement position
        if placement_type == "floor":
            check_pos = (center_x, recommended_floor_y, center_z)
        else:
            check_pos = (center_x, recommended_ceiling_y - 1, center_z)  # Below ceiling

        clear_space = blocks.get(check_pos, "air") == "air"

        return {
            "recommended_floor_y": recommended_floor_y,
            "recommended_ceiling_y": recommended_ceiling_y,
            "placement_type": placement_type,
            "clear_space": clear_space,
            "floor_block_y": floor_y,  # Actual floor block
            "ceiling_block_y": ceiling_y  # Actual ceiling block
        }

    def _analyze_roof_context(
        self,
        center_x: int,
        center_y: int,
        center_z: int,
        blocks: Dict[Tuple[int, int, int], str],
        radius: int
    ) -> Dict[str, Any]:
        """
        Analyze existing roof structure to guide next layer placement.

        Returns:
            {
                "existing_stairs": List of stair positions and orientations,
                "slope_direction": "north-south" or "east-west" or "unknown",
                "last_stair_layer_y": Highest Y with stairs,
                "next_layer_offset": {"x": 0, "y": 1, "z": 1} suggestion,
                "ridge_y": Estimated ridge height,
                "uses_full_blocks": True if ridge uses full blocks
            }
        """
        # Find all stair blocks
        stairs = []
        for (x, y, z), block in blocks.items():
            if "stairs" in block.lower():
                stairs.append({"pos": [x, y, z], "block": block})

        if not stairs:
            return {
                "existing_stairs": [],
                "slope_direction": "unknown",
                "recommendation": "No existing stairs found. Start fresh with proper offset pattern."
            }

        # Find highest stair layer
        max_stair_y = max(s["pos"][1] for s in stairs)

        # Detect slope direction by looking at stair positions
        # If stairs vary more in Z than X, slope is N-S
        # If stairs vary more in X than Z, slope is E-W
        x_variance = max(s["pos"][0] for s in stairs) - min(s["pos"][0] for s in stairs)
        z_variance = max(s["pos"][2] for s in stairs) - min(s["pos"][2] for s in stairs)

        if z_variance > x_variance:
            slope_direction = "north-south"
            offset_axis = "z"
        elif x_variance > z_variance:
            slope_direction = "east-west"
            offset_axis = "x"
        else:
            slope_direction = "unknown"
            offset_axis = "z"  # Default

        # Suggest next layer offset
        # Each layer should step inward by 1 block and up by 1 block
        next_offset = {
            "x": 1 if offset_axis == "x" else 0,
            "y": 1,
            "z": 1 if offset_axis == "z" else 0
        }

        # Estimate ridge Y (few blocks above highest stairs)
        ridge_y = max_stair_y + 3

        # Check if full blocks are used (common at ridge)
        full_blocks_at_top = any(
            blocks.get((x, max_stair_y + 1, z)) and "stairs" not in blocks.get((x, max_stair_y + 1, z), "").lower()
            for x, y, z in [s["pos"] for s in stairs]
        )

        return {
            "existing_stairs": stairs[:10],  # Limit to first 10 for readability
            "total_stairs_found": len(stairs),
            "slope_direction": slope_direction,
            "last_stair_layer_y": max_stair_y,
            "next_layer_offset": next_offset,
            "ridge_y": ridge_y,
            "uses_full_blocks": full_blocks_at_top,
            "recommendation": f"Step inward {offset_axis.upper()}+1 and up Y+1 for next layer. Use full blocks near ridge (Y≈{ridge_y})."
        }

    def _format_block_grid(
        self,
        center_x: int,
        center_y: int,
        center_z: int,
        blocks: Dict[Tuple[int, int, int], str]
    ) -> Dict[str, str]:
        """
        Format block grid as relative coordinates from center.

        Returns:
            {"dx,dy,dz": "block_type", ...}
        """
        grid = {}
        for (x, y, z), block in blocks.items():
            dx = x - center_x
            dy = y - center_y
            dz = z - center_z
            grid[f"{dx},{dy},{dz}"] = block

        return grid
