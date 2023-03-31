import pandas as pd
from preprocessor import Preprocessor

df = pd.read_csv('./universities.csv')

preprocessor = Preprocessor(df)
print("*****************************************\n")
print(df['extracted_keywords'].tolist())