# LEVEL 2: THE OBSERVATORY
Version: 1.0
Map type: Proposed top-down grid
Grid: 10 columns (A-J) x 8 rows (1-8)
Coordinate format: Column, Row

## Annotated Map
Legend:
P = Portal arrival
E = Observatory entrance
L = Star Map Hall landmark
C = Observatory clue
Q = Celestial puzzle chamber
F = Final discovery point
. = Walkable area
# = Boundary / blocked area

    A B C D E F G H I J
 1  # # # # # # # # # #
 2  # P . . . . . . . #
 3  # . . E . . . . . #
 4  # . . . L . C . . #
 5  # . . . . . . . . #
 6  # . . . Q . . . . #
 7  # . . . . . . F . #
 8  # # # # # # # # # #

## Player Route
P(B2) -> E(D3) -> L(E4) -> C(G4) -> Q(E6) -> F(H7)

## Exact Proposed Landmark and Clue Positions
- Portal arrival: B2
- Observatory entrance: D3
- Star Map Hall: E4
- Observatory clue: G4
- Celestial puzzle chamber: E6
- Final discovery point: H7

## Discovery Order
1. Arrive through the portal at B2.
2. Explore the Observatory entrance at D3.
3. Investigate the Star Map Hall at E4.
4. Discover the Observatory clue at G4.
5. Reach and complete the celestial puzzle at E6.
6. Reach the final discovery point at H7.

## Level Objectives
- Enter the Observatory.
- Explore the entrance and Star Map Hall.
- Discover the Observatory clue.
- Investigate or solve the celestial puzzle.
- Reach the final discovery point.

## Proposed Completion Condition
The level is complete when the player reaches the final discovery point after investigating the required landmarks and completing the puzzle.

## Integration Notes
Coordinates are proposed design-grid positions, not verified Unity world coordinates. Puzzle rules, scene dimensions, collision, and completion triggers must be confirmed during Unity integration.
