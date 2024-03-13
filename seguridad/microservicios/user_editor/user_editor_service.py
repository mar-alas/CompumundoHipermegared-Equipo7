from flask import Flask, request, jsonify

app = Flask(__name__)

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
