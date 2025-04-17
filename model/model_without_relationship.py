from typing import Optional
import datetime
import decimal


class Categories:
    def __init__(self, categoryid: int, categoryname: Optional[str], description: Optional[str]):
        self.categoryid = categoryid
        self.categoryname = categoryname
        self.description = description


class Customers:
    def __init__(
        self,
        customerid: str,
        companyname: Optional[str],
        contactname: Optional[str],
        contacttitle: Optional[str],
        address: Optional[str],
        city: Optional[str],
        region: Optional[str],
        postalcode: Optional[str],
        country: Optional[str],
        phone: Optional[str],
        fax: Optional[str]
    ):
        self.customerid = customerid
        self.companyname = companyname
        self.contactname = contactname
        self.contacttitle = contacttitle
        self.address = address
        self.city = city
        self.region = region
        self.postalcode = postalcode
        self.country = country
        self.phone = phone
        self.fax = fax


class Employees:
    def __init__(
        self,
        employeeid: int,
        lastname: Optional[str],
        firstname: Optional[str],
        title: Optional[str],
        titleofcourtesy: Optional[str],
        birthdate: Optional[datetime.datetime],
        hiredate: Optional[datetime.datetime],
        address: Optional[str],
        city: Optional[str],
        region: Optional[str],
        postalcode: Optional[str],
        country: Optional[str],
        homephone: Optional[str],
        extension: Optional[str],
        reportsto: Optional[int],
        notes: Optional[str]
    ):
        self.employeeid = employeeid
        self.lastname = lastname
        self.firstname = firstname
        self.title = title
        self.titleofcourtesy = titleofcourtesy
        self.birthdate = birthdate
        self.hiredate = hiredate
        self.address = address
        self.city = city
        self.region = region
        self.postalcode = postalcode
        self.country = country
        self.homephone = homephone
        self.extension = extension
        self.reportsto = reportsto
        self.notes = notes


class Orders:
    def __init__(
        self,
        orderid: int,
        customerid: str,
        employeeid: int,
        orderdate: Optional[datetime.datetime],
        requireddate: Optional[datetime.datetime],
        shippeddate: Optional[datetime.datetime],
        freight: Optional[decimal.Decimal],
        shipname: Optional[str],
        shipaddress: Optional[str],
        shipcity: Optional[str],
        shipregion: Optional[str],
        shippostalcode: Optional[str],
        shipcountry: Optional[str],
        shipperid: Optional[int]
    ):
        self.orderid = orderid
        self.customerid = customerid
        self.employeeid = employeeid
        self.orderdate = orderdate
        self.requireddate = requireddate
        self.shippeddate = shippeddate
        self.freight = freight
        self.shipname = shipname
        self.shipaddress = shipaddress
        self.shipcity = shipcity
        self.shipregion = shipregion
        self.shippostalcode = shippostalcode
        self.shipcountry = shipcountry
        self.shipperid = shipperid


class OrderDetails:
    def __init__(
        self,
        orderid: int,
        productid: int,
        unitprice: Optional[decimal.Decimal],
        quantity: Optional[int],
        discount: Optional[decimal.Decimal]
    ):
        self.orderid = orderid
        self.productid = productid
        self.unitprice = unitprice
        self.quantity = quantity
        self.discount = discount


class Products:
    def __init__(
        self,
        productid: int,
        supplierid: int,
        categoryid: int,
        productname: Optional[str],
        quantityperunit: Optional[str],
        unitprice: Optional[decimal.Decimal],
        unitsinstock: Optional[int],
        unitsonorder: Optional[int],
        reorderlevel: Optional[int],
        discontinued: Optional[str]
    ):
        self.productid = productid
        self.supplierid = supplierid
        self.categoryid = categoryid
        self.productname = productname
        self.quantityperunit = quantityperunit
        self.unitprice = unitprice
        self.unitsinstock = unitsinstock
        self.unitsonorder = unitsonorder
        self.reorderlevel = reorderlevel
        self.discontinued = discontinued


class Shippers:
    def __init__(self, shipperid: int, companyname: Optional[str], phone: Optional[str]):
        self.shipperid = shipperid
        self.companyname = companyname
        self.phone = phone


class Suppliers:
    def __init__(
        self,
        supplierid: int,
        companyname: Optional[str],
        contactname: Optional[str],
        contacttitle: Optional[str],
        address: Optional[str],
        city: Optional[str],
        region: Optional[str],
        postalcode: Optional[str],
        country: Optional[str],
        phone: Optional[str],
        fax: Optional[str],
        homepage: Optional[str]
    ):
        self.supplierid = supplierid
        self.companyname = companyname
        self.contactname = contactname
        self.contacttitle = contacttitle
        self.address = address
        self.city = city
        self.region = region
        self.postalcode = postalcode
        self.country = country
        self.phone = phone
        self.fax = fax
        self.homepage = homepage
