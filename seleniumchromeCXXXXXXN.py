from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
import pyautogui
import string
import random
import sys
import argparse
import time

screenWidth, screenHeight = pyautogui.size() #obtiene resolución de la pantalla, en este caso 1440*900
browser = Chrome()
browser.get('https://www.cuantocabron.com/login')
#browser.close()

def stringR(size=10, chars=string.ascii_lowercase + string.digits): #Randomizer para crear strings, de largo 10 aleatorios.
    return ''.join(random.choice(chars) for _ in range(size))
    
def correoR(largo): #Randomizer para crear strings, que luego al ser concatenados con un @gmail.com, se crea un correo aleatorio.
    return ''.join(random.choice(string.ascii_letters) for x in range(largo))
    
def escrituraL(elemento, texto): #función para escribir cada letra con retrasos de 0.3s, para imitar a una persona
    for character in texto:
        elemento.send_keys(character)
        time.sleep(0.3)
    
def dentroLogin(): #función creada para poder salir o modificar la contraseña, luego de haber realizado un login correctamente.
        print ('Ingrese 0 para terminar, o 1 para modificar la contraseña')
        loginop = int(input())
        if (loginop == 0):
             print ('Finalizado')
        elif (loginop == 1):
             browser.get('https://mi.cuantocabron.com/cuenta')
             passwordCCold = browser.find_element_by_id('password1') #Se busca el espacio donde va la contraseña antigua
             passwordCCold.send_keys('Lp3AbamKNUSCSuN')
             passwordCCnueva = browser.find_element_by_id('password2') #Se busca el espacio donde va la nueva contraseña
             passwordNueva = stringR()
             passwordCCnueva.send_keys(passwordNueva)
             rpasswordCCnueva = browser.find_element_by_id('password3') #Se busca el espacio donde va la nueva contraseña (repetir)
             rpasswordCCnueva.send_keys(passwordNueva)
             button = browser.find_element_by_id('send_profile') #se busca el botón de guardar nueva contraseña
             #button.click() #Se clickea en el botón de reseteo de contraseña, comentado por comodidad
             print ('contraseña cambiada')
        else:
            print ('error')
             
def RegistroCC(): #Código para registro de cuenta con datos aleatorios en CC.
    pyautogui.click(507, 455) #clickea el botón de registró en una pantalla de 1440x900
    usuarioCC = browser.find_element_by_id('input-register-username') #Obtiene id de usuario en la página
    escrituraL(usuarioCC, stringR()) # Ingresa un usuario aleatorio
    emailCC = browser.find_element_by_id('input-register-email') #Obtiene el ID de mail
    emailCCunico = correoR(8) + '@gmail.com' #Crea un mail aleatorio y luego lo concatena con @gmail.com
    escrituraL(emailCC, emailCCunico) # Ingresa el mail generado anteriormente
    remailCC = browser.find_element_by_id('input-register-email_confirm') #Obtiene el ID de mail (reingreso)
    escrituraL(remailCC, emailCCunico) # Ingresa el mail generado anteriormente
    passwordCC = browser.find_element_by_id('input-register-password') #Se busca el ID de contraseña
    passwordCCunica = stringR() #Se crea una contraseña aleatoria
    escrituraL(passwordCC, passwordCCunica) # Ingresa la contraseña generada anteriormente
    rpasswordCC = browser.find_element_by_id('input-register-password_confirm') #Se busca el ID de contraseña (reingreso)
    escrituraL(rpasswordCC, passwordCCunica) # Ingresa la contraseña generada anteriormente
    button = browser.find_element_by_id('input-register-privacy') #se busca el botón de aceptar los términos y condiciones
    button.click() #Se clickea el botón del ToS
    button = browser.find_element_by_id('input-register-submit') #se busca el botón de registro
    button.click() #Se clickea en el botón de registro luego de ingresar todos los datos, si o si hay que hacer un captcha manualmente
    time.sleep (45) #se dam 45 segundos para ingresar el captacha manualmente
    try: #se verifica si se paso el captcha o no
        button = browser.find_element_by_id('input-register-submit') #ve si se sigue viendo el botón de registro
        button.click()
        print ('Registro completado')
    except NoSuchElementException:
        print ('Registro completado')

def LoginCC():
    username = browser.find_element_by_id('input-login-username') #encuentra el id de usuario para login
    escrituraL(username, 'panchotest') #con la función escrituraL se escribe lentamente letra por letra
    #username.send_keys('francisco.jaqueat@gmail.com') 
    password = browser.find_element_by_id('input-login-password') #encuentra donde poner password en el formulario
    escrituraL(password, 'Lp3AbamKNUSCSuN')
    #password.send_keys('Lp3AbamKNUSCSuN')
    button = browser.find_element_by_id('input-login-submit') #busca el botón para ingresar
    button.click() #lo apreta
    time.sleep(30) #la página pide captcha la primera vez, se dan 30 segundos para ingresarlo (al hacerlo muchas veces con la misma IP, el tiempo de cada captacha sube mucho si estos son fallados)
    try: #ve si se paso el captacha o no
        browser.find_element_by_id('input-login-submit') #si no se paso, se encuentra el botón nuevamente
        button.click() #apreta el botón nuevamente luego del captcha
        dentroLogin() #opciones dentro del login para salir o modificar contraseña
    except NoSuchElementException:
        dentroLogin() ##opciones dentro del login para salir o modificar contraseña
        
   
def RestablecerC():
    button = browser.find_element_by_id('tab-reset-password') #se busca el botón de restablecimiento de contraseña
    button.click() #Se clickea en el botón de recuperación de contraseña
    print ('seleccione si poner correo random o uno en específico, con 1 o 2 respectivamente')
    mailopcion = int(input("Ingresa la opción : "))
    if (mailopcion == 1):
        username = browser.find_element_by_id('input-reset-email')
        emailBunicoR = correoR(8) + '@gmail.com' #Crea un mail aleatorio y luego lo concatena con @gmail.com
        escrituraL (username, emailBunicoR)
        button = browser.find_element_by_id('input-reset-submit') #se busca el botón de restablecer contraseña
        button.click() #Se clickea en el botón de reset de contraseña luego de ingresar el correo
    elif (mailopcion == 2):
        correoreal = input("Ingresa el correo al cual se le quiere recuperar la contraseña : ")
        username = browser.find_element_by_id('input-reset-email')
        escrituraL (username, correoreal)
        button = browser.find_element_by_id('input-reset-email') #se busca el botón de restablecer contraseña
        button.click() #Se clickea en el botón de reset de contraseña luego de ingresar el correo
    else:
        print ('error')
print ('Selecciona 1 para Login (y poder modificar la contraseña), 2 Para Registro o 3 para restablecer contraseña')
opcion = int(input("Ingresa la opción : "))
if (opcion == 1):
    LoginCC()
elif (opcion == 2):
    RegistroCC()
elif (opcion == 3):
    RestablecerC()
else:
    print ('error')
    
