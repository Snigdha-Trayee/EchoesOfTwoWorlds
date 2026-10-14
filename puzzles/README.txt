ECHOES OF TWO WORLDS - PUZZLE PACK

Files:
- puzzle_pack.py: Standalone Pygame puzzle demonstration.
- puzzle_logic.py: Reusable puzzle questions, answers and hints.
- test_puzzles.py: Automated tests for puzzle logic.

Requirements:
- Python 3.12
- Pygame 2.6.1 for the graphical demonstration.

Run the puzzle game:
py -3.12 puzzle_pack.py

Run the tests:
py -3.12 -m unittest test_puzzles.py -v

Controls:
- Mouse: Select an answer.
- H: Show a hint.
- N: Move to the next puzzle after solving.
- R: Restart after completing all puzzles.
- ESC: Exit.

INTEGRATION NOTE:
This is a separate puzzle pack. It has not been integrated into
the main game. The main game developer can import puzzle_logic.py
and connect its functions to the game's existing interaction system.
