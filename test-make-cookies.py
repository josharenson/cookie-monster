from mock import patch

from make_cookies import (
        Grams,
        Ingredient,
        get_recipe,
        prepare_ingredients
)


@patch('make_cookies.get_recipe_from_arensons_s3_bucket_as_json')
def test_get_recipe_defaults_work_correctly(mock_get_recipe_from_s3_as_json):
    default_recipe = """
    {
        "Paste" : 90
    }
    """
    mock_get_recipe_from_s3_as_json.return_value = default_recipe
    get_recipe()

    mock_get_recipe_from_s3_as_json.assert_called_with(
            'chocolate-chip-cookies')


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
