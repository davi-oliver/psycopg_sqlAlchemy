from typing import Optional, Tuple, List
from model.dao.orm_pedidodao import ORMPedidoDAO

class ORMPedidoController:
    def __init__(self, db):
        self.dao = ORMPedidoDAO(db)
    
    def get_all_clientes(self) -> List[tuple]:
        return self.dao.get_all_clientes()
    
    def get_all_vendedores(self) -> List[tuple]:
        return self.dao.get_all_vendedores()
    
    def get_all_produtos(self) -> List[tuple]:
        return self.dao.get_all_produtos()
    
    def get_all_shippers(self) -> List[tuple]:
        return self.dao.get_all_shippers()
    
    def criar_pedido(self, form_data: dict) -> Tuple[bool, str, Optional[int]]:
        try:
            # Validação básica
            if not form_data.get('customerid') or not form_data.get('employeeid'):
                return False, "Cliente e vendedor são obrigatórios", None
                
            order_id = self.dao.inserir_pedido(form_data)
            return True, f"Pedido {order_id} criado com sucesso via ORM", order_id
            
        except Exception as e:
            return False, f"Erro ao criar pedido: {str(e)}", None