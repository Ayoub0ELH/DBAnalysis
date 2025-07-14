import mysql.connector
import xml.etree.ElementTree as ET
import xml.dom.minidom

# On se connecte à la base de données
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="isib",
    database="sales_games"
)

cursor = db_connection.cursor()

# Créer l'élément racine du fichier XML --> games
root = ET.Element("games")

# récuperer toutes les données de la table game

cursor.execute("SELECT * FROM games")
rows = cursor.fetchall()

# Pour chaque ligne dans la liste de lignes
for row in rows:
    # Crée un sous-élément de la racine pour chaque enregistrement de la table --> game
    game = ET.SubElement(root, "game")

    # cursor.column_name reprend l'ensemble des noms de colonnes
    for i, column_name in enumerate(cursor.column_names):
        if column_name not in ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]:
            field = ET.SubElement(game, column_name)
            field.text = str(row[i])

    # Creer la balise sales
    sales = ET.SubElement(game, "Sales")
    sales.attrib["North_America"] = str(row[6])         # Créer les attributs  de Sales
    sales.attrib["Europe"] = str(row[7])
    sales.attrib["Japan"] = str(row[8])
    sales.attrib["Other"] = str(row[9])
    sales.attrib["Global"] = str(row[10])

# Créez un arbre XML à partir de l'élément racine
tree = ET.ElementTree(root)

# Enregistrez l'arbre XML dans un fichier
tree.write("table_data.xml")

cursor.close()
db_connection.close()

# Charger le fichier XML
document = xml.dom.minidom.parse("table_data.xml")

# Formater l'XML avec une indentation
xml_content = document.toprettyxml(indent="  ")

# Enregistrez le XML formaté dans le fichier
with open("game_list.xml", "w", encoding="utf-8") as output_file:
    output_file.write(xml_content)
