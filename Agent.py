class Agent:
    @staticmethod
    def get_legal_actions(player, initialized_map, current_map):
        legal_actions = ['draw']  # draw, build first track, .. 0 - not legal, 1 - legal

        num_red_cards = 0
        num_blue_cards = 0
        for card in player.hand:
            if card == 'red':
                num_red_cards += 1
            elif card == 'blue':
                num_blue_cards += 1

        for track in initialized_map:
            legal = True
            if track not in current_map:
                legal = False
            else:
                if track.track_type == 'red':
                    if num_red_cards < track.length:
                        legal = False
                elif track.track_type == 'blue':
                    if num_blue_cards < track.length:
                        legal = False
            if legal:
                legal_actions.append(track.name)

        return legal_actions

    def get_feature_vector(self, player, action: str = None):
        """
        Number of red cards
        Number of blue cards
        Number of connections build
        Number of wagons left
        :return: vector of features
        """
        num_red_cards = 0
        num_blue_cards = 0
        for card in player.hand:
            if card == 'red':
                num_red_cards += 1
            elif card == 'blue':
                num_blue_cards += 1
        num_connections = len(player.connections)
        num_wagons = player.wagons

        return [num_red_cards, num_blue_cards, num_connections, num_wagons]
