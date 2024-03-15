###
# Este componente simula el uso de certificados de seguridad para validar la autenticidad de las peticiones.
# El certificado y el keypass deben ser validos para que la peticion sea aceptada.
# El certificado y el keypass validos se encuentran en el directorio certificate.
# El certificado se encuentra en el archivo private-certificate.txt y el keypass en el archivo private-keypass.txt.
###

def validate_certificate(certificate, keypass):
    valid_certificate = get_certificate()
    valid_keypass = get_keypass()
    return certificate == valid_certificate and keypass == valid_keypass


def get_certificate():
    with open('certificate/private-certificate.txt', 'r') as file:
        content = file.read()
    return str(content)


def get_keypass():
    with open('certificate/private-keypass.txt', 'r') as file:
        content = file.read()
    return str(content)
