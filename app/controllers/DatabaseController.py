import pyodbc
import pandas as pd
import numpy as np
from hashlib import sha256
import time
from app.controllers.AIController import AIController
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('mode.chained_assignment', None)

from functools import wraps
import hashlib
from cache_to_disk import cache_to_disk

cache = {}

import time

def execution_time(func):
  """Decorator that prints the execution time of a function."""
  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_seconds = end_time - start_time
    print(f"Function '{func.__name__}' took {execution_seconds:.4f} seconds to execute.")
    return result
  return wrapper

def clear_cache():
    global cache
    cache.clear()

def cache_in_memory():
  global cache

  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      # Combine args and kwargs into a single tuple for hashing
      hash_key = hashlib.sha256(str(args[1]).encode()).hexdigest()

      if hash_key in cache:
        # Cache hit, return cached value
        print(f"Cache hit {hash_key}")
        return cache[hash_key]
      else:
        # Cache miss, execute function and store result
        result = func(*args, **kwargs)
        cache[hash_key] = result
        return result

    return wrapper

  return decorator

class DatabaseController():

    @staticmethod
    def build_sql_where_clause(filter_list):

        if not filter_list:
            return None

        where_clause = []

        for item in filter_list:
            if isinstance(item, dict):
            # Field and value pair
                field = item["f"]
                value = item["c"]
                where_clause.append(f"{field} = '{value}'")
            elif item == "and":
                where_clause.append("AND")
            elif item == "or":
                where_clause.append("OR")
            else:
                raise ValueError(f"Invalid filter element: {item}")

        return f"WHERE {' '.join(where_clause)}", filter_list[0]["f"]

    #Retorna dados do zenith por codigo do talhao (stand number)
    @staticmethod
    @execution_time
    @cache_to_disk(1)
    def get_data_zenith(view_name, where):

        # Example usage (replace with your own connection details)
        username = "sa"
        password = "p@55word"
        server = "10.20.84.25"
        view_name = view_name #"CADVWSTAND"
        database = "ZENITH_PRODUCTION"
        
        connection = None
        cursor = None
        try:
            connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"
            connection = pyodbc.connect(connection_string)
            query = f"SELECT * FROM {view_name} {where}"

            data = pd.read_sql(query, connection)
            return data

        except pyodbc.Error as error:
            print(f"Error connecting to Oracle database: {error}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return None

    @staticmethod
    @execution_time
    def parse_datetime(df):
        import pandas
        for column in df.columns:
            if pandas.api.types.is_datetime64_any_dtype(df[column]):
                df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')

        return df

    @staticmethod
    @execution_time
    def clean_data(dataf):
        # Clear the data, remove Nan numbers and convert datetime
        data = dataf.fillna(np.nan).replace([np.nan], [None])

        def format_id(item):
            return item.lstrip('0')


        # Preprocess data once outside the loop (assuming clean_data is defined)
        data.loc[:, 'STANDNUMBER'] = data['STANDNUMBER'].apply(format_id)


        return data

    @staticmethod
    def process_feature(args):
        feature, clean_data  = args

        matching_row = clean_data.loc[clean_data["STANDNUMBER"] == feature["properties"]["CD_TALHAO"]]

        # Access matching row data directly
        row_data = matching_row.loc[matching_row['LASTUPDATE'] == matching_row['LASTUPDATE'].max()]

        if not row_data.empty:
            from concurrent.futures import ThreadPoolExecutor
            from concurrent.futures import as_completed

            def create_dict(row):
                return row.to_dict()

            new_dict = {}
            with ThreadPoolExecutor() as executor:
                # Submit tasks to the executor using `executor.submit(function, *args, **kwargs)`
                futures = []
                for index, row in row_data.iterrows():
                    futures.append(executor.submit(create_dict, row))

                for future in as_completed(futures):
                    new_dict.update(future.result())

            feature["properties"].update(new_dict)
            return feature

    @staticmethod
    @execution_time
    @cache_in_memory()
    def data_to_geojson(geojson, query, view_name):

        # Extract data for efficiency
        data = DatabaseController.get_data_zenith(view_name, query)
        data = DatabaseController.parse_datetime(data)

        #Limpa os dados
        clean_data = DatabaseController.clean_data(data)

        #Carregar o dataframe para o agent de IA
        AIController.load_dataframe(clean_data)

        #Lista para guardar as features com os dados do Zenith
        new_features = []

        def yield_data():

            features = geojson.data['features']
            for f in features:
                yield f,clean_data
        
        from multiprocessing import Pool
        with Pool(4) as p:
            features = p.map(DatabaseController.process_feature, yield_data())
            new_features = [f for f in features if f]

        return new_features
