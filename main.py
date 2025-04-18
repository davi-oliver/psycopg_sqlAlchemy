 
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from config.database import Base, engine, get_db
from controller.pedido_controller import PedidoController
from dotenv import load_dotenv
import os

from model.dao.pedidodao import PedidoDAO

# Carregar variáveis de ambiente
load_dotenv()

# Criar tabelas se não existirem
Base.metadata.create_all(bind=engine)

app = Flask(__name__, template_folder='templates')

# Função para conexão direta com Psycopg2
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

@app.route('/')
def index():
    return redirect(url_for('novo_pedido'))

@app.route('/pedidos/novo', methods=['GET', 'POST'])
def novo_pedido():
    usar_orm = request.method == 'POST' and request.form.get('usar_orm') == 'on' or \
               request.method == 'GET' and request.args.get('orm') == 'true'
    
    if request.method == 'POST':
        try:
            if usar_orm:
                controller = PedidoController(usar_orm=True)
            else:
                conn = get_db_connection()
                controller = PedidoController(conn)
            
            success, message, order_id = controller.criar_pedido(request.form)
            
            if not usar_orm:
                conn.close()
            
            return render_template('pedidos/resultado.html', 
                                success=success, 
                                message=message,
                                order_id=order_id)
        
        except Exception as e:
            return render_template('pedidos/resultado.html',
                                success=False,
                                message=f"Erro grave: {str(e)}",
                                order_id=None)
    
    # GET: Mostrar formulário
    try:
        if usar_orm:
            controller = PedidoController(usar_orm=True)
        else:
            conn = get_db_connection()
            controller = PedidoController(conn)
        print('usar >>>>>> orm:', usar_orm)
        
      
        clientes = controller.get_all_clientes()
        vendedores = controller.get_all_vendedores()
        produtos = controller.get_all_produtos()
        shippers = controller.get_all_shippers()
        
        print(f"Produtos encontrados ({len(produtos)}): {produtos[:3]}...")  # Debug parcial
        
        context = {
            'clientes': clientes,
            'vendedores': vendedores,
            'produtos': produtos,
            'shippers': shippers,
            'usar_orm': usar_orm
        }
        

        if not usar_orm:
            conn.close()
        
        return render_template('pedidos/form.html', **context)
    
    except Exception as e:
        return render_template('pedidos/erro.html',
                            message=f"Erro ao carregar formulário: {str(e)}")
    
     
 

 
 

if __name__ == '__main__':
    app.run(debug=True)
    # demonstrar_injecao_sql()