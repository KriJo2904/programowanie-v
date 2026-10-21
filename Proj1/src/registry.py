from pathlib import Path

from src.errors import ConversionError
from src.converters.to_csv.json_to_csv import JsonToCsv
from src.converters.to_json.csv_to_json import CsvToJson

REGISTRY = {
    (".csv", ".json"): CsvToJson(),
    (".json", ".csv"): JsonToCsv(),
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
