import re


def validar_username(username) -> bool:
    # Verificar si el campo username es un correo válido
    if not re.match(r'^[\w\.-]+@[\w\.-]+$', username):
        return False
    return True

def validar_code(code) -> bool:
    # Verificar si el campo code tiene menos de 10 dígitos y es un número
    if not code.isdigit() or len(code) > 10:
        return False
    return True

def validar_password(password) -> bool:
    # Verificar si el campo code tiene menos de 10 dígitos y es un número
    if not len(password) >=8:
        return False
    return True

def validar_contrasena(contrasena):
    # Longitud mínima de 8 caracteres
    if len(contrasena) < 8:
        return False, 'La contraseña debe tener al menos 8 caracteres'

    # Contiene letras mayúsculas y minúsculas, números y caracteres especiales
    if not re.search(r'[A-Z]', contrasena) or \
       not re.search(r'[a-z]', contrasena) or \
       not re.search(r'[0-9]', contrasena) or \
       not re.search(r'[^A-Za-z0-9]', contrasena):
        return False, 'La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial'

    # No utilizar información personal
    if re.search(r'\b(nombre|apellido|fecha|telefono)\b', contrasena, flags=re.IGNORECASE):
        return False, 'La contraseña no debe contener información personal como nombre, apellido, fecha de nacimiento o número de teléfono'

    # No utilizar palabras comunes o secuencias alfabéticas o numéricas
    palabras_comunes = ['123456', 'password', 'qwerty', 'admin', 'abcd', '987654']
    if contrasena.lower() in palabras_comunes or \
       any(contrasena[i:i+3].lower() == contrasena[i]*3 for i in range(len(contrasena)-2)) or \
       any(ord(contrasena[i+1]) - ord(contrasena[i]) == 1 for i in range(len(contrasena)-1)):
        return False, 'La contraseña no debe ser una palabra común, una secuencia alfabética o numérica'

    return True, 'La contraseña cumple con la política de seguridad'

def validar_request(username, password, code) -> str:

    if not username or username.strip() == '':
        return 'El campo username está vacío o nulo'
    
    if not password or password.strip() == '':
        return 'El campo password está vacío o nulo'

    if not code or code.strip() == '':
        return 'El campo code está vacío o nulo'

    if not validar_username(username):
        return 'Username inválido'

    if not validar_code(code):
        return 'Code inválido', 400
    
    if not validar_password(password):
        return 'Password inválida'
    
    # Validamos cumpleimiento de la politica de claves.
    complies_policy, message = validar_contrasena(password)
    if not complies_policy:
        return message

    return 'OK'

