from flask import Flask, request, jsonify, abort
from user_editor_certificator import validate_certificate
from user_editor_data_validator import validate_request_to_edit_user

app = Flask(__name__)

# TODO: Cambiar AQUI el tamaño maximo de request que vamos a permitir para la prueba de seguridad.
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024 # 1MB
#app.config['MAX_CONTENT_LENGTH'] = 1 * 1 * 10 # 

@app.before_request
def check_request_size():
    """
    This function checks if the request size is valid.
    """
    content_length = request.content_length
    max_content_length = app.config['MAX_CONTENT_LENGTH']
    if content_length is not None and content_length > max_content_length:
        abort(413)  # 413 : Payload Too Large


@app.before_request
def check_certificate():
    """
    This function checks if the certificate is valid.
    # El certificado y el keypass deben ser enviados en el header de la peticion con los nombres 
    X-certificate-data y X-certificate-keypass respectivamente.
    """
    certificate_value = request.headers.get('X-certificate-data')
    if certificate_value is None:
        abort(401)

    keypass = request.headers.get('X-certificate-keypass')
    if keypass is None:
        abort(401)
    
    if not validate_certificate(certificate_value, keypass):
        abort(401)

data_to_edit = []

@app.route('/api/v1/users', methods=['PUT'])
def edit():
    data = request.json

    # Data Validation.
    validation_result = validate_request_to_edit_user(data)
    if validation_result!= "OK":
        return jsonify({'message': validation_result}), 400
    
    if 'username' not in data:
        return jsonify({'message': 'Unauthorized access!'}), 401

    new_data = data.get('new_data')
    data_to_edit.append(new_data)
    return jsonify({'message': 'Data edited successfully!', 'new_data': new_data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3002)
