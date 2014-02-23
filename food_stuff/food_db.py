"""

Created by: Nathan Starkweather
Created on: 02/16/2014
Created in: PyCharm Community Edition

All database-related things for food.
"""
from collections import OrderedDict
from os.path import dirname, exists
import re
from os import makedirs

from pysrc.food_stuff.food import Food


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

food_fields = __base_food_fields.copy()

# mapping of filenames <=> foods
__foods_db_map = {}


def db_write_header(file_obj, base_fields=__base_food_fields):
    """
    @param file_obj: file object supporting 'write' interface
    @type file_obj: _io._TextIOBase
    @param base_fields: fields to write
    @type base_fields: list[(str, type)]
    @return: None
    @rtype: None
    """
    fields, types = list(zip(*((name, cls.__name__) for name, cls in base_fields)))  # row <=> column order
    file_obj.write(','.join(fields))
    file_obj.write('\n')
    file_obj.write(','.join(types))
    file_obj.write('\n')


def db_init_foods(csvfile=None, base_fields=__base_food_fields):
    """
    @param csvfile: file to create or modify
    @type csvfile: str
    @param base_fields: list of fields to write
    @type base_fields: list[(str, type)]
    @return:
    @rtype:
    """
    if not csvfile:
        csvfile = __curdir + '/data/foods.csv'

    file_dir = dirname(csvfile)
    if not exists(file_dir):
        makedirs(file_dir)
    with open(csvfile, 'w') as f:
        db_write_header(f, base_fields)
    return csvfile


def get_foods_csv(fpath=None, make_new=False):
    """
    @param make_new: force re-creation of foods file if it already exists
    @type make_new: bool
    @return: str
    @rtype: str

    Get the csv file. If it doesn't currently exist,
    create it.
    """

    if fpath is None:
        fpath = __curdir + '/data'

    if not fpath.endswith('.csv'):
        csvfile = '/'.join((fpath, 'foods.csv'))
    else:
        csvfile = fpath

    if exists(csvfile) and not make_new:
        pass
    else:
        csvfile = db_init_foods(csvfile)
    return csvfile


__assert_pyname_re = r"([a-zA-Z_][a-zA-Z0-9_]*)"


def assert_pynames(foods, valid_id=__assert_pyname_re, re_match=re.match):
    """
    @param foods: list of foods
    @type foods: list[list[str]]
    @return: None
    @rtype: None

    Ensure that a valid pyname is present.

    Modifies list in place.
    """
    food_len = len(foods[0])
    for food in foods:
        assert len(food) == food_len, "Mal-formed data file"
        pyname = food[1]

        # if pyname is not a valid python identifier, obliterate it.
        if not pyname or re_match(valid_id, pyname).group(1) != pyname:
            food[1] = name_to_pyname(food[0])


def build_field_map(fnames, ftypes):
    """
    @param fnames: list of field names
    @type fnames: list[str]
    @param ftypes: names of types of fields
    @type ftypes: list[str]
    @return: dict mapping field names to their type
    @rtype: collections.OrderedDict[str, type]

    When the db file is imported, the first row contains a list
    of types corresponding to the python type of the contents
    of that column.

    This function parses that header, and builts a mapping of
    names to classes to use to initialize fields to their proper type.
    eg "str" -> str, call str(foo)
    """

    type_map = {
        "str": str,
        "float": float,
        "int": int
    }
    field_map = OrderedDict()
    for name, typename in zip(fnames, ftypes):
        cls = type_map[typename]
        field_map[name] = cls
    return field_map


def load_raw_csv(csvfile):
    """
    @param csvfile: file to open
    @type csvfile: str
    @return: tuple of attr values, field names, and field types
    @rtype: (list[list[str]], list[str], list[str])
    """
    with open(csvfile, 'r') as f:
        fnames = f.readline().split(",")
        ftypes = f.readline().split(",")
        attr_vals = [line.split(',') for line in f]
    ftypes[-1] = ftypes[-1].rstrip('\n')
    fnames[-1] = fnames[-1].rstrip('\n')

    for line in attr_vals:
        line[-1] = line[-1].rstrip('\n')

    return attr_vals, fnames, ftypes


def extract_raw_foods(fpath=None):
    """
    @param fpath: filepath to a .csv file with foods
    @type fpath: str
    @return: list
    @rtype: (collections.OrderedDict[str, type], list[list[str]]
    """

    csvfile = get_foods_csv(fpath)

    attr_vals, fnames, ftypes = load_raw_csv(csvfile)

    assert_pynames(attr_vals)
    field_map = build_field_map(fnames, ftypes)

    assert len(field_map) == len(attr_vals[0]), "Mal-formed data file"

    return field_map, attr_vals


def build_food_objects(field_map, foods_list):
    """
    @param field_map: ordered mapping of field names for the Food instance to types.
    @type field_map: collections.OrderedDict[str, type]
    @param foods_list: list of foods. each food is a list of attributes in order.
    @type foods_list: list[list[str]]
    @return: dict[str, Food]
    @rtype: collections.OrderedDict[str, pysrc.food_stuff.food.Food]
    """
    objs = OrderedDict()
    for food in foods_list:
        new = Food()
        for attr, val in zip(field_map, food):
            field_type = field_map[attr]
            if val:
                setattr(new, attr, field_type(val))
            else:
                setattr(new, attr, field_type())
        objs[new.PyName] = new

    assert len(foods_list) == len(objs), "Warning! Overlapping PyNames!"

    return objs


def name_to_pyname_repl(matchobj):
    """
    @param matchobj: match object
    @type matchobj: re.__Match
    @return: str
    @rtype: str

    Helper function for name_to_pyname
    act as repl parameter for re.sub()
    """
    match = matchobj.group(0)
    if "%" in match:
        return "pc"
    else:
        return ''


def save_db(foods, file=None, fields=__base_food_fields):
    """

    @param foods: list of foods
    @type foods: dict[str, pysrc.food_stuff.food.Food]
    @type fields: list[(str, type)]
    @return: None
    @rtype: None
    """

    if file is None:
        file = get_foods_csv()

    food_list = []
    for food in foods.values():
        food_ctxt = [str(getattr(food, attr, '')) for attr, _ in fields]
        food_list.append(food_ctxt)

    with open(file, 'w') as f:
        db_write_header(f, fields)
        for food in food_list:
            f.write(','.join(food))
            f.write('\n')


def name_to_pyname(name, ptrn=r"(^[^a-zA-Z_]+|[^a-zA-Z_0-9]*)", repl=name_to_pyname_repl, sub=re.sub):
    """
    @param name: invalid identifier
    @type name: str
    @return: valid python identifier
    @rtype: str
    """
    pyname = sub(ptrn, repl, name)
    return pyname


def _inject_foods(foods, mapping):
    """
    @param foods: foods to inject
    @type foods: collections.Mapping[str, Food]
    @param mapping: objet to inject into
    @type mapping: collections.MutableMapping
    @return: None
    @rtype: None
    """
    mapping.update(foods)


def inject_main():
    """
    Hack do not use!

    @return:
    @rtype:
    """
    import sys
    if __foods_db_map:
        for Foods in __foods_db_map.values():
            sys.modules['__main__'].__dict__.update(Foods)


def extract_db_foods(fpath=None):
    """
    @return: Extract all of the foods from the database
    @rtype: collections.OrderedDict[str, Food]
    """
    db_file = get_foods_csv(fpath)
    fmap, foods = extract_raw_foods(db_file)
    foods = build_food_objects(fmap, foods)

    __foods_db_map[fpath] = foods.copy()

    return foods

# Foods = extract_db_foods()


def __save_bkup_cache():
    """
    @return: None
    @rtype: None

    just in case user(me) is dumb,
    have a backup pickle cache that always
    saves the last foods dict.
    """
    from pysrc.snippets import safe_pickle
    pickle_bkup = __curdir + "/data/bkup_cache.pickle"
    safe_pickle(__foods_db_map, pickle_bkup)

from atexit import register
register(__save_bkup_cache)


if __name__ == '__main__':
    dbg = "C:\\Users\\Administrator\\Documents\\Programming\\python\\pysrc\\food_stuff\\data\\foods2.csv"
    foods = extract_db_foods(dbg)
    save_db(foods)
