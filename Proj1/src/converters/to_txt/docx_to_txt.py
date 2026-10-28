from docx import Document

from src.errors import ConversionError
from src.base import Converter


class DocxToTxt(Converter):
    def convert(self, input_path, output_path):
        try:
            document = Document(str(input_path))
        except Exception:
            raise ConversionError("Plik DOCX jest uszkodzony lub nie jest dokumentem DOCX.")

        lines = []
        for paragraph in document.paragraphs:
            lines.append(paragraph.text)

        try:
            with open(output_path, "w", encoding="utf-8", newline="") as f:
                f.write("\n".join(lines))
        except OSError as e:
            raise ConversionError("Nie można zapisać pliku TXT: " + str(e))
