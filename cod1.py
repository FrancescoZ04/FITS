import os
import requests
from io import BytesIO
from astropy.io import fits


def informazioni_fits(output_filename="informazioni_fits.txt"):

    repository = "FrancescoZ04/FITS"
    cartella = "FITS"
    branch = "main"

    url = (
        f"https://api.github.com/repos/{repository}/contents/"
        f"{cartella}?ref={branch}"
    )

    risposta = requests.get(url)
    risposta.raise_for_status()

    contenuti = risposta.json()

    file_list = [
        elemento for elemento in contenuti
        if elemento["type"] == "file"
        and elemento["name"].lower().endswith((".fits", ".fts"))
    ]

    if not file_list:
        print("Nessun file FITS trovato nella repository.")
        return

    headers = [
        "Nome file", "Matrice", "Data", "Tipo Immagine",
        "Strumento", "Filtro", "Alpha", "Delta"
    ]

    table_data = [headers]

    print(f"File FITS trovati: {len(file_list)}")

    for elemento in sorted(file_list, key=lambda x: x["name"]):

        filename = elemento["name"]

        try:
            download = requests.get(elemento["download_url"])
            download.raise_for_status()

            with fits.open(BytesIO(download.content)) as hdul:

                header = hdul[0].header
                data = hdul[0].data

                matrice = str(data.shape) if data is not None else "(Nessun Dato)"

                data_obs = header.get("DATE-OBS", "N/A")
                tipo_img = header.get("IMAGETYP", "N/A")
                strumento = header.get("INSTRUME", "N/A")
                filtro = header.get("FILTER", "N/A")
                ra = header.get("RA", "N/A")
                dec = header.get("DEC", "N/A")

        except Exception as e:

            print(f"Errore nella lettura di {filename}: {e}")

            matrice = "Errore"
            data_obs = "Errore"
            tipo_img = "Errore"
            strumento = "Errore"
            filtro = "Errore"
            ra = "Errore"
            dec = "Errore"

        table_data.append([
            filename,
            matrice,
            str(data_obs),
            str(tipo_img),
            str(strumento),
            str(filtro),
            str(ra),
            str(dec)
        ])

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

    output_file = os.path.join(
        cartella_principale,
        "informazioni_fits.txt"
    )

    informazioni_fits(output_file)
