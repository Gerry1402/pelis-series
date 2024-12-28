from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED, DOUBLE, SIMPLE, SQUARE, MINIMAL, HEAVY

class InfoEtiquetas:
    def __init__(self, enunciado: str, etiquetas: list, columnas: int = None):
        self.enunciado = enunciado
        self.etiquetas = etiquetas
        self.columnas = columnas or len(etiquetas)
        self.consola = Console()
    
    def _panel(self):
        return Panel(Text(self.enunciado, justify='center', style='white'), expand=True, box=SIMPLE)
    
    def _tabla(self):
        tabla = Table.grid(expand=True)
        [tabla.add_column() for _ in range(self.columnas)]
        fila = []
        for i, etiqueta in enumerate(self.etiquetas):
            fila.append(Panel(Text(etiqueta, justify='center', style='white'), expand=True, box=ROUNDED))
            if ((i+1)%self.columnas == 0 and i != 0) or i == len(self.etiquetas) - 1:
                tabla.add_row(fila)
                fila = []
        return tabla
    
    def mostrar(self):
        self.consola.print(self._panel())
        self.consola.print(self._tabla())