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
    
    def enter(self, player):
        pass

class Death(Scene):

    def enter(self, player):
        print("You have died.")
        exit(0)

class Shop(Scene):

    def __init__(self):
        self.catalog = [
            players.Weapon("Wooden Sword", "The most basic of the swords", 1),
            players.Potion("Health Potion", "Heals 5 HP.", 5)
        ]

    def buy(self, player, item_no):
        item = self.catalog[item_no]
        print(item.name)

        player.get_item(item)

    def enter(self, player):
        print("Welcome to the shop!")
        print("1. Buy")
        print("2. Sell")
        print("3. Leave")

        choice = int(input("> "))

        if choice == 1:
            count = 1
            for item in self.catalog:
                print(f"{count}. {item.name}")
                count += 1
            print(f"{count}. Back")

            item_to_buy = int(input("> "))
            if item_to_buy == len(self.catalog) + 1:
                self.enter(player)
            else:
                self.buy(player, item_to_buy - 1)
                self.enter(player)
        elif choice == 2:
            print("This function will be added later.")
            self.enter(player)
        else:
            print("Good seeing you!")
            # just a placeholder for now
            return 'death'

class Map(object):

    player = players.create_player()

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
    