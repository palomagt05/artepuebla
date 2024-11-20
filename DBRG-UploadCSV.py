import pandas as pd
import mysql.connector
from abc import ABC, abstractmethod

# Clase abstracta para la conexión a la base de datos
class DBConnection(ABC):

    @abstractmethod
    def connect(self):
        pass

# Clase concreta que implementa la conexión a MySQL
class MySQLConnection(DBConnection):

    def connect(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="prueba01"
        )

# Clase abstracta para el cargador de datos
class DataLoader(ABC):

    @abstractmethod
    def load_data(self, file_path):
        pass

# Clase concreta que implementa el cargador de datos para CSV a MySQL
class CSVToMySQLLoader(DataLoader):

    def __init__(self, db_connection: DBConnection):
        self.connection = db_connection.connect()

    def load_data(self, file_path):
        data = pd.read_csv(file_path)
        cursor = self.connection.cursor()

        for _, row in data.iterrows():
            cursor.execute("""
                INSERT INTO eventos (NAME_EVENT, TYPE_EVENT_ID, START_DATE, END_DATE, START_TIME, END_TIME, ADDRESS, PLACE, COST, PUBLIC_TYPE_ID, DESCRIPTION_EVENT)
                VALUES (%s, (SELECT ID FROM type_event WHERE TYPE_EVENTO = %s), %s, %s, %s, %s, %s, %s, %s, (SELECT ID_PUBLIC FROM type_public WHERE TYPE_PUBLIC = %s), %s)
            """, (
                row['NAME_EVENT'],
                row['TYPE_EVENT'],
                row['START_DATE'],
                row['END_DATE'],
                row['START_TIME'],
                row['END_TIME'],
                row['ADDRESS'],
                row['PLACE'],
                row['COST'],
                row['TYPE_PUBLIC'],
                row['DESCRIPTION_EVENT']
            ))
        
        self.connection.commit()
        cursor.close()
        self.connection.close()

# Factory Method para crear la conexión y cargar los datos
class DataLoaderFactory:

    @staticmethod
    def get_data_loader(loader_type: str, db_type: str) -> DataLoader:
        if db_type == "mysql":
            db_connection = MySQLConnection()
        
        if loader_type == "csv":
            return CSVToMySQLLoader(db_connection)

        raise ValueError(f"Unsupported loader type: {loader_type} or db type: {db_type}")

if __name__ == "__main__":
    file_path = "/home/derek/Escritorio/Dataset-ArtePuebla-Eventos-Nov2024.csv"
    data_loader = DataLoaderFactory.get_data_loader("csv", "mysql")
    data_loader.load_data(file_path)
    print("Datos cargados exitosamente a la base de datos.")

