from wit import Wit
from gtts import gTTS 
import os 
import datetime
from a import giveToken
from a import giveToken2
import pyowm
import requests 
import geocoder
access_token = giveToken()
access_token2 = giveToken2()
client = Wit(access_token)
owm = pyowm.OWM(access_token2)

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

def dimeHora():
    x = datetime.datetime.now()
    xS = str(x)
    fechaSplitted = xS.split(" ")

    horaDate = fechaSplitted[1]
    
    hora = horaDate.split(".")[0]
    
    horaAsistente = "Son las %s" % (hora)   
    
    return horaAsistente

def texto_audio(texto):
    tts = gTTS(texto, 'es')
    filename = '/tmp/temp.mp3'
    tts.save(filename)
    os.system("mpg321 "+filename) 
    os.remove(filename)

def dame_Localizacion():
    g = geocoder.ip('me')
    return g.latlng

def dame_Tiempo():
    loc = dame_Localizacion()
    observation = owm.weather_at_coords(loc[0],loc[1])
    w = observation.get_weather()
    return w



a = dame_Tiempo()

print(a)


'''
resp = None
with open('bon.wav', 'rb') as f:
  resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
print('Yay, got Wit.ai response: ' + str(resp))


myText = resp['_text']

if ('bonita' in myText):
    texto_audio('Muchas gracias, te lo agradezco.')
'''






