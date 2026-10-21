import csv
import json

from src.errors import ConversionError
from src.base import Converter


class JsonToCsv(Converter):
    def convert(self, input_path, output_path):
        try:
            with open(input_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ConversionError("Niepoprawny JSON: " + str(e))
        except UnicodeDecodeError:
            raise ConversionError("Plik JSON musi być zapisany w UTF-8.")
        except OSError as e:
            raise ConversionError("Nie można odczytać pliku JSON: " + str(e))

        if not isinstance(data, list):
            raise ConversionError("JSON musi być listą obiektów.")
        for record in data:
            if not isinstance(record, dict):
                raise ConversionError("Każdy element listy JSON musi być poprawnym obiektem.")

        columns = []
        for record in data:
            for key in record:
                if key not in columns:
                    columns.append(key)

        try:
            with open(output_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                for record in data:
                    row = []
                    for column in columns:
                        value = record.get(column)
                        if value is None:
                            row.append("")
                        else:
                            row.append(value)
                    writer.writerow(row)
        except OSError as e:
            raise ConversionError("Nie można zapisać pliku CSV: " + str(e))
