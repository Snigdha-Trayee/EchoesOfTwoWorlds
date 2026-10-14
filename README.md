# Echoes of Two Worlds

A Python/Pygame exploration and puzzle game featuring two connected realms, collectible memories, a Shadow Guardian, a rune puzzle, and audio/visual assets.

## Run the game

Install Pygame if needed:

```powershell
py -3.13 -m pip install pygame
```

Start the game from this folder:

```powershell
py -3.13 main.py
```

## Controls

- WASD or arrow keys: move
- E: interact, collect memories, use mechanism/portal
- Space: attack the Shadow Guardian
- 1, 2, 3: choose runes in the puzzle
- Enter: submit puzzle
- Backspace: clear puzzle selection
- R: restart after victory or game over
- Esc: close puzzle or quit

## Project layout

- `main.py`: Pygame gameplay
- `audio_manager.py`: music and sound effects
- `assets/backgrounds/`, `assets/player/`, `assets/world/`: visual assets
- `assets/audio/`: music and sound effects with included credits
- `game/`: Trayee's discovery, objectives, cinematic event, and progression logic
- `level_design/`: design document and proposed maps
- `tests/`: tests for the progression system

## Tests

```powershell
py -3.13 -m unittest discover -s tests -v
```

Read `INTEGRATION_NOTES.txt` for known differences between the proposed map sequence and current playable flow.


## Harini login, clues and rune quizzes
Run `py -3.13 login_screen.py` to open the new Pygame title/login/welcome flow and Harini rune clue quizzes. It contains the three rune challenges and all nine quiz questions ported from her React `App.jsx`, with images copied into `assets/harini/`. After restoring all rune challenges, choose Start Pygame Adventure to launch the existing `main.py`. The existing game files are preserved.
