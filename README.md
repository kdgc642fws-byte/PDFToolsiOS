# PDFToolsiOS

## Suppression de pages PDF

Installation : `python3 -m pip install pypdf`

Exemple : `python3 pdf_pages.py entree.pdf sortie.pdf "2,4-6"`

Les pages commencent a 1. La syntaxe accepte les listes (`2,5,8`), les plages (`4-7`) et leurs combinaisons (`2,4-6,9`).

## Tests sur GitHub

GitHub Actions lance automatiquement les tests a chaque `push` et pull request.
Pour les lancer manuellement : ouvrir l'onglet **Actions**, choisir **Tests Python**, puis cliquer sur **Run workflow**.
