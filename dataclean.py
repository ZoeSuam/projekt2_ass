import re


def clean_and_merge_txt_files(file_paths, output_file_path):
    """
    Entfernt HTML-Tags aus den angegebenen Textdateien und fügt sie zu einer einzigen Datei zusammen.

    :param file_paths: Liste der Pfade zu den Textdateien.
    :param output_file_path: Pfad zur Ausgabedatei.
    """
    html_tag_re = re.compile(r'<[^>]+>')  # Regex zum Finden von HTML-Tags

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    content = input_file.read()
                    cleaned_content = html_tag_re.sub('', content)  # Entferne HTML-Tags
                    output_file.write(cleaned_content + '\n\n')  # Füge etwas Abstand zwischen den Dateiinhalten hinzu
                print(f"Datei {file_path} wurde verarbeitet.")
            except FileNotFoundError:
                print(f"Datei {file_path} wurde nicht gefunden und übersprungen.")
            except Exception as e:
                print(f"Ein Fehler ist bei der Verarbeitung der Datei {file_path} aufgetreten: {e}")

def start():
    # Beispiel für die Verwendung der Funktion
    file_paths = ['data/Zusammengefasste_Inhalte_Bilanzierung.txt', 'data/Zusammengefasste_Inhalte_Finanzwissen.txt', 'data/Zusammengefasste_Inhalte_Investitionsrechnung.txt', 'data/Zusammengefasste_Inhalte_Kostenrechnung.txt',
                  'data/Zusammengefasste_Inhalte_Unternehmensziele.txt','data/Zusammengefasste_Inhalte_Wirtschaftsrecht.txt']
    output_file_path = 'data/lernpakete.txt'
    clean_and_merge_txt_files(file_paths, output_file_path)


if __name__ == '__main__':
    start()

