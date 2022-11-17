from .utils.database import Base
from sqlalchemy import Column,Integer,String
from .utils.config import settings

class Products(Base):
    """_summary_
       ORM model for products table
    """
    __tablename__= "products"
    id = Column(Integer,primary_key=True,nullable=False)
    product_code = Column(Integer)
    description = Column(String)
    __table_args__ = {'schema': settings.database_schema_name}
    def to_string(obj):
        return {"id":obj.id,
        "product_code":obj.product_code,
        "description":obj.description}
    
    
class Exchanges(Base):
    """_summary_
       ORM model for exchanges table
    """
    __tablename__= "exchanges"
    __table_args__ = {'schema': settings.database_schema_name}
    id = Column(Integer,primary_key=True,nullable=False)
    exchange_code=Column(Integer)
    name=Column(String)
    constant=Column(String)
    market_open=Column(Integer)
    market_close=Column(Integer)
    iso_code=Column(String)
    delay_time=Column(String)
    timezone_spec=Column(Integer)
    def to_string(obj):
        return {"id":obj.id,
        "exchange_code":obj.exchange_code,
        "name":obj.name,
        "constant":obj.constant,
        "market_open":obj.market_open,
        "market_close":obj.market_close,
        "iso_code":obj.iso_code,
        "delay_time":obj.delay_time,
        "timezone_spec":obj.timezone_spec}

class Field_Maps(Base):
    """_summary_
       ORM model for field_maps table
    """
    __tablename__= "field_maps"
    __table_args__ = {'schema': settings.database_schema_name}
    id = Column(Integer,primary_key=True,nullable=False)
    field_number=Column(Integer)
    description = Column(String)
    broadcast_name= Column(String)
    def to_string(obj):
        return {"id":obj.id,
        "field_number":obj.field_number,
        "description":obj.description,
        "broadcast_name":obj.broadcast_name}

class DataFeed_Types(Base):
    """_summary_
       ORM model for datafeed_types table
    """
    __tablename__= "datafeed_types"
    __table_args__ = {'schema': settings.database_schema_name}
    id = Column(Integer,primary_key=True,nullable=False)
    name= Column(String)
    def to_string(obj):
        return {"id":obj.id,
        "name":obj.name}

class DataFeed_Security_Types(Base):
    """_summary_
       ORM model for datafeed_security_types table
    """
    __tablename__= "datafeed_security_types"
    __table_args__ = {'schema': settings.database_schema_name}
    id = Column(Integer,primary_key=True,nullable=False)
    security_type=Column(Integer)
    description = Column(String)
    def to_string(obj):
        return {"id":obj.id,
        "security_type":obj.security_type,
        "description":obj.description }

class DataFeed_Fields(Base):
    """_summary_
       ORM model for datafeed_fields table
    """
    __tablename__= "datafeed_fields"
    __table_args__ = {'schema': settings.database_schema_name}
    id = Column(Integer,primary_key=True,nullable=False)
    name=Column(String)
    description = Column(String)
    def to_string(obj):
        return {"id":obj.id,
        "name":obj.name,
        "description":obj.description}


class finan_Statuses:
    """_summary_
       ORM model for datafeed_fields table
    """
    __tablename__= "finan_statuses"
    __table_args__ = {'schema': settings.database_schema_name}
    id = Column(Integer,primary_key=True,nullable=False)
    name=Column(String)
    description = Column(String)
    def to_string(obj):
        return {"id":obj.id,
        "name":obj.name,
        "description":obj.description}