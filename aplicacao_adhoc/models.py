from collections import OrderedDict
from decimal import Decimal

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import ObjectDeletedError
from sqlalchemy.orm.exc import StaleDataError

from dao import DAOCrud

class DatabaseHandler():
  def __init__(self):
    self.dao = DAOCrud()
    
  def validate_credentials(self, db_user, db_user_password):
    auth_result = self.dao.authentication(db_user, db_user_password)
    
    if auth_result == 0:
      return True
    elif auth_result == -1:
      return False  # Timeout de conexão
    elif auth_result == -2:
      return False  # Falha na autenticação da senha
    else:
      return False  # Outro erro operacional
  
  # Função para realizar a conversão do resultado da consulta em um dicionário Python
  def row2dict(self, result, result_dict):
    for row in result:
      entry = OrderedDict((key, value) for key, value in row.items() if key != '_sa_instance_state')
      result_dict.append(entry)
    return result_dict
  
  def search_in_database(self, info_to_search):
    try:
      session = self.dao.get_session()
      session.expire_on_commit = False # Não remover o objeto da aplicação após o commit
      result = self.dao.search_in_database(session, info_to_search)
      
      if result is None:
        return None
      
      # Tratamentos do dado recebido
      # Conversão do resultado em um dicionário Python
      result_dict = []
      if info_to_search["table"] == "t_count_data_in_database":
        # Tratamento especial para a View
        for row in result:
          # Converter Decimal para inteiro
          converted_row = {key: int(value) if isinstance(value, Decimal) else value for key, value in row.items()}
          result_dict.append(converted_row)
      else:
        result_dict = self.row2dict(result, result_dict)
        
      # print(result_dict)
      formatted_data = OrderedDict({"aaData": [], "columns": []})

      # Verifica se há dados em result_dict
      if result_dict:
        # Obtém a ordem das colunas a partir da primeira linha em result_dict
        columns_order = list(result_dict[0].keys())

        # Adiciona as colunas a formatted_data
        formatted_data["columns"] = columns_order

        # Adiciona os dados a formatted_data
        for row in result_dict:
          formatted_data["aaData"].append(list(row.values()))
      
      session.commit()
      session.close()
      
      # json_result = json.dumps(formatted_data, indent=2)
      return formatted_data
    except NoResultFound:
      return None