from enum import Enum


class PayloadTemplate(Enum):
    TEMPLATE = {
        "EventID": None,
        "DateTime": None,
        "Location": "Miami",
        "Stage": None,
        "Product": None
    }


class Stages(Enum):
    STAGES = [
        'PAYMENT',
        'ORDER TAKEN',
        'ORDER DELIVERED',
        'ORDER MODIFIED'
    ]


class Products(Enum):
    PRODUCTS = [
        'Bread',
        'Fritters',
        'Hamburger',
        'Cheeseburger',
        'Poppers',
        'Zingers',
        'Ham and Cheese',
        'Cheese Pizza',
        'Pepperoni Pizza',
        'Turkey',
        'Salami',
        'Popcorn Chicken',
        'Breast Tenders'
    ]