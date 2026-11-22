
"""
Script de lecture, visualisation et extraction de métadonnées audio.
Parcourt le dossier 'data/processed/audio/extrait', génère les graphiques
amplitude/durée dans 'reports/graphiques/' et enregistre les informations
dans 'data/audio.csv' en sautant les fichiers déjà traités.
"""

import csv
from pathlib import Path
import numpy as np
import librosa
import matplotlib.pyplot as plt


def obtenir_chemins_projet() -> Path:
    """
    Détermine automatiquement la racine du projet 'paraspeech'
    peu importe le sous-dossier de 'src/' où se trouve ce script.
    """
    chemin_actuel = Path(__file__).resolve()
    for parent in chemin_actuel.parents:
        if (parent / "data").exists() and (parent / "src").exists():
            return parent
    # Solution de repli : 2 niveaux au-dessus (ex: src/preprocessing/script.py -> paraspeech/)
    return chemin_actuel.parents[2]


def charger_audios_deja_traites(chemin_csv: Path) -> set:
    """
    Lit le fichier 'data/audio.csv' s'il existe et retourne l'ensemble (set)
    des noms de fichiers déjà enregistrés pour éviter de les retraiter.
    """
    deja_traites = set()
    if chemin_csv.exists():
        with open(chemin_csv, mode="r", encoding="utf-8", newline="") as fichier:
            lecteur = csv.DictReader(fichier)
            for ligne in lecteur:
                if "nom_fichier" in ligne and ligne["nom_fichier"]:
                    deja_traites.add(ligne["nom_fichier"])
    return deja_traites


def sauvegarder_graphique_amplitude(
    signal: np.ndarray,
    sr: int,
    duree: float,
    nom_audio: str,
    dossier_sortie: Path,
) -> Path:
    """
    Trace la courbe d'amplitude en fonction du temps (durée),
    la sauvegarde dans 'reports/graphiques/' au format PNG
    et retourne le chemin du fichier image créé.
    """
    # Calcul de l'axe des temps en secondes pour chaque échantillon
    temps = np.arange(len(signal)) / sr

    # Création de la figure
    plt.figure(figsize=(14, 5))
    plt.plot(temps, signal, color="steelblue", linewidth=0.5, alpha=0.85)

    # Habillage du graphique
    plt.title(f"Forme d'onde : {nom_audio} (Durée : {duree:.2f}s | SR : {sr} Hz)")
    plt.xlabel("Temps (secondes)")
    plt.ylabel("Amplitude (normalisée)")
    plt.xlim(0, duree)
    plt.ylim(-1.05, 1.05)  # Échelle fixe entre -1 et 1 pour comparer les audios entre eux
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    # Sauvegarde de l'image et libération de la mémoire
    chemin_image = dossier_sortie / f"{Path(nom_audio).stem}_amplitude.png"
    plt.savefig(chemin_image, dpi=150)
    plt.close()

    return chemin_image


def analyser_et_enregistrer_audio(
    chemin_audio: Path,
    dossier_graphiques: Path,
    racine_projet: Path,
) -> dict:
    """
    Charge un fichier audio en mono avec librosa, génère son graphique
    et retourne un dictionnaire contenant ses métadonnées importantes.
    """
    # 1. Chargement du signal en mono (mono=True) à sa fréquence d'origine (sr=None)
    signal, sr = librosa.load(chemin_audio, sr=None, mono=True)

    # 2. Calcul des informations fondamentales
    nb_echantillons = len(signal)
    duree_secondes = nb_echantillons / sr

    # 3. Calcul des indicateurs d'énergie (utiles pour détecter le bruit / la saturation)
    amplitude_max = float(np.max(np.abs(signal))) if nb_echantillons > 0 else 0.0
    energie_rms = float(np.sqrt(np.mean(signal**2))) if nb_echantillons > 0 else 0.0

    # 4. Génération et sauvegarde du graphique amplitude / durée
    chemin_image = sauvegarder_graphique_amplitude(
        signal=signal,
        sr=sr,
        duree=duree_secondes,
        nom_audio=chemin_audio.name,
        dossier_sortie=dossier_graphiques,
    )

    # 5. Retour des métadonnées structurées pour le fichier CSV
    return {
        "nom_fichier": chemin_audio.name,
        "chemin_relatif": str(chemin_audio.relative_to(racine_projet)),
        "chemin_graphique": str(chemin_image.relative_to(racine_projet)),
        "frequence_echantillonnage_hz": sr,
        "duree_secondes": round(duree_secondes, 4),
        "nombre_echantillons": nb_echantillons,
        "amplitude_max": round(amplitude_max, 6),
        "energie_rms_moyenne": round(energie_rms, 6),
    }


def executer_pipeline_audio():
    """
    Fonction principale : parcourt le dossier d'extraction audio, saute les
    fichiers déjà présents dans 'data/audio.csv' et traite uniquement les nouveaux.
    """
    # Définition des chemins du projet
    racine = obtenir_chemins_projet()
    dossier_audio = racine / "data" / "processed" / "audio" / "extrait"
    dossier_graphiques = racine / "reports" / "graphiques"
    fichier_csv = racine / "data" / "audio.csv"

    # Vérification de l'existence du dossier source
    if not dossier_audio.exists():
        print(f"[ERREUR] Le dossier source est introuvable : {dossier_audio}")
        return

    # Création des dossiers de destination si nécessaire
    dossier_graphiques.mkdir(parents=True, exist_ok=True)
    fichier_csv.parent.mkdir(parents=True, exist_ok=True)

    # Récupération des fichiers déjà traités
    audios_traites = charger_audios_deja_traites(fichier_csv)
    print(f"Audios déjà enregistrés dans {fichier_csv.name} : {len(audios_traites)}")

    # Extensions audio prises en charge
    extensions_valides = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}

    # Liste triée de tous les fichiers audio dans le dossier extrait
    fichiers_audio = sorted(
        [
            f
            for f in dossier_audio.iterdir()
            if f.is_file() and f.suffix.lower() in extensions_valides
        ]
    )

    if not fichiers_audio:
        print(f"Aucun fichier audio trouvé dans : {dossier_audio}")
        return

    # Colonnes du fichier CSV
    colonnes_csv = [
        "nom_fichier",
        "chemin_relatif",
        "chemin_graphique",
        "frequence_echantillonnage_hz",
        "duree_secondes",
        "nombre_echantillons",
        "amplitude_max",
        "energie_rms_moyenne",
    ]

    # Ouverture du CSV en mode ajout ('a' = append) pour conserver l'existant
    fichier_existe_deja = fichier_csv.exists() and fichier_csv.stat().st_size > 0
    nouveaux_traites = 0
    ignores = 0

    with open(fichier_csv, mode="a", encoding="utf-8", newline="") as f_csv:
        ecrivain = csv.DictWriter(f_csv, fieldnames=colonnes_csv)

        # Écrire l'en-tête uniquement si le fichier CSV vient d'être créé
        if not fichier_existe_deja:
            ecrivain.writeheader()

        # Parcours de chaque fichier audio
        for chemin_audio in fichiers_audio:
            if chemin_audio.name in audios_traites:
                print(f"[SAUTÉ] {chemin_audio.name} (déjà traité)")
                ignores += 1
                continue

            print(f"[TRAITEMENT] {chemin_audio.name}...")
            try:
                infos_audio = analyser_et_enregistrer_audio(
                    chemin_audio=chemin_audio,
                    dossier_graphiques=dossier_graphiques,
                    racine_projet=racine,
                )
                # Écriture immédiate de la ligne dans le CSV
                ecrivain.writerow(infos_audio)
                f_csv.flush()
                nouveaux_traites += 1
            except Exception as erreur:
                print(f"[ERREUR] Impossible de traiter {chemin_audio.name} : {erreur}")

    print("-" * 50)
    print(f"Résumé : {nouveaux_traites} nouveau(x) traité(s) | {ignores} sauté(s).")
    print(f"Données enregistrées dans : {fichier_csv}")
    print(f"Graphiques sauvegardés dans : {dossier_graphiques}")


if __name__ == "__main__":
    executer_pipeline_audio()
