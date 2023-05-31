import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import pickle
import os
from Player import Player
from Track import Track
from Agent import Agent


def visualize(game_map, connections):
    mp = nx.Graph()
    for x in range(13):
        mp.add_node(x+1)
    for track in game_map:
        mp.add_edge(track.station1, track.station2, length=track.length)

    colored_edges = []
    colored_nodes = []
    for connection in connections:
        if connection[0] < connection[1]:
            colored_edges.append((int(connection[0]), int(connection[1])))
        else:
            colored_edges.append((int(connection[1]), int(connection[0])))
        if int(connection[0]) not in colored_nodes:
            colored_nodes.append((int(connection[0])))
        if int(connection[1]) not in colored_nodes:
            colored_nodes.append((int(connection[1])))

    pos = nx.spring_layout(mp, seed=204, weight='length')
    node_colors = ['blue' if node in colored_nodes else 'lightblue' for node in mp.nodes()]

    edge_colors = ['blue' if edge in colored_edges else 'gray' for edge in mp.edges()]
    nx.draw(mp, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=12)

    nx.draw_networkx_edges(mp, pos, edgelist=mp.edges(), edge_color=edge_colors, width=10)
    edge_labels = nx.get_edge_attributes(mp, 'length')
    nx.draw_networkx_edge_labels(mp, pos, edge_labels=edge_labels,
                                 font_color='black', label_pos=0.5, verticalalignment='center')
    plt.show()


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


def games(episodes, iterations, min_epsilon, epsilon_dec, gamma,
          gather_data, learning_rate, save, show_best):
    agent = Agent()
    empty_player = Player("empty")
    best_score = 0
    period_best_score = 0
    game_map = []

    if os.path.isfile("data"):
        with open("data", 'rb') as f:
            gameplay_data = pickle.load(f)
    else:
        gameplay_data = []
    if os.path.isfile("model"):
        with open("model", 'rb') as f:
            weights, episode = pickle.load(f)
    else:
        weights = np.array([np.random.uniform(-0.1, 0.1) for _ in range(len(agent.get_feature_vector(empty_player)))])

    for episode in range(episodes):
        # Initializing environment, drawing routes
        track_12b = Track('track_12b', 1, 2, 5, 10, 'blue')
        track_23r = Track('track_23r', 2, 3, 1, 1, 'red')
        track_34b = Track('track_34b', 3, 4, 2, 2, 'blue')
        track_45r = Track('track_45r', 4, 5, 4, 7, 'red')
        track_35r = Track('track_35r', 3, 5, 3, 4, 'red')
        track_35b = Track('track_35b', 3, 5, 3, 4, 'blue')
        track_15r = Track('track_15r', 1, 5, 2, 2, 'red')
        track_46y = Track('track_46y', 4, 6, 1, 1, 'yellow')
        track_36y = Track('track_36y', 3, 6, 2, 2, 'yellow')
        track_27r = Track('track_27r', 2, 7, 4, 7, 'red')
        track_67b = Track('track_67b', 6, 7, 3, 4, 'blue')
        track_68y = Track('track_68y', 6, 8, 3, 4, 'yellow')
        track_89r = Track('track_89r', 8, 9, 4, 7, 'red')
        track_49b = Track('track_49b', 4, 9, 2, 2, 'blue')
        track_49y = Track('track_49y', 4, 9, 2, 2, 'yellow')
        track_910y = Track('track_910y', 9, 10, 3, 4, 'yellow')
        track_510b = Track('track_510b', 5, 10, 2, 2, 'blue')
        track_511b = Track('track_511b', 5, 11, 3, 4, 'blue')
        track_111y = Track('track_111y', 1, 11, 5, 10, 'yellow')
        track_1112r = Track('track_1112r', 11, 12, 3, 4, 'red')
        track_112b = Track('track_112b', 1, 12, 2, 2, 'blue')
        track_112y = Track('track_112y', 1, 12, 2, 2, 'yellow')
        track_113b = Track('track_113b', 1, 13, 2, 2, 'blue')
        track_213r = Track('track_213r', 2, 13, 3, 4, 'red')

        initialized_map = [track_12b, track_23r, track_34b, track_45r, track_35r, track_35b, track_15r, track_213r,
                           track_113b, track_112y, track_112b, track_1112r, track_111y, track_511b, track_510b,
                           track_910y, track_89r, track_68y, track_36y, track_46y, track_27r, track_67b, track_49b,
                           track_49y]
        current_map = initialized_map.copy()
        game_map = initialized_map.copy()
        small_routes = [("1", "11", 5), ("1", "2", 5), ("5", "6", 5), ("5", "9", 5),
                        ("3", "10", 5), ("2", "7", 4), ("4", "8", 4), ("2", "9", 5)]
        big_routes = [("9", "13", 11), ("1", "7", 13), ("6", "11", 10), ("8", "12", 14)]

        playing_player = Player("Gracz")
        playing_player.draw_route(random.choice(big_routes))
        playing_player.draw_route(random.choice(small_routes))
        players = [playing_player]

        game_end = False
        iterations_counter = 0

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

            if np.random.random() < epsilon:
                action = np.random.choice(actions)
            else:
                # Choose action with highest Q-value
                actions = agent.get_legal_actions(current_player, initialized_map, current_map)
                q_values = [np.dot(weights.T, agent.get_feature_vector(current_player)) for _ in actions]
                action_index = np.argmax(q_values)
                action = actions[action_index]

            if action == "draw":
                current_player.draw_cards(random.choice(['red', 'blue', 'yellow']))
            else:
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

            q_value = np.dot(weights.T, feature_vector)
            if game_end:
                target_q = reward
            else:
                max_q = max([np.dot(weights.T, feature_vector) for _ in actions])
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
    if show_best:
        visualize(game_map, best_connections)
    if save:
        with open("model", "wb") as f:
            data = (weights, episode)
            pickle.dump(data, f)
    if gather_data:
        with open("data", "wb") as f:
            pickle.dump(gameplay_data, f)
    return 0


game1 = games(episodes=11, iterations=100,  min_epsilon=0.01, epsilon_dec=0.01, gamma=0.5,
              gather_data=True, learning_rate=0.01, save=True, show_best=True)
