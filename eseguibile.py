import os
from info_fits import info_fits
from view_fits import view_fits
from view_LOG_fits import view_LOG_fits

def main():
    cartella_principale = os.path.dirname(os.path.abspath(__file__))

    output_file = os.path.join(
        cartella_principale,
        "informazioni_fits.txt"
    )

    info_fits(output_file)
    view_fits()
    view_LOG_fits()

if __name__ == "__main__":
    main()
