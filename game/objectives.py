
from dataclasses import dataclass


@dataclass
class Objective:
    objective_id: str
    title: str
    description: str
    completed: bool = False


class ObjectiveManager:
    def __init__(self):
        self.objectives = [
            Objective(
                "explore_garden",
                "Explore the Garden",
                "Find the ancient inscription."
            ),
            Objective(
                "find_symbols",
                "Discover the Symbols",
                "Investigate all three ancient symbols."
            ),
            Objective(
                "defeat_guardian",
                "Defeat the Guardian",
                "Clear the path through the ruins."
            ),
            Objective(
                "solve_arch",
                "Unlock the Ancient Arch",
                "Use the clues to activate the arch."
            ),
            Objective(
                "enter_portal",
                "Enter the Portal",
                "Travel to the Observatory."
            ),
        ]

    def get_current_objective(self):
        for objective in self.objectives:
            if not objective.completed:
                return objective
        return None

    def complete_objective(self, objective_id):
        current = self.get_current_objective()

        if current is None or current.objective_id != objective_id:
            return False

        current.completed = True
        return True

    def get_progress(self):
        total = len(self.objectives)
        completed = sum(
            objective.completed for objective in self.objectives
        )
        return completed, total

    def get_status(self):
        current = self.get_current_objective()

        if current is None:
            return "Level completed!"

        completed, total = self.get_progress()

        return (
            f"Objective: {current.title}\n"
            f"{current.description}\n"
            f"Progress: {completed}/{total}"
        )
