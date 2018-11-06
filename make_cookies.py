#!/usr/bin/env python3

# External imports
from typing import Dict, NewType

import errno
import json
import subprocess
import sys

# Internal imports
from make_the_demo.go_faster import get_recipe_from_arensons_s3_bucket_as_json


STANDARD_COOKIE_WEIGHT_G = 20
WORDS_FILE = "/usr/share/dict/words"

Grams = NewType('Grams', int)
Ingredient = NewType('Ingredient', str)

Dough = Grams
Recipe = Dict[Ingredient, Grams]


def bake(num_cookies):
    pass


def divide_dough(dough: Dough) -> int:
    """
    Take the floor of the fraction of cookies we can make. While this could
    return the fraction, that wouldn't leave us any raw cookie dough to eat
    which kind of defeats the purpose of baking cookies.
    """

    return dough // STANDARD_COOKIE_WEIGHT_G


def get_recipe(recipe_name: str='chocolate-chip-cookies') -> Recipe:
    """
    Fetch the recipe called `recipe_name` from Josh's S3 bucket.
    """

    recipe_json = get_recipe_from_arensons_s3_bucket_as_json(recipe_name)
    recipe_dict = json.loads(recipe_json)

    result = dict()
    for ingredient, grams in recipe_dict.items():
        result[Ingredient(ingredient)] = Grams(grams)
    return result


def prepare_ingredients(recipe: Recipe) -> Dough:
    """
    Validate ingredients and calculate the total weight of the recipe

    Each word of every ingredient is checked to ensure it is a known english
    word. While this technically would allow for a recipe to call for
    "Poison Acid", it is good enough for our unrefined tastes.
    """

    weight_g = Grams(0)
    for ingredient, grams in recipe.items():
        for token in ingredient.split():
            cmd = ["grep", "-i", token, WORDS_FILE]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print("{} is not a valid ingredient!".format(ingredient))
                sys.exit(errno.ENOENT)
        weight_g += grams
    return Dough(weight_g)


if __name__ == '__main__':
    # Yes, I realize there is no error checking here
    print()
    recipe_name = sys.argv[1]

    print("Downloading {} recipe from S3....".format(recipe_name))
    recipe = get_recipe(recipe_name)

    print("Validating ingredient list and calculating weight....")
    dough = prepare_ingredients(recipe)

    print("Calculating the number of cookies to bake....")
    num_cookies = divide_dough(dough)

    print("Baking {} cookies".format(num_cookies))
    bake(num_cookies)

    print("Bon Appétit!")
