# Archivo: servicio.py
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Contenido: Clase abstracta Servicio y los tres servicios especializados (Salas, Equipos, Asesorías)
# Responsable: Camilo Zambrano

from abc import ABC, abstractmethod


class Servicio(ABC):
    """
    Clase abstracta que representa una entidad general de tipo Servicio.
    Define atributos comunes, disponibilidad y el contrato que deben cumplir las subclases.
    """

    def __init__(self, codigo: str, nombre: str, costo_base: float, disponible: bool = True):
        if not codigo or not codigo.strip():
            raise ValueError("El código del servicio no puede estar vacío.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del servicio no puede estar vacío.")
        if costo_base < 0:
            raise ValueError("El costo base no puede ser negativo.")

        self._codigo = codigo.strip()
        self._nombre = nombre.strip()
        self._costo_base = float(costo_base)
        self._disponible = bool(disponible)

    @property
    def codigo(self) -> str:
        """Retorna el código identificador del servicio."""
        return self._codigo

    @property
    def nombre(self) -> str:
        """Retorna el nombre del servicio."""
        return self._nombre

    @property
    def costo_base(self) -> float:
        """Retorna el costo base del servicio."""
        return self._costo_base

    @costo_base.setter
    def costo_base(self, nuevo_costo: float) -> None:
        """Actualiza el costo base validando que no sea negativo."""
        if nuevo_costo < 0:
            raise ValueError("El costo base no puede ser negativo.")
        self._costo_base = float(nuevo_costo)

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para ser reservado."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Actualiza la disponibilidad del servicio."""
        self._disponible = bool(estado)

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Calcula el costo total del servicio según sus parámetros o ajustes opcionales."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna una descripción legible del servicio."""
        pass


class ReservaSalas(Servicio):
    """Servicio especializado 1: Reserva y alquiler de salas."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        costo_base: float,
        capacidad_personas: int,
        horas: int,
        disponible: bool = True,
    ):
        super().__init__(codigo, nombre, costo_base, disponible=disponible)
        if capacidad_personas <= 0:
            raise ValueError("La capacidad de personas debe ser mayor a 0.")
        if horas <= 0:
            raise ValueError("La cantidad de horas debe ser mayor a 0.")
        self.capacidad_personas = int(capacidad_personas)
        self.horas = int(horas)

    def calcular_costo(self, descuento: float = 0.0, horas: int | None = None) -> float:
        """
        Calcula el costo de la sala.
        - Aplica recargo del 15% si la capacidad supera 10 personas.
        - Permite sobrescribir horas y aplicar un descuento opcional (entre 0.0 y 1.0).
        """
        if not (0.0 <= descuento <= 1.0):
            raise ValueError("El descuento debe estar entre 0.0 y 1.0.")

        cantidad_horas = self.horas if horas is None else int(horas)
        if cantidad_horas <= 0:
            raise ValueError("Las horas deben ser mayores a 0.")

        subtotal = self._costo_base * cantidad_horas
        if self.capacidad_personas > 10:
            subtotal *= 1.15

        total = subtotal * (1.0 - descuento)
        return round(max(0.0, total), 2)

    def describir_servicio(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Sala] Código: {self._codigo} | Nombre: {self._nombre} | "
            f"Capacidad: {self.capacidad_personas} personas | Horas: {self.horas} | "
            f"Costo base: {self._costo_base} | Estado: {estado}"
        )


class AlquilerEquipos(Servicio):
    """Servicio especializado 2: Alquiler de equipos."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        costo_base: float,
        cantidad_equipos: int,
        dias: int,
        disponible: bool = True,
    ):
        super().__init__(codigo, nombre, costo_base, disponible=disponible)
        if cantidad_equipos <= 0:
            raise ValueError("La cantidad de equipos debe ser mayor a 0.")
        if dias <= 0:
            raise ValueError("La cantidad de días debe ser mayor a 0.")
        self.cantidad_equipos = int(cantidad_equipos)
        self.dias = int(dias)

    def calcular_costo(
        self,
        aplicar_seguro: bool = False,
        costo_seguro_por_equipo: float = 20000.0,
        dias: int | None = None,
    ) -> float:
        """
        Calcula el costo del alquiler de equipos por cantidad y días.
        Permite añadir seguro opcional por equipo y ajustar días si se requiere.
        """
        cantidad_dias = self.dias if dias is None else int(dias)
        if cantidad_dias <= 0:
            raise ValueError("Los días deben ser mayores a 0.")
        if costo_seguro_por_equipo < 0:
            raise ValueError("El costo del seguro no puede ser negativo.")

        total = self._costo_base * self.cantidad_equipos * cantidad_dias
        if aplicar_seguro:
            total += costo_seguro_por_equipo * self.cantidad_equipos

        return round(max(0.0, total), 2)

    def describir_servicio(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Equipo] Código: {self._codigo} | Nombre: {self._nombre} | "
            f"Cantidad: {self.cantidad_equipos} | Días: {self.dias} | "
            f"Costo base: {self._costo_base} | Estado: {estado}"
        )


class AsesoriasEspecializadas(Servicio):
    """Servicio especializado 3: Asesorías especializadas."""

    MULTIPLICADORES = {
        "junior": 1.0,
        "senior": 1.3,
        "master": 1.6,
    }

    def __init__(
        self,
        codigo: str,
        nombre: str,
        costo_base: float,
        nivel_experticia: str,
        sesiones: int,
        disponible: bool = True,
    ):
        super().__init__(codigo, nombre, costo_base, disponible=disponible)
        nivel_limpio = (nivel_experticia or "").strip().lower()
        if nivel_limpio not in self.MULTIPLICADORES:
            raise ValueError("Nivel de experticia inválido. Use: Junior, Senior o Master.")
        if sesiones <= 0:
            raise ValueError("La cantidad de sesiones debe ser mayor a 0.")

        self.nivel_experticia = nivel_limpio.capitalize()
        self.sesiones = int(sesiones)

    def calcular_costo(self, descuento: float = 0.0, sesiones: int | None = None) -> float:
        """
        Calcula el costo de la asesoría según el nivel de experticia y número de sesiones,
        con descuento opcional entre 0.0 y 1.0.
        """
        if not (0.0 <= descuento <= 1.0):
            raise ValueError("El descuento debe estar entre 0.0 y 1.0.")

        cantidad_sesiones = self.sesiones if sesiones is None else int(sesiones)
        if cantidad_sesiones <= 0:
            raise ValueError("Las sesiones deben ser mayores a 0.")

        multiplicador = self.MULTIPLICADORES[self.nivel_experticia.lower()]
        total = self._costo_base * cantidad_sesiones * multiplicador * (1.0 - descuento)
        return round(max(0.0, total), 2)

    def describir_servicio(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Asesoría] Código: {self._codigo} | Nombre: {self._nombre} | "
            f"Nivel: {self.nivel_experticia} | Sesiones: {self.sesiones} | "
            f"Costo base: {self._costo_base} | Estado: {estado}"
        )
