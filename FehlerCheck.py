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

@app.route("/analysiere", methods=["POST"])
def analysiere_fehlertext():
    text = request.get_data(as_text=True)
    infos = extrahiere_infos(text)

    if not infos:
        return jsonify({"antwort": "Fehlermeldung unvollständig oder unverständlich"}), 400

    datenbank = lade_fehlerdatenbank()

    for eintrag in datenbank:
        if (eintrag.get("fehlercode") == infos["fehlercode"] and
            eintrag.get("funktion") == infos["funktion"] and
            eintrag.get("zeile") == infos["zeile"] and
            eintrag.get("csb_version") == infos["csb_version"]):
            return jsonify({
                "ursache": eintrag["ursache"],
                "gefixtAbVersion": eintrag["gefixtAbVersion"],
                "antwort": eintrag["antwort"]
            })

    return jsonify({"antwort": "Fehler nicht bekannt. Bitte Support kontaktieren."}), 404

def extrahiere_infos(text):
    import re
    fehlercode = re.search(r"Fehler \((\d+)\)", text)
    funktion = re.search(r"in (\w+), Zeile", text)
    zeile = re.search(r"Zeile (\d+)", text)
    csb_match = re.search(r"CSB Version W2 vom\s*:\s*(\d{2}\.\d{2}\.\d{2})\s*\[(\d+)\]", text)

    if not (fehlercode and funktion and zeile and csb_match):
        return None

    return {
        "fehlercode": fehlercode.group(1),
        "funktion": funktion.group(1),
        "zeile": zeile.group(1),
        "csb_version": csb_match.group(2)
    }
