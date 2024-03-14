from seguridad.microservicios.security.validation_2fa_data_validator import validation_2fa_data_validator

# para testing, el codigo lo vamos a generar con esto:
# codigo_generado = pyotp.parse_uri('otpauth://totp/ExperimentoSeguridad:maria?secret=UniandesArquitectura&issuer=ExperimentoSeguridad')
# print(codigo_generado.now())

def validar_codigo(codigo_recibido):
    recibe_acceso = validation_2fa_data_validator(codigo_recibido)
    return recibe_acceso