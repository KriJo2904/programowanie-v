from src.base import Converter
from src.libreoffice import convert_to_pdf


class DocxToPdf(Converter):
    def convert(self, input_path, output_path):
        convert_to_pdf(input_path, output_path)
