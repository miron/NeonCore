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