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
        super(Player, self).__init__(attack, name, defense, hp, held_item)
        self.inventory = {'1' : None, '2' : None, '3' : None}
        self.level = 1
        self.xp = 0

    def use_item(self, item):
        if item in self.inventory:
            self.inventory.pop(item)

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
        super(Enemy, self).__init__(attack, name, defense, hp, held_item)
        self.xp = xp

class Item(object):

    def __init__(self, function, description):
        self.function = function
        self.description = description

class Weapon(Item):

    def __init__(self, function, description, damage):
        super(Weapon, self).__init__(function, description)
        self.damage = damage

# class Potion(Item):

#     def __init__(self, function, description):
#         super(Potion, self).__init__(function, description)

#     def consume(self, player):
#         player.hp += self.function


def attack(attacker, defender):
    damage = attacker.attack
    
    if damage > defender.defense:
        defender.hp -= damage
        print(f"You dealt {damage} damage.")
    else:
        print("You dealt no damage.")

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

        if choice == 1:
            attack(player, enemy)
        else:
            print("Use item")
        
        if enemy.hp > 0:
            print(f"{enemy.name} attacks.")
            attack(enemy, player)

            if player.hp <= 0:
                print(f"You died in battle to {enemy.name}")
    
    player.gain_xp(enemy.xp)

sword = Weapon("do thing", "A standard wooden sword", 1)
fist = Weapon("punch person", "Just a fist", 0)   
p1 = Player("Jacob", 2, 0, 10, sword, 1, 0)
e1 = Enemy("Slime", 1, 0, 4, fist, 30)

combat(p1, e1)