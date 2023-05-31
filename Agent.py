class Agent:
    @staticmethod
    def get_legal_actions(player, initialized_map, current_map):
        legal_actions = ['draw']  # draw, build first track, .. 0 - not legal, 1 - legal

        num_red_cards = 0
        num_blue_cards = 0
        num_yellow_cards = 0
        for card in player.hand:
            if card == 'red':
                num_red_cards += 1
            elif card == 'blue':
                num_blue_cards += 1
            elif card == 'yellow':
                num_yellow_cards += 1

        for track in initialized_map:
            legal = True
            if track not in current_map:
                legal = False
            if track.track_type == 'red':
                if num_red_cards < track.length:
                    legal = False
            elif track.track_type == 'blue':
                if num_blue_cards < track.length:
                    legal = False
            elif track.track_type == 'yellow':
                if num_yellow_cards < track.length:
                    legal = False
            if player.wagons < track.length:
                legal = False
            if legal:
                legal_actions.append(track.name)
        return legal_actions

    @staticmethod
    def get_feature_vector(player):
        """
        Number of red cards
        Number of blue cards
        Number of yellow cards
        Number of connections build
        Number of wagons left
        Number of unbuilt tracks connected to city 1
        Number of unbuilt tracks connected to city 2
        Number of unbuilt tracks connected to city 3
        Number of unbuilt tracks connected to city 4
        Number of unbuilt tracks connected to city 5
        Number of unbuilt tracks connected to city 6
        Number of unbuilt tracks connected to city 7
        Number of unbuilt tracks connected to city 8
        Number of unbuilt tracks connected to city 9
        Number of unbuilt tracks connected to city 10
        Number of unbuilt tracks connected to city 11
        Number of unbuilt tracks connected to city 12
        Number of unbuilt tracks connected to city 13
        Binary value if player needs to complete route from city 1 to city 11
        Binary value if player needs to complete route from city 1 to city 2
        Binary value if player needs to complete route from city 5 to city 6
        Binary value if player needs to complete route from city 5 to city 9
        Binary value if player needs to complete route from city 3 to city 10
        Binary value if player needs to complete route from city 2 to city 7
        Binary value if player needs to complete route from city 4 to city 8
        Binary value if player needs to complete route from city 2 to city 9
        Binary value if player needs to complete route from city 9 to city 13
        Binary value if player needs to complete route from city 1 to city 7
        Binary value if player needs to complete route from city 6 to city 11
        Binary value if player needs to complete route from city 8 to city 12
        :return: vector of features
        """
        num_red_cards = 0
        num_blue_cards = 0
        num_yellow_cards = 0
        for card in player.hand:
            if card == 'red':
                num_red_cards += 1
            elif card == 'blue':
                num_blue_cards += 1
            elif card == 'yellow':
                num_yellow_cards += 1
        num_connections = len(player.connections)
        num_wagons = player.wagons

        return [num_red_cards, num_blue_cards, num_yellow_cards, num_connections, num_wagons]
