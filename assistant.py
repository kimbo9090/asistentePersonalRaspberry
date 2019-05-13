# -*- coding: utf-8 -*-
from wit import Wit
from gtts import gTTS 
import os 
import ast
import wave
import datetime
from a import giveToken
from a import giveToken2
import pyowm
import urllib.request
from bs4 import BeautifulSoup
import requests 
import wave
import geocoder
import speech_recognition as sr
import pafy
import sqlite3
from pydub import AudioSegment



r = sr.Recognizer()
mic = sr.Microphone()
access_token = giveToken()
access_token2 = giveToken2()
client = Wit(access_token)
owm = pyowm.OWM(access_token2)


# Método que procesa un mes en número a Palabra.
def procesaMes(mes):
    mesPalabra = ''
    if (mes == 1):
        mesPalabra = 'enero'
    elif (mes == 2):
        mesPalabra = 'febrero'
    elif (mes == 3):
        mesPalabra = 'marzo'
    elif (mes == 4):
        mesPalabra = 'abril'
    elif (mes == 5):
        mesPalabra = 'mayo'
    elif (mes == 6):
        mesPalabra = 'junio'
    elif (mes == 7):
        mesPalabra = 'julio'
    elif (mes == 8):
        mesPalabra = 'agosto'       
    elif (mes == 9):
        mesPalabra = 'septiembre'
    elif (mes == 10):
        mesPalabra = 'octubre'
    elif (mes == 11):
        mesPalabra = 'noviembre'
    elif (mes == 12):
        mesPalabra = 'diciembre'
    
    return mesPalabra
# Método que utiliza la fecha local y la filtra
def dimeFecha():
    x = datetime.datetime.now()
    xS = str(x)
    fechaSplitted = xS.split(" ")

    ano_dia_mes = fechaSplitted[0]

    ano_dia_mesSplitted = ano_dia_mes.split("-")

    ano = ano_dia_mesSplitted[0]
    mes = int(ano_dia_mesSplitted[1])
    dia = ano_dia_mesSplitted[2]

    out = procesaMes(mes)

    fechaAsistente = "Estamos a %s de %s del año %s" % (dia,out,ano)

    return fechaAsistente
# Método que utiliza la hora local y la filtra 
def dimeHora():
    x = datetime.datetime.now()
    xS = str(x)
    fechaSplitted = xS.split(" ")

    horaDate = fechaSplitted[1]
    
    hora = horaDate.split(".")[0]
    
    horaAsistente = "Son las %s" % (hora)   
    
    return horaAsistente
# A partir de un String, nos genera un .mp3 con el audio de el asistente
def texto_audio(texto):
    tts = gTTS(texto, 'es')
    filename = 'temp.mp3'
    tts.save(filename)
    os.system("mpg321 -q "+filename) 
    os.remove(filename)
# A partir de nuestra IP, nos devuelve la latitud y longitud.
def dame_Localizacion():
    g = geocoder.ip('me')
    return g.latlng
# A través de la librería PyOWM y nuestra latitud, nos devuelve el tiempo que hará hoy.
def dame_Tiempo():
    loc = dame_Localizacion()
    observation = owm.weather_at_coords(loc[0],loc[1])
    weather = observation.get_weather()
    reponseString = str(weather)
    reponseSplitted = reponseString.split(",")
    reponseSplitted2 = reponseSplitted[2].strip(">")
    reponseSplitted3 = reponseSplitted2.split("=")
    return reponseSplitted3[1]
# A través de la librería PyOWM y nuestra latitud, nos devuelve la temperatura que hará hoy.
def dame_Temperatura():
    loc = dame_Localizacion()
    observation = owm.weather_at_coords(loc[0],loc[1])
    weather = observation.get_weather()
    temperatures = weather.get_temperature('celsius')

    temperatura = temperatures['temp']
    temperatura_maxima = temperatures['temp_max']
    temperatura_minima = temperatures['temp_min']

    temperatura_frase = "Hoy tenemos una temperatura de %s grados           , con máxima de %s               ,y mínima de %s " % (temperatura,temperatura_maxima,temperatura_minima)

    return temperatura_frase
# A partir de un string, hacemos una búsqueda en Youtube con Web Scraping y nos devuelve una lista de videos.
def dame_lista_videos(tituloVideo):
    fullVids = []
    query = urllib.parse.quote(tituloVideo)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        fullVids.append('https://www.youtube.com' + vid['href'])
    for vid in fullVids:
        if 'user' in vid or 'channel' in vid:
            fullVids.remove(vid)
    return fullVids[0]
# Exporta un video de m4a a mp3 
def exporta_mp3(m4aPath,url):
    m4a_audio = AudioSegment.from_file(m4aPath+'.m4a', format="m4a")
    m4a_audio.export('./videos/'+url+'.mp3', format="mp3")
# A partir de una URL devuelve cierta información
def dameInfoVideo(url):
    info = []
    video = pafy.new(url)
    info.append(video.duration)
    info.append(video.title)
    info.append(video.dislikes)
    info.append(video.likes)
    info.append(video.viewcount)
    info.append(video.username)
    return info
# Descarga un video en concreto y lo maneja
def reproduceVideo(tituloVideo):
    videoInfo = []
    url = dame_lista_videos(tituloVideo)
    videoInfo = dameInfoVideo(url)

    con_bd = sqlite3.connect('database.db')
    cursor_bd = con_bd.cursor()
    cursor_bd.execute("select * from VIDEOS where URL=?",(url,))
    videoURL = cursor_bd.fetchone()

    # TODO Hacer consulta por la búsqueda de el usuario

    if (videoURL is None): # TODO Filtrar por búsqueda de Usuario
        duration = videoInfo[0]
        durationSplitted = duration.split(":")   
        video = pafy.new(url)
        streams = video.streams
        download = video.getbestaudio(preftype="m4a",ftypestrict=True)
        download.download(filepath="./videos",quiet=False)
        exporta_mp3('./videos/'+videoInfo[1],videoInfo[1])    
        os.remove('./videos/'+videoInfo[1]+'.m4a')
        insert = (url,videoInfo[0],videoInfo[1],videoInfo[2],videoInfo[3],videoInfo[4],tituloVideo,videoInfo[5])
        cursor_bd.execute("INSERT INTO VIDEOS VALUES (?,?,?,?,?,?,?,?)",insert)
        con_bd.commit()
        con_bd.close()
        filename = './videos/'+ "\"" + videoInfo[1]+'.mp3' + "\""
        os.system("mpg321 -q "+filename) 
    else:
        filename = './videos/'+ "\"" + videoInfo[1]+'.mp3' + "\""
        os.system("mpg321 -q "+filename) 
        con_bd.close()

# TODO Filtar todo lo que diga el usuario despues de reproduce -->
def procesaInputUsuarioReproducir():
    pass

def playlist_aleatoria():
    os.system("mpg321 -B ./videos -Z")

while True:

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    a = r.recognize_wit(audio,access_token)
    if ("canela" in a):
        texto_audio("Que quieres, que pasa, ahora que")
        with mic as source2:
            r.adjust_for_ambient_noise(source2)
            audio2 = r.listen(source2)
        b = r.recognize_wit(audio2,access_token)
        if ('hora' in b):
            hora = dimeHora()
            texto_audio(hora)
        elif ('fecha' in b):
            fecha = dimeFecha()
            texto_audio(fecha)
        elif ('temperatura' in b):
            temperatura = dame_Temperatura()
            texto_audio(temperatura)
        elif ('tiempo' in b):
            temp = dame_Tiempo()
            texto_audio(temp)
        elif ('aleatorio' in b or 'aleatoria' in b):
            texto_audio('¿Una canción aleatoria? Voy')
            playlist_aleatoria()
        else:
            texto_audio('Perdona, no te he entendido, por favor llámame de nuevo y repite la acción')
    else:
        print("No has dicho canela")
        print (a)





