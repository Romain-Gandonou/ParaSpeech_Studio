
# ParaSpeech Studio

Projet fil rouge du PIIA, Cohorte 2 (Spécial Machine Learning), Académie des Mathématiques Appliquées(AMA).


## But du projet

De nombreuses vidéos africaines (prédications, conférences, cérémonies) contiennent une structure naturellement bilingue : un locuteur parle, puis un interprète restitue son message dans une autre langue. Ces contenus existent, mais ils ne sont ni découpés, ni associés, ni exploitables comme ressources linguistiques, alors que les langues africaines peu dotées manquent de données pour l'intelligence artificielle.

ParaSpeech Studio vise à transformer semi-automatiquement un audio ou une vidéo avec interprétation consécutive en un corpus bilingue structuré. En entrée : un fichier audio ou vidéo. En sortie : des paires de séquences (prise de parole source, interprétation correspondante), chacune avec un score de confiance et un statut validé par un humain.

Le projet ne construit pas un système de traduction ni de reconnaissance vocale : il résout d'abord le problème de la construction et de l'alignement de données bilingues, en passant par l'extraction de l'audio, la segmentation, la génération de paires candidates, un score par apprentissage automatique et une validation humaine.

La langue africaine peu dotée traitée par l'équipe est la langue fon. 
Dans la suite du projet on peut bien prendre en compte une multitude de langues à faible ressources. 

## Statut

Phase 0 (lancement) en cours : mise en place du dépôt, de l'environnement Python et de la structure du projet.

## Équipe

- Ablo Romain GANDONOU
- Loukouma Paul-Marie WENSEN'NA

Mentor
- Obed EGUEDJI

## Installation

1. Cloner le dépôt puis se placer dans son dossier.
Ce dépôt est privé et uniquement ceux qui y ont accès peuvent le cloner.
```bash
git clone https://github.com/Romain-Gandonou/ParaSpeech_Studio.git
cd paraspeech
```

2. Créer l'environnement virtuel :

```bash
python -m venv .venv
```

3. L'activer :

```bash
# Windows
.venv\Scripts\activate

# Linux ou macOS
source .venv/bin/activate
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

Les vidéos que nous avons exploitées dans ce projet sont issues du youtube.

## Conventions

## Modèles de nom des fichiers

Chaque type de fichier suit un modèle précis. Le suffixe _v####
s’incrémente à chaque modification de contenu d’un fichier d’annotation ou de données dérivées ;
les versions antérieures sont conservées, car une annotation écrasée est une expérience qu’on ne
peut plus reproduire.

| Type de fichier | Identifiant | Exemple | Dossier |
|---|---|---|---|
| Vidéo ou audio brut | S####.ext_d'origine | S0001.mp4 | data/raw/ |
| Audio extrait | identifiant  source.wav| S0001.wav | data/processed/audio/extrait |
| Audio Normalisé | identifiant  source_canaux_frequence.wav | S0001_mono_16k.wav | data/processed/audio/normalise |
| Segment | identifiant source_SEG####.wav | S0001_SEG0001.wav | data/processed/segments/ |
| Métadonnées d’une source | identifiant source_meta.json | S0001_meta.json | data/processed/ |
| Table des segments | identifiant source_segments_v####.csv | S001_segments_v01.csv | 
| Paires candidates | S######_pairs_v####.csv | S001_pairs_v01.csv | data/annotations/ |
| Annotations manuelles | S######_annot_init_v####.csv | S001_annot_pm_v01.csv | data/annotations |
| Gold Datase | S######_gold_v####.csv | S001_gold_v01.csv | data/annotations |
| Export du corpus | corpus_fon_fra_v####_date.parquet | corpus_fon_fra_v01_20270227.parquet | data/annotations |
| Modèle ML| algo_v####_date.joblib | logreg_v01_20261120.joblib | /src/models
| Notebook | ####_sujet.ipynb | 01_extraction_audio.ipynb | /notebooks


- Forme du message des commits : " "Chaque message de commit doit décrire de façon claire et explicite quel fichier a été modifié ou quelle action a été effectuée, afin que n'importe quel collaborateur puisse comprendre l'historique, même plusieurs mois après."
"
