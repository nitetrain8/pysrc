"""

Created by: Nathan Starkweather
Created on: 02/16/2014
Created in: PyCharm Community Edition


"""
from collections import OrderedDict

from os.path import dirname, exists
import re


__curdir = dirname(__file__)

# This is a human-readable mapping of field names to types
# To write to file, convert from row to column order via
# list(zip(*...))
__base_food_fields = [
                      ('PyName', str),
                      ("Name", str),
                      ("Protein", float),
                      ("Carbs", float),
                      ("Alcohol", float),
                      ("ServingSize", float),
                      ("ServingCal", float)
                      ]


class Food():
    pass


class FoodNutrition():
    pass


def new_foods_csv(csvfile=None, base_fields=__base_food_fields):
    if not csvfile:
        csvfile = __curdir + '/data/foods2.csv'
    fields, types = list(zip(*((name, cls.__name__) for name, cls in base_fields)))
    with open(csvfile, 'w') as f:
        f.write(','.join(types))
        f.write('\n')
        f.write(','.join(fields))
        f.write('\n')
    return csvfile


def get_foods_csv(fpath=__curdir + '/data', make_new=False):
    """
    @param make_new: force re-creation of foods file if it already exists
    @type make_new: bool
    @return: str
    @rtype: str
    """
    if not fpath.endswith('.csv'):
        csvfile = '/'.join((fpath, 'foods.csv'))
    else:
        csvfile = fpath

    if exists(csvfile) and not make_new:
        pass
    else:
        csvfile = new_foods_csv(csvfile)
    return csvfile


__assert_pyname_re = r"([a-zA-Z_][a-zA-Z0-9_]*)"


def assert_pynames(foods, magic_re=__assert_pyname_re, re_match=re.match):
    """
    @param foods: list of foods
    @type foods: list[list[str]]
    @return: None
    @rtype: None

    Perform the double-duty of stripping off newlines
    from the last item in the foods list (side-effect of
    TextIoWrapper.readlines()), and ensuring that a valid
    pyname is present.

    """
    for food in foods:
        food[-1] = food[-1].rstrip('\n')
        pyname = food[1]
        if not pyname or re_match(magic_re, pyname).group(1) != pyname:
            food[1] = name_to_pyname(food[0])


def build_field_map(fnames, ftypes):
    """
    @param fnames: list of field names
    @type fnames: list[str]
    @param ftypes: names of types of fields
    @type ftypes: list[str]
    @return: dict mapping field names to their type
    @rtype: collections.OrderedDict[str, type]
    """

    type_map = __name_type_map
    field_map = OrderedDict()
    for name, typename in zip(fnames, ftypes):
        cls = type_map[typename]
        field_map[name] = cls
    return field_map


def extract_raw_foods(fpath=None):
    """
    @param fpath: filepath to a .csv file with foods
    @type fpath: str
    @return: list
    @rtype: (collections.OrderedDict[str, type], list[list[str]]
    """
    if fpath:
        csvfile = get_foods_csv(fpath)
    else:
        csvfile = get_foods_csv()

    with open(csvfile, 'r') as f:
        ftypes = f.readline().split(",")
        fnames = f.readline().split(",")
        attr_vals = [line.split(',') for line in f]

    ftypes[-1] = ftypes[-1].rstrip('\n')
    fnames[-1] = fnames[-1].rstrip('\n')

    assert_pynames(attr_vals)
    field_map = build_field_map(fnames, ftypes)

    return field_map, attr_vals


def build_food_objects(field_map, foods_list):
    """
    @param field_map: ordered mapping of field names to types
    @type field_map: collections.OrderedDict[str, type]
    @param foods_list: list of foods. each food is a list of attributes in order.
    @type foods_list: list[list[str]]
    @return: dict[str, Food]
    @rtype: dict[str, Food]
    """
    objs = {}
    for food in foods_list:
        new = Food()
        for attr, val in zip(field_map, food):
            ftype = field_map[attr]
            if val:
                setattr(new, attr, ftype(val))
            else:
                setattr(new, attr, ftype())
        objs[new.PyName] = new

    for obj in objs:
        print(objs[obj])
        pass

    return objs


def name_to_pyname_repl(matchobj):
    """
    @param matchobj: match object
    @type matchobj: re.__Match
    @return: str
    @rtype: str
    """
    match = matchobj.group(0)
    if match == "%":
        return "pc"
    else:
        return ''


def name_to_pyname(name, ptrn=r"([^a-zA-Z_0-9]+)", repl=name_to_pyname_repl, sub=re.sub):
    """
    @param name: invalid identifier
    @type name: str
    @return: valid python identifier
    @rtype: str
    """
    pyname = sub(ptrn, repl, name)
    return pyname


def __is_type(obj):
    return isinstance(obj, type)
__name_type_map = {}
__name_type_map.update(globals())
__name_type_map.update(globals()['__builtins__'].__dict__)


if __name__ == '__main__':
    fmap, foods = extract_raw_foods()
    build_food_objects(fmap, foods)
