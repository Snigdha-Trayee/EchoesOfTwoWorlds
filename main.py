import os
import math
import random
import pygame

from audio_manager import AudioManager
from game.game_director import GameDirector

# ECHOES OF TWO WORLDS - Main Game
# Run with: py -3.13 main.py
pygame.init()
audio = AudioManager()
audio.play_music("living")

WIDTH, HEIGHT = 1280, 720
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echoes of Two Worlds")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 30)
SMALL_FONT = pygame.font.Font(None, 24)
TITLE_FONT = pygame.font.Font(None, 58)
BIG_FONT = pygame.font.Font(None, 38)

WHITE = (245, 245, 255)
GOLD = (255, 205, 80)
CYAN = (75, 230, 245)
PURPLE = (185, 115, 255)
RED = (235, 75, 90)
GREEN = (100, 235, 130)
DARK = (12, 10, 35)
PANEL = (24, 20, 58)
GREY = (170, 175, 200)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_DIR = os.path.join(BASE_DIR, "assets", "backgrounds")
PLAYER_DIR = os.path.join(BASE_DIR, "assets", "player")


def load_background(filename, fallback_color):
    path = os.path.join(BACKGROUND_DIR, filename)
    if not os.path.exists(path):
        path = os.path.join(BASE_DIR, filename)
    try:
        image = pygame.image.load(path).convert()
        return pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
    except (pygame.error, FileNotFoundError):
        fallback = pygame.Surface((WIDTH, HEIGHT))
        fallback.fill(fallback_color)
        return fallback


living_background = load_background("living_realm.png", (30, 95, 60))
forgotten_background = load_background("forgotten_realm.png", (35, 25, 80))

WORLD_DIR = os.path.join(BASE_DIR, "assets", "world")

def load_world_image(filename, size):
    """Load one of Bhavya's transparent world-art assets at its in-game size."""
    path = os.path.join(WORLD_DIR, filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, size)
    except (pygame.error, FileNotFoundError):
        return None

WORLD_ART = {
    "portal": load_world_image("portal.png", (116, 174)),
    "rune_stone": load_world_image("rune_stone.png", (76, 114)),
    "crystal": load_world_image("crystal.png", (82, 84)),
    "plant": load_world_image("plant.png", (92, 92)),
    "rock": load_world_image("rock.png", (112, 94)),
    "guardian": load_world_image("shadow_guardian.png", (112, 168)),
}

def blit_ground_art(name, center_x, bottom_y):
    image = WORLD_ART.get(name)
    if image:
        screen.blit(image, image.get_rect(midbottom=(center_x, bottom_y)))


def solid_obstacles(realm):
    """Collision boxes for solid scenery; decorative plants and portals stay passable."""
    if realm == "living":
        return [
            pygame.Rect(210, 574, 48, 36),  # left rock
            pygame.Rect(970, 574, 58, 36),  # right rock
            pygame.Rect(646, 580, 40, 28),  # crystal base
        ]
    return [
        pygame.Rect(225, 574, 48, 36),
        pygame.Rect(680, 580, 40, 28),
    ]

def move_player_with_collision(dx, dy):
    """Move on each axis separately so the player slides along solid props."""
    player = game["player"]
    obstacles = solid_obstacles(game["realm"])
    player.x += dx
    player.clamp_ip(screen.get_rect())
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            if dx > 0:
                player.right = obstacle.left
            elif dx < 0:
                player.left = obstacle.right
    player.y += dy
    player.clamp_ip(screen.get_rect())
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            if dy > 0:
                player.bottom = obstacle.top
            elif dy < 0:
                player.top = obstacle.bottom


def draw_text(text, x, y, color=WHITE, selected_font=None, center=False):
    image = (selected_font or FONT).render(str(text), True, color)
    rect = image.get_rect()
    rect.center = (x, y) if center else rect.center
    if not center:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def say(message):
    game["message"] = message
    game["message_timer"] = 240


# The three circles in the Living Realm teach this rune order.
RUNE_LEAF = 1
RUNE_STAR = 2
RUNE_MOON = 3
RUNE_NAMES = {
    RUNE_LEAF: "LEAF",
    RUNE_STAR: "STAR",
    RUNE_MOON: "MOON",
}
RUNE_COLORS = {
    RUNE_LEAF: GREEN,
    RUNE_STAR: CYAN,
    RUNE_MOON: PURPLE,
}

# Trayee's proposed 10x8 design grid translated to this 1280x720 Pygame scene.
# Cell centers use columns A-J and rows 1-8 from level_design/*.md.
def map_cell(column, row):
    col_index = ord(column.upper()) - ord("A")
    return (80 + col_index * 124, 80 + row * 75)

def cell_rect(column, row, width, height):
    cx, cy = map_cell(column, row)
    return pygame.Rect(cx - width // 2, cy - height // 2, width, height)

GARDEN_LANDMARK = cell_rect("E", 2, 46, 46)
INSCRIPTION = cell_rect("D", 3, 44, 44)
CLUES = [
    cell_rect("C", 4, 42, 42),  # Symbol 1
    cell_rect("F", 4, 42, 42),  # Symbol 2
    cell_rect("H", 5, 42, 42),  # Symbol 3
]
CLUE_NAMES = ["LEAF", "STAR", "MOON"]
CLUE_COLORS = [GREEN, CYAN, PURPLE]
PORTAL = cell_rect("H", 7, 70, 100)  # Ancient Arch at H7
MECHANISM = cell_rect("E", 6, 180, 130)  # Celestial puzzle chamber at E6
GUARDIAN_START = cell_rect("G", 6, 48, 60)  # Guardian arena at G6

# Observatory positions from Trayee's Level 2 map.
OBS_ENTRANCE = cell_rect("D", 3, 44, 44)
STAR_MAP_HALL = cell_rect("E", 4, 46, 46)
OBS_CLUE = cell_rect("G", 4, 42, 42)
FINAL_DISCOVERY = cell_rect("F", 2, 64, 64)  # Clearly separated from the mechanism and entrance


def reset_game():
    global CLUES

    # Randomize the three memory locations each time a new game/restart begins.
    # Keep them in the garden area and away from fixed landmarks and puzzle objects.
    clue_spots = [
        ("B", 3), ("C", 3), ("E", 3), ("F", 3), ("G", 3), ("H", 3), ("I", 3),
        ("B", 4), ("C", 4), ("E", 4), ("F", 4), ("H", 4), ("I", 4),
        ("B", 5), ("C", 5), ("D", 5), ("F", 5), ("H", 5), ("I", 5),
        ("B", 6), ("C", 6), ("D", 6), ("F", 6), ("H", 6), ("I", 6),
    ]
    chosen_spots = random.sample(clue_spots, 3)
    CLUES = [cell_rect(column, row, 42, 42) for column, row in chosen_spots]

    # Shuffle the memory-rune order for every new game/restart.
    randomized_runes = [RUNE_LEAF, RUNE_STAR, RUNE_MOON]
    random.shuffle(randomized_runes)

    return {
        "realm": "living",
        "rune_order": randomized_runes,
        "correct_sequence": randomized_runes.copy(),
        "player": cell_rect("B", 2, 36, 52),
        "player_animation": "idle",
        "collected": set(),
        "inscription_found": False,
        "landmark_examined": False,
        "observatory_clue_found": False,
        "portal_unlocked": False,
        "health": 100,
        "guardian_health": 100,
        "guardian": GUARDIAN_START.copy(),
        "puzzle_solved": False,
        "puzzle_active": False,
        "puzzle_screen": False,
        "puzzle_input": [],
        "puzzle_message": "The memories hold the answer.",
        "victory": False,
        "game_over": False,
        "message": "Explore the garden and collect three memories.",
        "message_timer": 300,
        "attack_cooldown": 0,
        "damage_cooldown": 0,
        "map_open": False,
        "hint_timer": 0,
    }


game = reset_game()
director = GameDirector()
director.explore_garden()
footstep_timer = 0


def near_player(rect, distance=80):
    return pygame.Vector2(game["player"].center).distance_to(
        pygame.Vector2(rect.center)
    ) <= distance


def load_animation(folder):
    """Load numbered transparent PNG frames and scale them for the game."""
    path = os.path.join(PLAYER_DIR, folder)
    frames = []
    if os.path.isdir(path):
        for filename in sorted(os.listdir(path)):
            if filename.lower().endswith(".png"):
                try:
                    image = pygame.image.load(os.path.join(path, filename)).convert_alpha()
                    image = pygame.transform.smoothscale(image, (92, 92))
                    frames.append(image)
                except pygame.error:
                    pass
    return frames

PLAYER_ANIMS = {
    "idle": load_animation("idle"),
    "walk": load_animation("walk"),
    "attack": load_animation("attack"),
}


def next_navigation_target():
    """Return the next story target so navigation is based on objectives, not grid codes."""
    if game["realm"] == "living":
        if not game["landmark_examined"]: return GARDEN_LANDMARK, "Garden Mark"
        if not game["inscription_found"]: return INSCRIPTION, "Stone Inscription"
        for i, clue in enumerate(CLUES):
            if i not in game["collected"]: return clue, f"Memory {i + 1}"
        return PORTAL, "Ancient Arch"
    if not game["observatory_clue_found"]: return OBS_CLUE, "Star Map"
    if game["guardian_health"] > 0: return game["guardian"], "Shadow Guardian"
    if not game["puzzle_solved"]: return MECHANISM, "Ancient Mechanism"
    return FINAL_DISCOVERY, "Final Discovery"


def draw_navigation_trail():
    """Soft glowing breadcrumbs point toward the current objective."""
    target, _name = next_navigation_target()
    start = pygame.Vector2(game["player"].center)
    end = pygame.Vector2(target.center)
    delta = end - start
    distance = delta.length()
    if distance < 95: return
    direction = delta.normalize()
    # Small pulsing beads along the direct route; visual guidance only, no teleporting.
    count = min(12, int(distance // 58))
    pulse = pygame.time.get_ticks() // 180
    for i in range(1, count + 1):
        pos = start + direction * (i * distance / (count + 1))
        if (i + pulse) % 3 == 0:
            pygame.draw.circle(screen, (70, 205, 230), (int(pos.x), int(pos.y)), 7)
            pygame.draw.circle(screen, (180, 250, 255), (int(pos.x), int(pos.y)), 3)


def draw_minimap():
    """Toggleable player-facing map: landmarks and labels, never A1-style coordinates."""
    panel = pygame.Rect(300, 92, 680, 520)
    shade = pygame.Surface(panel.size, pygame.SRCALPHA)
    shade.fill((8, 13, 28, 238))
    screen.blit(shade, panel.topleft)
    pygame.draw.rect(screen, GOLD, panel, 3, border_radius=12)
    title = "LIVING REALM MAP" if game["realm"] == "living" else "FORGOTTEN REALM MAP"
    draw_text(title, panel.centerx, panel.y + 24, GOLD, BIG_FONT, center=True)
    inner = pygame.Rect(panel.x + 30, panel.y + 58, panel.width - 60, panel.height - 100)
    pygame.draw.rect(screen, (25, 40, 52), inner, border_radius=8)
    # Soft path lines form a readable schematic, not a developer grid.
    path_points = [(inner.x+45, inner.y+inner.height-45), (inner.x+190, inner.y+inner.height-120), (inner.x+300, inner.y+150), (inner.x+inner.width-90, inner.y+95)]
    pygame.draw.lines(screen, (82, 120, 130), False, path_points, 9)
    if game["realm"] == "living":
        items = [(GARDEN_LANDMARK, "Garden Mark", GOLD, not game["landmark_examined"]), (INSCRIPTION, "Inscription", WHITE, not game["inscription_found"])]
        items += [(c, f"Memory {i+1}", CLUE_COLORS[i], i not in game["collected"]) for i,c in enumerate(CLUES)]
        items += [(PORTAL, "Ancient Arch", PURPLE, not game["portal_unlocked"])]
    else:
        items = [(OBS_CLUE, "Star Map", CYAN, not game["observatory_clue_found"]), (game["guardian"], "Guardian", RED, game["guardian_health"] > 0), (MECHANISM, "Mechanism", PURPLE, not game["puzzle_solved"])]
        if game["puzzle_solved"]:
            items.append((FINAL_DISCOVERY, "FINAL DISCOVERY", GOLD, True))
    def map_point(rect):
        return (inner.x + int(rect.centerx / WIDTH * inner.width), inner.y + int(rect.centery / HEIGHT * inner.height))
    for rect, name, color, active in items:
        pt = map_point(rect)
        pygame.draw.circle(screen, color if active else (95, 115, 120), pt, 8 if active else 5)
        draw_text(name, pt[0], pt[1]-16, WHITE, SMALL_FONT, center=True)
    player_pt = map_point(game["player"])
    pygame.draw.circle(screen, (255,255,255), player_pt, 9, 3)
    draw_text("YOU", player_pt[0], player_pt[1]+14, WHITE, SMALL_FONT, center=True)
    draw_text("M: close map    Gold/bright markers = unfinished objectives", panel.centerx, panel.bottom-22, WHITE, SMALL_FONT, center=True)


def draw_hint():
    if game.get("hint_timer", 0) > 0:
        target, name = next_navigation_target()
        msg = f"HINT: Look for {name}. Follow the glowing trail or press M for the map."
        box = pygame.Rect(260, HEIGHT-92, 760, 42)
        pygame.draw.rect(screen, (12, 20, 34), box, border_radius=8)
        pygame.draw.rect(screen, CYAN, box, 2, border_radius=8)
        draw_text(msg, box.centerx, box.centery, WHITE, SMALL_FONT, center=True)


def draw_player():
    frames = PLAYER_ANIMS.get(game.get("player_animation", "idle"), [])
    if frames:
        frame_index = (pygame.time.get_ticks() // 110) % len(frames)
        sprite = frames[frame_index]
        # Keep the character's feet close to the player collision rectangle.
        sprite_rect = sprite.get_rect(midbottom=(game["player"].centerx, game["player"].bottom + 13))
        screen.blit(sprite, sprite_rect)
    else:
        # Fallback if sprite files are missing.
        pygame.draw.rect(screen, GOLD, game["player"], border_radius=8)
        pygame.draw.circle(screen, (255, 235, 190),
                           (game["player"].centerx, game["player"].y + 10), 8)


def draw_health_bar(x, y, width, height, value, maximum=100):
    pygame.draw.rect(screen, (45, 35, 55), (x, y, width, height), border_radius=4)
    fill_width = max(0, int(width * value / maximum))
    if fill_width:
        pygame.draw.rect(screen, RED if value <= 30 else GREEN,
                         (x, y, fill_width, height), border_radius=4)
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=4)


def draw_message():
    if game["message_timer"] > 0 and game["message"]:
        box = pygame.Rect(160, 20, 960, 46)
        pygame.draw.rect(screen, (15, 15, 30), box, border_radius=8)
        pygame.draw.rect(screen, GOLD, box, 2, border_radius=8)
        draw_text(game["message"], WIDTH // 2, 43, WHITE, SMALL_FONT, center=True)


def draw_living_realm():
    screen.blit(living_background, (0, 0))
    draw_text("LIVING REALM", 25, 25, GREEN, BIG_FONT)
    draw_text(f"Memories: {len(game['collected'])}/3", 25, 65, WHITE, SMALL_FONT)
    # Props and landmarks are positioned from Trayee's Level 1 grid.
    blit_ground_art("plant", GARDEN_LANDMARK.centerx, GARDEN_LANDMARK.bottom + 18)
    blit_ground_art("rock", *map_cell("B", 5))
    blit_ground_art("plant", *map_cell("I", 3))
    blit_ground_art("rock", *map_cell("I", 6))
    blit_ground_art("crystal", *map_cell("E", 5))

    # Make the required Garden Mark unmistakable: the original tiny marker was
    # lost against the busy background and left players stuck.
    if not game["landmark_examined"]:
        pulse = 10
        pygame.draw.circle(screen, (255, 215, 90), GARDEN_LANDMARK.center, pulse + 8, 3)
        pygame.draw.circle(screen, (255, 245, 170), GARDEN_LANDMARK.center, pulse, 3)
        draw_text("GARDEN MARK", GARDEN_LANDMARK.centerx, GARDEN_LANDMARK.y - 24,
                  GOLD, SMALL_FONT, center=True)
        if near_player(GARDEN_LANDMARK, 125):
            draw_text("[E] EXAMINE GARDEN MARK", GARDEN_LANDMARK.centerx,
                      GARDEN_LANDMARK.bottom + 32, GOLD, SMALL_FONT, center=True)
    else:
        draw_text("GARDEN MARK EXAMINED", GARDEN_LANDMARK.centerx,
                  GARDEN_LANDMARK.y - 18, GOLD, SMALL_FONT, center=True)

    # Inscription at D3 is a separate discovery, not one of the three symbols.
    if not game["inscription_found"]:
        if near_player(INSCRIPTION, 155):
            blit_ground_art("rune_stone", INSCRIPTION.centerx, INSCRIPTION.bottom + 20)
            draw_text("[E] READ INSCRIPTION", INSCRIPTION.centerx, INSCRIPTION.bottom + 28,
                      WHITE, SMALL_FONT, center=True)
        else:
            pygame.draw.circle(screen, (145, 155, 175),
                               (INSCRIPTION.centerx, INSCRIPTION.centery), 3, 1)
    else:
        draw_text("INSCRIPTION READ", INSCRIPTION.centerx, INSCRIPTION.centery,
                  GOLD, SMALL_FONT, center=True)

    # Memory stones are deliberately concealed until the player explores nearby.
    # No permanent labels or collect prompts: discovery relies on observation.
    for index, clue in enumerate(CLUES):
        collected = index in game["collected"]
        rune_id = game["rune_order"][index]
        color = RUNE_COLORS[rune_id]
        cx, cy = clue.center
        nearby = near_player(clue, 92)

        if collected:
            # Keep a small, quiet marker after discovery instead of a large label.
            pygame.draw.circle(screen, (115, 190, 145), (cx, cy - 4), 7, 2)
            draw_text("✓", cx, cy - 4, WHITE, SMALL_FONT, center=True)
        elif nearby:
            # Reveal the rune stone and interaction prompt only at close range.
            stone = WORLD_ART.get("rune_stone")
            if stone:
                screen.blit(stone, stone.get_rect(midbottom=(cx, cy + 39)))
            else:
                pygame.draw.circle(screen, color, (cx, cy), 20, 3)
            pygame.draw.circle(screen, color, (cx, cy - 8), 25, 2)
            draw_text("[E] INVESTIGATE", cx, cy + 43, WHITE, SMALL_FONT, center=True)
        else:
            # Only a faint environmental glimmer hints that something may be here.
            pulse = 3 + int((pygame.time.get_ticks() // 350 + index) % 3)
            pygame.draw.circle(screen, (145, 155, 175), (cx, cy + 4), pulse, 1)

    portal_art = WORLD_ART.get("portal")
    if portal_art:
        screen.blit(portal_art, portal_art.get_rect(midbottom=PORTAL.midbottom))
    else:
        portal_color = PURPLE if game["portal_unlocked"] else (90, 85, 125)
        pygame.draw.ellipse(screen, portal_color, PORTAL, 5)
    if near_player(PORTAL, 155) or game["portal_unlocked"]:
        draw_text("ANCIENT ARCH", PORTAL.centerx, PORTAL.y - 25, WHITE, SMALL_FONT, center=True)
        draw_text("OPEN" if game["portal_unlocked"] else "DORMANT",
                  PORTAL.centerx, PORTAL.bottom + 8,
                  GREEN if game["portal_unlocked"] else RED, SMALL_FONT, center=True)
    draw_player()


def draw_forgotten_realm():
    screen.blit(forgotten_background, (0, 0))
    draw_text("OBSERVATORY ABOVE THE CLOUDS", 25, 25, PURPLE, BIG_FONT)
    # Observatory landmarks/clue/final point follow Trayee's Level 2 grid.
    blit_ground_art("rock", *map_cell("B", 5))
    blit_ground_art("plant", STAR_MAP_HALL.centerx, STAR_MAP_HALL.bottom + 18)
    blit_ground_art("crystal", map_cell("I", 5)[0], map_cell("I", 5)[1] + 18)
    if not game["observatory_clue_found"]:
        if near_player(OBS_CLUE, 155):
            blit_ground_art("rune_stone", OBS_CLUE.centerx, OBS_CLUE.bottom + 20)
            draw_text("[E] INVESTIGATE", OBS_CLUE.centerx, OBS_CLUE.bottom + 28,
                      WHITE, SMALL_FONT, center=True)
        else:
            pygame.draw.circle(screen, (145, 155, 175),
                               (OBS_CLUE.centerx, OBS_CLUE.centery), 3, 1)
    else:
        draw_text("CLUE FOUND", OBS_CLUE.centerx, OBS_CLUE.centery,
                  GOLD, SMALL_FONT, center=True)
    pulse = 16 + (pygame.time.get_ticks() // 250) % 7
    discovery_color = GOLD if game["puzzle_solved"] else (100, 100, 145)
    pygame.draw.circle(screen, discovery_color, FINAL_DISCOVERY.center, pulse, 3)
    pygame.draw.circle(screen, CYAN if game["puzzle_solved"] else (100, 100, 145),
                       FINAL_DISCOVERY.center, 7, 0)
    draw_text("FINAL DISCOVERY", FINAL_DISCOVERY.centerx, FINAL_DISCOVERY.bottom + 8,
              WHITE, SMALL_FONT, center=True)
    if game["puzzle_solved"]:
        draw_text("[E] REVEAL THE TRUTH", FINAL_DISCOVERY.centerx,
                  FINAL_DISCOVERY.y - 18, GOLD, SMALL_FONT, center=True)

    # Use Bhavya's actual portal artwork for the Ancient Mechanism in the
    # Forgotten Realm instead of the old placeholder rectangle/circles.
    mechanism_art = WORLD_ART.get("portal")
    if mechanism_art:
        mechanism_image = pygame.transform.smoothscale(mechanism_art, (190, 230))
        mechanism_rect = mechanism_image.get_rect(midbottom=(MECHANISM.centerx, MECHANISM.bottom + 75))
        screen.blit(mechanism_image, mechanism_rect)
        # Keep a clear state indicator without covering the portal artwork.
        state_color = GREEN if game["puzzle_solved"] else (CYAN if game["guardian_health"] <= 0 else RED)
        pygame.draw.circle(screen, state_color, (MECHANISM.centerx, MECHANISM.y + 8), 7)
    else:
        pygame.draw.rect(screen, PURPLE, MECHANISM, 4, border_radius=12)
        pygame.draw.circle(screen, GREEN if game["puzzle_solved"] else CYAN,
                           MECHANISM.center, 30, 4)
        pygame.draw.circle(screen, GOLD, MECHANISM.center, 12, 2)
    draw_text("ANCIENT MECHANISM", MECHANISM.centerx, MECHANISM.y - 28,
              WHITE, SMALL_FONT, center=True)
    if game["puzzle_solved"]:
        draw_text("RESTORED", MECHANISM.centerx, MECHANISM.centery + 48,
                  GREEN, SMALL_FONT, center=True)
    elif game["guardian_health"] <= 0:
        draw_text("Press E to solve", MECHANISM.centerx, MECHANISM.centery + 48,
                  WHITE, SMALL_FONT, center=True)
    else:
        draw_text("GUARDED", MECHANISM.centerx, MECHANISM.centery + 48,
                  RED, SMALL_FONT, center=True)

    if game["guardian_health"] > 0:
        guardian = game["guardian"]
        guardian_art = WORLD_ART.get("guardian")
        if guardian_art:
            screen.blit(guardian_art, guardian_art.get_rect(midbottom=(guardian.centerx, guardian.bottom + 34)))
        else:
            pygame.draw.rect(screen, (90, 55, 125), guardian, border_radius=8)
            pygame.draw.circle(screen, PURPLE, (guardian.centerx, guardian.y + 15), 13)
        draw_health_bar(guardian.x - 10, guardian.y - 18, 68, 9,
                        game["guardian_health"])
        draw_text("SHADOW GUARDIAN", guardian.centerx, guardian.y - 42,
                  WHITE, SMALL_FONT, center=True)

    draw_player()
    draw_text(f"Health: {game['health']}", 25, 65, WHITE, SMALL_FONT)
    draw_health_bar(25, 90, 180, 16, game["health"])


def draw_puzzle_screen():
    """A dedicated puzzle screen in the existing Pygame window."""
    screen.fill(DARK)
    frame = pygame.Rect(36, 30, WIDTH - 72, HEIGHT - 60)
    pygame.draw.rect(screen, (55, 45, 105), frame, border_radius=22)
    pygame.draw.rect(screen, GOLD, frame, 2, border_radius=22)
    draw_text("ANCIENT RUNE PUZZLE", WIDTH // 2, 83, GOLD,
              TITLE_FONT, center=True)
    draw_text("The three memories reveal the order.", WIDTH // 2, 132,
              WHITE, FONT, center=True)

    rune_cards = [
        (pygame.Rect(220, 205, 240, 190), RUNE_LEAF, "LEAF", GREEN),
        (pygame.Rect(520, 205, 240, 190), RUNE_STAR, "STAR", CYAN),
        (pygame.Rect(820, 205, 240, 190), RUNE_MOON, "MOON", PURPLE),
    ]
    for rect, rune_id, label, color in rune_cards:
        pygame.draw.rect(screen, PANEL, rect, border_radius=16)
        pygame.draw.rect(screen, color, rect, 3, border_radius=16)
        cx, cy = rect.centerx, rect.y + 65
        if rune_id == RUNE_LEAF:
            pygame.draw.ellipse(screen, color, (cx - 24, cy - 34, 48, 65), 4)
            pygame.draw.line(screen, color, (cx - 15, cy + 20),
                             (cx + 15, cy - 20), 3)
        elif rune_id == RUNE_STAR:
            points = []
            for i in range(10):
                angle = -math.pi / 2 + i * math.pi / 5
                radius = 34 if i % 2 == 0 else 15
                points.append((cx + math.cos(angle) * radius,
                               cy + math.sin(angle) * radius))
            pygame.draw.polygon(screen, color, points, 4)
        else:
            pygame.draw.circle(screen, color, (cx, cy), 31, 4)
            pygame.draw.circle(screen, PANEL, (cx + 14, cy - 9), 27)
            pygame.draw.arc(screen, color, (cx - 25, cy - 25, 50, 50),
                            math.radians(50), math.radians(300), 4)
        draw_text(f"{rune_id} - {label}", cx, rect.y + 135,
                  WHITE, BIG_FONT, center=True)
        draw_text(f"Press {rune_id}", cx, rect.y + 166,
                  GREY, SMALL_FONT, center=True)

    pygame.draw.rect(screen, PANEL, (260, 430, 760, 78), border_radius=12)
    pygame.draw.rect(screen, (100, 90, 150), (260, 430, 760, 78), 2,
                     border_radius=12)
    names = {RUNE_LEAF: "LEAF", RUNE_STAR: "STAR", RUNE_MOON: "MOON"}
    sequence_text = "   →   ".join(names[n] for n in game["puzzle_input"])
    if not sequence_text:
        sequence_text = "Choose three runes using keys 1, 2, and 3"
    draw_text(sequence_text, WIDTH // 2, 469, WHITE, FONT, center=True)
    draw_text(game["puzzle_message"], WIDTH // 2, 540, GOLD, FONT, center=True)
    draw_text("ENTER: Submit     BACKSPACE: Clear     ESC: Return to game",
              WIDTH // 2, 610, WHITE, SMALL_FONT, center=True)


def draw_end_screen(title, subtitle, color):
    screen.fill(DARK)
    draw_text(title, WIDTH // 2, 250, color, TITLE_FONT, center=True)
    draw_text(subtitle, WIDTH // 2, 325, WHITE, FONT, center=True)
    draw_text("Press R to restart or ESC to quit", WIDTH // 2, 400,
              GOLD, FONT, center=True)


def start_puzzle():
    game["puzzle_active"] = True
    game["puzzle_screen"] = True
    game["puzzle_input"] = []
    game["puzzle_message"] = "Choose the runes in the order revealed by your memories."


running = True
while running:
    clock.tick(FPS)
    if footstep_timer > 0:
        footstep_timer -= 1
    if game["message_timer"] > 0:
        game["message_timer"] -= 1
    if game.get("hint_timer", 0) > 0:
        game["hint_timer"] -= 1
    if game["attack_cooldown"] > 0:
        game["attack_cooldown"] -= 1
    if game["damage_cooldown"] > 0:
        game["damage_cooldown"] -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game["puzzle_screen"]:
                    game["puzzle_screen"] = False
                    game["puzzle_active"] = False
                    game["puzzle_input"] = []
                    say("Puzzle closed. Return to the mechanism and press E to try again.")
                else:
                    running = False

            elif event.key == pygame.K_m and not (game["game_over"] or game["victory"]):
                game["map_open"] = not game["map_open"]
            elif event.key == pygame.K_h and not (game["game_over"] or game["victory"]):
                game["hint_timer"] = 240
                target, name = next_navigation_target()
                say(f"Hint: look for {name}. Follow the glowing trail or press M for the map.")
            elif event.key == pygame.K_r and (game["game_over"] or game["victory"]):
                game = reset_game()
                director = GameDirector()
                director.explore_garden()
                audio.play_music("living")

            # Puzzle controls take priority over normal game controls.
            elif game["puzzle_screen"]:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    if len(game["puzzle_input"]) < 3:
                        game["puzzle_input"].append(RUNE_LEAF)
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    if len(game["puzzle_input"]) < 3:
                        game["puzzle_input"].append(RUNE_STAR)
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    if len(game["puzzle_input"]) < 3:
                        game["puzzle_input"].append(RUNE_MOON)
                elif event.key == pygame.K_BACKSPACE:
                    game["puzzle_input"] = []
                    game["puzzle_message"] = "Your choices have been cleared."
                elif event.key == pygame.K_RETURN:
                    if len(game["puzzle_input"]) != 3:
                        game["puzzle_message"] = "Choose all three runes first!"
                    elif game["puzzle_input"] == game["correct_sequence"]:
                        game["puzzle_solved"] = True
                        director.unlock_arch()
                        audio.play_sound("puzzle")
                        audio.play_sound("portal")
                        game["puzzle_active"] = False
                        game["puzzle_screen"] = False
                        game["puzzle_message"] = "The ancient mechanism is restored!"
                        say("The mechanism is restored! Press E near it to complete the story.")
                    else:
                        game["puzzle_input"] = []
                        game["puzzle_message"] = "Wrong sequence! Try again."
                        audio.play_sound("puzzle_wrong")
                # Prevent this key event from also triggering normal gameplay.
                continue

            elif not game["game_over"] and not game["victory"]:
                if event.key == pygame.K_e:
                    if game["realm"] == "living":
                        collected_one = False
                        if not game["landmark_examined"] and near_player(GARDEN_LANDMARK, 125):
                            game["landmark_examined"] = True
                            audio.play_sound("puzzle")
                            say("The garden mark shows three paths converging. Search the nearby stone inscription before the symbols.")
                            collected_one = True
                        if not collected_one and not game["inscription_found"] and near_player(INSCRIPTION, 60):
                            game["inscription_found"] = True
                            director.discover_clue("garden_inscription")
                            audio.play_sound("puzzle")
                            say("Inscription: 'Three scattered lights remember the path. Seek where the garden's landmarks meet.'")
                            collected_one = True
                        for index, clue in enumerate(CLUES):
                            if collected_one:
                                break
                            if index not in game["collected"] and near_player(clue, 65):
                                game["collected"].add(index)
                                director.discover_clue(f"memory_{index + 1}")
                                director.discover_symbol(f"symbol_{index + 1}")
                                audio.play_sound("collect")
                                say(f"Memory collected: {RUNE_NAMES[game['rune_order'][index]]} rune.")
                                collected_one = True
                                break
                        if not collected_one:
                            if len(game["collected"]) == 3 and game["inscription_found"] and game["landmark_examined"]:
                                game["portal_unlocked"] = True
                            if near_player(PORTAL, 100):
                                if game["portal_unlocked"]:
                                    game["realm"] = "forgotten"
                                    audio.play_sound("portal")
                                    audio.play_music("forgotten")
                                    game["player"].topleft = cell_rect("B", 2, 36, 52).topleft
                                    say("You entered the Observatory. Defeat the shadow guardian.")
                                else:
                                    missing = []
                                    if not game["landmark_examined"]: missing.append("examine the garden mark")
                                    if not game["inscription_found"]: missing.append("read the stone inscription")
                                    if len(game["collected"]) < 3: missing.append(f"find {3-len(game['collected'])} more symbol(s)")
                                    say("The Arch remains dormant: " + "; ".join(missing) + ".")
                            else:
                                say("Look closely at the garden. Investigate anything unusual with E.")
                    else:
                        if not game["observatory_clue_found"] and near_player(OBS_CLUE, 75):
                            game["observatory_clue_found"] = True
                            director.discover_clue("observatory_star_map")
                            audio.play_sound("puzzle")
                            say("The star map points toward the celestial chamber at E6.")
                        elif game["guardian_health"] > 0:
                            say("The guardian protects the mechanism. Press SPACE nearby to attack!")
                        elif not game["puzzle_solved"] and near_player(MECHANISM, 110):
                            start_puzzle()
                        elif game["puzzle_solved"] and near_player(FINAL_DISCOVERY, 100):
                            game["victory"] = True
                            director.enter_portal()
                            audio.play_sound("portal")
                            say("The final memory reveals the truth: the two realms were once one world.")
                        elif game["puzzle_solved"] and near_player(MECHANISM, 140):
                            say("The mechanism is restored. The FINAL DISCOVERY is marked in gold. Follow the glowing trail, press M to view the map, then press E at the gold marker.")
                        elif game["puzzle_solved"]:
                            say("The final memory is waiting at the gold FINAL DISCOVERY marker. Press M for the map or H for a hint.")

                elif event.key == pygame.K_SPACE and game["realm"] == "forgotten":
                    if game["attack_cooldown"] == 0:
                        game["attack_cooldown"] = 25
                        game["player_animation"] = "attack"
                        game["animation_until"] = pygame.time.get_ticks() + 420
                        audio.play_sound("attack")
                        if game["guardian_health"] > 0 and near_player(game["guardian"], 100):
                            game["guardian_health"] = max(0, game["guardian_health"] - 25)
                            audio.play_sound("hit")
                            say("You struck the shadow guardian!")
                            if game["guardian_health"] == 0:
                                director.defeat_guardian()
                                audio.play_sound("guardian_defeat")
                                say("Guardian defeated! Approach the mechanism and press E.")
                        else:
                            say("Move closer to the guardian to attack.")

    # Dedicated puzzle screen: no world movement or world drawing occurs here.
    if game["puzzle_screen"]:
        draw_puzzle_screen()
        pygame.display.flip()
        continue

    if not game["game_over"] and not game["victory"]:
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 4
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 4
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 4
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 4
        if dx and dy:
            dx = int(dx * 0.7071)
            dy = int(dy * 0.7071)
        if pygame.time.get_ticks() < game.get("animation_until", 0):
            game["player_animation"] = "attack"
        else:
            game["player_animation"] = "walk" if (dx or dy) else "idle"
            if (dx or dy) and footstep_timer == 0:
                audio.play_sound("footstep")
                footstep_timer = 22
        move_player_with_collision(dx, dy)

        if game["realm"] == "forgotten" and game["guardian_health"] > 0:
            guardian = game["guardian"]
            px, py = game["player"].center
            gx, gy = guardian.center
            if abs(px - gx) + abs(py - gy) < 480:
                guardian.x += 1 if px > gx else -1 if px < gx else 0
                guardian.y += 1 if py > gy else -1 if py < gy else 0
            if near_player(guardian, 48) and game["damage_cooldown"] == 0:
                game["health"] = max(0, game["health"] - 10)
                game["damage_cooldown"] = 50
                say("The shadow guardian hit you!")
                if game["health"] <= 0:
                    game["game_over"] = True

        if game["realm"] == "living" and len(game["collected"]) == 3 and game["inscription_found"] and game["landmark_examined"]:
            game["portal_unlocked"] = True

    if game["game_over"]:
        draw_end_screen("GAME OVER", "The shadow realm was too strong.", RED)
    elif game["victory"]:
        draw_end_screen("THE WORLDS ARE RESTORED",
                        "You connected the memories of both realms.", GREEN)
    else:
        if game["realm"] == "living":
            draw_living_realm()
        else:
            draw_forgotten_realm()
        draw_navigation_trail()
        if game.get("map_open"):
            draw_minimap()
        draw_hint()
        draw_text("Move: WASD/Arrows | E: Interact | SPACE: Attack | M: Map | H: Hint | ESC: Quit",
                  20, HEIGHT - 32, WHITE, SMALL_FONT)
        objective = director.get_current_objective()
        if game["realm"] == "living":
            if not game["landmark_examined"]:
                objective_title = "Examine the Garden Mark"
            elif not game["inscription_found"]:
                objective_title = "Read the Stone Inscription"
            elif len(game["collected"]) < 3:
                objective_title = "Find the 3 Memories"
            else:
                objective_title = "Enter the Ancient Arch"
            label = f"OBJECTIVE: {objective_title}"
        elif objective is not None:
            label = f"OBJECTIVE: {objective.title}"
        else:
            label = "OBJECTIVE: Explore the Observatory"
            pygame.draw.rect(screen, (12, 10, 35), (WIDTH - 390, 24, 365, 38), border_radius=8)
            pygame.draw.rect(screen, (185, 115, 255), (WIDTH - 390, 24, 365, 38), 2, border_radius=8)
            draw_text(label, WIDTH - 207, 43, WHITE, SMALL_FONT, center=True)
        draw_message()
    pygame.display.flip()

audio.stop_music()
pygame.quit()
