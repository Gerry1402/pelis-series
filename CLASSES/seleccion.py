from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.box import ROUNDED, DOUBLE, SIMPLE, SQUARE, MINIMAL, HEAVY
from rich import print
import readchar, itertools

class Menu:
    def __init__(self, opciones: list, columnas: int = 4):
        self.opciones = opciones
        self.columnas = min(columnas, len(opciones))
        self.n_opciones = len(opciones)
        self.consola = Console()
        self.current_pos = 0
        
        # Precompute panels
        texto = {'style': "white", 'justify': 'center'}
        panel_base = {   
            'border_style': "white",
            'expand': True,
            'box': SQUARE,
            'title_align': 'center',
            'subtitle': '2002'
        }
        self.paneles = [Panel(Text(option, **texto), **panel_base) for option in self.opciones]

    def crear_tabla(self):
        tabla = Table.grid(expand=True)
        [tabla.add_column() for _ in range(self.columnas)]

        # Optimize panel styling in a single pass
        for i, panel in enumerate(self.paneles):
            panel.style = "bold green" if i == self.current_pos else "white"
            panel.border_style = "bold green" if i == self.current_pos else "white"
            panel.box = HEAVY if i == self.current_pos else SQUARE

        # Add rows to the new table
        for i in range(0, len(self.opciones), self.columnas):
            row_display = self.paneles[i:i+self.columnas]
            tabla.add_row(*row_display)

        return tabla

    def mostrar(self):
        with Live(self.crear_tabla(), refresh_per_second=20, console=self.consola, vertical_overflow="ellipsis") as live:
            while True:
                live.update(self.crear_tabla())
                key = readchar.readkey()

                # Simplified navigation with modulo arithmetic
                if key == readchar.key.UP:
                    self.current_pos = (self.current_pos - self.columnas) % self.n_opciones
                elif key == readchar.key.DOWN:
                    self.current_pos = (self.current_pos + self.columnas) % self.n_opciones
                elif key == readchar.key.LEFT:
                    self.current_pos = (self.current_pos - 1) % self.n_opciones
                elif key == readchar.key.RIGHT:
                    self.current_pos = (self.current_pos + 1) % self.n_opciones

                if key == readchar.key.ENTER:
                    return self.opciones[self.current_pos]
                elif key == readchar.key.ESC:
                    return None


result = Menu([f"Option {i}" for i in range(1,21)]).mostrar()

print(result)