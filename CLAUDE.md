# NeonCore Project Guidelines

## Build Commands
- Install: `pip install -e .`
- Run game: `python run_game.py`
- Run all tests: `python -m unittest discover tests`
- Run single test: `python -m unittest tests.test_command_manager`
- Format code: `black NeonCore/`

## Code Style
- Use type hints (Protocol for interfaces)
- Follow PEP 8 conventions and use Black formatter
- Use snake_case for variables, functions, methods
- Use CamelCase for classes
- Use abstract classes (ABC) for interfaces when appropriate
- Organize imports: standard lib, third-party, local with alphabetical sorting
- Document functions with docstrings
- Log errors using Python's logging module (configured in core/dependencies.py)
- Use dataclasses for data containers
- Follow dependency injection pattern through constructors

## Project Structure
- Core game logic in managers/
- Keep modules small and focused on single responsibility
- Separate interface from implementation
- Use Protocol for interface definitions

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