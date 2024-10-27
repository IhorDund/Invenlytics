from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ean = Column(Integer)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    product = relationship("Product", back_populates="purchases")


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    sale_price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    product = relationship("Product", back_populates="sales")

# class Return(Base):
#     __tablename__ = 'returns'
#
#     id = Column(Integer, primary_key=True)
#     product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
#     quantity = Column(Integer, nullable=False)
#     return_price = Column(Float, nullable=False)
#     date = Column(Date, nullable=False)
#     return_to_stock = Column(String, nullable=False)
#
#     product = relationship("Product", back_populates='returns')

# Product.returns = relationship("Return", order_by=Return.id, back_populates="product")
Product.purchases = relationship("Purchase", order_by=Purchase.id, back_populates="product")
Product.sales = relationship("Sale", order_by=Sale.id, back_populates="product")
