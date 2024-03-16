#autor: daniel
# script que corre experimento de edicion no autorizada en la base de datos

import os
os.chdir("seguridad/pruebas_experimento")

from experimento_utils import setup_experimento
from experimento_utils import teardown_experimento
from experimento_utils import modificar_sin_autorizacion_bd
from experimento_utils import detectar_modificacion_sin_autorizacion_bd
import time
import pandas as pd

ruta_resultado_experimento="resultados_experimentos/resultados_experimento_integridad_003_edicion_no_autorizada.csv"
fecha_experimento=time.strftime("%Y-%m-%d %H:%M:%S")

setup_experimento()

usuario_prueba="dgamez@gmail.com"

if not detectar_modificacion_sin_autorizacion_bd(usuario_prueba):
    print("La base de datos NO fue modificada sin autorización")
else:
    print("La base de datos FUE modificada sin autorización")

modificar_sin_autorizacion_bd(usuario_prueba)
time.sleep(5)

deteccion_modificacion=detectar_modificacion_sin_autorizacion_bd(usuario_prueba)
if not deteccion_modificacion:
    print("La base de datos NO fue modificada sin autorización")
else:
    print("La base de datos FUE modificada sin autorización")

resultado_experimento=pd.DataFrame({'fecha':[fecha_experimento],
                                    'nombre_experimento':["experimento_integridad_003_edicion_no_autorizada"],
                                    'categoria':['integridad'],
                                    'id_request':[1],
                                    'request':['modificar_sin_autorizacion_bd'],
                                    'response':['La base de datos FUE modificada sin autorización'],
                                    'tipo_resultado':['booleano_deteccion_ataque'],
                                    'resultado_esperado':['True'],
                                    'resultado_obtenido':deteccion_modificacion,
                                    'LOGIN_LIMITER_MAX':[None]
                                    })
resultado_experimento.to_csv(ruta_resultado_experimento, index=False, header=True, sep=";")