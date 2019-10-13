"""

Created by: Nathan Starkweather
Created on: 02/17/2014
Created in: PyCharm Community Edition


"""


class Food():
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
                 PyName='',
                 Name='',
                 Protein=0,
                 Carbs=0,
                 Fat=0,
                 Alcohol=0,
                 ServingSize=1,
                 ServingCal=1,
                 **kwargs):

        """
        @type PyName: str
        @type Name: str
        @type Protein: float
        @type Carbs: float
        @type Fat: float
        @type Alcohol: float
        @type ServingSize: float
        @type ServingCal: float
        """
        self.Fat = Fat
        self.ServingCal = ServingCal
        self.ServingSize = ServingSize
        self.Alcohol = Alcohol
        self.Carbs = Carbs
        self.Protein = Protein
        self.PyName = PyName
        self.Name = Name

        for k, v in kwargs.items():
            setattr(self, k, v)

    def CalculateMacroCalories(self):
        """
        Calculate the amount of calories according to the macro
        nutrient content of the food.

        @return: float
        @rtype: float
        """

        protein_cal = self.cal_per_g_protein * self.Protein
        carb_cal = self.cal_per_g_carb * self.Carbs
        fat_cal = self.cal_per_g_fat * self.Fat
        alcohol_cal = self.cal_per_g_alcohol * self.Alcohol

        return sum((protein_cal, carb_cal, fat_cal, alcohol_cal))

    def __repr__(self):
        return '\n'.join("%s = %r" % (k, v) for k, v in self.__dict__.items())
