"""
Advanced Building Tools for VibeCraft
Provides mathematical and analytical tools for sophisticated Minecraft building
"""

import math
import logging
import re
from typing import List, Tuple, Dict, Any, Optional
from collections import Counter

from .rcon_manager import RCONManager

logger = logging.getLogger(__name__)


def fetch_block_state(rcon: RCONManager, x: int, y: int, z: int) -> Optional[Dict[str, Any]]:
    """Fetch block state (id + properties) at coordinates via RCON."""
    try:
        result = rcon.send_command(f"execute positioned {x} {y} {z} run data get block ~ ~ ~")
    except Exception as exc:
        logger.error(f"Error querying block at ({x},{y},{z}): {exc}")
        return None

    if result is None:
        return None

    text = str(result)
    match = re.search(r"minecraft:([a-z0-9_/]+)(?:\{([^}]*)\})?", text)
    if not match:
        return None

    block_id = match.group(1)
    props_str = match.group(2) or ""
    properties: Dict[str, str] = {}

    if props_str:
        for fragment in props_str.split(','):
            if ':' not in fragment:
                continue
            key, value = fragment.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"')
            properties[key] = value

    if properties:
        ordered = ','.join(f"{k}={properties[k]}" for k in sorted(properties))
        key_repr = f"{block_id}[{ordered}]"
    else:
        ordered = ""
        key_repr = block_id

    return {
        "namespaced_id": f"minecraft:{block_id}",
        "id": block_id,
        "properties": properties,
        "state": ordered,
        "key": key_repr,
        "raw": text.strip(),
    }


def block_is_air(block: Optional[Dict[str, Any]]) -> bool:
    return block is None or block.get("id") == "air"


class CircleCalculator:
    """
    Generate circles, ellipses, spheres, domes, and arches using mathematical algorithms.
    All calculations use Bresenham's algorithms for pixel-perfect results.
    """

    @staticmethod
    def calculate_circle(radius: int, filled: bool = False, center: Tuple[int, int] = (0, 0)) -> Dict[str, Any]:
        """
        Calculate a 2D circle using Bresenham's circle algorithm.

        Args:
            radius: Circle radius in blocks
            filled: If True, returns all interior points; if False, only perimeter
            center: Center coordinates (x, z)

        Returns:
            Dictionary with coordinates, block count, and WorldEdit commands
        """
        cx, cz = center
        coordinates = set()

        if filled:
            # Filled circle: use all points within radius
            for x in range(-radius, radius + 1):
                for z in range(-radius, radius + 1):
                    if x * x + z * z <= radius * radius:
                        coordinates.add((cx + x, cz + z))
        else:
            # Hollow circle: Bresenham's algorithm
            x = 0
            z = radius
            d = 3 - 2 * radius

            def add_circle_points(cx, cz, x, z):
                """Add 8-way symmetric points"""
                points = [
                    (cx + x, cz + z), (cx - x, cz + z),
                    (cx + x, cz - z), (cx - x, cz - z),
                    (cx + z, cz + x), (cx - z, cz + x),
                    (cx + z, cz - x), (cx - z, cz - x)
                ]
                return points

            while x <= z:
                coordinates.update(add_circle_points(cx, cz, x, z))
                if d < 0:
                    d = d + 4 * x + 6
                else:
                    d = d + 4 * (x - z) + 10
                    z -= 1
                x += 1

        coords_list = sorted(list(coordinates))

        # Generate ASCII preview
        ascii_preview = CircleCalculator._generate_ascii_preview(coords_list, radius, center)

        return {
            "shape": "circle",
            "center": list(center),
            "radius": radius,
            "filled": filled,
            "blocks_count": len(coords_list),
            "coordinates": coords_list,
            "ascii_preview": ascii_preview,
            "usage_tip": f"Use these coordinates to place blocks in a perfect circle (radius {radius})"
        }

    @staticmethod
    def calculate_sphere(radius: int, hollow: bool = True, center: Tuple[int, int, int] = (0, 0, 0)) -> Dict[str, Any]:
        """
        Calculate a 3D sphere.

        Args:
            radius: Sphere radius in blocks
            hollow: If True, only outer shell; if False, filled solid
            center: Center coordinates (x, y, z)

        Returns:
            Dictionary with 3D coordinates, block count, and WorldEdit commands
        """
        cx, cy, cz = center
        coordinates = set()

        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                for z in range(-radius, radius + 1):
                    distance_sq = x * x + y * y + z * z

                    if hollow:
                        # Only outer shell (distance very close to radius)
                        if abs(math.sqrt(distance_sq) - radius) < 0.7:
                            coordinates.add((cx + x, cy + y, cz + z))
                    else:
                        # Filled sphere
                        if distance_sq <= radius * radius:
                            coordinates.add((cx + x, cy + y, cz + z))

        coords_list = sorted(list(coordinates))

        return {
            "shape": "sphere",
            "center": list(center),
            "radius": radius,
            "hollow": hollow,
            "blocks_count": len(coords_list),
            "coordinates": coords_list,
            "worldedit_command": f"//sphere {'h' if hollow else ''} <block> {radius}",
            "usage_tip": f"Teleport to center then use WorldEdit or place blocks at coordinates"
        }

    @staticmethod
    def calculate_dome(radius: int, style: str = "hemisphere", center: Tuple[int, int, int] = (0, 0, 0)) -> Dict[str, Any]:
        """
        Calculate a dome (half-sphere or partial sphere).

        Args:
            radius: Dome radius in blocks
            style: "hemisphere" (half), "three_quarter" (3/4 sphere), "low" (1/4 sphere)
            center: Center coordinates (x, y, z)

        Returns:
            Dictionary with 3D coordinates for dome structure
        """
        cx, cy, cz = center
        coordinates = set()

        # Determine Y cutoff based on style
        if style == "hemisphere":
            y_min = 0
        elif style == "three_quarter":
            y_min = -radius // 2
        elif style == "low":
            y_min = radius // 2
        else:
            y_min = 0  # Default to hemisphere

        for x in range(-radius, radius + 1):
            for y in range(y_min, radius + 1):
                for z in range(-radius, radius + 1):
                    distance_sq = x * x + y * y + z * z

                    # Only outer shell
                    if abs(math.sqrt(distance_sq) - radius) < 0.7:
                        coordinates.add((cx + x, cy + y, cz + z))

        coords_list = sorted(list(coordinates))

        return {
            "shape": "dome",
            "style": style,
            "center": list(center),
            "radius": radius,
            "blocks_count": len(coords_list),
            "coordinates": coords_list,
            "usage_tip": f"Perfect for {style} dome structures (cathedrals, temples, rotundas)"
        }

    @staticmethod
    def calculate_ellipse(width: int, height: int, filled: bool = False, center: Tuple[int, int] = (0, 0)) -> Dict[str, Any]:
        """
        Calculate a 2D ellipse.

        Args:
            width: Width (X axis diameter)
            height: Height (Z axis diameter)
            filled: If True, returns all interior points
            center: Center coordinates (x, z)

        Returns:
            Dictionary with coordinates and metadata
        """
        cx, cz = center
        a = width // 2  # Semi-major axis
        b = height // 2  # Semi-minor axis
        coordinates = set()

        if filled:
            # Filled ellipse
            for x in range(-a, a + 1):
                for z in range(-b, b + 1):
                    if (x * x) / (a * a) + (z * z) / (b * b) <= 1:
                        coordinates.add((cx + x, cz + z))
        else:
            # Hollow ellipse (perimeter only)
            for angle in range(0, 360, 1):
                rad = math.radians(angle)
                x = int(a * math.cos(rad))
                z = int(b * math.sin(rad))
                coordinates.add((cx + x, cz + z))

        coords_list = sorted(list(coordinates))

        return {
            "shape": "ellipse",
            "center": list(center),
            "width": width,
            "height": height,
            "filled": filled,
            "blocks_count": len(coords_list),
            "coordinates": coords_list,
            "usage_tip": f"Ellipse {width}×{height} - useful for oval rooms, ponds, decorative features"
        }

    @staticmethod
    def calculate_arch(width: int, height: int, depth: int = 1, center: Tuple[int, int, int] = (0, 0, 0)) -> Dict[str, Any]:
        """
        Calculate an arch shape (semi-circular or pointed).

        Args:
            width: Arch width in blocks
            height: Arch height in blocks
            depth: Arch depth (thickness)
            center: Center bottom coordinates (x, y, z)

        Returns:
            Dictionary with 3D coordinates for arch structure
        """
        cx, cy, cz = center
        coordinates = set()

        # Use semi-circle formula for the arch curve
        radius = width // 2

        for x in range(-radius, radius + 1):
            # Calculate Y height at this X position (semi-circle)
            y_offset = int(math.sqrt(radius * radius - x * x))

            # Limit to specified height
            if y_offset > height:
                y_offset = height

            # Add blocks for arch thickness (depth)
            for d in range(depth):
                for y in range(y_offset):
                    # Only add blocks on the perimeter (hollow arch)
                    if abs(x) >= radius - 1 or y == y_offset - 1:
                        coordinates.add((cx + x, cy + y, cz + d))

        coords_list = sorted(list(coordinates))

        return {
            "shape": "arch",
            "center": list(center),
            "width": width,
            "height": height,
            "depth": depth,
            "blocks_count": len(coords_list),
            "coordinates": coords_list,
            "usage_tip": f"Arch {width}×{height} - perfect for doorways, bridges, windows"
        }

    @staticmethod
    def _generate_ascii_preview(coordinates: List[Tuple[int, int]], radius: int, center: Tuple[int, int]) -> str:
        """Generate ASCII art preview of 2D shape"""
        if not coordinates:
            return ""

        # Create grid
        size = radius * 2 + 3
        grid = [[' ' for _ in range(size)] for _ in range(size)]

        cx, cz = center
        offset_x = radius + 1 - cx
        offset_z = radius + 1 - cz

        for x, z in coordinates:
            grid_x = x + offset_x
            grid_z = z + offset_z
            if 0 <= grid_x < size and 0 <= grid_z < size:
                grid[grid_z][grid_x] = '█'

        # Add center marker
        center_x = cx + offset_x
        center_z = cz + offset_z
        if 0 <= center_x < size and 0 <= center_z < size:
            grid[center_z][center_x] = '+'

        return '\n'.join([''.join(row) for row in grid])


class WindowPlacementCalculator:
    """
    Calculate optimal window and door spacing for building facades.
    Based on architectural principles and aesthetic guidelines.
    """

    @staticmethod
    def calculate_window_spacing(
        wall_length: int,
        window_width: int,
        spacing_style: str = "even",
        window_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calculate optimal window placement along a wall.

        Args:
            wall_length: Total wall length in blocks
            window_width: Width of each window in blocks
            spacing_style: "even", "golden_ratio", "symmetric", "clustered"
            window_count: Optional specific number of windows (auto-calculated if None)

        Returns:
            Dictionary with window positions and spacing details
        """
        # Auto-calculate window count if not specified
        if window_count is None:
            # Rule of thumb: one window per 4-6 blocks of wall
            window_count = max(1, (wall_length - 2) // 5)

        # Calculate spacing based on style
        if spacing_style == "even":
            positions, spacing_info = WindowPlacementCalculator._even_spacing(
                wall_length, window_width, window_count
            )
        elif spacing_style == "golden_ratio":
            positions, spacing_info = WindowPlacementCalculator._golden_ratio_spacing(
                wall_length, window_width, window_count
            )
        elif spacing_style == "symmetric":
            positions, spacing_info = WindowPlacementCalculator._symmetric_spacing(
                wall_length, window_width, window_count
            )
        elif spacing_style == "clustered":
            positions, spacing_info = WindowPlacementCalculator._clustered_spacing(
                wall_length, window_width, window_count
            )
        else:
            # Default to even
            positions, spacing_info = WindowPlacementCalculator._even_spacing(
                wall_length, window_width, window_count
            )

        windows = []
        for i, pos in enumerate(positions):
            windows.append({
                "index": i + 1,
                "start_position": pos,
                "end_position": pos + window_width - 1,
                "center": pos + window_width // 2,
                "note": f"Window {i + 1} of {len(positions)}"
            })

        return {
            "wall_length": wall_length,
            "window_width": window_width,
            "window_count": len(positions),
            "spacing_style": spacing_style,
            "windows": windows,
            "spacing_info": spacing_info,
            "recommendation": WindowPlacementCalculator._get_style_recommendation(spacing_style)
        }

    @staticmethod
    def _even_spacing(wall_length: int, window_width: int, count: int) -> Tuple[List[int], Dict]:
        """Calculate evenly spaced windows"""
        total_window_width = window_width * count
        total_gap_space = wall_length - total_window_width
        gap_size = total_gap_space / (count + 1)

        positions = []
        for i in range(count):
            pos = int(gap_size * (i + 1) + window_width * i)
            positions.append(pos)

        return positions, {
            "gap_between_windows": int(gap_size),
            "edge_margins": int(gap_size),
            "style_description": "Evenly distributed with equal spacing"
        }

    @staticmethod
    def _golden_ratio_spacing(wall_length: int, window_width: int, count: int) -> Tuple[List[int], Dict]:
        """Calculate spacing based on golden ratio (1.618)"""
        golden_ratio = 1.618
        positions = []

        if count == 1:
            # Single window at golden ratio point
            pos = int(wall_length / golden_ratio) - window_width // 2
            positions.append(pos)
        else:
            # Distribute using golden ratio proportions
            segment_size = wall_length / (count + 1)
            for i in range(count):
                pos = int(segment_size * (i + 1) * (1 + 1/golden_ratio)) - window_width // 2
                positions.append(pos)

        return positions, {
            "style_description": "Positioned using golden ratio (φ = 1.618) for aesthetic balance",
            "artistic_note": "Creates visually pleasing, organic-looking arrangement"
        }

    @staticmethod
    def _symmetric_spacing(wall_length: int, window_width: int, count: int) -> Tuple[List[int], Dict]:
        """Calculate symmetric spacing around center"""
        positions = []
        center = wall_length // 2

        if count % 2 == 1:
            # Odd number: place one at center
            positions.append(center - window_width // 2)
            remaining = count - 1
            for i in range(1, remaining // 2 + 1):
                offset = i * (window_width + 2)
                positions.append(center - offset - window_width // 2)
                positions.append(center + offset - window_width // 2)
        else:
            # Even number: space around center
            for i in range(count // 2):
                offset = (i + 0.5) * (window_width + 2)
                positions.append(int(center - offset - window_width // 2))
                positions.append(int(center + offset - window_width // 2))

        positions.sort()
        return positions, {
            "center_point": center,
            "style_description": "Symmetrically arranged around center axis",
            "architectural_note": "Classic formal facade layout"
        }

    @staticmethod
    def _clustered_spacing(wall_length: int, window_width: int, count: int) -> Tuple[List[int], Dict]:
        """Calculate clustered grouping (windows in pairs or triplets)"""
        positions = []
        cluster_size = 2 if count <= 4 else 3

        num_clusters = count // cluster_size
        remaining = count % cluster_size

        # Space clusters evenly
        cluster_gap = wall_length / (num_clusters + 1)

        for i in range(num_clusters):
            cluster_start = int(cluster_gap * (i + 1))
            for j in range(cluster_size):
                pos = cluster_start + j * (window_width + 1)
                positions.append(pos)

        # Add remaining windows
        if remaining > 0:
            last_cluster_start = int(cluster_gap * (num_clusters + 0.5))
            for j in range(remaining):
                pos = last_cluster_start + j * (window_width + 1)
                positions.append(pos)

        positions.sort()
        return positions, {
            "cluster_size": cluster_size,
            "num_clusters": num_clusters,
            "style_description": f"Grouped in clusters of {cluster_size} for rhythmic pattern",
            "architectural_note": "Modern/contemporary aesthetic"
        }

    @staticmethod
    def _get_style_recommendation(style: str) -> str:
        """Get recommendation text for spacing style"""
        recommendations = {
            "even": "Best for: Modern buildings, simple facades, balanced appearance",
            "golden_ratio": "Best for: Artistic builds, museums, galleries, visually striking designs",
            "symmetric": "Best for: Castles, palaces, formal government buildings, classical architecture",
            "clustered": "Best for: Contemporary designs, urban buildings, industrial aesthetics"
        }
        return recommendations.get(style, "Spacing calculated successfully")

    @staticmethod
    def calculate_door_position(
        wall_length: int,
        door_width: int = 2,
        position: str = "center",
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Calculate optimal door placement.

        Args:
            wall_length: Total wall length
            door_width: Door width (1 or 2 typically)
            position: "center", "left", "right", "offset"
            offset: Block offset from calculated position

        Returns:
            Dictionary with door position and recommendations
        """
        if position == "center":
            door_start = (wall_length - door_width) // 2 + offset
        elif position == "left":
            door_start = 2 + offset  # 2 blocks from edge
        elif position == "right":
            door_start = wall_length - door_width - 2 + offset
        else:
            door_start = offset

        return {
            "wall_length": wall_length,
            "door_width": door_width,
            "position_style": position,
            "door_start": door_start,
            "door_end": door_start + door_width - 1,
            "door_center": door_start + door_width // 2,
            "clearance_left": door_start,
            "clearance_right": wall_length - (door_start + door_width),
            "recommendation": f"Door positioned {position}, with {door_start} blocks clearance on left"
        }


class SymmetryChecker:
    """
    Analyze structure symmetry across different axes.
    Detects asymmetries and provides correction recommendations.
    """

    def __init__(self, rcon_manager):
        """
        Initialize the symmetry checker.

        Args:
            rcon_manager: RCONManager instance for querying world blocks
        """
        self.rcon = rcon_manager

    def check_symmetry(
        self,
        x1: int, y1: int, z1: int,
        x2: int, y2: int, z2: int,
        axis: str = "x",
        tolerance: int = 0,
        resolution: int = 1
    ) -> Dict[str, Any]:
        """
        Check symmetry of a structure across a specified axis.

        Args:
            x1, y1, z1: First corner of region
            x2, y2, z2: Second corner of region
            axis: Axis to check ("x", "z", "y", "diagonal")
            tolerance: Number of allowed asymmetric blocks (0 = perfect symmetry required)
            resolution: Sampling resolution (1 = every block, 2 = every other block)

        Returns:
            Dictionary with symmetry score, asymmetric blocks, and recommendations
        """
        # Normalize coordinates
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        min_z, max_z = min(z1, z2), max(z1, z2)

        logger.info(f"Checking symmetry on {axis} axis for region ({min_x},{min_y},{min_z}) to ({max_x},{max_y},{max_z})")

        # Calculate center plane based on axis
        if axis == "x":
            center = (min_x + max_x) // 2
        elif axis == "z":
            center = (min_z + max_z) // 2
        elif axis == "y":
            center = (min_y + max_y) // 2
        else:
            return {"error": f"Invalid axis '{axis}'. Must be 'x', 'y', or 'z'."}

        # Sample blocks in region
        samples = []
        differences = []
        total_checked = 0

        for x in range(min_x, max_x + 1, resolution):
            for y in range(min_y, max_y + 1, resolution):
                for z in range(min_z, max_z + 1, resolution):
                    # Get mirror position based on axis
                    if axis == "x":
                        mirror_x = 2 * center - x
                        mirror_y, mirror_z = y, z
                        # Skip if mirror position is out of bounds or same as original
                        if mirror_x < min_x or mirror_x > max_x or mirror_x == x:
                            continue
                    elif axis == "z":
                        mirror_x, mirror_y = x, y
                        mirror_z = 2 * center - z
                        if mirror_z < min_z or mirror_z > max_z or mirror_z == z:
                            continue
                    elif axis == "y":
                        mirror_x, mirror_z = x, z
                        mirror_y = 2 * center - y
                        if mirror_y < min_y or mirror_y > max_y or mirror_y == y:
                            continue

                    # Get blocks at both positions
                    block1 = self._get_block_at(x, y, z)
                    block2 = self._get_block_at(mirror_x, mirror_y, mirror_z)

                    if block_is_air(block1) and block_is_air(block2):
                        continue

                    total_checked += 1

                    # Compare blocks
                    key1 = block1.get('key') if block1 else None
                    key2 = block2.get('key') if block2 else None

                    if key1 != key2:
                        display_block1 = key1 or "air"
                        display_block2 = key2 or "air"
                        differences.append({
                            "position1": [x, y, z],
                            "block1": display_block1,
                            "position2": [mirror_x, mirror_y, mirror_z],
                            "block2": display_block2,
                            "recommendation": f"Replace {display_block2} at ({mirror_x},{mirror_y},{mirror_z}) with {display_block1} for symmetry"
                        })

        # Calculate symmetry score
        symmetric_count = total_checked - len(differences)
        symmetry_score = (symmetric_count / total_checked * 100) if total_checked > 0 else 0

        # Determine verdict
        if len(differences) <= tolerance:
            verdict = "SYMMETRIC"
        elif symmetry_score >= 90:
            verdict = "MOSTLY_SYMMETRIC"
        elif symmetry_score >= 70:
            verdict = "PARTIALLY_SYMMETRIC"
        else:
            verdict = "ASYMMETRIC"

        logger.info(f"Symmetry check complete: {symmetry_score:.1f}% symmetric ({len(differences)} differences)")

        return {
            "symmetry_score": round(symmetry_score, 2),
            "axis": axis,
            "center_plane": center,
            "total_blocks_checked": total_checked,
            "symmetric_blocks": symmetric_count,
            "asymmetric_blocks": len(differences),
            "tolerance": tolerance,
            "verdict": verdict,
            "differences": differences[:50],  # Limit to first 50 differences
            "total_differences": len(differences),
            "summary": self._generate_symmetry_summary(symmetry_score, verdict, len(differences), axis)
        }

    def _get_block_at(self, x: int, y: int, z: int) -> Optional[Dict[str, Any]]:
        """Get block state at specific coordinates."""
        return fetch_block_state(self.rcon, x, y, z)

    def _generate_symmetry_summary(self, score: float, verdict: str, diff_count: int, axis: str) -> str:
        """Generate natural language summary of symmetry check."""
        if verdict == "SYMMETRIC":
            return f"Structure is perfectly symmetric across {axis} axis (within tolerance)"
        elif verdict == "MOSTLY_SYMMETRIC":
            return f"Structure is mostly symmetric ({score:.1f}%) with {diff_count} minor differences"
        elif verdict == "PARTIALLY_SYMMETRIC":
            return f"Structure has significant asymmetries ({score:.1f}%) - {diff_count} differences found"
        else:
            return f"Structure is highly asymmetric ({score:.1f}%) - major reconstruction needed"


class LightingAnalyzer:
    """
    Analyze lighting levels in a region and suggest optimal light source placement.
    Identifies dark spots where mobs can spawn (light level < 8).
    """

    LIGHT_SOURCE_ALWAYS = {
        'torch', 'wall_torch', 'soul_torch', 'soul_wall_torch',
        'lantern', 'soul_lantern', 'redstone_torch', 'redstone_wall_torch',
        'glowstone', 'sea_lantern', 'shroomlight', 'jack_o_lantern',
        'end_rod', 'amethyst_cluster', 'ochre_froglight', 'pearlescent_froglight',
        'verdant_froglight', 'beacon', 'sea_pickle'
    }

    LIGHT_SOURCE_REQUIRES_LIT = {
        'campfire', 'soul_campfire', 'redstone_lamp', 'furnace',
        'blast_furnace', 'smoker', 'candle', 'candle_cake',
        'white_candle', 'orange_candle', 'magenta_candle', 'light_blue_candle',
        'yellow_candle', 'lime_candle', 'pink_candle', 'gray_candle',
        'light_gray_candle', 'cyan_candle', 'purple_candle', 'blue_candle',
        'brown_candle', 'green_candle', 'red_candle', 'black_candle'
    }

    TRANSPARENT_BLOCKS = {
        'air', 'glass', 'glass_pane', 'white_stained_glass', 'light_gray_stained_glass',
        'gray_stained_glass', 'black_stained_glass', 'red_stained_glass', 'blue_stained_glass',
        'green_stained_glass', 'yellow_stained_glass', 'lime_stained_glass', 'brown_stained_glass',
        'cyan_stained_glass', 'purple_stained_glass', 'pink_stained_glass', 'orange_stained_glass',
        'magenta_stained_glass', 'light_blue_stained_glass', 'iron_bars', 'chain', 'vine', 'ladder',
        'scaffolding'
    }

    LIGHT_OFFSETS = [
        (dx, dy, dz)
        for dx in range(-4, 5)
        for dy in range(-2, 3)
        for dz in range(-4, 5)
        if abs(dx) + abs(dy) + abs(dz) <= 4
    ]

    SKY_CHECK_MAX = 40
    MAX_WORLD_HEIGHT = 319

    def __init__(self, rcon_manager):
        """
        Initialize the lighting analyzer.

        Args:
            rcon_manager: RCONManager instance for querying world data
        """
        self.rcon = rcon_manager

    def analyze_lighting(
        self,
        x1: int, y1: int, z1: int,
        x2: int, y2: int, z2: int,
        resolution: int = 2
    ) -> Dict[str, Any]:
        """
        Analyze lighting in a region.

        Args:
            x1, y1, z1: First corner of region
            x2, y2, z2: Second corner of region
            resolution: Sampling resolution (1 = every block, 2 = every other)

        Returns:
            Dictionary with light analysis and placement recommendations
        """
        # Normalize coordinates
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        min_z, max_z = min(z1, z2), max(z1, z2)

        logger.info(f"Analyzing lighting for region ({min_x},{min_y},{min_z}) to ({max_x},{max_y},{max_z})")

        # Sample light levels
        light_samples = []
        dark_spots = []

        for x in range(min_x, max_x + 1, resolution):
            for y in range(min_y, max_y + 1, resolution):
                for z in range(min_z, max_z + 1, resolution):
                    light_level = self._get_light_level(x, y, z)

                    if light_level is not None:
                        light_samples.append({
                            "position": [x, y, z],
                            "light_level": light_level
                        })

                        # Dark spot detection (< 8 allows mob spawning)
                        if light_level < 8:
                            dark_spots.append({
                                "position": [x, y, z],
                                "light_level": light_level
                            })

        if not light_samples:
            return {"error": "No light data collected from region"}

        # Calculate statistics
        light_levels = [s["light_level"] for s in light_samples]
        avg_light = sum(light_levels) / len(light_levels)

        well_lit = sum(1 for l in light_levels if l >= 12)
        dim = sum(1 for l in light_levels if 8 <= l < 12)
        dark = sum(1 for l in light_levels if l < 8)

        # Determine mob spawn risk
        dark_percentage = (dark / len(light_levels)) * 100
        if dark_percentage > 30:
            mob_risk = "HIGH"
        elif dark_percentage > 10:
            mob_risk = "MEDIUM"
        else:
            mob_risk = "LOW"

        # Calculate optimal light placements
        optimal_placements = self._calculate_light_placements(dark_spots, resolution, block_cache)

        logger.info(f"Lighting analysis complete: {len(light_samples)} samples, {len(dark_spots)} dark spots")

        return {
            "region": {
                "min": [min_x, min_y, min_z],
                "max": [max_x, max_y, max_z]
            },
            "average_light_level": round(avg_light, 2),
            "total_samples": len(light_samples),
            "dark_spots_count": len(dark_spots),
            "mob_spawn_risk": mob_risk,
            "light_distribution": {
                "well_lit": well_lit,
                "dim": dim,
                "dark": dark,
                "well_lit_percentage": round(well_lit / len(light_levels) * 100, 1),
                "dim_percentage": round(dim / len(light_levels) * 100, 1),
                "dark_percentage": round(dark / len(light_levels) * 100, 1)
            },
            "dark_spots": dark_spots[:20],  # First 20 dark spots
            "optimal_placements": optimal_placements,
            "summary": self._generate_lighting_summary(avg_light, mob_risk, len(dark_spots))
        }

    def _get_light_level(
        self,
        x: int,
        y: int,
        z: int,
        cache: Dict[Tuple[int, int, int], Optional[Dict[str, Any]]]
    ) -> Optional[int]:
        block = self._get_cached_block(x, y, z, cache)

        if block is None:
            return None

        if self._is_light_source(block):
            return 15

        if self._is_open_to_sky(x, y, z, cache):
            return 15

        nearest = self._nearest_light_source(x, y, z, cache)
        if nearest is not None:
            light_level = max(1, 15 - nearest)
        else:
            light_level = 8 if block.get('id') == 'air' else 5

        return max(0, min(15, light_level))

    def _get_cached_block(
        self,
        x: int,
        y: int,
        z: int,
        cache: Dict[Tuple[int, int, int], Optional[Dict[str, Any]]]
    ) -> Optional[Dict[str, Any]]:
        key = (x, y, z)
        if key not in cache:
            cache[key] = fetch_block_state(self.rcon, x, y, z)
        return cache[key]

    def _is_light_source(self, block: Optional[Dict[str, Any]]) -> bool:
        if not block:
            return False

        block_id = block.get('id')
        if block_id in self.LIGHT_SOURCE_ALWAYS:
            return True

        if block_id in self.LIGHT_SOURCE_REQUIRES_LIT:
            lit = block.get('properties', {}).get('lit', 'false')
            if lit.lower() == 'true':
                return True

        if block_id == 'sea_pickle':
            count = block.get('properties', {}).get('pickles', '1')
            return count not in {'0', '1'}

        return False

    def _nearest_light_source(
        self,
        x: int,
        y: int,
        z: int,
        cache: Dict[Tuple[int, int, int], Optional[Dict[str, Any]]]
    ) -> Optional[int]:
        nearest: Optional[int] = None

        for dx, dy, dz in self.LIGHT_OFFSETS:
            block = self._get_cached_block(x + dx, y + dy, z + dz, cache)
            if self._is_light_source(block):
                distance = abs(dx) + abs(dy) + abs(dz)
                if nearest is None or distance < nearest:
                    nearest = distance
                    if nearest == 0:
                        break

        return nearest

    def _is_open_to_sky(
        self,
        x: int,
        y: int,
        z: int,
        cache: Dict[Tuple[int, int, int], Optional[Dict[str, Any]]]
    ) -> bool:
        check_y = y + 1
        steps = 0

        while steps < self.SKY_CHECK_MAX and check_y <= self.MAX_WORLD_HEIGHT:
            block = self._get_cached_block(x, check_y, z, cache)
            if block and block.get('id') not in self.TRANSPARENT_BLOCKS:
                return False
            check_y += 1
            steps += 1

        return check_y > self.MAX_WORLD_HEIGHT or steps >= self.SKY_CHECK_MAX

    def _calculate_light_placements(
        self,
        dark_spots: List[Dict],
        resolution: int,
        cache: Dict[Tuple[int, int, int], Optional[Dict[str, Any]]]
    ) -> List[Dict]:
        """Calculate optimal positions for light sources based on dark spots."""
        if not dark_spots:
            return []

        # Group dark spots into clusters
        # Place one light source per cluster (roughly every 10-12 blocks)
        placements = []
        used_positions = set()

        for spot in dark_spots:
            pos = tuple(spot["position"])

            # Check if we already have a light source nearby
            nearby = False
            for used_pos in used_positions:
                distance = sum((a - b) ** 2 for a, b in zip(pos, used_pos)) ** 0.5
                if distance < 10:  # Within 10 blocks
                    nearby = True
                    break

            if not nearby:
                x, y, z = spot["position"]
                open_sky = self._is_open_to_sky(x, y, z, cache)
                block_here = self._get_cached_block(x, y, z, cache)
                suggested = "lantern" if open_sky or (block_here and block_here.get('id') not in {'air', 'water'}) else "torch"

                placements.append({
                    "position": spot["position"],
                    "current_light": spot["light_level"],
                    "suggested_source": suggested,
                    "reason": f"Dark spot (light={spot['light_level']}) - needs illumination"
                })
                used_positions.add(pos)

                # Limit to reasonable number of suggestions
                if len(placements) >= 30:
                    break

        return placements

    def _generate_lighting_summary(self, avg_light: float, mob_risk: str, dark_count: int) -> str:
        """Generate natural language summary of lighting analysis."""
        if mob_risk == "HIGH":
            return f"Poor lighting ({avg_light:.1f} avg) - {dark_count} dark spots with HIGH mob spawn risk"
        elif mob_risk == "MEDIUM":
            return f"Adequate lighting ({avg_light:.1f} avg) - {dark_count} dark spots with MEDIUM spawn risk"
        else:
            return f"Good lighting ({avg_light:.1f} avg) - {dark_count} dark spots with LOW spawn risk"


class StructureValidator:
    """
    Validate structural integrity of builds.
    Detects floating blocks, unsupported regions, and physics violations.
    """

    # Blocks affected by gravity
    GRAVITY_BLOCKS = {
        'sand', 'red_sand', 'gravel', 'concrete_powder',
        'white_concrete_powder', 'orange_concrete_powder', 'magenta_concrete_powder',
        'light_blue_concrete_powder', 'yellow_concrete_powder', 'lime_concrete_powder',
        'pink_concrete_powder', 'gray_concrete_powder', 'light_gray_concrete_powder',
        'cyan_concrete_powder', 'purple_concrete_powder', 'blue_concrete_powder',
        'brown_concrete_powder', 'green_concrete_powder', 'red_concrete_powder',
        'black_concrete_powder', 'anvil', 'chipped_anvil', 'damaged_anvil',
        'dragon_egg', 'scaffolding'
    }

    # Blocks that provide support
    SUPPORT_BLOCKS = {
        'stone', 'dirt', 'grass_block', 'cobblestone', 'planks', 'log', 'wood',
        'stone_bricks', 'bricks', 'obsidian', 'bedrock', 'concrete', 'terracotta',
        'wool', 'glass', 'iron_block', 'gold_block', 'diamond_block', 'emerald_block'
        # Add more solid blocks as needed
    }

    def __init__(self, rcon_manager):
        """
        Initialize the structure validator.

        Args:
            rcon_manager: RCONManager instance for querying world blocks
        """
        self.rcon = rcon_manager

    def validate_structure(
        self,
        x1: int, y1: int, z1: int,
        x2: int, y2: int, z2: int,
        resolution: int = 1
    ) -> Dict[str, Any]:
        """
        Validate structural integrity of a build.

        Args:
            x1, y1, z1: First corner of region
            x2, y2, z2: Second corner of region
            resolution: Sampling resolution

        Returns:
            Dictionary with validation results and issues found
        """
        # Normalize coordinates
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        min_z, max_z = min(z1, z2), max(z1, z2)

        logger.info(f"Validating structure integrity for ({min_x},{min_y},{min_z}) to ({max_x},{max_y},{max_z})")

        floating_blocks = []
        gravity_violations = []
        total_blocks = 0

        for x in range(min_x, max_x + 1, resolution):
            for y in range(min_y, max_y + 1, resolution):
                for z in range(min_z, max_z + 1, resolution):
                    block = self._get_block_at(x, y, z)

                    if block_is_air(block):
                        continue

                    total_blocks += 1

                    # Check if block is affected by gravity
                    if block and block['id'] in self.GRAVITY_BLOCKS:
                        # Check if there's support below
                        block_below = self._get_block_at(x, y - 1, z)

                        if block_is_air(block_below):
                            gravity_violations.append({
                                "position": [x, y, z],
                                "block": block.get('key'),
                                "issue": f"No support below (air at Y={y-1})",
                                "severity": "HIGH",
                                "recommendation": "Add support column or replace with non-gravity block"
                            })

                    # Check for floating non-supported blocks (simple heuristic)
                    # A block is "floating" if it has no solid neighbors (simplified check)
                    if y > min_y:  # Skip bottom layer
                        neighbors = [
                            self._get_block_at(x, y - 1, z),  # Below
                            self._get_block_at(x + 1, y, z),  # Adjacent blocks
                            self._get_block_at(x - 1, y, z),
                            self._get_block_at(x, y, z + 1),
                            self._get_block_at(x, y, z - 1),
                        ]

                        solid_neighbors = sum(1 for n in neighbors if not block_is_air(n))

                        # If no solid neighbors at all, likely floating
                        if solid_neighbors == 0:
                            floating_blocks.append({
                                "position": [x, y, z],
                                "block": block.get('key'),
                                "issue": "No adjacent solid blocks detected",
                                "severity": "MEDIUM",
                                "recommendation": "Connect to main structure or add supports"
                            })

        # Combine all issues
        all_issues = gravity_violations + floating_blocks
        structure_valid = len(all_issues) == 0

        logger.info(f"Validation complete: {total_blocks} blocks checked, {len(all_issues)} issues found")

        return {
            "structure_valid": structure_valid,
            "total_blocks_checked": total_blocks,
            "issues_found": len(all_issues),
            "gravity_violations": gravity_violations,
            "floating_blocks": floating_blocks[:20],  # First 20
            "total_floating": len(floating_blocks),
            "summary": self._generate_validation_summary(structure_valid, len(all_issues))
        }

    def _get_block_at(self, x: int, y: int, z: int) -> Optional[Dict[str, Any]]:
        """Get block state at specific coordinates."""
        return fetch_block_state(self.rcon, x, y, z)

    def _generate_validation_summary(self, valid: bool, issue_count: int) -> str:
        """Generate natural language summary of validation."""
        if valid:
            return "Structure passed validation - no physics violations detected"
        elif issue_count < 5:
            return f"Structure has {issue_count} minor issues that should be fixed"
        elif issue_count < 20:
            return f"Structure has {issue_count} issues requiring attention"
        else:
            return f"Structure has {issue_count} significant issues - major reconstruction recommended"
