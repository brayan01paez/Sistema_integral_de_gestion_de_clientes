# Archivo: reserva.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: clase Reserva y gestión de reservas
# Responsable: Esneyder

# Importe las excepciones y las funciones para guardar eventos y errores en el log
from excepciones import ErrorSistema, ErrorValidacion, ErrorNoEncontrado, ErrorOperacion
from registro_logs import registrar_evento, registrar_error


class Reserva:

    def __init__(self, id_reserva, cliente, servicio, duracion):
        if cliente is None or servicio is None:
            raise ErrorValidacion("La reserva necesita un cliente y un servicio.")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorValidacion("La duración debe ser un número mayor que cero.")
        if not getattr(servicio, "disponible", True):
            raise ErrorOperacion(f"El servicio '{servicio.nombre}' no está disponible.")

        # Atributos
        self.__id = id_reserva
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

    # lectura para la consulta del ID
    @property
    def id(self):
        return self.__id

    # lectura para consultar el estado
    @property
    def estado(self):
        return self.__estado

    # calculo de costos
    def calcular_total(self, impuesto=0, descuento=0):
        try:
            if descuento < 0 or descuento > 1:
                raise ValueError("El descuento debe estar entre 0 y 1.")
            costo = self.__servicio.calcular_costo()
            return costo * (1 - descuento) * (1 + impuesto)
        except Exception as error:
            raise ErrorOperacion("No se pudo calcular el total de la reserva.") from error

    # Se confirma la reserva pero solo si esta pendiente
    def confirmar(self):
        if self.__estado != "Pendiente":
            raise ErrorOperacion(f"No se puede confirmar una reserva {self.__estado}.")
        self.__estado = "Confirmada"
        registrar_evento(f"Reserva {self.__id} confirmada.")

    # Se cancela la reserva, claramente si no esta cancelada o procesada
    def cancelar(self):
        if self.__estado in ("Cancelada", "Procesada"):
            raise ErrorOperacion(f"No se puede cancelar una reserva {self.__estado}.")
        self.__estado = "Cancelada"
        registrar_evento(f"Reserva {self.__id} cancelada.")

    # Procesa la reserva y devuelve el total a pagar, pero valga la redundancia debe estar confirmada
    def procesar(self):
        try:
            # Solo se procesa una reserva confirmada
            if self.__estado != "Confirmada":
                raise ErrorOperacion("La reserva debe estar confirmada.")
            total = self.calcular_total(impuesto=0.19)
        except ErrorSistema as error:
            # Si falla, esto guarda el error y arroja uno nuevo conservando el original
            registrar_error(f"Error al procesar la reserva {self.__id}: {error}")
            raise ErrorOperacion("No se pudo procesar la reserva.") from error
        else:
            # Solo se va a ejecutar si no hubo errores :v
            self.__estado = "Procesada"
            registrar_evento(f"Reserva {self.__id} procesada. Total: {total}")
            return total
        finally:
            # Se va a ejecutar siempre , haya o no haya error, en otras palabras por que si, porque no y por si acaso xd
            registrar_evento(f"Fin del intento de procesar la reserva {self.__id}.")

    # Esta partecita corresponde al texto con los datos de la reserva
    def __str__(self):
        return (f"Reserva {self.__id} | {self.__cliente.nombre} | "
                f"{self.__servicio.nombre} | {self.__duracion} h | {self.__estado}")


# Esta clasesita va a guardar las reservas en una lista
class GestorReservas:

    def __init__(self):
        self.__reservas = []

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(len(self.__reservas) + 1, cliente, servicio, duracion)
        except ErrorSistema as error:
            registrar_error(f"No se creó la reserva: {error}")
            print(f"[ERROR] {error}")
            return None
        else:
            # Solo se va a guardar en la lista si se creó bien, sino pues no 
            self.__reservas.append(reserva)
            registrar_evento(f"Reserva {reserva.id} creada.")
            print(f"[OK] {reserva}")
            return reserva

    # Esta seccion busca una reserva por su id, pero si no existe arroja el mensaje ErrorNoEncontrado
    def buscar(self, id_reserva):
        for reserva in self.__reservas:
            if reserva.id == id_reserva:
                return reserva
        raise ErrorNoEncontrado(f"No existe la reserva {id_reserva}.")

    # Esta confirma la reserva por el id
    def confirmar_reserva(self, id_reserva):
        try:
            self.buscar(id_reserva).confirmar()
            print(f"[OK] Reserva {id_reserva} confirmada.")
        except ErrorSistema as error:
            registrar_error(f"Error al confirmar: {error}")
            print(f"[ERROR] {error}")

    # Permite cancelar la reserva por el id
    def cancelar_reserva(self, id_reserva):
        try:
            self.buscar(id_reserva).cancelar()
            print(f"[OK] Reserva {id_reserva} cancelada.")
        except ErrorSistema as error:
            registrar_error(f"Error al cancelar: {error}")
            print(f"[ERROR] {error}")

    # Procesa la reserva por el id y muestra el total
    def procesar_reserva(self, id_reserva):
        try:
            total = self.buscar(id_reserva).procesar()
            print(f"[OK] Reserva {id_reserva} procesada. Total: {total:,.2f}")
        except ErrorSistema as error:
            registrar_error(f"Error al procesar: {error}")
            print(f"[ERROR] {error} (causa: {error.__cause__})")

    # Por ultimo pero no menos importante, esta ultima partecita, muestra todas las reservas guardadas
    def listar(self):
        for reserva in self.__reservas:
            print(reserva)