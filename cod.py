import os
import glob
from astropy.io import fits

def informazioni_fits(directory_path, output_filename="informazioni_fits.txt"):
    file_list = []

    for filepath in glob.glob(os.path.join(directory_path, "*")):
        if filepath.lower().endswith((".fits", ".fts")):
            file_list.append(filepath)
            
    if not file_list:
        print(f"Nessun file FITS trovato nella directory: {directory_path}")
        return

    headers = ["Nome file","Matrice","Data","Tipo Immagine","Strumento","Alpha","Delta"]

    table_data = [headers]

    print(f"File FITS trovati: {len(file_list)}")

    for filepath in sorted(file_list):
        filename = os.path.basename(filepath)
        try:
            with fits.open(filepath) as hdul:
                header = hdul[0].header
                data = hdul[0].data

                if data is not None:
                    matrice = str(data.shape)
                else:
                    matrice = "(Nessun Dato)"

                data_obs = header.get("DATE-OBS", "N/A")
                tipo_img = header.get("IMAGETYP", "N/A")
                strumento = header.get("INSTRUME", "N/A")
                ra = header.get("RA", "N/A")
                dec = header.get("DEC", "N/A")

                #if isinstance(ra, (int, float)):
                #    ra = f"{ra:.4f}"

                #if isinstance(dec, (int, float)):
                #   dec = f"{dec:.4f}"

        except Exception as e:
            print(f"Errore nella lettura di {filename}: {e}")
            matrice = "Errore"
            data_obs = "Errore"
            tipo_img = "Errore"
            strumento = "Errore"
            ra = "Errore"
            dec = "Errore"

        table_data.append([filename, matrice, str(data_obs), str(tipo_img), str(strumento), str(ra), str(dec)])

    col_widths = [
        max(len(str(row[i])) for row in table_data)
        for i in range(len(headers))
    ]

    with open(output_filename, "w", encoding="utf-8") as f:
        for row in table_data:
            formatted_row = " | ".join(
                str(val).ljust(col_widths[i])
                for i, val in enumerate(row)
            )
            f.write(formatted_row + "\n")

            if row == headers:
                separator = "-+-".join(
                    "-" * col_widths[i]
                    for i in range(len(headers))
                )
                f.write(separator + "\n")

    print(f"\nTabella salvata correttamente in:\n{output_filename}")

if __name__ == "__main__":
    cartella_principale = os.path.dirname(os.path.abspath(__file__))

    cartella_fits = os.path.join(cartella_principale, "FITS")

    output_file = os.path.join(
        cartella_principale,
        "informazioni_fits.txt"
    )

    informazioni_fits(cartella_fits, output_file)