# Archivo: registro_logs.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: registro de eventos y errores en el archivo de logs
# Responsable: Yeison Andrés

import logging

# Configuracion del registro de eventos y errores
logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# Funcion para guardar los eventos importantes del sistema
def registrar_evento(mensaje):
    logging.info(mensaje)


# Funcion para guardar los errores que se presenten
def registrar_error(mensaje):
    logging.error(mensaje)


# Funcion para guardar advertencias del sistema
def registrar_advertencia(mensaje):
    logging.warning(mensaje)
