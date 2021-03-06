from sys import exit
import random

class Character(object):

    def __init__(self, name, attack, defense, hp, held_item):
        self.attack = attack
        self.defense = defense
        self.held_item = held_item
        self.hp = hp
        self.max_hp = hp
        self.name = name

class Player(Character):

    def __init__(self, name, attack, defense, hp, held_item, level, xp):
        super(Player, self).__init__(name, attack, defense, hp, held_item)
        self.inventory = []
        self.level = 1
        self.xp = 0
        self.gold = 0

    # adds an item to the inventory
    def get_item(self, item):
        self.inventory.append(item)

    # allows you to select an item from the inventory to use
    def item_selection(self):
        count = 1
        if len(self.inventory) > 0:
            for item in self.inventory:
                print(f"{count}. {item.name}")
                count += 1
            print(f"{count + 1}. Back")
        else:
            print(f"{count}. Back")

        choice = input("> ")

        int_input = int(choice)
        if int_input <= len(self.inventory) and int_input != 0:
            item = self.inventory[int_input - 1]
            item.use(self)
        # this else if is still buggy
        elif int_input == len(self.inventory) + 1:
            pass
        else:
            print("I do not understand.")
            self.item_selection()

    def get_gold(self, amount):
        self.gold += amount

    def combat_choice(self):
        print(" ")
        print("1. Attack")
        print("2. Item")

        choice = input("> ")

        if "1" in choice:
            return 1
        elif "2" in choice:
            return 2
        else:
            print("I didn't understand that.")
            self.combat_choice()
    
    def gain_xp(self, reward_xp):
        print(f"You gained {reward_xp} xp!")
        self.xp += reward_xp
        if self.xp >= 100:
            self.level_up()
    
    def level_up(self):
        self.xp -= 100
        print("You leveled up!")
        print(f"{self.level} > {self.level + 1}")
        self.level += 1

        random_hp = random.randint(1, 5)
        self.max_hp += random_hp
        self.hp += random_hp
        print(f"You gained {random_hp} hp.")

        atk_random = random.randint(0,10)
        if atk_random <= 2:
            print("You gained 0 attack.")
        elif atk_random < 10:
            self.attack += 1
            print("You gained 1 attack.")
        else:
            self.attack += 2
            print("You gained 2 attack.")

        def_random = random.randint(0, 1)
        if def_random == 0:
            print("You gained 0 defense.")
        else:
            self.defense += 1
            print("You gained 1 defense.")


class Enemy(Character):

    def __init__(self, name, attack, defense, hp, held_item, xp):
        super(Enemy, self).__init__(name, attack, defense, hp, held_item)
        self.xp = xp

class Item(object):

    def __init__(self, name, description, price):
        self.price = price
        self.name = name
        self.description = description
    
    def use(self, player):
        print("Use item and remove it from player inventory.")

class Weapon(Item):

    def __init__(self, name, description, price, damage):
        super(Weapon, self).__init__(name, description, price)
        self.damage = damage

class Potion(Item):

    def __init__(self, name, description, price, restoration):
        super(Potion, self).__init__(name, description, price)
        self.restoration = restoration

    def use(self, player):
        print(f"You gained {self.restoration} HP.")
        player.hp += self.restoration
        
        if player.max_hp < player.hp:
            player.hp = player.max_hp

        player.inventory.remove(self)

def attack(attacker, defender):

    damage = attacker.attack + attacker.held_item.damage
    
    if damage > defender.defense:
        defender.hp -= damage
        return damage
    else:
        return 0

def check_death(defender):
    if defender.hp <= 0:
        return False
    else:
        return True

def combat(player, enemy):
    print(f"You have entered combat with {enemy.name}.")
    while check_death(enemy):
        print(" ")
        print("-" * 10)
        print(" ")
        print("It is your turn.")

        choice = player.combat_choice()

        print(" ")

        if choice == 1:
            damage = attack(player, enemy)
            print(f"You dealt {damage} damage.")
        else:
            player.item_selection()
        
        if enemy.hp > 0:
            print(f"{enemy.name} attacks.")
            enemy_damage = attack(enemy, player)
            print(f"{enemy.name} did {enemy_damage} damage.")

            if player.hp <= 0:
                print(f"You died in battle to {enemy.name}")
                exit(0)
    
    print(f"{enemy.name} has been defeated!")
    player.gain_xp(enemy.xp)

def create_player():
    print("Tell me your name.")

    choice = input("> ")

    print(f"Good, then your name is {choice}")
    print("Get ready to embark on an epic journey!")

    print(" ")
    print("-" * 10)
    print(" ")

    if choice == 'Spencer':
        sword = Weapon("Debug Sword", "This is broken", 100, 20)
        return Player(choice, 10, 10, 10, sword, 1, 0)
    else:
        sword = Weapon("Wooden Sword", "A standard wooden sword", 5, 1)
        return Player(choice, 2, 0, 10, sword, 1, 0)

sword = Weapon("Wooden Sword", "A standard wooden sword", 5, 1)
fist = Weapon("Fists", "Just a fist", 0, 0)