
PUZZLES = [
    {
        "id": "garden_riddle",
        "level": 1,
        "realm": "Living Realm",
        "clue": "Garden Mark",
        "type": "riddle",
        "question": "I have roots but never walk. I drink water but have no mouth. What am I?",
        "options": ["A TREE", "A RIVER", "A STONE"],
        "answer": "A TREE",
        "hint": "Think about something that grows in a garden.",
        "success": "The Garden Mark awakens!"
    },
    {
        "id": "forgotten_symbols",
        "level": 1,
        "realm": "Living Realm",
        "clue": "Star Inscription",
        "type": "symbol_riddle",
        "question": "I shine at night and guide lost travellers. Which symbol am I?",
        "options": ["LEAF", "STAR", "STONE"],
        "answer": "STAR",
        "hint": "Look up at the night sky.",
        "success": "The star symbol glows!"
    },
    {
        "id": "guardian_pattern",
        "level": 1,
        "realm": "Living Realm",
        "clue": "Garden Pattern",
        "type": "pattern",
        "question": "Complete the pattern: LEAF, FLOWER, LEAF, FLOWER, ____.",
        "options": ["STAR", "LEAF", "WATER"],
        "answer": "LEAF",
        "hint": "The two symbols alternate.",
        "success": "The garden pattern is restored!"
    },
    {
        "id": "memory_sequence",
        "level": 1,
        "realm": "Living Realm",
        "clue": "Memory Crystal",
        "type": "sequence",
        "question": "MOON, LEAF, STAR. Which symbol appeared second?",
        "options": ["MOON", "LEAF", "STAR"],
        "answer": "LEAF",
        "hint": "Count the symbols from left to right.",
        "success": "The memory crystal restores its light!"
    },
    {
        "id": "symbol_cipher",
        "level": 2,
        "realm": "Forgotten Realm",
        "clue": "Encoded Message",
        "type": "cipher",
        "question": "Decode using A=1, B=2, C=3 ... Z=26: 19 - 20 - 1 - 18.",
        "options": ["STAR", "MOON", "LEAF"],
        "answer": "STAR",
        "hint": "Convert each number into its matching alphabet letter.",
        "success": "The encoded message is decoded!"
    },
    {
        "id": "rotating_constellation",
        "level": 2,
        "realm": "Forgotten Realm",
        "clue": "Constellation Wheel",
        "type": "rotation_logic",
        "question": "A constellation points NORTH. Rotate it 90 degrees clockwise. Which direction does it point?",
        "options": ["EAST", "WEST", "SOUTH"],
        "answer": "EAST",
        "hint": "A clockwise turn from north points toward the right.",
        "success": "The constellation aligns!"
    },
    {
        "id": "guardian_rune_order",
        "level": 2,
        "realm": "Forgotten Realm",
        "clue": "Final Rune Trial",
        "type": "rune_order",
        "question": "The inscription says LEAF comes first, STAR second, and MOON last. Which order is correct?",
        "options": [
            "LEAF - STAR - MOON",
            "MOON - STAR - LEAF",
            "STAR - LEAF - MOON"
        ],
        "answer": "LEAF - STAR - MOON",
        "hint": "Follow the three positions in the inscription.",
        "success": "The Final Seal opens! Both worlds' memories are united!"
    }
]


def get_puzzle(puzzle_id):
    aliases = {
        "final_riddle": "guardian_rune_order"
    }

    puzzle_id = aliases.get(puzzle_id, puzzle_id)

    for puzzle in PUZZLES:
        if puzzle["id"] == puzzle_id:
            return puzzle.copy()

    return None


def get_puzzles_by_level(level):
    return [
        puzzle.copy()
        for puzzle in PUZZLES
        if puzzle["level"] == level
    ]


def get_puzzles_by_realm(realm):
    if not isinstance(realm, str):
        return []

    return [
        puzzle.copy()
        for puzzle in PUZZLES
        if puzzle["realm"].casefold() == realm.casefold()
    ]


def get_hint(puzzle_id):
    puzzle = get_puzzle(puzzle_id)
    return puzzle["hint"] if puzzle else None


def check_answer(puzzle_id, answer):
    puzzle = get_puzzle(puzzle_id)

    if puzzle is None or not isinstance(answer, str):
        return False

    return answer.strip().casefold() == puzzle["answer"].casefold()


def get_total_puzzles():
    return len(PUZZLES)
