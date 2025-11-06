from flask import Flask, render_template, request, redirect, url_for, flash
from bakery import Bakery

app = Flask(__name__)
app.secret_key = 'dev-key'

bakery = Bakery()

@app.route('/')
def index():
    bakery.seed_if_empty()
    totals = {
        'products': len(bakery.products),
        'customers': len(bakery.customers),
        'available': len(bakery.list_available_products()),
        'orders': len(bakery.orders)
    }
    return render_template('index.html', totals=totals)

# ---- Productos ----
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    bakery.seed_if_empty()
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            precio = float(request.form.get('precio', '0'))
            stock = int(request.form.get('stock', '0'))
            if not nombre or precio <= 0:
                raise ValueError('Nombre y precio válidos son requeridos')
            bakery.add_product(nombre, descripcion, precio, stock)
            flash('Producto agregado', 'success')
            return redirect(url_for('productos'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('productos.html', products=bakery.products)

@app.route('/productos/delete/<int:producto_id>', methods=['POST'])
def delete_producto(producto_id):
    try:
        bakery.delete_product(producto_id)
        flash('Producto eliminado', 'success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('productos'))

# ---- Clientes ----
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    bakery.seed_if_empty()
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            if not nombre:
                raise ValueError('Nombre es requerido')
            bakery.add_customer(nombre)
            flash('Cliente agregado', 'success')
            return redirect(url_for('clientes'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('clientes.html', customers=bakery.customers)

@app.route('/clientes/delete/<int:cliente_id>', methods=['POST'])
def delete_cliente(cliente_id):
    try:
        bakery.delete_customer(cliente_id)
        flash('Cliente eliminado', 'success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('clientes'))

# ---- Pedidos ----
@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    bakery.seed_if_empty()
    if request.method == 'POST':
        try:
            producto_id = int(request.form.get('producto_id'))
            cliente_id = int(request.form.get('cliente_id'))
            cantidad = int(request.form.get('cantidad'))
            bakery.place_order(producto_id, cliente_id, cantidad)
            flash('Pedido registrado', 'success')
            return redirect(url_for('pedidos'))
        except Exception as e:
            flash(str(e), 'error')
    # preparar vista
    enriched_orders = []
    for o in bakery.orders:
        prod = bakery.find_product(o.producto_id)
        cust = bakery.find_customer(o.cliente_id)
        enriched_orders.append({'order': o, 'product': prod, 'customer': cust})
    return render_template('pedidos.html', orders=enriched_orders, products=bakery.products, customers=bakery.customers)

@app.route('/pedidos/cancel/<int:pedido_id>', methods=['POST'])
def cancel_pedido(pedido_id):
    try:
        bakery.cancel_order(pedido_id)
        flash('Pedido cancelado', 'success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('pedidos'))

if __name__ == '__main__':
    app.run(debug=True)
