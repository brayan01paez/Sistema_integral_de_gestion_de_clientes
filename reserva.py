# Archivo: reserva.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: clase Reserva y gestión de reservas
# Responsable: Esneyder

from datetime import datetime

# Esto solo lo agregue de manera temporal para que el codigo no falle, pero pues ya cuando se cuente con la info de los compañeros pues lo corregire y actualizare

class ReservaError(Exception):
    # El error sera solo al momento de crear o manejar una reserva
    pass


def registrar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now()} | {mensaje}\n")
# ---------------------------------------------------------------


class Reserva:

    def __init__(self, id_reserva, cliente, servicio, duracion):
        # Esta parte corresponde a validaciones por ende, si algo está mal, arroja un error
        if cliente is None or servicio is None:
            raise ReservaError("La reserva necesita un cliente y un servicio.")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaError("La duración debe ser un número mayor que cero.")
        if not servicio.disponible:
            raise ReservaError(f"El servicio '{servicio.nombre}' no está disponible.")

        # Los atributos 
        self.__id = id_reserva
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

    @property
    def id(self):
        return self.__id

    @property
    def estado(self):
        return self.__estado

    def calcular_total(self, impuesto=0, descuento=0):
        try:
            if descuento < 0 or descuento > 1:
                raise ValueError("El descuento debe estar entre 0 y 1.")
            costo = self.__servicio.calcular_costo(self.__duracion)
            return costo * (1 - descuento) * (1 + impuesto)
        except (ValueError, TypeError) as error:
            raise ReservaError("No se pudo calcular el total.") from error

    def confirmar(self):
        if self.__estado != "Pendiente":
            raise ReservaError(f"No se puede confirmar una reserva {self.__estado}.")
        self.__estado = "Confirmada"
        registrar_log(f"Reserva {self.__id} confirmada.")

    def cancelar(self):
        if self.__estado in ("Cancelada", "Procesada"):
            raise ReservaError(f"No se puede cancelar una reserva {self.__estado}.")
        self.__estado = "Cancelada"
        registrar_log(f"Reserva {self.__id} cancelada.")

    def procesar(self):
        # Tramita la reserva la cual debe estar confirmada, por ende devuelve el total
        try:
            if self.__estado != "Confirmada":
                raise ReservaError("La reserva debe estar confirmada.")
            total = self.calcular_total(impuesto=0.19)
        except ReservaError as error:
            registrar_log(f"Error al procesar la reserva {self.__id}: {error}")
            raise ReservaError("No se pudo procesar la reserva.") from error
        else:
            # Solo se ejecuta si no se han presentado errores
            self.__estado = "Procesada"
            registrar_log(f"Reserva {self.__id} procesada. Total: {total}")
            return total
        finally:
            # Esta se ejecuta siempre
            registrar_log(f"Fin del intento de procesar la reserva {self.__id}.")

    def __str__(self):
        return f"Reserva {self.__id} | {self.__cliente.nombre} | {self.__servicio.nombre} | {self.__duracion} h | {self.__estado}"


class GestorReservas:
    # Guarda las reservas en una lista

    def __init__(self):
        self.__reservas = []

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(len(self.__reservas) + 1, cliente, servicio, duracion)
        except ReservaError as error:
            registrar_log(f"No se creó la reserva: {error}")
            print(f"[ERROR] {error}")
            return None
        else:
            self.__reservas.append(reserva)
            registrar_log(f"Reserva {reserva.id} creada.")
            print(f"[OK] {reserva}")
            return reserva

    def buscar(self, id_reserva):
        for reserva in self.__reservas:
            if reserva.id == id_reserva:
                return reserva
        raise ReservaError(f"No existe la reserva {id_reserva}.")

    def confirmar_reserva(self, id_reserva):
        try:
            self.buscar(id_reserva).confirmar()
            print(f"[OK] Reserva {id_reserva} confirmada.")
        except ReservaError as error:
            registrar_log(f"Error al confirmar: {error}")
            print(f"[ERROR] {error}")

    def cancelar_reserva(self, id_reserva):
        try:
            self.buscar(id_reserva).cancelar()
            print(f"[OK] Reserva {id_reserva} cancelada.")
        except ReservaError as error:
            registrar_log(f"Error al cancelar: {error}")
            print(f"[ERROR] {error}")

    def procesar_reserva(self, id_reserva):
        try:
            total = self.buscar(id_reserva).procesar()
            print(f"[OK] Reserva {id_reserva} procesada. Total: {total:,.2f}")
        except ReservaError as error:
            registrar_log(f"Error al procesar: {error}")
            print(f"[ERROR] {error} (causa: {error.__cause__})")

    def listar(self):
        for reserva in self.__reservas:
            print(reserva)