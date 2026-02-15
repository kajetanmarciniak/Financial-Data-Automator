import pandas as pd
from pathlib import Path
import pdfplumber
import re
import sys
import os

def resource_path(relative_path):
    """ Potrzebne, jeśli kiedyś zrobisz z tego plik .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def extract_from_pdf(pdf_path):
    """ Wyciąga dane tekstowe z PDF bez użycia AI (szybko i za darmo) """
    data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            # Wzorce dopasowania (RegEx):
            matches = re.findall(r"([^;\n]+);\s*([\d\s,.]+)", text)
            for m in matches:
                user_id = m[0].strip()
                amount = m[1].strip()
                data.append({'ID_USERS': user_id, 'Wyplata': amount})
    except Exception as e:
        print(f"⚠️ Błąd odczytu PDF {pdf_path.name}: {e}")
    return data

def find_data_folder():
    """ Szuka folderu PLIKI w kilku miejscach """
    base_dir = Path(sys.argv[0]).parent
    paths = [
        base_dir / "PLIKI",
        Path.cwd() / "PLIKI",
        Path.home() / "Desktop" / "PLIKI",
        Path.home() / "OneDrive" / "Desktop" / "PLIKI"
    ]
    for p in paths:
        if p.exists() and p.is_dir():
            return p
    return None

def main():
    folder = find_data_folder()
    
    if not folder:
        print("❌ NIE ZNALEZIONO FOLDERU 'PLIKI'!")
        print("Stwórz folder o nazwie PLIKI obok tego programu i wrzuć tam dokumenty.")
        input("\nNaciśnij Enter, aby zamknąć..."); return

    print(f"📂 Folder źródłowy: {folder}")
    all_extracted_data = []

    for file_path in folder.glob("*.*"):
        if file_path.name.startswith("RAPORT"): continue
        
        # 1. PRZETWARZANIE EXCEL / CSV
        if file_path.suffix in ['.xlsx', '.xls', '.csv']:
            try:
                df = pd.read_csv(file_path, sep=None, engine='python') if file_path.suffix == '.csv' else pd.read_excel(file_path)
                
                # --- INTELIGENTNE SZUKANIE ---
                cols = [str(c).lower() for c in df.columns]
                
                id_idx = next((i for i, c in enumerate(cols) if any(k in c for k in ['id', 'user', 'name', 'osoba', 'pracownik', 'identy'])), None)
                val_idx = next((i for i, c in enumerate(cols) if any(k in c for k in ['wyplata', 'salary', 'total', 'amount', 'suma', 'kasa', 'kwota', 'wynagro'])), None)

                if id_idx is not None and val_idx is not None:
                    print(f"📊 Czytam Excel: {file_path.name} (Znalazłem: {df.columns[id_idx]} + {df.columns[val_idx]})")
                    temp_df = df.iloc[:, [id_idx, val_idx]].copy()
                    temp_df.columns = ['ID_USERS', 'Wyplata']
                    all_extracted_data.append(temp_df.dropna())
            except Exception as e:
                print(f"⚠️ Pominąłem Excel {file_path.name} (Błąd: {e})")

        # 2. PRZETWARZANIE PDF
        elif file_path.suffix == '.pdf':
            print(f"📄 Czytam PDF: {file_path.name}")
            pdf_data = extract_from_pdf(file_path)
            if pdf_data:
                all_extracted_data.append(pd.DataFrame(pdf_data))

    # --- GENEROWANIE RAPORTU ---
    if all_extracted_data:
        final_df = pd.concat(all_extracted_data, ignore_index=True)
        final_df['Wyplata'] = final_df['Wyplata'].astype(str).str.replace(',', '.')
        final_df['Wyplata'] = pd.to_numeric(final_df['Wyplata'].str.extract(r'(\d+\.?\d*)')[0], errors='coerce')
        
        report = final_df.groupby('ID_USERS', as_index=False)['Wyplata'].sum()
        output_path = folder / "RAPORT_ZBIORCZY.xlsx"
        report.to_excel(output_path, index=False)
        
        print("-" * 30)
        print(f"✅ SUKCES! Utworzono raport: {output_path.name}")
        print(f"💰 Suma wszystkich płatności: {report['Wyplata'].sum():.2f}")
        print("-" * 30)
    else:
        print("❌ Nie znaleziono żadnych danych w plikach.")

    input("\nNaciśnij Enter, aby zakończyć...")

if __name__ == "__main__":
    main()
