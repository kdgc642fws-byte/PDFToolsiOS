import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pypdf import PdfReader, PdfWriter

from pdf_pages import parse_pages, remove_pages


class PdfPagesTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory.name)
        self.input_path = self.directory / "entree.pdf"
        self.output_path = self.directory / "Documents" / "PDFTools" / "resultat.pdf"
        self.output_patch = patch("pdf_pages.OUTPUT_PATH", self.output_path)
        self.output_patch.start()
        writer = PdfWriter()
        for _ in range(9):
            writer.add_blank_page(width=100, height=100)
        with self.input_path.open("wb") as pdf_file:
            writer.write(pdf_file)

    def tearDown(self):
        self.output_patch.stop()
        self.temporary_directory.cleanup()

    def test_list_range_and_combination(self):
        self.assertEqual(parse_pages("2,4-6,9", 9), {1, 3, 4, 5, 8})

    def test_creates_pdf_without_requested_pages(self):
        result = remove_pages(self.input_path, "2,4-6,9")
        self.assertEqual(result, self.output_path.resolve())
        self.assertTrue(self.output_path.is_file())
        self.assertEqual(len(PdfReader(str(self.output_path)).pages), 4)

    def test_replaces_existing_output(self):
        self.output_path.parent.mkdir(parents=True)
        self.output_path.write_bytes(b"ancien contenu")
        remove_pages(self.input_path, "2")
        self.assertEqual(len(PdfReader(str(self.output_path)).pages), 8)

    def test_rejects_missing_input(self):
        with self.assertRaisesRegex(ValueError, "n'existe pas"):
            remove_pages(self.directory / "absent.pdf", "1")

    def test_rejects_out_of_bounds_page(self):
        with self.assertRaisesRegex(ValueError, "hors limites"):
            parse_pages("10", 9)

    def test_rejects_removing_every_page(self):
        with self.assertRaisesRegex(ValueError, "toutes les pages"):
            remove_pages(self.input_path, "1-9")

    def test_main_prints_exact_output_path(self):
        with patch("builtins.print") as print_mock:
            from pdf_pages import main

            self.assertEqual(main([str(self.input_path), "2"]), 0)
        print_mock.assert_called_once_with(f"PDF créé : {self.output_path.resolve()}")

    def test_rejects_invalid_syntax(self):
        for specification in ("", "2,,4", "4-2", "a", "1-2-3"):
            with self.subTest(specification=specification):
                with self.assertRaises(ValueError):
                    parse_pages(specification, 9)


if __name__ == "__main__":
    unittest.main()
