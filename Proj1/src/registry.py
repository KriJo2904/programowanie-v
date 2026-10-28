from pathlib import Path

from src.errors import ConversionError
from src.converters.to_csv.json_to_csv import JsonToCsv
from src.converters.to_json.csv_to_json import CsvToJson
from src.converters.to_docx.txt_to_docx import TxtToDocx
from src.converters.to_txt.docx_to_txt import DocxToTxt
from src.converters.to_pdf.docx_to_pdf import DocxToPdf
from src.converters.to_pdf.odt_to_pdf import OdtToPdf

REGISTRY = {
    (".csv", ".json"): CsvToJson(),
    (".json", ".csv"): JsonToCsv(),
    (".txt", ".docx"): TxtToDocx(),
    (".docx", ".txt"): DocxToTxt(),
    (".docx", ".pdf"): DocxToPdf(),
    (".odt", ".pdf"): OdtToPdf(),
}


def convert(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise ConversionError("Plik wejściowy nie istnieje: " + str(input_path))

    pair = (input_path.suffix.lower(), output_path.suffix.lower())
    if pair not in REGISTRY:
        raise ConversionError("Nieobsługiwana konwersja: %s -> %s" % pair)

    REGISTRY[pair].convert(input_path, output_path)
