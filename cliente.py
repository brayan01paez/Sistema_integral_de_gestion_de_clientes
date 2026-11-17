# Archivo: cliente.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: clase Cliente con validaciones y encapsulación de datos personales
# Responsable: Brayan Paez

# Importa la clase abstracta Entidad, de la que hereda la clase Cliente
from entidad import Entidad

# Clase Cliente: representa a un cliente de Software FJ y hereda de Entidad
class Cliente(Entidad):
    
    # Constructor: recibe los datos personales del cliente
    def __init__(self, documento, nombre, correo, telefono):
        # Llama al constructor de Entidad y usa el documento como identificador
        super().__init__(documento)
        # Atributo privado que guarda el nombre del cliente
        self.__nombre = nombre
        # Atributo privado que guarda el correo del cliente
        self.__correo = correo
        # Atributo privado que guarda el teléfono del cliente
        self.__telefono = telefono
    
    # Propiedad de solo lectura para consultar el nombre    
    @property
    def nombre(self):
        # Devuelve el nombre sin permitir modificarlo desde afuera
        return self.__nombre
    
    # Propiedad de solo lectura para consultar el correo
    @property
    def correo(self):
        # Devuelve el correo sin permitir modificarlo desde afuera
        return self.__correo
    
    # Propiedad de solo lectura para consultar el teléfono
    @property
    def telefono(self):
        # Devuelve el teléfono sin permitir modificarlo desde afuera
        return self.__telefono
    
    # Implementa el método abstracto describir heredado de Entidad
    def describir(self):
         # Devuelve un texto con los datos principales del cliente
        return f"Cliente: {self.__nombre} - Documento: {self.identificador} - Correo: {self.__correo}"
    
    # Implementa el método abstracto validar heredado de Entidad
    def validar(self):
        # Devuelve True por ahora
        return True
         