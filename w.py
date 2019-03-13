from wit import Wit
from gtts import gTTS 
import os 
import datetime
import re
access_token = 'KE3X3T55WGUX6QLPO7RIBTDT2LQOP2H6'
client = Wit(access_token)

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
	


# hora = dimeFecha()
# texto_audio(hora)
fecha = dimeFecha()
hora = dimeHora()

texto_audio(fecha)
texto_audio(hora)
'''
client = Wit(access_token)
resp = None
with open('yo.wav', 'rb') as f:
  resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
print('Yay, got Wit.ai response: ' + str(resp))
'''

# myText = resp['_text']













