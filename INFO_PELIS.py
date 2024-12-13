import imdb
ia = imdb.Cinemagoer()
import asyncio
from themoviedb import aioTMDb
tmdb = aioTMDb()

CARPETA_XML="D:\\Gerard\\Videos\\XML\\"
LINKS=r"D:\Gerard\Desktop\Caratulas\enlaces.txt"
COMANDOS_PROPEDIT=r"D:\Gerard\Desktop\Caratulas\comandos.txt"

tmdb.key = "8e17e18c37a5c23d92f728038974e868"
etiquetas={'cinematographer':'DIRECTOR_OF_PHOTOGRAPHY','animation department':'DIRECTOR_OF_PHOTOGRAPHY'}
ETIQUETAS={'COUNTRY':'countries','TITLE':'title','SUBTITLE':'tagline','URL':'url','COMPOSITION_LOCATION':'countries','COMPOSER':'composer','DIRECTOR':'director','ASSISTANT_DIRECTOR  ':'assistant director','DIRECTOR_OF_PHOTOGRAPHY':'cinematographer','SOUND_ENGINEER':'sound crew','ART_DIRECTOR':'art direction','PRODUCTION_DESIGNER':'production design','COSTUME_DESIGNER':'costume designer','ACTOR':'actors','CHARACTER':'characters','WRITTEN_BY':'writer','EDITED_BY':'editor','PRODUCER':'producer','PRODUCTION_STUDIO':'production companies','GENRE':'genres','CONTENT_TYPE':'kind','KEYWORDS':'keywords','SUMMARY':'plot','SYNOPSIS':'synopsis','DATE_RELEASED':'year','RATING':'rating'}
for key in ETIQUETAS.keys():
    etiquetas[ETIQUETAS[key]]=key

def item (category):
    d=[]
    for it in category:
        try:
            if it['name'] not in d:
                d.append(it['name'])
        except KeyError:
            a=0
    return d

async def main(title):
    D={'actors':[],'characters':[],'keywords':[]}
    movies = await tmdb.search().movies(title)
    movie_id = movies[0].id  # get first result
    movie = await tmdb.movie(movie_id).details(append_to_response="belongs_to_collection,tagline,credits,keywords,imdb_url")

    if movie.belongs_to_collection:
        D['collection']=[movie.belongs_to_collection.name[:-11]]
    
    D['tagline']=[movie.tagline]
    D['url']=[movie.imdb_url]
    for person in movie.credits.cast:
        name=person.name
        character=person.character
        if 'uncredited' in name or 'uncredited' in character:
            continue
        if '(voice)' in character:
            character=character.replace(' (voice)','')
        D['actors'].append(name)
        D['characters'].append(character)
    try:
        for key in movie.keywords.results:
            D['keywords'].append(key.name)
    except:
        a=1
    return D

def pelicula (link_IMDB):
    id_IMDB=link_IMDB.split('/')[4][2:]
    tags=['genres', 'runtimes', 'countries', 'rating', 'languages', 'title', 'year', 'director', 'writer', 'producer', 'composer', 'editor', 'production companies']
    movie=ia.get_movie(str(id_IMDB))
    if 'cinematographer' not in movie.infoset2keys['main']:
        tags.append('animation department')
    else:
        tags.append('cinematographer')
    M={}
    try:
        for tag in tags:
            var=movie[tag]
            if type(var)==str:
                M[tag]=[var]
            elif type(movie[tag])==list:
                if type(var[0])==str:
                    M[tag]=var
                else:
                    M[tag]=item(var)
            elif type(var)==float or type(var)==int:
                if type(var)==float:
                    var=var/2
                M[tag]=[str(var)]
            elif type(var)==dict:
                for t in var:
                    M[t]=var[t]
            else:
                M[tag]=var['name']
    except:
        a=1
    M['plot']=[movie['plot'][0]]
    try:
        M['synopsis']=[movie['synopsis'][0]]
    except:
        try:
            M['synopsis']=[movie['plot'][1].split('—')[0]]
        except:
            a=1
    D=asyncio.run(main(M['title']))
    M |= D
    return M

def xml (link_IMDB):
    info=pelicula(link_IMDB)
    title=info['title'][0].replace(':',' -')
    with open (CARPETA_XML+title+'.xml','w',encoding='utf8') as doc:
        doc.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE Tags SYSTEM "matroskatags.dtd">\n<Tags>\n  <Tag>\n')
        if 'collection' in info:
            doc.write('    <Targets>\n      <TargetTypeValue>70</TargetTypeValue>\n    </Targets>\n    <Simple>\n      <Name>TITLE</Name>\n      <String>'+''.join(info['collection'])+'</String>\n    </Simple>\n  </Tag>\n  <Tag>\n')
        doc.write('    <Targets>\n      <TargetTypeValue>50</TargetTypeValue>\n    </Targets>\n')
        for key in info.keys():
            if key not in etiquetas:
                continue
            doc.write('    <Simple>\n      <Name>'+etiquetas[key]+'</Name>\n      <String>'+', '.join(info[key])+"</String>\n      <TagLanguage>und</TagLanguage>\n      <DefaultLanguage>1</DefaultLanguage>\n    </Simple>\n")
        doc.write('  </Tag>\n</Tags>')
    print (info['title'][0])

def XML ():
    with open (LINKS, 'r') as LIST, open (COMANDOS_PROPEDIT, 'w') as COM:
        for linia in LIST:
            link_IMDB=linia.strip()
            COM.write(xml(link_IMDB))
