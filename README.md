# NeonCore

![image](https://user-images.githubusercontent.com/109377/211684849-7c9ffe0a-898c-4f84-bb96-642e179b29b2.jpeg)

Welcome to NeonCore - A Text-Based Cyberpunk RPG

Dive into the neon-soaked streets of Night City in this immersive text-based role-playing game. As a cyberpunk operative, navigate through a world of corporate intrigue, street-level conflicts, and high-tech warfare.

Features:
- Choose your role: Become a street-smart Netrunner, a combat-ready Solo, or other unique characters
- Deep character customization with detailed lifepaths and backgrounds
- Dynamic skill-based gameplay system
- Text-based exploration of Night City's various districts
- Engaging NPC interactions and encounters (Combat & Social)
- Command-line interface with cyberpunk aesthetic
- Detailed Life Path system including cultural regions, personality, and background

Built with Python, NeonCore delivers a classic RPG experience inspired by the Cyberpunk 2020 tabletop game system. Use your skills, cyber-enhancements, and street smarts to survive and thrive in the dark future of 2045.

### Installation & Usage

#### Windows (PowerShell)
1. **Setup Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\python.exe -m pip install --upgrade pip
   .\venv\Scripts\python.exe -m pip install -e .
   ```

2. **Run NeonCore**:
   **Client-Server Mode (Default)**:
   ```powershell
   .\play.ps1
   ```
   *Starts the Game Server in the background and launches the Client.*

   **Standalone Mode**:
   ```powershell
   .\play.ps1 -Local
   ```
   *Runs the game as a single monolithic process (useful for development/debugging).*

   > **Note:** `play.ps1` automatically uses the virtual environment's Python, bypassing the need for manual activation scripts and avoiding common PowerShell permission errors.

#### Linux/MacOS
1. Setup:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```
2. Run:
   ```bash
   python run_game.py
   ```

### AI & Architecture

#### Architecture
NeonCore utilizes a **Client-Server** architecture by default.
- **Server**: Handles game state, world simulation, and AI requests (`server.py`).
- **Client**: Handles UI and user input (`client.py`).
- **Database (Concept)**: A decentralized **Nostr** relay system is planned for persistent world state and player communications, but is currently in conceptual phase.

#### AI Backend
The game requires an LLM to power the "Digital Soul" and NPC interactions.

1. **Ollama (Recommended - Local)**
   - Install [Ollama](https://ollama.com/) and pull the verified model:
     ```bash
     ollama pull qwen3:32b
     ```
   - *Note: Code includes specific JSON sanitization fixes for Qwen's creative output.*
   - Configurable in `NeonCore/config.py`.

2. **Gemini (Alternative - Cloud)**
   - Get API Key from Google AI Studio.
   - Set env var: `GEMINI_API_KEY="your-key"`
   - Change `default_backend` to `gemini` in `config.py`.

3. **Remote Inference (Optional)**
   If running Ollama on a separate powerful machine (e.g., a desktop with an RTX 4090), follow these steps:

   **Host Machine (where Ollama runs):**
   - **Bind Address:** Ensure Ollama listens on all interfaces.
     - *Linux:* `OLLAMA_HOST="0.0.0.0" ollama serve`
     - *Windows:* Set env var `OLLAMA_HOST` to `0.0.0.0` before starting.
   - **Firewall:** Allow inbound traffic on port `11434` (TCP).
     - *Fedora/RHEL:* `sudo firewall-cmd --add-port=11434/tcp --permanent && sudo firewall-cmd --reload`
     - *Windows:* Add an Inbound Rule in "Windows Defender Firewall".

   **Client Machine (where NeonCore runs):**
   - Edit `.env` to point to the host:
     ```bash
     OLLAMA_HOST="http://192.168.0.x:11434"
     OLLAMA_MODEL="qwen3:32b"  # Or your preferred model
     ```
   
### In-Game Chat
1. **Approach NPC**: Type `talk [NPC Name]` (e.g., `talk Lenard`).
2. **Chat**: Just type natural text.
   ```
   You -> Lenard > Where is the money?
   Lenard: (Sweating) look, I don't have it all...
   ```
3. **Commands**: Type `bye` to exit, or `take [item]` to grab things mid-conversation.

### Developer & Debug Commands
Use these commands to test game systems on the fly without setting up complex scenarios.

- **`dev_fan [npc_name]`**: Forces the specified NPC to become a "Fan" of the player (Relationship Status: Fan).
  - *Usage*: `dev_fan lenard`
  - *Effect*: `look` shows `[ FAN ]` tag. `talk` uses "Charismatic Impact" context.

## Future Development Roadmap

To expand NeonCore into a more substantial text RPG (similar to Sindome), the following components would need to be developed:

1. **Command System**
   - More sophisticated command parser with aliases
   - Command help system with examples
   - Support for compound commands and macros

2. **Game State Management**
   - Proper database for persistent game state
   - Save/load functionality
   - Transaction system for atomic operations

3. **World Model**
   - [x] Hierarchical location system (Implemented)
   - Dynamic environment with time-based events
   - Weather and environmental effects
   - Object interaction framework

4. **Character System**
   - More detailed character stats and progression
   - Skills system with advancement
   - [x] Character customization (Life Path Implemented)
   - Inventory management

5. **NPC System**
   - Advanced NPC AI using ML models
   - Conversation and relationship tracking
   - NPC schedules and routines
   - Faction system with reputation

6. **Combat System**
   - [x] Turn-based combat mechanics (Basic Implementation)
   - [x] Weapon and armor simulation
   - Status effects and conditions
   - Tactical options (Cover implemented)

7. **Quest System**
   - Quest tracking and progression
   - Branching quest paths
   - Dynamic quest generation

8. **User Interface Improvements**
   - Color-coded output
   - Status bar/HUD elements
   - Mini-map visualization
   - Help system

9. **Networking**
   - Multi-user support
   - Chat/communication systems
   - Player interaction mechanics
