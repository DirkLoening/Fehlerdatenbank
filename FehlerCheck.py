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
    code = request.args.get("code")
    funktion = request.args.get("funktion")
    zeile = request.args.get("zeile")
    csb_version = request.args.get("csb_version")

    datenbank = lade_fehlerdatenbank()

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
