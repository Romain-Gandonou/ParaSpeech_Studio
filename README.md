
# ParaSpeech Studio

Projet fil rouge du PIIA, Cohorte 2 (Spécial Machine Learning), Académie des Mathématiques Appliquées(AMA).

## But du projet

## But du projet

De nombreuses vidéos africaines (prédications, conférences, cérémonies) contiennent une structure naturellement bilingue : un locuteur parle, puis un interprète restitue son message dans une autre langue. Ces contenus existent, mais ils ne sont ni découpés, ni associés, ni exploitables comme ressources linguistiques, alors que les langues africaines peu dotées manquent de données pour l'intelligence artificielle.

ParaSpeech Studio vise à transformer semi-automatiquement un audio ou une vidéo avec interprétation consécutive en un corpus bilingue structuré. En entrée : un fichier audio ou vidéo. En sortie : des paires de séquences (prise de parole source, interprétation correspondante), chacune avec un score de confiance et un statut validé par un humain.

Le projet ne construit pas un système de traduction ni de reconnaissance vocale : il résout d'abord le problème de la construction et de l'alignement de données bilingues, en passant par l'extraction de l'audio, la segmentation, la génération de paires candidates, un score par apprentissage automatique et une validation humaine.

La langue africaine peu dotée traitée par l'équipe est la langue fon.
## Statut

Phase 0 (lancement) en cours : mise en place du dépôt, de l'environnement Python et de la structure du projet.

## Équipe

- Ablo Romain GANDONOU
- Loukouma Paul-Marie WENSEN'NA

Mentor
- Obed EGUEDJI

## Installation

1. Cloner le dépôt puis se placer dans son dossier.
2. Créer l'environnement virtuel :

```bash
python -m venv .env
```

3. L'activer :

```bash
# Windows
.env\Scripts\activate

# Linux ou macOS
source .env/bin/activate
```

4. Installer les bibliothèques :

```bash
pip install -r requirements.txt
```

## Organisation du dépôt

```
paraspeech/
├── data/
│   ├── raw/          données brutes, jamais modifiées
│   ├── processed/    données transformées par le code
│   └── annotations/  étiquettes faites par des humains
├── notebooks/        essais et exploration
├── src/
│   ├── preprocessing/  préparation de l'audio
│   ├── features/       caractéristiques calculées sur les segments
│   ├── alignment/      génération des paires source-interprétation
│   ├── models/         modèles d'apprentissage
│   └── evaluation/     mesure de la qualité des résultats
├── app/              application ParaSpeech Studio
├── tests/            vérifications automatiques du code
└── README.md
```

Les fichiers `.gitkeep` servent uniquement à conserver les dossiers vides dans le dépôt.

## Données

Les données audio et vidéo ne sont pas versionnées dans ce dépôt : elles sont lourdes et leur usage est soumis à des droits. Seul le dossier `data/raw/` est conservé, avec un fichier `.gitkeep`.

[À COMPLÉTER : où et comment récupérer ou déposer les données brutes, et où se trouve la fiche de provenance de chaque source.]

## Conventions

- Nommage des données : [À COMPLÉTER après le travail 2 du guide de la Phase 0]
- Forme du message des commits : " telle fichier modifier ou telle action effectuer de façon explicite et claire."
