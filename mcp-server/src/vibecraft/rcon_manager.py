"""RCON Connection Manager for Minecraft server communication"""

import logging
from typing import Optional
import warnings
from mcrcon import MCRcon
from .config import VibeCraftConfig

logger = logging.getLogger(__name__)


class RCONManager:
    """Manages RCON connections to Minecraft server"""

    def __init__(self, config: VibeCraftConfig):
        self.config = config
        self.host = config.rcon_host
        self.port = config.rcon_port
        self.password = config.rcon_password
        self.timeout = config.rcon_timeout
        self._connection: Optional[MCRcon] = None
        self._warned_send_command = False

    def execute_command(self, command: str) -> str:
        """
        Execute a command on the Minecraft server via RCON.

        Args:
            command: The command to execute (without leading slash)

        Returns:
            The server's response

        Raises:
            ConnectionError: If RCON connection fails
            TimeoutError: If command execution times out
        """
        try:
            # Create a new connection for each command
            # This is more reliable than maintaining a persistent connection
            with MCRcon(self.host, self.password, port=self.port, timeout=self.timeout) as mcr:
                if self.config.enable_command_logging:
                    logger.info(f"Executing command: {command}")

                response = mcr.command(command)

                if self.config.enable_command_logging:
                    logger.info(f"Response: {response}")

                return response

        except ConnectionRefusedError as e:
            error_msg = (
                f"Failed to connect to Minecraft server at {self.host}:{self.port}. "
                f"Ensure the server is running and RCON is enabled. Error: {str(e)}"
            )
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e

        except TimeoutError as e:
            error_msg = (
                f"Command execution timed out after {self.timeout} seconds. "
                f"The server may be overloaded or unresponsive. Command: {command}"
            )
            logger.error(error_msg)
            raise TimeoutError(error_msg) from e

        except Exception as e:
            error_msg = f"Error executing RCON command: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def test_connection(self) -> bool:
        """
        Test the RCON connection to the Minecraft server.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.execute_command("list")
            logger.info(f"RCON connection test successful: {response}")
            return True
        except Exception as e:
            logger.error(f"RCON connection test failed: {str(e)}")
            return False

    def detect_worldedit_version(self) -> Optional[str]:
        """
        Detect WorldEdit version installed on the server.

        Returns:
            WorldEdit version string or None if detection fails
        """
        try:
            response = self.execute_command("version WorldEdit")

            # Parse version from response
            # Expected format: "WorldEdit version 7.3.10"
            if "WorldEdit" in response:
                # Extract version number
                import re

                match = re.search(r"WorldEdit.*?(\d+\.\d+\.\d+)", response)
                if match:
                    version = match.group(1)
                    logger.info(f"Detected WorldEdit version: {version}")
                    return version

            logger.warning("Could not detect WorldEdit version from response: " + response)
            return None

        except Exception as e:
            logger.warning(f"Failed to detect WorldEdit version: {str(e)}")
            return None

    def get_server_info(self) -> dict[str, str]:
        """
        Get basic server information.

        Returns:
            Dictionary with server info (players, time, etc.)
        """
        info = {}

        try:
            info["players"] = self.execute_command("list")
        except Exception:
            info["players"] = "Unable to retrieve player list"

        try:
            info["time"] = self.execute_command("time query daytime")
        except Exception:
            info["time"] = "Unable to retrieve time"

        try:
            info["difficulty"] = self.execute_command("difficulty")
        except Exception:
            info["difficulty"] = "Unable to retrieve difficulty"

        return info

    # ------------------------------------------------------------------
    # Backwards-compatibility helpers
    # ------------------------------------------------------------------
    def send_command(self, command: str) -> str:
        """Compatibility wrapper for legacy code expecting send_command.

        Historically the RCON helper exposed ``send_command``. The current
        API uses ``execute_command``. Some modules (terrain analysis, player
        context helpers) still import the legacy name, so we proxy here and
        strip a leading slash if present.
        """

        if not self._warned_send_command:
            warnings.warn(
                "RCONManager.send_command is deprecated; use execute_command",
                DeprecationWarning,
                stacklevel=2,
            )
            self._warned_send_command = True

        sanitized = command.strip()
        if sanitized.startswith("/"):
            sanitized = sanitized[1:]
        return self.execute_command(sanitized)
