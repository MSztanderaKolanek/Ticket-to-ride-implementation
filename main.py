from Player import Player
from Track import Track
import random
import networkx as nx

# Initializing environment, drawing routes

track_12b = Track('track_12b', 1, 2, 5, 10, 'blue')
track_23r = Track('track_23r', 2, 3, 1, 1, 'red')
track_34b = Track('track_34b', 3, 4, 2, 2, 'blue')
track_45r = Track('track_45r', 4, 5, 4, 5, 'red')
track_35r = Track('track_35r', 3, 5, 3, 3, 'red')
track_35b = Track('track_35b', 3, 5, 3, 3, 'blue')
track_15r = Track('track_15r', 1, 5, 2, 2, 'red')
current_map = [track_12b, track_23r, track_34b, track_45r, track_35r, track_35b, track_15r]
routes = [("1", "2", 3), ("1", "3", 5), ("1", "4", 10), ("3", "2", 1), ("4", "5", 3), ("3", "5", 2)]
first_player = Player("Marek")
second_player = Player("Mirek")
first_player.draw_route(routes.pop(random.randint(0, len(routes) - 1)))
second_player.draw_route(routes.pop(random.randint(0, len(routes) - 1)))

def check_routes(player):
    points=0
    route = list(player.routes[0])
    print(route)
    start=int(route[0])
    end=int(route[1])
    p=route[2]

    mp = nx.Graph()
    for i in player.connections:
        mp.add_edge(i[0],i[1])
    if nx.has_path(mp,start,end):
        points=p

    return points

def game(player1, player2, map):
    game_end = False
    players = [player1, player2]
    while not game_end:
        current_player = players[0]
        print(f"{current_player.name}, your routes are: {current_player.routes}")
        print(f"You have {current_player.wagons} wagons")
        print(f"Your cards: {current_player.hand}")
        print(current_player.connections)
        print(f"{current_player.name}, type draw or build")
        decision = current_player.draw_or_build_decision()
        if decision == "draw":
            current_player.draw_cards(random.choice(['red', 'blue']))
        elif decision == "build":
            print(f"{current_player.name}, type 0/1/2 .. according to track you want to build")
            print(f"{[track.name for track in map]}")
            decision = current_player.decision_getter([str(i) for i in range(len(map))])
            track_to_built = map[int(decision)]

            # check if player has enough cards to built track
            cards_with_matching_color = 0
            for card in current_player.hand:
                if card == track_to_built.track_type:
                    cards_with_matching_color += 1
            if cards_with_matching_color >= track_to_built.length:
                map.pop(int(decision))
                current_player.build_connection(track_to_built)
                print(f"{current_player.name} built track {track_to_built.name}."
                      f" Current score: {current_player.score}, wagons left: {current_player.wagons}")
            else:
                print("You don't have enough cards to build chosen track")
        if current_player.wagons <= 0:
            game_end = True
        players[0], players[1] = players[1], players[0]

    print(player1.score, player2.score)
    player1.score+=check_routes(player1)
    player2.score += check_routes(player2)
    print(player1.score, player2.score)
    return 0


game1 = game(first_player, second_player, current_map)
