class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.routes = []
        self.connections = []
        self.wagons = 6
        self.score = 0

    def decision_getter(self, decision_range):
        decision = None
        while decision not in decision_range:
            decision = input()
        return decision

    def draw_or_build_decision(self):
        decision = None
        while decision != "draw" and decision != "build":
            decision = input()
        return decision

    def draw_cards(self, cards):
        self.hand.append(cards)

    def draw_route(self, route):
        self.routes.append(route)

    def build_connection(self, track):
        self.wagons -= track.length
        self.score += track.points
        for i in range(track.length):
            self.hand.remove(track.track_type)
