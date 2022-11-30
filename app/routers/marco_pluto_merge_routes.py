from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from app import models_marco
from app.utils.database_marco import get_db as get_marco_db
from app.utils.database import get_db,engine
from app import models
from sqlalchemy import text
import numpy as np


router = APIRouter(
    prefix='/merge',
    tags=['Merge'] # for swagger docs
)

dict_table_models={
    "products":models_marco.Products_marco
}
dict_table_models_pluto={
    "products":models.Products,
    "exchanges":models.Exchanges,
    "field_maps":models.Field_Maps,
    "datafeed_types":models.DataFeed_Fields,
    "datafeed_security_types":models.DataFeed_Security_Types,
    "datafeed_fields":models.DataFeed_Fields
}

@router.get("/{table_name}",status_code=status.HTTP_200_OK)
def get_data(table_name:str,db: Session = Depends(get_marco_db),db_pluto:Session = Depends(get_db)):
    #getting key data as list from marco table
    query_data_of_primary_keys_marco=db.query(dict_table_models[table_name].product_code).from_statement(text(f'select {dict_table_models[table_name].primary_key_ref()} from dbo.{table_name} where active is TRUE')).all()
    #getting key data as list from pluto table
    query_data_of_primary_keys_pluto=db_pluto.query(dict_table_models[table_name].product_code).from_statement(text(f'select {dict_table_models_pluto[table_name].primary_key_ref()} from dbo.{table_name}')).all()
    list_of_primary_keys_marco=[]
    list_of_primary_keys_pluto=[]
    #convert obj into list
    for row in query_data_of_primary_keys_marco:
        list_of_primary_keys_marco.append(dict_table_models[table_name].to_int(row))
     #convert obj into list
    for row in query_data_of_primary_keys_pluto:
        list_of_primary_keys_pluto.append(dict_table_models_pluto[table_name].to_int(row))
    
    
    query_string_for_delete_in_active_data=str(list_of_primary_keys_marco).strip('[]')
    query_string_for_delete_in_active_data=f'({query_string_for_delete_in_active_data})'
    
     
    #delete pluto_table where the oks not in list of marco
    data_test = db_pluto.query(dict_table_models_pluto[table_name]).from_statement(text(f'select * from dbo.{table_name} where {dict_table_models_pluto[table_name].primary_key_ref()} not in {query_string_for_delete_in_active_data} ')).all()
    #getting data ok pks which are there in marco but not pluto
    list_of_primary_keys_to_be_added_pluto= np.setdiff1d(list_of_primary_keys_pluto,list_of_primary_keys_marco)
    
    #convert into tuple
    data_need_to_be_added_pluto=str(list(list_of_primary_keys_to_be_added_pluto)).strip('[]')
    data_need_to_be_added_pluto=f'({data_need_to_be_added_pluto})'
    
    
    list_to_be_added_pluto=[]
    #data to be added to pluto and getting  them from marco
    if(len(list_of_primary_keys_to_be_added_pluto)>1):
        list_to_be_added_pluto=db_pluto.query(dict_table_models[table_name]).from_statement(text(f'select * from dbo.{table_name} where {dict_table_models_pluto[table_name].primary_key_ref()} in {data_need_to_be_added_pluto}'))
    list_of_data_to_be_added=[]


    #list of tuples to be added
    for row in list_to_be_added_pluto:
        list_of_data_to_be_added.append(dict_table_models[table_name].to_tuple(row))
      
    
    #data need to be inserted 
    insert_data_pluto=str(list_of_data_to_be_added).strip('[]')

    if(len(list_of_data_to_be_added)>1):
        sql=(text(f'insert into dbo.products {dict_table_models_pluto[table_name].colums_data()} values {insert_data_pluto}'))
        engine.execute(sql)
    
     
    return "merged sucessfully"



