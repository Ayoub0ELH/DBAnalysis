from lxml import etree

# Charger le fichier XML et le fichier XSLT
xml_doc = etree.parse("game_list.xml")
xslt_doc = etree.parse("new_html_rules.xslt")

# Créer un transformateur XSLT
transform = etree.XSLT(xslt_doc)

# Appliquer la transformation sur le fichier xml
result = transform(xml_doc)

# Enregistrer le résultat dans un fichier HTML, ecriture en mode binaire
with open("resultat.html", "wb") as f:
    f.write(result)

print("Transformation XML vers HTML terminée.")
