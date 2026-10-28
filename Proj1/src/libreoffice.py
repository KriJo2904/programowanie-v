import shutil
import subprocess
import tempfile
from pathlib import Path

from src.errors import ConversionError

MAC_PATH = "/Applications/LibreOffice.app/Contents/MacOS/soffice"


def find_soffice():
    path = shutil.which("soffice")
    if path is None and Path(MAC_PATH).is_file():
        path = MAC_PATH
    return path


def convert_to_pdf(input_path, output_path):
    soffice = find_soffice()
    if soffice is None:
        raise ConversionError(
            "Nie znaleziono LibreOffice (polecenie soffice). "
            "Zainstaluj LibreOffice i spróbuj ponownie."
        )

    with tempfile.TemporaryDirectory() as temp_dir:
        command = [soffice, "--headless", "--convert-to", "pdf",
                   "--outdir", temp_dir, str(input_path)]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            raise ConversionError("LibreOffice nie zakończył pracy w ciągu 120 s.")
        except OSError as e:
            raise ConversionError("Nie można uruchomić LibreOffice: " + str(e))

        if result.returncode != 0:
            raise ConversionError(
                "LibreOffice zakończył się błędem (kod %d): %s"
                % (result.returncode, result.stderr.strip())
            )

        created = Path(temp_dir) / (Path(input_path).stem + ".pdf")
        if not created.is_file():
            raise ConversionError("LibreOffice nie utworzył pliku PDF (plik wejściowy może być uszkodzony).")

        try:
            shutil.move(str(created), str(output_path))
        except OSError as e:
            raise ConversionError("Nie można zapisać pliku PDF: " + str(e))
