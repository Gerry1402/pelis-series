import os
from .start import *
from .proceso import *
from rich.progress import Progress



# tiempo_base = time.time()

# for i, archivo in enumerate(archivos, start=1):

#     proceso(archivo)

#     tamaño_analizado += os.path.getsize(archivo)

#     porcentaje = tamaño_analizado/tamaño_total

#     tiempo = int(time.time()-tiempo_base)

#     print(f'Multiplexar: {i}/{n_archivos}   {round(porcentaje*100, 2)}%.   {int(((1/porcentaje)-1) * tiempo)} segundos restantes         ',end='\r')

def main():
    with Progress(transient=False) as progreso:
        principal = progreso.add_task(f"Progreso Total ({n_archivos} archivos)", total=tamaño_total)
        # Barra de progreso total
        for id, archivo in enumerate(archivos, start=1):
            nombre = os.path.splitext(os.path.basename(archivo))[0]
            progreso.add_task(f"{nombre[:28]}{'...' if nombre[:28] != nombre else ''}", total=100)
            
            # for id, archivo in enumerate(archivos, start=(i-1)*(numero_archivos_conjunto+1)+2):
            proceso_consola(archivo, progreso, id)  # Procesar la parte
            progreso.update(principal, advance=os.path.getsize(archivo))  # Avanzar en el progreso total

if __name__ == '__main__':
    main()