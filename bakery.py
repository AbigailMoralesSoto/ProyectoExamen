from typing import List, Optional
from models import Producto, Cliente, Pedido

class Bakery:
    def __init__(self):
        self.products: List[Producto] = []
        self.customers: List[Cliente] = []
        self.orders: List[Pedido] = []

    # ----- Productos -----
    def add_product(self, nombre: str, descripcion: str, precio: float, stock: int) -> Producto:
        new_id = (max([p.producto_id for p in self.products]) + 1) if self.products else 1
        prod = Producto(producto_id=new_id, nombre=nombre.strip(), descripcion=descripcion.strip(), precio=float(precio), stock=int(stock))
        self.products.append(prod)
        return prod

    def find_product(self, producto_id: int) -> Optional[Producto]:
        return next((p for p in self.products if p.producto_id == producto_id), None)

    def delete_product(self, producto_id: int) -> None:
        p = self.find_product(producto_id)
        if not p:
            raise ValueError("Producto no encontrado")
        # eliminar pedidos asociados (opcional)
        self.orders = [o for o in self.orders if o.producto_id != producto_id]
        self.products = [x for x in self.products if x.producto_id != producto_id]

    # ----- Clientes -----
    def add_customer(self, nombre: str) -> Cliente:
        new_id = (max([c.cliente_id for c in self.customers]) + 1) if self.customers else 1
        c = Cliente(cliente_id=new_id, nombre=nombre.strip())
        self.customers.append(c)
        return c

    def find_customer(self, cliente_id: int) -> Optional[Cliente]:
        return next((c for c in self.customers if c.cliente_id == cliente_id), None)

    def delete_customer(self, cliente_id: int) -> None:
        c = self.find_customer(cliente_id)
        if not c:
            raise ValueError("Cliente no encontrado")
        # eliminar pedidos asociados (opcional)
        self.orders = [o for o in self.orders if o.cliente_id != cliente_id]
        self.customers = [x for x in self.customers if x.cliente_id != cliente_id]

    # ----- Pedidos -----
    def place_order(self, producto_id: int, cliente_id: int, cantidad: int) -> Pedido:
        prod = self.find_product(producto_id)
        cust = self.find_customer(cliente_id)
        if not prod:
            raise ValueError("Producto no encontrado")
        if not cust:
            raise ValueError("Cliente no encontrado")
        if prod.stock < cantidad:
            raise ValueError("Stock insuficiente")
        new_id = (max([o.pedido_id for o in self.orders]) + 1) if self.orders else 1
        pedido = Pedido(pedido_id=new_id, producto_id=producto_id, cliente_id=cliente_id, cantidad=int(cantidad))
        prod.stock -= int(cantidad)
        self.orders.append(pedido)
        return pedido

    def cancel_order(self, pedido_id: int) -> None:
        order = next((o for o in self.orders if o.pedido_id == pedido_id), None)
        if not order:
            raise ValueError("Pedido no encontrado")
        # devolver stock
        prod = self.find_product(order.producto_id)
        if prod:
            prod.stock += order.cantidad
        self.orders = [o for o in self.orders if o.pedido_id != pedido_id]

    def list_available_products(self):
        return [p for p in self.products if p.is_available()]

    # utilidades
    def seed_if_empty(self):
        if not self.products and not self.customers:
            self.add_product('Pastel de chocolate', 'Delicioso pastel de chocolate', 450.0, 5)
            self.add_product('Cupcake vainilla', 'Cupcake con frutas', 35.0, 20)
            self.add_product('Donas glaseadas', 'Paquete de 6 donitas', 90.0, 15)
            self.add_customer('Gabriel Martinez')
            self.add_customer('Jesus Bautista')
