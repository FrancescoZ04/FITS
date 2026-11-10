import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import requests
from fits_utils import get_fits_files, open_fits_file


def view_LOG_fits():
    # Definizione della cartella di output locale per le immagini
    cartella_principale = os.path.dirname(os.path.abspath(__file__))
    cartella_output = os.path.join(cartella_principale, "ImmaginiLOG")

    os.makedirs(cartella_output, exist_ok=True)

    # Utilizziamo requests.Session() per ottimizzare le richieste HTTP
    with requests.Session() as session:
        file_list = get_fits_files(session)

        if not file_list:
            print("Nessun file FITS trovato nella repository.")
            return

        print(f"File FITS trovati: {len(file_list)}")

        for elemento in sorted(file_list, key=lambda x: x["name"]):
            filename = elemento["name"]

            try:
                with open_fits_file(session, elemento["download_url"]) as hdul:
                    data = hdul[0].data
                    header = hdul[0].header

                    tipo_img = str(header.get("IMAGETYP", "N/A")).upper()

                    if data is None:
                        print(f"Nessun dato trovato in {filename}.")
                        continue

                    data = np.asarray(data, dtype=float)

                    valori_positivi = data[
                        np.isfinite(data) & (data > 0)
                    ]

                    if len(valori_positivi) == 0:
                        print(f"Nessun valore positivo in {filename}.")
                        continue

                    fig, ax = plt.subplots(figsize=(9, 7))

                    immagine = ax.imshow(
                        data,
                        cmap="gray",
                        origin="lower",
                        norm=LogNorm(
                            vmin=valori_positivi.min(),
                            vmax=valori_positivi.max()
                        )
                    )

                    fig.colorbar(
                        immagine,
                        ax=ax,
                    )

                    ax.set_title(f"{filename}\nTipo: {tipo_img}")
                    ax.set_xlabel("X")
                    ax.set_ylabel("Y")

                    fig.tight_layout()

                    nome_immagine = os.path.splitext(filename)[0] + ".png"
                    percorso_output = os.path.join(
                        cartella_output,
                        nome_immagine
                    )

                    fig.savefig(
                        percorso_output,
                        dpi=200,
                        bbox_inches="tight"
                    )

                    plt.close(fig)

                    print(f"Immagine salvata: {nome_immagine}")

            except Exception as e:
                print(f"Errore nella visualizzazione di {filename}: {e}")

    print(f"\nImmagini salvate nella cartella:\n{cartella_output}")