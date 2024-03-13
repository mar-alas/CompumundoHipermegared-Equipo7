from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy user data (replace this with your actual user data)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid username or password!'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5001)
