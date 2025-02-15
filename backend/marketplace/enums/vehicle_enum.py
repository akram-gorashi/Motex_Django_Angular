from enum import Enum


class BodyType(Enum):
    SEDAN = "Sedan"
    SUV = "SUV"
    TRUCK = "Truck"
    HATCHBACK = "Hatchback"
    COUPE = "Coupe"

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]


class Transmission(Enum):
    AUTOMATIC = "Automatic"
    MANUAL = "Manual"

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]


class FuelType(Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    ELECTRIC = "Electric"

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]


class Condition(Enum):
    NEW = "New"
    USED = "Used"

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]
