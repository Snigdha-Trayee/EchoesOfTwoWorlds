
from game.cinematic_events import CinematicEventManager
from game.discovery_manager import DiscoveryManager
from game.objectives import ObjectiveManager


class GameDirector:
    def __init__(self):
        self.objectives = ObjectiveManager()
        self.discoveries = DiscoveryManager()
        self.cinematics = CinematicEventManager()
        self.guardian_defeated = False
        self.arch_unlocked = False
        self.portal_entered = False

    def explore_garden(self):
        first_visit = self.discoveries.visit_location("garden")

        if first_visit:
            self.objectives.complete_objective("explore_garden")
            self.cinematics.trigger(
                "garden_discovered",
                {"location": "garden"},
            )

        return first_visit

    def discover_clue(self, clue_id):
        discovered = self.discoveries.discover_clue(clue_id)

        if discovered:
            self.cinematics.trigger(
                "clue_discovered",
                {"clue_id": clue_id},
            )

        return discovered

    def discover_symbol(self, symbol_id):
        discovered = self.discoveries.discover_symbol(symbol_id)

        if discovered:
            self.cinematics.trigger(
                "symbol_discovered",
                {
                    "symbol_id": symbol_id,
                    "total_symbols": self.discoveries.get_symbol_count(),
                },
            )

        if self.discoveries.all_symbols_found():
            self.objectives.complete_objective("find_symbols")

        return discovered

    def defeat_guardian(self):
        if self.guardian_defeated:
            return False

        self.guardian_defeated = True
        self.objectives.complete_objective("defeat_guardian")
        self.cinematics.trigger("guardian_defeated")
        return True

    def unlock_arch(self):
        if self.arch_unlocked:
            return False

        if not self.discoveries.discovered_clues:
            return False

        if not self.discoveries.all_symbols_found():
            return False

        if not self.guardian_defeated:
            return False

        self.arch_unlocked = True
        self.objectives.complete_objective("solve_arch")
        self.cinematics.trigger("ancient_arch_unlocked")
        return True

    def enter_portal(self):
        if self.portal_entered or not self.arch_unlocked:
            return False

        self.portal_entered = True
        self.objectives.complete_objective("enter_portal")
        self.cinematics.trigger(
            "portal_entered",
            {"destination": "observatory"},
        )
        return True

    def get_current_objective(self):
        return self.objectives.get_current_objective()

    def get_status(self):
        completed, total = self.objectives.get_progress()

        return {
            "objective_status": self.objectives.get_status(),
            "completed_objectives": completed,
            "total_objectives": total,
            "discoveries": self.discoveries.get_discovery_summary(),
            "guardian_defeated": self.guardian_defeated,
            "arch_unlocked": self.arch_unlocked,
            "portal_entered": self.portal_entered,
            "level_completed": completed == total,
        }

    def get_next_cinematic(self):
        return self.cinematics.get_next_event()
