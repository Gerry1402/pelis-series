import os, cv2, subprocess, re
from pymkv import MKVTrack as mkvt, MKVFile as mkvf, MKVAttachment as mkva
from typing import Union, List, Dict
from rich.progress import Progress

iso6392 = ['cat', 'spa', 'eng', 'jpn', 'ita', 'fra']
idiomas_sub = ['Subtítols', 'Subtítulos', 'Subtitles', '字幕', 'Sottotitoli', 'Sous-titres']
idiomas_forz = ['Subtítols Forçats', 'Subtítulos Forzados', 'Subtitles Forced', '強制字幕', 'Sottotitoli forzati', 'Sous-titres forcés']
sub = {iso6392[i]: idiomas_sub[i] for i in range(len(iso6392))}
forz = {iso6392[i]: idiomas_forz[i] for i in range(len(iso6392))}

class MKV: #Clase para archivos MKV

    def __init__(self, archivo_mkv:str):
        self.dir: str = archivo_mkv
        self.archivo = mkvf(self.dir)
        self.lenguajes = [track.language for track in self.archivo.tracks]
        self.subtitulos = []
        self.audios = []
        self.nombre: str = os.path.splitext(os.path.basename(self.dir))[0]
        self.carpeta: str = os.path.join(os.path.dirname(self.dir), self.nombre)
        self.cap = cv2.VideoCapture(self.dir)
        self.ancho: int = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.alto: int = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.nuevo_ancho_alto: List[str] = None
        self.frames_totales: int = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps: float = self.cap.get(cv2.CAP_PROP_FPS)
        self.tiempo_total: int = int(self.frames_totales / self.fps * 100)/100
        self.split_inicio: bool = None
        self.split_final: bool = None

    def detalles(self, type: Union[str, List[str]] = None) -> List[dict]:
        """
        Esta funcion permite obtener los detalles de las pistas de un archivo mkv de manera fácil y organizada.\n
        detalles(type = [''audio', 'subtitles', ...])\n
        detalles(type = 'subtitles')

        Args:
            type (str or list[str]], optional): Tipos de archivo que se quieran analizar. Las opciones son 'video', 'audio' y 'subtitles'

        Returns:
            list[dict]: El resultado es una lista ordenada en la que aparecen las categrías 'id', 'name', 'type' y 'codec'. Dependiendo del tipo de pista, se añaden 'language' y/o 'forced'
        """
        detalles_tracks = []

        for track in self.archivo.tracks:

            if not type:
                if isinstance(type, str):
                    if track.track_type != type:
                        continue
                elif isinstance(type, list):
                    if track.track_type not in type:
                        continue

            info_track = {'id': track.track_id, 'name': track.track_name, 'type': track.track_type, 'codec': track.track_codec}
            if track.track_type == 'audio' or track.track_type == 'subtitles':
                info_track.update({'language': track.language, 'default': track.default_track, 'sync': track.sync})
                if track.track_type == 'subtitles':
                    info_track.update({'forced': track.forced_track})
            detalles_tracks.append(info_track)

        return detalles_tracks
    
    def idiomas(self, idiom: Dict[int, str], forz: List[int]):
        """ 
        Método para establecer los idiomas i las pistas que son forzadas.\n
        idiomas( idiom = {1: 'cat', 2: 'spa', 3: 'eng', ...}, forz = [3, 5])

        Args:
            idiom (Dict[int, str]): Diccionario en el que cada clave es un int (representando el id) y cada valor el idioma correspondiente.
            forz (List[int]): Lista de ids de pistas forzadas. Sólo se especificarán las pistas forzadas, el resto se pondrán como falsas.
        """

        for id, idioma in idiom.items():
            self.archivo.tracks[id].language = idioma
            self.archivo.tracks[id].forced_track = id in forz
    
    def eliminar(self, tracks: Union[int, List[int]] = [], idiomas: List[str] = [], und: bool = False):
        """
        Método para eliminar las pistas especificadas. Las pistas con idiomas indefinidos no se eliminan por defecto.
        eliminar(tracks = [5,3,4,2])
        eliminar(idiomas = ['ita', 'fra'], und = True)

        Args:
            tracks (List[int]): Lista de tracks a eliminar.
            idiomas (List[str]): Pistas de idiomas a eliminar.
            und (bool): Añadir los 'undefined' a la lista de pistas a eliminar
        """
        if tracks:
            self.archivo.tracks = [track for id, track in enumerate(self.archivo.tracks) if id not in tracks]
        
        else:
            self.archivo.tracks = [track for track in self.archivo.tracks if track.language not in idiomas+(['und'] if und else [])]
    
    def conservar(self, tracks: Union[int, List[int]] = [], idiomas: List[str] = [], und: bool = True):
        """
        Método para conservar las pistas especificadas. Las pistas con idiomas indefinidos se conservan por defecto.
        conservar(tracks = [5,3,4,2])
        conservar(idiomas = ['cat', 'jpn'], und = False)

        Args:
            tracks (List[int]): Lista de tracks a conservar.
            idiomas (List[str]): Pistas de idiomas a conservar.
            und (bool): Añadir los 'undefined' a la lista de pistas a conservar
        """
        if tracks:
            self.archivo.tracks = [track for id, track in enumerate(self.archivo.tracks) if id in [0] + tracks]
        
        else:
            self.archivo.tracks = [self.archivo.tracks[0]] + [track for track in self.archivo.tracks[1:] if track.language in idiomas+(['und'] if und else [])]

    def reordenar(self, tracks:List[int] = [], idiomas: List[str] = []):
        """
        Método para organizar las pistas del archivo. Se recomienda utilizar sólo una variable, ya que si se utilizan las dos se estaría reordenando las pistas del archivo dos veces.\n
        ordenar(tracks = [5, 3, 4, 2, 1, ...])\n
        ordenar(idiomas = ['cat', 'jpn', 'eng', 'spa', ...])

        Args:
            tracks (List[int]): Lista de ints en la que el valor es el id original de la pista del archivo y su posición dentro la lista és la nueva posición que tomará.
            idiomas (List[str]): Lista de idiomas en formato ISO 639-2. Primero situará los idiomas en el orden correspondiente y luego los subtitulos, priorizando entre los del mismo idioma los forzados.
        """
        if tracks:
            for i in range(len(tracks)):
                if tracks[i] == i+1:
                    continue
                self.archivo.swap_tracks(tracks[i], i+1)
                actual, nuevo = i, tracks.index(i+1)
                tracks[actual], tracks[nuevo] = tracks[nuevo], tracks[actual]
        
        idiomas.append('und')
        audios = []
        subtitulos = []
        self.audios = []
        self.subtitulos = []
        for track in self.archivo.tracks:
            if track.track_type == 'audio':
                audios.append(track)
                self.audios.append(track.language) if track.language not in self.audios else None
            elif track.track_type == 'subtitles':
                subtitulos.append(track)
                self.subtitulos.append(track.language) if track.language not in self.subtitulos else None
        audios.sort(key = lambda x: (idiomas.index(x.language)))
        self.audios.sort(key = lambda x: (idiomas.index(x)))
        subtitulos.sort(key = lambda x: (idiomas.index(x.language), not x.forced_track))
        self.subtitulos.sort(key = lambda x: (idiomas.index(x)))
        self.archivo.tracks = [self.archivo.tracks[0]] + audios + subtitulos
    
    def predeterminar(self, tracks:List[int] = [], audio: str = '', subtitulo: str = '', forzado: bool = True, auto: bool = False):
        """
        Método para definir las pistas predeterminadas.\n
        predeterminar(tracks = [5, 3, 4, 2, 1, ...])\n
        predeterminar(audio = 'cat', subtitulo = 'spa', forzado = False)\n
        predeterminar(auto = True, forzado = False)

        Args:
            tracks (List[int]): Lista de pistas del archivo.
            audio (str): Idioma de audio que se pondrá como el predeterminado
            subtitulo (str): Idioma de subtitulo que se pondrá como el predeterminado.
            forzado (bool): Especificar si el subtitulo a establecer como predeterminado es forzado o no. Por defecto en True.
            auto (bool): Variable para activar las pistas predeterminadas de forma automática una vez se han ordenado las pistas tambiés de forma automática.
        """
        for id in tracks:
            self.archivo.tracks[id].default_track = id in tracks

        audio_predeterminado = audio or (self.audios[0] if auto else None)
        subtitulo_predeterminado = subtitulo or (self.subtitulos[0] if auto else None)

        for id, track in enumerate(self.archivo.tracks[1:], start=1):
            if track.track_type == 'audio':
                self.archivo.tracks[id].default_track = self.archivo.tracks[id].language == audio_predeterminado
            elif track.track_type == 'subtitles':
                self.archivo.tracks[id].default_track = self.archivo.tracks[id].language == subtitulo_predeterminado and track.forced_track == forzado


    def renombrar(self, titulo:str = '', nombres:Dict[int, str] = {}, auto:bool = False):
        """
        Método para renombrar los diferentes tracks. Utilizar la variable de 'nombres' o 'auto' únicamente. Especificar el título es opcional.\n
        renombrar(nombres: {1: 'AAC', 2: 'Subtítulos', 2: 'AAC'}, titulo = 'Ejemplo')\n
        renombrar(auto = True, titulo = 'Ejemplo')

        Args:
            titulo (str): Título que tendrá el archivo.
            nombres (Dict[int, str]): Id del track y su nombre correspondiente.
            auto: Opción para renombrar todas las pistas de manera automática. Se necesita haber especificado el idioma de todas las pistas y haber marcado las que son forzadas.
        """
        if titulo:
            self.archivo.title = titulo

        if nombres:
            for id, nombre in nombres.items():
                self.archivo.tracks[id].track_name = nombre

        elif auto:

            self.archivo.tracks[0].track_name = f'HEVC {self.ancho}×{self.alto}'

            for id, track in enumerate(self.archivo.tracks[1:], start=1):

                if track.track_type == 'audio':
                    nombre = track.track_codec

                elif track.track_type == 'subtitles':
                    nombre = sub.get(track.language, track.track_name)
                    if track.forced_track:
                        nombre = forz.get(track.language, track.track_name)
                        nombre = nombre.capitalize()

                self.archivo.tracks[id].track_name = nombre

    def sincronizar (self, tiempo:int, tracks:List[int] = [], audios:List[str] = [], subtitulos:List[str] = [], forz:Dict[str, bool] = {}):
        """
        Método para ajustar o sincronizar las pistas al tiempo especificado. Utilizar la variable 'tracks' o las variables 'audios', 'subtitulos' y 'forz'.\n
        sincronizar(tiempo=350, tracks([1, 2, 4, 5]))\n
        sincronizar(tiempo=350, subtitulos = ['eng', 'cat'], forz = {'eng': True})

        Args:
            tiempo (int): Tiempo en milisegundos. Puede ser negativo (para avanzar) o positivo (para retrasar)
            tracks (List[int], optional): Lista de pistas a ajustar.
            audios (List[str], optional): Lista de idiomas de audios a ajustar.
            subtitulos (List[str], optional): Lista de idiomas de subtitulos a ajustar.
            forz (dict, optional): Diccionario de los idiomas de los subtitulos. En caso de que sólo haya que ajustar una pista en concreto de un idioma, hay que especificar si esta es la forzada (siendo 'True' la forzada y 'False' la no forzada). En caso contrario no utilizar esta variable.
        """

        if tracks:
            for id in tracks:
                self.archivo.tracks[id].sync = tiempo
        
        elif audios or subtitulos:
            for id, track in enumerate(self.archivo.tracks[1:], start=1):
                if audios and track.track_type == 'audio' and track.language in audios:
                    self.archivo.tracks[id].sync = tiempo
                elif subtitulos and track.track_type == 'subtitles' and track.language in subtitulos:
                    if not forz:
                        self.archivo.tracks[id].sync = tiempo
                    elif (self.archivo.tracks[id].forced_track == forz[self.archivo.tracks[id].language]) or forz.get(self.archivo.tracks[id].language, True):
                        self.archivo.tracks[id].sync = tiempo
        else:
            for id in range(1, len(self.archivo.tracks)+1):
                self.archivo.tracks[id].sync = tiempo
    
    def recortar(self, inicio: bool = False, final: bool = False, frames: Union[int, List[int]] = [], segundos: Union[int, List[int]] = []):
        """
        Método para recortar el archivo. Necesario indicar si el recorte afecta a la primarsa parte o la segunda y utilizar el método de frames o segundos.

        Args:
            inicio (bool, optional): Variable para saber si se recorta el inicio o no. Si se activa, se eliminará el archivo que contenga desde el instante 0 al especificado.
            final (bool, optional): Variable para saber si se recorta el final o no. Si se activa, se eliminará el archivo que contenga desde el último instante especificado al final.
            frames (Union[int, List[int]], optional): Variable en la que se especifica el numero de los frames por los que se separa el archivo. Puede ser un único valor o varios
            segundos (Union[int, List[int]], optional): Variable en la que se especifica el tiempo por el que se separa el archivo. Puede ser un único valor o varios
        """

        if not inicio and not final:
            quit('Especificar si se separa para recortar la parte del inicio o la parte del final')
        self.split_inicio, self.split_final = inicio, final
        
        if frames:
            self.archivo.split_frames(frames)
        elif segundos:
            self.archivo.split_duration(segundos)
    
    def redimensionar(self, ancho:int, alto:int):
        self.nuevo_ancho_alto = ['--display-dimensions', f'0:{ancho}x{alto}']
        self.archivo.tracks[0].track_name = f'HEVC {ancho}×{alto}'
    
    def multiplexar(self, output: str = None):
        """ 
        Función para muxear el archivo final.\n
        Si no se especifica una carpeta, se una con el mismo nombre del archivo en la ruta de este y se pone ahí el resultado.

        Args:
            output (str, optional): _description_. Defaults to None.
        """

        if not output:
            os.makedirs(self.carpeta, exist_ok=True)
            output = self.carpeta

        output = os.path.join(output, f'{self.nombre}.mkv')

        comando = self.archivo.command(output_path=output, subprocess=True)

        if self.nuevo_ancho_alto:
            comando = comando[:3] + self.nuevo_ancho_alto + comando[3:]
        
        #subprocess.run(comando)
        
        process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        pattern = re.compile(r"[A-Za-z]+:\s([0-9]+)%", re.IGNORECASE)
        for line in process.stdout:
            # Buscar el porcentaje de progreso
            match = pattern.search(line)
            if match:
                yield int(match.group(1))

        if os.path.isfile(os.path.join(os.path.dirname(output), f'{self.nombre}-003.mkv')):
            archivos = {'-001.mkv', '-002.mkv', '-003.mkv'}
            eliminar = {'-001.mkv', '-003.mkv'}
        elif os.path.isfile(os.path.join(os.path.dirname(output), f'{self.nombre}-002.mkv')):
            archivos = {'-001.mkv', '-002.mkv'}
            eliminar = {'-002.mkv'} if self.split_inicio else {'-001.mkv'}
        else:
            return

        for eliminacion in eliminar:
            os.remove(os.path.join(os.path.dirname(output), f'{self.nombre}{eliminacion}'))

        conservar = list(archivos - eliminar)[0]

        os.rename(os.path.join(os.path.dirname(output), f'{self.nombre}{conservar}'), output)
    
    def separar_frames(self, output: str, inicio: int, intervalo: int = 4):

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, inicio)

        for i, _ in enumerate(range(int(intervalo*self.fps)), start = int(inicio*self.fps)):
            _, frame = self.cap.read()
            frame_filename = os.path.join(output, f"frame_{str(i).zfill(3)}.png")
            cv2.imwrite(frame_filename, frame)

    def __str__(self):
        return self.archivo.title
    
    def __call__(self):
        return self.archivo.title