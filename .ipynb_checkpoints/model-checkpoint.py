class Order:
    def __init__(self, orderid, customerid, employeeid, orderdate, shipname=None, shipaddress=None):
        self.orderid = orderid              # int
        self.customerid = customerid        # string (char[5] geralmente)
        self.employeeid = employeeid        # int
        self.orderdate = orderdate          # date
        self.shipname = shipname            # opcional: string
        self.shipaddress = shipaddress      # opcional: string

class OrderDetail:
    def __init__(self, orderid, productid, unitprice, quantity, discount):
        self.orderid = orderid            # int
        self.productid = productid        # int
        self.unitprice = unitprice        # decimal (13,4)
        self.quantity = quantity          # smallint
        self.discount = discount          # decimal (10,4)
class Customer:
    def __init__(self, customerid, companyname):
        self.customerid = customerid  # string (PK)
        self.companyname = companyname  # string (nome da empresa)
class Employee:
    def __init__(self, employeeid, firstname, lastname):
        self.employeeid = employeeid  # int (PK)
        self.firstname = firstname
        self.lastname = lastname