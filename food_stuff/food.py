"""

Created by: Nathan Starkweather
Created on: 02/17/2014
Created in: PyCharm Community Edition


"""
from weakref import WeakSet


class _FoodMeta(type):
    all_foods = WeakSet()

    def __call__(cls, *args):
        self = super().__call__(*args)
        type(cls).all_foods.add(self)
        return self

FoodMeta = type


class Food(metaclass=FoodMeta):
    """

    Food instance is intended primarily to be a
    data container for a single food. All attributes are
    public, and few methods are available.

    The constructor allows setting abitrary attributes,
    though one could just as easily assign them directly
    to the instance object.

    Ivars:
    @type PyName: str
    @type Name: str
    @type Protein: float
    @type Carbs: float
    @type Alcohol: float
    @type ServingSize: float
    @type ServingCal: float

    Cvars:
    @type cal_per_g_protein: float
    @type cal_per_g_fat: float
    @type cal_per_g_carb: float
    @type cal_per_g_alcohol: float
    """
    cal_per_g_protein = 3.4
    cal_per_g_fat = 9.0
    cal_per_g_carb = 4.0
    cal_per_g_alcohol = 2.31 / 0.40  # based on 40% w/v Vodka 231cal per 100g

    def __init__(self,
                 PyName=None,
                 Name=None,
                 Protein=None,
                 Carbs=None,
                 Alcohol=None,
                 ServingSize=None,
                 ServingCal=None,
                 **kwargs):

        """
        @type PyName: str
        @type Name: str
        @type Protein: float
        @type Carbs: float
        @type Alcohol: float
        @type ServingSize: float
        @type ServingCal: float
        """
        self.ServingCal = ServingCal
        self.ServingSize = ServingSize
        self.Alcohol = Alcohol
        self.Carbs = Carbs
        self.Protein = Protein
        self.PyName = PyName
        self.Name = Name

        for k, v in kwargs.items():
            setattr(self, k, v)
