import os
import requests
import matplotlib.pyplot as plt

from fits_utils import get_fits_files, open_fits_file


def view_fits():

    # Cartella di salvataggio delle immagini
    cartella_principale = os.path.dirname(os.path.abspath(__file__))
    cartella_output = os.path.join(cartella_principale, "Immagini")

    os.makedirs(cartella_output, exist_ok=True)

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

                    data = hdul[0].data
                    header = hdul[0].header

                    if data is None:
                        print(f"Nessun dato disponibile in {filename}.")
                        continue

                    tipo_img = str(
                        header.get("IMAGETYP", "N/A")
                    ).upper()

                    # Creazione della figura
                    fig, ax = plt.subplots(figsize=(9, 7))

                    try:
                        immagine = ax.imshow(
                            data,
                            cmap="gray",
                            origin="lower"
                        )

                        fig.colorbar(
                            immagine,
                            ax=ax,
                            orientation="vertical",
                            pad=0.04
                        )

                        ax.set_title(
                            f"{filename} - Tipo: {tipo_img}"
                        )
                        ax.set_xlabel("X")
                        ax.set_ylabel("Y")

                        fig.tight_layout()

                        nome_immagine = (
                            os.path.splitext(filename)[0] + ".png"
                        )

                        percorso_output = os.path.join(
                            cartella_output,
                            nome_immagine
                        )

                        fig.savefig(
                            percorso_output,
                            dpi=200,
                            bbox_inches="tight"
                        )

                        print(f"Immagine salvata: {nome_immagine}")

                    finally:
                        plt.close(fig)

            except Exception as errore:
                print(
                    f"Errore nella visualizzazione di "
                    f"{filename}: {errore}"
                )

    print(f"\nImmagini salvate nella cartella:\n{cartella_output}")
