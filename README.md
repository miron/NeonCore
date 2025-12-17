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
1. Create fresh virtual environment:
```powershell
python -m venv venv
```

2. Allow PowerShell script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3.### Activation
*   **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
*   **Windows (CMD):** `.\venv\Scripts\activate.bat`
*   **Linux/Mac:** `source venv/bin/activate`

> **Note:** If you encounter an error about scripts being disabled or "not digitally signed", run this in your PowerShell terminal before activating:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```
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
NeonCore requires an AI backend to power NPC interactions and the "Digital Soul" system.

#### Option A: Gemini (Cloud - Recommended)
This is the default and most powerful option.
1. Get an API Key from [Google AI Studio](https://aistudio.google.com/).
2. Set it in your `.env` file or environment:
   ```bash
   GEMINI_API_KEY="your-api-key-here"
   ```

#### Option B: Ollama (Local - Private)
Run the game offline using your own GPU.
1. Install [Ollama](https://ollama.com/).
2. Pull a model (e.g., Mistral or Llama3):
   ```bash
   ollama pull mistral
   ```
3. Update `config.py` or sets environment variables:
   ```bash
   OLLAMA_MODEL="mistral"
   OLLAMA_HOST="http://localhost:11434"
   ```
   
### In-Game Chat
1. **Approach NPC**: Type `talk [NPC Name]` (e.g., `talk Lenard`).
2. **Chat**: Just type natural text.
   ```
   You -> Lenard > Where is the money?
   Lenard: (Sweating) look, I don't have it all...
   ```
3. **Commands**: Type `bye` to exit, or `take [item]` to grab things mid-conversation.

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
