
# Importation de la bibliothèque pandas
import pandas as pd

# URL du fichier Parquet à télécharger
parquet_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"

# Lecture du fichier Parquet dans un DataFrame pandas
df = pd.read_parquet(parquet_url)

# Affichage de la liste des colonnes du DataFrame
print("Liste des colonnes du DataFrame :")
print(df.columns.tolist())

# Affichage des types de données de chaque colonne
print("\nTypes de données des colonnes :")
print(df.dtypes)

# Affichage des premières lignes du DataFrame
print("\nAperçu des premières lignes du DataFrame :")
print(df.head())