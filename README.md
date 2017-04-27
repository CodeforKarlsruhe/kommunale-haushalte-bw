# Kommunale Haushalte in Baden-Württemberg

Für kommunale Haushalte in Baden-Württemberg gelten der [kommunale Produktplan Baden-Württemberg][produktplan] und die [Verwaltungsvorschrift Produkt- und Kontenrahmen][vwv]. Diese enthalten Regeln zur Struktur der Haushalte und zu Bezeichnungen und Nummerierungen.

Dieses Repository enthält die in den Dokumenten enthaltenen Listen in maschinenlesbarer Form.


## Kommunaler Produktplan

[JSON](produktrahmen.json)


## Verwaltungsvorschrift Produkt- und Kontenrahmen

### Anlage 29 (Produktbereiche)

[CSV](vwv-anlage_29-produktbereiche.csv) [ODS](vwv-anlage_29-produktbereiche.ods)


### Anlage 30.2 (Kontenrahmen)
[JSON](vwv-anlage_30.2-kontenrahmen.json) [CSV](vwv-anlage_30.2-kontenrahmen.csv) [ODS](vwv-anlage_30.2-kontenrahmen.ods)

Der Kontenrahmen ist hierarchisch aufgebaut. Die CSV- und ODS-Varianten enthalten diese Hierarchie (wie das Originaldokument) nur implizit. In der JSON-Variante ist die Hierarchie explizit abgebildet:

    klassen = load_json('vwv-anlage_30.2-kontenrahmen.json')
    print(klassen['1']['gruppen']['11']['arten']['111']['konten']['1112']['beschreibung'])
    # Gibt 'Nichtbörsennotierte Aktien' aus

## Quellen

Die Originaldateien aus denen die Daten extrahiert wurden sind im Unterverzeichnis `quellen`.


[produktplan]: sources/Kommunaler_Produktplan_Stand_14.06.2016.pdf
[vwv]: sources/VwV_Produkt-_und_Kontenrahmen_komplett_29062016.pdf

