from fastapi import status,HTTPException,Depends,APIRouter,Response,Query
from .. import models
from ..utils.database import get_db
from sqlalchemy.orm import Session
import pandas as pd
from dict2xml import dict2xml
from xml.dom.minidom import parseString
from typing import Union,List
from sqlalchemy import text
from app.utils.config import settings




router = APIRouter(
    prefix='/meta',
    tags=['Meta'] # for swagger docs
)

#global tables dictonary
dict_table_models={
    "products":models.Products,
    "exchanges":models.Exchanges,
    "field_maps":models.Field_Maps,
    "datafeed_types":models.DataFeed_Fields,
    "datafeed_security_types":models.DataFeed_Security_Types,
    "datafeed_fields":models.DataFeed_Fields
}

def get_data_in_lidt_of_dictonaries(data,table_name:str):
    """_summary_:
          used to convert data in form of refernace to dictonaries

    Args:
        data (_type_): _description_
        table_name (str): _description_

    Returns:
        _type_: return a list of dictonaries
    """
    list_of_row=[]
    for row in data:
        list_of_row.append(dict_table_models[table_name].to_string(row))
    return list_of_row


def get_data_in_xml(list_of_row:list,table_name:str):
    """_summary_
         used to convert list of dictonaries to xml string
    Args:
        list_of_row (list): _description_
        table_name (str): _description_

    Returns:
        _type_: returns xml string
    """
    xml= dict2xml(list_of_row,wrap =table_name[0:-1])
    ans="<"+table_name+">"+xml+"</"+table_name+">"
    return ans

def save_data_as_csv_file(list_of_row:list):
    """_summary_:
         saves list of dictonaries as an csv file
    Args:
        list_of_row (list): _description_

    Returns:
        _type_: save csv file from the data 
    """
    df=pd.DataFrame(list_of_row)
    df.to_csv('file1.csv')
    return "your file have been store sucessfully"

def process_based_on_format(table_name:str,format:str,data):
    """_summary_:
       base on the format it returns the exact data
       json format json data
       xml format xml data
       csv format csv data
    Args:
        table_name (str): _description_
        format (str): _description_
        data (_type_): _description_

    Returns:
        _type_: return data to out based on format
    """
    if(format=="json"):
        return data
    if(format=="xml" or format=="csv"):
        if(format=="xml"):
            ans=get_data_in_xml(get_data_in_lidt_of_dictonaries(data,table_name),table_name)
            return Response(content=ans,media_type="application/xml")
        else:
            return save_data_as_csv_file(get_data_in_lidt_of_dictonaries(data,table_name))

def query_data_with_id(id:str,table_name:str,db:Session):
    """_summary_:
       querys the data base with the list of id present in db or not
       query (select * from table_name where id in list)
    Args:
        id (str): _description_
        table_name (str): _description_
        db (Session): _description_

    Returns:
        _type_: data retrived form database with where clause
    """
    value=','.join([str(i) for i in id])
    select_data=db.query(dict_table_models[table_name]).from_statement(text(f'select * from {settings.database_schema_name}.{table_name} where id in ({value})')).all()
    return select_data

def query_data(table_name:str,db:Session):
    """_summary_

    Args:
        table_name (str): _description_
        db (Session): _description_

    Returns:
        _type_: data retrived form database
    """
    data=db.query(dict_table_models[table_name]).all()
    return data

@router.get("/{table_name}",status_code=status.HTTP_200_OK)
def get_data(table_name:str,format:str = Query(default = "json"),id: Union[List[int], None] = Query(default=None),db: Session = Depends(get_db)):
    """_summary_
          fetches the data from database based on the table name ans
        returns data in the specified format

    Args:
        table_name (str): _description_
        format (str): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: based on format
    """
    table_name=table_name.lower()

    if table_name not in dict_table_models:
        return "table mentioned is not there in the data base please do check the request"

    if id:
        data= query_data_with_id(id,table_name,db)
        return process_based_on_format(table_name,format,data)
    
    data= query_data(table_name,db)
    return process_based_on_format(table_name,format,data)
   

