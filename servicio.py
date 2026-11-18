# Archivo: servicio.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: Clase abstracta Servicio y los tres servicios especializados (Salas, Equipos, Asesorías)
# Responsable: Camilo Andres Zambrano 

from abc import ABC, abstractmethod

class Servicio(ABC):
    """
    Clase abstracta que representa una entidad general de tipo Servicio.
    Define la estructura base, atributos comunes y métodos abstractos que 
    las clases hijas (servicios especializados) están obligadas a implementar.
    """
    
    def __init__(self, codigo: str, nombre: str, costo_base: float):
        """
        Constructor de la clase abstracta Servicio.
        :param codigo: Código único identificador del servicio.
        :param nombre: Nombre descriptivo del servicio.
        :param costo_base: Costo base inicial del servicio.
        """
        self._codigo = codigo
        self._nombre = nombre
        self._costo_base = costo_base

    @property
    def codigo(self) -> str:
        """Método getter para obtener el código del servicio."""
        return self._codigo

    @property
    def nombre(self) -> str:
        """Método getter para obtener el nombre del servicio."""
        return self._nombre

    @property
    def costo_base(self) -> float:
        """Método getter para obtener el costo base."""
        return self._costo_base

    @costo_base.setter
    def costo_base(self, nuevo_costo: float):
        """Método setter para actualizar el costo base con validación de seguridad."""
        if nuevo_costo < 0:
            raise ValueError("El costo base no puede ser negativo.")
        self._costo_base = nuevo_costo

    @abstractmethod
    def calcular_costo(self) -> float:
        """Método abstractor para calcular el costo total del servicio."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método abstractor para retornar la descripción detallada del servicio."""
        pass


class ReservaSalas(Servicio):
    """Servicio especializado 1: Gestión y alquiler de salas."""
    
    def __init__(self, codigo: str, nombre: str, costo_base: float, capacidad_personas: int, horas: int):
        super().__init__(codigo, nombre, costo_base)
        self.capacidad_personas = capacidad_personas
        self.horas = horas

    def calcular_costo(self) -> float:
        """Calcula el costo multiplicando las horas por el costo base, aplicando recargo por capacidad si supera 10 personas."""
        costo_total = self._costo_base * self.horas
        if self.capacidad_personas > 10:
            costo_total *= 1.15  # Recargo del 15% por salas grandes
        return costo_total

    def calcular_costo(self, descuento: float = 0.0) -> float:
        """Sobrecarga de método: Permite calcular el costo aplicando un descuento opcional."""
        base = self.calcular_costo() if descuento == 0.0 else (self._costo_base * self.horas)
        return max(0.0, base * (1 - descuento))

    def describir_servicio(self) -> str:
        return f"[Sala] Código: {self._codigo} | Nombre: {self._nombre} | Capacidad: {self.capacidad_personas} personas | Horas: {self.horas}"


class AlquilerEquipos(Servicio):
    """Servicio especializado 2: Alquiler de equipos tecnológicos o de oficina."""
    
    def __init__(self, codigo: str, nombre: str, costo_base: float, cantidad_equipos: int, dias: int):
        super().__init__(codigo, nombre, costo_base)
        self.cantidad_equipos = cantidad_equipos
        self.dias = dias

    def calcular_costo(self) -> float:
        """Calcula el costo del alquiler de equipos por día y cantidad."""
        return self._costo_base * self.cantidad_equipos * self.dias

    def calcular_costo(self, aplicar_seguro: bool = False) -> float:
        """Sobrecarga de método: Permite añadir un costo fijo de seguro para los equipos."""
        total = self._costo_base * self.cantidad_equipos * self.dias
        if aplicar_seguro:
            total += 20000 * self.cantidad_equipos  # Seguro adicional por equipo
        return total

    def describir_servicio(self) -> str:
        return f"[Equipo] Código: {self._codigo} | Nombre: {self._nombre} | Cantidad: {self.cantidad_equipos} | Días: {self.dias}"


class AsesoriasEspecializadas(Servicio):
    """Servicio especializado 3: Asesorías profesionales personalizadas."""
    
    def __init__(self, codigo: str, nombre: str, costo_base: float, nivel_experticia: str, sesiones: int):
        super().__init__(codigo, nombre, costo_base)
        self.nivel_experticia = nivel_experticia  # Ej: 'Junior', 'Senior', 'Master'
        self.sesiones = sesiones

    def calcular_costo(self) -> float:
        """Calcula el costo de las asesorías basándose en el nivel de experticia del asesor."""
        multiplicador = 1.0
        if self.nivel_experticia.lower() == 'senior':
            multiplicador = 1.3
        elif self.nivel_experticia.lower() == 'master':
            multiplicador = 1.6
            
        return self._costo_base * self.sesiones * multiplicador

    def describir_servicio(self) -> str:
        return f"[Asesoría] Código: {self._codigo} | Nombre: {self._nombre} | Nivel: {self.nivel_experticia} | Sesiones: {self.sesiones}"
