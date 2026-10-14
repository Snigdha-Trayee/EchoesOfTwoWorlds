
import sys
import pygame

from puzzle_logic import (
    PUZZLES,
    check_answer,
    get_hint,
    get_puzzle
)

pygame.init()

WIDTH = 1000
HEIGHT = 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echoes of Two Worlds - Puzzle Trials")
CLOCK = pygame.time.Clock()

BG = (18, 22, 42)
PANEL = (31, 38, 66)
BUTTON = (48, 61, 96)
WHITE = (240, 243, 255)
MUTED = (174, 185, 213)
GOLD = (245, 196, 92)
CYAN = (105, 220, 225)
GREEN = (100, 220, 153)
RED = (246, 110, 120)
PURPLE = (174, 135, 245)

FONT = pygame.font.SysFont("arial", 22)
SMALL = pygame.font.SysFont("arial", 17)
MEDIUM = pygame.font.SysFont("arial", 27, bold=True)
LARGE = pygame.font.SysFont("arial", 38, bold=True)

PUZZLE_IDS = [p["id"] for p in PUZZLES]

index = 0
score = 0
attempts = 0
hints_used = 0
solved = set()
feedback = ""
feedback_color = WHITE
hint_text = ""
input_text = ""
selected_runes = []
direction_index = 0
screen_state = "intro"


def draw_text(text, x, y, font=FONT, color=WHITE, center=False):
    image = font.render(str(text), True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    SCREEN.blit(image, rect)
    return rect


def wrap_text(text, x, y, width, font=FONT, color=WHITE):
    words = str(text).split()
    line = ""

    for word in words:
        test = word if not line else line + " " + word

        if font.size(test)[0] <= width:
            line = test
        else:
            draw_text(line, x, y, font, color)
            y += font.get_linesize() + 5
            line = word

    if line:
        draw_text(line, x, y, font, color)
        y += font.get_linesize() + 5

    return y


def draw_button(rect, label, color=BUTTON, text_color=WHITE,
                font=FONT):
    pygame.draw.rect(SCREEN, color, rect, border_radius=12)
    pygame.draw.rect(SCREEN, CYAN, rect, 2, border_radius=12)
    draw_text(label, rect.centerx, rect.centery,
              font, text_color, True)


def current_puzzle():
    return get_puzzle(PUZZLE_IDS[index])


def reset_puzzle():
    global feedback, hint_text, input_text
    global selected_runes, direction_index

    feedback = ""
    hint_text = ""
    input_text = ""
    selected_runes = []
    direction_index = 0


def submit_answer(answer):
    global score, attempts, feedback, feedback_color

    puzzle = current_puzzle()
    attempts += 1

    if check_answer(puzzle["id"], answer):
        if puzzle["id"] not in solved:
            score += 100 if not hint_text else 75
            solved.add(puzzle["id"])

        feedback = puzzle["success"]
        feedback_color = GREEN
    else:
        feedback = "Incorrect answer. Try again!"
        feedback_color = RED


def show_hint():
    global hint_text, hints_used

    puzzle = current_puzzle()

    if not hint_text:
        hint_text = get_hint(puzzle["id"]) or "No hint available."
        hints_used += 1


def next_puzzle():
    global index, screen_state

    if index < len(PUZZLE_IDS) - 1:
        index += 1
        reset_puzzle()
    else:
        screen_state = "results"


def draw_intro():
    SCREEN.fill(BG)

    draw_text("ECHOES OF TWO WORLDS", 500, 180,
              LARGE, GOLD, True)
    draw_text("THE SEVEN PUZZLE TRIALS", 500, 240,
              MEDIUM, CYAN, True)

    wrap_text(
        "Solve seven puzzles across the Living Realm "
        "and the Forgotten Realm. Use clues, reveal hints, "
        "and unlock the Final Rune Seal.",
        180, 310, 640, FONT, WHITE
    )

    draw_text("Mouse: Select    H: Hint    ESC: Quit",
              500, 410, SMALL, MUTED, True)

    start = pygame.Rect(350, 480, 300, 65)
    draw_button(start, "Begin the Trials", PANEL, GOLD, MEDIUM)

    return start


def draw_header(puzzle):
    pygame.draw.rect(SCREEN, PANEL,
                     (25, 20, 950, 110), border_radius=16)

    draw_text("ECHOES OF TWO WORLDS", 48, 35,
              MEDIUM, GOLD)

    draw_text(
        f"Puzzle {index + 1} of {len(PUZZLE_IDS)}",
        48, 78, SMALL, MUTED
    )

    draw_text(puzzle["realm"], 690, 38, FONT, CYAN)

    draw_text(
        f"Score: {score}    Solved: {len(solved)}/7",
        590, 80, SMALL, WHITE
    )

    pygame.draw.rect(SCREEN, BUTTON,
                     (48, 145, 904, 8), border_radius=4)

    progress_width = int(904 * (index + 1) / len(PUZZLE_IDS))
    pygame.draw.rect(SCREEN, GOLD,
                     (48, 145, progress_width, 8),
                     border_radius=4)

    draw_text(puzzle["clue"], 48, 165, MEDIUM, PURPLE)


def draw_choices(puzzle, y=355):
    rects = []

    for i, option in enumerate(puzzle["options"]):
        rect = pygame.Rect(120, y + i * 65, 760, 52)
        draw_button(rect, f"{i + 1}.  {option}")
        rects.append((rect, option))

    return rects


def draw_puzzle():
    SCREEN.fill(BG)

    puzzle = current_puzzle()
    draw_header(puzzle)

    wrap_text(puzzle["question"], 65, 220, 870, FONT, WHITE)

    mechanic = puzzle["type"]
    rects = []
    extra = {}

    if mechanic == "cipher":
        draw_text("ANCIENT CIPHER", 500, 310,
                  MEDIUM, GOLD, True)

        draw_text("A=1, B=2, C=3 ... Z=26",
                  500, 350, FONT, MUTED, True)

        rect = pygame.Rect(250, 405, 500, 58)
        pygame.draw.rect(SCREEN, PANEL, rect, border_radius=10)
        pygame.draw.rect(SCREEN, GOLD, rect, 2, border_radius=10)

        shown_text = input_text or "Type your answer"
        shown_color = WHITE if input_text else MUTED

        draw_text(shown_text, rect.centerx, rect.centery,
                  FONT, shown_color, True)

        draw_text("Type the decoded word and press ENTER.",
                  500, 480, SMALL, MUTED, True)

        extra["input"] = rect

    elif mechanic == "rotation_logic":
        directions = ["NORTH", "EAST", "SOUTH", "WEST"]
        direction = directions[direction_index]

        draw_text("CONSTELLATION COMPASS", 500, 310,
                  MEDIUM, GOLD, True)

        pygame.draw.circle(SCREEN, PANEL, (500, 420), 65)
        pygame.draw.circle(SCREEN, GOLD, (500, 420), 65, 3)
        draw_text(direction, 500, 420, MEDIUM, CYAN, True)

        left = pygame.Rect(230, 520, 170, 52)
        right = pygame.Rect(415, 520, 170, 52)
        check = pygame.Rect(600, 520, 170, 52)

        draw_button(left, "Rotate Left")
        draw_button(right, "Rotate Right")
        draw_button(check, "Check Direction", PANEL, GOLD, SMALL)

        extra.update(left=left, right=right, check=check)

    elif mechanic == "rune_order":
        draw_text("FINAL RUNE SEAL", 500, 300,
                  MEDIUM, GOLD, True)

        draw_text("Select the runes in the correct order.",
                  500, 335, SMALL, MUTED, True)

        for i, rune in enumerate(["LEAF", "STAR", "MOON"]):
            rect = pygame.Rect(115 + i * 275, 390, 220, 75)
            color = GREEN if rune in selected_runes else BUTTON
            draw_button(rect, rune, color, WHITE, MEDIUM)
            rects.append((rect, rune))

        shown_order = " - ".join(selected_runes) or "No runes selected"
        draw_text("Your order: " + shown_order,
                  500, 485, SMALL, CYAN, True)

        check = pygame.Rect(340, 530, 160, 50)
        clear = pygame.Rect(520, 530, 140, 50)

        draw_button(check, "Check Order", PANEL, GOLD, SMALL)
        draw_button(clear, "Clear", PANEL, WHITE, SMALL)

        extra.update(check=check, clear=clear)

    else:
        if mechanic == "pattern":
            draw_text("COMPLETE THE PATTERN",
                      500, 300, MEDIUM, GOLD, True)
        elif mechanic == "sequence":
            draw_text("MEMORY CHALLENGE",
                      500, 300, MEDIUM, GOLD, True)
        elif mechanic == "symbol_riddle":
            draw_text("DECODE THE SYMBOL",
                      500, 300, MEDIUM, GOLD, True)
        else:
            draw_text("SOLVE THE RIDDLE",
                      500, 300, MEDIUM, GOLD, True)

        rects = draw_choices(puzzle, 355)

    hint_button = pygame.Rect(65, 570, 140, 45)
    draw_button(hint_button, "Show Hint", PANEL, GOLD, SMALL)

    if hint_text:
        wrap_text("Hint: " + hint_text, 230, 580, 700,
                  SMALL, GOLD)

    if feedback:
        wrap_text(feedback, 65, 630, 650,
                  SMALL, feedback_color)

    next_button = None

    if puzzle["id"] in solved:
        next_button = pygame.Rect(760, 615, 175, 48)
        label = "Finish" if index == len(PUZZLE_IDS) - 1 else "Next Puzzle"
        draw_button(next_button, label, PANEL, GREEN, SMALL)

    draw_text("H: Hint    ESC: Quit", 65, 675, SMALL, MUTED)

    extra.update(
        puzzle=puzzle,
        rects=rects,
        hint=hint_button,
        next=next_button
    )

    return extra


def handle_click(pos, ui):
    global direction_index, feedback, feedback_color

    puzzle = ui["puzzle"]
    mechanic = puzzle["type"]

    if ui["hint"].collidepoint(pos):
        show_hint()
        return

    if ui["next"] and ui["next"].collidepoint(pos):
        if puzzle["id"] in solved:
            next_puzzle()
        return

    if mechanic == "cipher":
        return

    if mechanic == "rotation_logic":
        if ui["left"].collidepoint(pos):
            direction_index = (direction_index - 1) % 4
        elif ui["right"].collidepoint(pos):
            direction_index = (direction_index + 1) % 4
        elif ui["check"].collidepoint(pos):
            direction = ["NORTH", "EAST", "SOUTH", "WEST"][direction_index]
            submit_answer(direction)
        return

    if mechanic == "rune_order":
        for rect, rune in ui["rects"]:
            if rect.collidepoint(pos):
                if rune in selected_runes:
                    selected_runes.remove(rune)
                elif len(selected_runes) < 3:
                    selected_runes.append(rune)
                return

        if ui["clear"].collidepoint(pos):
            selected_runes.clear()
            return

        if ui["check"].collidepoint(pos):
            if len(selected_runes) != 3:
                feedback = "Select all three runes first."
                feedback_color = RED
            else:
                submit_answer(" - ".join(selected_runes))
        return

    for rect, option in ui["rects"]:
        if rect.collidepoint(pos):
            submit_answer(option)
            return


def draw_results():
    SCREEN.fill(BG)

    draw_text("TRIALS COMPLETE", 500, 135,
              LARGE, GOLD, True)

    draw_text("Both realms' memories are united!",
              500, 205, MEDIUM, CYAN, True)

    percentage = round(len(solved) / len(PUZZLE_IDS) * 100)

    draw_text(f"Puzzles solved: {len(solved)} / 7",
              500, 285, MEDIUM, WHITE, True)

    draw_text(f"Completion: {percentage}%",
              500, 330, MEDIUM, GREEN, True)

    draw_text(f"Final score: {score}",
              500, 375, MEDIUM, GOLD, True)

    draw_text(f"Answer attempts: {attempts}",
              500, 420, FONT, MUTED, True)

    draw_text(f"Hints used: {hints_used}",
              500, 455, FONT, MUTED, True)

    restart = pygame.Rect(350, 520, 300, 60)
    draw_button(restart, "Play Again", PANEL, GOLD, MEDIUM)

    return restart


def restart_game():
    global index, score, attempts, hints_used
    global solved, screen_state

    index = 0
    score = 0
    attempts = 0
    hints_used = 0
    solved = set()
    reset_puzzle()
    screen_state = "intro"


def main():
    global screen_state, input_text

    running = True

    while running:
        CLOCK.tick(60)

        if screen_state == "intro":
            start_button = draw_intro()
            ui = {}
            results_button = None

        elif screen_state == "puzzle":
            ui = draw_puzzle()
            start_button = None
            results_button = None

        else:
            results_button = draw_results()
            start_button = None
            ui = {}

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif screen_state == "puzzle":
                    if event.key == pygame.K_h:
                        show_hint()

                    elif current_puzzle()["type"] == "cipher":
                        if event.key == pygame.K_RETURN:
                            submit_answer(input_text.strip().upper())
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        elif event.unicode.isalpha() and len(input_text) < 20:
                            input_text += event.unicode.upper()

                elif screen_state == "results" and event.key == pygame.K_r:
                    restart_game()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if screen_state == "intro":
                    if start_button.collidepoint(event.pos):
                        screen_state = "puzzle"
                        reset_puzzle()

                elif screen_state == "puzzle":
                    handle_click(event.pos, ui)

                elif screen_state == "results":
                    if results_button.collidepoint(event.pos):
                        restart_game()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
