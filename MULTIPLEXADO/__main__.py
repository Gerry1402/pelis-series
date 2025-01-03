import os, time
from .start import *
from .proceso import *
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text

def main():

    console = Console()
    tiempo = time.time()

    def crear_tabla(progreso_total, archivo_actual, avance_actual, tiempo):
        tabla = Table.grid(expand=True)
        tabla.add_column(ratio=4)
        [tabla.add_column(ratio=1) for i in range(2)]
        tabla.add_row('', Text('Tiempo Restante', justify='center'), Text('Progreso Actual', justify='center'))
        tabla.add_row('Progreso Total', Text(f'{int((100/progreso_total-1)*tiempo)} segundos', justify='center'),Text(f"{progreso_total:.2f}%", justify='center'))
        tabla.add_row(f'{archivo_actual}', Text(f'{int((100/avance_actual-1)*tiempo)} segundos', justify='center'), Text(f'{avance_actual}%', justify='center'))
        return tabla

    with Live(console=console) as live:
        tamaño_analizado = 0
        for archivo in archivos:
            nombre_archivo = os.path.splitext(os.path.basename(archivo))[0]
            tamaño_archivo = os.path.getsize(archivo)
            for avance in proceso(archivo):
                porcentaje = tamaño_archivo * (avance / 100)
                progreso_total = (tamaño_analizado + porcentaje) * 100 / tamaño_total
                if progreso_total != 0:
                    live.update(crear_tabla(progreso_total, nombre_archivo, avance, time.time() - tiempo))
            tamaño_analizado += os.path.getsize(archivo)

if __name__ == '__main__':
    main()