from Player import Player
from Track import Track
import random
import networkx as nx
from Agent import Agent
import numpy as np
import os
import pickle


def check_routes(player):
    points = 0
    if not player.routes:
        return points
    for route in player.routes:
        # print(route)
        start = int(route[0])
        end = int(route[1])
        p = route[2]
        mp = nx.Graph()
        for i in player.connections:
            mp.add_edge(i[0], i[1])
        start_ok = False
        end_ok = False
        for edge in mp.edges:
            if start in edge:
                start_ok = True
            if end in edge:
                end_ok = True
        if start_ok and end_ok:
            if nx.has_path(mp, start, end):
                points += p
                player.complete_route(route)
    return points


def check_reward(action, player, initialized_map, current_map):
    reward = -1
    if action == "draw":
        return reward
    if not player.routes:
        reward = 100
        return reward
    reward = -100
    track_built = 0
    for track in initialized_map:
        if track.name == action:
            track_built = track
    mp = nx.Graph()
    for track in current_map:
        mp.add_edge(track.station1, track.station2)
    for connection in player.connections:
        mp.add_edge(connection[0], connection[1])
    for route in player.routes:
        start = int(route[0])
        end = int(route[1])
        if start in mp:
            if end in mp:
                if nx.has_path(mp, start, end):
                    for path in nx.all_shortest_paths(mp, start, end):
                        for i in range(len(path) - 1):
                            if track_built.station1 == path[i] and track_built.station2 == path[i+1]:
                                reward = 100
                            elif track_built.station1 == path[i+1] and track_built.station2 == path[1]:
                                reward = 100
    return reward


def games(episodes, iterations, number_of_features, min_epsilon, epsilon_dec, gamma, gather_data, learning_rate, save):
    if os.path.isfile("data"):
        with open("data", 'rb') as f:
            gameplay_data = pickle.load(f)
    else:
        gameplay_data = []
    if os.path.isfile("model"):
        with open("model", 'rb') as f:
            weights, episode = pickle.load(f)
    else:
        weights = np.array([np.random.uniform(-0.1, 0.1) for _ in range(number_of_features)])
    agent = Agent()

    best_score = 0
    period_best_score = 0

    for episode in range(episodes):
        # Initializing environment, drawing routes
        track_12b = Track('track_12b', 1, 2, 5, 10, 'blue')
        track_23r = Track('track_23r', 2, 3, 1, 1, 'red')
        track_34b = Track('track_34b', 3, 4, 2, 2, 'blue')
        track_45r = Track('track_45r', 4, 5, 4, 5, 'red')
        track_35r = Track('track_35r', 3, 5, 3, 3, 'red')
        track_35b = Track('track_35b', 3, 5, 3, 3, 'blue')
        track_15r = Track('track_15r', 1, 5, 2, 2, 'red')
        initialized_map = [track_12b, track_23r, track_34b, track_45r, track_35r, track_35b, track_15r]
        current_map = [track_12b, track_23r, track_34b, track_45r, track_35r, track_35b, track_15r]
        routes = [("1", "2", 3), ("1", "3", 5), ("1", "4", 10), ("3", "2", 1), ("4", "5", 3), ("3", "5", 2)]

        playing_player = Player("Marek")
        # playing_player.draw_route(routes[1])
        playing_player.draw_route(random.choice(routes))
        players = [playing_player]

        game_end = False
        iterations_counter = 0
        #print(check_reward('track_34b', playing_player, initialized_map, current_map))
        while not game_end:
            current_player = players[0]
            # printing stuff
            # print(f"{current_player.name}, your routes are: {current_player.routes}")
            # print(f"You have {current_player.wagons} wagons")
            # print(f"Your cards: {current_player.hand}")
            # print(current_player.connections)
            # print(f"{current_player.name}, type draw or build")

            epsilon = max(min_epsilon, 0.9 - episode * epsilon_dec)
            actions = agent.get_legal_actions(current_player, initialized_map, current_map)

            # print(actions)
            if np.random.random() < epsilon:
                action = np.random.choice(actions)
            else:
                # choose action with highest Q-value
                actions = agent.get_legal_actions(current_player, initialized_map, current_map)
                q_values = [np.dot(weights.T, agent.get_feature_vector(current_player, a)) for a in actions]
                action_index = np.argmax(q_values)
                action = actions[action_index]
            # print(action)

            # decision = current_player.draw_or_build_decision()
            if action == "draw":
                current_player.draw_cards(random.choice(['red', 'blue']))
            else:
                # print(f"{current_player.name}, type 0/1/2 .. according to track you want to build")
                # print(f"{[track.name for track in current_map]}")
                # decision = current_player.decision_getter([str(i) for i in range(len(current_map))])
                # track_to_built = current_map[int(decision)]

                # check if player has enough cards to built track
                # cards_with_matching_color = 0
                # for card in current_player.hand:
                #     if card == track_to_built.track_type:
                #         cards_with_matching_color += 1
                # if cards_with_matching_color >= track_to_built.length:
                #     current_map.pop(int(decision))
                #     current_player.build_connection(track_to_built)
                #     print(f"{current_player.name} built track {track_to_built.name}."
                #           f" Current score: {current_player.score}, wagons left: {current_player.wagons}")
                # else:
                #     print("You don't have enough cards to build chosen track")
                track_to_built = 0
                for track in current_map:
                    if action == track.name:
                        track_to_built = current_map.pop(current_map.index(track))
                current_player.build_connection(track_to_built)
                current_player.score += check_routes(current_player)

            # Check if game ends
            if current_player.wagons <= 0:
                game_end = True
            iterations_counter += 1
            if iterations_counter == iterations:
                game_end = True

            # Update weights
            feature_vector = agent.get_feature_vector(current_player)
            if gather_data:
                gameplay_data.append([feature_vector, action])
            reward = check_reward(action, current_player, initialized_map, current_map)
            # print(check_reward(action, current_player, initialized_map, current_map))
            # print(current_player.completed_routes)
            q_value = np.dot(weights.T, feature_vector)
            if game_end:
                target_q = reward
            else:
                max_q = max([np.dot(weights.T, feature_vector) for a in actions])
                target_q = reward + gamma * max_q

            error = target_q - q_value
            for j in range(len(weights)):
                weights[j] += learning_rate * error * feature_vector[j]
        if episode == 0:
            best_score = playing_player.score
            best_connections = playing_player.connections
            best_routes_uncom = playing_player.routes
            best_routes_com = playing_player.completed_routes
        if playing_player.score > best_score:
            best_score = playing_player.score
            best_connections = playing_player.connections
            best_routes_uncom = playing_player.routes
            best_routes_com = playing_player.completed_routes
            if save:
                with open(os.path.join("model"), "wb") as f:
                    data = (weights, episode)
                    pickle.dump(data, f)
        if playing_player.score > period_best_score:
            period_best_score = playing_player.score
            best_connections = playing_player.connections
            best_routes_uncom = playing_player.routes
            best_routes_com = playing_player.completed_routes
        if episode % 10 == 0:
        # if True:
            print(f"Episode: {episode}, Best period Score: {period_best_score},"
                  f" Best Score: {best_score}, Routes uncompleted: {best_routes_uncom}, "
                  f"Routes completed: {best_routes_com}, Connections Built: {best_connections}")
            if save:
                with open("model", "wb") as f:
                    data = (weights, episode)
                    pickle.dump(data, f)
            period_best_score = 0

    if save:
        with open("model", "wb") as f:
            data = (weights, episode)
            pickle.dump(data, f)
    if gather_data:
        with open("data", "wb") as f:
            pickle.dump(gameplay_data, f)
    # print(players[0].score)
    # players[0].score += check_routes(players[0])
    # print(players[0].score)


# episodes = 10

game1 = games(episodes=100, iterations=100, number_of_features=4, min_epsilon=0.01, epsilon_dec=0.003, gamma=0.5, gather_data=True, learning_rate=0.001, save=True)
