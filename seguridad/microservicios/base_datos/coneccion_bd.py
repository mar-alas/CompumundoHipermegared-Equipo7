import csv

def validar_datos_usuario(username, password):
    # Initialize an empty dictionary
    users = {}
    # Open the CSV file
    with open("seguridad/microservicios/base_datos/table_usuarios.csv", mode='r') as file:
        # Create a CSV reader object
        reader = csv.reader(file, delimiter=';')
        # Skip the header if present
        next(reader, None)
        # Loop through each row in the CSV file
        for row in reader:
            # Extract email and password from the row
            email, password, _ = row
            # Add the email and password to the dictionary
            users[email.strip()] = password.strip()
    if username in users and users[username] == password:
        return True
    else:
        return False
