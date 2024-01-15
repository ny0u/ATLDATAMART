import gc
import os
import sys

import pandas as pd
from sqlalchemy import create_engine

from minio import Minio
from io import BytesIO

def write_data_postgres(dataframe: pd.DataFrame) -> bool:
    """
    Dumps a Dataframe to the DBMS engine

    Parameters:
        - dataframe (pd.Dataframe) : The dataframe to dump into the DBMS engine

    Returns:
        - bool : True if the connection to the DBMS and the dump to the DBMS is successful, False if either
        execution is failed
    """
    db_config = {
        "dbms_engine": "postgresql",
        "dbms_username": "postgres",
        "dbms_password": "admin",
        "dbms_ip": "localhost",
        "dbms_port": "5432",
        "dbms_database": "nyc_db",
        "dbms_table": "nyc_tab"
    }

    db_config["database_url"] = (
        f"{db_config['dbms_engine']}://{db_config['dbms_username']}:{db_config['dbms_password']}@"
        f"{db_config['dbms_ip']}:{db_config['dbms_port']}/{db_config['dbms_database']}"
    )
    try:
        engine = create_engine(db_config["database_url"])
        with engine.connect():
            success: bool = True
            print("Connection successful! Processing parquet file")
            dataframe.to_sql(db_config["dbms_table"], engine, index=False, if_exists='append')

    except Exception as e:
        success: bool = False
        print(f"Error connection to the database: {e}")
        return success

    return success


def clean_column_name(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Take a Dataframe and rewrite it columns into a lowercase format.
    Parameters:
        - dataframe (pd.DataFrame) : The dataframe columns to change

    Returns:
        - pd.Dataframe : The changed Dataframe into lowercase format
    """
    dataframe.columns = map(str.lower, dataframe.columns)
    return dataframe





    """
    Télécharge les fichiers Parquet depuis un bucket MinIO spécifique.

    Paramètres :
        bucket_name (str) : Le nom du bucket MinIO d'où télécharger les fichiers.
        minio_client (Minio) : Le client MinIO configuré.
        limit (int) : Nombre maximal de fichiers à télécharger.

    Retourne :
        Génère des DataFrames un par un.
    """
def download_from_minio(bucket_name, minio_client, limit=1):

    count = 0
    objects = minio_client.list_objects(bucket_name)

    for obj in objects:
        if count >= limit:
            break
        if obj.object_name.endswith('.parquet'):
            response = minio_client.get_object(bucket_name, obj.object_name)
            data = BytesIO(response.read())
            df = pd.read_parquet(data, engine='pyarrow')
            yield df
            count += 1

def main() -> None:

    minio_client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    bucket_name = "bigbucket"

    for parquet_df in download_from_minio(bucket_name, minio_client, limit=1):

        parquet_df = parquet_df.head(100)
        clean_column_name(parquet_df)
        if not write_data_postgres(parquet_df):
            del parquet_df
            gc.collect()
            print("Erreur du chargement des données.")
            continue

            del parquet_df
    gc.collect()
    print("Chargement avec succés dans la BDD.")

if __name__ == '__main__':
    sys.exit(main())
    