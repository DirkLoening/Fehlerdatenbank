import logging
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.debug = True
logging.basicConfig(level=logging.DEBUG)  # Alle Logs ab DEBUG und höher werden angezeigt

def lade_fehlerdatenbank():
    try:
        with open("Fehlerdatenbank.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def lade_fehlerdatenbank():
    try:
        with open("Fehlerdatenbank.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route("/check", methods=["GET"])
def check_fehler():
    app.logger.debug('Dies ist eine Debug-Nachricht')
    code = request.args.get("code")
    funktion = request.args.get("funktion")
    zeile = request.args.get("zeile")
    csb_version = request.args.get("csb_version")

    app.logger.debug('Erhaltener Fehlercode: {code}')
    app.logger.debug('Erhaltene Funktion: {funktion}')
    app.logger.debug('Erhaltene Zeile: {zeile}')
    app.logger.debug('Erhaltene CSB-Version: {csb_version}')

    datenbank = lade_fehlerdatenbank()
    if not datenbank:
        print("Datenbank ist leer!")
    else:
        print(f"Datenbank hat {len(datenbank)} Einträge.")
        
    for eintrag in datenbank:
        if (eintrag.get("fehlercode") == code and
            eintrag.get("funktion") == funktion and
            eintrag.get("zeile") == zeile and
            eintrag.get("csb_version") == csb_version):
            return jsonify({
                "ursache": eintrag["ursache"],
                "gefixtAbVersion": eintrag["gefixtAbVersion"],
                "antwort": eintrag["antwort"]
            })

    return jsonify({"antwort": "Fehler nicht bekannt. Bitte Support kontaktieren."}), 404


@app.route("/check_full", methods=["POST"])
def check_full_fehler():
    data = request.get_json()

    # Extrahiere den Fehlertext
    fehlertext = data.get("text")

    # Hier könntest du die Logik zur Fehleranalyse einfügen, z.B. Fehlercode, Funktion, Zeile usw. aus dem Text extrahieren.

    # Angenommen, wir extrahieren diese Werte aus dem Fehlertext:
    fehlercode = "22"  # Beispiel: Muss aus dem Fehlertext extrahiert werden.
    funktion = "HONDAMELD"  # Beispiel: Muss aus dem Fehlertext extrahiert werden.
    zeile = "9649"  # Beispiel: Muss aus dem Fehlertext extrahiert werden.
    csb_version = "14084"  # Beispiel: Muss aus dem Fehlertext extrahiert werden.

    datenbank = lade_fehlerdatenbank()

    for eintrag in datenbank:
        if (eintrag.get("fehlercode") == fehlercode and
            eintrag.get("funktion") == funktion and
            eintrag.get("zeile") == zeile and
            eintrag.get("csb_version") == csb_version):
            return jsonify({
                "ursache": eintrag["ursache"],
                "gefixtAbVersion": eintrag["gefixtAbVersion"],
                "antwort": eintrag["antwort"]
            })

    return jsonify({"antwort": "Fehler nicht bekannt. Bitte Support kontaktieren."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

@app.route("/check_full", methods=["POST"])
def check_full_fehler():
    data = request.get_json()

    # Extrahiere den Fehlertext
    fehlertext = data.get("text")

    # Hier könntest du die Logik zur Fehleranalyse einfügen, z.B. Fehlercode, Funktion, Zeile usw. aus dem Text extrahieren.

    # Angenommen, wir extrahieren diese Werte aus dem Fehlertext:
    fehlercode = "22"  # Beispiel: Muss aus dem Fehlertext extrahiert werden.
    funktion = "HONDAMELD"  # Beispiel: Muss aus dem Fehlertext extrahiert werden.
    zeile = "9649"  # Beispiel: Muss aus dem Fehlertext extrahiert werden.
    csb_version = "14084"  # Beispiel: Muss aus dem Fehlertext extrahiert werden.

    datenbank = lade_fehlerdatenbank()

    for eintrag in datenbank:
        if (eintrag.get("fehlercode") == fehlercode and
            eintrag.get("funktion") == funktion and
            eintrag.get("zeile") == zeile and
            eintrag.get("csb_version") == csb_version):
            return jsonify({
                "ursache": eintrag["ursache"],
                "gefixtAbVersion": eintrag["gefixtAbVersion"],
                "antwort": eintrag["antwort"]
            })

    return jsonify({"antwort": "Fehler nicht bekannt. Bitte Support kontaktieren."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
