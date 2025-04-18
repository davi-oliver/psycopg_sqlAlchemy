 
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
    return render_template('base.html')

@app.route('/relatorios/pedido', methods=['GET', 'POST'])
def relatorio_pedido():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        conn = get_db_connection()
        try:
            # Obter informações do pedido
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.orderid, o.orderdate, c.contactname, 
                       CONCAT(e.firstname, ' ', e.lastname) as employeename
                FROM northwind.orders o
                JOIN northwind.customers c ON o.customerid = c.customerid
                JOIN northwind.employees e ON o.employeeid = e.employeeid
                WHERE o.orderid = %s
            """, (order_id,))
            pedido = cursor.fetchone()

            # Obter itens do pedido
            cursor.execute("""
                SELECT p.productname, od.quantity, od.unitprice
                FROM northwind.order_details od
                JOIN northwind.products p ON od.productid = p.productid
                WHERE od.orderid = %s
            """, (order_id,))
            itens = cursor.fetchall()

            return render_template('relatorios/pedido_resultado.html',
                                pedido=pedido,
                                itens=itens)
        except Exception as e:
            return render_template('relatorios/erro.html',
                                message=f"Erro ao gerar relatório: {str(e)}")
        finally:
            conn.close()
    
    return render_template('relatorios/pedido_form.html')


@app.route('/relatorios/ranking', methods=['GET', 'POST'])
def ranking_funcionarios():
    if request.method == 'POST':
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    CONCAT(e.firstname, ' ', e.lastname) as employeename,
                    COUNT(o.orderid) as total_pedidos,
                    SUM(od.unitprice * od.quantity * (1 - od.discount)) as total_vendido
                FROM northwind.employees e
                JOIN northwind.orders o ON e.employeeid = o.employeeid
                JOIN northwind.order_details od ON o.orderid = od.orderid
                WHERE o.orderdate BETWEEN %s AND %s
                GROUP BY e.employeeid, employeename
                ORDER BY total_vendido DESC
            """, (data_inicio, data_fim))
            
            ranking = cursor.fetchall()
            
            return render_template('relatorios/ranking_resultado.html',
                                ranking=ranking,
                                data_inicio=data_inicio,
                                data_fim=data_fim)
        except Exception as e:
            return render_template('relatorios/erro.html',
                                message=f"Erro ao gerar ranking: {str(e)}")
        finally:
            conn.close()
    
    return render_template('relatorios/ranking_form.html')

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