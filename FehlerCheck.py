import json
import re
import argparse

def lade_fehlerdatenbank():
    """Lädt die Fehlerdatenbank aus einer JSON-Datei."""
    try:
        with open("Fehlerdatenbank.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Falls die Datei nicht existiert, eine leere Liste zurückgeben

def speichere_fehlerdatenbank(datenbank):
    """Speichert die Fehlerdatenbank in einer JSON-Datei."""
    with open("Fehlerdatenbank.json", "w") as f:
        json.dump(datenbank, f, indent=4)

def fehler_aus_datei_auslesen(dateipfad):
    """Liest den Fehler aus der Datei und gibt die Daten zurück."""
    with open(dateipfad, "r") as f:
        content = f.read()
    
    # Extrahieren des Fehlercodes, der Funktion, Zeile, Version und Datum mit regulären Ausdrücken
    fehlercode = re.search(r"Fehler \((\d+)\)", content).group(1)
    funktion = re.search(r"in (\w+)", content).group(1)
    zeile = re.search(r"Zeile (\d+)", content).group(1)
    csb_version = re.search(r"CSB Version W2 vom\s*:\s*(\d+)", content).group(1)
    match = re.search(r"CSB Version W2 vom\s*:\s*(\d{2}\.\d{2}\.\d{2})\s*\[(\d+)\]", content)
    if match:
       version_datum = match.group(1)
       csb_version = match.group(2)
    else:
       version_datum = "unbekannt"
       csb_version = "unbekannt"
    
    if not match:
       print("⚠️  Konnte kein gültiges Versions-Datum finden.")
       return

    return {
        "fehlercode": fehlercode,
        "funktion": funktion,
        "zeile": zeile,
        "csb_version": csb_version,
        "version_datum": version_datum
    }

def fehler_suchen_und_hinzufuegen(dateipfad, benutzer_rolle):
    """Sucht nach einem Fehler in der Datenbank und fügt ihn hinzu, wenn er nicht gefunden wird."""
    fehler = fehler_aus_datei_auslesen(dateipfad)
    datenbank = lade_fehlerdatenbank()

    # Prüfen, ob der Fehler bereits in der Datenbank vorhanden ist
    for eintrag in datenbank:
        if (eintrag['fehlercode'] == fehler['fehlercode'] and
            eintrag['funktion'] == fehler['funktion'] and
            eintrag['zeile'] == fehler['zeile'] and
            eintrag['csb_version'] == fehler['csb_version']):
            print("Fehler bereits in der Datenbank gefunden.")
            print("Antwort:", eintrag['antwort'])
            return

    # Wenn der Fehler nicht gefunden wird, abhängig vom Benutzertyp weitere Informationen hinzufügen
    if benutzer_rolle == 'servicetechniker':
        ursache = input("Gib die Ursache des Fehlers ein: ")
        gefixtAbVersion = input("Gib die Version ein, ab der der Fehler behoben wurde: ")
        antwort = input("Gib die Lösung ein: ")
        fehler['ursache'] = ursache
        fehler['gefixtAbVersion'] = gefixtAbVersion
        fehler['antwort'] = antwort
        datenbank.append(fehler)
        speichere_fehlerdatenbank(datenbank)
        print("Fehler wurde zur Datenbank hinzugefügt.")
    else:
        print("Fehler nicht gefunden.")
        print("Wende dich bitte an den Support.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fehlerbehandlungssystem")
    parser.add_argument("path", help="Pfad zur Textdatei mit der Fehlermeldung")
    parser.add_argument("role", choices=["endkunde", "servicetechniker"], default="endkunde", nargs="?", help="Benutzerrolle (optional, Standard: endkunde)")
    args = parser.parse_args()

    fehler_suchen_und_hinzufuegen(args.path, args.role)
