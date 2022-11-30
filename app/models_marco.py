from app.utils.database_marco import Base
from sqlalchemy import Column,Integer,String,BOOLEAN,TIMESTAMP

class Products_marco(Base):
    """_summary_
       ORM model for products table
    """
    __tablename__= "products"
    product_code = Column(Integer,primary_key=True)
    realtime_acess= Column(String)
    delayed_acess=Column(String)
    created_at=Column(TIMESTAMP)
    updated_at=Column(TIMESTAMP)
    description = Column(String)
    constant = Column(String)
    product_typr=Column(String)
    reviewed =Column(BOOLEAN)
    filtered =Column(BOOLEAN)
    active=Column(BOOLEAN)
    __table_args__ = {'schema': 'dbo'}
    def to_int(obj):
        return obj.product_code
    def to_tuple(obj):
        return (obj.product_code,obj.description)
    def primary_key_ref():
        return 'product_code'