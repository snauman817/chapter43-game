from sys import exit
import players

map_idea = """
    (0, 0)      (0, 1)      (0, 2)
    _________________________________
    |          |          |          |
    |          |          |          |
    |          |          |          |
    |__________|__________|__________|
    |          |          |          |
    |          |          |          |
    |          |          |          |
    |__________|__________|__________|
    (1, 0)      (1, 1)      (1, 2)
"""

class Scene(object):
    
    def enter(self):
        pass

class Death(Scene):

    def enter(self):
        print("You have died.")
        exit(0)

class Shop(Scene):

    catalog = [
        players.Weapon("Wooden Sword", "The most basic of the swords", 1),
        players.Potion("Health Potion", "Heals 5 HP.", 5)
    ]

    def enter(self):
        print("Welcome to the shop!")
        print("1. Buy")
        print("2. Sell")

        choice = input("> ")

        if choice == 1:
            print("catalog")

class Map(object):

    scenes = {
        'death' : Death(),
        'shop' : Shop(),
        'floor1' : {
            (0, 0) : None, (0, 1) : None, (0, 2) : None,
            (1, 0) : None, (1, 1) : None, (1, 2) : None
        },
        'floor2' : {

        }
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        return Map.scenes.get(scene_name)
    
    def opening_scene(self):
        return self.next_scene(self.start_scene)
    