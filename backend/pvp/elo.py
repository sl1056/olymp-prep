def calculate_elo(rating1, rating2, result):
    K = 32
    expected1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
    new_rating1 = rating1 + K * (result - expected1)
    new_rating2 = rating2 + K * ((1 - result) - (1 - expected1))
    return round(new_rating1), round(new_rating2)