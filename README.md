# weRoom — Agenda Salle de Réunion we.law
# Généré le 2026-02-27

## Contenu du projet

weroom/
├── app.py              ← serveur Python
├── requirements.txt    ← dépendances
├── Procfile            ← pour Render.com
├── README.md           ← ce fichier
└── templates/
    ├── login.html      ← page de connexion
    └── index.html      ← agenda principal

---

## ÉTAPE 1 — Adapter la liste des collaborateurs

Dans app.py, modifier la liste COLLABORATEURS :

COLLABORATEURS = [
    "Ludovic",
    "Marie",
    ...
]

---

## ÉTAPE 2 — Tester en local (optionnel)

pip install flask gunicorn
python app.py
→ Ouvrir http://localhost:5000

---

## ÉTAPE 3 — Déployer sur Render.com (gratuit, accessible partout)

1. Créer un compte sur https://render.com
2. Cliquer "New +" → "Web Service"
3. Choisir "Deploy from existing code" → uploader le dossier ou connecter GitHub
4. Remplir :
   - Name : weroom-welaw (ou ce que vous voulez)
   - Runtime : Python 3
   - Build Command : pip install -r requirements.txt
   - Start Command : gunicorn app:app
5. Cliquer "Create Web Service"
6. En 2-3 minutes, vous avez une URL du type : https://weroom-welaw.onrender.com

⚠️ Sur le plan gratuit Render, l'app "s'endort" après 15 min d'inactivité
   et met ~30 secondes à se réveiller. Pour éviter ça : plan Starter à 7$/mois.

---

## Alternative : hébergement local réseau

Si vous avez un PC allumé en permanence au bureau :

python app.py
→ Accessible sur le réseau local via http://IP_DU_PC:5000

---

## Fonctionnalités

- Connexion par nom (liste fermée, pas de mot de passe)
- Vue calendrier semaine (lundi-vendredi, 7h-20h)
- Cliquer sur un créneau pour pré-remplir le formulaire
- Détection des conflits automatique
- Annulation uniquement de ses propres réservations
- Accessible depuis PC, téléphone, tablette
