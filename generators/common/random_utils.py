import random
from datetime import date, timedelta

DEFAULT_SEED = 42

def get_rng(seed: int = DEFAULT_SEED) -> random.Random:
    return random.Random(seed)

def random_date(rng: random.Random, start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=rng.randint(0, delta))

def choice_weighted(rng: random.Random, values, weights):
    return rng.choices(values, weights=weights, k=1)[0]
