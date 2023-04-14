class Player:
    def __init__(self):
        self.hand = []
        self.routes = []
        self.wagons = 6
        self.score = 0

    def draw_or_build_decision(self):
        decision = None
        while decision != "draw" and decision != "build":
            decision = input()
        return decision

    def draw_cards(self, cards):
        self.hand.append(cards)

    def build_connection(self, wagons_needed, points):
        self.wagons -= wagons_needed
        self.score += points
