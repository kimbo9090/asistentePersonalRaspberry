from wit import Wit
from gtts import gTTS 
import os 
import ast
import vlc
import wave
import datetime
from a import giveToken
from a import giveToken2
import pyowm
import urllib.request
from bs4 import BeautifulSoup
import requests 
import geocoder
import speech_recognition as sr
import pafy

r = sr.Recognizer()
mic = sr.Microphone()
mic = sr.Microphone(device_index=5)

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
        if 'user' in vid:
            fullVids.remove(vid)
    return fullVids

a = dame_lista_videos('Alexelcapo')
b = dame_Temperatura()
texto_audio(b)


'''
while True:

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    a = r.recognize_wit(audio,access_token)
    if ("canela" in a):
        texto_audio("Dime que quieres que te diga, hermoso")
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
        else:
            texto_audio('Perdona, no te he entendido, por favor llámame de nuevo y repite la acción')
    else:
        print("No has dicho canela")
        print (a)
'''




