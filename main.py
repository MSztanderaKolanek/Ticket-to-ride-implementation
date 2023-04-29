from Player import Player
import random

# Initializing environment, drawing routes

routes = [("1", "2"), ("1", "3"), ("1", "4"), ("3", "2"), ("4", "5"), ("3", "5")]
player1 = Player()
player2 = Player()
player1.draw_route(routes.pop(random.randint(0, 5)))
player2.draw_route(routes.pop(random.randint(0, 5)))
