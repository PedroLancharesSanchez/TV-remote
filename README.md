# 🖥️ API de Control del PC

API desarrollada en Python Flask que permite controlar diferentes aspectos de un ordenador con Python: ratón, teclado, brillo, volumen, pantalla y apertura de aplicaciones. Integrada con una APP movil, preparada para sistemas de automatización.

## ✨ Funcionalidades:

🖱️ Raton → Mover el puntero y hacer clics (izquierdo/derecho).

🔠 Texto → Escribir cadenas o borrar con backspace.

🔊 Volumen → Ajustar el volumen principal del sistema (0–100%).

💡 Brillo → Ajustar el brillo de la pantalla (0–100%).

🖥️ Pantalla → Apagar/encender monitor.

🎬 Atajos → Abrir Netflix o YouTube directamente en Chrome.

🔊 Voz → Recibir comandos de voz.

## Android_APP.apk

Es una APP desarrollada para Android, que permite enviar peticiones a un API dentro de la misma red WiFi. 
La configuración por defecto del API es 192.168.1.108:5000
![1000050868](https://github.com/user-attachments/assets/ab76a8e4-a727-43ed-9357-4b7b666fa800)

Se puede editar la IP y el puerto en botón de configuración. Al ejecutar MANDO.py aparecerá un mensaje 

* Running on http://192.168.1.108:5000

solo hay que copiar la IP (http://192.168.1.108) en la parte de arriba y el puerto (5000) en la parte de abajo y así conectaremos el movil con el ordenador.

El APP permite generar llamadas a nuevos endpoints de forma flexible en el panel de atajos.

<p align="center">
  <img src="https://github.com/user-attachments/assets/9ffba683-8a73-454f-b26c-6e0ec7bcca94" alt="img1" width="300"/>
  <img src="https://github.com/user-attachments/assets/dfc4cc2c-3a0e-47bf-81be-af589585dcca" alt="img2" width="300"/>
</p>


este atajo hará llamadas al endpoint que le hayas puesto de nombre en este caso, llamará a http://192.168.1.108:5000/cerrar

Puede personalizar los atajos y meterlos dentro de MANDO.py de la forma que quieras

## MANDO.py

Solo es un pequeño ejemplo de las funcionalidades que se pueden hacer, los atajos son tan expandibles como uno quiera.


