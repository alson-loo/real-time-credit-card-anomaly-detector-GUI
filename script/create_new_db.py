import sqlite3
import pandas as pd

# import dataset into dataframe
df = pd.read_csv(r'./data/creditcard.csv')
df.insert(30, 'CheckBy', 'startnew')

# extract column names for sqlite script
create_table='CREATE TABLE IF NOT EXISTS transactions (id integer PRIMARY KEY '
table_names=''
for i, col_name in enumerate(df):
    if df[col_name].dtypes == 'float64':
        table_names += (',' + col_name + ' REAL')
    elif df[col_name].dtypes == 'int64':
        table_names += (',' + col_name + ' INTEGER')
    elif df[col_name].dtypes == 'object':
        table_names += (',' + col_name + ' TEXT')
create_table = create_table + table_names + ')'
print(create_table)

# Create table and database
con = sqlite3.Connection(r'./data/creditcard.db')
cur = con.cursor()
con.execute("PRAGMA journal_mode=WAL")
cur.execute(create_table)

# insert dataframe into sqlite database
df.to_sql("transactions", con, if_exists='append', index=False)
con.close()
