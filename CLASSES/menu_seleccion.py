from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.box import ROUNDED, DOUBLE, SIMPLE, SQUARE, MINIMAL, HEAVY
from rich import print
import readchar

class PanelBase:
    def __init__(self, texto='', color='white', color_text = '', title='', subtitulo='', heavy=False):
        self.texto = texto
        self.color = color
        self.color_text = color_text
        self.titulo = title
        self.subtitulo = f' ({subtitulo})' if subtitulo else ''
        self.grosor = HEAVY if heavy else SQUARE
    def crear_panel(self):
        self.color_text = self.color_text or self.color
        return Panel(Text(self.texto, justify='center', style=self.color_text), expand=True, border_style=self.color, box=self.grosor, subtitle=self.subtitulo, title=self.titulo)

class BaseMenu:
    def __init__(self, pregunta: str, opciones: list, columnas: int = 4, subtitulos: list = None, titulos: list = None):
        self.pregunta = pregunta
        self.opciones = opciones
        self.n_opciones = len(opciones)
        self.columnas = min(columnas, self.n_opciones)
        self.filas = len(opciones) // self.columnas + (1 if len(opciones) % columnas else 0)
        self.restantes_fila = (self.n_opciones % self.columnas) if self.filas > 1 else 0
        self.consola = Console()
        self.current_pos = 0
        self.subtitulos = subtitulos or ['' for _ in range(self.n_opciones)]
        self.titulos = titulos or ['' for _ in range(self.n_opciones)]
        self.nav_config = {
            readchar.key.DOWN: {
                'criticos_2': range(self.n_opciones - self.columnas, self.n_opciones-self.restantes_fila),
                'criticos_1': range(self.n_opciones - self.restantes_fila, self.n_opciones)
            },
            readchar.key.UP: {
                'criticos_1': range(self.restantes_fila),
                'criticos_2': range(self.restantes_fila, self.columnas)
            }
        }

    def _crear_tabla(self):
        tabla = Table.grid(expand=True)
        [tabla.add_column() for _ in range(self.columnas)]

        paneles = []
        for i in range(self.n_opciones):
            panel = PanelBase(self.opciones[i])
            if i == self.current_pos:
                panel.color = 'red' if hasattr(self, 'selected_options') and i in self.selected_options else 'green'
                panel.grosor = HEAVY
            elif hasattr(self, 'selected_options') and i in self.selected_options:
                panel.color = 'yellow'
            panel.subtitulo = self.subtitulos[i]
            panel.titulo = self.titulos[i]
            paneles.append(panel.crear_panel())
            if ((i+1)%self.columnas == 0 and i != 0) or i == self.n_opciones - 1:
                tabla.add_row(*paneles)
                paneles = []

        return tabla

    def _cambiar_pos_arr_abaj(self, key):
        simbolo = 1 if key == readchar.key.DOWN else -1
        criticos_1 = self.nav_config[key]['criticos_1']
        criticos_2 = self.nav_config[key]['criticos_2']
        if self.current_pos not in criticos_1 and self.current_pos not in criticos_2:
            return self.columnas * simbolo
        elif self.current_pos in criticos_1:
            return self.restantes_fila * simbolo
        return (self.columnas + self.restantes_fila) * simbolo

    def _cambiar_pos(self, key):
        if key in [readchar.key.UP, readchar.key.DOWN]:
            valor = self._cambiar_pos_arr_abaj(key)
        elif key in [readchar.key.LEFT, readchar.key.RIGHT]:
            valor = - 1 if key == readchar.key.LEFT else + 1
        self.current_pos = (self.current_pos + valor) % self.n_opciones

    def _mostrar_base(self, index=False, multi_select=False):
        self.consola.print(Panel(Text(self.pregunta, style='box', justify='center'), box=SIMPLE, expand=True))
        with Live(self._crear_tabla(), refresh_per_second=20, console=self.consola, vertical_overflow="ellipsis") as live:
            while True:
                live.update(self._crear_tabla())
                key = readchar.readkey()

                if key in [readchar.key.UP, readchar.key.DOWN, readchar.key.LEFT, readchar.key.RIGHT]:
                    self._cambiar_pos(key)

                elif key == ' ' and multi_select:
                    self._seleccionar_desselecionar(self.current_pos)

                elif key == readchar.key.ENTER:
                    if not multi_select:
                        return self.current_pos if index else self.opciones[self.current_pos]

                    if index:
                        return sorted(self.selected_options)
                    return [self.opciones[idx] for idx in sorted(self.selected_options)]

                elif key == readchar.key.ESC:
                    return [] if multi_select else None


class MultiSelectMenu(BaseMenu):
    def __init__(self, opciones: list, columnas: int = 4, subtitulos: list = None, titulos: list = None, max_selections=None):
        super().__init__(opciones, columnas, subtitulos, titulos)
        self.selected_options = set()
        self.max_selections = max_selections or self.n_opciones

    def _seleccionar_desselecionar(self, idx):
        if idx in self.selected_options:
            self.selected_options.remove(idx)
        elif len(self.selected_options) < self.max_selections:
            self.selected_options.add(idx)

    def mostrar(self, index=False):
        return self._mostrar_base(index=index, multi_select=True)


class Menu(BaseMenu):
    def mostrar(self, index=False):
        return self._mostrar_base(index=index, multi_select=False)