import psycopg2
from psycopg2 import sql

class PedidoDAO:
    def __init__(self, conexao):
        self.con = conexao

    def inserir_pedido_inseguro(self, customer_name, employee_name, order_data, order_items):
        cursor = self.con.cursor()

        # SQL Injection: construindo a query com interpolação direta
        query = f"""
        INSERT INTO northwind.orders (customerid, employeeid, orderdate, requireddate, shipname)
        VALUES (
            (SELECT customerid FROM northwind.customers WHERE contactname = '{customer_name}'),
            (SELECT employeeid FROM northwind.employees WHERE firstname = '{employee_name}'),
            '{order_data["orderdate"]}',
            '{order_data["requireddate"]}',
            '{order_data["shipname"]}'
        ) RETURNING orderid;
        """

        cursor.execute(query)
        order_id = cursor.fetchone()[0]

        for item in order_items:
            query_item = f"""
            INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity, discount)
            VALUES (
                {order_id}, {item["productid"]}, {item["unitprice"]}, {item["quantity"]}, {item["discount"]}
            );
            """
            cursor.execute(query_item)

        self.con.commit()
        cursor.close()
        return order_id

    def inserir_pedido_seguro(self, customer_name, employee_name, order_data, order_items):
        cursor = self.con.cursor()

        # Busca segura de IDs
        cursor.execute(
            "SELECT customerid FROM northwind.customers WHERE contactname = %s", (customer_name,)
        )
        customer_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT employeeid FROM northwind.employees WHERE firstname = %s", (employee_name,)
        )
        employee_id = cursor.fetchone()[0]

        # Inserção segura do pedido
        cursor.execute(
            """
            INSERT INTO northwind.orders (customerid, employeeid, orderdate, requireddate, shipname)
            VALUES (%s, %s, %s, %s, %s) RETURNING orderid
            """,
            (customer_id, employee_id, order_data["orderdate"], order_data["requireddate"], order_data["shipname"])
        )
        order_id = cursor.fetchone()[0]

        for item in order_items:
            cursor.execute(
                """
                INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity, discount)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (order_id, item["productid"], item["unitprice"], item["quantity"], item["discount"])
            )

        self.con.commit()
        cursor.close()
        return order_id
