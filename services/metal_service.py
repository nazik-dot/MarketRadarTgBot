def find_precious_metal(metal: str):
    prices = {
        "gold": 2300,
        "silver": 25,
        "platinum": 900,
        "palladium": 1000
    }

    return prices.get(metal.lower())