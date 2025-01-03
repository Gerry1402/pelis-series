from .start import *
from .proceso import *
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
import time


def main():

    console = Console()
    tiempo_base = time.time()

    def crear_tabla(progreso_total, archivo_actual, avance_actual, tiempo_base, tiempo_parcial):
        tabla = Table.grid(expand=True)
        tabla.add_column(ratio=4)
        [tabla.add_column(ratio=1) for i in range(2)]
        tabla.add_row('', Text('Tiempo Restante', justify='center'), Text('Progreso Actual', justify='center'))
        tabla.add_row('Progreso Total', Text(f'{int((100/progreso_total-1)*tiempo_base)} segundos', justify='center'),Text(f"{progreso_total:.2f}%", justify='center'))
        tabla.add_row(f'{archivo_actual}', Text(f'{int((100/avance_actual-1)*tiempo_parcial)} segundos', justify='center'), Text(f'{avance_actual}%', justify='center'))
        return tabla

    with Live(console=console) as live:
        tamaño_analizado = 0
        for i, video in enumerate(videos):
            nombre_video = os.path.splitext(os.path.basename(video))[0]
            tamaño_video = os.path.getsize(video)
            if hacer_audios:
                tamaño_video += os.path.getsize(audios[i])
            if hacer_subtitulos:
                tamaño_video += os.path.getsize(subtitulos[i])
            tiempo_parcial = time.time()
            for avance in proceso(i):
                porcentaje = tamaño_video * (avance / 100)
                progreso_total = (tamaño_analizado + porcentaje) * 100 / tamaño_total
                if progreso_total != 0 and avance != 0:
                    live.update(crear_tabla(progreso_total, nombre_video, avance, time.time() - tiempo_base, time.time() - tiempo_parcial))
            tamaño_analizado += tamaño_video

if __name__ == '__main__':
    main()
