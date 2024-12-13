import os

## Cambiar solo las variables que hay aquí abajo, siguinedo el patrón.
## Primero, ir a la pestaña "Run" de este programa y dar clic a "Run Module".
## Luego hay que copiar "creacion_forzados_ingles()" y pegar en la ventana de comandos.
## En la ventana de comandos salen los archivos que han dado algún error.
## Probar a ajustar la tolerancia, puede dar mejores resultados.

Carpeta_con_subtitulos=r"D:\Users\paula\Videos"
Archivo_referencia_cabecera=r"D:\Users\paula\Videos\Starwars6.1983.2160P.Dovi_Track04.ass"
Numero_caracteres_a_mantener_del_título=20
Distintivo_Forzados="Track05.ass"
Distintivo_Ingles="Track04.ass"
tolerancia=0.4

def lista_subtitulos_forzados():
    os.chdir(Carpeta_con_subtitulos)
    files=os.listdir()
    subs_forzados=[]
    for file in files:
        if Distintivo_Forzados in file:
            subs_forzados.append(Carpeta_con_subtitulos+"/"+file)
    return subs_forzados

def lista_subtitulos_ingles():
    os.chdir(Carpeta_con_subtitulos)
    files=os.listdir()
    subs=[]
    for file in files:
        if Distintivo_Ingles in file:
            subs.append(Carpeta_con_subtitulos+"/"+file)
    return subs

def lista_subtitulos_ingles_forzados():
    Subtitulos=lista_subtitulos_ingles()
    for i in range (0,len(Subtitulos)):
        Subtitulos[i]=Subtitulos[i][:len(Carpeta_con_subtitulos)+Numero_caracteres_a_mantener_del_título+1]+".ass"
    return Subtitulos

def cabecera_subtitulo():
    cab=[]
    linia=""
    with open (Archivo_referencia_cabecera, 'r', encoding='cp437') as f:
        while linia!='[Events]\n':
            linia=f.readline()
            cab.append(linia)
        cab.append(f.readline())
    return cab

def creacion_forzados_ingles():
    Forzados=lista_subtitulos_forzados()
    Ingles=lista_subtitulos_ingles()
    Ingles_forzados=lista_subtitulos_ingles_forzados()
    Cabecera=cabecera_subtitulo()
    for i in range (0,len(Ingles)):
        forzados=Forzados[i]
        ingles=Ingles[i]
        ingles_forzados=Ingles_forzados[i]
        linias_transformadas=0
        AVISO=False
        with open (forzados,'r', encoding='cp437') as F,open (ingles,'r', encoding='cp437') as I, open (ingles_forzados,'w', encoding='cp437') as IF:
            for li in Cabecera:
                IF.write(li)
            tiempos=[]
            linia=""
            while linia!="[Events]\n":
                linia=F.readline()
            F.readline()
            linia=""
            while linia!="[Events]\n":
                linia=I.readline()
            I.readline()
            for lin in F:
                l=lin.split(',')
                h=l[1].split(':')
                tiempos.append(3600*float(h[0])+60*float(h[1])+float(h[2]))
            linias_a_transformar=len(tiempos)
            for lin in I:
                l=lin.split(',')
                if l[-1]=='_\n':
                    AVISO=True
                h=l[1].split(':')
                tiempo=3600*float(h[0])+60*float(h[1])+float(h[2])
                for t in tiempos:
                    if abs(tiempo-t)<tolerancia:
                        IF.write(lin)
                        linias_transformadas+=1
        ingles_forzados=ingles_forzados.replace(Carpeta_con_subtitulos+'/','')
        if linias_transformadas!=linias_a_transformar and AVISO==False:
            print(ingles_forzados)
        elif AVISO:
            print(ingles_forzados+' _ (Guión Bajo)')
