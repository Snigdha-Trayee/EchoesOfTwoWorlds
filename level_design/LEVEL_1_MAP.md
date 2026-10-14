# LEVEL 1: THE FORGOTTEN GARDEN
Version: 1.0
Map type: Proposed top-down grid
Grid: 10 columns (A-J) x 8 rows (1-8)
Coordinate format: Column, Row

## Annotated Map
Legend:
P = Player start
L = Garden landmark
C = Inscription clue
1 = Symbol 1
2 = Symbol 2
3 = Symbol 3
G = Guardian arena
A = Ancient Arch
. = Walkable area
# = Boundary / blocked area

    A B C D E F G H I J
 1  # # # # # # # # # #
 2  # P . . L . . . . #
 3  # . . C . . . . . #
 4  # . 1 . . 2 . . . #
 5  # . . . L . . 3 . #
 6  # . . . . . G . . #
 7  # . . . . . . A . #
 8  # # # # # # # # # #

## Player Route
P(B2) -> L(E2) -> C(D3) -> 1(C4) -> 2(F4) -> 3(H5) -> G(G6) -> A(H7)

## Exact Proposed Discovery Positions
- Player start: B2
- Garden landmark: E2
- Inscription clue: D3
- Symbol 1: C4
- Symbol 2: F4
- Symbol 3: H5
- Guardian arena: G6
- Ancient Arch: H7

## Discovery Order
1. Spawn at B2 and explore the garden.
2. Visit the garden landmark at E2.
3. Discover the inscription clue at D3.
4. Find Symbol 1 at C4.
5. Find Symbol 2 at F4.
6. Find Symbol 3 at H5.
7. Defeat the guardian at G6.
8. Unlock and reach the Ancient Arch at H7.
9. Enter the portal to travel to Level 2.

## Level Objectives
- Explore the garden.
- Discover at least one clue.
- Find all three symbols.
- Defeat the guardian.
- Unlock the Ancient Arch.
- Enter the portal.

## Arch Unlock Conditions
At least one clue discovered, all three symbols discovered, and guardian defeated.

## Integration Notes
Coordinates are proposed design-grid positions, not verified Unity world coordinates. The Unity team must map these cells to the actual scene and confirm collision, accessibility, and encounter placement.
