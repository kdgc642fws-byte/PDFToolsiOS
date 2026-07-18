# PDFToolsiOS

## Suppression de pages PDF

Installation : `python3 -m pip install pypdf`

Commande : `python3 pdf_pages.py entree.pdf sortie.pdf "2,4-6"`

Les pages commencent a 1. La syntaxe accepte les listes (`2,5,8`), les plages (`4-7`) et leurs combinaisons (`2,4-6,9`).

Exemple dans a-Shell :

```bash
python3 ~/Documents/PDFTools/pdf_pages.py \
~shortcuts/entree.pdf \
~Downloads/resultat.pdf \
"2,4-6"
```

Le dossier parent du fichier de sortie est créé automatiquement et le fichier existant est remplacé.

## Tests sur GitHub

GitHub Actions lance automatiquement les tests a chaque `push` et pull request.
Pour les lancer manuellement : ouvrir l'onglet **Actions**, choisir **Tests Python**, puis cliquer sur **Run workflow**.
