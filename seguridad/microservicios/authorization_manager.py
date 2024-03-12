from security.twofa_code_generator import generate_2fa_code
from security.validation_2fa_data_validator import validation_2fa_data_validator
import pyotp

# tengo que cambiar este codigo para que haga lo q deberia hacer segun el plan
# lo que hay ahorita es para probar los codigods 2fa de autenticacion

# descomentando esta linea, se llama al generate_2fa_code
# que genera un qr.png que se puede agregar en la app de google
# generate_2fa_code(user_name="maria")

# para testing, el codigo lo vamos a generar con esto:
codigo_generado = pyotp.parse_uri('otpauth://totp/GeeksforGeeks:maria?secret=GeeksforGeeksIsBestForEverything&issuer=GeeksforGeeks')
print(codigo_generado.now())

codigo_recibido = input("Digite su codigo: (el codigo que se imprine en la linea anterior)")
recibe_acceso = validation_2fa_data_validator(codigo_recibido)
print(f"Recibe acceso: {recibe_acceso}")