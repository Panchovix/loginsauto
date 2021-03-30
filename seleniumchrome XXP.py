from selenium.webdriver import Chrome
import pyautogui
import string
import random
import sys
import argparse
import time

screenWidth, screenHeight = pyautogui.size() #obtiene resolución de la pantalla, en este caso 1440*900
browser = Chrome()
browser.get('https://bip.cl/canasta')
#browser.close()

def calculaDV(rut): #Calcula dígito verificador para obtener un RUT válido
    rut_str=str(rut)[::-1] #Se invierte el RUT
    multiplicador=2
    suma=0
    for c in rut_str: #Se itera sobre los carácteres con el RUT ya invertido, para luego sumar los digitos* con el multiplicador.
        suma+=int(c)*multiplicador
        multiplicador+=1
        if multiplicador>7:
            multiplicador=2
    dv=str(11-(suma%11))  # 11 - Módulo
    #Para excepciones (rut 11, o 10 a 0 y K, respectivamente)
    if dv=='11':
        dv='0'
    if dv=='10':
        dv='K'
    return dv
    
def generaRut(rango_inf, rango_sup): #En conjunto a la función CalculaDV, genera un RUT completo y válido.
    rut=random.randint(rango_inf, rango_sup)
    dv=calculaDV(rut)
    res=str(rut)+'-'+dv
    return res

def stringR(size=10, chars=string.ascii_lowercase + string.digits): #Randomizer para crear strings, de largo 10 aleatorios.
    return ''.join(random.choice(chars) for _ in range(size))
    
def correoR(largo): #Randomizer para crear strings, que luego al ser concatenados con un @gmail.com, se crea un correo aleatorio.
    return ''.join(random.choice(string.ascii_letters) for x in range(largo))
    
def RegistroBIP(): #Código para registro de cuenta con datos aleatorios en BIP, y válidos (RUT especialmente)
    pyautogui.click(113, 774) #clickea el botón de registró en una pantalla de 1440x900
    nombreB = browser.find_element_by_id('nombre') #Obtiene id de nombre en la página
    nombreB.send_keys(stringR()) #Ingresa un nombre aleatorio en ese elemento.
    apellidoB = browser.find_element_by_id('apellido') #Obtiene id de apellido en la página
    apellidoB.send_keys(stringR()) #Genera e ingresa un apellido aleatorio para ese elemento.
    rutB = browser.find_element_by_id('rut') #Busca el id con respecto a RUT
    rutRandom = random.randint(1000000, 100000000) #Se crea un RUT, sin digito verificador entre 1.000.000 y 100.000.000
    rutRandomString = str(rutRandom) #Convierte el int a string
    rutRandomDigito = rutRandomString + '0' #Concatena el RUT más un digito verificador temporal 0
    rutRandomDigitoValido= calculaDV(rutRandomDigito) #Se ingresa el rut creado anteriormente, para luego calcular un dígito verificador válido para ese RUT.
    rutValido = generaRut(1000000,100000000) #Con el digito verificador válido, se aplica al RUT anterior y se guarda en la variable rutValido.
    rutB.send_keys(generaRut(1000000,100000000)) #Se crea un RUT en el intervalo mencionado anteriormente, y se ingresa en el formulario de registro.
    fonoB = browser.find_element_by_id('fono') #Obtiene el ID de fono
    fonoB.send_keys(random.randint(11111111, 99999999)) #Ingresa fono aleatorio entre el intervalo.
    emailB = browser.find_element_by_id('email') #Obtiene el ID de mail
    emailBunico = correoR(8) + '@gmail.com' #Crea un mail aleatorio y luego lo concatena con @gmail.com
    emailB.send_keys(emailBunico) #Ingresa el mail generado anteriormente
    remailB = browser.find_element_by_id('remail') #Obtiene el ID de mail (reingreso)
    remailB.send_keys(emailBunico) #Se ingresa el mail generado anteriormente.
    passwordB = browser.find_element_by_id('contrasenia') #Se busca el ID de contraseña
    passwordBunica = stringR() #Se crea una contraseña aleatoria
    passwordB.send_keys(passwordBunica) # Se ingresa la contraseña creada anteriormente.
    rpasswordB = browser.find_element_by_id('rcontrasenia') #Se busca el ID de contraseña (reingreso)
    rpasswordB.send_keys(passwordBunica) #Se ingresa la contraseña creada anteriormente
    button = browser.find_element_by_id('btnRegistro') #se busca el botón de registro
    button.click() #Se clickea en el botón de registro luego de ingresar todos los datos
    print ('Registro completado')

def LoginBIP():
    username = browser.find_element_by_id('usuario') #encuentra el id de usuario para login
    username.send_keys('panchovixmenn@gmail.com') #ingresa el usuario, (mail) en este caso
    password = browser.find_element_by_id('clave') #encuentra donde poner password en el formulario
    password.send_keys('B5wNeV5yzrKziMV') #ingresa la contraseña
    button = browser.find_element_by_id('btnIngreso') #busca el botón para ingresar
    button.click() #lo apreta
    print ('Ingrese 0 para terminar, o 1 para modificar la contraseña')
    loginop = int(input())
    if (loginop == 0):
         print ('Finalizado')
    else:
         pyautogui.click(200, 515) #mueve el cursor y apreta en mi Cuenta
         time.sleep(5) #espera 5 segundos
         pyautogui.click(408, 505) #mueve el cursor a mi Perfil
         time.sleep(3) #espera 3 segundos
         passwordL = browser.find_element_by_id('contrasenia') #Se busca el ID de contraseña
         passwordNueva = stringR()
         passwordL.send_keys(passwordNueva)
         rpasswordL = browser.find_element_by_name('rcontrasenia') #Se busca el name de la contraseña (ya que en este caso BIP uso el mismo ID para ambos campos)
         rpasswordL.send_keys(passwordNueva)
         button = browser.find_element_by_id('btnGuardarPerfil') #se busca el botón de guardar nueva contraseña
         #button.click() #Se clickea en el botón de reseteo de contraseña, comentado por comodidad
         print ('contraseña cambiada')
   
def RestablecerC():
    pyautogui.click(113, 720)
    print ('seleccione si poner correo random o uno en específico, con 1 o 2 respectivamente')
    mailopcion = int(input("Ingresa la opción : "))
    if (mailopcion == 1):
        username = browser.find_element_by_id('usuario')
        emailBunicoR = correoR(8) + '@gmail.com' #Crea un mail aleatorio y luego lo concatena con @gmail.com
        username.send_keys(emailBunicoR)
        button = browser.find_element_by_id('btnRecordar') #se busca el botón de registro
        button.click() #Se clickea en el botón de registro luego de ingresar todos los datos
    elif (mailopcion == 2):
        correoreal = input("Ingresa el correo al cual se le quiere recuperar la contraseña : ")
        username = browser.find_element_by_id('usuario')
        username.send_keys(correoreal)
        button = browser.find_element_by_id('btnRecordar') #se busca el botón de registro
        button.click() #Se clickea en el botón de registro luego de ingresar todos los datos
    else:
        print ('error')
print ('Selecciona 1 para Login (y poder modificar la contraseña), 2 Para Registro o 3 para restablecer contrasenia')
opcion = int(input("Ingresa la opción : "))
if (opcion == 1):
    LoginBIP()
elif (opcion == 2):
    RegistroBIP()
else:
    RestablecerC()
    
