import psycopg2
from psycopg2 import sql
from typing import Dict, List, Optional, Tuple

class PedidoDAO:
    def __init__(self, conexao):
        self.con = conexao
        

    def inserir_pedido(self, form_data: dict) -> int:
        cursor = self.con.cursor()
        try:
            cursor.execute("SELECT MAX(orderid) FROM northwind.orders")
            max_orderid = cursor.fetchone()[0]
            orderid = (max_orderid or 0) + 1  # Incrementar o maior valor encontrado

            # Inserir pedido principal
            query = sql.SQL("""
                INSERT INTO northwind.orders (
                    orderid, customerid, employeeid, orderdate, requireddate,
                    shippeddate, freight, shipname, shipaddress,
                    shipcity, shipregion, shippostalcode, shipcountry, shipperid
                ) VALUES (
                   %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                ) RETURNING orderid
            """)
            
            shipped_date = form_data.get('shippeddate')
            freight = form_data.get('freight')
            shipper_id = form_data.get('shipperid')
            
            params = (
                orderid,
                form_data['customerid'],
                form_data['employeeid'],
                form_data['orderdate'],
                form_data['requireddate'],
                shipped_date,
                float(freight) if freight else None,
                form_data['shipname'],
                form_data['shipaddress'], 

                form_data['shipcity'],
                form_data.get('shipregion'),
                form_data['shippostalcode'],
                form_data['shipcountry'],
                int(shipper_id) if shipper_id else None
            )
            print("Params: >>>> ", params)
            
            cursor.execute(query, params)
            order_id = cursor.fetchone()[0]
            
            # Inserir itens do pedido
            i = 0
            while f'item_{i}_productid' in form_data:
                item_query = sql.SQL("""
                    INSERT INTO northwind.order_details (
                        orderid, productid, unitprice, quantity, discount
                    ) VALUES (%s, %s, %s, %s, %s)
                """)
                
                item_params = (
                    order_id,
                    int(form_data[f'item_{i}_productid']),
                    float(form_data[f'item_{i}_unitprice']),
                    int(form_data[f'item_{i}_quantity']),
                    float(form_data.get(f'item_{i}_discount', 0.0))
                )
                
                cursor.execute(item_query, item_params)
                i += 1
            
            self.con.commit()
            return order_id
            
        except Exception as e:
            self.con.rollback()
            raise e
        finally:
            cursor.close()

    def get_all_clientes(self) -> List[tuple]:
        cursor = self.con.cursor()
        try:
            cursor.execute("""
                SELECT customerid, contactname 
                FROM northwind.customers 
                ORDER BY contactname
            """)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_vendedores(self) -> List[tuple]:
        cursor = self.con.cursor()
        try:
            cursor.execute("""
                SELECT employeeid, CONCAT(firstname, ' ', lastname) AS nome_completo 
                FROM northwind.employees 
                ORDER BY firstname
            """)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_produtos(self) -> List[tuple]:
        cursor = self.con.cursor()
        try:
            cursor.execute("""
                SELECT productid, productname, unitprice 
                FROM northwind.products 
                
                ORDER BY productname
            """)
            # print("Produtos: >>>> ", cursor.fetchall()) 
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_shippers(self) -> List[tuple]:
        cursor = self.con.cursor()
        try:
            cursor.execute("""
                SELECT shipperid, companyname 
                FROM northwind.shippers 
                ORDER BY companyname
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            
     