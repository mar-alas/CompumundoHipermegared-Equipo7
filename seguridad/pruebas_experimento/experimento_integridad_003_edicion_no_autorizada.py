#autor: daniel
# script que corre experimento de edicion no autorizada en la base de datos
#este script se corre desde la carpeta de seguridad
#con el comando python3 pruebas_experimento/experimento_integridad_003_edicion_no_autorizada.py

import os
#os.chdir("seguridad")

from experimento_utils import setup_experimento
from experimento_utils import teardown_experimento
from experimento_utils import modificar_sin_autorizacion_bd
from experimento_utils import detectar_modificacion_sin_autorizacion_bd
from experimento_utils import agregar_usuario_bd
import time
import pandas as pd
from faker import Faker

ruta_resultado_experimento="pruebas_experimento/resultados_experimentos/resultados_experimento_integridad_003_edicion_no_autorizada.csv"
fecha_experimento=time.strftime("%Y-%m-%d %H:%M:%S")
fecha_experimento_menos1dia=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-86400))
setup_experimento()

numero_iteraciones=200

for intento in range(1, numero_iteraciones+1):
    # Your code here
    fake = Faker()
    usuario_prueba = fake.email()
    agregar_usuario_bd(usuario=usuario_prueba,
                        contrasenia="Password1!",
                        nombre_usuario=fake.name(),
                        fecha_insercion=fecha_experimento_menos1dia,
                        fecha_modificacion=fecha_experimento_menos1dia)

    modificar_sin_autorizacion_bd(usuario_prueba)
    time.sleep(0.2)

    deteccion_modificacion=detectar_modificacion_sin_autorizacion_bd(usuario_prueba)

    resultado_experimento=pd.DataFrame({'fecha':[fecha_experimento],
                                        'nombre_experimento':["experimento_integridad_003_edicion_no_autorizada"],
                                        'categoria':['integridad'],
                                        'id_request':[intento],
                                        'request':['modificar_sin_autorizacion_bd'],
                                        'response':['La base de datos FUE modificada sin autorización'],
                                        'tipo_resultado':['booleano_deteccion_ataque'],
                                        'resultado_esperado':['True'],
                                        'resultado_obtenido':deteccion_modificacion,
                                        'LOGIN_LIMITER_MAX':[None]
                                        })
    resultado_experimento.to_csv(ruta_resultado_experimento, mode='a', index=False, header=False, sep=";")
    print("intento: ", intento)