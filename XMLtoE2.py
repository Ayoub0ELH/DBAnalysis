import xml.etree.ElementTree as ET
import mysql.connector
platform_list = []
# Charger le fichier XML
tree = ET.parse("game_list.xml")

root = tree.getroot()


# Établir une connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="isib",
    port=3307,
    database="sales_games_final"
)

# Créer un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()
cursor.execute("drop database if exists sales_games_final;")
cursor.execute("create database if not exists sales_games_final;")
cursor.execute("Use sales_games_final")
create_t2 = """CREATE TABLE PLATFORM (
                        Platform_ID     INT UNIQUE,
                        Platform        VARCHAR(100) UNIQUE,
                        primary key     (Platform_ID));"""
create_t1 = """CREATE TABLE GAMES (
                        ID             INT AUTO_INCREMENT,
                        Name            VARCHAR(1000),
                        Platform_ID               INT,
                        FOREIGN KEY (Platform_ID) REFERENCES PLATFORM(Platform_ID),
                        Year            INT  not null,
                        Genre           VARCHAR(100),
                        Publisher       VARCHAR(100),
                        NA_Sales        DECIMAL(10,2)  not null,
                        EU_Sales        DECIMAL(10,2)   not null,
                        JP_Sales        DECIMAL(10,2)   not null,
                        Other_Sales     DECIMAL(10,2)   not null,
                        Global_Sales    DECIMAL(10,2)   not null,
                        primary key (ID));"""
cursor.execute(create_t2)
cursor.execute(create_t1)
cursor.execute("ALTER TABLE GAMES MODIFY Name VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
#la colonne ne prenait pas en charge certains caractères

cursor.close()
conn.close()

# retoruve chaque jeu
for game in root.findall("game"):
    # Extraire les données de chaque élément "record"
    id = game.find("ID").text
    name = game.find("Name").text
    platform = game.find("Platform").text
    # if platform not in platform_list:
    # platform_list.append(platform)
    year = game.find("Year").text
    genre = game.find("Genre").text
    publisher = game.find("Publisher").text
    sales_element = game.find('.//Sales')
    if sales_element is not None:
        north_america_sales = sales_element.attrib.get('North_America')

        europe_sales = sales_element.attrib.get('Europe')

        japan_sales = sales_element.attrib.get('Japan')

        other_sales = sales_element.attrib.get('Other')

        global_sales = sales_element.attrib.get('Global')


    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="isib",
        database="sales_games_final",
        port=3307
    )
    cursor = conn.cursor()
    # Insère les données dans la 2e table de donnée
    find_max_id = f"SELECT MAX(Platform_ID) FROM Platform"
    cursor.execute(find_max_id)
    max_id = cursor.fetchone()[0]

    if max_id is not None:
        new_id = max_id + 1
    else:  # Au debut il y a 0 id
        new_id = 1
    request_insert_t1 = """INSERT IGNORE INTO platform (Platform_ID, Platform) VALUES (%s, %s)"""
    data1 = (new_id, platform)
    cursor.execute(request_insert_t1, data1)
    request_search = f"SELECT Platform_ID FROM platform WHERE Platform = '{platform}'"
    cursor.execute(request_search)
    result = cursor.fetchone()

    request_insert_t2 = """INSERT INTO games (Name, PLatform_ID, Year, Genre, Publisher, NA_Sales,
                                EU_Sales, JP_Sales, Other_Sales, Global_Sales) VALUES (%s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s)"""
    data2 = (name, result[0], year, genre, publisher, north_america_sales, europe_sales, japan_sales, other_sales,
             global_sales)
    cursor.execute(request_insert_t2, data2)


    conn.commit()
# Fermer le curseur et la connexion à la base de données
    cursor.close()
    conn.close()
