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
            players.Weapon("Iron Sword", "The most basic of the swords", 70, 4),
            players.Potion("Health Potion", "Heals 5 HP.", 50, 5),
            players.Potion("Health Potion", "Heals 5 HP.", 50, 5)
        ]

    def buy(self, player, item_no):
        item = self.catalog[item_no]
        if player.gold >= item.price:
            print(f"You bought the {item.name} for {item.price} gold.")
            player.get_item(item)
            player.gold -= item.price
            self.catalog.remove(item)
        else:
            print("You do not have enough gold to purchase this item.")

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
                print(f"{count}. {item.name} ({item.price} gold)")
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
        elif choice == 3:
            print("Good seeing you!")
            return 'slime room'

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

            slime = players.Enemy("Slime", 1, 0, 4, players.fist, 60)

            players.combat(player, slime)

            print("You found 30 gold in the slime's remains.")
            player.get_gold(30)

            self.cleared = True
        
        return self.next_room_option()

class TrogRoom(DungeonRoom):

    def __init__(self, name, other_rooms):
        super(TrogRoom, self).__init__(name, other_rooms)

    def enter(self, player):
        if not self.cleared:
            print("A troglodyte, previously blended into the wall, appears and tries to attack you.")

            trog = players.Enemy("Troglodyte", 1, 1, 4, players.fist, 0)

            players.combat(player, trog)

            print("You found 40 gold on the trog's body.")
            player.get_gold(40)

            self.cleared = True
        
        return self.next_room_option()

class ChestRoom(DungeonRoom):

    def __init__(self, name, other_rooms):
        super(ChestRoom, self).__init__(name, other_rooms)

    def enter(self, player):
        if not self.cleared:
            print("You see a chest in the middle of the room.")
            
            print("1. Open the chest")
            print("2. Leave the room")

            choice = int(input("> "))

            if choice == 1:
                print("You open the chest and get one health potion!")
                player.get_item(players.Potion("Health Potion", "Heals 5 HP.", 50, 5))
                self.cleared = True
        
        return self.next_room_option()

class VampireRoom(DungeonRoom):

    def __init__(self, name, other_rooms):
        super(VampireRoom, self).__init__(name, other_rooms)

    def enter(self, player):
        if not self.cleared:
            print("A vampire stands in your way.")

            vampire = players.Enemy('Vampire', 3, 1, 10, players.fist, 40)
            players.combat(player, vampire)
            
            print("You got 70 gold!")
            player.get_gold(70)
            
            self.cleared = True
        
        return self.next_room_option()

class Map(object):

    def __init__(self, start_scene):
        self.start_scene = start_scene
        self.scenes = {
            'death' : Death(),
            'shop' : Shop(),
            'slime room' : SlimeRoom('slime room', ['shop', 'trog room']),
            'trog room' : TrogRoom('trog room', ['slime room', 'chest room', 'vampire room']),
            'chest room' : ChestRoom('chest room', ['trog room']),
            'vampire room' : VampireRoom('vampire room', ['trog room']),
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