"""

Created by: Nathan Starkweather
Created on: 04/16/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'


class Pokemon():
    def __init__(self, type, move, generation, defense):
        self.type = type
        self.move = move
        self.generation = generation
        self.defense = defense


def load_pokemon(type, move, generation, defense):
    return Pokemon(type, move, generation, defense)


def compare_pokemons(pokelist):
    same_attrs = []
    reference = pokelist[0]
    reference_attrs = vars(reference)

    for attr, ref_value in reference_attrs.items():
        if all(getattr(pokemon, attr) == ref_value for pokemon in pokelist):
            same_attrs.append(attr)

    return same_attrs


def compare_pokemons2(pokelist):
    same_attrs = []
    reference = pokelist[0]

    if all(poke.type == reference.type for poke in pokelist):
        same_attrs.append('type')

    if all(poke.move == reference.move for poke in pokelist):
        same_attrs.append('move')

    if all(poke.generation == reference.generation for poke in pokelist):
        same_attrs.append('generation')

    if all(poke.defense == reference.defense for poke in pokelist):
        same_attrs.append('defense')




