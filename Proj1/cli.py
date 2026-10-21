import sys

from src.errors import ConversionError
from src.registry import convert

if len(sys.argv) != 3:
    print("Użycie: python cli.py plik_wejsciowy plik_wyjsciowy")
    sys.exit(1)

try:
    convert(sys.argv[1], sys.argv[2])
    print("Gotowe: " + sys.argv[2])
except ConversionError as e:
    print("Błąd: " + str(e))
    sys.exit(1)
