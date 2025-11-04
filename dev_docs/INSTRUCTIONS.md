Plan for VibeCraft POC: AI‐Powered WorldEdit in Minecraft

Overview

VibeCraft is a proof-of-concept for AI-assisted building in Minecraft using the WorldEdit toolset. The goal is to let a coding agent (e.g. Anthropic’s Claude or similar) generate Minecraft builds via code. We will achieve this by exposing WorldEdit’s powerful editing functions through a Model Context Protocol (MCP) server. This MCP server acts as a bridge between the AI and a running Minecraft server, allowing the AI to execute WorldEdit commands in the game world ￼ ￼. In summary, the POC will consist of:
	•	A Minecraft server (running on Linux or macOS) with WorldEdit installed (latest version).
	•	A Model Context Protocol server that exposes WorldEdit functions via a simple API (using Minecraft’s RCON or a custom plugin).
	•	Integration with an AI coding agent (like Claude Code or Cursor) so the AI can call the MCP server’s functions to manipulate the Minecraft world.

This plan outlines how to set up each component and integrate them into a working system. The emphasis is on simplicity for a minimal POC, even if some trade-offs (like using RCON) are made for ease of implementation.

1. Set Up Minecraft Server with WorldEdit

Choose the Latest Supported Versions: To maximize compatibility, use the latest Minecraft version that WorldEdit supports. As of late 2025, WorldEdit 7.3.17 is the newest stable release and supports Minecraft Java Edition up to version 1.21.10 ￼. This ensures we have access to the newest game features and WorldEdit functions. Key setup steps:
	•	Install a Minecraft Server: Use a server modding platform that supports WorldEdit. A simple choice is PaperMC (a high-performance Spigot fork) for the corresponding Minecraft version (e.g. Paper 1.21.x if available). Paper/Bukkit allows easy plugin installation. Alternatively, Fabric or NeoForge can be used with WorldEdit’s mod version ￼ ￼, but this POC will assume a Paper server for simplicity.
	•	Download WorldEdit: Get the latest WorldEdit plugin JAR for your platform/version. For Paper (Bukkit API), download WorldEdit 7.3.17 (Bukkit/Paper edition) which supports MC 1.21.3–1.21.10 ￼. Place the WorldEdit.jar into the server’s plugins/ directory. (On Fabric or Forge, you’d instead use the WorldEdit mod file in the mods/ folder.)
	•	Initial Server Configuration: Accept the EULA and run the server once to generate config files. Then, enable cheats and admin access. If using Paper, make sure you are an operator (/op <yourname>) so you can use WorldEdit commands in-game. We will also enable RCON (Remote Console) for external control: in the generated server.properties file, set:

enable-rcon=true  
rcon.password=<choose-a-secure-password>  
rcon.port=25575  

These settings allow an external program to send console commands to the server ￼. Use a strong password since RCON is powerful.

	•	Launch the Server: Start the Minecraft server (e.g. java -Xms1G -Xmx2G -jar paper-1.21.jar nogui). On first launch with WorldEdit, verify that WorldEdit loads (you should see WorldEdit messages in the console). Once running, you can join the server with your Minecraft client (for testing/observation). Use a creative mode, flat world for ease of building.

At this stage, we have a vanilla Minecraft world with WorldEdit installed and ready. You can manually test WorldEdit (e.g., select an area and run //set stone) in-game to ensure it functions. The server’s RCON interface is also enabled for external tool access.

2. Implement the MCP Server Bridge to WorldEdit

Next, we create a Model Context Protocol (MCP) server that bridges AI commands to Minecraft/WorldEdit actions. The simplest approach for a POC is to leverage Minecraft’s RCON to send WorldEdit commands to the server console ￼. This avoids writing a custom Minecraft plugin and uses existing infrastructure: the MCP server will just act as an RCON client. Key steps:
	•	Use MCP SDK or Example: The Model Context Protocol provides SDKs in multiple languages (Python, TypeScript, etc.) ￼. For quick development on Linux/Mac, Python is a good choice due to its simplicity and available libraries. In fact, open-source MCP server examples already exist for Minecraft RCON. For example, Kyle Kelley’s “Minecraft RCON MCP server” demonstrates connecting AI assistants to Minecraft via RCON ￼. We can draw inspiration or even reuse components from such projects. (Another reference is Peterson047’s Minecraft-MCP-Server, which uses a similar approach with a tool called run_minecraft_command that sends commands via the mcrcon library ￼.)
	•	Implement RCON Command Tool: Using the Python MCP SDK, implement a tool function (e.g. run_command(command: str)) that takes a command string and executes it on the Minecraft server via RCON. For this, use a Python RCON client library (such as mcrcon or mcipc on PyPI) to connect to localhost:25575 with the password set earlier ￼. The tool should then send the given command and return any output or confirmation. Example: If the AI calls run_command("/setblock 100 64 100 minecraft:stone"), the MCP server will send that to Minecraft’s console and perhaps return the result (“Block placed” or similar).
	•	Note: WorldEdit commands typically start with //. The RCON tool can handle any console command, including WorldEdit’s. Ensure the WorldEdit plugin allows console usage of a command or provide necessary context (e.g. using //pos1 x,y,z syntax for console selections as needed). Many WorldEdit functions can be invoked by console if coordinates are specified, as an operator ￼. For instance, one can set region corners via //pos1 X,Y,Z from console (with comma-separated coords) and then run //set <block> ￼. We may have the AI directly specify coordinates in its commands to avoid relying on a player’s selection.
	•	Expose WorldEdit Functions: For a minimal POC, it might be sufficient to expose a generic “execute command” tool (letting the AI send arbitrary commands, including all WorldEdit // commands). This effectively gives access to all WorldEdit functionality without having to wrap each function individually. However, one can improve AI’s understanding by providing a list of available commands (a resource or JSON of WorldEdit commands and descriptions). In fact, the MCP server could load a commands dictionary (e.g. listing commands like //set, //copy, //paste, etc.) as a read-only resource for the AI ￼ ￼. This helps the AI plan complex actions by knowing what tools are at its disposal. For the POC, we can skip the full dictionary and rely on the AI’s general knowledge or simple documentation.
	•	Security & Constraints: Since this is local and a quick demo, we won’t implement heavy security. But do be mindful that giving an AI unrestricted command access is powerful. You can mitigate risk by instructing the AI (in its prompt) to only build within a certain coordinate range and avoid destructive commands outside that region. If needed, the MCP server itself could enforce bounds (e.g. check the coordinates in the command string against allowed min/max and refuse if out of range). For the initial POC, a clear coordinate range in the prompt and using a dedicated creative world should suffice.

Development tip: To speed up this step, you can leverage existing code. For example, the rcon-mcp project can be installed and used directly. According to its docs, you can install it via the MCP CLI and run it with a one-liner ￼. This server already includes tools for listing players, executing commands, etc. Using such a pre-built MCP server can save time – just ensure to configure the RCON credentials (host, port, password) in its config or environment as required. If you prefer writing it yourself, use the MCP Python SDK to scaffold a server and define a single tool function as described. Either way, the MCP server will run as a separate process, continuously listening for requests from the AI and forwarding them to Minecraft.

3. Integrate the MCP Server with an AI Agent

With the Minecraft world and the MCP bridge in place, the next step is to hook this up to a coding AI assistant (Claude, etc.) so it can actually use the new “VibeCraft” tool. The integration will differ slightly depending on the agent, but generally involves registering the MCP server in the AI assistant’s settings:
	•	Claude Code / Claude Desktop: Claude supports MCP servers via config files. You need to add an entry for our new server. For example, in Claude Desktop’s config (claude_desktop_config.json on macOS/Linux), under "mcpServers" you would add something like:

{
  "mcpServers": {
     "minecraft-worldedit": {
       "command": "python",
       "args": ["-m", "rcon"], 
       "env": { "RCON_HOST": "127.0.0.1", "RCON_PORT": "25575", "RCON_PASSWORD": "<your-password>" }
     }
  }
}

This assumes you installed a module rcon that runs the MCP server (for instance, if using the rcon-mcp package). The above configuration is illustrative – you’d replace it with the actual command to start your MCP server. Claude’s documentation shows that you can also add servers via the CLI; e.g., running a command like claude mcp add-json "minecraft-worldedit" '{"command":"python","args":["-m","rcon"]}' achieves a similar result ￼. After adding the config, restart Claude Desktop. Claude should detect the new MCP server and list the tools it provides (e.g. a tool to run Minecraft commands).

	•	Cursor or Other IDE Agents: If you use Cursor (an AI coding assistant IDE) or similar, they also support MCP. For Cursor, you’d edit or create an .cursor/mcp.json file with an entry for the MCP server (very similar JSON structure as Claude’s) ￼. The concept is the same: point the AI to the executable that runs the MCP server. Ensure the MCP server is running before you start using the agent.
	•	Test the Connection: Once configured, you can verify the agent sees the MCP server’s tools. For example, you might ask the AI (in natural language) “What tools do you have available?”. It should mention something related to Minecraft or WorldEdit. Alternatively, check the MCP server’s console logs to see if the AI connected and queried the available functions.

At this point, your AI assistant knows how to call the WorldEdit API via the MCP server. We can now issue a build command to test the whole loop.

4. Testing the VibeCraft POC

Finally, it’s time to prompt the AI to build something and watch it happen in Minecraft. Make sure all components are running: the Minecraft server (with you logged in to observe), and the MCP server process (connected via RCON). Then:
	•	Define the Build Region: As the user, tell the AI what area it can build in. For example: “You can build within the region from (100, 64, 100) to (130, 80, 130) in the Minecraft world. Please create a structure or scene within these coordinates.” This gives the assistant the boundaries (a ~30×16×30 area in this case). The AI will use these coordinates in its planning. (This step is important to keep the AI’s operations focused and manageable, as well as to mimic the “vibe” or theme context if needed.)
	•	Request a Build: Now ask the AI to build something creative. For example: “Build a small wooden cottage with a stone chimney and glass windows within the given region.” The AI (Claude or others) will interpret this and translate it into a series of WorldEdit (or vanilla Minecraft) commands. Depending on the agent’s capabilities and the provided tools, it might do something like: select coordinates for walls, use //set to fill in walls, //cut out door/window holes, etc., or place individual schematic pieces. Because we gave it access to WorldEdit functions, it can manipulate large areas quickly (e.g. fill a volume with a block type in one command).
	•	Execution via MCP: The AI will call the MCP server’s tool functions as needed. For instance, it may invoke minecraft-worldedit.run_command with arguments like "/fill 100 64 100 130 64 130 minecraft:oak_planks" to lay a floor, or WorldEdit’s //walls command to erect walls. Each call goes from the AI to the MCP server, which sends it via RCON to Minecraft. WorldEdit processes it on the server and modifies the world. The outcome (like “2100 blocks changed”) might be returned and the AI can use that feedback or proceed to the next step. All these changes happen in real time – if you’re in the game, you will see blocks appearing as the AI “builds”.
	•	Observe and Iterate: Watch the structure take shape in Minecraft. You may need a few iterations to get a sensible result – AI might make an error or you might need to clarify the prompt. For example, if the AI’s first attempt isn’t quite right, you can refine the request (“make the house taller” or “add a roof”). Thanks to WorldEdit, adjustments are easy (it can replace materials or expand selections quickly). The POC’s success criterion is that you can conversationally instruct the AI to create or modify the build, and it happens in the game via WorldEdit. This demonstrates the core concept of VibeCraft.

Throughout testing, ensure the AI stays within the allowed range and uses appropriate commands. In a POC setting, you’ll likely guide the AI step-by-step. For example, you might first ask it to fill a foundation, then build walls, etc., rather than one-shot “build a castle” (which is complex). This helps identify which WorldEdit functions are useful and verify each in turn.

5. Platform Notes (Linux/Mac)

The above setup is OS-agnostic with a slight leaning on Unix-like environments (which covers Linux and macOS). Both Linux and Mac have no issues running Java for the server and Python for the MCP. A few tips specific to these platforms:
	•	Java Installation: Ensure you have a recent Java JDK/JRE installed (Minecraft 1.21+ likely requires Java 17 or higher). On Mac, the AdoptOpenJDK or Temurin distribution works well; on Ubuntu/Debian, use the package manager to install OpenJDK.
	•	Firewall/Networking: If all processes run on the same machine, you don’t need special network config (the MCP server can connect to localhost:25575). If you separate them (e.g. Minecraft in Docker or another host), make sure to allow the RCON port. For local testing, it’s simplest to keep everything on one machine.
	•	Scripts and Permissions: On Linux/Mac, you can create shell scripts to start the server and MCP easily. For example, a start_minecraft.sh to launch the Paper JAR, and a start_mcp.sh to run the Python MCP server (activate a venv if used). Ensure these scripts have execute permission (chmod +x).
	•	Logging: Tail the Minecraft server log (e.g. logs/latest.log) in a terminal to see incoming commands and any errors. This is useful on Linux/macOS with tail -f. It will show WorldEdit actions (and any mistakes the AI made in commands). The MCP server process may also print its own logs to stdout. Using two terminal windows (one for server, one for MCP) can be very helpful for debugging in real time.

By following this plan, you will have a working POC of VibeCraft. In this setup, all WorldEdit functionality is at the AI’s fingertips – from simple block placement to complex terraforming. The combination of Model Context Protocol and WorldEdit’s extensive API is what makes this possible. You’ve essentially created a sandbox where an AI coder can “dream up” a structure and directly manifest it in Minecraft via code.

6. Next Steps and Enhancements (Beyond POC)

(Optional, for future consideration.) Once the basic POC is working, you could enhance VibeCraft in several ways:
	•	Direct WorldEdit API Integration: For more fine-grained control, writing a custom Minecraft plugin that exposes WorldEdit’s Java API to the MCP server (e.g. via a WebSocket or HTTP API) could eliminate reliance on RCON text commands. This could provide structured functions like createSphere(center, radius, block) rather than free-form strings. It’s more complex to implement, but can give better feedback and error handling.
	•	Safety and Constraints: Implement more checks so the AI cannot accidentally destroy areas outside the vibe zone. Also, consider running the server in a controlled environment (e.g. snapshots of world or a disposable world) when letting an AI execute commands, especially if using powerful WorldEdit operations.
	•	AI Prompt Engineering: Provide the AI with the WorldEdit command reference (or a summary of key commands) so it can plan builds more effectively. This can be done by supplying a “commands dictionary” resource via MCP, as mentioned earlier, or simply including a brief cheat-sheet in the prompt. For example, listing that //walls builds perimeter walls of a selection, //sphere creates a sphere at your position, etc. The richer the AI’s understanding, the more creative and correct its outputs will be.
	•	Multi-Step Builds & Memory: Encourage the AI to break down large builds into steps (foundation, structure, detailing). The MCP/Claude environment might allow maintaining state or notes. WorldEdit also supports schematics; an AI could generate a schematic file and have WorldEdit load it – this could be a future improvement for very complex structures.

By implementing the above, the VibeCraft project can evolve from a simple POC into a robust system for AI-driven creative building in Minecraft. For now, you have a complete plan to get a minimal version up and running. Happy building! 🚀

Sources:
	•	WorldEdit latest version and compatibility ￼ (EngineHub/Modrinth release data)
	•	Model Context Protocol usage with Minecraft RCON ￼ ￼ (MCP server example by Kyle Kelley)
	•	Enabling and using RCON for Minecraft ￼ ￼ (Minecraft MCP Server by Peterson047)
	•	Claude Code integration for MCP ￼ (Claude documentation for adding custom MCP servers)


https://github.com/rgbkrk/rcon-mcp
