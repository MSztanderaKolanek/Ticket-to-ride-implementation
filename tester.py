from Player import Player
from Track import Track
import random
import networkx as nx

#To use tester, removing cards from player's hand for building connections in Player cards must be commented

random.seed(1)
tb = Track('tb',2,3,1,1,'b')
tr = Track('tr',2,3,1,1,'r')
tr1 = Track('tr',4,3,1,1,'r')
tb2 = Track('tr',1,3,1,1,'b')
tb1 = Track('tr',1,5,1,1,'b')

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

player = Player("Pl1")
player.draw_cards(random.choice(['red', 'red']))
player.draw_cards(random.choice(['red', 'red']))
player.draw_cards(random.choice(['blue', 'blue']))
player.draw_cards(random.choice(['blue', 'blue']))
player.draw_cards(random.choice(['blue', 'blue']))
#print(player.hand)
#print(tr)
player.build_connection(tr)
player.build_connection(tr1)
player.build_connection(tb)
player.build_connection(tb1)
player.build_connection(tb2)
print(player.connections)
routes = [("1", "2", 3), ("1", "3", 5), ("1", "4", 10), ("3", "2", 1), ("4", "5", 3), ("3", "5", 2)]
player.draw_route(routes.pop(random.randint(0, len(routes) - 1)))
print(check_routes(player))