from model.dao.pedidodao import PedidoDAO

class PedidoController:
    def __init__(self, conexao_db):
        self.dao = PedidoDAO(conexao_db)
    
    def criar_pedido(self, form_data, seguro=True):
        try:
            # Preparar dados do formulário
            dados = {
                'customer_name': form_data['customer_name'],
                'employee_name': form_data['employee_name'],
                'order_data': {
                    'orderdate': form_data['orderdate'],
                    'requireddate': form_data['requireddate'],
                    'shipname': form_data['shipname']
                },
                'order_items': self._parse_items(form_data)
            }
            
            if seguro:
                order_id = self.dao.inserir_pedido_seguro(**dados)
            else:
                order_id = self.dao.inserir_pedido_inseguro(**dados)
                
            return True, f"Pedido {order_id} criado com sucesso!", order_id
        except Exception as e:
            return False, f"Erro: {str(e)}", None
    
    def _parse_items(self, form_data):
        items = []
        # Assumindo que os itens vêm como item_0_productid, item_0_quantity, etc.
        i = 0
        while True:
            productid = form_data.get(f'item_{i}_productid')
            if not productid:
                break
            items.append({
                'productid': int(productid),
                'unitprice': float(form_data[f'item_{i}_unitprice']),
                'quantity': int(form_data[f'item_{i}_quantity']),
                'discount': float(form_data[f'item_{i}_discount'])
            })
            i += 1
        return items