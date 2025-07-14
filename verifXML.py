from lxml import etree

# Charger le fichier XML source
xml_tree = etree.parse('table_data_formatted.xml')


xsd_tree = etree.parse('verif_data.xsd')


xmlschema = etree.XMLSchema(xsd_tree)

# Vérifier si le fichier XML est conforme au XSD
is_valid = xmlschema.validate(xml_tree)

if is_valid:
    print("Le fichier XML est conforme au XSD.")
else:
    print("Le fichier XML n'est pas conforme au XSD.")
    # Afficher les erreurs de validation
    for error in xmlschema.error_log:
        print(f"Erreur: {error.message} (ligne {error.line}, colonne {error.column})")
