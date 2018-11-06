from time import sleep

import os


def get_recipe_from_arensons_s3_bucket_as_json(key: str) -> str:
    this_files_dir = dir_path = os.path.dirname(os.path.realpath(__file__))
    recipe_file = os.path.join(this_files_dir, "{}.json".format(key))
    with open(recipe_file, 'r') as fp:
        sleep(10)
        return fp.read()
