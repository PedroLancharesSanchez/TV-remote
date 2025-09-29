from flask import Flask, request, jsonify
import pyautogui
from threading import Lock

# Para brillo con WMI
try:
    import wmi
    import pythoncom
except ImportError:
    wmi = None
    pythoncom = None

# Para volumen con Pycaw
try:
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
except ImportError:
    AudioUtilities = None
    CLSCTX_ALL = None
    IAudioEndpointVolume = None

app = Flask(__name__)

estado = {
    "raton": {"dx": 0, "dy": 0},
    "click": {"boton": ""},
    "brillo": 0,
    "volumen": 0,
    "texto": "",
    "pantalla": "on"
}

# === OBJETO GLOBAL DE AUDIO ===
audio_lock = Lock()
audio_interface = None

def inicializar_audio():
    global audio_interface
    if AudioUtilities is None:
        print("⚠️ Pycaw no disponible")
        return
    try:
        import pythoncom
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        audio_interface = cast(interface, POINTER(IAudioEndpointVolume))
        print("🔊 Audio inicializado correctamente")
    except Exception as e:
        print("⚠️ Error inicializando audio:", e)

inicializar_audio()

# === UTILIDADES ===
def extraer_valor(texto):
    try:
        return int(''.join(filter(str.isdigit, str(texto))))
    except:
        return None

def ajustar_brillo(valor):
    if wmi is None:
        print("⚠️ WMI no disponible")
        return
    pythoncom.CoInitialize()
    try:
        valor = max(0, min(valor, 100))
        c = wmi.WMI(namespace='wmi')
        for monitor in c.WmiMonitorBrightnessMethods():
            monitor.WmiSetBrightness(int(valor), 0)
        print(f"💡 Brillo ajustado a {valor}%")
        estado["brillo"] = valor
    finally:
        pythoncom.CoUninitialize()

def ajustar_volumen(valor):
    global audio_interface
    if audio_interface is None:
        print("⚠️ Audio no inicializado")
        return
    valor = max(0, min(valor, 100))
    with audio_lock:
        try:
            audio_interface.SetMasterVolumeLevelScalar(valor / 100, None)
            estado["volumen"] = valor
            print(f"🔊 Volumen ajustado a {valor}%")
        except Exception as e:
            print("⚠️ Error ajustando volumen:", e)

# === ENDPOINTS ===
@app.route("/raton", methods=["POST"])
def raton():
    data = request.get_json()
    dx = data.get("dx", 0)
    dy = data.get("dy", 0)
    pyautogui.moveRel(dx, dy)
    estado["raton"] = data
    return jsonify({"status": "ok"})

@app.route("/click", methods=["POST"])
def click():
    data = request.get_json()
    tipo = data.get("boton", "izquierdo")
    if tipo == "izquierdo":
        pyautogui.click()
    elif tipo == "derecho":
        pyautogui.click(button="right")
    estado["click"] = data
    return jsonify({"status": "ok"})

@app.route("/brillo", methods=["POST"])
def brillo():
    data = request.get_json()
    valor = data.get("brillo")
    if valor is not None:
        ajustar_brillo(valor)
    return jsonify({"status": "ok"})

@app.route("/volumen", methods=["POST"])
def volumen():
    data = request.get_json()
    valor = data.get("volumen")
    if valor is not None:
        ajustar_volumen(valor)
    return jsonify({"status": "ok"})

@app.route("/texto", methods=["POST"])
def texto():
    data = request.get_json()
    t = data.get("texto", "")
    if t == "backspace":
        pyautogui.press("backspace")
    else:
        pyautogui.typewrite(t)
    estado["texto"] = t
    return jsonify({"status": "ok"})

import os

import ctypes

# Estado interno de la pantalla
pantalla_apagada = False

@app.route("/power", methods=["POST"])
def power():
    global pantalla_apagada
    data = request.get_json()
    accion = data.get("accion", "")
    print(data    )

    if accion == "apagar":
        if not pantalla_apagada:
            # Apagar monitor
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, 2)
            pantalla_apagada = True
            estado["pantalla"] = "off"
            print("🖥 Pantalla apagada")
        else:
            # Encender monitor simulando actividad
            pyautogui.click()
            pantalla_apagada = False
            estado["pantalla"] = "on"
            print("🖥 Pantalla encendida")
 
    return jsonify({"status": "ok", "pantalla": estado["pantalla"]})


@app.route("/estado", methods=["GET"])
def get_estado():
    return jsonify(estado)

import subprocess
import webbrowser

@app.route("/Netflix", methods=["POST"])
def abrir_netflix():
    try:
        # Intentar abrir con la ruta habitual de Chrome en Windows
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        url = "https://www.netflix.com"
        subprocess.Popen([chrome_path, url])
        print("🎬 Netflix abierto en Chrome")
        return jsonify({"status": "ok", "accion": "Netflix abierta"})
    except Exception as e:
        print("⚠️ Error abriendo Netflix:", e)
        return jsonify({"status": "error", "detalle": str(e)}), 500

@app.route("/YouTube", methods=["POST"])
def abrir_youtube():
    try:
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        url = "https://www.youtube.com"
        subprocess.Popen([chrome_path, url])
        print("▶️ YouTube abierto en Chrome")
        return jsonify({"status": "ok", "accion": "YouTube abierta"})
    except Exception as e:
        print("⚠️ Error abriendo YouTube:", e)
        return jsonify({"status": "error", "detalle": str(e)}), 500
    
@app.route("/cerrar", methods=["POST"])
def cerrar():
    try:
        pyautogui.hotkey("alt", "f4")  # Cierra la ventana activa
        print("❌ Aplicación cerrada (Alt+F4)")
        return jsonify({"status": "ok", "accion": "ventana cerrada"})
    except Exception as e:
        print("⚠️ Error cerrando aplicación:", e)
        return jsonify({"status": "error", "detalle": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
