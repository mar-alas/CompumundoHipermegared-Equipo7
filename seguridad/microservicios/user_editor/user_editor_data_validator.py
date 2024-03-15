import re

def validar_tamano(datos):
    if len(datos["username"]) > 20 or len(datos["name"]) < 2 or len(datos["phone"]) != 10:
        return False
    return True

def validar_username(username) -> bool:
    if not re.match(r'^[\w\.-]+@[\w\.-]+$', username):
        return False
    return True

def validar_nombre(nombre):
    if not nombre.isalpha():
        return False
    return True

def validar_phone(phone):
    if not phone.isdigit() or len(phone) != 10:
        return False
    return True

def validar_caracteres(datos):
    for key, value in datos.items():
        if not re.match("^[a-zA-Z0-9 ]+$", value):
            return False
    return True

def validate_request_to_edit_user(data):
    if data["name"] is not None and data["phone"] is not None and data["username"] is not None:
        if not validar_tamano(data):
            return "Invalid data size"
        
    if data["name"] is not None:
        if validar_nombre(data["name"]):
            return "Invalid name"
        
    if data["phone"] is not None:
        if not validar_phone(data["phone"]):
            return "Invalid phone"
        
    return "OK"