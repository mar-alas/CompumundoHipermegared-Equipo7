
from user_registration_service_principal import registrar_usuario_principal

def registrar_usuario_manager(email):
    try:
        registrar_usuario_principal.delay(email)
    except Exception as e:
        try:
            from user_registration_service_redundancia1 import registrar_usuario_redundancia1
            registrar_usuario_redundancia1.delay(email)
        except Exception as e:
            from user_registration_service_redundancia2 import registrar_usuario_redundancia2
            registrar_usuario_redundancia2.delay(email)
    