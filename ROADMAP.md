# NeonCore Project Roadmap

## Immediate Fixes (Regressions)
- [x] **Choking Regression**: `choke lenard` confirms damage, but `look` shows full HP. (Fixed via `look` dynamic update)
- [x] **Grappling UX**: Visual feedback in prompt when grappling; ensuring grappled target moves with player.
- [x] **Reflect Crashes**: Investigate `test_soul_integration.py` failures/timeouts. (Added robust Error Handling)

## Phase 1: The Hook (Current Focus)
- [ ] **Scene Implementation**:
    - [/] Script "The Phone Call" (Trigger: `ActionManager` - [x] Intro Hook Implemented).
    - [ ] Script "Heywood Industrial" (Full mission: Ambush, Key Fumble, Signal).
        - *Reference*: `reference/full_mission.txt`
- [ ] **Skill Checks**:
    - [ ] Implement `Human Perception` (DV 17) check for Lazlo's call.
    - [ ] Implement `Forgery` (DV 17) check for the counterfeit money.
- [ ] **NPCs**:
    - [ ] Create `Lazlo` (Fixer).
    - [ ] Create `Lenard Houston` (Dirty Cop).
    - [ ] Create generic `Dirty Cop` enemies (Ambush).

## Phase 2: Combat System Refinement
- [ ] **Core Mechanics**:
    - [ ] **Initiative System**:
        - [ ] Roll `REF` + `1d10` + `Combat Awareness` (Solo).
        - [ ] Tie-breaking: Roll again.
        - [ ] Cyclic Queue: Descending order, loops every round.
    - [ ] Ranged Combat (Distances, DV table).
    - [ ] Cover & Line of Sight.
- [ ] **Damage**:
    - [ ] Ablation of SP (Armor).
    - [ ] Critical Injuries table.

## Phase 3: Advanced Roles (Future)
- [ ] **Netrunner**:
    - [ ] **Interface Menu**: Dedicated UI mode for `Interface` skill users.
    - [ ] **Actions**: `Locate Remote`, `Run Software`, `Control Remote`, `Link LDL`, `Load/Create/Delete`.
    - [ ] **Actions**: `Locate Remote`, `Run Software`, `Control Remote`, `Link LDL`, `Load/Create/Delete`.
    - [ ] **Architecture**:
        - [ ] Cyberdeck state vs World state.
        - [ ] **Procedural Generation**: Use DFS/Maze algorithms for random Net Architectures.
- [ ] **Nomad**: Implement `Moto` (Vehicle handling).
- [ ] **Fixer**: Implement `Operator` (Trading/Sourcing).

## Technical Debt / Cleanup
- [ ] **Inventory System**: Refactor `inventory` list into a managed class with weight/capacity.
- [ ] **Testing**: Increase coverage for `ActionManager` and Combat scenarios.
- [ ] **Data Structures**:
    - [ ] **Lifepath**: Extract tables from `Character.py` to `lifepath.json` (Simplify Dicts to Lists).
        - [ ] **Language Selection**: Interactive prompt to choose Native Language (+4 Skill) after rolling Region.

## Phase 4: Core Systems Expansion
- [ ] **Command System**:
    - [ ] **Aliases & Simplification**:
        - [ ] Map `skill` -> `use_skill` (Remove snake_case requirement).
        - [ ] Map `use` -> `use_object`.
        - [ ] `note` -> `add_note` / `read_notes` (Persistent Player Journal).
    - [ ] Advanced parser with macro support.
    - [ ] Comprehensive help system.
        - [ ] **Context-Aware Help Listing**: Uncomment existing `do_help` logic to display available commands immediately (fixes "Tab to see commands" issue).
- [ ] **Game State**:
    - [ ] Persistence (Save/Load functionality).
    - [x] Database integration (SQLite).
    - [ ] Nostr Integration (Future).
- [ ] **World Model**:
    - [ ] Time-based events and dynamic environment.
    - [ ] Weather effects.
    - [ ] **Contextual Interactions**:
        - [ ] Overload `take` for abstract items (`take job`).
        - [ ] Overload `use` for terminals/boards (`use terminal`).
- [ ] **NPC System**:
    - [ ] ML-driven AI for advanced interactions.
    - [ ] **Experimental**: Simulated Annealing for dynamic NPC stats (Currently stub).
    - [ ] Schedules, routines, and faction reputation.
    - [ ] **Placement Strategy** (Client-Server/Multiplayer Prep):
        - [ ] **Background Simulation**: NPCs move/act even when no players are nearby (Solves "Empty World" problem).
        - [ ] **Predetermined Placement**: Fixed locations for specific NPCs/story.
        - [ ] **Dynamic Placement**: Hybrid approach based on player progress/decisions.
        - [ ] Implement `spawn_npcs()`: Handler for new areas/time-based spawns.
- [ ] **Architecture (Future-Proofing)**:
    - [ ] **Networking**:
        - [ ] **WebSockets**: Real-time bidirectional communication (Server <-> Client).
        - [ ] **Nostr Integration**:
            - [ ] Use `nostr-sdk` (Rust bindings) for performance and Windows support.
            - [ ] **Currency**: Implement **Cashu (Ecash)** Mint integration (No channels, token-based) for Sats <-> Eddies.
            - [ ] **Identity**: `npub` login and Badge definitions for Character Permadeath/Status.
    - [ ] **State Synchronization**: Server propagates `WorldState` updates to connected Clients.
    - [ ] **Decoupling**: Refactor `wprint` to emit structured JSON events (Game Loop -> API -> UI).
    - [ ] **Frontend Agnostic**: Server handles state; Client handles presentation (Text, Web, FMV).
        - [ ] **Web Client**: Support custom fonts (e.g., Cyberpunk-themed, Silhouettes) and CRT effects.
    - [ ] **Server-Side Persistence**: Replace transient per-connection state with a persistent Database/State Manager (Redis/SQL).
        - *Note: Avoid Singleton pattern; use Dependency Injection.*
    - [ ] **Story Engine**:
        - [ ] **StoryManager**: Implement to manage active quest states (Decouple from `ActionManager`).
        - [ ] **Refactor**: Move hardcoded mission logic (`briefcase` checks, `do_deposit`) from `ActionManager` into `StoryModules`.
    - [ ] **Dynamic Command Handling**: Investigate State Pattern or Dynamic Registration to clean up `ActionManager`.
    - [ ] **Dynamic Economy (Cyber-Finance)**:
        - [ ] **Stock/Crypto Simulation**: Background market updates (Real-world API or simulated).
            - *Resource*: `streetyoga/atapi` (`cmp/algo.py` for risk models, `api.py` for client base).
        - [ ] **Interactive Terminals**: "Risk/Reward Analysis" course framed as Corporate Training/Netrunner Tutorials.
        - [ ] **Urbit-style Sovereign Identity**: Crypto-wallets as player identity/bank.
    - [ ] **Code Architecture**:
        - [ ] **Decorators for Composition**: Use `functools` to compose behaviors (e.g., `@requires_state`, `@log_action`) instead of monolithic method logic.
        - [ ] **Policy/Mechanism Separation**: Abstract *policies* (rules) from *mechanisms* (actions) to support dynamic rule changes (e.g., House Rules, different game modes).
        - [ ] **Templates for String Replacement**: Use `string.Template` for user-facing text (prompts, dialogue) to allow for safe, externalizable configuration (e.g., config files for "Slang Packs") without code modification.
        - [ ] **Nested Command Loops (Sub-shells)**: Replace `game_state` flags and proxy methods with true **Nested `cmdloop()` calls**.
            - *Benefit*: Clean isolation of commands. When in `GrappleShell`, the `ActionManager` is paused on the stack, and only `Grapple` commands are valid. No `delattr` hacks needed.

## Phase 5: Multiplayer & Networking
- [ ] **Networking**:
    - [ ] Multi-user support.
    - [ ] Real-time communication/chat.


## Backlog: Game Mechanics
- [ ] **Skill Rules**:
    - [ ] "Trying Again" Logic:
        - [ ] Only allow if: Time taken increased (4x), Better Tool used, or Complementary Skill bonus applied.
    - [ ] **Movement Modes**:
        - [ ] Swim/Climb/Jump: Require `Athletics` check.
        - [ ] Consumes Move Action (Rate: HALF Move Stat).
    - [ ] "Complementary Skills": +1 bonus implementation.
    - [ ] "Taking Extra Time": +1 bonus for 4x time.
    - [ ] "Lucky Pool": Timer to refill every real-world hour.
    - [ ] **Role Mechanics**:
        - [ ] **Surgery**: Restrict checks to Medtechs only.
        - [ ] **Charismatic Impact**: Apply +2 to all EMP/COOL checks when target is a `Fan` (Attack or Defense).
- [ ] **Combat**:
    - [ ] 3-second round timer (simulation).
    - [ ] **Range & Movement** (Abstracted):
        - [ ] **Universal Range Model**: NPCs *and* Objects exist at Bands relative to Player.
            - [ ] *Implementation*: Runtime dictionary `player.distances = {target_id: band}`. Default is 'Far'. No DB changes needed.
            - [ ] **Interception**: Enemies can "Guard" objects. Moving to guarded object triggers Combat/Stop.
        - [ ] **Micro-Movement** (Combat): Actions change Band relative to target (Move = Close Gap).
            - [ ] **Economy**: `Attack` command strictly checks `MOVE` stat.
            - [ ] *Reachable* (Dist <= MOVE*2): Auto-move & Attack (1 Turn).
            - [ ] *Unreachable*: Sprint to close gap only (No Attack).
        - [ ] **Macro-Movement** (World): `go <dir>` changes Rooms (Flee check if in Combat).

## Backlog: Items & Cyberware
- [ ] **Cyberware mechanics**:
    - [ ] *Teleoptic Cybereye*:
        - [ ] *Scope*: Negates Range penalties for visual Perception checks.
        - [ ] *Scout*: Allows `look <dir>` to view adjacent Room description without moving.
    - [ ] *Tool Hand* (Tech bonus integration).
    - [ ] *Pain Editor* (Ignores -2 from Seriously Wounded State).
- [ ] **Gear**:
    - [ ] **Internal Agent** (Smart Phone/AI):
        - [ ] `call/text`: Communication.
        - [ ] `map/gps`: Local area info (Data Pool).
        - [ ] `query`: Library Search / News.
        - [ ] *Constraint*: Cannot Hack (requires Cyberdeck) or Teleport items.
    - [ ] **Glow Paint**:
        - [ ] *Spray Object/Wall*: Narrative marker (visible in `look`).
        - [ ] *Spray Enemy*: Negates Darkness penalties against them.
        - [ ] *Spray Eyes* (Called Shot -4): Causes Blindness/Distraction.
    - [ ] **Video Camera**:
        - [ ] *Record*: Captures event log to a timestamped file/"tape".
        - [ ] *Evidence*: Tapes work as Quest Items (Blackmail/Bounties) or Media Content (Credibility bonus).
    - [ ] **Musical Instruments** (Rockerboy focus):
        - [ ] *Mechanics*: `perform` (Busking/Crowd Impact), `play` (Combat Distraction/Intimidation).
        - [ ] *Varieties*: Holographic Harp, Neutron Synth, Plasma Violin (Flavor + unique sound profiles).
        - [ ] *Pocket Amp*: Boosts Range/Effect. `amplify` command for Voice (Intimidation) or Music (Area interaction).
        - [ ] *Audio Implementation*: Basic sound support via `winsound` or `playsound` (Beeps -> WAVs).
    - [ ] **Burner Phone**:
        - [ ] *Anonymity*: Masked Identity in calls/texts.
        - [ ] *Disposable*: `burn` command to destroy phone & wipe logs (Anti-Tracking).
        - [ ] *Decoy*: Leave active to mislead NPC trackers.

## Backlog: ID & Narrative
- [ ] **Narrative**:
    - [ ] Influence of Lifepath on Story (e.g., region determines heist location).
    - [ ] **Dynamic Slang Injection**:
        - [ ] Create `SlangProfile` enum/class (Corp-Speak, Net-Speak, Street-Slang, Euro-Lingo).
        - [ ] Update AI Prompt in `StoryManager` to inject specific dialect instructions based on NPC Profile.
- [ ] **UI/UX**:
    - [ ] **Visuals**:
        - [ ] Animated ASCII dice for rolls (Combat & Lifepath generation).
        - [ ] Show individual Lifepath roll results to player during creation.
    - [ ] **Tab Completion**:
        - [ ] Restrict `use_skill` autocomplete to only skills the character possesses (Clean UI).
        - [ ] **Unskilled Checks**: Allow manual execution of missing General Skills (use `STAT + 0`).
            - [ ] *UX*: Display warning "[UNSKILLED] Relying on REF Stat only!" when attempted.
        - [ ] **Role Validation**: Block missing Exclusive Skills (e.g. `Surgery`) completely.

