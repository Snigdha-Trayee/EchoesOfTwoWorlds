\# Echoes of Two Worlds



\## Project Overview

Echoes of Two Worlds is a fantasy game concept featuring exploration, discoveries, objectives, and progression through connected story events.



\## My Contribution

I developed the Python game progression and story logic.



\### Main Components

\- `game/objectives.py` — manages the sequence of game objectives.

\- `game/discovery\_manager.py` — tracks discovered clues, symbols, and locations.

\- `game/cinematic\_events.py` — manages one-time cinematic events and event data.

\- `game/game\_director.py` — coordinates exploration, discoveries, the guardian, the Ancient Arch, and portal progression.



\## Level Design

The `level\_design` folder contains:

\- `GAME\_DESIGN\_DOCUMENT.md` — proposed game story, progression, and design.

\- `LEVEL\_1\_MAP.md` — proposed Forgotten Garden map and discovery route.

\- `LEVEL\_2\_MAP.md` — proposed Observatory map and objectives.



\## Testing

Automated tests are located in the `tests` folder.



Run the tests using Python 3.12:



```powershell

py -3.12 -m unittest discover -s tests -v

```



Latest test result: 10 tests passed.



\## Integration Note

The Python progression logic and text-based level maps are a prototype contribution. The team should verify map positions and integrate or reimplement the required logic in Unity before the final game demo.

