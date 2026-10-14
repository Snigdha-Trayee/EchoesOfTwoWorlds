"""Audio support for Echoes of Two Worlds using Bhavya's supplied audio."""
from pathlib import Path
import pygame


class AudioManager:
    def __init__(self, project_dir=None, sound_volume=0.70, music_volume=0.32):
        # Default to the folder containing this file, so main.py can use AudioManager()
        if project_dir is None:
            project_dir = Path(__file__).resolve().parent
        self.audio_dir = Path(project_dir) / "assets" / "audio"
        self.sound_volume = sound_volume
        self.music_volume = music_volume
        self.enabled = False
        self.sounds = {}
        self.current_music_key = None
        self.last_end_state = None
        self.last_footstep_ms = 0
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.enabled = True
            self._load_sounds()
        except pygame.error as exc:
            print(f"Audio disabled; the game will still run: {exc}")

    def _load_sound(self, key, filename):
        path = self.audio_dir / filename
        if not path.is_file():
            print(f"Audio file not found (skipping): {path.name}")
            return
        try:
            sound = pygame.mixer.Sound(str(path))
            sound.set_volume(self.sound_volume)
            self.sounds[key] = sound
        except pygame.error as exc:
            print(f"Could not load sound {path.name}: {exc}")

    def _load_sounds(self):
        # Actual filenames supplied in Bhavya's Art.zip.
        self._load_sound("footstep", "footstep04.ogg")
        self._load_sound("memory_collect", "handleCoins.ogg")
        self._load_sound("portal", "jingles_HIT02.ogg")
        self._load_sound("attack", "metalClick.ogg")
        self._load_sound("guardian_hit", "metalClick.ogg")
        self._load_sound("guardian_defeat", "jingles_HIT02.ogg")
        self._load_sound("puzzle_success", "jingles_HIT02.ogg")
        self._load_sound("puzzle_wrong", "metalClick.ogg")

    def play(self, name):
        if not self.enabled:
            return
        if name == "footstep":
            now = pygame.time.get_ticks()
            if now - self.last_footstep_ms < 300:
                return
            self.last_footstep_ms = now
        sound = self.sounds.get(name)
        if sound is not None:
            try:
                sound.play()
            except pygame.error as exc:
                print(f"Could not play sound '{name}': {exc}")

    def _music_path(self, realm):
        filename = "012_Sirens_in_Darkness.mp3" if realm == "forgotten" else "Forest Whisper.ogg"
        path = self.audio_dir / filename
        return path if path.is_file() else None

    def _start_realm_music(self, realm):
        key = f"realm:{realm}"
        if self.current_music_key == key:
            return
        self.current_music_key = key
        if not self.enabled:
            return
        path = self._music_path(realm)
        if path is None:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
        except pygame.error as exc:
            print(f"Could not play music {path.name}: {exc}")

    # Compatibility aliases used by main.py.
    def play_music(self, realm):
        self._start_realm_music(realm)

    def play_sound(self, name):
        aliases = {
            "collect": "memory_collect",
            "puzzle": "puzzle_success",
            "hit": "guardian_hit",
            "footstep": "footstep",
        }
        self.play(aliases.get(name, name))

    def stop_music(self):
        if self.enabled:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass
        self.current_music_key = None

    def update(self, realm, game_over=False, victory=False):
        end_state = "game_over" if game_over else "victory" if victory else None
        if end_state is not None and end_state != self.last_end_state:
            try:
                if self.enabled:
                    pygame.mixer.music.stop()
            except pygame.error:
                pass
            self.current_music_key = None
        elif end_state is None:
            self._start_realm_music(realm)
        self.last_end_state = end_state

    def set_volume(self, sound_volume=None, music_volume=None):
        if sound_volume is not None:
            self.sound_volume = max(0.0, min(1.0, float(sound_volume)))
            for sound in self.sounds.values():
                sound.set_volume(self.sound_volume)
        if music_volume is not None:
            self.music_volume = max(0.0, min(1.0, float(music_volume)))
            if self.enabled:
                try:
                    pygame.mixer.music.set_volume(self.music_volume)
                except pygame.error:
                    pass
