import faultier 
import serial
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

def print_title(title):
    print ("\033[1m" + title + "\033[0m")

def print_subtitle(subtitle):
    print ("\033[3m" + subtitle + "\033[0m")

def print_green(message):
    print("\033[92m" + message + "\033[0m")

def print_red(message):
    print("\033[91m" + message + "\033[0m")
    

# The Faultier comes up as two serial ports. 
# The first one is the control channel
# The second one is the UART bridge onto the 20-pin connector.

def find_serial_port(index):
    for port in serial.tools.list_ports.comports():
        #print (port.hwid)
        if "faultier" == port.serial_number.lower():
            if index == 0 and ":x.0" in port.hwid.lower():
                return port.device
            if index == 1 and ":x.3" in port.hwid.lower():
                return port.device
    return None

print          ("------------------------")
print_title    ("Hardware Hacking Village")
print_subtitle ("Fault Injection Workshop")
print          ("------------------------")
print ("")
print ("Demo: Atacar el GlichTag")
print ("")

paso = ""

try:
    paso = "Inicializar Faultier"
    ft = faultier.Faultier(find_serial_port(0))
    print_green ("[+] Faultier: OK")

    paso = f"Inicializar serial"    
    ser = serial.Serial(find_serial_port(1), baudrate=115200) 
    ser.timeout = 1 
    print_green (f"[+] Serial {ft.get_serial_path()}: OK")

    paso = f"Configurar glitcher"
    ft.configure_glitcher(
        glitch_output = faultier.OUT_CROWBAR
    )
    print_green ("[+] Configure Glitcher: OK")

    print_green ("[+] Ejecutar ataque...")
    
    paso = "Ejecutar ataque: ejecutar glitch"
    for d in range(0, 100000):
        for p in range(1, 10):
            if ser.in_waiting:
                ser.read(ser.in_waiting)
            ft.glitch(delay=d, pulse=p)
            data = ser.read(3)
            if b"X" in data:
                print_green (f"[+] Exito! Delay: {d} Pulse: {p} -> {ser.read(50)}")

except Exception as e:
    print_red (f"[-] Error: {paso}")
    print_red (f"[-] {e}")



