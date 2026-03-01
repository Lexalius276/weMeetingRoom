# weRoom - Agenda de réservation de salle de réunion
# Généré le 2026-03-01 — we.law
# Version 1.1 — objet réunion optionnel

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "welaw-salle-reunion-2026"

DB_PATH = "weroom.db"

COLLABORATEURS = [
    "SC - Salomé CAMARA",
    "LDB - Ludovic DE BLOCK",
    "CDD - Charles-Eric de DECKER",
    "ED - Emmanuel DELANNOY",
    "HEZ - Hiba EL ZAZI",
    "FH - Florence HOFMANS",
    "GH - Guillaume HOET",
    "CL - Clélia LAMBOT",
    "PL - Patricia LEVINTOFF",
    "NL - Nastassja LORIAUX",
    "MD - Maureen DEMEURE",
    "HM - Hortense MIROUX",
    "CHV - Charlotte VERHAEGHE",
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            heure_debut TEXT NOT NULL,
            heure_fin TEXT NOT NULL,
            collaborateur TEXT NOT NULL,
            objet TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    if not session.get("collaborateur"):
        return redirect(url_for("login"))
    return render_template("index.html", collaborateurs=COLLABORATEURS, current_user=session["collaborateur"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nom = request.form.get("collaborateur")
        if nom in COLLABORATEURS:
            session["collaborateur"] = nom
            return redirect(url_for("index"))
    return render_template("login.html", collaborateurs=COLLABORATEURS)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/api/reservations")
def get_reservations():
    date_debut = request.args.get("date_debut")
    date_fin = request.args.get("date_fin")
    conn = get_db()
    if date_debut and date_fin:
        rows = conn.execute(
            "SELECT * FROM reservations WHERE date BETWEEN ? AND ? ORDER BY date, heure_debut",
            (date_debut, date_fin)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM reservations ORDER BY date, heure_debut"
        ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/reserver", methods=["POST"])
def reserver():
    if not session.get("collaborateur"):
        return jsonify({"error": "Non connecté"}), 401
    data = request.json
    date = data.get("date")
    heure_debut = data.get("heure_debut")
    heure_fin = data.get("heure_fin")
    objet = (data.get("objet") or "").strip()
    collaborateur = session["collaborateur"]

    # Objet optionnel — valeur par défaut si vide
    if not objet:
        objet = "Réunion"

    if not all([date, heure_debut, heure_fin]):
        return jsonify({"error": "La date et les heures sont requises"}), 400

    if heure_fin <= heure_debut:
        return jsonify({"error": "L'heure de fin doit être après l'heure de début"}), 400

    # Vérifier les conflits
    conn = get_db()
    conflits = conn.execute("""
        SELECT * FROM reservations
        WHERE date = ?
        AND NOT (heure_fin <= ? OR heure_debut >= ?)
    """, (date, heure_debut, heure_fin)).fetchall()

    if conflits:
        c = conflits[0]
        conn.close()
        return jsonify({"error": f"Créneau déjà réservé par {c['collaborateur']} ({c['heure_debut']}-{c['heure_fin']})"}), 409

    conn.execute(
        "INSERT INTO reservations (date, heure_debut, heure_fin, collaborateur, objet) VALUES (?, ?, ?, ?, ?)",
        (date, heure_debut, heure_fin, collaborateur, objet)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/api/annuler/<int:reservation_id>", methods=["DELETE"])
def annuler(reservation_id):
    if not session.get("collaborateur"):
        return jsonify({"error": "Non connecté"}), 401
    conn = get_db()
    row = conn.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Réservation introuvable"}), 404
    if row["collaborateur"] != session["collaborateur"]:
        conn.close()
        return jsonify({"error": "Vous ne pouvez annuler que vos propres réservations"}), 403
    conn.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
