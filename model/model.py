from typing import Optional
from sqlalchemy import ForeignKey, DateTime, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass

class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        PrimaryKeyConstraint('categoryid', name='categories_pkey'),
        {'schema': 'northwind'}
    )

    categoryid: Mapped[int] = mapped_column(Integer, primary_key=True)
    categoryname: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Relacionamento com produtos
    products: Mapped[list["Products"]] = relationship(back_populates="category")

class Customers(Base):
    __tablename__ = 'customers'
    __table_args__ = (
        PrimaryKeyConstraint('customerid', name='customers_pkey'),
        {'schema': 'northwind'}
    )

    customerid: Mapped[str] = mapped_column(String(5), primary_key=True)
    companyname: Mapped[Optional[str]] = mapped_column(String(50))
    contactname: Mapped[Optional[str]] = mapped_column(String(30))
    contacttitle: Mapped[Optional[str]] = mapped_column(String(30))
    address: Mapped[Optional[str]] = mapped_column(String(50))
    city: Mapped[Optional[str]] = mapped_column(String(20))
    region: Mapped[Optional[str]] = mapped_column(String(15))
    postalcode: Mapped[Optional[str]] = mapped_column(String(9))
    country: Mapped[Optional[str]] = mapped_column(String(15))
    phone: Mapped[Optional[str]] = mapped_column(String(17))
    fax: Mapped[Optional[str]] = mapped_column(String(17))
    
    # Relacionamento com pedidos
    orders: Mapped[list["Orders"]] = relationship(back_populates="customer")

class Employees(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        PrimaryKeyConstraint('employeeid', name='employees_pkey'),
        {'schema': 'northwind'}
    )

    employeeid: Mapped[int] = mapped_column(Integer, primary_key=True)
    lastname: Mapped[Optional[str]] = mapped_column(String(10))
    firstname: Mapped[Optional[str]] = mapped_column(String(10))
    title: Mapped[Optional[str]] = mapped_column(String(25))
    titleofcourtesy: Mapped[Optional[str]] = mapped_column(String(5))
    birthdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    hiredate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    address: Mapped[Optional[str]] = mapped_column(String(50))
    city: Mapped[Optional[str]] = mapped_column(String(20))
    region: Mapped[Optional[str]] = mapped_column(String(2))
    postalcode: Mapped[Optional[str]] = mapped_column(String(9))
    country: Mapped[Optional[str]] = mapped_column(String(15))
    homephone: Mapped[Optional[str]] = mapped_column(String(14))
    extension: Mapped[Optional[str]] = mapped_column(String(4))
    reportsto: Mapped[Optional[int]] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relacionamento com pedidos
    orders: Mapped[list["Orders"]] = relationship(back_populates="employee")

class OrderDetails(Base):
    __tablename__ = 'order_details'
    __table_args__ = (
        PrimaryKeyConstraint('orderid', 'productid', name='order_details_pkey'),
        {'schema': 'northwind'}
    )

    orderid: Mapped[int] = mapped_column(Integer, ForeignKey('northwind.orders.orderid'), primary_key=True)
    productid: Mapped[int] = mapped_column(Integer, ForeignKey('northwind.products.productid'), primary_key=True)
    unitprice: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(13, 4))
    quantity: Mapped[Optional[int]] = mapped_column(SmallInteger)
    discount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 4))
    
    # Relacionamentos
    order: Mapped["Orders"] = relationship(back_populates="details")
    product: Mapped["Products"] = relationship(back_populates="order_details")

class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        PrimaryKeyConstraint('orderid', name='orders_pkey'),
        {'schema': 'northwind'}
    )

    orderid: Mapped[int] = mapped_column(Integer, primary_key=True)
    customerid: Mapped[str] = mapped_column(String(5), ForeignKey('northwind.customers.customerid'))
    employeeid: Mapped[int] = mapped_column(Integer, ForeignKey('northwind.employees.employeeid'))
    orderdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    requireddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    shippeddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    freight: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 4))
    shipname: Mapped[Optional[str]] = mapped_column(String(95))
    shipaddress: Mapped[Optional[str]] = mapped_column(String(50))
    shipcity: Mapped[Optional[str]] = mapped_column(String(15))
    shipregion: Mapped[Optional[str]] = mapped_column(String(15))
    shippostalcode: Mapped[Optional[str]] = mapped_column(String(9))
    shipcountry: Mapped[Optional[str]] = mapped_column(String(15))
    shipperid: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('northwind.shippers.shipperid'))
    
    # Relacionamentos
    customer: Mapped["Customers"] = relationship(back_populates="orders")
    employee: Mapped["Employees"] = relationship(back_populates="orders")
    shipper: Mapped[Optional["Shippers"]] = relationship()
    details: Mapped[list["OrderDetails"]] = relationship(back_populates="order")

class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        PrimaryKeyConstraint('productid', name='products_pkey'),
        {'schema': 'northwind'}
    )

    productid: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplierid: Mapped[int] = mapped_column(Integer, ForeignKey('northwind.suppliers.supplierid'))
    categoryid: Mapped[int] = mapped_column(Integer, ForeignKey('northwind.categories.categoryid'))
    productname: Mapped[Optional[str]] = mapped_column(String(35))
    quantityperunit: Mapped[Optional[str]] = mapped_column(String(20))
    unitprice: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(13, 4))
    unitsinstock: Mapped[Optional[int]] = mapped_column(SmallInteger)
    unitsonorder: Mapped[Optional[int]] = mapped_column(SmallInteger)
    reorderlevel: Mapped[Optional[int]] = mapped_column(SmallInteger)
    discontinued: Mapped[Optional[str]] = mapped_column(String(1))
    
    # Relacionamentos
    supplier: Mapped["Suppliers"] = relationship()
    category: Mapped["Categories"] = relationship(back_populates="products")
    order_details: Mapped[list["OrderDetails"]] = relationship(back_populates="product")

class Shippers(Base):
    __tablename__ = 'shippers'
    __table_args__ = (
        PrimaryKeyConstraint('shipperid', name='shippers_pkey'),
        {'schema': 'northwind'}
    )

    shipperid: Mapped[int] = mapped_column(Integer, primary_key=True)
    companyname: Mapped[Optional[str]] = mapped_column(String(20))
    phone: Mapped[Optional[str]] = mapped_column(String(14))
    
    # Relacionamento com pedidos
    orders: Mapped[list["Orders"]] = relationship(back_populates="shipper")

class Suppliers(Base):
    __tablename__ = 'suppliers'
    __table_args__ = (
        PrimaryKeyConstraint('supplierid', name='supplier_pk'),
        {'schema': 'northwind'}
    )

    supplierid: Mapped[int] = mapped_column(Integer, primary_key=True)
    companyname: Mapped[Optional[str]] = mapped_column(String(50))
    contactname: Mapped[Optional[str]] = mapped_column(String(30))
    contacttitle: Mapped[Optional[str]] = mapped_column(String(30))
    address: Mapped[Optional[str]] = mapped_column(String(50))
    city: Mapped[Optional[str]] = mapped_column(String(20))
    region: Mapped[Optional[str]] = mapped_column(String(15))
    postalcode: Mapped[Optional[str]] = mapped_column(String(8))
    country: Mapped[Optional[str]] = mapped_column(String(15))
    phone: Mapped[Optional[str]] = mapped_column(String(15))
    fax: Mapped[Optional[str]] = mapped_column(String(15))
    homepage: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Relacionamento com produtos
    products: Mapped[list["Products"]] = relationship(back_populates="supplier")