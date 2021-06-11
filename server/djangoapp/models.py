from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object  
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='name')
    description = models.CharField(null=False, max_length=100, default='this is a car')
    
    def __str__(self):
        return self.name + " (" + self.description + ")"

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='name')
    dealerId = models.IntegerField(null=False)
    CAR_TYPES = [
        ('SEDAN','sedan'),
        ('SUV','SUV'),
        ('WAGON','wagon')
    ]    
    carType = models.CharField(null=False, max_length=20,choices=CAR_TYPES)
    year = models.DateField(null=True)
    
    # Create a toString method for object string representation
    def __str__(self):
        return self.name + " ("+ self.carType+", "+str(self.year)+")"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, id, sentiment, purchase_date=None, car_make=None, car_model=None, car_year=None):
        self.dealership = dealership
        self.name = name
        self.purchase=purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Review: " + self.review