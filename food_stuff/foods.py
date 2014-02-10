"""

Created by: Nathan Starkweather
Created on: 02/09/2014
Created in: PyCharm Community Edition


"""
from os.path import dirname as path_dirname, exists as path_exists
from json import load as json_load, dump as json_dump, JSONEncoder

__author__ = 'Nathan Starkweather'

__current_path = path_dirname(__file__)
db_file = '/'.join((__current_path, 'foods.json'))


class FoodEncoder(JSONEncoder):
    _default = JSONEncoder.default

    def default(self, o):
        if isinstance(o, Food):
            food = {k : v for k, v in vars(o).items() if not k.startswith("__")}
            food['__classhint'] = "Food"
            return food
        return self._default(o)


class Food():

    """
    Class to represent food.
    """
    cal_per_g_protein = 3.4
    cal_per_g_fat = 9
    cal_per_g_carb = 4
    cal_per_g_alcohol = 2.31 / 0.40  # based on 40% w/v Vodka 231cal per 100g

    def __init__(self,
                name: str,
                serving_size: int,
                serving_cal: float=None,
                protein: float=0,
                carbs: float=0,
                fat: float=0,
                alcohol: float=0):

        """
        @param serving_size: serving size in grams
        @param serving_cal: calories per serving
        @param protein: grams of protein per serving
        @param carbs: grams of carbs per serving
        @param fat: grams of fat per serving
        @param alcohol: grams of alcohol per serving
        """

        self.name = name
        self.serving_size = serving_size
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.alcohol = alcohol

        if serving_cal is None:
            serving_cal = self.macro_to_cal(self.protein,
                                            self.carbs,
                                            self.fat,
                                            self.alcohol)

        self.serving_cal = serving_cal
        self.serving_size = serving_size


    @classmethod
    def from_batch(cls, total_size, **initkwargs):

        serving_size = initkwargs['serving_size']
        scale = total_size / serving_size

        for k, v in initkwargs.items():
            initkwargs[k] = v / scale

        return cls(serving_size=serving_size, **initkwargs)

    def macro_to_cal(self,
                     protein: float=0,
                     carbs: float=0,
                     fat: float=0,
                     alcohol: float=0) -> float:

        protein_cal = self.cal_per_g_protein * protein
        carb_cal = self.cal_per_g_carb * carbs
        fat_cal = self.cal_per_g_fat * fat
        alchol_cal = self.cal_per_g_alcohol * alcohol

        return protein_cal + carb_cal + fat_cal + alchol_cal


def food_hook(o):
    if o.pop('__classhint', None) == "Food":
        return Food(**o)
    else:
        return o



def parse_num(num):
    as_int = int(num)
    as_float = float(num)
    if as_int == as_float:
        return as_int
    else:
        return as_float

def load_database() -> dict:
    if not path_exists(db_file):
        data = {}
    else:
        with open(db_file, 'r') as f:
            data = json_load(f, object_hook=food_hook, parse_int=parse_num)
    return data


def save_database(new: dict) -> None:
    saved = load_database()
    saved.update(new)

    from io import StringIO
    temp = StringIO()

    try:
        # write to temp first in case of errors
        json_dump(saved, temp, cls=FoodEncoder, indent=4, sort_keys=True)
    except:
        raise
    else:
        with open(db_file, 'w') as f:
            f.write(temp.getvalue())


def foods_from_dict(mapping: dict)-> dict:
    """
     Hackily get all foods found in a dict,
     eg globals() or locals()
    """

    foods = {k: v for k, v in mapping.items() if isinstance(v, Food)}
    return foods

Foods = load_database()

if __name__ == '__main__':

    save_database({})







