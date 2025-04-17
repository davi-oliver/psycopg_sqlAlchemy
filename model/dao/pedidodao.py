import psycopg2
from psycopg2 import sql

class PedidoDAO:
    def __init__(self, conexao):
        self.con = conexao
    
    # Versão INSEGURA (para demonstração)
    def inserir_pedido_inseguro(self, customer_name, employee_name, order_data, order_items):
        cursor = self.con.cursor()
        cursor.execute("SELECT MAX(orderid) + 1 FROM northwind.orders")
        order_id = cursor.fetchone()[0]
        query = f"""
        INSERT INTO northwind.orders (orderid, customerid, employeeid, orderdate, requireddate, shipname)
        VALUES (
            {order_id},
            (SELECT customerid FROM northwind.customers WHERE contactname = '{customer_name}'),
            (SELECT employeeid FROM northwind.employees WHERE firstname = '{employee_name}'),
            '{order_data['orderdate']}',
            '{order_data['requireddate']}',
            '{order_data['shipname']}'
        ) RETURNING orderid;
        """
        
        cursor.execute(query)
        order_id = cursor.fetchone()[0]
        print(f"Pedido inserido com ID: {order_id}")
        for item in order_items:
            query_item = f"""
            INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity, discount)
            VALUES (
                {order_id}, {item['productid']}, {item['unitprice']}, {item['quantity']}, {item['discount']}
            );
            """
            cursor.execute(query_item)
        
        self.con.commit()
        cursor.close()
        return order_id

    # Versão SEGURA
    def inserir_pedido_seguro(self, customer_name, employee_name, order_data, order_items):
        cursor = self.con.cursor()
        
        try:
            # Obter IDs de forma segura
            cursor.execute(
                "SELECT customerid FROM northwind.customers WHERE contactname = %s",
                (customer_name,)
            )
            customer_id = cursor.fetchone()[0]
            print(f"ID do cliente: {customer_id}")
            
            cursor.execute(
                "SELECT employeeid FROM northwind.employees WHERE firstname = %s",
                (employee_name,)
            )
            employee_id = cursor.fetchone()[0]
            print(f"ID do cliente: {customer_id}, ID do funcionário: {employee_id}")
            
            cursor.execute("SELECT MAX(orderid) + 1 FROM northwind.orders")
            order_id = cursor.fetchone()[0]
            # Inserir pedido
            cursor.execute(
                """
                INSERT INTO northwind.orders 
                    (orderid, customerid, employeeid, orderdate, requireddate, shipname)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING orderid
                """,
                (order_id, customer_id, employee_id, 
                 order_data['orderdate'], 
                 order_data['requireddate'], 
                 order_data['shipname'])
            )
            order_id_aux = cursor.fetchone()[0]
            print(f"Pedido inserido com ID: {order_id_aux}")
            
            # Inserir itens
            for item in order_items:
                cursor.execute(
                    """
                    INSERT INTO northwind.order_details
                        (orderid, productid, unitprice, quantity, discount)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (order_id_aux, item['productid'], item['unitprice'], 
                     item['quantity'], item['discount'])
                )
            
            self.con.commit()
            return order_id
            
        except Exception as e:
            print(f"Erro ao inserir pedido: {e}")
            self.con.rollback()
            raise e
        finally:
            cursor.close()