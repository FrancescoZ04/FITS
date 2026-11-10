from fits_utils import get_fits_files, open_fits_file
import requests


def info_fits(output_filename="informazioni_fits.txt"):

    headers = [
        "Nome file", "Matrice", "Data", "Tipo Immagine",
        "Strumento", "Filtro", "Alpha", "Delta"
    ]

    table_data = [headers]

    with requests.Session() as session:

        file_list = get_fits_files(session)

        if not file_list:
            print("Nessun file FITS trovato nella repository.")
            return

        print(f"File FITS trovati: {len(file_list)}")

        for elemento in file_list:

            filename = elemento["name"]

            try:
                with open_fits_file(
                    session, elemento["download_url"]
                ) as hdul:

                    header = hdul[0].header
                    data = hdul[0].data

                    matrice = (
                        str(data.shape)
                        if data is not None
                        else "(Nessun Dato)"
                    )

                    riga = [
                        filename,
                        matrice,
                        header.get("DATE-OBS", "N/A"),
                        header.get("IMAGETYP", "N/A"),
                        header.get("INSTRUME", "N/A"),
                        header.get("FILTER", "N/A"),
                        header.get("RA", "N/A"),
                        header.get("DEC", "N/A")
                    ]

            except Exception as errore:
                print(f"Errore nella lettura di {filename}: {errore}")
                riga = [filename] + ["Errore"] * 7

            table_data.append([str(valore) for valore in riga])

    col_widths = [
        max(len(riga[i]) for riga in table_data)
        for i in range(len(headers))
    ]

    with open(output_filename, "w", encoding="utf-8") as file:

        for indice, riga in enumerate(table_data):

            formatted_row = " | ".join(
                valore.ljust(col_widths[i])
                for i, valore in enumerate(riga)
            )

            file.write(formatted_row + "\n")

            if indice == 0:
                separator = "-+-".join(
                    "-" * width for width in col_widths
                )
                file.write(separator + "\n")

    print(f"\nTabella salvata correttamente in:\n{output_filename}")
