# Archivo: excepciones.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: excepciones personalizadas del sistema
# Responsable: Yeison Andrés


# Excepcion principal para los errores del sistema
class ErrorSistema(Exception):
    pass


# Se utiliza cuando un dato ingresado no es correcto
class ErrorValidacion(ErrorSistema):
    pass


# Se utiliza cuando no se encuentra un cliente, servicio o reserva
class ErrorNoEncontrado(ErrorSistema):
    pass


# Se utiliza cuando no se puede completar una operacion
class ErrorOperacion(ErrorSistema):
    pass
