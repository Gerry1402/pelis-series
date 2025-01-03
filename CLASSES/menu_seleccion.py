from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.box import ROUNDED, DOUBLE, SIMPLE, SQUARE, MINIMAL, HEAVY
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
    def __init__(self, enunciado: str, opciones: list, columnas: int = 4, subtitulos: list = None, colores: list = None, titulos: list = None, limite: int = None, nombre_limite:str = 'Más'):
        self.enunciado = enunciado
        self.limite = None
# sourcery skip: merge-nested-ifs
        if limite:
            if limite < len(opciones):
                self.limite = limite
        self.limitado = self.limite < len(opciones) if self.limite else False
        self.opciones_completas = opciones
        self.opciones = opciones[:limite]+[nombre_limite] if self.limite else opciones
        self.n_opciones = len(self.opciones)
        self.columnas_original = columnas
        self.columnas = self.limite + 1 if self.limite else min(columnas, self.n_opciones)
        self.filas = len(self.opciones) // self.columnas + (1 if len(self.opciones) % columnas else 0)
        self.restantes_fila = (self.n_opciones % self.columnas) if self.filas > 1 else 0
        self.consola = Console()
        self.current_pos = 0
        self.subtitulos = subtitulos
        self.titulos = titulos
        self.colores = colores if type(colores)==list and len(colores) == 3 else ['#ff0000', '#ff7f00', '#ffff00']
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
        [tabla.add_column(ratio=1) for _ in range(self.columnas)]

        paneles = []
        for i in range(self.n_opciones):
            panel = PanelBase(self.opciones[i])
            if i == self.current_pos:
                panel.color = self.colores[2] if hasattr(self, 'selected_options') and i in self.selected_options else self.colores[0]
                panel.grosor = HEAVY
            elif hasattr(self, 'selected_options') and i in self.selected_options:
                panel.color = self.colores[1]
            if (i != self.limite and self.limitado) or not self.limitado:
                if self.subtitulos:
                    panel.subtitulo = self.subtitulos[i]
                if self.titulos:
                    panel.titulo = self.titulos[i]
            paneles.append(panel.crear_panel())
            if (i+1)%self.columnas == 0 and i != 0:
                tabla.add_row(*paneles)
                paneles = []
        if paneles:
            tabla.add_row(*paneles, end_section=True)

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
    
    def _update_dimensions(self):
        self.limitado = False
        self.opciones = self.opciones_completas
        self.n_opciones = len(self.opciones)
        self.columnas = self.columnas_original
        self.filas = len(self.opciones) // self.columnas + (1 if len(self.opciones) % self.columnas else 0)
        self.restantes_fila = (self.n_opciones % self.columnas) if self.filas > 1 else 0
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

    def _mostrar_base(self, index=False, multi_select=False):
        self.consola.print(Panel(Text(self.enunciado, style='box', justify='center'), box=SIMPLE, expand=True))
        with Live(self._crear_tabla(), refresh_per_second=20, console=self.consola, vertical_overflow="ellipsis") as live:
            while True:
                live.update(self._crear_tabla())
                key = readchar.readkey()

                if key in [readchar.key.UP, readchar.key.DOWN, readchar.key.LEFT, readchar.key.RIGHT]:
                    self._cambiar_pos(key)

                elif key == ' ' and multi_select:
                    self._seleccionar_desselecionar(self.current_pos)

                elif key == readchar.key.ENTER:
                    if self.current_pos == self.limite and self.limitado:
                        self._update_dimensions()
                    elif not multi_select:
                        return self.current_pos if index else self.opciones[self.current_pos]
                    elif index:
                        return sorted(self.selected_options)
                    else:
                        return [self.opciones[idx] for idx in sorted(self.selected_options)]

                elif key == readchar.key.ESC:
                    return [] if multi_select else None


class MultiSelectMenu(BaseMenu):
    def __init__(self, enunciado: str, opciones: list, columnas: int = 4, subtitulos: list = None, titulos: list = None, max_selections=None, limite: int=None, nombre_limite: str='Más'):
        super().__init__(enunciado, opciones, columnas, subtitulos, titulos, limite, nombre_limite)
        self.selected_options = set()
        self.max_selections = max_selections or self.n_opciones

    def _seleccionar_desselecionar(self, idx):
        if not (self.current_pos == self.limite and self.limitado):
            if idx in self.selected_options:
                self.selected_options.remove(idx)
            elif len(self.selected_options) < self.max_selections:
                self.selected_options.add(idx)

    def mostrar(self, index=False):
        return self._mostrar_base(index=index, multi_select=True)


class Menu(BaseMenu):
    def mostrar(self, index=False):
        return self._mostrar_base(index=index, multi_select=False)