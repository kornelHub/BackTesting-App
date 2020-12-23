import calculate_indicators
import pandas as pd

print(calculate_indicators.weighted_moving_average(pd.read_csv("data/data.csv", sep=';'), 2, 'Open'))
