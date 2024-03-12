import pyotp
import qrcode

def generate_2fa_code(user_name: str):
    key = "GeeksforGeeksIsBestForEverything"
    uri = pyotp.totp.TOTP(key).provisioning_uri(
        name=user_name,
        issuer_name='GeeksforGeeks')
    print(uri)
    # Qr code generation step
    qrcode.make(uri).save("qr.png")
    