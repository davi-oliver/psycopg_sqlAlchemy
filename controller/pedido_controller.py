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