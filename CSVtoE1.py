import mysql.connector
import pandas as pd

def fill_table(database, table, df):
    try:
        # Connexion à la base de données MySQL
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='isib',
            database=database
        )

        cursor = conn.cursor()

        # Creer la requête SQL qui inserer les données dans la table
        columns = ', '.join(df.columns)
        values_placeholder = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table} ({columns}) VALUES ({values_placeholder})"

        # executemany insère plusieurs lignes d'un coup
        cursor.executemany(insert_query, df.values.tolist())


        # Valider la transaction
        conn.commit()

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

    finally:
        # Fermer le curseur et la connexion
        cursor.close()
        conn.close()


if __name__ == "__main__":
    sales_df = pd.read_csv("vgsales.csv")
    print(sales_df)
    # enlever les n/a
    sales_df.dropna(inplace=True)
    # créer une colonne ID cohérente
    sales_df = sales_df.drop(sales_df.columns[0], axis=1)
    sales_df["ID"] = range(1, len(sales_df) + 1)

    request_create = """CREATE TABLE GAMES (
                        ID             INT,
                        Name            VARCHAR(1000),
                        Platform        VARCHAR(100),
                        Year            INT  not null,
                        Genre           VARCHAR(100),
                        Publisher       VARCHAR(100),
                        NA_Sales        DECIMAL(10,2)  not null,
                        EU_Sales        DECIMAL(10,2)   not null,
                        JP_Sales        DECIMAL(10,2)   not null,
                        Other_Sales     DECIMAL(10,2)   not null,
                        Global_Sales    DECIMAL(10,2)   not null,
                        primary key (ID));"""
    with mysql.connector.connect(host="127.0.0.1", user="root", password="isib", database="sales_games") as mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("drop database if exists sales_games;")
        my_cursor.execute("create database if not exists sales_games;")

        mydb.commit()
    with mysql.connector.connect(host="127.0.0.1", user="root", password="isib", database="sales_games") as mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute(request_create)
        mydb.commit()

    fill_table('sales_games', 'games', sales_df)
















