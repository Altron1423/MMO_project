from dataclasses import dataclass


@dataclass
class AttributeEntityDTO:
    constitution: int = 0
    agility: int = 0
    defense: int = 0
    strength: int = 0
    intellect: int = 0
    spirit: int = 0
    health_reg: int = 0
    max_mana: int = 0

    def __add__(self, other: "AttributeEntityDTO"):
        return AttributeEntityDTO(
            constitution=   self.constitution + other.constitution,
            agility=        self.agility + other.agility,
            defense=        self.defense + other.defense,
            strength=       self.strength + other.strength,
            intellect=      self.intellect + other.intellect,
            spirit=         self.spirit + other.spirit,
            health_reg=     self.health_reg + other.health_reg,
            max_mana=       self.max_mana + other.max_mana
        )

    def __mul__(self, other: "AttributeEntityDTO"):
        return AttributeEntityDTO(
            constitution=   int(self.constitution * other.constitution),
            agility=        int(self.agility * other.agility),
            defense=        int(self.defense * other.defense),
            strength=       int(self.strength * other.strength),
            intellect=      int(self.intellect * other.intellect),
            spirit=         int(self.spirit * other.spirit),
            health_reg=     int(self.health_reg * other.health_reg),
            max_mana=       int(self.max_mana * other.max_mana)
        )
