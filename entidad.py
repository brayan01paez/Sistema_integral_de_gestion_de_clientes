# Archivo: entidad.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: clase abstracta general del sistema
# Responsable: Brayan Paez

# Importa la clase ABC y el decorador abstractmethod del módulo abc para definir clases abstractas y métodos abstractos
from abc import ABC, abstractmethod

# Define la clase abstracta Entidad que hereda de ABC
class Entidad(ABC):
    
    # Define el método constructor de la clase Entidad que recibe un identificador como parámetro
    def __init__(self, identificador):
        
        # Asigna el valor del parámetro identificador al atributo de instancia self._indentificador
        self._identificador = identificador
    
    #propiedad de solo lectura para el atributo identificador
    @property
    def identificador(self):
        #Devuelve el valor sin permitir modificarlo desde fuera de la clase
        return self._identificador    
    
    # metodo abstracto : cada clase hija debe indicar como se describe
    @abstractmethod
    def describir(self):
        #sin contenido, ya que es un método abstracto que debe ser implementado por las subclases
        pass
    
    # metodo abstracto : cada clase hija debe indicar como se valida
    @abstractmethod
    def validar(self):
        # sin contenido, lo describe cada clase hija
        pass
    