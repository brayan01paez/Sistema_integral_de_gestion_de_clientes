
# Archivo: reserva.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: clase Reserva y gestión de reservas
# Responsable: Esneyder

import math

# Importamos las excepciones y las funciones para guardar eventos y errores
from excepciones import ErrorSistema, ErrorValidacion, ErrorNoEncontrado, ErrorOperacion
from registro_logs import registrar_evento, registrar_error

# Importamos los tres tipos de servicios
from servicio import ReservaSalas, AlquilerEquipos, AsesoriasEspecializadas


class Reserva:

    def __init__(self, id_reserva, cliente, servicio, duracion):
        if cliente is None or servicio is None:
            raise ErrorValidacion("La reserva necesita un cliente y un servicio.")

        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise ErrorValidacion("La duración debe ser un número entero mayor que cero.")

        if not getattr(servicio, "disponible", True):
            raise ErrorOperacion(f"El servicio '{servicio.nombre}' no está disponible.")

        if not isinstance(servicio, (ReservaSalas, AlquilerEquipos, AsesoriasEspecializadas)):
            raise ErrorValidacion("El tipo de servicio no está reconocido por el sistema.")

        # Atributos de la reserva
        self.__id = id_reserva
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

    # Permite consultar el ID de la reserva
    @property
    def id(self):
        return self.__id

    # Permite consultar el estado de la reserva
    @property
    def estado(self):
        return self.__estado

    # Calcula el costo total teniendo en cuenta la duración, el descuento y el impuesto
    def calcular_total(self, impuesto=0, descuento=0):

        # Validación del impuesto
        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise ErrorValidacion("El impuesto debe ser un número.")

        if not math.isfinite(impuesto) or impuesto < 0 or impuesto > 1:
            raise ErrorValidacion("El impuesto debe estar entre 0 y 1.")

        # Validación del descuento
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise ErrorValidacion("El descuento debe ser un número.")

        if not math.isfinite(descuento) or descuento < 0 or descuento > 1:
            raise ErrorValidacion("El descuento debe estar entre 0 y 1.")

        try:
            # Se utiliza la duración de la reserva según el tipo de servicio
            if isinstance(self.__servicio, ReservaSalas):
                costo = self.__servicio.calcular_costo(horas=self.__duracion)

            elif isinstance(self.__servicio, AlquilerEquipos):
                costo = self.__servicio.calcular_costo(dias=self.__duracion)

            elif isinstance(self.__servicio, AsesoriasEspecializadas):
                costo = self.__servicio.calcular_costo(sesiones=self.__duracion)

            else:
                raise ErrorValidacion("No se puede calcular el costo de este servicio.")

            # Se aplica el descuento y después el impuesto
            total = costo * (1 - descuento) * (1 + impuesto)
            return round(total, 2)

        except ErrorSistema:
            raise

        except Exception as error:
            raise ErrorOperacion("No se pudo calcular el total de la reserva.") from error

    # Confirma la reserva únicamente si está pendiente
    def confirmar(self):
        if self.__estado != "Pendiente":
            raise ErrorOperacion(f"No se puede confirmar una reserva {self.__estado}.")

        self.__estado = "Confirmada"
        registrar_evento(f"Reserva {self.__id} confirmada.")

    # Cancela la reserva si todavía no ha sido procesada o cancelada
    def cancelar(self):
        if self.__estado in ("Cancelada", "Procesada"):
            raise ErrorOperacion(f"No se puede cancelar una reserva {self.__estado}.")

        self.__estado = "Cancelada"
        registrar_evento(f"Reserva {self.__id} cancelada.")

    # Procesa la reserva y devuelve el total a pagar
    def procesar(self):
        try:
            # Solo se procesa una reserva confirmada
            if self.__estado != "Confirmada":
                raise ErrorOperacion("La reserva debe estar confirmada.")

            total = self.calcular_total(impuesto=0.19)

        except ErrorSistema as error:
            registrar_error(f"Error al procesar la reserva {self.__id}: {error}")
            raise ErrorOperacion("No se pudo procesar la reserva.") from error

        else:
            self.__estado = "Procesada"
            registrar_evento(f"Reserva {self.__id} procesada. Total: {total}")
            return total

        finally:
            # Este registro se ejecuta haya o no haya ocurrido un error
            registrar_evento(f"Fin del intento de procesar la reserva {self.__id}.")

    # Muestra los datos principales de la reserva
    def __str__(self):
        if isinstance(self.__servicio, ReservaSalas):
            unidad = "horas"
        elif isinstance(self.__servicio, AlquilerEquipos):
            unidad = "días"
        else:
            unidad = "sesiones"

        return (
            f"Reserva {self.__id} | {self.__cliente.nombre} | "
            f"{self.__servicio.nombre} | {self.__duracion} {unidad} | "
            f"{self.__estado}"
        )


# Esta clase guarda y administra las reservas en una lista
class GestorReservas:

    def __init__(self):
        self.__reservas = []

    # Crea una reserva y la guarda si los datos son correctos
    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(len(self.__reservas) + 1, cliente, servicio, duracion)

        except ErrorSistema as error:
            registrar_error(f"No se creó la reserva: {error}")
            print(f"[ERROR] {error}")
            return None

        else:
            self.__reservas.append(reserva)
            registrar_evento(f"Reserva {reserva.id} creada.")
            print(f"[OK] {reserva}")
            return reserva

    # Busca una reserva por su ID
    def buscar(self, id_reserva):
        for reserva in self.__reservas:
            if reserva.id == id_reserva:
                return reserva

        raise ErrorNoEncontrado(f"No existe la reserva {id_reserva}.")

    # Confirma una reserva por su ID
    def confirmar_reserva(self, id_reserva):
        try:
            self.buscar(id_reserva).confirmar()
            print(f"[OK] Reserva {id_reserva} confirmada.")

        except ErrorSistema as error:
            registrar_error(f"Error al confirmar: {error}")
            print(f"[ERROR] {error}")

    # Cancela una reserva por su ID
    def cancelar_reserva(self, id_reserva):
        try:
            self.buscar(id_reserva).cancelar()
            print(f"[OK] Reserva {id_reserva} cancelada.")

        except ErrorSistema as error:
            registrar_error(f"Error al cancelar: {error}")
            print(f"[ERROR] {error}")

    # Procesa una reserva por su ID y muestra el total
    def procesar_reserva(self, id_reserva):
        try:
            total = self.buscar(id_reserva).procesar()
            print(f"[OK] Reserva {id_reserva} procesada. Total: {total:,.2f}")

        except ErrorSistema as error:
            registrar_error(f"Error al procesar: {error}")
            print(f"[ERROR] {error} (causa: {error.__cause__})")

    # Muestra todas las reservas guardadas
    def listar(self):
        if not self.__reservas:
            print("No hay reservas registradas.")
            return

        for reserva in self.__reservas:
            print(reserva)
