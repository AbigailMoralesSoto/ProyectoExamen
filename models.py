from dataclasses import dataclass, field

@dataclass
class Producto:
    producto_id: int
    nombre: str
    descripcion: str
    precio: float
    stock: int

    def is_available(self) -> bool:
        return self.stock > 0

@dataclass
class Cliente:
    cliente_id: int
    nombre: str

@dataclass
class Pedido:
    pedido_id: int
    producto_id: int
    cliente_id: int
    cantidad: int
