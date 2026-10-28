from docx import Document

from src.errors import ConversionError
from src.base import Converter


class TxtToDocx(Converter):
    def convert(self, input_path, output_path):
        try:
            with open(input_path, "r", encoding="utf-8-sig") as f:
                text = f.read()
        except UnicodeDecodeError:
            raise ConversionError("Plik TXT musi być zapisany w UTF-8.")
        except OSError as e:
            raise ConversionError("Nie można odczytać pliku TXT: " + str(e))

        document = Document()
        for line in text.splitlines():
            document.add_paragraph(line)

        try:
            document.save(str(output_path))
        except OSError as e:
            raise ConversionError("Nie można zapisać pliku DOCX: " + str(e))
