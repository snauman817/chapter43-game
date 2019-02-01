class Character(object):

    def __init__(self, attack, defense, hp, held_item):
        self.attack = attack
        self.defense = defense
        self.held_item = held_item
        self.hp = hp
        self.max_hp = hp

class Player(Character):

    def __init__(self, attack, defense, hp, held_item):
        super(Player, self).__init__(attack, defense, hp, held_item)
        self.inventory = {'1' : None, '2' : None, '3' : None}

    def use_item(self, item):
        if item in self.inventory:
            self.inventory.pop(item)

class Enemy(Character):

    def __init__(self, attack, defense, hp, held_item):
        super(Enemy, self).__init__(attack, defense, hp, held_item)


def attack(attacker, defender):
    damage = attacker.attack + attacker.held_item.damage
    
    if damage > defender.defense:
        defender.hp -= damage