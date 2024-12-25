import os
from .start import *
from .proceso import *
from rich.progress import Progress


def main():
    with Progress() as progreso:
        # Barra de progreso total
        principal = progreso.add_task("Progreso Total", total=tamaño_total)
        
        for archivo in archivos:
            nombre = os.path.splitext(os.path.basename(archivo))[0]
            progreso.add_task(f"{nombre[:28]}{'...' if nombre[:28] != nombre else ''}", total=100)
        
        for id, archivo in enumerate(archivos, start=1):
            proceso_consola(archivo, progreso, id)  # Procesar la parte
            progreso.update(principal, advance=os.path.getsize(archivo))  # Avanzar en el progreso total

if __name__ == '__main__':
    main()