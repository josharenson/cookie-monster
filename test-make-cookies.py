from make_cookies import (
        Grams,
        Ingredient,
        prepare_ingredients
)


def test_ingredient_validation_can_tokenize_ingredient_names_with_spaces():
    ingredient_names = [
        "Brown Sugar",
        " Opossum",
        "Broken Glass"
    ]

    recipe = dict()
    for ingredient_name in ingredient_names:
        recipe[Ingredient(ingredient_name)] = Grams(5)

    prepare_ingredients(recipe)
