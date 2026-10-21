import csv
import json

from src.errors import ConversionError
from src.base import Converter


class CsvToJson(Converter):
    def convert(self, input_path, output_path):
        records = []
        try:
            with open(input_path, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    raise ConversionError("Plik CSV jest pusty (brak nagłówka).")
                for row in reader:
                    record = {}
                    for column in reader.fieldnames:
                        value = row[column]
                        if value is None or value == "":
                            record[column] = None
                        else:
                            record[column] = value
                    records.append(record)
        except UnicodeDecodeError:
            raise ConversionError("Plik CSV musi być zapisany w UTF-8.")
        except OSError as e:
            raise ConversionError("Nie można odczytać pliku CSV: " + str(e))

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise ConversionError("Nie można zapisać pliku JSON: " + str(e))
