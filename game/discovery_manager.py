
class DiscoveryManager:
    def __init__(self):
        self.discovered_clues = set()
        self.discovered_symbols = set()
        self.visited_locations = set()

    def discover_clue(self, clue_id):
        if clue_id in self.discovered_clues:
            return False

        self.discovered_clues.add(clue_id)
        return True

    def discover_symbol(self, symbol_id):
        if symbol_id in self.discovered_symbols:
            return False

        self.discovered_symbols.add(symbol_id)
        return True

    def visit_location(self, location_id):
        if location_id in self.visited_locations:
            return False

        self.visited_locations.add(location_id)
        return True

    def get_symbol_count(self):
        return len(self.discovered_symbols)

    def all_symbols_found(self, required_count=3):
        return self.get_symbol_count() >= required_count

    def get_discovery_summary(self):
        return {
            "clues": len(self.discovered_clues),
            "symbols": len(self.discovered_symbols),
            "locations": len(self.visited_locations),
        }
