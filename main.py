from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from controller.pedido_controller import PedidoController
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='templates')

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

@app.route('/pedidos/novo', methods=['GET', 'POST'])
def novo_pedido():
    if request.method == 'POST':
        seguro = request.form.get('modo_seguro') == 'on'
        conn = get_db_connection()
        print(f"Conexão com o banco de dados estabelecida: {conn}")
        controller = PedidoController(conn)
        
        success, message, order_id = controller.criar_pedido(request.form, seguro)
        conn.close()
        
        return render_template('pedidos/resultado.html', 
                            success=success, 
                            message=message,
                            order_id=order_id)
    
    # GET: Mostrar formulário
    return render_template('pedidos/form.html')

if __name__ == '__main__':
    app.run(debug=True)