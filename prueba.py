''' Rssi y SNR LoRa punto a punto
paquete de datos desde puerto Serial
generados desde dispositivo LoRa
modelo Heltec Lora 32 v.2
Girni 2020-10-07 propuesta: edelros@espol.edu.ec
'''
import numpy as np
import matplotlib.pyplot as plt
import serial, time

# INGRESO
# Puerto de captura de datos USB-Serial
puerto = 'com3'
baudios = 115200

# Archivo para el registro de cada evento rx,tx
nombrearchivo = 'multipuntoFIEC101.txt'

# identificadores de balizas
baliza = ['d1','d2','d3']

# Mínimo de lecturas por baliza
lecturasMin = 100

# PROCEDIMIENTO
# Crea registro de lecturas
n = len (baliza)
registro = {}
for elemento in baliza:
    registro[elemento] = {'cuenta': 0 ,
                          'rssi': np.array([0.0,0.0]),
                          'snr':  np.array([0.0,0.0]),
                          'SumaRssi': np.array([0.0,0.0]),
                          'SumaSnr':  np.array([0.0,0.0]),
                          'minmaxRssi': np.array([0.0,-200.0,0.0,-200.0]),
                          'minmaxSnr': np.array([100.0,0.0,100.0,0.0])
                          }

# inicializa archivo.txt a vacio
archivo = open(nombrearchivo,'w')
archivo.close()  # Cierra el archivo

# Abre puerto Serial
arduino = serial.Serial(puerto, baudios)
arduino.setDTR(False)
time.sleep(0.3)

# limpia buffer de datos anteriores
arduino.flushInput()  
arduino.setDTR()  
time.sleep(0.3)
print('\nEstado del puerto: ',arduino.isOpen())
print('Nombre del dispositivo conectado: ', arduino.name)
print('Dump de la configuración:\n ',arduino)
print('\n###############################################\n')

# Lectura de datos
np.set_printoptions(precision=2)
conteo = 0
difunde = 0
while conteo<lecturasMin:
    #esperar hasta recibir un paquete
    while (arduino.inWaiting()==0):
        pass 

    # leer linea desde puerto serial
    linea = arduino.readline()
    # binario a texto, elimina /r/n
    texto = linea.decode()
    texto = linea.strip()
    
    # identificar la trama como rx, tx
    cond1 = texto.startswith('tx')
    cond2 = texto.startswith('rx')
    if cond1 or cond2:
        archivo = open(nombrearchivo,'a')
        archivo.write(texto+'\n')
        archivo.close()
        
        if (texto.startswith('tx')):
            difunde = difunde + 1
        if (texto.startswith('rx')):
            texto = texto.split(',')
            tipo  = texto[0]
            dir_remite = texto[2]
            paqrcbvID  = texto[3]
            rssi_tx    = float(texto[4])
            snr_tx     = float(texto[5])
            rssi_rx    = float(texto[6])
            snr_rx     = float(texto[7])
            if tipo == "rx":
                # conteo de lecturas
                cual = dir_remite
                registro[cual]['cuenta']=registro[cual]['cuenta']+1
                if registro[cual]['cuenta']<conteo:
                    conteo = registro[cual]['cuenta']

                # acumulado
                registro[cual]['SumaRssi'][0] = registro[cual]['SumaRssi'][0]+rssi_tx
                registro[cual]['SumaSnr'][0]  = registro[cual]['SumaSnr'][0]+snr_tx
                registro[cual]['SumaRssi'][1] = registro[cual]['SumaRssi'][1]+rssi_rx
                registro[cual]['SumaSnr'][1]  = registro[cual]['SumaSnr'][1]+snr_rx

                # promedios
                cuantos = registro[cual]['cuenta']
                registro[cual]['rssi'] = registro[cual]['SumaRssi']/cuantos
                registro[cual]['snr']  = registro[cual]['SumaSnr']/cuantos

                # minimos y maximos
                registro[cual]['minmaxRssi'][0] = np.min([rssi_tx,registro[cual]['minmaxRssi'][0]])
                registro[cual]['minmaxRssi'][1] = np.max([rssi_tx,registro[cual]['minmaxRssi'][1]])
                registro[cual]['minmaxRssi'][2] = np.min([rssi_rx,registro[cual]['minmaxRssi'][2]])
                registro[cual]['minmaxRssi'][3] = np.max([rssi_rx,registro[cual]['minmaxRssi'][3]])

                registro[cual]['minmaxSnr'][0] = np.min([snr_tx,registro[cual]['minmaxSnr'][0]])
                registro[cual]['minmaxSnr'][1] = np.max([snr_tx,registro[cual]['minmaxSnr'][1]])
                registro[cual]['minmaxSnr'][2] = np.min([snr_rx,registro[cual]['minmaxSnr'][2]])
                registro[cual]['minmaxSnr'][3] = np.max([snr_rx,registro[cual]['minmaxSnr'][3]])

            # Muestra en pantalla el estado de recepción
            print('\n difusion: ',difunde)
            print(texto)
            for elemento in baliza:
                print(elemento,registro[elemento]['cuenta'],
                      '\tprom Rssi[tx,rx] \t   Snr[tx,rx]')
                print("prom   :",registro[elemento]['rssi'],"\t  ",
                      registro[elemento]['snr'])
                print("min,max:",registro[elemento]['minmaxRssi'],
                      registro[elemento]['minmaxSnr'])

# Cerrar el puerto serial.
serial.Serial.close
CATEGORÍAS