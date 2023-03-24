import re
from functools import cache
from operator import attrgetter

number = attrgetter("number")


class Group:
    __pattern = re.compile(
        r"^(?P<number>\d+) units each with (?P<hp>\d+) hit points(?: \((?P<attrs>[^)]+)\))? with an attack that does (?P<damage>\d+) (?P<type>[a-z]+) damage at initiative (?P<initiative>\d+)$"
    )

    def __init__(self, number, hp, damage, type, initiative, weak, immune, army, id):
        self.number = number
        self.hp = hp
        self.damage = damage
        self.type = type
        self.initiative = initiative
        self.weak = weak
        self.immune = immune
        self.army = army
        self.id = id
        self.alive = True
        # Uniquely identify instance for its whole lifetime
        self.__hash__ = lambda: hash(
            (number, hp, damage, type, initiative, weak, immune)
        )

    @staticmethod
    def parse(line):
        result = re.match(__class__.__pattern, line)
        if not result:
            raise ValueError
        data = result.groupdict()
        for field in ("number", "hp", "damage", "initiative"):
            data[field] = int(data[field])
        attributes = data.pop("attrs")
        data["weak"] = frozenset()
        data["immune"] = frozenset()
        if attributes:
            data.update(__class__._parse_attributes(attributes))
        return data

    def __repr__(self):
        return (
            self.number,
            self.hp,
            self.damage,
            self.type,
            self.initiative,
            self.weak,
            self.immune,
            self.army,
            self.id,
        ).__repr__()

    @staticmethod
    def _parse_attributes(attrs):
        attrs = attrs.split("; ")
        result = {"weak": frozenset(), "immune": frozenset()}
        for field in attrs:
            parts = field.split(" ")
            attr = parts[0]
            types = frozenset(word.rstrip(",") for word in parts[2:])
            result[attr] = types
        return result

    # Sustain an attack
    def receive(self, damage):
        # Immune to attack
        self.number -= damage // self.hp
        # All units destroyed
        if self.number <= 0:
            self.alive = False

    @cache
    def casualties(self, type, power):
        return (
            0 if type in self.immune else power if type not in self.weak else 2 * power
        )

    @property
    def power(self):
        return self.number * self.damage

    def bool(self):
        return self.alive


def make_armies(armies, boost=0, boost_army="Immune System"):
    data = {}
    i = 0
    for army in armies:
        army = army.splitlines()
        name = army[0].rstrip(":")
        for group in army[1:]:
            parsed = Group.parse(group)
            parsed.update({"army": name, "id": i})
            if name == boost_army:
                parsed["damage"] += boost
            data[i] = Group(**parsed)
            i += 1

    return data


# Are two armies still on the field?
def both_active(groups):
    prev = None
    for group in groups:
        this = group.army
        if prev and this != prev:
            return True
        prev = this
    return False


# Check if new target has higher priority than best known target
def better_target(previous, candidate, attacker):
    if previous is None:
        return attacker.type not in candidate.immune
    if (
        candidate_casualties := candidate.casualties(attacker.type, attacker.power)
    ) == (previous_casualties := previous.casualties(attacker.type, attacker.power)):
        return candidate.power > previous.power or (
            candidate.power == previous.power
            and candidate.initiative > previous.initiative
        )
    elif candidate_casualties > previous_casualties:
        return True
    else:
        return False


def simulate(combatants):
    while both_active(combatants.values()):
        targeting_order = sorted(
            combatants.items(),
            key=lambda x: (x[1].power, x[1].initiative),
            reverse=True,
        )

        # Attacker : target
        # breakpoint()
        targeted = {}
        for attacker_id, attacker in targeting_order:
            attacker_army = attacker.army
            current_target = None
            # Target choice does account for target weakness/immunity in damage computation
            for defender_id, defender in combatants.items():
                if (
                    defender.army != attacker_army
                    and defender_id not in targeted.values()
                ) and better_target(current_target, defender, attacker):
                    current_target = defender
            if current_target is not None:
                targeted[attacker_id] = current_target.id

        # assert len(targeted.values()) == len(set(targeted.values()))
        attack_order = sorted(
            targeted.items(),
            key=lambda x: combatants[x[0]].initiative,
            reverse=True,
        )

        if not len(attack_order):
            return combatants
        dead = set()
        for attacker_id, defender_id in attack_order:
            if attacker_id in dead:
                continue
            defender = combatants[defender_id]
            attacker = combatants[attacker_id]
            damage = defender.casualties(attacker.type, attacker.power)
            defender.receive(damage)
            if not defender.alive:
                dead.add(defender_id)

        for id in dead:
            combatants.pop(id)

    return combatants


def count_units(army):
    return sum(map(number, army))


def find_boost(armies):
    boost = 1

    while True:
        data = make_armies(armies, boost=boost)
        result = simulate(data)
        for survivor in result.values():
            if survivor.army == "Infection":
                break
        else:
            return count_units(result.values())
        boost += 1


# 15035 too low
# Effective power is damage
# Damage doubled if target weak to attacker's attack type, 0 if immune
# min(attack_strength // unit_hitpoints, n_units) are killed

with open("inputs/day24.txt") as f:
    raw_input = f.read().rstrip("\n")

armies = raw_input.split("\n\n")
data = make_armies(armies)
result = simulate(data)
part1 = count_units(result.values())
print(part1)

part2 = find_boost(armies)
print(part2)
