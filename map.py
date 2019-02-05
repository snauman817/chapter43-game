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
        print(f"You bought the {item.name}")

        player.get_item(item)

        self.catalog.remove(item)

    def enter(self, player):
        print("Welcome to the shop!")
        print("1. Buy")
        print("2. Sell")
        print("3. Leave")

        choice = int(input("> "))

        if choice == 1:
            print("What would you like to buy?")
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

class DungeonRoom(Scene):

    def __init__(self, name, other_rooms):
        self.name = name
        self.other_rooms = other_rooms
        self.cleared = False
        self.entrance = False
        self.exit = False
    
    def enter(self, player):
        if self.cleared:
            print("You have already cleared this room.")
        else:
            # actually write specifics
            print("Combat will start then.")
        
        if self.entrance:
            # will do this eventually
            print("Go to shop.")
        elif self.exit:
            # eventually as well
            print("Go down a floor.")
    
    def next_room_option(self):
        count = 1
        for room in self.other_rooms:
            print(f"{count}. {room}")
            count += 1
        
        choice = int(input("> "))

        if choice <= len(self.other_rooms):
            return self.other_rooms[choice - 1]

class SlimeRoom(DungeonRoom):

    def __init__(self, name, other_rooms):
        super(SlimeRoom, self).__init__(name, other_rooms)
    
    def enter(self, player):
        if not self.cleared:
            print("This room has only a slime, but it wants to fight.")

            slime = players.Enemy("Slime", 1, 0, 4, players.fist, 30)

            players.combat(player, slime)

            print("You found 30 gold in the slime's remains.")
            player.get_gold(30)

            self.cleared = True
        
        return self.next_room_option()

class Map(object):

    def __init__(self, start_scene):
        self.start_scene = start_scene
        self.scenes = {
            'death' : Death(),
            'shop' : Shop(),
            'slime room' : SlimeRoom('slime room', ['death', 'shop']),
            'floor1' : {
                (0, 0) : {
                    'room options' : [(0, 1), (1, 0)], 
                    'cleared' : False, 
                    'encounter' : None,
                    'entrance' : False,
                    'exit' : False
                },
                (0, 1) : {
                    'room options' : [(0, 0), (0, 2), (1, 1)], 
                    'cleared' : False, 
                    'encounter' : None,
                    'entrance' : False,
                    'exit' : False
                },
                (0, 2) : {
                    'room options' : [(0, 1), (1, 2)], 
                    'cleared' : False, 
                    'encounter' : None,
                    'entrance' : False,
                    'exit' : False
                },
                (1, 0) : {
                    'room options' : [(0, 0), (1, 1)], 
                    'cleared' : False, 
                    'encounter' : None,
                    'entrance' : False,
                    'exit' : False
                },
                (1, 1) : {
                    'room options' : [(1, 0), (1, 2), (0, 1)], 
                    'cleared' : False, 
                    'encounter' : None,
                    'entrance' : False,
                    'exit' : False
                },
                (1, 2) : {
                    'room options' : [(1, 1), (0, 2)], 
                    'cleared' : False, 
                    'encounter' : None,
                    'entrance' : False,
                    'exit' : False
                }
            },
            'floor2' : {

            }
        }
        self.player = players.create_player()

    def next_scene(self, scene_name):
        return self.scenes.get(scene_name)
    
    def opening_scene(self):
        return self.next_scene(self.start_scene)