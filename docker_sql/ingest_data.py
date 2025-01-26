import argparse
from time import time
import os
from sqlalchemy import create_engine
import pandas as pd


def parse_dates(df, date_cols):
    if date_cols is not None:
        df[date_cols] = df[date_cols].apply(pd.to_datetime)
    return df

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    date_cols = None
    csv_name = 'output.csv'
    os.system(f'wget {url} -O {csv_name}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    if 'tripdata' in os.path.split(url)[-1]:
        date_cols = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]

    compression = 'gzip' if url.lower().endswith('.gz') else 'infer'
    df_iter = pd.read_csv(csv_name, iterator=True, 
                          chunksize=100000, compression = compression)
    df = next(df_iter)
    df = parse_dates(df, date_cols)
    df.head(0).to_sql(name = table_name, con=engine, if_exists='replace')
    t_start = time()

    while True:
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print('Inserted another chunk. Took {:.3f} seconds'.format(t_end - t_start))
        t_start = time()
        df = next(df_iter)
        df = parse_dates(df, date_cols)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data into Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password name for postgres')
    parser.add_argument('--host', help='host name for postgres')
    parser.add_argument('--port', help='port name for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args=parser.parse_args()
    main(args)
    