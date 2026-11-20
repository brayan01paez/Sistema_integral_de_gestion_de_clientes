
# Archivo: main.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: programa principal con la simulación de las 10 operaciones
# Responsables: todos los integrantes del grupo

from cliente import Cliente
from servicio import ReservaSalas, AlquilerEquipos, AsesoriasEspecializadas
from reserva import GestorReservas
from excepciones import ErrorSistema
from registro_logs import registrar_evento, registrar_error


print("=" * 60)
print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
print("=" * 60)

registrar_evento("Inicio del programa principal.")

# ==========================================================
# OPERACIÓN 1. CREACIÓN Y VALIDACIÓN DE CLIENTES
# ==========================================================

print("\nOPERACIÓN 1: CREACIÓN Y VALIDACIÓN DE CLIENTES")

try:
    cliente = Cliente(
        "123456",
        "Carlos",
        "carlos@gmail.com",
        "3001234567"
    )

    print("[OK]", cliente.describir())
    print("Validación:", cliente.validar())

except ErrorSistema as error:
    registrar_error(f"Error al crear el cliente: {error}")
    print("[ERROR]", error)

# Se intenta crear un cliente con información incorrecta
try:
    Cliente("789456", "", "correo@gmail.com", "3001234567")

except ErrorSistema as error:
    registrar_error(f"Cliente rechazado: {error}")
    print("[ERROR] Cliente no creado:", error)


# ==========================================================
# OPERACIÓN 2. REGISTRO DE LOS SERVICIOS
# ==========================================================

print("\nOPERACIÓN 2: REGISTRO DE SERVICIOS")

try:
    sala = ReservaSalas(
        "S01", "Sala de reuniones", 50000, 15, 3
    )

    equipos = AlquilerEquipos(
        "E01", "Alquiler de computadores", 30000, 2, 2
    )

    asesoria = AsesoriasEspecializadas(
        "A01", "Asesoría de sistemas", 100000, "Senior", 2
    )

    print(sala.describir_servicio())
    print(equipos.describir_servicio())
    print(asesoria.describir_servicio())

    registrar_evento("Servicios registrados correctamente.")

except (ErrorSistema, ValueError) as error:
    registrar_error(f"Error al registrar servicios: {error}")
    print("[ERROR]", error)


# Se crea el administrador de reservas
gestor = GestorReservas()


# ==========================================================
# OPERACIÓN 3. CREACIÓN DE UNA RESERVA DE SALA
# ==========================================================

print("\nOPERACIÓN 3: RESERVA DE SALA")

reserva_sala = gestor.crear_reserva(cliente, sala, 3)


# ==========================================================
# OPERACIÓN 4. CREACIÓN DE UN ALQUILER DE EQUIPOS
# ==========================================================

print("\nOPERACIÓN 4: ALQUILER DE EQUIPOS")

reserva_equipos = gestor.crear_reserva(cliente, equipos, 2)


# ==========================================================
# OPERACIÓN 5. CREACIÓN DE UNA ASESORÍA
# ==========================================================

print("\nOPERACIÓN 5: ASESORÍA ESPECIALIZADA")

reserva_asesoria = gestor.crear_reserva(cliente, asesoria, 2)


# ==========================================================
# OPERACIÓN 6. CONSULTA DE LAS RESERVAS
# ==========================================================

print("\nOPERACIÓN 6: CONSULTA DE RESERVAS")

gestor.listar()


# ==========================================================
# OPERACIÓN 7. CONFIRMACIÓN DE LAS RESERVAS
# ==========================================================

print("\nOPERACIÓN 7: CONFIRMACIÓN DE RESERVAS")

gestor.confirmar_reserva(1)
gestor.confirmar_reserva(2)
gestor.confirmar_reserva(3)


# ==========================================================
# OPERACIÓN 8. PROCESAMIENTO Y CÁLCULO DE PAGOS
# ==========================================================

print("\nOPERACIÓN 8: PROCESAMIENTO DE RESERVAS")

gestor.procesar_reserva(1)
gestor.procesar_reserva(2)
gestor.procesar_reserva(3)


# ==========================================================
# OPERACIÓN 9. PRUEBAS DE DATOS Y BÚSQUEDAS INCORRECTAS
# ==========================================================

print("\nOPERACIÓN 9: PRUEBAS DE ERRORES")

# Se intenta crear una reserva con duración igual a cero
gestor.crear_reserva(cliente, sala, 0)

# Se busca una reserva que no existe
try:
    gestor.buscar(99)

except ErrorSistema as error:
    registrar_error(f"Búsqueda fallida: {error}")
    print("[ERROR]", error)


# ==========================================================
# OPERACIÓN 10. CONTROL DE ESTADOS Y CONTINUIDAD
# ==========================================================

print("\nOPERACIÓN 10: CONTROL DE ESTADOS")

# Se crea una reserva que queda pendiente
reserva_pendiente = gestor.crear_reserva(cliente, sala, 1)

# Se intenta procesar sin haber confirmado
gestor.procesar_reserva(4)

# Se cancela la reserva pendiente
gestor.cancelar_reserva(4)

# Se intenta cancelar nuevamente una reserva cancelada
gestor.cancelar_reserva(4)


# ==========================================================
# FINALIZACIÓN DEL PROGRAMA
# ==========================================================

print("\nESTADO FINAL DE LAS RESERVAS")

gestor.listar()

registrar_evento("Finalización del programa principal.")

print("\nEl sistema terminó sus operaciones.")
print("Los eventos y errores fueron registrados en sistema.log.")
