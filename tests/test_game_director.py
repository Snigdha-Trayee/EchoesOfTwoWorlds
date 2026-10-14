
import unittest

from game.objectives import ObjectiveManager
from game.discovery_manager import DiscoveryManager
from game.cinematic_events import CinematicEventManager
from game.game_director import GameDirector


class TestGameDirector(unittest.TestCase):

    def test_objective_progress(self):
        manager = ObjectiveManager()

        self.assertEqual(manager.get_progress(), (0, 5))
        self.assertTrue(manager.complete_objective("explore_garden"))
        self.assertEqual(manager.get_progress(), (1, 5))
        self.assertEqual(
            manager.get_current_objective().objective_id,
            "find_symbols",
        )

    def test_discoveries_are_not_duplicated(self):
        manager = DiscoveryManager()

        self.assertTrue(manager.discover_symbol("symbol_1"))
        self.assertFalse(manager.discover_symbol("symbol_1"))

        manager.discover_symbol("symbol_2")
        manager.discover_symbol("symbol_3")

        self.assertTrue(manager.all_symbols_found())
        self.assertEqual(manager.get_symbol_count(), 3)

    def test_cinematic_event_triggers_once(self):
        manager = CinematicEventManager()

        self.assertTrue(manager.trigger("portal_activated"))
        self.assertFalse(manager.trigger("portal_activated"))

        event = manager.get_next_event()

        self.assertEqual(event["event"], "portal_activated")
        self.assertIsNone(manager.get_next_event())

    def test_cinematic_payload_is_preserved(self):
        manager = CinematicEventManager()
        payload = {"destination": "observatory"}

        self.assertTrue(manager.trigger("portal_entered", payload))

        event = manager.get_next_event()

        self.assertEqual(event["event"], "portal_entered")
        self.assertEqual(event["payload"], payload)

    def test_cinematic_reset_allows_event_again(self):
        manager = CinematicEventManager()

        self.assertTrue(manager.trigger("portal_entered"))
        self.assertFalse(manager.trigger("portal_entered"))

        manager.reset()

        self.assertTrue(manager.trigger("portal_entered"))
        self.assertTrue(manager.has_triggered("portal_entered"))

    def test_garden_completes_first_objective(self):
        game = GameDirector()

        self.assertTrue(game.explore_garden())
        self.assertFalse(game.explore_garden())
        self.assertEqual(game.objectives.get_progress(), (1, 5))

    def test_arch_requires_all_prerequisites(self):
        game = GameDirector()

        self.assertFalse(game.unlock_arch())

        game.explore_garden()
        game.discover_clue("ancient_inscription")

        for symbol in ("symbol_1", "symbol_2", "symbol_3"):
            game.discover_symbol(symbol)

        self.assertFalse(game.unlock_arch())

        game.defeat_guardian()

        self.assertTrue(game.unlock_arch())
        self.assertFalse(game.unlock_arch())

    def test_complete_game_flow(self):
        game = GameDirector()

        game.explore_garden()
        game.discover_clue("ancient_inscription")

        for symbol in ("symbol_1", "symbol_2", "symbol_3"):
            game.discover_symbol(symbol)

        game.defeat_guardian()

        self.assertTrue(game.unlock_arch())
        self.assertTrue(game.enter_portal())
        self.assertFalse(game.enter_portal())

        status = game.get_status()

        self.assertEqual(status["completed_objectives"], 5)
        self.assertEqual(status["total_objectives"], 5)
        self.assertTrue(status["level_completed"])

    def test_objectives_cannot_be_completed_out_of_order(self):
        manager = ObjectiveManager()

        self.assertFalse(
            manager.complete_objective("defeat_guardian")
        )
        self.assertFalse(
            manager.complete_objective("unknown_objective")
        )
        self.assertEqual(manager.get_progress(), (0, 5))

        self.assertTrue(
            manager.complete_objective("explore_garden")
        )
        self.assertEqual(manager.get_progress(), (1, 5))

    def test_portal_objective_requires_arch_objective(self):
        manager = ObjectiveManager()

        self.assertFalse(
            manager.complete_objective("enter_portal")
        )
        self.assertEqual(manager.get_progress(), (0, 5))


if __name__ == "__main__":
    unittest.main()
