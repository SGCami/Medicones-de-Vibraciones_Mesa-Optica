import serial
import time

DataBase = open('SGCami/Medicones-de-Vibraciones_Mesa-Optica/base de datos/bd1.txt', 'w')
serialArduino= serial.Serial('COM3', 9600)
time.sleep(1)

while True:
    CAD = serialArduino.readline().decode('ascii')
    print(CAD)

    DataBase.write(CAD)