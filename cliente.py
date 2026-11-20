
# Archivo: cliente.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: clase Cliente con validaciones y encapsulación de datos personales
# Responsable: Brayan Paez

from entidad import Entidad
from excepciones import ErrorValidacion


class Cliente(Entidad):

    def __init__(self, documento, nombre, correo, telefono):

        # Se guardan los datos del cliente
        if not isinstance(documento, str) or not documento.strip():
            raise ErrorValidacion("El documento no puede estar vacío.")

        super().__init__(documento.strip())

        self.__nombre = nombre.strip() if isinstance(nombre, str) else nombre
        self.__correo = correo.strip() if isinstance(correo, str) else correo
        self.__telefono = telefono.strip() if isinstance(telefono, str) else telefono

        # Se validan los datos al crear el cliente
        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        return (
            f"Cliente: {self.__nombre} - "
            f"Documento: {self.identificador} - "
            f"Correo: {self.__correo}"
        )

    def validar(self):

        if not isinstance(self.__nombre, str) or not self.__nombre:
            raise ErrorValidacion("El nombre del cliente no puede estar vacío.")

        if not isinstance(self.__correo, str) or not self.__correo:
            raise ErrorValidacion("El correo del cliente no puede estar vacío.")

        partes_correo = self.__correo.split("@")

        if (
            len(partes_correo) != 2
            or not partes_correo[0]
            or "." not in partes_correo[1]
            or " " in self.__correo
        ):
            raise ErrorValidacion("El correo electrónico no tiene un formato válido.")

        if not isinstance(self.__telefono, str):
            raise ErrorValidacion("El teléfono debe contener números.")

        telefono_limpio = self.__telefono.replace(" ", "").replace("-", "")

        if not telefono_limpio.isdigit() or not 7 <= len(telefono_limpio) <= 15:
            raise ErrorValidacion("El teléfono debe tener entre 7 y 15 números.")

        return True
