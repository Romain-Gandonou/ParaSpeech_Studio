
import os
import subprocess
import json
import csv

# Définition des chemins selon l'arborescence officielle de ParaSpeech
DOSSIER_RAW = "data/raw"
DOSSIER_AUDIO = "data/processed/audio"
FICHIER_REGISTRE = "data/processed/videos.csv"

def inspecter_et_extraire_tout():
    # 1. S'assurer que les dossiers de sortie existent, sinon on les crée
    os.makedirs(DOSSIER_AUDIO, exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # 2. Préparer le fichier CSV s'il n'existe pas encore
    # On l'ouvre en mode "a" (append) pour ajouter des lignes sans effacer le reste
    if not os.path.exists(FICHIER_REGISTRE):
        with open(FICHIER_REGISTRE, mode='w', newline='', encoding='utf-8') as f:
            ecrivain = csv.writer(f)
            # On écrit les colonnes exactes de ta convention
            ecrivain.writerow([
                'video_id', 'provenance', 'titre', 'date', 
                'licence_ou_autorisation', 'langue_source', 
                'langue_interpretation', 'fichier_original', 
                'duree_s', 'frequence_hz'
            ])

    # 3. Parcourir tous les fichiers du dossier data/raw/
    for nom_fichier in os.listdir(DOSSIER_RAW):
        # On ne traite que les fichiers vidéos (ex: .mp4)
        if nom_fichier.endswith(".mp4"):
            
            # Construire les chemins complets
            chemin_video_complete = os.path.join(DOSSIER_RAW, nom_fichier)
            
            # Extraire l'identifiant (ex: "V001.mp4" devient "V001")
            video_id = os.path.splitext(nom_fichier)[0]
            
            # Définir le nom du fichier audio de sortie (ex: V001.wav)
            nom_audio = f"{video_id}.wav"
            chemin_audio_complet = os.path.join(DOSSIER_AUDIO, nom_audio)
            
            print(f"--- Traitement de {video_id} ---")
            
            # 4. APPEL À FFPROBE (Inspection)
            commande_probe = [
                'ffprobe', '-v', 'quiet', 
                '-print_format', 'json', 
                '-show_format', '-show_streams', 
                chemin_video_complete
            ]
            resultat_probe = subprocess.run(commande_probe, capture_output=True, text=True)
            infos = json.loads(resultat_probe.stdout)
            
            # Récupération de la durée (dans la section format)
            duree = infos.get('format', {}).get('duration', '0')
            
            # Récupération de la fréquence d'échantillonnage de l'audio d'origine
            frequence = 0
            for flux in infos.get('streams', []):
                if flux.get('codec_type') == 'audio':
                    frequence = flux.get('sample_rate', 0)
                    break # On a trouvé l'audio, on s'arrête
            
            # 5. APPEL À FFMPEG (Extraction)
            commande_ffmpeg = [
                'ffmpeg', '-y', 
                '-i', chemin_video_complete,
                '-vn', 
                '-acodec', 'pcm_s16le', 
                '-ar', '16000', # Ta cible pour l'audio propre de ParaSpeech
                chemin_audio_complet
            ]
            subprocess.run(commande_ffmpeg, capture_output=True)
            
            # 6. ENREGISTREMENT DANS LE REGISTRE CSV
            with open(FICHIER_REGISTRE, mode='a', newline='', encoding='utf-8') as f:
                ecrivain = csv.writer(f)
                ecrivain.writerow([
                    video_id, 
                    "Inconnue",         # Provenance (à remplir plus tard)
                    "Sans titre",       # Titre (à remplir plus tard)
                    "2026-10-15",       # Date par défaut
                    "Privée",           # Licence
                    "fr",               # Langue source
                    "fr",               # Langue interprétation
                    nom_fichier,        # Nom d'origine (ex: V001.mp4)
                    duree, 
                    frequence
                ])
                
            print(f"✅ {video_id} traité et enregistré dans le registre.")

if __name__ == "__main__":
    inspecter_et_extraire_tout()
