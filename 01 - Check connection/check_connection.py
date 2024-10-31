import faultier 
import serial

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

print_title    ("Hardware Hacking Village")
print_subtitle ("Fault Injection Workshop")
print          ("------------------------")
print ("")
print ("Demo: se verificará la conexión con la Faultier")
print ("")

try:
    ft = faultier.Faultier(find_serial_port(0))
    print_green ("[+] Faultier: OK")
except Exception:
    print_red ("[-] Faultier: Fallo. Verifique conexión y firmwware")

