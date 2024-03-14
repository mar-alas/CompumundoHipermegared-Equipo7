from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# TODO: Cambiar AQUI el tamaño maximo de request que vamos a permitir para la prueba de seguridad.
# app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 # 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1 * 10 # 

@app.before_request
def check_request_size():
    content_length = request.content_length
    max_content_length = app.config['MAX_CONTENT_LENGTH']
    if content_length is not None and content_length > max_content_length:
        abort(413)  # 413 : Payload Too Large


# Dummy data for demonstration
data_to_edit = []

@app.route('/edit', methods=['POST'])
def edit():
    data = request.json
    # Check if user is authenticated (you may implement this logic)
    if 'username' not in data:
        return jsonify({'message': 'Unauthorized access!'}), 401

    new_data = data.get('new_data')
    data_to_edit.append(new_data)
    return jsonify({'message': 'Data edited successfully!', 'new_data': new_data}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
