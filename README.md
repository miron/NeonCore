# NeonCore

![image](https://user-images.githubusercontent.com/109377/211684849-7c9ffe0a-898c-4f84-bb96-642e179b29b2.jpeg)

Welcome to NeonCore - A Text-Based Cyberpunk RPG

Dive into the neon-soaked streets of Night City in this immersive text-based role-playing game. As a cyberpunk operative, navigate through a world of corporate intrigue, street-level conflicts, and high-tech warfare.

Features:
- Choose your role: Become a street-smart Netrunner, a combat-ready Solo, or other unique characters
- Deep character customization with detailed lifepaths and backgrounds
- Dynamic skill-based gameplay system
- Text-based exploration of Night City's various districts
- Engaging NPC interactions and encounters
- Command-line interface with cyberpunk aesthetic

Built with Python, NeonCore delivers a classic RPG experience inspired by the Cyberpunk 2020 tabletop game system. Use your skills, cyber-enhancements, and street smarts to survive and thrive in the dark future of 2045.

### Installation & Usage

#### Windows (PowerShell)
1. Create fresh virtual environment:
```powershell
python -m venv venv
```

2. Allow PowerShell script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Activate virtual environment:
```powershell
./venv/bin/Activate.ps1
```

4. Upgrade pip:
```powershell
python -m pip install --upgrade pip
```

5. Install OpenAI using pre-built wheels only:
```powershell
python -m pip install openai --no-build-isolation --only-binary :all:
```

6. Run the game:
```powershell
python run_game.py
```

#### Standard Installation (Linux/MacOS)
1. Clone the repository to your local machine
2. Install using pip:
   ```bash
   pip install -e .
   ```
3. Run the game:
   ```bash
   python run_game.py
   ```

### AI Chat Features

NeonCore includes an AI chat system that lets you interact with NPCs. The system supports two backends:

#### Using Grok API
Set up your environment variables:
```bash
# Windows PowerShell
$env:XAI_API_KEY="your-api-key-here"

# Linux/MacOS
export XAI_API_KEY="your-api-key-here"
```

#### Using Ollama
1. Install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Download the smollm2 model (271MB):
```bash
ollama pull smollm2:135m
```

3. Set Ollama host (default is http://localhost:11434):
```bash
# Windows PowerShell
$env:OLLAMA_HOST="http://localhost:11434"

# Linux/MacOS
export OLLAMA_HOST="http://localhost:11434"
```

### In-Game Chat

Use the `talk` command to chat with NPCs. For example:

```
ᐸ/> talk Hey Judy, what's the word on the street about the latest cyberware?
Judy: Hey there, V! Word on the street is there's some nova chrome hittin'
the black market. Heard about this new neural booster that's supposed to
jack your processing speed through the roof. But watch yourself - corps
are crackin' down hard on unauthorized tech these days.
```

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
   - Hierarchical location system
   - Dynamic environment with time-based events
   - Weather and environmental effects
   - Object interaction framework

4. **Character System**
   - More detailed character stats and progression
   - Skills system with advancement
   - Character customization
   - Inventory management

5. **NPC System**
   - Advanced NPC AI using ML models
   - Conversation and relationship tracking
   - NPC schedules and routines
   - Faction system with reputation

6. **Combat System**
   - Turn-based combat mechanics
   - Weapon and armor simulation
   - Status effects and conditions
   - Tactical options

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
