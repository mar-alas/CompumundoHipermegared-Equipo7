from flask import Flask, request, jsonify, abort
from user_editor_certificator import validate_certificate
from user_editor_data_validator import validate_request_to_edit_user
from flask_restful import Api,Resource
app = Flask(__name__)
api = Api(app)
import pandas as pd
import os
import time

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

def agregar_log_edicion_usuario(usuario,fecha_modificacion):
    """
    Esta funcion agrega un log de usuario al archivo de logs.
    """
    ruta_log_usuarios = '../base_datos/table_usuario_edicion_logs.csv'
    existe_csv=os.path.exists(ruta_log_usuarios)

    fecha_log= fecha_modificacion
    df_log_usuarios = pd.DataFrame({'fecha_log':[fecha_log],'usuario': [usuario],'edicion_exitosa':[1]})
    df_log_usuarios.to_csv(ruta_log_usuarios, mode='a', header=not(existe_csv), index=False, sep=';')


    
   

#@app.route('/api/v1/users', methods=['PUT'])
class UserEdition(Resource):
    def put(self):
        data = request.json
        data_pd = pd.DataFrame([data])
        print("Data to edit: ", data_pd)

        if "usuario" not in data_pd.columns:
            return jsonify({'message': 'Unauthorized access!'}), 401

        fecha_modificacion = time.strftime("%Y-%m-%d %H:%M:%S")
        data_pd['fecha_modificacion'] = fecha_modificacion
        data_pd.set_index('usuario', inplace=True)

        # Data Validation.
        #validation_result = validate_request_to_edit_user(data)
        #print("Validation result: ", validation_result)
        #validation_result="OK"
        #if validation_result!= "OK":
        #    return jsonify({'message': validation_result}), 400
        
        #if 'username' not in data:
        #    return jsonify({'message': 'Unauthorized access!'}), 401


        ruta_table_usuarios = '../base_datos/table_usuarios.csv'
        df_usuarios = pd.read_csv(ruta_table_usuarios, header=0, sep=';')

        if "usuario" not in df_usuarios.columns:
            return jsonify({'message': 'Error BD incorrecta!'}), 401

        df_usuarios.set_index('usuario', inplace=True)
        df_usuarios.update(data_pd)
        df_usuarios.reset_index(inplace=True)

        df_usuarios.to_csv(ruta_table_usuarios, sep=';', index=False)
        
        agregar_log_edicion_usuario(data['usuario'],fecha_modificacion)

        return jsonify({'message': 'Data edited successfully!'})
    
api.add_resource(UserEdition, '/api/v1/users')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3002)
