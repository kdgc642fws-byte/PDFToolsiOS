#!/usr/bin/env python3
"""Supprime des pages d'un fichier PDF avec pypdf."""

import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def expand_path(path):
    """Developpe un chemin commencant par ~/ de facon portable."""
    path = str(path)
    if path.startswith(("~/", "~\\")):
        return Path.home() / path[2:]
    return Path(path).expanduser()


def parse_pages(specification, page_count):
    """Convertit une specification telle que ``2,4-6`` en indices de pages."""
    pages = set()

    if not specification.strip():
        raise ValueError("la liste des pages est vide")

    for item in specification.split(","):
        item = item.strip()
        if not item:
            raise ValueError("syntaxe de pages invalide")

        if "-" in item:
            parts = item.split("-")
            if len(parts) != 2:
                raise ValueError(f"plage invalide : {item}")
            try:
                start, end = (int(part.strip()) for part in parts)
            except ValueError as error:
                raise ValueError(f"plage invalide : {item}") from error
            if start > end:
                raise ValueError(f"plage invalide (debut apres la fin) : {item}")
            requested = range(start, end + 1)
        else:
            try:
                requested = (int(item),)
            except ValueError as error:
                raise ValueError(f"numero de page invalide : {item}") from error

        for page_number in requested:
            if page_number < 1 or page_number > page_count:
                raise ValueError(
                    f"page hors limites : {page_number} "
                    f"(le PDF contient {page_count} page(s))"
                )
            pages.add(page_number - 1)

    return pages


def remove_pages(input_path, output_path, specification):
    """Cree un nouveau PDF sans les pages demandees."""
    input_path = expand_path(input_path)
    output_path = expand_path(output_path)

    if not input_path.is_file():
        raise ValueError(f"le fichier PDF d'entree n'existe pas : {input_path}")

    try:
        reader = PdfReader(str(input_path))
    except Exception as error:
        raise ValueError(f"impossible de lire le PDF d'entree : {error}") from error

    pages_to_remove = parse_pages(specification, len(reader.pages))
    if len(pages_to_remove) == len(reader.pages):
        raise ValueError("impossible de supprimer toutes les pages du PDF")

    writer = PdfWriter()
    for index, page in enumerate(reader.pages):
        if index not in pages_to_remove:
            writer.add_page(page)

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("wb") as output_file:
            writer.write(output_file)
    except OSError as error:
        raise ValueError(f"impossible de creer le PDF de sortie : {error}") from error

    return output_path.resolve()


def main(arguments=None):
    arguments = sys.argv[1:] if arguments is None else arguments
    if len(arguments) != 3:
        print(
            'Usage : python3 pdf_pages.py entree.pdf sortie.pdf "2,4-6"',
            file=sys.stderr,
        )
        return 2

    try:
        output_path = remove_pages(arguments[0], arguments[1], arguments[2])
    except ValueError as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 1

    print(f"PDF créé : {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
