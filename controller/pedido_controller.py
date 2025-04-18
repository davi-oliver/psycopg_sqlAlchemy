from typing import Tuple, Optional, List
from model.dao.pedidodao import PedidoDAO
from controller.orm_controller import ORMPedidoController
from config.database import get_db as get_sqlalchemy_db

class PedidoController:
    def __init__(self, conexao=None, usar_orm=False):
        self.usar_orm = usar_orm
        if usar_orm:
            self.orm_controller = ORMPedidoController(next(get_sqlalchemy_db()))
        else:
            self.dao = PedidoDAO(conexao)
    
    def criar_pedido(self, form_data: dict) -> Tuple[bool, str, Optional[int]]:
        try:
            if self.usar_orm:
                return self.orm_controller.criar_pedido(form_data)
            else:
                order_id = self.dao.inserir_pedido(form_data)
                return True, f"Pedido {order_id} criado com sucesso via Psycopg2", order_id
        except Exception as e:
            return False, f"Erro ao criar pedido: {str(e)}", None
    
    def get_all_clientes(self) -> List[tuple]:
        if self.usar_orm:
            return self.orm_controller.get_all_clientes()
        return self.dao.get_all_clientes()
    
    def get_all_vendedores(self) -> List[tuple]:
        if self.usar_orm:
            return self.orm_controller.get_all_vendedores()
        return self.dao.get_all_vendedores()
    
    def get_all_produtos(self) -> List[tuple]:
        if self.usar_orm:
            return self.orm_controller.get_all_produtos()
        prod = self.dao.get_all_produtos()
        print(f"Produtos encontrados>>> ({len(prod)}): {prod[:3]}...")
        return  prod
    
    def get_all_shippers(self) -> List[tuple]:
        if self.usar_orm:
            return self.orm_controller.get_all_shippers()
        return self.dao.get_all_shippers()
    def gerar_relatorio_pedido(self, order_id):
        if self.usar_orm:
            # Implementação com SQLAlchemy
            pedido = self.session.query(...)  # Implemente conforme seu modelo
            itens = self.session.query(...)   # Implemente conforme seu modelo
            return pedido, itens
        else:
            # Implementação com psycopg2
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT o.orderid, o.orderdate, c.contactname, 
                    CONCAT(e.firstname, ' ', e.lastname) as employeename
                FROM northwind.orders o
                JOIN northwind.customers c ON o.customerid = c.customerid
                JOIN northwind.employees e ON o.employeeid = e.employeeid
                WHERE o.orderid = %s
            """, (order_id,))
            pedido = cursor.fetchone()

            cursor.execute("""
                SELECT p.productname, od.quantity, od.unitprice
                FROM northwind.order_details od
                JOIN northwind.products p ON od.productid = p.productid
                WHERE od.orderid = %s
            """, (order_id,))
            itens = cursor.fetchall()
            return pedido, itens

    def gerar_ranking_funcionarios(self, data_inicio, data_fim):
        if self.usar_orm:
            # Implementação com SQLAlchemy
            ranking = self.session.query(...)  # Implemente conforme seu modelo
            return ranking
        else:
            # Implementação com psycopg2
            cursor = self.conn.cursor()
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
            return cursor.fetchall()