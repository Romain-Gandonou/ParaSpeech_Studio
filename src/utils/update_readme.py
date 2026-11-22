
"""
Met à jour automatiquement l'arborescence du projet dans README.md
entre les balises <!-- TREE_START --> et <!-- TREE_END -->.
"""

from pathlib import Path

# Éléments à ignorer pour que l'arborescence reste claire et professionnelle
DOSSIERS_IGNORES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".ipynb_checkpoints",
    ".vscode",
}

# Extensions de données brutes ou images générées en masse à masquer
EXTENSIONS_IGNOREES = {".wav", ".mp4", ".mp3", ".png", ".jpg"}


def obtenir_racine_projet() -> Path:
    """Remonte jusqu'à la racine du projet contenant 'src'."""
    chemin_actuel = Path(__file__).resolve()
    for parent in chemin_actuel.parents:
        if (parent / "src").exists():
            return parent
    return chemin_actuel.parents[2]


def generer_arborescence(dossier: Path, prefixe: str = "") -> list[str]:
    """Parcourt récursivement les dossiers et formate l'arbre."""
    lignes = []
    elements = sorted(
        [
            e
            for e in dossier.iterdir()
            if e.name not in DOSSIERS_IGNORES
            and e.suffix.lower() not in EXTENSIONS_IGNOREES
        ],
        key=lambda x: (x.is_file(), x.name.lower()),
    )

    for index, element in enumerate(elements):
        est_dernier = index == len(elements) - 1
        connecteur = "└── " if est_dernier else "├── "
        nom_affiche = f"{element.name}/" if element.is_dir() else element.name

        lignes.append(f"{prefixe}{connecteur}{nom_affiche}")

        if element.is_dir():
            extension_prefixe = "    " if est_dernier else "│   "
            lignes.extend(generer_arborescence(element, prefixe + extension_prefixe))

    return lignes


def mettre_a_jour_readme():
    """Remplace le bloc d'arborescence dans README.md."""
    racine = obtenir_racine_projet()
    fichier_readme = racine / "README.md"

    balise_debut = "<!-- TREE_START -->"
    balise_fin = "<!-- TREE_END -->"

    lignes_arbre = [f"{racine.name}/"] + generer_arborescence(racine)
    bloc_arborescence = (
        f"{balise_debut}\n```text\n"
        + "\n".join(lignes_arbre)
        + f"\n```\n{balise_fin}"
    )

    if not fichier_readme.exists():
        fichier_readme.write_text(
            f"# ParaSpeech Africa\n\n## Architecture du projet\n\n{bloc_arborescence}\n",
            encoding="utf-8",
        )
        print("[README] Fichier README.md créé avec l'arborescence.")
        return

    contenu = fichier_readme.read_text(encoding="utf-8")

    if balise_debut in contenu and balise_fin in contenu:
        avant = contenu.split(balise_debut)[0]
        apres = contenu.split(balise_fin)[1]
        nouveau_contenu = f"{avant}{bloc_arborescence}{apres}"
        fichier_readme.write_text(nouveau_contenu, encoding="utf-8")
        print("[README] Arborescence mise à jour automatiquement.")
    else:
        print(f"[ATTENTION] Balises {balise_debut} / {balise_fin} absentes de README.md.")


if __name__ == "__main__":
    mettre_a_jour_readme()
