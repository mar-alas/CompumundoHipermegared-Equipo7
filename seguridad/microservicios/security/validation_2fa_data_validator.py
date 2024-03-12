import time 
import pyotp 


def validation_2fa_data_validator(code):
    key = "UniandesArquitectura"
    totp = pyotp.TOTP(key)
    # verifying the code
    return totp.verify(code)