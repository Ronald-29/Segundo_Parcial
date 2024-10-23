from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Ruta para la página principal
@app.route('/')
def index():
    if 'productos' not in session:
        session['productos'] = []
    return render_template('index.html', productos=session['productos'])

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        # Obtener los datos del formulario
        id_producto = len(session['productos']) + 1
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']
        
        # Crear el diccionario del producto
        producto = {
            'id': id_producto,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }
        
        # Agregar el producto a la sesión
        productos = session['productos']
        productos.append(producto)
        session['productos'] = productos
        
        return redirect(url_for('index'))

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    productos = session['productos']
    session['productos'] = [producto for producto in productos if producto['id'] != id]
    return redirect(url_for('index'))

# Ruta para editar un producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session['productos']
    producto = next((p for p in productos if p['id'] == id), None)
    
    if request.method == 'POST':
        # Actualizar los datos del producto
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = request.form['cantidad']
        producto['precio'] = request.form['precio']
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
