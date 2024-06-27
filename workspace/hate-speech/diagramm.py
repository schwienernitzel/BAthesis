import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

csv_file = 'out/hate-clean-test.csv'

df = pd.read_csv(csv_file, delimiter='\t')

print(df.head())