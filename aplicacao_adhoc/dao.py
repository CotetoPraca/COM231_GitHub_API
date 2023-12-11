from config import DB_NAME, DB_HOST_ADDRESS, DB_PORT, DB_USER_PASSWORD, DB_USER

from mappings import UserAccount
from mappings import Repository
from mappings import Issue
from mappings import PullRequest
from mappings import GitCommit
from mappings import t_count_data_in_database

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine, select
from sqlalchemy.sql.expression import and_
from socket import timeout

class DAOCrud:
  def __init__(self):
    # Inicializa com os dados de conexão do banco
    self.db_name = DB_NAME
    self.db_user = DB_USER
    self.db_user_password = DB_USER_PASSWORD
    self.db_host = DB_HOST_ADDRESS
    self.db_port = DB_PORT
    
  def authentication(self, db_user, db_user_password):
    try:
      engine = create_engine(f'postgresql://{db_user}:{db_user_password}@{self.db_host}:{self.db_port}/{self.db_name}', echo=True)
      Session = sessionmaker(bind=engine)
      session = Session()
      session.rollback()
      session.close()
      self.db_user = db_user
      self.db_user_password = db_user_password
      return 0
    except OperationalError as e:
      if isinstance(e.orig, timeout):
        return -1  # Timeout de conexão
      elif "password authentication failed" in str(e):
        return -2  # Falha na autenticação da senha
      else:
        return -3  # Outro erro operacional
    
  def get_session(self):
    engine = create_engine(f'postgresql://{self.db_user}:{self.db_user_password}@{self.db_host}:{self.db_port}/{self.db_name}', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
  
  def search_in_database(self, session, info_to_search):
    result = None
    # Obtenha a classe de modelo associada ao nome da tabela
    model_class = globals()[info_to_search["table"]]
    
    if info_to_search["table"] == "t_count_data_in_database":
      # Cria a lista de colunas para a view
      selected_columns = list(t_count_data_in_database.columns)
    
    elif info_to_search["columns"]:
      # Crie um objeto de tabela dinâmico com base no nome da tabela e nas colunas selecionadas
      selected_columns = [getattr(model_class, column) for column in info_to_search["columns"]]
    
    else:
      # Se a lista de colunas estiver vazia, selecione todas as colunas
      selected_columns = [getattr(model_class, column.name) for column in model_class.__table__.columns]
    
    # print("SELECTED COLUMNS", selected_columns)
    query = select(*selected_columns)
    
    if info_to_search["filters"]:
      # Aplica os filtros à consulta
      filters = [getattr(model_class, filter["column"]) == filter["value"] for filter in info_to_search["filters"]]
      query = query.where(and_(*filters))
      
    elif info_to_search["search_option"] == "multi_table":
      pass

    # Execute a consulta
    result = session.execute(query).mappings()
    
    return result