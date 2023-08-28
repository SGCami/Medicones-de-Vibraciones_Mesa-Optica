import serial
import time

DataBase = open('C:\Denis\ICE\VI SEM\Diseño 2 - ELEL210\Base-de-Datos_Mesa-Optica\prueba_acc.txt', 'w')
Arduino = serial.Serial('COM3', 57600)
time.sleep(1)

while True:
    CAD = Arduino.readline().decode('ascii')
    print(CAD)

    DataBase.write(CAD)