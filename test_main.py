from engine import calculate_indicators
import pandas as pd

print(calculate_indicators.simple_moving_average(pd.read_csv("data/data.csv", sep=';'), 3, 'Open'))