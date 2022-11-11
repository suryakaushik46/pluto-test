from fastapi import status,HTTPException,Depends,APIRouter,Response
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
import pandas as pd
from dict2xml import dict2xml
from xml.dom.minidom import parseString




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




@router.get("/{table_name}",status_code=status.HTTP_200_OK)
async def get_data(table_name:str,format:str,db: Session = Depends(get_db)):
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
    
    data=db.query(dict_table_models[table_name]).all()
    
    if(format=="json"):
        return data
    
    if(format=="xml" or format=="csv"):
         list_of_row=[]
         for row in data:
            list_of_row.append(dict_table_models[table_name].to_string(row))
         if(format=="xml"):
            xml= dict2xml(list_of_row,wrap =table_name[0:-1])
            ans="<"+table_name+">"+xml+"</"+table_name+">"
            return Response(content=ans,media_type="application/xml")
         else:
            df=pd.DataFrame(list_of_row)
            df.to_csv('file1.csv')
            return "your file have been store sucessfully"
    return "wrong format"
   
    
