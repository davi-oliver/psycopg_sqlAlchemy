from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Optional
from model.model import Orders, OrderDetails, Shippers

class ORMPedidoDAO:
    def __init__(self, db: Session):
        self.db = db

    def inserir_pedido(self, form_data: dict) -> int:
        try:
            # Preparar dados do pedido
            shipped_date = None
            if form_data.get('shippeddate'):
                shipped_date = datetime.strptime(form_data['shippeddate'], '%Y-%m-%d')
            
            freight = None
            if form_data.get('freight'):
                freight = Decimal(form_data['freight'])
            
            shipper_id = None
            if form_data.get('shipperid'):
                shipper_id = int(form_data['shipperid'])
            
            # buscar quantidade de orders e incrementar + 1 no orderid  
            max_orderid = self.db.query(func.max(Orders.orderid)).scalar()
            orderid = (max_orderid or 0) + 1

            
            novo_pedido = Orders(
            orderid=orderid,
            customerid=form_data['customerid'],
            employeeid=int(form_data['employeeid']),
            orderdate=datetime.strptime(form_data['orderdate'], '%Y-%m-%d'),
            requireddate=datetime.strptime(form_data['requireddate'], '%Y-%m-%d'),
            shipname=form_data['shipname'],
            shipaddress=form_data['shipaddress'], 
            shipcity=form_data['shipcity'],
            shipregion=form_data.get('shipregion'),
            shippostalcode=form_data['shippostalcode'],
            shipcountry=form_data['shipcountry'],
            shipperid=int(form_data['shipperid']) if form_data.get('shipperid') else None
            )
            
            self.db.add(novo_pedido)
            self.db.flush()  # Para obter o orderid
            
            # Adicionar itens do pedido
            i = 0
            while f'item_{i}_productid' in form_data:
                order_item = OrderDetails(
                    orderid=novo_pedido.orderid,
                    productid=int(form_data[f'item_{i}_productid']),
                    unitprice=Decimal(form_data[f'item_{i}_unitprice']),
                    quantity=int(form_data[f'item_{i}_quantity']),
                    discount=Decimal(form_data.get(f'item_{i}_discount', '0.0'))
                )
                self.db.add(order_item)
                i += 1
            
            self.db.commit()
            return novo_pedido.orderid
            
        except Exception as e:
            self.db.rollback()
            raise e

    def get_all_clientes(self) -> List[tuple]:
        return self.db.execute("""
            SELECT customerid, contactname 
            FROM northwind.customers 
            ORDER BY contactname
        """).fetchall()

    def get_all_vendedores(self) -> List[tuple]:
        return self.db.execute("""
            SELECT employeeid, CONCAT(firstname, ' ', lastname) AS nome_completo 
            FROM northwind.employees 
            ORDER BY firstname
        """).fetchall()

    def get_all_produtos(self) -> List[tuple]:
        return self.db.execute("""
            SELECT productid, productname, unitprice 
            FROM northwind.products 
            WHERE discontinued = 'N'
            ORDER BY productname
        """).fetchall()

    def get_all_shippers(self) -> List[tuple]:
        return self.db.execute("""
            SELECT shipperid, companyname 
            FROM northwind.shippers 
            ORDER BY companyname
        """).fetchall()